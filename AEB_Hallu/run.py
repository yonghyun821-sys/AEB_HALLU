"""Portable entry point. Default/check/test/replay never make API requests."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib
import importlib.metadata
import json
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path, PurePosixPath
from unittest.mock import patch

BUNDLE = Path(__file__).resolve().parent
WORKSPACE = BUNDLE / '.workspace'
REFERENCE_WORK = BUNDLE / '.reference_work'
EXPERIMENT = 'experiments/hallu_errorbench_taxonomy'


def digest_file(path):
    result=hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b''):result.update(chunk)
    return result.hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def checked_path(root,name):
    relative=PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or '\\' in name or ':' in name:
        raise ValueError('Unsafe bundle member: '+name)
    target=root.joinpath(*relative.parts)
    if not target.resolve().is_relative_to(root.resolve()):raise ValueError('Bundle member escapes its destination')
    return target


def verify_bundle():
    manifest=read_json(BUNDLE/'bundle_manifest.json')
    required={'run.py','requirements.txt','assets/frozen_experiment.zip','reference/completed_run.zip'}
    if not required<=manifest['bundle_files_sha256'].keys():raise ValueError('Bundle manifest is incomplete')
    for name,expected in manifest['bundle_files_sha256'].items():
        path=checked_path(BUNDLE,name)
        if not path.is_file() or digest_file(path)!=expected:raise ValueError('Bundle file missing/changed: '+name)
    return manifest


def unpack(archive,destination,expected):
    if not destination.resolve().is_relative_to(BUNDLE.resolve()):raise ValueError('Extraction destination is outside this folder')
    with zipfile.ZipFile(archive) as zipped:
        names=[i.filename for i in zipped.infolist() if not i.is_dir()]
        if len(names)!=len(set(names)) or set(names)!=set(expected):raise ValueError('Archive membership differs from manifest')
        for name in names:
            target=checked_path(destination,name)
            if target.exists():
                if digest_file(target)!=expected[name]:raise ValueError('Extracted file changed; refusing to overwrite: '+str(target))
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            temporary=None
            try:
                with tempfile.NamedTemporaryFile('wb',dir=target.parent,delete=False) as handle:
                    temporary=Path(handle.name)
                    with zipped.open(name) as source:shutil.copyfileobj(source,handle)
                if digest_file(temporary)!=expected[name]:raise ValueError('Archive member checksum failed: '+name)
                os.replace(temporary,target);temporary=None
            finally:
                if temporary is not None:temporary.unlink(missing_ok=True)


def bootstrap(manifest):
    if sys.version_info<(3,11):raise ValueError('Python 3.11 or newer is required; Python 3.11 is recommended')
    unpack(BUNDLE/'assets/frozen_experiment.zip',WORKSPACE,manifest['payload_files_sha256'])
    sys.path[:0]=[str(WORKSPACE/'src'),str(WORKSPACE)]
    try:
        module=importlib.import_module('experiments.hallu_errorbench_taxonomy.runner')
    except ModuleNotFoundError as exc:
        raise ValueError('Dependency missing: '+str(exc.name)+'. Install requirements.txt in your virtual environment.') from None
    for name,loaded in tuple(sys.modules.items()):
        if name=='experiments' or name.startswith(('experiments.','taxonomy_experiment')):
            file=getattr(loaded,'__file__',None)
            if file and not Path(file).resolve().is_relative_to(WORKSPACE.resolve()):
                raise ValueError('A project import came from outside this bundle: '+name)
    return module


@contextlib.contextmanager
def offline_only():
    def denied(*args,**kwargs):raise RuntimeError('Network disabled for this offline command')
    with patch('socket.socket.connect',denied),patch('socket.create_connection',denied):yield


def load_local_env():
    from taxonomy_experiment.config import _load_project_dotenv
    _load_project_dotenv(BUNDLE)


def check(manifest,runner):
    load_local_env()
    result=runner.preflight()
    result.update(bundle_directory=str(BUNDLE),self_contained=True,
        reference_run=manifest['reference']['identity_sha256'],
        dependency_versions={name:importlib.metadata.version(name) for name in manifest['original_inference_versions']},
        original_inference_versions=manifest['original_inference_versions'])
    return result


def replay(manifest,runner):
    """Reparse frozen raw responses and repeat the original scoring, at no cost."""
    from taxonomy_experiment.io import write_json
    from experiments.taxonomy_contrastive_attribution.runtime import load_rows
    from experiments.hallu_errorbench_taxonomy.design import messages,guide_for,parse,sha,canonical
    from experiments.taxonomy_contrastive_attribution.prepare import sha as request_sha
    from experiments.hallu_errorbench_taxonomy.results import summarize
    from experiments.hallu_errorbench_taxonomy.runtime import Ledger,client_config

    unpack(BUNDLE/'reference/completed_run.zip',REFERENCE_WORK,manifest['reference_files_sha256'])
    plan,data,tasks,_=runner.snapshot();lookup={r['case_id']:r for r in data}
    prepared=WORKSPACE/EXPERIMENT/'prepared'
    guides={name:(prepared/'guidance'/(name+'.txt')).read_text(encoding='utf-8') for name in ('agenthallu','agenterrorbench','merged')}
    saved=load_rows(REFERENCE_WORK/'predictions.jsonl');rows={}
    allowed={(t['case_id'],t['arm']):t for t in tasks};request_settings=client_config(plan)['request']
    for row in saved:
        key=(row['case_id'],row['arm'])
        if key not in allowed or key in rows:raise ValueError('Unexpected/duplicate reference prediction')
        record=lookup[row['case_id']];prompt=messages(record,guide_for(record['dataset'],row['arm'],guides))
        if row['prompt_sha256']!=sha(canonical(prompt)) or row['prompt_sha256']!=allowed[key]['prompt_sha256']:
            raise ValueError('Reference prompt differs from the frozen experiment')
        cached=read_json(REFERENCE_WORK/'cache'/(row['cache_key']+'.json'))
        if request_sha(cached['request'])!=row['cache_key'] or cached['request']!={**request_settings,'messages':prompt}:
            raise ValueError('Reference request differs from the frozen settings')
        raw=cached['raw_response'];prediction=None;valid=False
        try:
            choice=raw['choices'][0]
            if choice.get('finish_reason')!='stop':raise ValueError('Non-stop response')
            prediction=parse(json.loads(choice['message'].get('content') or ''),record);valid=True
        except (ValueError,TypeError,KeyError,IndexError):pass
        if valid!=row['json_valid'] or prediction!=row['prediction']:
            raise ValueError('Raw-response parsing does not reproduce original prediction')
        rows[key]={**row,'prediction':prediction,'json_valid':valid}
    if set(rows)!=set(allowed):raise ValueError('Reference predictions are incomplete')
    ledger=Ledger(REFERENCE_WORK/'ledger.jsonl',plan['budget']['hard_cap_usd'])
    if ledger.summary()['holds']:raise ValueError('Reference billing has unresolved reservations')
    output=BUNDLE/'reproduced_results';output.mkdir(exist_ok=True)
    report=summarize(plan,data,load_rows(prepared/'gold.jsonl'),rows,output,ledger)
    original=read_json(REFERENCE_WORK/'RESULTS.json')
    if report!=original:raise ValueError('Reproduced scientific results differ from the original report')
    unique={row['cache_key']:row for row in saved}
    usage={'logical_predictions':len(saved),'unique_responses':len(unique),
        'prompt_tokens':sum(r['usage'].get('prompt_tokens',0) for r in unique.values()),
        'completion_tokens':sum(r['usage'].get('completion_tokens',0) for r in unique.values()),
        'cached_tokens':sum((r['usage'].get('prompt_tokens_details') or {}).get('cached_tokens',0) for r in unique.values()),
        'historical_billed_usd':ledger.summary()['billed'],'new_paid_calls':0,
        'note':'Original resource_summary sums prediction rows and counts four shared cached responses twice. These are deduplicated totals.'}
    write_json(output/'resource_summary_unique.json',usage)
    return {'status':'OFFLINE_REPLAY_COMPLETE','results_identical_to_reference':True,
        'raw_responses_reparsed':len(unique),'logical_predictions':len(rows),'new_paid_calls':0,
        'historical_billed_usd':ledger.summary()['billed'],'result_file':str(output/'RESULTS_KO.md')}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    actions=parser.add_mutually_exclusive_group()
    for flag in ('check','run','replay','test','verify'):actions.add_argument('--'+flag,action='store_true')
    args=parser.parse_args()
    try:
        manifest=verify_bundle()
        if args.verify:
            print(json.dumps({'status':'BUNDLE_INTEGRITY_OK','bundle_files':len(manifest['bundle_files_sha256']),
                'frozen_files':len(manifest['payload_files_sha256']),'paid_calls':0},indent=2));return 0
        with contextlib.nullcontext() if args.run else offline_only():
            runner=bootstrap(manifest)
            if args.test:
                suite=unittest.defaultTestLoader.loadTestsFromName('experiments.hallu_errorbench_taxonomy.test_study')
                result=unittest.TextTestRunner(verbosity=2).run(suite)
                print('Offline test run; network disabled; paid calls: 0',flush=True)
                return 0 if result.wasSuccessful() else 1
            if args.replay:result=replay(manifest,runner)
            elif args.run:
                load_local_env()
                print('Starting/resuming a NEW paid study, hard cap $8. Reference results are archived separately.',flush=True)
                result=runner.run()
            else:result=check(manifest,runner)
        print(json.dumps(result,ensure_ascii=False,indent=2),flush=True);return 0
    except KeyboardInterrupt:
        print('Interrupted. Saved work is retained; resume with the same command.',flush=True);return 130
    except Exception as exc:
        print(json.dumps({'status':'STOPPED','reason':str(exc)},ensure_ascii=False,indent=2),flush=True);return 2


if __name__=='__main__':raise SystemExit(main())

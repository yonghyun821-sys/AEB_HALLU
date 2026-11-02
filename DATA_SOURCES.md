# Data and code provenance

This folder reproduces an existing experiment; it does not collect a new dataset.

## Included snapshot

- Original study identity: `916d5a7acda0b330eaf6506452fd9b046d158a41a5d8f65d078bc9d6aa2de096`.
- All 453 files listed in the original `identity.json` are preserved byte for byte inside `assets/frozen_experiment.zip`.
- Those files include the prepared 411 inputs, separate gold, 1,644-request manifest, guidance, provenance, protocol, selected raw records, and the upstream prepared sources needed by the original integrity checks.
- Additional local Python modules and package initializers required by transitive imports are included. Their individual origin and hash are recorded in `bundle_manifest.json`. These supplemental modules were not listed in the original run identity; they are not presented as part of that original frozen-file list.
- The original 15 offline tests are included. The portable `run.py` only adds extraction, dependency bootstrapping and offline replay; the frozen experiment code is not rewritten.
- The completed reference response cache, predictions, ledger and reports are in `reference/completed_run.zip`. The original absolute paths in archived historical status files are provenance only; the portable launcher resolves its own location.

## Original data sources

| Source | Upstream reference | Included experimental use |
|---|---|---|
| AgentHallu | https://github.com/liuxuannan/AgentHallu ; https://arxiv.org/html/2601.06818v1 | Existing 240-positive-trajectory research subset; 14 source definitions |
| AgentErrorBench / AgentDebug | https://arxiv.org/abs/2509.25370 | Existing audited 171-trajectory subset; 17 canonical definitions |

The AgentHallu source audit pins commit `9ffe8bc888feaf15d89833f4b0e3c4697f44acc1`. Per-file source checksums and exclusions are preserved in the prepared source audit. AgentErrorBench uses the original local label files and raw trajectories already used in the completed study; per-file hashes are preserved rather than claiming a new upstream revision.

The original records and third-party material remain subject to their upstream terms. The available AgentDebug license is copied to `licenses/AgentDebug-LICENSE`. No new blanket license for third-party datasets is asserted. The locally available AgentHallu source export did not include a standalone license file.

## Credentials and generated files

No project `.env`, service API key, original virtual environment, Hugging Face cache, Git metadata, or editor configuration is included. `requirements.txt` pins the 24 distributions used by the packaged code and their base dependencies in the original environment. An installation needs access to Python packages; replay does not need network access or an API key.

The reference results were produced earlier. Export, installation verification and offline replay create no new billable model calls. Fresh remote API inference is enabled only by `--run`.

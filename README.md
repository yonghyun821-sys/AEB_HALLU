# AEB–Hallu 독립 실행 패키지

**이 폴더만 Git으로 받아서 설치·실행할 수 있습니다.** 상위 `taxonomy-v2` 프로젝트나 원래 컴퓨터의 데이터 경로는 필요하지 않습니다.

포함한 실험은 완료된 **Hallu 240개 + AgentErrorBench 171개, 네 조건의 All-at-Once 실험**입니다. DSQA 실험이나 새 What 실험으로 바꾸지 않았습니다.

## 1. 다른 Windows 컴퓨터에서 설치

Python **3.11**을 권장합니다. 받은 `AEB_Hallu` 폴더에서 PowerShell 터미널을 열고 실행합니다. 가상환경을 activate할 필요는 없습니다.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -u run.py --check
```

`OFFLINE_READY`, Hallu 240, AEB 171, planned_calls 1644가 나오면 오프라인 준비가 된 것입니다. 이 명령은 API를 호출하지 않습니다. API 키 없이도 실행할 수 있습니다. 최초 실행 시 포함된 고정 파일을 `.workspace/`에 자동으로 풀며, 외부에서 데이터셋을 다운로드하지 않습니다.

## 2. 기존 결과를 무료로 재현

```powershell
.\.venv\Scripts\python.exe -u run.py --replay
```

저장된 원본 응답 1,640개를 다시 파싱하고, 1,644개 예측의 채점을 다시 계산해 원래 `RESULTS.json`과 같은지 확인합니다. **새 API 호출·추가 청구가 없고 API 키도 필요하지 않습니다.** 네트워크 연결은 이 명령에서 차단됩니다.

결과는 `reproduced_results/RESULTS_KO.md`에 생성됩니다. 이미 완료된 결과만 읽으려면 [기존 결과](reference/RESULTS_KO.md)를 열면 됩니다. [자세한 해석](reference/INTERPRETATION_KO.md)도 포함했습니다.

## 3. 같은 설정으로 새 유료 실험 시작

먼저 자신의 OpenRouter workspace API 키를 이 폴더의 `.env`에 넣습니다. 원래 컴퓨터의 키는 복사하지 않았습니다.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
notepad .env
```

`.env`의 내용:

```dotenv
OPENROUTER_API_KEY=본인의_OpenRouter_workspace_API_키
```

저장한 다음 실행합니다.

```powershell
.\.venv\Scripts\python.exe -u run.py --run
```

**`--run`만 유료 호출을 합니다.** 목표 $5, 새 실행 전체 상한 $8입니다. 이전 실험의 $3.1264는 참고 기록이며 새 실행의 장부에 합산하지 않습니다. 모델은 Gemini 2.5 Flash, thinking off, 출력 상한 512, 동시 요청 2개로 고정돼 있습니다. Google AI Studio standard 및 workspace-credit 청구를 확인하며 공급 경로를 임의로 바꾸지 않습니다.

30초마다 데이터셋별·조건별 진행, 토큰, 청구/예약액, 경과 시간과 ETA를 출력합니다. 중단됐다면 **같은 명령을 다시 실행**하면 이어집니다. 재개할 때 `.workspace/`를 보존해야 장부·원본 응답·완료 지점이 유지됩니다.

새 실행 결과 경로는 완료 시 터미널에 출력됩니다. 위치 기록은 다음 파일입니다.

```text
.workspace/experiments/hallu_errorbench_taxonomy/artifacts/active_run.json
```

새 API 실행은 같은 데이터·프롬프트·설정을 사용합니다. 공급자 가용성·캐시 할인·모델 응답이 달라질 수 있으므로 기존 정확도나 청구액이 똑같이 나오는 것은 보장하지 않습니다. 과거 결과의 정확한 재채점은 `--replay`로 확인합니다.

## 4. 추가 오프라인 확인

```powershell
# 설치 전에도 가능: 압축 파일과 배포 파일의 SHA-256 확인
py -3.11 run.py --verify

# 설치 후: 원본 오프라인 테스트 15개 실행
.\.venv\Scripts\python.exe -u run.py --test
```

`--verify`, `--check`, `--test`, `--replay`는 새 모델 응답을 생성하지 않습니다. 설치 자체에는 Python 패키지 다운로드를 위한 인터넷이 필요합니다.

## 5. 폴더 구성

```text
AEB_Hallu/
  run.py                         독립 실행 진입점
  requirements.txt               원래 실행 환경의 패키지 버전 고정
  .env.example                   API 키 설정 양식
  .gitignore / .gitattributes     비밀키·실행파일 제외, 압축 데이터 보존
  bundle_manifest.json           전체 파일 해시 및 원본 실행 정보
  EXPERIMENT_SUMMARY_KO.md        실험 내용 요약
  DATA_SOURCES.md                데이터 출처와 보존 범위
  VALIDATION.json                패키지 검증 기록
  assets/frozen_experiment.zip   고정 코드·표본·정답·taxonomy·원본 자료
  reference/
    RESULTS_KO.md                완료된 기존 결과
    RESULTS.json                 완료된 기존 수치
    INTERPRETATION_KO.md          기존 결과 해석
    POSTHOC_CAUSE_AUDIT.json      사후 데이터 검사
    original_identity.json       원본 453개 파일의 해시·환경
    completed_run.zip            원본 응답·예측·장부·보고서
```

실행하면 `.workspace/`, `.reference_work/`, `reproduced_results/`가 생성됩니다. 이 폴더들과 `.venv/`, `.env`는 Git에서 제외됩니다. `.workspace/` 안에서 실제 실험 코드와 데이터를 읽을 수 있습니다. 고정 파일이 변경되면 무결성 검사가 중단하므로 기존 실행 중에 수정하지 않습니다.

원본 고정 파일은 압축 내부에서 바이트 단위로 보존했습니다. Git의 줄바꿈 변환으로 데이터·프롬프트 해시가 바뀌지 않도록 압축 파일은 binary로 취급합니다. 개별 압축 파일은 100MB보다 작아 Git LFS 없이 올릴 수 있는 크기입니다. **`assets/`와 `reference/completed_run.zip`도 반드시 함께 Git에 올려야 합니다.**

폴더 전체를 독립 저장소로 올리거나 기존 저장소 안의 `AEB_Hallu/`로 올려도 됩니다. 원격 저장소 생성·업로드는 이 패키지를 만드는 과정에서 수행하지 않았습니다.

## 6. Linux/macOS 설치 명령

```bash
# 받은 AEB_Hallu 폴더에서 실행
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run.py --check
.venv/bin/python run.py --replay
```

새 유료 실험은 `.env.example`을 `.env`로 복사해 키를 입력한 뒤 `.venv/bin/python -u run.py --run`으로 시작합니다. 패키지는 운영체제별 사용자 경로를 사용하지 않습니다. 실제 검증은 Windows/Python 3.11에서 수행했고 Linux/macOS의 실측 검증은 하지 않았습니다.

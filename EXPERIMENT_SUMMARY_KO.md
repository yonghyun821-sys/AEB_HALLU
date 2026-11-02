# 복사한 실험의 범위

이 패키지는 완료된 `run-916d5a7acda0b330`을 재현하기 위한 것입니다. 데이터·병합·채점 방식을 새로 설계하지 않았습니다.

| 항목 | 설정 |
|---|---|
| 데이터 | AgentHallu 240개 + AgentErrorBench 171개 |
| 조건 | no_label / own / foreign / merged |
| 호출 단위 | 전체 기록을 한 번에 읽는 All-at-Once |
| 논리적 예측 수 | 411 × 4 = 1,644 |
| 모델 | `google/gemini-2.5-flash`, temperature 0, thinking off |
| 처리 | 두 기록 병렬, 한 기록의 네 조건 순차 |
| 새 실행 예산 | 목표 $5, 상한 $8, 재개 시 같은 장부 유지 |

Hallu의 Own은 Hallu taxonomy, Foreign은 AgentError taxonomy입니다. AEB에서는 반대로 적용합니다. Merged는 Hallu 14개와 AgentError 17개 원본 정의를 보존하고 구별 관계 지침 9개를 붙인 동일한 텍스트입니다.

When은 Hallu의 최초 환각 유입 단계와 AEB의 원본 critical failure 단계를 각각 정확 일치로 채점합니다. AEB는 책임 모듈을 보조 지표로 평가합니다. Hallu는 해당 기준에 맞는 59개 기록의 유도 발화자 지표를 보고하며 독립적인 책임 Who 정답으로 해석하지 않습니다. What 및 joint 정확도는 계산하지 않습니다.

AEB의 같은 과제 반복 실행은 질문 그룹 단위로 묶어 통계를 계산합니다. 두 데이터셋의 Own−Foreign, Merged−Own 총 네 When 비교에 Holm 보정을 적용합니다. 저성능을 이유로 일부 답만 재생성하지 않습니다.

## 기존 완료 결과

| 데이터셋 | No label When | Own When | Foreign When | Merged When |
|---|---:|---:|---:|---:|
| Hallu | 38.33% | 41.25% | 39.17% | 42.08% |
| AEB | 16.96% | 15.79% | 15.20% | 16.37% |

주요 네 비교에서 유의한 우위는 확인되지 않았습니다. 실행은 약 19분 56초, 기존 청구액은 $3.12639172였습니다. 새 실행의 시간·비용·정확도가 동일하게 나올 것을 보장하는 수치는 아닙니다.

고유 원본 응답은 1,640개입니다. 완전히 같은 요청 4개는 당시 실행 내부 캐시를 재사용해 1,644개 예측에 반영했습니다. 재현 스크립트는 원본 응답을 다시 파싱하고 원래 전체 결과 JSON과 비교합니다.

기존 `resource_summary.json`은 예측 행 기준 집계여서 캐시 재사용 4건의 토큰을 중복 합산합니다. 원본은 보존하고, 재현 시 `resource_summary_unique.json`에 고유 응답 기준 토큰을 추가로 저장합니다.

로컬 AEB에는 원본 기록이 같은데 정답 단계·모듈이 다른 한 쌍이 확인돼 있습니다. 이 패키지는 원래 실험 재현을 위해 해당 표본도 그대로 유지했습니다. 사후 검사는 [POSTHOC_CAUSE_AUDIT.json](reference/POSTHOC_CAUSE_AUDIT.json)에 있습니다. 기존 표본을 사용한 탐색적 연구이며 Merged와 단순 Union의 효과를 분리한 실험은 아닙니다.

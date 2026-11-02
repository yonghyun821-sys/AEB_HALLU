# Hallu–AgentErrorBench taxonomy attribution results

두 데이터셋의 native When을 각각 채점했습니다. What·joint 정확도는 계산하지 않았습니다.

| 데이터셋 | 조건 | When | 보조 지표 | JSON 오류 |
|---|---|---:|---:|---:|
| agenthallu | no_label | 38.33% (92/240) | 72.88% (43/59) | 1 |
| agenthallu | own | 41.25% (99/240) | 71.19% (42/59) | 0 |
| agenthallu | foreign | 39.17% (94/240) | 76.27% (45/59) | 0 |
| agenthallu | merged | 42.08% (101/240) | 76.27% (45/59) | 0 |
| agenterrorbench | no_label | 16.96% (29/171) | 18.13% (31/171) | 0 |
| agenterrorbench | own | 15.79% (27/171) | 23.39% (40/171) | 0 |
| agenterrorbench | foreign | 15.20% (26/171) | 22.81% (39/171) | 0 |
| agenterrorbench | merged | 16.37% (28/171) | 28.65% (49/171) | 0 |

Hallu 보조 지표는 정답 단계의 발화자에서 유도한 값이며 독립적인 책임 Who 정답이 아닙니다. AEB 보조 지표는 원본 책임 모듈 정답입니다. 서로 합산하지 않습니다.

주요 비교: 같은 과제를 묶은 paired cluster bootstrap CI 및 sign-flip 검정, 네 비교 전체에 Holm 보정.

- agenthallu / own - foreign: +2.08pp; 95% CI [-2.08, +6.25]; 개선 16, 악화 11; Holm p=1.
- agenthallu / merged - own: +0.83pp; 95% CI [-2.50, +4.17]; 개선 10, 악화 8; Holm p=1.
- agenterrorbench / own - foreign: +0.58pp; 95% CI [-2.89, +4.05]; 개선 5, 악화 4; Holm p=1.
- agenterrorbench / merged - own: +0.58pp; 95% CI [-2.86, +4.05]; 개선 5, 악화 4; Holm p=1.

새 실험 청구액: $3.1264 / $8. 이전 실험 비용은 이 한도에 포함하지 않습니다.

기존 실험에서 노출된 표본을 사용한 탐색적 결과입니다. Merged−Own 차이는 정의 추가와 관계 지침 전체의 효과이며, 단순 union 대비 병합 관계만의 효과는 분리하지 못합니다.

| 데이터셋 | 프레임워크/환경 | 조건 | N | When |
|---|---|---|---:|---:|
| agenthallu | BFCL | no_label | 57 | 22.81% |
| agenthallu | BFCL | own | 57 | 24.56% |
| agenthallu | BFCL | foreign | 57 | 26.32% |
| agenthallu | BFCL | merged | 57 | 26.32% |
| agenthallu | Camel | no_label | 31 | 48.39% |
| agenthallu | Camel | own | 31 | 58.06% |
| agenthallu | Camel | foreign | 31 | 48.39% |
| agenthallu | Camel | merged | 31 | 54.84% |
| agenthallu | Magentic_One | no_label | 29 | 41.38% |
| agenthallu | Magentic_One | own | 29 | 41.38% |
| agenthallu | Magentic_One | foreign | 29 | 51.72% |
| agenthallu | Magentic_One | merged | 29 | 41.38% |
| agenthallu | Octotools | no_label | 15 | 33.33% |
| agenthallu | Octotools | own | 15 | 33.33% |
| agenthallu | Octotools | foreign | 15 | 40.00% |
| agenthallu | Octotools | merged | 15 | 40.00% |
| agenthallu | OpenDeepSearch | no_label | 31 | 45.16% |
| agenthallu | OpenDeepSearch | own | 31 | 48.39% |
| agenthallu | OpenDeepSearch | foreign | 31 | 41.94% |
| agenthallu | OpenDeepSearch | merged | 31 | 54.84% |
| agenthallu | OpenManus | no_label | 46 | 39.13% |
| agenthallu | OpenManus | own | 46 | 43.48% |
| agenthallu | OpenManus | foreign | 46 | 36.96% |
| agenthallu | OpenManus | merged | 46 | 41.30% |
| agenthallu | SmolAgents | no_label | 31 | 48.39% |
| agenthallu | SmolAgents | own | 31 | 48.39% |
| agenthallu | SmolAgents | foreign | 31 | 41.94% |
| agenthallu | SmolAgents | merged | 31 | 48.39% |

agenthallu 위치 기준선: first=54/240, last=14/240, penultimate=71/240.

| agenterrorbench | alfworld | no_label | 73 | 10.96% |
| agenterrorbench | alfworld | own | 73 | 10.96% |
| agenterrorbench | alfworld | foreign | 73 | 9.59% |
| agenterrorbench | alfworld | merged | 73 | 9.59% |
| agenterrorbench | gaia | no_label | 49 | 24.49% |
| agenterrorbench | gaia | own | 49 | 22.45% |
| agenterrorbench | gaia | foreign | 49 | 22.45% |
| agenterrorbench | gaia | merged | 49 | 26.53% |
| agenterrorbench | webshop | no_label | 49 | 18.37% |
| agenterrorbench | webshop | own | 49 | 16.33% |
| agenterrorbench | webshop | foreign | 49 | 16.33% |
| agenterrorbench | webshop | merged | 49 | 16.33% |

agenterrorbench 위치 기준선: first=17/171, last=27/171, penultimate=9/171.

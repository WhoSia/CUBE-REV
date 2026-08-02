# CUBE-REV 0.8.6 — Opaque Stimulus Blinding, Resume-complete Telemetry & Demand-firewall Post-task Capture

## 공식 판정
`PASS-BLINDING-AND-TELEMETRY-CERTIFIED / LIVE-COLLECTOR-SMOKE-PENDING`

0.8.5의 공개 bank에서 연구 가설을 역추론할 수 있던 P4/P6, pair/member, distance, branch metadata를 제거했다. participant bundle은 `CR086-S001` 형식의 opaque stimulus ID만 보유하며, 분석 crosswalk는 로컬 연구 묶음의 `private_analysis/`에 분리하고 공개 branch에는 포함하지 않는다.

중단·재개, visibility, pagehide, 응답 기록, post-task 저장, 제출 시도·실패·확정 이벤트를 local resume state와 함께 보존한다. 28개 응답 뒤 과제 추측·확신도·의도적 전략 변경·기술 메모를 받아 demand-awareness firewall을 복원한다.

Collector 파일은 수정하지 않으며 health/POST 계약은 0.7.12, exported app JSON은 0.8.6으로 분리한다.

## 한계
이 blinding은 참가자 UI와 공개 metadata에 대한 실용적 blinding이다. 공개 bank에는 렌더링과 정규화에 필요한 `state_id`, `rotation_id`, `face_map`이 남으므로, 원본 연구 bank를 별도로 가진 고급 분석자가 대응관계를 재구성하는 것을 암호학적으로 차단하지는 않는다. 실제 참가자 대상 live collector smoke test와 production default-entry cutover는 아직 수행하지 않았다.

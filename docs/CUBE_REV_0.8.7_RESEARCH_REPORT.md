# CUBE-REV 0.8.7 — Collector Shadow-submit Harness, Receipt-loss Recovery & Default-entry Cutover Gate

## 공식 판정
`PASS-SHADOW-CONTRACT / HOLD-RECEIPT-LOSS-SEMANTICS / DEFAULT-CUTOVER-NO_GO`

0.8.5–0.8.6 participant route가 사용하는 기존 `CubeRevCollectorClient.submit()`의 상태 전이를 독립 shadow model로 재현했다. 정상 stored, 현재 payload checksum을 반환하는 duplicate, checksum mismatch 거부, 잘못된 collector health의 POST 차단, 동시 호출의 단일 POST 수렴은 통과했다.

## 새로 확인한 복구 경계
첫 POST가 서버에는 저장되었지만 receipt만 소실되면 다음 제출에서는 `attempt_count`, `last_attempt_at`, collector health, nonce 등 `data_submission` 상태가 바뀐 JSON을 다시 직렬화하므로 checksum도 달라질 수 있다.

- 서버 duplicate receipt가 **재시도 payload의 현재 checksum**을 반환하는 정책이면 복구된다.
- 서버 duplicate receipt가 **처음 저장된 파일의 원래 checksum**을 반환하는 정책이면 현재 client는 `CHECKSUM_MISMATCH`로 복구를 거부한다.

이는 실제 서버 정책을 확인하기 전까지 제거할 수 없는 계약 의존성이다. 무결성 거부 자체는 올바르지만, receipt-loss recovery의 의미론은 아직 닫히지 않았다.

## 산출물
- Node에서 실행된 submit shadow model과 7개 시나리오
- 실제 repository collector client를 로드하도록 만든 브라우저 shadow harness
- production default-entry cutover gate

## Cutover 판정
`NO_GO`. collector 코드는 수정하지 않았고, live collector/browser smoke와 exact `index.html` default-entry patch가 없으며, duplicate checksum 정책도 미확인이다.

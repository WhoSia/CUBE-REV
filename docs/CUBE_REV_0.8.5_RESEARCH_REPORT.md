# CUBE-REV 0.8.5 — Participant-facing Cognitive Mode Integration, Legacy Fixed-set Retirement & Resume-safe UX Certification

## 공식 판정
`PASS-MODULE-CERTIFIED / DEFAULT-INDEX-INTEGRATION-PENDING`

참가자용 인지 모드가 독립 route로 구현되었다. 연구용 N, probe 명칭, 고정 세트/무작위 선택기는 참가자 화면에서 제거했고, 24개 counterbalance sequence는 익명 토큰의 안정 해시로 자동 배정한다. 새로고침 뒤에도 동일 session, sequence, cursor와 응답이 복구되며 손상 상태는 격리한다. 완료 후 중복 전송은 차단한다.

## Collector 경계
`collector-config.js`와 `js/collector-client.js`는 패키지에 복사하거나 수정하지 않는다. participant route는 production의 두 파일을 로드하고 실제 production API인 `new CubeRevCollectorClient(options).submit()`을 사용한다. health/POST 계약 버전은 collector가 기대하는 `0.7.12`로 고정하고, export되는 session JSON의 app version은 `CUBE-REV 0.8.5`로 분리한다. 따라서 collector endpoint·fallback transport·receipt 처리의 소유권은 기존 코드에 남는다.

## Legacy fixed-set retirement
참가자가 12/48, random/fixed, 연구용 sequence ID를 선택하는 UI는 없다. trial count 28은 진행도에만 표시되고 표본수 N과 혼동되는 문구는 없다. 내부 class는 `A/B/F` opaque code로만 전달한다.

## Resume-safe invariant
1. anonymous token → sequence ID가 결정론적이다.
2. 저장된 schedule이 현재 config와 다르면 재사용하지 않고 quarantine한다.
3. cursor와 responses 길이가 다르면 quarantine한다.
4. trial order가 어긋난 기록은 거부한다.
5. `SUBMITTED` 상태에서는 collector를 다시 호출하지 않는다.

## 남은 통합 경계
GitHub의 기존 `index.html`은 2,588,604-byte 단일 압축 행이라 현재 connector가 내용을 반환하지 못했다. 그러므로 이 단계에서는 위험한 전체 교체를 하지 않았다. branch에는 직접 실행 가능한 `participant-cognitive-mode.html`과 런타임을 올리고, production default entry의 한 줄 연결은 원문을 안전하게 취득한 뒤 별도 commit으로 수행해야 한다.

# 연구자 배포 전 점검표

## 코드와 버전

- [ ] 시작 화면, HTML title, JSON `version`, manifest가 모두 `0.6.11`
- [ ] session ID가 `CR-YYYYMMDDhhmmss-12hex`
- [ ] `target_distance` 필드가 존재하지 않음
- [ ] 생성 자극의 `proposal_distance`와 `actual_distance`가 일치함
- [ ] 내부 self-test가 전부 통과함

## 실험 UI

- [ ] 초기 카메라가 정면으로 시작함
- [ ] 선택 옵션이 새 세션에서도 복원됨
- [ ] 동의 체크는 새 세션마다 다시 필요함
- [ ] 랜덤 생성 세션이 기본 선택임
- [ ] 되돌리기와 시행 초기화가 작동함
- [ ] 많은 회전을 빠르게 입력해도 멈추지 않음
- [ ] x·y·z 뒤 방위 표시가 조작축과 일치함

## 데이터

- [ ] 짧은 시험 세션의 JSON을 직접 열어봄
- [ ] `expected_distance`가 난이도 분석의 기준임
- [ ] timing summary가 기록됨
- [ ] move, camera, undo, reset, timeout 이벤트가 구분됨
- [ ] 참가자 코드에 실명을 쓰지 말라는 안내가 있음

## 자동 수집

- [ ] `setupCollector()` 실행 완료
- [ ] Apps Script 웹 앱 URL이 `/exec`로 끝남
- [ ] `collector-config.js`의 endpoint와 token이 정확함
- [ ] 실제 Drive 폴더에 시험 JSON이 생성됨
- [ ] 제출 색인 Sheet에 시험 행이 추가됨
- [ ] 중복 제출이 duplicate로 처리됨
- [ ] 자동 수집 실패 시 로컬 다운로드가 가능함

## 연구 운영

- [ ] 모집 대상과 연령 조건 확정
- [ ] 미성년자 참여 절차 확인
- [ ] 자료 이용 목적, 보관 기간, 철회 방법 명시
- [ ] 파일럿 자료와 본 연구 자료를 구분
- [ ] 분석 전 preregistration 여부 결정
- [ ] 버전이 다른 세션을 병합할 때 변경점을 검토

## 0.6.11 추가 확인

- [ ] 저장소에 `js/collector-client.js`와 `js/cube-drag-controller.js`가 있다.
- [ ] 배경을 드래그하면 카메라만 움직인다.
- [ ] 큐브를 좌우로 드래그하면 y축 전체 회전이 한 번 적용된다.
- [ ] 큐브를 위아래로 드래그하면 x축 전체 회전이 한 번 적용된다.
- [ ] 짧은 큐브 드래그는 회전으로 승인되지 않는다.
- [ ] 자동 제출 성공 뒤 Drive와 Sheets를 확인했다.
- [ ] Apps Script 주소를 직접 열면 JSON 파일 선택 화면이 나타난다.
- [ ] 자동 제출 실패 상황에서 `JSON 저장 후 직접 제출` 흐름을 시험했다.
- [ ] Sheets의 `submission_method`가 자동/수동 제출을 구분한다.

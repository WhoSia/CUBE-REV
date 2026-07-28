# CUBE-REV 0.6.11 반영 순서

이번 패치는 버전 번호를 올리지 않습니다. 화면·저장 JSON·수집기는 모두 `0.6.11`을 사용합니다.

## 들어 있는 변경 파일

```text
index.html
CUBE-REV_0.6.11_GitHub_Pages_Pilot.html
js/
├─ collector-client.js
├─ cube-drag-controller.js
└─ responsive-layout-controller.js
collector/
└─ google-apps-script/
   └─ Code.gs
```

GitHub에는 HTML 두 파일과 `js` 폴더를 덮어씁니다. Google Apps Script에는 `Code.gs`만 반영합니다.

## 1. Google Apps Script를 먼저 갱신하기

현재 사용 중인 CUBE-REV 수집기 프로젝트를 엽니다. 새 Apps Script 프로젝트를 만들지 않습니다.

1. 기존 `Code.gs` 내용을 모두 지웁니다.
2. 패치의 `collector/google-apps-script/Code.gs` 내용을 붙여넣습니다.
3. 저장합니다.
4. 필요하면 `setupCollector()`를 한 번 실행해 기존 Drive 폴더·Sheets·study token이 정상적으로 잡히는지 확인합니다.
5. `배포 → 배포 관리`로 들어갑니다.
6. 현재 웹 앱 배포의 연필 아이콘을 누릅니다.
7. 버전을 `새 버전`으로 선택하고 배포합니다.

기존 배포를 새 버전으로 갱신하면 아래 `/exec` 주소는 그대로 유지됩니다.

```text
https://script.google.com/macros/s/AKfycbwJEB0khZSmbbvUkjlzdWE9y33ALHml9D8NUnDhPi9_Z5Z6ZmhoRfjwaRo6vjjaDVVyPw/exec
```

배포 후 다음 주소를 열어 `expected_version`이 `0.6.11`인지 확인합니다.

```text
위 웹 앱 주소 뒤에 ?format=json 추가
```

예상되는 핵심 값은 다음과 같습니다.

```json
{
  "ok": true,
  "expected_version": "0.6.11",
  "receipt_confirmation_available": true
}
```

### study token 확인

기존 Apps Script 프로젝트와 Script Properties를 그대로 사용했다면 token도 그대로 유지됩니다. `setupCollector()` 출력의 `studyToken`이 HTML에 들어 있는 값과 다를 때만 HTML 두 파일에서 `studyToken`을 검색해 새 값으로 바꿉니다.

## 2. GitHub 파일 덮어쓰기

GitHub 저장소 최상단에서 다음 파일을 교체합니다.

```text
index.html
CUBE-REV_0.6.11_GitHub_Pages_Pilot.html
```

`js` 폴더에는 다음 세 파일을 올립니다.

```text
js/collector-client.js
js/cube-drag-controller.js
js/responsive-layout-controller.js
```

기존 `collector-config.js`는 이번 실행 파일에서 사용하지 않습니다. 저장소에 남겨 두어도 실행에는 영향을 주지 않지만, 혼동을 줄이려면 삭제해도 됩니다.

커밋 메시지 예시는 다음과 같습니다.

```text
Add confirmed receipts and responsive mobile layout
```

Pages 배포가 끝난 뒤 데스크탑에서는 `Ctrl + Shift + R`, 모바일에서는 브라우저의 사이트 데이터 삭제 또는 새로고침으로 이전 캐시를 지웁니다.

## 3. 최종 제출 시험

1. 시행 수를 1로 설정합니다.
2. 큐브를 완성하거나 세션 종료를 누릅니다.
3. 완료 화면의 상태가 다음 순서로 변하는지 봅니다.

```text
수집기 연결 상태 확인
→ 결과 파일 준비
→ 수집기로 전송
→ 저장 확인 대기
→ 수신 완료
```

`수신 완료`가 나타나면 다음 정보도 표시됩니다.

```text
저장된 JSON 파일 이름
수신 확인 코드
```

마지막으로 Google Drive 폴더와 제출 색인 Sheets에서 같은 세션 ID를 확인합니다.

## 오류별 확인 지점

### 수집기 연결 확인 시간이 초과됨

Apps Script 코드는 저장했지만 웹 앱을 새 버전으로 배포하지 않았을 가능성이 큽니다. 배포 관리에서 기존 배포를 다시 갱신합니다.

### 수집기 버전이 0.6.10으로 표시됨

새 `Code.gs`가 현재 `/exec` 배포에 반영되지 않은 상태입니다.

### 인증 정보가 일치하지 않음

`setupCollector()`에서 출력된 `studyToken`과 HTML의 `studyToken`이 다른 상태입니다.

### 전송 뒤 수신 확인을 받지 못함

Apps Script 실행 기록에서 `doPost` 오류를 확인합니다. Drive에 파일이 실제로 생겼다면 receipt 조회 부분을 확인하고, 파일도 생기지 않았다면 token·웹 앱 공개 범위·JSON 버전을 먼저 확인합니다.

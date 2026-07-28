# CUBE-REV 0.6.11 결과 수집 설정

## 수집 흐름

0.6.11은 자동 제출과 수동 업로드를 같은 Google Apps Script 수집기에서 처리합니다.

```text
GitHub Pages 실험
├─ 세션 종료 시 자동 제출
└─ 실패 시 JSON 다운로드 + 수동 제출 페이지
                         ↓
                 Google Apps Script
                         ↓
        비공개 Drive JSON + Sheets 색인
```

이미 JSON 파일을 전달받은 사람은 웹 앱 주소를 바로 열어 수동으로 제출할 수 있습니다.

## 기존 수집기 업데이트

새 Apps Script 프로젝트를 만들 필요는 없습니다.

1. 기존 프로젝트의 `Code.gs`를 0.6.11 파일로 교체합니다.
2. `setupCollector()`를 한 번 실행합니다.
3. `Deploy → Manage deployments`에서 기존 웹 앱 배포를 편집합니다.
4. Version을 `New version`으로 바꾸고 다시 배포합니다.
5. 기존 `/exec` 주소가 유지되는지 확인합니다.
6. 주소를 열었을 때 파일 선택 화면이 나타나는지 확인합니다.

`?format=json`을 붙이면 상태 확인용 JSON이 표시됩니다.

```text
https://script.google.com/macros/s/.../exec?format=json
```

## GitHub 설정

`collector-config.js`에는 자동 제출 주소와 수동 업로드 주소가 함께 들어 있습니다.

```javascript
window.CUBE_REV_COLLECTOR_CONFIG = {
  enabled: true,
  endpoint: 'Apps Script /exec 주소',
  manualUploadUrl: 'Apps Script /exec 주소',
  studyId: 'CUBE-REV-0.6.11',
  studyToken: '수집기 intake key',
  autoSubmitOnComplete: true,
  gzipWhenAvailable: true,
  timeoutMs: 30000
};
```

GitHub Pages에서는 이 파일이 공개됩니다. `studyToken`은 비밀번호가 아니라 엉뚱한 자동 요청을 조금 줄이기 위한 intake key입니다.

## 자동 제출 시험

1. 짧은 세션을 완료합니다.
2. 완료 화면에 제출 완료 메시지가 나타나는지 확인합니다.
3. Drive에 `CR-....json` 파일이 생겼는지 확인합니다.
4. Sheets 색인에 `automatic_form_post` 행이 추가됐는지 확인합니다.
5. 같은 세션을 다시 제출했을 때 중복 파일이 생기지 않는지 확인합니다.

## 수동 업로드 시험

1. 실험 완료 화면에서 JSON을 내려받습니다.
2. **수집 페이지 열기**를 누릅니다.
3. JSON을 선택해 제출합니다.
4. Sheets의 `submission_method`가 `manual_upload_portal`인지 확인합니다.
5. 이미 제출된 파일을 다시 올렸을 때 중복 안내가 나오는지 확인합니다.

## 운영상 주의

- 웹 앱은 `Execute as: Me`, `Who has access: Anyone`으로 배포해야 외부 참가자가 제출할 수 있습니다.
- 학교 Google Workspace 계정은 외부 공개가 제한될 수 있습니다.
- 공개 링크에는 스팸 제출 가능성이 있으므로 Drive와 Sheets를 주기적으로 확인합니다.
- 이름, 학번, 연락처와 같은 직접 식별정보를 참가자 코드에 넣지 않도록 안내합니다.

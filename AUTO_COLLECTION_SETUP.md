# 자동 JSON 수집 설정

## 결론

GitHub Pages 자체에는 참가자 JSON을 저장할 서버 기능이 없습니다. 이 묶음은 Google Apps Script 웹 앱을 외부 수집기로 사용하여 다음 흐름을 구현합니다.

```text
GitHub Pages 실험 페이지
→ 세션 종료
→ 압축된 JSON 자동 제출
→ 연구자 Google Drive의 비공개 폴더
→ Google Sheets 제출 색인
```

자동 제출에 실패해도 참가자는 JSON을 직접 내려받을 수 있습니다.

Google Apps Script 웹 앱은 `doPost(e)`로 HTTP POST 요청을 처리할 수 있습니다.
공식 문서: https://developers.google.com/apps-script/guides/web

Google Drive 파일 생성 공식 문서: https://developers.google.com/apps-script/reference/drive/drive-app

## 1. Apps Script 프로젝트 만들기

1. https://script.google.com 에서 새 프로젝트를 만듭니다.
2. `collector/google-apps-script/Code.gs`의 내용을 기본 코드 파일에 붙여넣습니다.
3. 프로젝트 설정에서 `appsscript.json` 표시를 켭니다.
4. 제공된 `appsscript.json` 내용으로 교체합니다.

## 2. 수집 저장소 초기화

Apps Script 편집기에서 함수 목록을 `setupCollector`로 선택하고 실행합니다.

처음 실행할 때 Google Drive와 Google Sheets 권한을 승인해야 합니다. 실행 로그에는 다음 정보가 출력됩니다.

```json
{
  "folderId": "...",
  "sheetId": "...",
  "studyToken": "...",
  "expectedVersion": "0.6.10"
}
```

자동 생성되는 항목:

- Google Drive 폴더: `CUBE-REV 0.6.10 submissions`
- Google Sheets 파일: `CUBE-REV 0.6.10 submission index`
- study token

## 3. 웹 앱 배포

1. 우측 상단 `Deploy → New deployment`
2. 유형: `Web app`
3. Execute as: `Me`
4. Who has access: `Anyone`
5. 배포 후 `/exec`로 끝나는 URL을 복사

학교·기관 Google Workspace 정책에 따라 `Anyone` 옵션이 없을 수 있습니다. 이 경우 개인 Google 계정을 사용하거나 자동 수집을 끄고 JSON을 직접 받는 방법을 사용하십시오.

## 4. 실험 페이지에 연결

루트의 `collector-config.js`를 수정합니다.

```javascript
window.CUBE_REV_COLLECTOR_CONFIG = {
  enabled: true,
  endpoint: 'https://script.google.com/macros/s/배포_ID/exec',
  studyId: 'CUBE-REV-0.6.10',
  studyToken: 'setupCollector에서 출력된 값',
  autoSubmitOnComplete: true,
  gzipWhenAvailable: true,
  timeoutMs: 30000
};
```

수정한 파일을 GitHub에 올리면 Pages에 반영됩니다.

## 5. 작동 시험

1. 본인 코드로 짧은 세션을 실행합니다.
2. 세션을 종료합니다.
3. 완료 화면에 자동 제출 완료 메시지가 뜨는지 확인합니다.
4. Drive 폴더에 `CR-....json` 파일이 생겼는지 확인합니다.
5. 제출 색인 Sheet에 한 행이 추가됐는지 확인합니다.
6. 같은 세션을 다시 제출했을 때 중복 파일이 생기지 않는지 확인합니다.

## 수집기의 동작

- Chrome·Edge에서 지원되면 JSON을 gzip으로 압축한 뒤 base64로 전송
- 수집기는 압축을 풀어 원본 JSON으로 Drive에 저장
- session ID가 같은 파일은 중복 저장하지 않음
- 프로젝트와 버전, session ID 형식을 검사
- 저장 결과를 완료 화면으로 회신
- 실패 시 로컬 JSON 다운로드 유지

## 제한

- `studyToken`은 공개된 JavaScript 파일에 들어가므로 비밀번호가 아닙니다. 무관한 우발적 제출을 줄이는 intake key 정도로만 사용됩니다.
- 공개적으로 넓게 배포하면 스팸 요청이나 Apps Script 할당량 소모가 발생할 수 있습니다.
- 이 수집기는 소규모 주변인 파일럿에 적합합니다.
- 민감한 개인정보, 의료정보, 정확한 실명은 수집하지 마십시오.
- 수십~수백 명 이상 또는 장기 운영에는 인증·데이터베이스·접근제어가 있는 별도 백엔드가 더 적절합니다.

## 수집을 사용하지 않는 경우

`collector-config.js`에서 다음을 유지합니다.

```javascript
enabled: false,
endpoint: ''
```

이 경우 자동 제출 버튼은 나타나지 않고 JSON 다운로드만 제공됩니다.

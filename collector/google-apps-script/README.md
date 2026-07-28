# Google Apps Script Collector

이 폴더는 CUBE-REV 0.6.10 결과 JSON을 Google Drive로 받는 선택형 수집기입니다.

## 파일

- `Code.gs`: 웹 앱과 저장 로직
- `appsscript.json`: Apps Script manifest

## 설치 요약

1. 새 Apps Script 프로젝트 생성
2. 두 파일 내용 복사
3. `setupCollector()` 실행 및 권한 승인
4. 로그의 `studyToken` 복사
5. 웹 앱으로 배포
6. `collector-config.js`에 endpoint와 token 입력
7. 시험 세션 제출

상세 내용은 저장소 루트의 `AUTO_COLLECTION_SETUP.md`를 참고하십시오.

## 저장 구조

- Drive folder: 원본 JSON 파일
- Spreadsheet: 수신 시각, session ID, 참가자 코드, 버전, 시행 수, 파일 ID 색인

## 중복 처리

같은 session ID 파일이 이미 있으면 새 파일을 만들지 않고 `duplicate` 상태를 반환합니다.

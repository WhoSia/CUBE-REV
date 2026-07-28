# CUBE-REV 0.6.10

2×2 가상 큐브의 최종 상태만 보고 직접 복원하는 행동 실험 도구입니다. 큐브 조작, 카메라 이동, 전체 회전, 시행 시간, 되돌리기와 초기화 사용, 성공·포기·시간초과 상태를 JSON 세션 파일에 기록합니다.

## 바로 실행

GitHub Pages에 배포할 때 저장소 루트의 `index.html`이 실험 페이지가 됩니다.

- 온라인 실행: GitHub Pages URL
- 오프라인 실행: `CUBE-REV_0.6.10_GitHub_Pages_Pilot.html`을 내려받아 브라우저에서 열기
- 결과 저장: 로컬 JSON 다운로드는 항상 가능
- 선택 기능: Google Apps Script 수집기를 연결하면 세션 종료 시 비공개 Google Drive 폴더로 자동 제출

## 중요한 구조

GitHub Pages는 정적 호스팅 서비스이므로 HTML·CSS·JavaScript를 제공할 수 있지만, 참가자 JSON을 GitHub Pages 자체에 저장할 수는 없습니다. 자동 수집을 사용하려면 별도 수집 엔드포인트가 필요합니다.

이 배포 묶음은 다음 두 방식 모두를 지원합니다.

1. **로컬 제출 방식**: 참가자가 JSON을 내려받아 연구자에게 전달
2. **자동 제출 방식**: 포함된 Google Apps Script 수집기가 JSON을 연구자의 Google Drive에 저장

GitHub Pages 공식 설명: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

## 빠른 배포

1. 새 GitHub 저장소를 만듭니다.
2. 이 폴더의 파일을 저장소 루트에 올립니다.
3. GitHub 저장소에서 `Settings → Pages`로 이동합니다.
4. 배포 원본을 `Deploy from a branch`, 브랜치를 `main`, 폴더를 `/ (root)`로 설정합니다.
5. 표시된 Pages URL을 엽니다.

상세 절차는 [DEPLOYMENT_GITHUB_PAGES.md](DEPLOYMENT_GITHUB_PAGES.md)를 참고합니다.

## 자동 수집 설정

자동 수집은 기본적으로 꺼져 있습니다. 설정 절차:

1. `collector/google-apps-script/Code.gs`를 Google Apps Script에 배포합니다.
2. `setupCollector()`를 한 번 실행합니다.
3. 배포 URL과 생성된 study token을 `collector-config.js`에 입력합니다.
4. `enabled: true`로 바꿉니다.

상세 절차는 [AUTO_COLLECTION_SETUP.md](AUTO_COLLECTION_SETUP.md)를 참고합니다.

## 0.6.10의 주요 수정

- 세션 ID: `CR-YYYYMMDDhhmmss-12hex`
- 버전 문자열 전체 통일: `0.6.10`
- 생성기 메타데이터: `proposal_distance`, `actual_distance`
- exact-depth outward walk 생성기로 제안 거리와 실제 거리를 일치시킴
- 자동 제출 상태와 영수증 메타데이터 추가
- 수집기 미설정·실패 시 로컬 JSON 다운로드 유지
- 시작 화면의 선택값은 브라우저에 보존하되 동의 체크는 매 세션 다시 요구

## 문서

- [DEPLOYMENT_GITHUB_PAGES.md](DEPLOYMENT_GITHUB_PAGES.md): GitHub Pages 배포
- [AUTO_COLLECTION_SETUP.md](AUTO_COLLECTION_SETUP.md): Google Apps Script 자동 수집
- [PARTICIPANT_GUIDE.md](PARTICIPANT_GUIDE.md): 참가자 안내문
- [RESEARCHER_CHECKLIST.md](RESEARCHER_CHECKLIST.md): 배포 전 점검표
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md): JSON 필드 설명
- [PRIVACY_NOTICE_TEMPLATE.md](PRIVACY_NOTICE_TEMPLATE.md): 개인정보·연구 안내문 초안
- [SECURITY.md](SECURITY.md): 수집 엔드포인트의 한계와 보호 조치
- [CHANGELOG.md](CHANGELOG.md): 변경 이력

## 브라우저

PC용 최신 Chrome 또는 Edge를 권장합니다. 모바일은 화면과 키보드 조건이 달라지므로 본 실험에서는 별도 조건으로 다루는 편이 안전합니다.

## 라이선스

코드는 [MIT License](LICENSE)로 배포합니다. 연구 자료·논문·실험 프로토콜의 사용 조건은 연구자가 별도로 명시할 수 있습니다.

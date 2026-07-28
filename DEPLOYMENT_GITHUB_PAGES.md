# GitHub Pages 배포 절차

## 1. 저장소 만들기

1. GitHub에서 새 저장소를 만듭니다.
2. 저장소 이름 예시: `cube-rev-pilot`
3. 주변인을 대상으로 한 파일럿이라면 공개 저장소가 가장 간단합니다.
4. 참가자 데이터는 저장소에 올리지 않습니다.

## 2. 파일 올리기

이 배포 폴더의 내용을 저장소 루트에 올립니다. 최소 필수 파일은 다음입니다.

```text
index.html
collector-config.js
js/collector-client.js
js/cube-drag-controller.js
```

문서와 수집기 코드는 저장소에 함께 보관하는 것을 권장합니다.

## 3. Pages 켜기

1. 저장소의 `Settings`를 엽니다.
2. 왼쪽 메뉴에서 `Pages`를 선택합니다.
3. `Build and deployment`에서 `Deploy from a branch`를 선택합니다.
4. Branch는 `main`, Folder는 `/ (root)`로 선택합니다.
5. 저장 후 몇 분 뒤 URL이 생성됩니다.

GitHub 공식 절차: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## 4. 배포 확인

Pages URL에서 다음을 점검합니다.

- 시작 화면에 `CUBE-REV 0.6.11`이 표시되는가
- 내부 검증이 모두 통과하는가
- 내부 랜덤 생성 세션이 기본 선택인가
- 세션 ID가 `CR-날짜-임의값` 형식인가
- 배경 드래그와 큐브 드래그가 서로 다른 기능으로 작동하는가
- 세션 종료 후 자동 제출 상태가 표시되는가
- 수집기 주소를 직접 열면 JSON 업로드 화면이 나타나는가
- Drive와 Sheets에 자동/수동 제출이 기록되는가

## 5. 업데이트

`index.html`이나 설정 파일을 수정하여 `main` 브랜치에 올리면 Pages가 다시 배포됩니다. 배포본을 바꿀 때는 다음을 지킵니다.

- 버전 번호를 올림
- `CHANGELOG.md` 갱신
- 기존 자료와 새 자료를 같은 분석에 섞기 전 버전 차이를 검토
- 수집기 `EXPECTED_VERSION`도 같은 버전으로 갱신

## 6. 검색 노출

`robots.txt`는 검색 로봇에 사이트를 색인하지 말라고 요청합니다. 이는 접근 통제가 아닙니다. URL을 아는 사람은 페이지에 접근할 수 있습니다.

공개 전면 배포가 아니라 제한된 파일럿이라면 링크를 필요한 참가자에게만 전달하십시오.

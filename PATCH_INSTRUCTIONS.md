# 0.6.11 업데이트 적용 순서

이 ZIP에는 0.6.10 저장소에서 바뀐 파일만 들어 있습니다. 압축을 푼 뒤 같은 경로에 덮어쓰면 됩니다.

## 1. Apps Script 먼저 갱신

`collector/google-apps-script/Code.gs`를 Apps Script 프로젝트에 붙여넣고 기존 웹 앱을 새 버전으로 다시 배포합니다.

웹 앱 주소를 열었을 때 `CUBE-REV 결과 제출` 화면이 나타나야 합니다.

## 2. GitHub 파일 교체

ZIP 안의 파일과 폴더를 저장소 최상단에 업로드합니다. 같은 이름의 파일은 교체합니다.

새 `js` 폴더를 빠뜨리지 마세요.

```text
js/
├── collector-client.js
└── cube-drag-controller.js
```

커밋 메시지 예시:

```text
Update CUBE-REV to 0.6.11
```

## 3. 예전 보조 HTML 정리

저장소의 `CUBE-REV_0.6.10_GitHub_Pages_Pilot.html`은 삭제하고, 새 `CUBE-REV_0.6.11_GitHub_Pages_Pilot.html`을 올립니다. 실제 GitHub Pages 진입점은 계속 `index.html`입니다.

## 4. 배포 확인

1. 화면에 `0.6.11`이 표시되는지 확인합니다.
2. 배경 드래그로 카메라가 움직이는지 확인합니다.
3. 큐브 드래그로 전체 회전이 적용되는지 확인합니다.
4. 짧은 세션의 자동 제출을 확인합니다.
5. 수집기 주소에서 JSON 수동 업로드도 확인합니다.

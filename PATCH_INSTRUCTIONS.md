# CUBE-REV 0.6.11 Hotfix 적용 방법

이 ZIP에는 이번 수정에서 바뀐 파일만 들어 있습니다. Google Apps Script 수집기는 이미 정상 작동하므로 수정하지 않습니다.

## GitHub에 덮어쓸 파일

저장소 최상단에 다음 파일을 덮어씁니다.

- `index.html`
- `CUBE-REV_0.6.11_GitHub_Pages_Pilot.html`
- `collector-config.js`

`js` 폴더 안에서는 다음 두 파일을 덮어씁니다.

- `js/cube-drag-controller.js`
- `js/collector-client.js`

## 반드시 확인할 것

1. 저장소 최상단의 `index.html`이 새 파일인지 확인합니다.
2. 예전 `CUBE-REV_0.6.10_GitHub_Pages_Pilot.html`이 남아 있다면 삭제합니다.
3. GitHub Pages 재배포가 끝난 뒤 `Ctrl + Shift + R`로 강력 새로고침합니다.
4. 시작 화면에 `자동 제출 연결됨`이 표시되는지 확인합니다.
5. 짧은 세션을 끝낸 뒤 자동 제출 성공 문구를 확인합니다.
6. 내려받은 JSON에서 다음 값을 확인합니다.

```json
{
  "version": "0.6.11",
  "build_id": "0.6.11-hotfix-2"
}
```

## 큐브 드래그 확인

- 큐브 스티커 또는 큐브 내부의 빈 틈에서 가로로 드래그하면 `y` 또는 `y'`가 적용됩니다.
- 세로로 드래그하면 `x` 또는 `x'`가 적용됩니다.
- 큐브 바깥 배경을 드래그하면 카메라 시점만 이동합니다.
- 드래그 거리가 너무 짧으면 회전하지 않습니다.

## 수집기

Apps Script의 `Code.gs`와 웹 앱 배포는 그대로 둡니다. 실험 페이지는 다음 수집기에 직접 연결되어 있습니다.

```text
https://script.google.com/macros/s/AKfycbwJEB0khZSmbbvUkjlzdWE9y33ALHml9D8NUnDhPi9_Z5Z6ZmhoRfjwaRo6vjjaDVVyPw/exec
```

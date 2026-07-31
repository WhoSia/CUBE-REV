# CUBE-REV

CUBE-REV is an interactive research tool for studying how people recover a scrambled 2×2 Rubik’s Cube from the visible final state.

The experiment does not require participants to watch the scrambling process. A trial begins with a generated or preselected cube state, and the participant attempts to restore the cube. The system records the solution path, timing, camera movement, sticker-drag gestures, resets, undo operations, device environment, interface language, and submission status.

**Current public version: 0.7.12**

## Research question

CUBE-REV asks how far a person can mentally reverse a cube state when the generating path is not shown. It is designed to separate several factors that are often mixed together:

- the exact distance of a state from the solved cube;
- the number and order of moves actually attempted by the participant;
- visual inspection and camera movement before the first face turn;
- correction behaviour, including undo and trial reset;
- whole-cube reorientation versus metric face turns;
- interaction method, device type, viewport, and interface language.

The current public build is a governance-locked run-in. Do not use it for prospective human data collection; the collector and eligibility clock remain disabled until the later receipt and governance gates pass.

## What participants do

1. Select an age group, cube-experience level, session mode, and optional best time.
2. View a scrambled 2×2 cube state.
3. Restore it using sticker drags, on-screen buttons, or a desktop keyboard.
4. Continue for the selected number of trials or end the session manually.
5. Save the run-in JSON locally. Automatic collection is intentionally disabled.

No name, email address, or participant-code field is requested by the experiment page. Each session receives a random identifier such as:

```text
CR-20260728171127-ceb02c08b4b4
```

## Controls

### Mouse, trackpad, and touch

- Drag a visible sticker: turn one layer by exactly 90°.
- Drag empty background: freely orbit the camera, including complete vertical rotations past the U and D views.
- Background dragging is screen-relative, so horizontal and vertical directions remain stable after crossing 180°.
- Use the small compass icon to align the camera to the default view.
- Mouse wheel or two-finger trackpad scroll: zoom in or out.
- Two-finger pinch on a touch screen: zoom in or out.
- A single sticker drag never produces a double turn such as `R2`.

### On-screen controls

The control panel provides face turns, whole-cube rotations, undo, trial reset, trial abandonment, and session termination. On phones, the larger control panel opens as a bottom sheet so that the cube remains visible.

### Desktop keyboard

Desktop users may choose either the two-hand virtual-cube layout or direct notation input. Keyboard selection is hidden on phones and touch-oriented tablets, where drag and button controls are the primary interface.

## Session modes

- **Generated session:** creates new states within a selected exact-distance range.
- **Randomized 48-trial pilot:** runs the fixed pilot set in randomized order.
- **Free test:** accepts a custom scramble.

The generated-session metadata distinguishes the proposed generation depth from the exact verified distance. Analysis should use the recorded exact distance.

## Timing policy

A trial does not automatically advance merely because a long time has passed. When the relative-time cap is reached, the participant may continue solving. Later trial-relative timing fields are recorded as `max`, while interaction events continue to be preserved.

## Data and collection

The browser creates a JSON record for each session. Automatic submission follows a confirmed-receipt protocol:

```text
browser submission
→ Apps Script validation
→ Google Drive storage
→ receipt creation
→ browser receipt check
→ “Received” status
```

The completion screen treats the submission as successful only after the collector confirms that the file was stored or already existed. Local JSON saving remains available as a fallback.

The public page is connected to the deployed collector through:

```text
collector-config.js
```

The separately deployed Google Apps Script server source is managed outside this public GitHub Pages repository. GitHub Pages only serves the browser client.

## Languages

The interface currently supports:

- Korean
- English
- Simplified Chinese
- Traditional Chinese
- Japanese
- Spanish
- French
- German
- Portuguese
- Indonesian

The selected interface language and the language-selection source are recorded in the session JSON. A language can also be selected through a URL parameter, for example `?lang=en` or `?lang=zh-Hant`.

## Repository structure

```text
cube-rev/
├─ .github/workflows/validate-static.yml
├─ index.html
├─ CUBE-REV_0.7.12_GitHub_Pages_Pilot.html
├─ CUBE-REV_0.6.11_GitHub_Pages_Pilot.html
├─ collector-config.js
├─ README.md
├─ robots.txt
├─ js/
│  ├─ camera-zoom-controller.js
│  ├─ camera-orbit.js
│  ├─ collector-client.js
│  ├─ cube-drag-controller.js
│  ├─ i18n-controller.js
│  └─ responsive-layout-controller.js
└─ scripts/
   └─ validate-static.mjs
```

`index.html` is the GitHub Pages entry point and is byte-identical to `CUBE-REV_0.7.12_GitHub_Pages_Pilot.html`. `CUBE-REV_0.6.11_GitHub_Pages_Pilot.html` remains frozen as the verified baseline archive.

The static validator and GitHub Actions workflow prevent version drift, missing controller files, cache-key mismatches, divergence between the two HTML copies, and regression of the unrestricted camera orbit.

## Deployment

Upload the repository contents so that `index.html` is at the repository root. In GitHub Pages settings, deploy from the `main` branch and the root folder.

Collector server changes are deployed separately by updating the existing Apps Script web-app version rather than creating a new deployment. This preserves the configured `/exec` endpoint.

## Privacy and research use

The tool records detailed behavioural data, including precise interaction times, browser and screen information, cube moves, camera actions, gestures, and submission receipts. Researchers should:

- avoid asking participants to enter names or other direct identifiers;
- explain the purpose, storage period, access policy, and withdrawal procedure;
- comply with institutional and guardian-consent requirements for minors;
- keep the Drive collection folder private;
- verify the collector and exported schema before formal data collection.

## Technical note

The interface is separated into focused controllers for gesture recognition, camera zoom, responsive layout, internationalization, and collection transport. This keeps input handling, rendering, data submission, and presentation concerns from being coupled unnecessarily.

---

# CUBE-REV

CUBE-REV는 참가자가 **생성 경로를 보지 않은 채**, 화면에 제시된 2×2 루빅스 큐브의 최종 상태를 얼마나 복원할 수 있는지 연구하기 위한 인터랙티브 실험 도구입니다.

각 시행은 생성되었거나 미리 정해진 큐브 상태에서 시작합니다. 참가자는 큐브를 직접 맞추며, 시스템은 풀이 경로, 시간, 카메라 움직임, 스티커 드래그, 초기화와 되돌리기, 장치 환경, 인터페이스 언어, 제출 상태를 기록합니다.

**현재 공개 버전: 0.7.12**

## 연구 질문

CUBE-REV는 생성 과정을 보여 주지 않았을 때 사람이 큐브 상태를 어느 정도까지 정신적으로 역추적할 수 있는지 묻습니다. 기존의 단순 성공·실패 기록에서 섞이기 쉬운 요소를 다음처럼 분리해 관찰하도록 설계되었습니다.

- 완성 상태까지의 정확한 거리
- 참가자가 실제로 수행한 회전의 수와 순서
- 첫 면 회전 전의 시각적 탐색과 카메라 이동
- 되돌리기와 시행 초기화를 포함한 오류 수정 행동
- 전체 큐브 재정향과 거리 계산에 포함되는 면 회전의 구분
- 입력 방식, 장치 종류, 화면 크기, 인터페이스 언어

현재 공개 빌드는 governance가 잠긴 run-in입니다. 후속 receipt·governance gate가 통과하기 전에는 인간 자료를 전향적으로 수집하지 않으며 수집기와 eligibility clock도 비활성 상태입니다.

## 참가자가 하는 일

1. 연령대, 큐브 경험, 실행 모드, 선택 사항인 최고 기록을 입력합니다.
2. 화면에 제시된 2×2 큐브 상태를 관찰합니다.
3. 스티커 드래그, 화면 버튼 또는 데스크탑 키보드로 큐브를 맞춥니다.
4. 정해진 시행 수를 완료하거나 직접 세션을 종료합니다.
5. run-in JSON을 로컬에 저장합니다. 자동 수집은 의도적으로 꺼져 있습니다.

실험 화면은 이름, 이메일, 참가자 코드를 요구하지 않습니다. 각 세션에는 다음과 같은 무작위 식별자가 부여됩니다.

```text
CR-20260728171127-ceb02c08b4b4
```

## 조작법

### 마우스·터치패드·터치 화면

- 보이는 스티커 드래그: 해당 층을 정확히 90° 한 번 회전
- 빈 배경 드래그: U·D 시점을 넘어 수직으로 한 바퀴 도는 동작까지 제한 없이 카메라 회전
- 마우스 휠 또는 터치패드 두 손가락 스크롤: 확대·축소
- 터치 화면 두 손가락 핀치: 확대·축소
- 한 번의 스티커 드래그에서 `R2`와 같은 2회전은 발생하지 않음

### 화면 버튼

조작 패널에는 면 회전, 전체 큐브 회전, 되돌리기, 시행 초기화, 시행 포기, 세션 종료 기능이 있습니다. 휴대폰에서는 큐브 영역을 확보하기 위해 큰 조작 패널을 하단 시트로 엽니다.

### 데스크탑 키보드

데스크탑에서는 양손 virtual-cube 배열과 문자 표기 배열 중 하나를 선택할 수 있습니다. 휴대폰과 터치 중심 태블릿에서는 키맵 선택란을 숨기고 드래그와 화면 버튼을 기본 조작으로 사용합니다.

## 실행 모드

- **내부 랜덤 생성 세션:** 선택한 exact-distance 범위에서 새로운 상태를 생성합니다.
- **무작위화 파일럿 48시행:** 고정 파일럿 세트를 무작위 순서로 실행합니다.
- **자유 테스트:** 사용자가 입력한 스크램블을 사용합니다.

생성 세션은 제안된 생성 깊이와 실제로 검증된 exact distance를 구분해 기록합니다. 난이도 분석에는 검증된 실제 거리를 사용해야 합니다.

## 시간 측정 정책

시간이 오래 지났다는 이유로 시행이 자동으로 넘어가지 않습니다. 상대 시간 측정 상한에 도달해도 참가자는 계속 풀 수 있습니다. 이후 시행 상대 시간은 `max`로 기록되지만, 입력 행동 기록은 계속 보존됩니다.

## 자료와 자동 수집

브라우저는 세션마다 JSON 자료를 만듭니다. 자동 제출은 다음과 같은 수신 확인 절차를 사용합니다.

```text
브라우저 제출
→ Apps Script 검증
→ Google Drive 저장
→ 영수증 생성
→ 브라우저의 영수증 확인
→ “수신 완료” 표시
```

완료 화면은 수집기가 실제 저장 또는 기존 동일 파일의 존재를 확인한 뒤에만 제출 성공으로 처리합니다. 문제가 생기면 JSON을 직접 저장해 제출할 수 있습니다.

공개 페이지는 다음 설정 파일을 통해 배포된 수집기에 연결됩니다.

```text
collector-config.js
```

별도로 배포된 Google Apps Script 서버 소스는 이 공개 GitHub Pages 저장소 밖에서 관리합니다. GitHub Pages는 브라우저 클라이언트만 제공합니다.

## 지원 언어

현재 인터페이스는 다음 언어를 지원합니다.

- 한국어
- 영어
- 중국어 간체
- 중국어 번체
- 일본어
- 스페인어
- 프랑스어
- 독일어
- 포르투갈어
- 인도네시아어

선택한 인터페이스 언어와 선택 경로는 세션 JSON에 기록됩니다. `?lang=en`, `?lang=zh-Hant`처럼 URL 매개변수로 언어를 지정할 수도 있습니다.

## 저장소 구조

```text
cube-rev/
├─ .github/workflows/validate-static.yml
├─ index.html
├─ CUBE-REV_0.7.12_GitHub_Pages_Pilot.html
├─ CUBE-REV_0.6.11_GitHub_Pages_Pilot.html
├─ collector-config.js
├─ README.md
├─ robots.txt
├─ js/
│  ├─ camera-zoom-controller.js
│  ├─ camera-orbit.js
│  ├─ collector-client.js
│  ├─ cube-drag-controller.js
│  ├─ i18n-controller.js
│  └─ responsive-layout-controller.js
└─ scripts/
   └─ validate-static.mjs
```

`index.html`은 GitHub Pages가 여는 진입 파일이며 `CUBE-REV_0.7.12_GitHub_Pages_Pilot.html`과 바이트 단위로 같습니다. `CUBE-REV_0.6.11_GitHub_Pages_Pilot.html`은 검증된 baseline 보관본으로 동결합니다.

정적 검증기와 GitHub Actions는 버전 표류, 누락된 컨트롤러 파일, 캐시 키 불일치, 두 HTML 사본의 내용 차이, 자유 카메라 회전의 회귀를 자동으로 막습니다.

## 배포

`index.html`이 저장소 최상단에 오도록 위 파일을 업로드합니다. GitHub Pages에서는 `main` 브랜치의 루트 폴더를 배포 대상으로 설정합니다.

수집기 서버를 바꿀 때는 새로운 웹 앱 주소를 만들기보다 기존 Apps Script 배포를 **새 버전으로 업데이트**해야 합니다. 그래야 설정된 `/exec` 주소가 유지됩니다.

## 개인정보와 연구 이용

이 도구는 정밀한 행동 시각, 브라우저와 화면 정보, 큐브 회전, 카메라 조작, 제스처, 제출 영수증을 기록합니다. 연구자는 다음 사항을 지켜야 합니다.

- 이름과 같은 직접 식별자를 입력하도록 요구하지 않기
- 연구 목적, 보관 기간, 접근 범위, 철회 절차를 설명하기
- 미성년자 연구에 필요한 기관 승인과 보호자 동의 요건 확인하기
- 수집용 Google Drive 폴더를 비공개로 유지하기
- 공식 수집 전 수집기와 JSON 스키마를 다시 검증하기

## 기술 구조

제스처 판정, 카메라 확대·축소, 반응형 레이아웃, 다국어 처리, 자료 전송을 각각 독립된 컨트롤러로 분리했습니다. 입력 처리, 렌더링, 제출, 화면 표시가 한 파일에 불필요하게 얽히지 않도록 구성한 것입니다.

## 0.7.12 browser run-in

0.7.12는 decision point에서 Web Crypto exact-bucket 60/20/20 배정을 사용합니다.
배포 호스트의 모든 시행은 `TERMINAL_ONLY`이며, 생성 경로의 회전 모션과
회전 기호 텍스트를 참가자에게 노출하지 않습니다. 고정된 2,400 ms 비노출 구간
뒤에 최종 상태만 제시합니다. `TIME_MATCHED_NEUTRAL`은 중립 기호와 700 ms 최소
노출만 사용합니다. csTimer 양손 키맵에는 x·y·z 회전이 포함되며, 카메라는
180° 이후에도 방향이 유지되는 screen-relative matrix orbit을 사용합니다.

Collection은 잠겨 있고 eligibility clock은 `NOT_STARTED`입니다. 별도 collector의
synthetic receipt는 이후 검증 범위이며, 생성 history 모션 조건은 사용하지 않습니다.

## 0.7.11 calibration history

검증된 0.6.11 공개 baseline은 그대로 유지합니다. Source-bound 0.7.11
run-in host, 고정 probe policy, memory factorial, two-pass annotation packet,
eligibility clock gate, 누적 CR07-BATCH registry는
[`docs/CUBE-REV_0.7.11_DEPLOYMENT.md`](docs/CUBE-REV_0.7.11_DEPLOYMENT.md)에
정리되어 있습니다.

Calibration route는 의도적으로 수집이 잠겨 있습니다. Governance,
collector receipt, linkage, clock authorization gate가 모두 통과하기
전에는 prospective human data에 사용하면 안 됩니다.

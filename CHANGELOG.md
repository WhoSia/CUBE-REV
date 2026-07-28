# 변경 이력

## 0.6.10 — GitHub Pages Distribution & Optional Automatic Collection

- 모든 버전 표시를 `0.6.10`으로 통일
- 세션 ID를 버전 중립 형식 `CR-YYYYMMDDhhmmss-12hex`로 변경
- 참가자 코드 hash를 session ID에서 제거
- 내부 생성기를 `exact_depth_outward_walk_v1`로 교체
- `target_distance` 제거
- `proposal_distance`, `actual_distance`, `generation_attempts` 추가
- 생성 제안 거리와 실제 exact distance 일치 self-test 추가
- 선택형 Google Apps Script 자동 제출 기능 추가
- gzip 가능한 브라우저에서 제출 payload 압축
- 제출 성공·중복·실패 상태와 receipt metadata 기록
- 자동 제출 미설정 또는 실패 시 로컬 JSON 다운로드 유지
- 사용자 설정 저장 key를 버전 중립 형식으로 변경
- 시작 화면과 하단 안내 문구 정리
- GitHub Pages 배포 문서, 수집기, 데이터 사전, 개인정보 안내문 추가

## 0.6.9

- 초기 카메라 정면 고정
- 사용자 선택 옵션 localStorage 복원
- 버전 표기 정리

## 0.6.8

- 한 단계 되돌리기
- 시행 초기화
- analysis epoch 도입

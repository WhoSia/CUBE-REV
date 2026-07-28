# CUBE-REV 0.6.10 JSON 데이터 사전

## 세션 최상위

| 필드 | 의미 |
|---|---|
| `project` | `CUBE-REV` |
| `version` | 실험 도구 버전. 이번 배포는 `0.6.10` |
| `session_id` | `CR-YYYYMMDDhhmmss-12hex` 형식의 세션 식별자 |
| `session_id_scheme` | 식별자 형식 설명 |
| `participant_code` | 참가자가 입력한 가명 코드 |
| `mode` | `generated`, `pilot`, `custom` |
| `created_at`, `completed_at` | 세션 시작·종료 ISO 시각 |
| `randomization_seed` | 자극 순서와 생성 재현용 seed |
| `participant_metadata` | 연령대, 경험 수준, 최고 기록, 동의 시각 |
| `interface_settings` | 키맵, 카메라, 전체 회전 처리 정책 등 |
| `generator_settings` | 생성 거리 범위, 시행 수, timeout |
| `data_submission` | 자동 제출 설정·상태·영수증 정보 |
| `trials` | 실제로 시작된 시행 기록 |
| `events` | 세션 수준 사건 로그 |

## 생성기 메타데이터

| 필드 | 의미 |
|---|---|
| `generator_metadata.algorithm` | `exact_depth_outward_walk_v1` |
| `proposal_distance` | 생성기가 이번 시행에 선택한 exact distance |
| `actual_distance` | 생성된 상태에서 측정한 exact distance |
| `generation_attempts` | exact-depth 경로를 찾기 위해 시도한 횟수 |
| `expected_distance` | 시행 분석에 사용하는 최종 난이도 값 |

0.6.10의 내부 랜덤 생성에서는 다음이 성립하도록 검사합니다.

```text
proposal_distance = actual_distance = expected_distance
```

분석 코드에서는 언제나 `expected_distance`를 주 난이도 변수로 사용하는 것을 권장합니다.

## 시행 상태

| 필드 | 의미 |
|---|---|
| `trial_id`, `ordinal` | 시행 식별자와 순번 |
| `initial_state_id` | 처음 제시된 상태의 exact atlas ID |
| `initial_distance` | 처음 제시된 상태의 exact HTM distance |
| `status` | `solved`, `gave_up`, `timed_out`, `session_terminated` 등 |
| `accepted_moves` | 실제 적용된 회전 명령 목록 |
| `events` | 키 입력·카메라·회전·종료 사건 |
| `undo_count` | 한 단계 되돌리기 적용 횟수 |
| `reset_count` | 시행 초기화 횟수 |
| `analysis_epoch_count` | 초기화로 나뉜 분석 구간 수 |

## 회전 기록

| 필드 | 의미 |
|---|---|
| `move` | U, R, F, D, L, B, x, y, z와 역·180도 표기 |
| `move_kind` | `face_turn` 또는 `view_rotation` |
| `metric_included` | 최단거리 비용에 포함되는지 여부 |
| `source` | keyboard, button, undo_button 등 |
| `action_role` | 참가자 행동 또는 undo inverse |
| `analysis_epoch` | 초기화 이후 구간 번호 |
| `state_before_id`, `state_after_id` | 전후 exact state ID |
| `distance_before`, `distance_after` | 전후 최단거리 |
| `distance_delta` | 한 명령으로 바뀐 최단거리 |
| `cube_frame_after` | x·y·z 이후 현재 조작 좌표계 |

x·y·z는 관찰·재그립 명령으로 별도 기록되며 metric cost는 0입니다. 이후 면 회전은 후처리에서 `cube_frame_after`를 사용해 기준 좌표계로 정규화해야 합니다.

## 시간 변수

| 필드 | 의미 |
|---|---|
| `trial_total_ms` | 시행 전체 시간 |
| `input_window_ms` | 입력 허용 후 종료까지 시간 |
| `first_interaction_latency_ms` | 첫 승인 상호작용까지 시간 |
| `first_face_move_latency_ms` | 첫 면 회전까지 시간 |
| `first_view_rotation_latency_ms` | 첫 x·y·z까지 시간 |
| `first_camera_action_latency_ms` | 첫 카메라 조작까지 시간 |
| `solve_time_from_input_ms` | 입력 허용부터 논리적 완성까지 시간 |
| `solve_time_from_first_face_move_ms` | 첫 면 회전부터 완성까지 시간 |

## 자동 제출

| 필드 | 의미 |
|---|---|
| `collector_configured` | 수집 엔드포인트 연결 여부 |
| `status` | `not_attempted`, `preparing`, `uploading`, `stored`, `duplicate`, `failed` |
| `attempt_count` | 제출 시도 횟수 |
| `encoding` | `gzip-base64` 또는 `json` |
| `receipt_id` | 수집기가 반환한 Drive file ID |
| `file_name` | Drive에 저장된 JSON 파일명 |
| `last_error` | 제출 실패 메시지 |

연구 분석용 데이터에는 Apps Script endpoint나 study token을 저장하지 않습니다.

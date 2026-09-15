# G3-P14-R1 WCA attempt-level spine

## Scope

This stage materializes a **secondary-data world-contact spine** from the official WCA Results Export v2. It does not authorize bespoke human collection and it does not treat competition telemetry as a clinical dataset.

Primary domain for the first materialization: `event_id = 333`.

## Attempt semantics

Source values are preserved before any scientific recoding:

- `value > 0` → `VALID`; for 3×3 this is centiseconds.
- `value = -1` → `DNF`.
- `value = -2` → `DNS`.
- `value = 0` → `NO_RESULT`.
- any other non-positive value → `UNEXPECTED_VALUE`, which forces a preanalysis HOLD.

`DNF`, `DNS`, and `NO_RESULT` are three distinct source states. In particular, `0` is not silently interpreted as missing, failure, nonparticipation, or zero seconds.

## Derived long table

`wca_333_attempt_long.parquet` contains:

- `competitor_key`
- `competition_id`
- `competition_date`
- `event_id`
- `round_type_id`
- `format_id`
- `result_id`
- `attempt_number`
- `raw_value`
- `attempt_status`
- `solve_centiseconds`
- `solve_seconds`
- `round_best_raw`
- `round_average_raw`

The release-facing table excludes names. `competitor_key` is a deterministic pseudonymous convenience key derived from the public WCA person identifier. It is **not an anonymization guarantee**.

## Longitudinal boundary

Competition date provides the longitudinal axis. The export does not provide within-solve cognitive state, so P14-R1 does not infer attention, planning, memory, recovery mechanism, or other latent cognitive variables directly from a single attempt row.

## Release boundary

GitHub stores compiler code, schema, manifest, provenance and small receipts. Google Drive stores the immutable raw snapshot and large derived tables. A later Zenodo/Kaggle release may package derived tables and recipes only after WCA attribution/republication requirements are copied into the release notice.

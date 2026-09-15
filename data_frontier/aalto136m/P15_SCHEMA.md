# G3-P15 Aalto compiler schema and state-transition specification

## Custody and identity

Raw Aalto files are restricted research/non-commercial source material. Git
contains only this semantic schema, code, tests, manifests, receipt, and small
aggregate outputs. A typist identifier is a source join key for within-person
resampling; it is not an anonymization guarantee and will never be published as
a row-level release surface.

## Units

- **Raw key event:** one observable source row with raw key identity and, where
  available, press/release timing.
- **Stream/transcription:** one ordered target-sentence input sequence. The
  source adapter must fail closed if its grouping/order fields cannot be
  identified.
- **Error episode:** one uniquely reconstructible target mismatch plus its
  observable correction path, collapsed before the primary recurrence analysis.
- **Typist:** an intrinsic source stream identity; metadata is excluded unless
  an independent join audit authorizes it.

## Required adapter fields

`typist_source_id`, `stream_source_id`, `event_order`, `target_text`,
`logged_final_text` (when supplied), `raw_key`, `press_ms`, `release_ms`, and
one observable text-output representation. Source-specific aliases are written
to the acquisition receipt after archive census. Missing a required grouping or
ordering field is `SOURCE-INTEGRITY_HOLD`, not a reason to guess.

## Derived timing fields

| Field | Definition |
| --- | --- |
| `dwell_ms` | release minus press for the same key when nonnegative |
| `iki_down_down_ms` | next press minus current press |
| `flight_release_down_ms` | next press minus current release |
| `rollover` | next press precedes current release |
| `timing_valid` | finite, observable source timestamps; raw values retained even outside analysis windows |

## Online state machine

| Observable input | State/output | Rule |
| --- | --- | --- |
| Text key uniquely equal to next target character | `TARGET_MATCH_KEY` | advance observable end-buffer |
| Text key uniquely unequal to next target character | `TARGET_MISMATCH_KEY` | open candidate mismatch episode; do not infer cause |
| Backspace immediately removing active candidate mismatch | `CORRECTION_KEY` plus `CORRECTED_ERROR_EPISODE` | collapse as one corrected error episode |
| Backspace removing a matched key | `CORRECTION_KEY` plus `AMBIGUOUS_EDIT` | cannot know whether user edits observed end-buffer only |
| Delete, correction without active observable buffer, nontext key, or target cursor made nonunique | `AMBIGUOUS_EDIT` | never infer cursor/mouse/selection action |
| Unresolved mismatch at stream end | `UNCORRECTED_ERROR` summary plus retained mismatch key | final target disagreement is explicit |
| Logged final text differs from reconstructed stream text | `STREAM_RECONSTRUCTION_MISMATCH` stream flag | preserve both representations |

The module retains raw events, the final reconstructed text, a target-alignment
audit, source flags, and episode identifiers. It does not convert correction
keys into errors and does not treat several key rows from one edit path as
independent primary error events.

## Release-safe summaries

Only aggregate censuses, effect estimates, null distributions, and
typist-resampled uncertainty are release candidates. Source-row tables,
identifiers, target strings, and raw timestamps remain restricted custody.

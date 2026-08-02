# CUBE-REV 0.8.17 validation report

## Official decision

`PASS-VERSIONED-SMALL-EXTERNAL-SNAPSHOT / PASS-ROUTE-GRAMMAR-NORMALIZATION / PASS-LOCAL-MOTIF-SUPPORT / PASS-MATCHED-SCRAMBLE-ROUTE-NONUNIQUENESS / HOLD-DISTRIBUTIONAL-ECOLOGICAL-ALIGNMENT / HOLD-PER-MOVE-TIMING-TRANSFER / HOLD-WCA-BULK-MATERIALIZATION / HOLD-PUBLIC-RECONSTRUCTION-BULK-INGESTION / HOLD-SMART-CUBE-CONSENTED-COHORT / NO-GO-COGNITIVE-MECHANISM-TRANSFER / NO-PARTICIPANT-DEPLOYMENT`

## Snapshot

The frozen fixture contains 11 attributed public 3×3 reconstructions: 10 official and one unofficial. Its date range is 1982-06-05 to 2026-04-26. The WCA anchor is export format 2.0.2, export date 2026-08-02T16:15:23+00:00 and filename `WCA_export_v2_214_20260802T000025Z.tsv.zip`; the full 352 MB archive was not downloaded or claimed as custodied.

The fixture is a canonical transcription of visible fields, not a raw-HTML mirror and not a population sample. Public names and URLs remain only in source records for attribution; derived route rows use R001–R011 and contain no name or WCA-ID fields.

## Route grammar

Normalization separates face, wide, slice and cube-rotation tokens. Quarter-turn powers of three are reduced to inverse turns, half-turn primes are removed and `Xw` wide notation becomes lowercase. Unsupported tokens fail closed.

Observed totals:

- 466 nonrotation action tokens;
- 492 tokens including 26 in-solve cube rotations;
- 61 source-labelled stages;
- 42 wide moves and 14 slice moves;
- exact source-reported STM agreement in 10 of 10 routes with reported STM.

## Ecological transfer estimands

The 0.8.16 probe trajectories and external routes were mapped to a rotation-invariant face-relation alphabet: `START`, `SAME`, `OPPOSITE`, `ADJACENT`.

| Estimand | Result | Decision |
|---|---:|---|
| weighted relation bigram coverage | 0.976190 | PASS local support |
| weighted relation trigram coverage | 0.916667 | PASS local support |
| unique bigram coverage | 0.833333 | partial |
| unique trigram coverage | 0.666667 | partial |
| bigram Jensen–Shannon divergence | 0.501325 | HOLD alignment |
| trigram Jensen–Shannon divergence | 0.927702 | HOLD alignment |

The missing probe motifs are `OPPOSITE|OPPOSITE` and `START|OPPOSITE|OPPOSITE`. Most weighted local motifs occur in the fixture, but their distribution differs strongly. The correct conclusion is therefore local grammar support, not ecological distributional equivalence.

## Matched-scramble counterexample

Routes R002 and R003 report the same 4.54 s result on the same scramble but use 41 and 45 action tokens. Their normalized move-token edit distance is 0.466667, LCS ratio 0.600000 and relation edit distance 0.155556. State, scramble and total time therefore do not identify a unique route.

## Timing and cognition boundary

Public reconstruction stage labels and total times do not supply per-move timestamps. Latencies are not imputed. The external fixture cannot validate the latency component that made 0.8.16 mechanisms separable, and route similarity is not evidence of a named solver's planning depth, working memory, awareness or recovery intention.

## Reproducibility

The analysis emits a canonical result JSON, deidentified route-row JSONL and manifest binding the fixture, 0.8.16 probe registry and outputs by SHA-256. CI executes the full snapshot analysis twice and requires a byte-identical diff, then runs 22 contract gates and inherited 0.8.16/0.8.15 tests.

## Limitations

- only 11 deliberately selected public reconstructions;
- elite 3×3 routes are not a representative 2×2 cognitive cohort;
- raw WCA archive and source HTML are not custodied;
- source stage labels may reflect reconstruction conventions;
- no per-move timestamps;
- no inter-reconstructor disagreement model;
- no human mechanism inference.

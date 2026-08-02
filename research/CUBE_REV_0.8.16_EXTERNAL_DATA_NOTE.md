# CUBE-REV 0.8.16 External Cubing Trajectory Data Note

## Why this source layer matters

Official result times alone collapse many possible solving paths into one scalar. CUBE-REV needs full or partial action trajectories to study chunk continuation, re-planning, and recovery. The cubing community already maintains several complementary data layers; they must not be treated as interchangeable.

## Source hierarchy

### 1. WCA Results Export — official outcome anchor

Observed snapshot:

```text
export format       2.0.2
export date         2026-08-02T16:15:23+00:00
TSV file            WCA_export_v2_214_20260802T000025Z.tsv.zip
reported size       352 MB
```

Useful tables include competitions, persons, events, results, result_attempts, rankings, and scrambles. This layer establishes that an attempt was official and supplies its result and scramble context. It does not supply the moves executed by the competitor.

Any future use must preserve the WCA attribution statement associated with the export snapshot.

### 2. reco.nz — public reconstruction layer

reco.nz is the successor to several community reconstruction databases. Its index contains more than thirteen thousand reconstruction IDs and supports official and unofficial solves, methods, competitions, movecount, TPS, and reconstructor attribution.

The individual solve pages can include:

- scramble;
- inspection rotation;
- full reconstructed move sequence;
- labelled method stages;
- total and stage times;
- STM/ETM and TPS.

These are reconstructed trajectories, not smart-cube telemetry. Per-move timestamps generally cannot be recovered from a stage total.

### Matched-scramble natural comparison

The fixture pack includes reco.nz solve IDs 9269 and 9274. They report:

- the same 3×3 scramble;
- the same total result, 4.54 seconds;
- different move routes;
- reported STM 41 and 45.

This is useful evidence that state and total time do not determine a unique trajectory. It is not evidence that one named solver had a particular latent cognitive trait.

### reco.nz 2×2 caution

The reco.nz FAQ explicitly argues that short one-look puzzles such as 2×2 cannot properly display what is behind a solution without the solver explaining the thought process. CUBE-REV adopts that caution. Public 3×3 reconstructions can inform motif discovery and parser validation, but they do not solve the 2×2 cognitive-identification problem.

### 3. Smart-cube/timer data — consented high-resolution layer

- csTimer supports Bluetooth-cube input and user export/backup.
- Cubeast records, stores, analyses, and shares Bluetooth-cube solves, including phase recognition and execution information.
- Solved offers a reconstructor and shareable solves.

These sources may provide real per-move timing, but access must be through explicit owner export or an intentionally shared link. Private account data, server backups, and profiles are outside scope.

## Linkage ladder

A reconstruction may be linked to an official attempt only through an auditable rule.

### Exact unique

Required:

- same event;
- same result in centiseconds;
- same normalized scramble hash;
- same date;
- exactly one candidate.

Competition, round, attempt number, and public person key should then be retained as disambiguators.

### Ambiguous

More than one official attempt matches the exact event/time/scramble/date key. The record is not automatically assigned.

### Unlinked

No exact candidate exists. The reconstruction may still be used as a public trajectory fixture, but not described as linked to a WCA attempt through the export.

## Identity and ethics

Public names may be retained only for source attribution and record linkage. CUBE-REV will model trajectories and motifs, not rank named people by inferred memory, planning depth, confidence, or cognitive capacity.

## 0.8.16 decision

```text
PASS  source discovery and role separation
PASS  public fixture parsing
PASS  matched-scramble route nonuniqueness
PASS  linkage adjudication dry run
HOLD  full WCA archive materialization
HOLD  bulk reco.nz snapshot and custody audit
HOLD  consented smart-cube cohort
```

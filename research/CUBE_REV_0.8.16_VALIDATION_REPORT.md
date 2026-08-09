# CUBE-REV 0.8.16 Validation Report

## Official title

**CUBE-REV 0.8.16 — Minimal Nonreactive Multi-action Trajectory Probes, Rotational-equivalence Families & Recovery-opportunity Certification**

## Official decision

> **PASS-MINIMAL-MULTI-ACTION-TRAJECTORY / PASS-ROTATIONAL-EQUIVALENCE-FAMILIES / PASS-RECOVERY-OPPORTUNITY-DENSITY / PASS-SECOND-ACTION-PLUS-LATENCY-MINIMALITY / PASS-ROBUST-NOISE / PASS-EXTERNAL-TRAJECTORY-SOURCE-DISCOVERY / PASS-MATCHED-SCRAMBLE-ROUTE-NONUNIQUENESS / HOLD-WCA-BULK-MATERIALIZATION / HOLD-SMART-CUBE-CONSENTED-COHORT / NO-HUMAN-MECHANISM-CLAIM / NO-PARTICIPANT-DEPLOYMENT**

## Research question

CUBE-REV 0.8.15 established that a single first action cannot distinguish open-loop continuation from closed-loop re-evaluation, cannot reveal what happens after an error, and cannot expose chunk boundaries. CUBE-REV 0.8.16 asks for the smallest nonreactive extension that makes those mechanisms observably different without asking the participant to name a strategy or admit an error.

The predeclared candidate extension is a trajectory of at most three moves with intermediate cube states and inter-move latency. Trialwise confidence, correctness feedback, strategy labels, error prompts, and planning-depth reports remain absent.

## Probe construction

### Valid one-move-neighbour seeds

The certified 0.8.13 public bank remains unchanged. New research-only seed states are generated only by applying one legal face move to a certified parent state. Every generated seed records:

- parent stimulus ID;
- generator move;
- generation depth;
- exact resulting state hash;
- rotational orbit hash.

This produced six selected base families from five distinct parent stimuli. No two selected families belong to the same whole-cube rotational orbit.

| Family | Seed | Parent | Generator | Recovery opportunities |
|---|---|---|---|---:|
| CR0816-F01 | `CR086-S001~R2` | CR086-S001 | R2 | 6 |
| CR0816-F02 | `CR086-S009~Rp` | CR086-S009 | R' | 9 |
| CR0816-F03 | `CR086-S010~Dp` | CR086-S010 | D' | 10 |
| CR0816-F04 | `CR086-S010~U` | CR086-S010 | U | 10 |
| CR0816-F05 | `CR086-S022~R` | CR086-S022 | R | 8 |
| CR0816-F06 | `CR086-S023~L2` | CR086-S023 | L2 | 8 |

The minimum recovery-opportunity density is 6, the mean is 8.5, and the maximum is 10 per base family.

### Rotational-equivalence families

Each base state is transformed into six selected orientations. The selected rotations jointly balance both:

- planned first-move face: U/R/F/D/L/B each 6 times across 36 probes;
- designated recovery-error face: U/R/F/D/L/B each 6 times across 36 probes.

The move transform is not inferred from face names alone. It is certified by conjugating every face move through a whole-cube rotation on a uniquely labelled 24-sticker state. All 24 proper rotations × 18 moves satisfy the exact transition identity.

### Recovery opportunities

A preregistered recovery opportunity has the following structure:

1. a first move decreases the orientation-normalized solved score;
2. the exact inverse restores the previous score;
3. a non-inverse second move produces a better continuation than simply repeating the deteriorating move;
4. undo, non-undo reset, and persistence therefore create distinct observable trajectories.

Participant-facing text never calls the first move an error. Recovery is classified only after the fact when the observed action matches a preregistered opportunity.

## Schedule design

Twelve schedules contain twelve trials each. Every schedule presents two orientations of each of the six families. The same family is separated by at least six trials. Across the twelve schedules every family appears in every target orientation exactly four times. Adjacent trials never share the same planned first-move face.

## Synthetic mechanism court

Ten mechanisms generated 3,600 trajectories, 360 per mechanism:

- open-loop chunk continuation;
- closed-loop re-planning after the first move;
- exact-undo recovery;
- non-undo subgoal reset;
- persistence after deterioration;
- two latent labels with exactly identical trajectories;
- same-action fast chunk;
- same-action boundary pause;
- viewer-centred orientation alias.

Thirty-one repeated train/test splits were used for every predeclared contrast.

### Full three-action observation

| Contrast | Mean balanced accuracy | Decision |
|---|---:|---|
| open-loop vs closed-loop | 1.0000 | IDENTIFIABLE |
| exact undo vs non-undo reset | 1.0000 | IDENTIFIABLE |
| reset vs persistence | 1.0000 | IDENTIFIABLE |
| same actions, fast chunk vs boundary pause | 1.0000 | IDENTIFIABLE |
| object-centred vs viewer-centred frame | 0.9587 | IDENTIFIABLE |
| identical latent mechanisms | 0.4976 | NON_IDENTIFIABLE |

The negative control is part of the success condition. The analysis must not recover a latent distinction after both mechanisms have been defined to generate the same current observables.

## Minimality result

| Observation view | Open/closed | Undo/reset | Boundary pause |
|---|---:|---:|---:|
| first action only | 0.4260 | 0.4421 | 0.4279 |
| first two actions, no latency | 0.7444 | 0.5403 | 0.4127 |
| first two actions + latency | 0.9626 | 0.9903 | 0.9991 |

The result does not support a universal statement that two actions are always sufficient. Under this probe design, the smallest robust extension is **the second action plus inter-move latency**. Action identity alone remains partial or non-identifiable for the principal open/closed-loop and recovery contrasts.

## Noise stress

A second audit independently applies:

- 8% action-slip probability at each observed move;
- multiplicative latency noise with log-scale sigma 0.25;
- coherent recomputation of intermediate states and score deltas.

Under the minimal two-action-plus-latency view:

| Contrast | Noisy mean balanced accuracy |
|---|---:|
| open/closed | 0.9205 |
| undo/reset | 0.9086 |
| reset/persist | 0.9488 |
| boundary pause | 0.9365 |
| object/viewer | 0.8477 |
| identical latent negative | 0.4250 |

All preregistered robustness conditions pass.

## External trajectory sources

### WCA Results Export

The official WCA v2 export observed on 2026-08-03 reports format 2.0.2 and an August 2, 2026 snapshot. It contains competition metadata, competitors, official results, individual attempts, and official scrambles. It does not contain executed solution sequences, per-move timestamps, or cognitive annotations.

The 352 MB TSV archive was not materialized into the repository. This version therefore certifies the source schema and linkage contract, not a full WCA cohort analysis.

### reco.nz

The public reconstruction database exposes scrambles, reconstructed move sequences, method-stage comments, movecount, TPS, official/unofficial labels, competition information, and source attribution. It is used here for notation fixtures, stage-boundary fixtures, route motifs, and external trajectory-shape priors.

A matched-scramble fixture demonstrates a useful empirical fact: solve IDs 9269 and 9274 report the same scramble and the same total time, 4.54 seconds, but different move routes and reported STM counts, 41 and 45. The same state and total time therefore do not identify a unique trajectory.

This does not justify attributing different latent cognitive traits to the named solvers. reco.nz itself cautions that short one-look puzzles such as 2x2 do not disclose what was behind the solution without the solver explaining the thought process.

### Smart-cube and timer data

csTimer can export user-owned solve histories and supports Bluetooth-cube input. Cubeast records and analyses Bluetooth-cube solves and can generate shareable solve links. Solved provides a shareable reconstructor. These are candidates for true per-move timestamps, but only through explicit owner export or intentionally shared links. No account scraping or unconsented cohort collection is authorized.

## External linkage dry run

A separate linkage adapter normalizes result time and scramble text, hashes the scramble, and distinguishes:

- `EXACT_UNIQUE` — one matching event/date/time/scramble attempt;
- `AMBIGUOUS_MULTIPLE` — more than one matching attempt;
- `UNLINKED` — no exact candidate.

The dry run passes all three cases. Actual WCA–reconstruction joins remain held until the versioned WCA archive is materialized, hashed, and audited.

## Nonreactivity firewall

The proposed trial contract records at most three moves, intermediate state hashes, action timestamps, and inter-move latency. It does not collect trialwise confidence, strategy names, error admissions, or planning-depth reports. No correctness or strategy feedback is shown. Existing post-task global demand capture remains the only self-report boundary.

## Evidence boundary

### Certified

- exact legal-state generation from certified parents;
- six unique rotational families and 36 probes;
- exact move conjugation under all proper whole-cube rotations;
- balanced planned and recovery faces;
- dense recovery opportunities;
- balanced 12-schedule design;
- synthetic identifiability and negative controls;
- robust action/latency noise audit;
- external source-role registry;
- matched-scramble route nonuniqueness fixture;
- exact/ambiguous/unlinked linkage adjudication contract.

### Not certified

- any human cognitive mechanism;
- ecological validity of synthetic latencies;
- bulk WCA/reco.nz cohort ingestion;
- per-move timing from public video reconstructions;
- a consented smart-cube cohort;
- participant-facing trajectory UI;
- Collector or Factory support for trajectory records;
- deployment or recruitment.

## Decision

CUBE-REV 0.8.16 closes the research-asset design and synthetic falsification stage. It does not modify the participant instrument. The next promotion must first build an offline executable trajectory route and certify that the additional actions and timestamps do not alter the original first-action estimand.

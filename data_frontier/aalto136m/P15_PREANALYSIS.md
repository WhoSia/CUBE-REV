# G3-P15 preanalysis constitution

## Stage and inheritance

**Stage:** CUBE-REV Generation III G3-P15 — Aalto 136M Keystrokes Immutable
Acquisition, Error-State Persistence Reconstruction, Repeated-Error Hazard,
Bidirectional Peri-Error Dynamics & Cross-Corpus Failure-State Discrimination
Preseal.

This document was frozen before any substantive Aalto result was inspected.
It inherits only the following P14-R2 result: WCA contains a robust DNF
clustering signature (DNF-to-DNF 6.465% versus VALID-to-DNF 1.961%;
structure-preserving permutation p=0.005), but no general attempt-order serial
signal and no cognitive-recovery promotion. P15 asks whether an analogous
**failure-state persistence** structure is visible in a different naturalistic
motor-performance corpus. It does not reopen Paper 1.

## Epistemic ceiling

The corpus records keystrokes in a self-selected online transcription task. It
does not measure attention, fatigue, planning, memory, practice exposure, or a
cognitive state. Permitted language is *failure event*, *behavioral
sequential signature*, *observed typing-performance trajectory*, and
*post-error transition*. Forbidden endpoint labels include cognitive recovery,
attention lapse, mental fatigue, planning failure, and cognitive failure state.

## Acquisition and source-integrity gates

No scientific estimand is evaluated until all of the following are recorded:

1. original-source URL, acquisition time, response metadata, archive byte size,
   SHA-256, member census, and license/readme byte hashes;
2. immutable restricted/research-use custody, with raw and large derived
   material excluded from Git history;
3. an independently measured final-input versus keystroke-reconstruction
   disagreement rate; both representations remain available;
4. a documented participant-metadata join test. An undocumented or nonunique
   join is `NOT_AUTHORIZED`; no demographic or training covariate then enters a
   confirmatory model.

The keystroke reconstruction becomes the primary representation only if its
online compiler is explicit, its end-state reconstruction is auditable, and
the final-input disagreement sensitivity is completed.

## Error-state compiler contract

The compiler never equates Backspace/Delete with error. It emits the following
mutually traceable labels:

- `TARGET_MATCH_KEY`
- `TARGET_MISMATCH_KEY`
- `CORRECTION_KEY`
- `CORRECTED_ERROR_EPISODE`
- `UNCORRECTED_ERROR`
- `AMBIGUOUS_EDIT`
- `STREAM_RECONSTRUCTION_MISMATCH`

It consumes target text, the ordered observable key stream, and press/release
times. It preserves raw key identity and timing. It makes no unobserved
mouse/cursor/selection repair: when the edit path is not uniquely reconstructible
the event is marked ambiguous. A primary error event is an episode-collapsed,
uniquely reconstructed mismatch episode; sensitivity analyses retain key-level
events and exclude ambiguous or final-input-disagreeing transcriptions.

Synthetic tests must cover insertion, substitution, deletion, correction by
Backspace, uncorrected error, and ambiguous edit paths before corpus execution.

## Timing constitution

For valid events retain press time, release time, dwell, press-to-next-press
IKI, release-to-next-press flight, and a rollover indicator. Raw timing is not
silently clipped. The primary non-pause timing window is 15--2,000 ms; 15--1,000
ms and 15--5,000 ms are prespecified sensitivities. Values below 15 ms and
rollover observations are retained in a separately flagged channel rather than
used to support mechanistic timing claims. Effects comparable to the reported
10--15 ms instrumentation scale receive no mechanistic interpretation.

## Estimands

### Descriptive atlas

Report transcription and typist coverage, stream-state census, target/final/
reconstructed agreement, error-episode count, correction use, timing coverage,
rollover, baseline error propensity, typing-speed distribution, and exposure
depth. These are descriptive only.

### Primary repeated-error hazard

For each prespecified lag **j in {1, 2, 3, 4, 5, 8, 12}**, estimate the
episode-collapsed probability of a subsequent uniquely reconstructed error event
after an error event, compared with matched correct-event anchors. The primary
contrast is within typist and conditions on exact target key where observable,
sentence/transcription identity where useful, character and word position,
local target bigram/context, and preceding non-pause IKI difficulty bin.

Report risk difference, risk ratio, typist-resampled uncertainty, the full lag
curve, and a within-typist structure-preserving null. No lag selected after
inspection receives special status.

### Persistence-length discrimination

Discriminate these prespecified rivals:

- **POINT_ERROR:** no excess hazard once local difficulty is conditioned on.
- **SHORT_PERSISTENT_STATE:** bounded, decaying excess across future lags.
- **SLOW_CONTEXT:** contextual key/bigram/word/sentence difficulty explains
  the cluster.
- **PERSON_PROPENSITY:** stable typist error rate explains the cluster.
- **EDIT_EPISODE_ARTIFACT:** multiple keys from one correction episode create
  artificial recurrence.

The primary estimate is episode-collapsed; key-level recurrence is diagnostic
only and cannot establish persistence by itself.

### Secondary bidirectional timing-state analysis

Compare residual flight and dwell in prespecified pre-error (-5 to -1), error,
and post-error (+1 to +5) windows with context-matched correct anchors.
Rollover and execution-difficulty explanations are explicit rivals. This is a
secondary discriminator, not a test of cognitive recovery or anticipation.

### Skill/trajectory stratification

Use only intrinsically derived early-stream measures: high/low baseline error
propensity and high/low typing speed. No future information defines an early
stratum. Describe transcription-order trajectories as observed exposure, not
total practice history.

## Mandatory negative controls and sensitivities

1. within-typist local permutation preserving error count;
2. context-matched correct-event controls;
3. episode-collapsed versus key-level analysis;
4. reverse-time comparison;
5. high/low baseline-error and typing-speed strata;
6. sentence-position and local-context strata;
7. exclusion of final-input/stream-reconstruction disagreement cases;
8. the three frozen pause windows and a rollover-excluded timing analysis;
9. source-status and incomplete-stream census.

Typist is the top-level resampling unit. Nominal p-values never substitute for
effect magnitude, null distribution, typist-resampled uncertainty, or
cross-stratum stability.

## Promotion ladder and adjudication

`NO_SIGNAL` → `DESCRIPTIVE_POPULATION_STRUCTURE` →
`BEHAVIORAL_SEQUENTIAL_SIGNATURE` → `ROBUST_NATURALISTIC_SIGNAL` →
`COGNITIVE_SIGNAL_CANDIDATE` is the general vocabulary ladder; P15 cannot
promote beyond structural cross-corpus support and cannot use the final label.

Allowed P15 verdicts are `ACQUISITION_HOLD`, `SOURCE-INTEGRITY_HOLD`,
`NO_ERROR-STATE_PERSISTENCE`, `CONTEXT-EXPLAINED_ERROR_CLUSTERING`,
`WITHIN-CORPUS_ERROR-STATE_PERSISTENCE`, and
`CROSS-CORPUS_FAILURE-STATE_PERSISTENCE_SUPPORTED`.

The highest verdict requires all seven conditions: episode collapse; typist
baseline adjustment; local key/bigram/position controls; disagreement
sensitivity; nontrivial magnitude; interpretable short-range decay; and a
result not reducible to correction-key mechanics. Failure of any condition
keeps the lower verdict and is preserved as a result.

## Cross-corpus transport rule and successor gate

P15 compares structural patterns, never the numerical size or cognitive meaning
of WCA DNF and typing-error events. Its transport table must retain their
different resolution, local difficulty, and selection threats.

No EdNet download follows automatically. It may be promoted only if an observed
P15 ambiguity specifically requires a learning/history comparator. Aalto support
would motivate cross-domain state-persistence geometry and common-cause attacks;
context explanation would return the mechanism attack to WCA; G4 human contact
remains dormant unless secondary-data identification reaches a specific ceiling.

# G3-P14-R2 results and scientific verdict

## Verdict

**ROBUST_NATURALISTIC_SIGNAL_DNF_CLUSTERING / NO_GENERAL_ORDER-SPECIFIC_SERIAL_SIGNAL / NO_COGNITIVE_RECOVERY / DESCRIPTIVE_SKILL-TRAJECTORIES_ONLY**

P14-R2 identifies a bounded naturalistic signal: DNF events cluster within observed WCA 3x3 rounds. It does not identify cognitive recovery, attention failure, planning, memory, or a learning mechanism. The dominant VALID-to-VALID residual association is not distinguishable from a within-result order-permutation null, and both pre-DNF and post-DNF VALID attempts are slower than ordinary neighboring VALID attempts.

## Provenance closure

- Export format/version: v2.0.2, anchored 2026-09-14T00:00:16Z.
- Raw TSV ZIP: 376,033,641 bytes; SHA-256 95ab3be3db10ca759e2328b6a487e592d8ce206352f77e689dd7681b681d9482.
- Derived Drive package: 99,376,424 bytes; SHA-256 694fca87aacc9a0dd71331d478af3b574b20cd560c3ee36399ff84f275ca8e75.
- Attempt Parquet SHA-256: 6840d5441fecc7b0e37159fba5b27fe0ee018110ca809afb78bc5c104d579727.
- Longitudinal index SHA-256: 4ef5f4620b876ca1ab69440daabc3f78f85f2e3c0606ec181f5da3af4798e635.
- Acquisition workflow run 34910083516 and four-part split run 34910991071 completed successfully.
- The separate legacy UI static-validation failure concerns historical HTML byte parity and is repository housekeeping, not a P14 data/compiler failure.

All 9,278,024 primary keys are unique. Counts reproduce exactly: 9,084,452 VALID, 189,559 DNF, 4,013 DNS, zero NO_RESULT rows, zero unexpected codes, and zero status/time mismatches. NO_RESULT remains a distinct compiler/schema state despite its zero realized count.

## Population atlas

The atlas covers 285,697 competitors and 15,316 competitions from 1982-06-05 through 2026-09-13. The median competitor has one observed competition; the 90th percentile has seven and the 99th percentile 39. Median observed longitudinal span is zero years, the 75th percentile is 1.076 years, and the 99th percentile is 10.771 years. This depth imbalance makes participation selection a first-class property of every trajectory estimate.

Calendar-time medians changed from 31.50 s in the sparse 1982 material to 13.79 s in partial-year 2026. This is a population mixture, cohort, competition-composition, and within-person combination; it is not an individual learning curve. Annual entrant/returner counts, quantiles, DNF/DNS rates, concentration, and round/format composition are in p14_r2_summaries.

## Within-round sequential dependence

Across positions 1–5, the leave-result-out competitor residual changes from +0.475% at attempt 1 to -0.286% at attempt 5, a small monotone descriptive shift of about 0.76%. The estimand is conditional on an observed attempt.

The adjacent adjusted-residual correlation is large (r=0.548, n=6,678,418), but a structure-preserving within-result permutation yields observed 0.5557, null mean 0.5551, Monte Carlo p=0.32 in the frozen hash-selected 18,539-block audit. The dominant association therefore reflects shared round/competitor/context geometry that does not require actual attempt order. It is not promoted as an order-specific sequential signal.

Format audit shows that modern format a overwhelmingly has five observed rows, while old format h and rare cutoff-like structures have variable observed lengths. All transition estimands are therefore stated conditional on an observed next attempt and are stratified or sensitivity-checked by format and round type.

## DNF transition geometry

Among adjacent observed attempts:

- after DNF: next-attempt DNF 9,521 / 147,263 = 6.465%;
- after VALID: next-attempt DNF 142,590 / 7,269,723 = 1.961%;
- after DNS: next-attempt DNF 17 / 2,184 = 0.778% (small and composition-sensitive).

In the frozen 18,539-block permutation audit, repeated-DNF probability is 7.249% versus null mean 6.067%, upper-tail Monte Carlo p=0.005. The excess is present across major positions and both final/non-final strata, though magnitudes vary by era and round composition.

There is no performance-recovery signature. After exact prespecified cell matching on predecessor position, finality, era, format, round type, early-skill quartile, and observation depth, the next VALID is +1.63% slower after DNF in finals (11,282 DNF predecessors across 76 supported cells) and +3.37% slower in non-finals (103,465 across 373 cells) than after a VALID predecessor.

The reverse-time placebo is also positive: 125,012 VALID attempts immediately before a DNF average +2.02% on the adjusted log scale, while 117,681 immediately after a DNF average +2.88%; ordinary VALID neighborhoods average approximately -0.09%. This bidirectional signature downgrades recovery and supports a persistent low-performance neighborhood, regression-to-the-mean, and/or selection mixture.

## Skill trajectories

Competition-index curves show strong observed improvement among returners: relative to competition 1, the mean log-time difference reaches approximately -43.2% by competition 10 (n=21,319 at index 10). The curve is steeper in initially slower strata and flattens with competition index. For competitors observed at 20+ competitions, mean log-time from index 1 to 10 changes by about -36% in initial-skill quartile 1 and -54% in quartile 4.

These are observed competitive-performance trajectories. Attrition is extreme (284,910 at index 1 versus 21,319 at index 10), initial skill is defined only from early observations, and WCA participation is not total practice exposure. Therefore P14-R2 admits descriptive heterogeneous trajectory geometry but not a learning mechanism.

## Promotion ladder

| Object | Level | Reason |
|---|---|---|
| Population and trajectory atlas | DESCRIPTIVE_POPULATION_STRUCTURE | Large, reproducible structure; selection and unobserved practice prohibit mechanism claims |
| Attempt-position shift | BEHAVIORAL_SEQUENTIAL_SIGNATURE | Small within-person descriptive gradient; conditional on observed attempt |
| VALID residual serial correlation | NO_ORDER-SPECIFIC_SIGNAL | Does not reject within-result order permutation |
| DNF clustering | ROBUST_NATURALISTIC_SIGNAL | Large denominator, cross-stratum persistence, and structure-preserving null rejection |
| DNF recovery | NO_SIGNAL | Direction is slower, not faster; reverse-time placebo is also present |
| Cognitive interpretation | NOT_PROMOTED | Attempt-level telemetry cannot discriminate the required cognitive mechanisms |

## Comparator gate and successor

One concrete ambiguity remains: whether the bidirectional slowdown and repeated-error hazard around DNF-like events is a generic fine-motor/error-state persistence signature or a competition-format/selection phenomenon specific to WCA. Aalto 136M Keystrokes can test the prespecified comparator estimand error event → repeated-error hazard plus pre/post inter-key slowing at finer temporal resolution. Aalto is therefore promoted to acquisition-next for P15, subject to its research/non-commercial terms and a new immutable acquisition receipt.

EdNet remains QUALIFIED_NO_DOWNLOAD_YET: P14-R2 does not yet require a non-motor adaptive-learning corpus to distinguish the live ambiguity.

## Authority boundary

Paper 1 (BR-Org-26-1124) remains sealed. P12 ΔR and G4 human Cube↔Navigation contact remain dormant/deferred. No public release, Zenodo change, journal action, human recruitment, Aalto download, or EdNet download occurred in P14-R2.

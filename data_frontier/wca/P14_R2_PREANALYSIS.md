# G3-P14-R2 preanalysis constitution

## Stage and frozen source

**Stage:** CUBE-REV Generation III G3-P14-R2 — WCA Longitudinal Population-Dynamics Atlas, Within-Round Sequential Dependence, DNF-Recovery Geometry, Skill-Trajectory Stratification & Naturalistic Cognitive-Signal Qualification.

The sole primary source is the already acquired WCA Results Export `v2.0.2` anchored at `2026-09-14T00:00:16Z` (TSV ZIP SHA-256 `95ab3be3db10ca759e2328b6a487e592d8ce206352f77e689dd7681b681d9482`). Analysis uses the P14-R1 3x3 attempt spine with 9,278,024 rows. No source reacquisition, outcome-driven cohort replacement, or comparator download is authorized.

`competitor_key` is a deterministic key derived from a public WCA identifier. It is not an anonymization guarantee.

## Epistemic ceiling

The source is attempt-level competition telemetry. It contains neither moves nor direct measurements of attention, planning, memory, learning mechanism, or cognitive state. Allowed default terms are **behavioral sequential signature**, **post-DNF transition**, and **observed competitive-performance trajectory**. DNF does not prove attentional failure; a faster later attempt does not prove cognitive recovery; an observed trajectory does not identify total practice exposure or a learning mechanism.

## Frozen estimand families

### A. Descriptive population atlas

By calendar year, with era summaries where sparse early years require pooling:

1. number of competitions, rounds/results, attempts, active competitors, first-observed competitors, and returning competitors;
2. VALID, DNF, DNS, and NO_RESULT counts and rates, preserving all four source states;
3. VALID solve-time quantiles (p10, p25, p50, p75, p90) on raw seconds and log-seconds;
4. within-person attempt depth, competitions per competitor, and observed longitudinal span;
5. round-type and format composition;
6. participation concentration: top 1%, 5%, and 10% shares of attempts, plus an attempt-share Herfindahl index;
7. entrant/veteran mixture and decomposition of annual median log-time into within-competitor and changing-population components where overlap permits.

These are descriptive statistics for observed WCA competitors, not population-representative estimates.

### B. Within-round sequential dependence

The analysis unit is a VALID attempt or an adjacent observed attempt pair within the same `result_id`.

Primary estimands:

1. attempt-position differences in log solve time, reported within competitor and within competition-year/round-type/format strata;
2. adjacent residual association: slope/correlation of attempt `k+1` residual on attempt `k` residual after subtracting a leakage-safe competitor baseline and context-position cells;
3. heterogeneity of direction and magnitude across early-skill quartile, era, format, round type, and observation-depth stratum.

The leakage-safe competitor baseline uses only observations outside the focal result. Rows without an observed next attempt define no adjacent transition and are counted separately. The estimand is explicitly conditional on an observed next attempt. Same-round mean normalization is forbidden because it mechanically induces dependence.

### C. Post-DNF transition geometry

Primary objects:

1. transition counts and row-normalized probabilities among VALID, DNF, DNS, and NO_RESULT for adjacent observed attempts;
2. next-attempt DNF probability conditional on predecessor state, by position and strata;
3. next-VALID log-time residual after DNF versus a matched/stratified VALID predecessor;
4. repeated-DNF clustering and run lengths;
5. position-specific pre-DNF and post-DNF residual profiles.

Matching/stratification uses predecessor attempt number, era, format, round type, early-skill stratum, and observation-depth stratum. It never treats DNS as DNF.

### D. Skill trajectories

Two clocks are mandatory: calendar date and time since first observed competition / competition index. Initial-skill quartiles use only the first two competitions with at least three VALID attempts in total; no future observations enter stratum assignment. Competitor×competition aggregates may be used for trajectories.

Report early change (competition indices 1–5), later slope/plateau (6+), within-person volatility, return after gaps, participation-depth dependence, initial-skill heterogeneity, and cohort/era differences. Observed WCA history is not total practice exposure.

## Negative controls and rival attacks

All primary sequential and DNF results face the following fixed attacks:

1. final versus non-final rounds;
2. competition/round composition, format, and era stratification;
3. initial-skill and observation-depth strata;
4. entrant versus veteran population;
5. missing-next-attempt and incomplete-round structure;
6. DNF versus DNS predecessor comparison where supported;
7. reverse-time placebo comparing the preceding VALID residual around DNF;
8. deterministic structure-preserving null: permute attempt order within eligible `result_id` blocks while preserving their observed values and statuses. Seed is `314159`, with 199 permutations for summary-level tests;
9. exposure/selection sensitivity: repeat within non-final rounds, fixed common formats, and competitors with at least five observed competitions.

Signals that disappear under a reasonable prespecified attack are preserved as evidence against the stronger interpretation.

## Inference and uncertainty

Effect sizes and stratum consistency take priority over very small p-values at this scale. Cluster-robust or competitor-block bootstrap intervals are used when feasible. Machine summaries retain exact denominators. No arbitrary significance threshold can rescue an inconsistent or selection-sensitive result.

## Cognitive promotion ladder

The maximum possible P14-R2 level is `COGNITIVE_SIGNAL_CANDIDATE`:

`NO_SIGNAL` → `DESCRIPTIVE_POPULATION_STRUCTURE` → `BEHAVIORAL_SEQUENTIAL_SIGNATURE` → `ROBUST_NATURALISTIC_SIGNAL` → `COGNITIVE_SIGNAL_CANDIDATE`.

Promotion beyond `BEHAVIORAL_SEQUENTIAL_SIGNATURE` requires reproducible direction across major strata, survival of exposure/selection controls, discrimination from DNS and reverse-time patterns, rejection of the structure-preserving null, and a prespecified mechanism rivalry that the observed signature distinguishes. P14-R2 cannot establish a cognitive mechanism.

## Comparator acquisition gate

Aalto 136M Keystrokes and EdNet remain `QUALIFIED_NO_DOWNLOAD_YET`. At adjudication, acquisition is promoted only if P14-R2 leaves a named ambiguity that the specific second corpus can distinguish: motor/error-recovery microdynamics for Aalto, or non-motor sequential-learning/history for EdNet.

## Stop and hold rules

Unexpected attempt codes, checksum mismatch, broken primary-key semantics, or irreconcilable source-schema drift halt substantive analysis. Sparse cells are pooled only by the rules above or reported unavailable. Paper 1, human G4 recruitment, P12 ΔR, public release, Zenodo, and journal actions are outside this stage.

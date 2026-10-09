# CUBE-REV 0.19 — P8: Order-Invariant Fractional Proofs, Five-Source Separation and Dual-Guided Six-Word Conflicts

## Frozen physical ontology and exactness status

A tracked UR edge starts in one of twelve original edge positions, intrinsic flip zero, undergoes exactly five sticker-derived legal HTM actions, and emits one intrinsic flip bit after each action. A dictionary of nonadaptive fixed physical words covers every admitted original known-source subset A if one word's full five-bit history is injective on A. There are exactly **1,192 original sources**, including 480 five-position requirements and 64 four-position requirements surviving the exact L5 row quotient. The optimum dictionary cardinality **M*(5) is an integer** and still has independently verified local **6 <= M*(5) <= 8**. Neither ordinary LP fractions nor an unconfirmed numerical MIP infeasibility verdict settle k=6 or k=7.

L6 physical optimum **M*(6)=4** is locally complete finite checked in P7 (full GitHub CI receipt pending); independently DRUP-checked L4 optimum is **M*(4)=34**. Do not promote a new L5 exact number without an actual physical witness or external UNSAT checking.

## New exact five-source-only fractional optimum

Consider the subfamily of **all original 480 five-position sources** (none of the 64 four-position sources). Over the same 14,446 physically generated distinct five-turn source-coverage types, the **standard real-valued set-cover LP** has optimal cost:

`OPT_LP(L5, five-source-only) = 185/39 = 4.743589743589... exactly.`

This was computed and then certified by **two exact rational witnesses** built from the sixteen verified physical-source incidence automorphisms, not by trusting approximate LP objectives:
- 37 orbits of admitted five-position requirements and 196 physically generated maximal experiment-column orbits in the 544×2,887 quotient.
- Nine primal column orbits, a total of **106 actual physical source-coverage masks**, with common denominator 312. For every one of the 480 original five-position source requirements, the weighted sum of distinguishing physical experiments is >=1. Total primal cost is exactly 185/39.
- Nine positive dual row orbits, represented on **80 original five-position source constraints** with common denominator 312; total dual weight 185/39. For *all 14,446 distinct physically realized source-coverage types*, the sum of covered dual weights is <=1. Thus the dual certifies the matching lower bound.
- All physical masks and source rows are identified in the **original frozen 1,192-row coordinate system**, not by rank-dependent or enumeration-order-dependent reduced column indices. Exact separate local checker PASS.

## Consequence: an exact marginal cost for 64 mixed four-source requirements

The original **all-1192-source LP optimum** is already exactly 16/3 = 208/39: independent full-source rational primal uses eight physical incidence orbits / 96 actual physical masks; nonnegative integer dual is 70 source weights, total 384, per-word capacity 72 (giving 384/72).

Therefore the exact increase in the fractional relaxation's optimum when adding the 64 retained mixed four-source constraints to the 480 five-source constraints is

`OPT_LP(all 1192) - OPT_LP(five-only 480) = 208/39 - 185/39 = **23/39**.`

This **does not** mean 23/39 of a physical experiment can be executed, and is NOT the change in the unknown *integer* minimum. It demonstrates precisely that the admitted *source-family ontology* affects even the relaxed physical identification cost, beyond the number of available observation bits.

## New k=6 exact pair-obstruction lemma and physical count

From the original 70-row integer covering dual, total required weighted demand W=384 and every single genuine physical five-turn experiment has weighted score at most B=72. For a hypothetical cover D of <=k words and any t selected words T, their weighted source union must satisfy

`U(T) >= W-(k-t)*B.`

For k=6:
- t=1 forces **every selected word's dual coverage mass >=24**; among all 2,887 undominated physical reduced columns exactly **1,877 are eligible**, and **1,010 are ineligible**.
- t=2 forces **each pair of selected words to jointly cover dual mass >=96**. Checking all C(1877,2)=**1,760,626** pairs with exact integer dot products of their physical 70-row dual incidence, **1,194,707 pairs are impossible** (weighted union strictly <96), leaving 565,919 pairwise-compatible pairs.
- These 1,194,707 valid Boolean clauses `not x_i OR not x_j`, plus 1,010 exclusion unit clauses, are sound consequences of the **original** full 1,192-row cover condition plus cardinality <=6. They have been integrated into the GitHub k6 SAT court. Count of forbidden pairs can be checked independently from the full 70-row dual and actual coverage masks; this is a necessary condition, not a k6 UNSAT proof.
- For k7 the preexisting dual's pair threshold is merely 24, giving 247,348 valid forbidden pairs (already integrated in the k7 court); k6 reasoning must NOT be incorrectly applied to k7.

Thus under k6 the dual-based forbidden-pair graph is extremely dense (~67.9% of all eligible candidate pairs), giving a mathematically grounded new branching and propagation device. It does not by itself rule out a compatible six-word clique or satisfy all 544 set-cover constraints.

## Why order-invariant proof identifiers matter

The previous P3 certificate keyed witness columns by reduced integer indices such as 0,4,112. The P3 local C++ physical partition exporter iterates an unordered-map collection whereas the current GitHub JavaScript exporter preserves first-insertion order under a different word traversal. The **physical set of columns is unchanged**, but their **array indices are not invariant** under such a change. Reliance on matching column IDs risks a false reproducibility failure (or an incorrect witness correspondence) despite identical original source-coverage geometry.

P8 re-expresses both the full 16/3 proof and the five-only 185/39 proof using SHA-locked full **1,192-bit source-coverage masks** as representative identifiers. The independent verifier recomputes all 14,938 actual five-HTM observation partitions, checks exactly 14,446 unique original source-coverage types, verifies every 16-element signed-coordinate orbit and each physical mask's existence, and checks all primal original-row coverage and dual original-column capacities with **integer/fraction arithmetic only**.

Locally reproduced exact certificate log:

```
CUBE_REV_019_L5_ORDER_INVARIANT_EXACT_FRACTIONAL_PROOF_PASS ALL_1192 objective 16/3 real_physical_masks 14446 rows 1192 fractional_word_support 96 primal_orbits 8 positive_dual_rows 70 denominator 72
CUBE_REV_019_L5_ORDER_INVARIANT_EXACT_FRACTIONAL_PROOF_PASS FIVE_ONLY_480 objective 185/39 real_physical_masks 14446 rows 480 fractional_word_support 106 primal_orbits 9 positive_dual_rows 80 denominator 312
CUBE_REV_019_L5_64_FOUR_STATE_RESTRICTIONS_RAISE_EXACT_FRACTIONAL_OPTIMUM_BY_23_OVER_39_PASS
```

The existing five-source-only k=5 mixed-integer feasibility court reported numerical infeasible (HiGHS) on original 480 requirements in roughly ten seconds, but this **is NOT an independent proof of UNSAT**; a verified SAT/DRUP or other finite certificate is still required to infer the *integer* five-source optimum >=6. A separate six-word numerical search timed out with UNKNOWN. Do not mislabel either result as proven.

## Executable proof and storage

- [Full 1192-source original-mask primal/dual certificate](P8_ORDER_INVARIANT_L5_FULL_LP_CERT.json).
- [Five-only 480-source original-mask primal/dual certificate](P8_ORDER_INVARIANT_L5_FIVE_ONLY_LP_CERT.json).
- [Independent, no-solver, order-invariant exact arithmetic court](../../scripts/cuberev-019/verify-L5-order-invariant-LP.py).
- [Five-turn proof producing k7/k6 physical SAT court](../../scripts/cuberev-019/prove-L5-k7-k6.py), updated to require the P8 order-invariant proof and impose the exact k6 weighted pair cuts.
- Drive source+proof custody folder: https://drive.google.com/drive/folders/1DboAVDmbMmOXD7CMgznchCMX2RIRxrCf .
- Parent research authority: https://app.notion.com/p/3f4ef561cf92813d9edfff4911db39d2 .
- The CI for this P8 proof should produce a **new verified receipt** before stating GitHub external PASS. Locally verified equality of rational upper and lower bounds is already a complete finite arithmetic argument, but distinct from a remotely checked CI execution.

## Next exact integer frontier

1. Obtain an externally independently checked DRUP/FRAT/VeriPB negative certificate for the 480-five-source 5-word subsystem. If such a proof succeeds, any full 6-word dictionary must use six rank>=5 physical experiments.
2. Use source-locked 16-element incidence symmetries and the k6 1,010 unit exclusions / 1,194,707 pair clauses to attack the five surviving k6 first-word orbit representatives, without guessing a stronger LP bound (full LP is **exactly** 16/3).
3. Attack k7 separately with the valid weaker 247,348 pair conflicts; construct an actual 7-word physical cover or independently check its UNSAT proof. Neither a time-limited solver UNKNOWN nor a numerical MIP infeasibility verdict is a theorem.
4. Reuse collision-hypergraph proof methods from L6, not the L6 optimum itself; every transferred dominance lemma must be re-audited on the original 1,192-source L5 coverage family.

## Relevant external proof-methodology

- Procacci–Sanchis, *Perfect and separating hash families: new bounds via the algorithmic cluster expansion local lemma*, arXiv:1601.05389 — prior art for perfect hashing, not CUBE-REV-specific novelty.
- Shangguan–Ge, *Separating hash families: A Johnson-type bound and new constructions*, arXiv:1601.04807 — combinatorial graph and additive arguments; theoretical inspiration, not an existing proof of our particular physical instance.
- Bogaerts et al., *Certified Dominance and Symmetry Breaking for Combinatorial Optimisation*, JAIR 2023, DOI 10.1613/jair.1.14296 — framework for proof-producing source-preserving reductions.
- Koops et al., *Practically Feasible Proof Logging for Pseudo-Boolean Optimization*, CP 2025, DOI 10.4230/LIPIcs.CP.2025.21 — appropriate proof-certificate route for advanced cutting planes and integer selection constraints, rather than over-interpreting HiGHS status.

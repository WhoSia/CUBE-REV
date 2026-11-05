# CUBE-REV 0.28 — R14-P4: Exact Partial-Color Completion Counts by Parity-Tracked Matching DP

**Date:** 2026-11-05. **Scientific status:** executable exact finite combinatorial algorithm, independently compared against full enumeration on a 5-edge/3-corner legal residual court. The full-size 12-edge/8-corner *unobserved* count is calculated without enumerating any factorial assignment. This is NOT a novel permanent algorithm claim, NOT a full-size physical P48 observation replay, and NOT an 18/19/20-frame policy proof.

## 1. Mathematical state and recurrence

For n spatial positions and n original cubie labels, consider each source label j at destination i with orientation o modulo q (q=2 for edges; q=3 for corners). A partial color-reading constraint is an ordered list of fixed spatial sticker slot/color pairs. A transition assigning (j,o) at i is permitted exactly when the ordered source colors under orientation o agree with all currently observed sticker colors at destination i.

Maintain a DP indexed by

    (used_source_labels_bitmask, accumulated_permutation_parity, orientation_residue_mod_q).

When assigning source j not previously used, the inversion parity increment is the number of **already selected** labels greater than j, modulo two. The orientation residue is incremented by o modulo q. At the final position, accept only orientation residue zero. The two terminal permutation parities are counted separately. The recurrence's counted branches correspond bijectively to the legal assignments: no loss or duplication from masking and no enumeration of the full factorial state space.

In the absence of restrictions:
- 12-edge per-parity count = 12!/2 × 2^11 = 490,497,638,400.
- 8-corner per-parity count = 8!/2 × 3^7 = 44,089,920.
- Full legal cube count = 2×these products = 43,252,003,274,489,856,000.

These are known group-theoretic counts, not new numerical theorems. Their role here is an exact full-size boundary check for the counting implementation.

For any realized adaptive paired-query transcript h, compute the two parity-count vectors N_E(h), N_C(h) separately using this DP with the transcript's known initial-spatial facelet coordinates. Then

    |B(h)| = N_E(h)[0] N_C(h)[0] + N_E(h)[1] N_C(h)[1].

To evaluate the number of surviving legal states under hypothetical next response colors (u,v) at a chosen edge-facelet i and corner-facelet j, append those two slot-color constraints and rerun the counting recurrence. This produces an exact paired response histogram without enumerating candidate full cube states. In a full game, routing actual fixed dual probes through legal actions must be tracked separately.

## 2. Independent full-enumeration comparison on finite mixed residual court

The standalone Python checker constructs a cyclic color assignment model with five edge labels and three corner labels, enumerates its complete physically-legal *permutation parity/orientation-sum algebraic* state family, and schedules three paired queries adaptively according to preceding colors. It checks every realized transcript:

- 51,840 parity-coupled joint states, including exactly 960 edge and 27 corner states per permutation parity.
- 2,464 distinct adaptive three-pair observation transcripts.
- Every one of those transcripts: parity-DP product count equals direct joint-state enumeration exactly.
- Independent next-query branch census for two same-size-marginal histories: a single identical query has nonzero response class sizes [20,20,20,12] versus [48,24].
- Exact full-cube no-observation state count reproduced as above.

The code has **no imports from repository machinery**. Its cyclic 3-corner sticker triples are *abstract* and NOT a new P48 sticker-position generator. All specific finite-subcourt observation results must retain this restriction. The general parity matching recurrence, however, is a direct mathematical consequence of the cubie-permutation and orientation constraints.

## 3. Complexity and relevance to the main unresolved question

For fixed mod q=2 or 3, a memoized bitmask recurrence requires at most O(n·2^n·2q·nq) primitive candidate checks with simple caching and up to O(2^n·2q) memo states (depending on the state indexing/implementation). Unlike enumeration of n! label assignments times q^(n-1) orientations, this is tractable even for 12 edges and 8 corners for a *single exact posterior count*.

The next hard step is **not** to claim that counts solve minimax: distinct information states with identical four parity-class counts can give different future observation partitions, as R14-P3 already proved. To solve a 20-frame adaptive policy one must preserve *entire branching structure* for future queries, including each observation-conditioned matching set and possible physical turn routes. The matching DP is an exact counting oracle supporting that higher-level search, not a sufficient belief quotient on its own.

## 4. Custody and verification

- Active code: `scripts/cuberev-observation/audit_r14_p4_matching_parity_dp.py`.
- Original Python in Drive: https://drive.google.com/file/d/16MWCnRCAlw1627eLZp58NZTPTCFKw6or/view
- Exact JSON receipt in Drive: https://drive.google.com/file/d/19mv_bYX7DdhERiSix7N6nWHZJcwF9eVk/view
- Original Python SHA-256: `ef3a7258139a7d7ccfcdc9782b22e98d5c4bbd8ecc512643be68fa8dad833a2f` (6,030 bytes).
- Original JSON SHA-256: `1ef10cc9ba54e6d518c7b07931f9c17a38a0d015b966e3d10c604e2cabdad516`.
- Local execution: PASS; an exact read-only CI gate should compare the JSON receipt fields.
- Drive-byte remote re-read and new GitHub CI: verification status must be stated separately.

No inference about human strategy or cognitive memory follows from this mathematical counting model. The full color-only legal Rubik adaptive horizon remains **18 <= h_adaptive <= 21**.

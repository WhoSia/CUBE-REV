# CUBE-REV 0.28 R9 — Exact Feedback versus Fixed-Query Separation in Physical Edge-Color Identification

**Date:** 2026-11-05. Research status: exact finite 96-state parity-constrained decision-tree enumeration and executable verification; remote CI must be checked separately. Original CUBE-REV ambition remains full-cube observation/action/representation and empirically grounded human reconstruction, not an easier finite paper.

## Mathematical task

Grant the complete true corner state and read both facelets at eight fixed edge positions (16 single-color queries). Exactly four distinct original edge types remain unknown in their positions and orientations. Their type set L is known. Given known corner parity and previously observed edge flip/permutation, the residual permutation parity and flip parity are fixed. There are exactly 4!/2 times 2^3 = 96 legal residual states for each of the four parity combinations.

The next query can access any of the eight remaining spatial edge facelets without physical rotation costs. Define d_fixed as the minimum number of predetermined facelet slots distinguishing all 96 states, and d_feedback as the minimum *worst-case* depth of an exact adaptive tree choosing each query based on earlier color results. These are the same zero-error target and same possible probe slots, differing only by availability of feedback.

## R9 theorem: exact decision-tree gap

All 495 choices of four remaining types and all four prescribed parity combinations were tested.

| Adaptive minimum | Fixed minimum | Four-type sets | Four-parity conditioned instances |
| ---: | ---: | ---: | ---: |
| 3 | 4 | 72 | 288 |
| 4 | 4 | 225 | 900 |
| 4 | 5 | 144 | 576 |
| 5 | 5 | 54 | 216 |
| **Total** | | **495** | **1,980** |

Hence **216 / 495** of the four-edge type sets exhibit a rigorous *one-query improvement in worst-case identification* when observations are selected adaptively. The other 279 sets show no gain. The result is independent of the required permutation/flip parity bits within each instance. No 2-query identifier exists because at most 6²=36 color outcomes could represent 96 states.

The 12 edge color types form the octahedral color graph K_{2,2,2}. For the graph induced by the four remaining edge types, **d_fixed=4 if and only if the graph maximum degree is ≤2** (297 sets). If a face color occurs in three or four leftover edge types, **d_fixed=5** (198 sets). The R8 adaptive classification is d_feedback=3 exactly for P4+K2 (72), d_feedback=5 exactly for K1,4 (6) or a triangle with a pendant edge (48), and d_feedback=4 otherwise (369).

All classification statements are exact *finite-case certificate* claims, not new general active-perception theorems. Symmetry/general theoretical derivations beyond this finite color graph still require work.

## Independent executable proof

The repository source at scripts/cuberev-observation/audit_r9_feedback_fixed_separation.py imports R8 actual P48-generated edge colors and exact parity-conditioned 96-state enumerator.

For each physical residual problem it:
1. Examines every 3- and 4-facelet predetermined query set for injectivity over all 96 configurations; an explicit 5-read schedule is also verified.
2. Recomputes optimal adaptive minimax depth using all eight physical facelet slots and all possible six-color branch partitions.
3. Extracts the concrete feedback query policy and replays all 96 legal configurations against the decision tree (not merely checking a feasibility Boolean).
4. Confirms the results for all 495 four-type sets and all four parity combinations, giving **190,080 replayed state/policy instances**, and independently verifies the graph-degree/fixed-depth classification and count table.

A CI success certificate must be read back before claiming remote success.

## Cost comparison with careful boundaries

Under an expressly hypothetical uniform initial edge state distribution, every remaining four-type set has equal multiplicity. The average *per-type worst-case budget bound*, not actual mean stopping-time, is:

- Feedback: (72·3 + 369·4 + 54·5)/495 = **1962/495 ≈ 3.9636** additional observations.
- Fixed: (297·4 + 198·5)/495 = **2178/495 = 4.4** additional observations.
- Difference in these declared budget statistics: **216/495 ≈ 0.4364** per four-type set.

Adding the common 16-read prefix gives upper budget averages 19.9636 (feedback) versus 20.4 (fixed), but **does not** yield a full cube 20-frame strategy. True complete corners are granted for free and arbitrary physical edge slots may be accessed without legal-turn cost; both relaxations invalidate direct motor-cost or human inference claims.

## What stays unresolved

The R8 natural stage strategy with 16 complete facelet queries followed by four adaptive ones fails in 54 four-edge graph classes. No complete legal 20-frame full-cube color policy has been constructed and no new full-group lower bound beyond 18 is claimed. Current hard result remains:

- full legal cube with two single-six-color facelet probes: 18 ≤ h_adaptive ≤ 21.
- predetermined/nonadaptive full-group minimum exactly 21.
- corner-oracle single-state edge certificate exactly 17, with 14,664 minimal certificates per state.

The R9 result shows a real geometry-driven *feedback benefit* within a parity-constrained residual belief, rather than a broad philosophical assertion that feedback is useful.

## Next R10 research gate

Transfer the explicit color-decision-tree witness to the fully coupled edge+corner sensory state and legal-turn route constraints, without free corner or unconstrained slot access; seek a 20-or-fewer-frame identifying policy, or a stronger adversarial lower bound. If a generalization fails, preserve it as a negative result. Separately, human reconstruction interpretations require independent controlled behavior measurements. This work does not infer human memory or cognitive cost from Rubik combinatorics.

**Evidence custody:** GitHub compact source and CI receipts; P7 registered code; Notion semantic record; private participants' data never published. Human author/committer only and read-only Actions.


## R14 follow-up (2026-11-05): color symmetry orbit certificate

**Precise claim, separate from global R14.** Write the six face colors as three
opposite pairs, and regard each of the twelve legal edge color types as an
edge of the octahedral color graph (K_{2,2,2}). Permute opposite pairs and
independently exchange endpoints within each pair. This gives the color-graph
automorphism group (W=C_2^3\rtimes S_3), order 48, acting on the 495
unordered four-edge-type subsets.

The 495 subsets split into **18 orbits**. The orbit-size distribution is
one size-3 orbit, two size-6 orbits, two size-12 orbits, seven size-24 orbits,
and six size-48 orbits. The exact previously established R8/R9 residual
depth classes are constant on these orbits:

| Adaptive / fixed worst-case reads | Orbits | Four-type subsets |
|---|---:|---:|
| 3 / 4 | 2 | 72 |
| 4 / 4 | 10 | 225 |
| 4 / 5 | 4 | 144 |
| 5 / 5 | 2 | 54 |
| **Total** | **18** | **495** |

The R12 four-edge obstruction is thus exactly two color-graph orbits,
of cardinalities 48 (triangle with pendant edge) and 6 (four-edge star).
This is an algebraic compression of **existing** conditional residual
minimax classification, not a new global depth-20 impossibility theorem.

**Independent finite cross-check.** For each of the 48 induced edge
permutations, factor its 12-point cycle structure into cycle lengths
(lambda_1,\dots,lambda_k). Its fixed unordered four-subsets are the
degree-four coefficient of
(prod_j(1+x^{lambda_j})). Exhaustive integer computation yields
(sum_{w\in W}|\mathrm{Fix}_{\binom{12}{4}}(w)|=864);
Burnside's lemma independently gives (864/48=18).
This equals direct orbit enumeration.

**Reproduction.** Existing active-set script
`scripts/cuberev-observation/audit_r9_feedback_fixed_separation.py`
now supports `--color-orbits` for a fast no-full-minimax orbit/Burnside
check. It derives the edge types from the existing physical P48 source,
but **does not independently replay physical moves** in this fast mode.
The original full R9 audit and its remote evidence remain separate.
The new mode is committed by human writer in
`ce9b709e98f13aaafe5509b33968cd95f0c09b76`;
a read-only remote CI PASS for the new mode is **not yet claimed**.

**Critical R14 scope warning.** Color relabelings preserve the abstract
residual four-edge game's graph structure and its parity-condition-independent
minimax table. They do not automatically preserve a partially observed
spatial facelet mask, a fixed physical sensor position, a specific turn word,
or its HTM action cost. The full joint edge/corner adaptive belief quotient
must verify transition-and-observation equivariance before reducing states
by this symmetry. In particular, 18 orbits here do not solve the original
18–21 adaptive full-cube horizon.

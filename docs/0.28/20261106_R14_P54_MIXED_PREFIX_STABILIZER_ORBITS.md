# CUBE-REV 0.28 R14-P5.4 — Exact Mixed-Prefix Facelet Stabilizer Orbits

**Date:** 2026-11-06. **Status:** finite full-P48 geometric audit PASS on **all 77 profile pairs**, with a mathematically explained exceptional boundary. This is a **spatial-slot pointwise-stabilizer orbit** result, NOT yet a minimal adaptive search-depth result or a proof of literature-first novelty.

## Theorem (one initial facelet observed per distinct visited cubie)

In the standard legal fixed-centre 3×3×3 cube group, fix the spatial coordinates of one chosen facelet on each of `k` distinct edge positions and one chosen facelet on each of `l` distinct corner positions. Let `H_{k,l}` be the subgroup fixing **each such facelet position pointwise**. Let `Q` be the 24×24=576 pairs of one edge and one corner facelet. For all `0<=k<=10` and `0<=l<=6`, the number of `H_{k,l}`-orbits on `Q` is

    N(k,l)=(2k+1)(3l+1)       if (k,l)!=(10,6),
    N(10,6)=400.

The formula counts **available spatial paired-query symmetry classes**, not the number of distinct future candidate-color beliefs. For (k,l)=(1,1), it returns the previous twelve second-query orbits; for (k,l)=(2,2), it predicts **35** third-query orbits after two spatially distinct edge and corner sticker reads.

## Proof of the orbit partition

Fixing even one oriented facelet coordinate of a spatial cubie forces the whole cubie at that coordinate to be fixed with its orientation unchanged, because legal edge orientation is either identity/swap and legal corner orientation is cyclic. Hence on the 24 edge facelet locations there are `2k` singleton orbits (all stickers of visited edges), plus the remaining `2(12-k)` edge facelets; similarly, there are `3l` singleton corner facelets plus `3(8-l)` remaining corner facelets. Any legal H-element respects each singleton and cannot mix the remaining sector with it.

The legal cubie permutation conditions are: edge/corner permutation parities match; total edge flip parity is zero; total corner twist vanishes mod 3. For at least two untouched cubies in each sector, all untouched edge facelets are transitively connected by paired position swaps (compensated by a corner swap) and paired flips; analogously, all untouched corner facelets are transitively connected using compensated edge swaps and opposite twists. To make the Cartesian product of the untouched edge/untouched corner facelet classes a single orbit, one may need to alter the *parity* of the action on one sector while preserving the target facelet in that sector. Whenever at least **three** untouched cubies remain in either sector, this parity adjustment can be made by transposing two untouched cubies other than that target. Thus all `(2k+1)(3l+1)` evident Cartesian blocks are single orbits if at least one sector has >=3 untouched cubies.

The exceptional `(k,l)=(10,6)` leaves exactly two untouched cubies in each sector. Their permutations can only be identity or the transposition, and matching parity forces them to be swapped *together*. The untouched-edge × untouched-corner facelet rectangle (4×6=24 paired queries) consequently splits into **two 12-element** orbits. Every other block remains a single orbit, giving one extra orbit:

    N(10,6)=(2*10+1)(3*6+1)+1=400.

The exceptional orbit-size histogram (size: number of orbits) is `{1:360, 4:18, 6:20, 12:2}`. The four contributions sum to all 576 paired queries.

## Exact 48-sticker executable audit

A P48 3D facelet geometry module independently built in R14-P5.1 is reused as an **explicit declared dependency**. This script does **not** independently reconstruct the physical geometry; the P5.1 source does. For each of the 77 integer pairs `(k,l)` with `0<=k<=10` and `0<=l<=6`, the auditor generates up to 36 explicit 48-slot legal generators: paired odd edge/corner unvisited position swaps, two unvisited edge flips, and opposite unvisited corner twists. Each generator is checked for legal 48-sticker orientation/parity and for fixing the queried coordinates. A BFS on all 576 possible next dual-facelet query locations finds every orbit. For all 76 ordinary pairs the orbit number and entire size histogram match the formula; the exceptional pair yields the two 12-element classes and total 400. The `k=l=2` case is exactly 35 orbits with histogram `{1:24,18:4,20:6,360:1}`.

This method guarantees that the generated subgroup fills each claimed invariant block. Since the full pointwise stabilizer cannot move a visited-coordinate facelet or interchange visited and unvisited cubie positions, the subgroup orbit cover proves the same orbit partition for the **full** pointwise stabilizer, not merely for the listed generators.

## Importance and limitations

This generalizes R14-P5.1's root-second-query orbit classification to diverse mixed observation prefixes, including a precise **joint parity boundary effect**. It supports safe pruning of spatial paired-query action choices as long as the chosen group elements stabilize the *entire realized observation history*, not just the set of coordinates. Here every generated element fixes each observed coordinate, so any transcript's observed colors remain invariant under the left group action. The actual hidden-state posterior also admits color/label automorphisms, which may yield a **coarser** quotient. Do not assert maximality under all possible belief automorphisms. Repeated readings of other stickers on an already visited cubie are covered as spatial slots but are generally predetermined once a cubie is fixed by a *group element*; this is about symmetry of query choices, not information yielded to the observer.

**CRITICAL:** This is not a proof that a 20-frame full adaptive policy exists or does not exist; the open global horizon remains `18<=h_adaptive<=21`. The stabilizer-orbit formula may be a straightforward finite-group consequence in prior literature, and must be subjected to exact-model novelty screening before any priority or innovation claim.

## Canonical evidence

- P5.4 executable 77-profile checker: `scripts/cuberev-observation/audit_r14_p54_mixed_prefix_stabilizer_orbits.py`.
- Source original in Drive: https://drive.google.com/file/d/1aRBSLXTyhbirh4gPRqoiTRPr5yhFI6Lm/view
- Output original in Drive: https://drive.google.com/file/d/1bIBXYI-CbZ6IXvA5Cmmphht-egarQtWl/view
- Source SHA256 `a48a85d258f10148eba41c9d8dd199e03c46c3fdd4f3585ef7d6e892a12e4a86`.
- Receipt SHA256 `f3497775055567bc18189575dc307949557c4485130d07b59da219945e1106b8`.
- New remote GitHub CI PASS: pending independent observation.

## Next decisive research step

Canonicalize the **actual partial-color constraints** after the fixed root `(q0,(U,U))` and a second paired query. Compute admissible color outcome partitions with the P48 matching/parity DP, then use only legal history-preserving symmetry transformations to transport all children, rather than merely comparing cardinalities. Integrate the two-sector parity boundary as a negative test. Attack an actual mixed-prefix no20 / yes20 certificate, not just more stabilizer tables.

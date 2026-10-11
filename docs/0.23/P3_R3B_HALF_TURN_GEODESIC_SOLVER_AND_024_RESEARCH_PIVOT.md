# CUBE-REV 0.23 P3-R3B — Exact Physical Half-Turn Solver, Geodesic Multiplicity & the Finite-Cohort Specialization Trap

**Proposed substage title:** CUBE-REV 0.23 P3-R3B — Geodesic Program Synthesis on the Actual Rubik's Cube: Independent 54-Sticker Turn Semantics, Half-Turn Subgroup Membership, All-18-HTM Shortest-Word Census, 3+2 Meet-in-the-Middle Solving & Out-of-Cohort Falsification.

**Status:** Original 62-cube source fixture directly computed in a separate geometric facelet action model; formal release of the GitHub Node/Go code remains conditional on independently completed Actions CI. This is an extension of 0.23 and NOT an activation of 0.24.

## Research-direction recovery: what we learned from the history

In [historical Drive Chat Archive 26.md](https://drive.google.com/file/d/17-CmE97mrzmh_pqPLGMS_RFvV1jjlJk-/view) and the preserved 0.22→0.23 Notion/GitHub chain, the key object was an actual physical 3×3 cube and its authentic authored FMC search candidates. Exact DR/HTR subgroup geometry, original full-face cubie state replay, source-prefix-constrained exact solved distances, and the 10/10 Pareto PDB rank-reversal counterexample are strong results because they are *about executable physical cube moves and geodesics*. The P3-R0/R1 exact 62-cube source subset was valuable, but the progression to increasingly abstract observation and error models risks treating a specialized synthetic finite cohort as the research object itself. The privately archived 451 human solves similarly have no identified source-balanced causal cognitive effect at the strictest P3-R2 comparison; no amount of unpriced abstraction should manufacture one.

Our corrective principle is to use P3-R3's observation/coding proofs as *inherited specialized mathematical results*, not to let them become the governing topic. The immediate question is not "how many faces can one inspect?" but **what legal Rubik cube move structure permits one finite executable program to generate actual shortest solution words for distinct physical states, and when does that program fail?** The human source grade remains explicit, but provenance and audits are scientific safeguards, not research endpoints. The existing subgroup and meet-in-the-middle ideas are standard ingredients; claim only precisely reproduced finite source-conditioned results, not the invention of MITM or new generic Rubik's algorithms.

## Frozen physical source and independent cube semantics

Inputs are the unchanged public P3-R1B [62 real 3×3 whole-cube nine-sticker face signatures](../../data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv), whose original 54-sticker/cubie genesis was independently certified in P3-R1A. The source distribution is **60 actual different physical cube states at exact 18-HTM distance five and two at distance three** (not 62 independent human solves). The original maximum-62 same-corner-fiber selection is a special deterministic cohort selection rule, not an unbiased sample of WCA scrambles.

[Original 54-sticker independent Node rotation/solver](../../scripts/cuberev-023/verify-p3-r3b-62-original-sticker-halfturn-mitm-geodesic.mjs) and [independent original 54-sticker Go verifier](../../scripts/cuberev-023/p3_r3b_halfturn_physical_go/main.go) reconstruct all six ordered 9-color physical face grids from their actual coordinates and outward normals. Their legal move permutations are generated from the true outer-layer 90/180/270 degree rotations of each of the six faces, and checked to be bijections over all 54 facelets. Face indexing matches the original fixture's geometry and is not defined by arbitrary source index lookup. The full move alphabet is exactly all 18 outer-face HTM moves:
U/U'/U2, R/R'/R2, F/F'/F2, D/D'/D2, L/L'/L2, B/B'/B2.

The subgroup experiment restricts permitted actions to the exact six genuine involutive half turns H={U2,R2,F2,D2,L2,B2}. The solver receives the *complete ordered original 54-sticker source state as its input*. There is no unpriced human recognition, implicit corner-only state oracle, impossible observation query or assumed individualized memory.

## P3-R3B theorem — Exact distances and halfturn-only shortest geodesics

Independent full18 rooted original facelet BFS gives exact layers through 4:
**[1,18,243,3,240,43,239]**.

Independent H-only physical Cayley BFS gives exact layers through 5:
**[1,6,27,120,519,1,932]**; its goal-centered radius2 contains precisely **34** distinct physical states.

All 62 actual frozen full-cubie source states belong to this H-only 5-ball and satisfy the **same exact distance** under the six half-turn subgrammar and under the full eighteen legal moves: sixty length-five, two length-three. For the length-five sources the complete full18 depth<=4 ball proves *absence of shorter* words; for the length-three sources the full18 exact BFS confirms distance three. Every computed half-turn word is individually replayed from the original ordered 54-sticker source state to the exact original solved orientation.

For each real source state s, enumerate all eighteen possible first legal face turns and compare the exact full18 distance of the resulting neighbor with d(s)-1. A first action belongs to a globally shortest HTM solution **iff** it reaches that precise layer, since the word metric is the shortest path metric on the real cube Cayley graph. The resulting exact physical census is:

| Exact frozen-source property | Result |
|---|---:|
| Whole physical states | 62 |
| States with exactly **one** optimal first action | **58** |
| States with exactly **two** optimal first actions | **4** |
| States with exactly **one** shortest complete 18-HTM word | **50** |
| States with exactly **two** shortest complete 18-HTM words | **12** |
| Total distinct shortest full 18-HTM words, counting all source states | **74** |
| Shortest words with any quarter turn | **0** |
| Sum of one chosen shortest word length for all 62 states | **306 HTM tokens** |

This is a **complete finite geodesic multiplicity census** for the frozen 62 states; the witness for zero non-half shortest words is equality of the total full18 and H-only shortest word counts for each source, with no assumed human cognitive shortest-path ability. Different actual 3×3 source states cannot share the same full solving word, as earlier Lean proves, but a **single input-dependent algorithm can compute 62 distinct words** without storing a 62-row literal solution dictionary. The latter distinction is *policy-program vs output-string*; it is not a literal byte compression result without pricing code, facelet representation, state tables and computation.

## Executable 3+2 halfturn physical solver

Construct one **global halfturn goal-ball radius two** via the real 54-sticker physical move engine, keyed by complete 54-facelet states and storing the shortest path from solved (half turns self-inverse). This yields exactly **34 keys**. Given a source cube, enumerate all halfturn words to distance at most **three** forward, intersect the reached original 54-sticker states with the 34 goal-side states, and concatenate the forward source moves with the reverse of the stored solved-to-intersection word. Select the shortest candidate.

The worst-case source-side BFS reaches exactly **154 distinct full cube states** within distance three (1+6+27+120); therefore the finite solver can test at most 154 source-side entries per source, using a 34-entry reverse table. Its code is the same for all 62 independent whole-cubie inputs. Actual replay of each returned solution *must* solve the entire original cube in the original frame, not merely the corners.

**Theorem's exact limit:** because the frozen source cohort was selected for a maximal *same-corner* fiber at small radius, finding that all 62 lie in a 5-turn halfturn ball is a **specialization warning**. It cannot be generalized to all 3×3 scrambles, all FMC human authored DR candidates, other corners, or the full 663,552-element HTR subgroup without new enumerations and independent tests. A 34-state reverse table is *runtime working storage*, not a proof of a 34-byte or 34-human-algorithm memory minimum. The six-generator restriction does not establish a strictly faster wall-clock algorithm than established solvers.

### Protocol-negative controls and next experiment

**Implemented 12 original-cube out-of-cohort negative controls:** construct each of U/U', R/R', F/F', D/D', L/L', B/B' directly from the solved physical 54 stickers. Every control has full18 exact depth one and is absent from the independently enumerated radius<=5 *half-turn-only* reachable set. Both Node and Go physical verifiers now assert this explicit negative result as a test; if the solver's halfturn domain is accidentally broadened, its regression should fail. This is only a **finite horizon-five refusal to generalize**, not a mathematical proof of non-membership in the entire 663552-state HTR subgroup or a wall-clock performance comparison. Independent read-only CI success is still pending readback.

## Transition to a genuinely new physical-cube research program

The **0.24 candidate** should not simply rename observation error or algorithm description length. It should begin with an actual puzzle-solving advance, adversarially compared with honest baselines on independent real cube scrambles and verified human-authored FMC branches:

1. Source-independent full physical move oracle, exact geodesic multi-move-frontier witnesses and HTR/DR subgroup-specific search gates with explicit failure on out-of-domain states.
2. At least two sharply different physical puzzle ecologies: this halfturn-biased 62-state cohort and source-authored human FMC states which are NOT automatically in H; a held-out scramble/candidate group.
3. Fixed comparable move metric and compute resources: optimal HTM length, expanded physical cubies, wall-clock and resident memory, with hardware and toolchain declared. A new policy must beat or meaningfully explain a baseline for a specified scope, not merely relabel group-theoretic prior art.
4. Proof-carrying complete original 54-sticker witness for every output; negative controls/failed branches preserved; no participant timing/cognition inferred from authored retrospective text.
5. **No automatic 0.24 promotion**: keep the active 0.23 frozen import and explicitly seek researcher acceptance for any new title and version.

[Read-only physical independent CI](../../.github/workflows/cuberev-023-P3-R3B-full-sticker-halfturn-solver.yml) must complete before marking external PASS. All commits on research/current from WhoSia account only; no github-actions[bot] or github-action[bot] author/committer, read-only workflow. Preserve P7 exact-path manifest and earlier source/privacy holds without permitting repository administration to displace the cube science.

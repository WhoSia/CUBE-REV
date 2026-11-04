# CUBE-REV 0.28 — B6 41-target independent 48-sticker proof protocol (D0.3 gate)

Status: **DESIGN / NOT A NEW B6 CERTIFICATE**. Prepared after re-reading `34.md` and the committed B5 and B6 generators on 2026-11-04.

## Why this gate exists

The current 41-goal MITM receipt is exact **conditional on its physical action**. Both `emit_b6_41_mitm_inputs.py` and `make_b6_factor_table.py` derive their target and action representations from the historical 54-facelet `independent_b4.py`. An algorithmically separate search over the same action table is not an independent physical model.

The fresh `b5_independent_48sticker_seed_search.cpp` supplies a separate geometric 48-moving-sticker implementation. Its 621,649-state B5 census and independently Python-replayed 13 orbit-pair witnesses provide strong low-radius checks, but **do not certify any B6 distance-13 exclusion**.

## Mathematical target and exact decision criterion

Let `T` be the six face generators with clockwise, counterclockwise, and half-turn moves (18 HTM generators); let `B6` be the distinct legal cube states of HTM distance at most six. For each nonidentity stabilized full cubie state `g`, the positive-layout obligation is

`B6(identity) ∩ B6(g) = ∅`  iff  `d_HTM(identity,g) > 12`.

This equivalence requires symmetric generators, a consistent left/right group convention, and complete legal full-state equality. The right-hand side must not be interpreted as a proof that `d_HTM = 13`.

## Required independently checkable components

1. **Physical model P48.** Construct all 48 individually labelled moving stickers from coordinates `p in {-1,0,1}^3` with 2 or 3 nonzero components and outward unit normals. Generate 18 moves by rotating `p` and `n` on a selected outer layer. Do **not** import an archived 54-facelet transition table or the 20×24 factor table.
2. **Semantics and orientation.** Declare whether each state maps original sticker to current slot or slot to original sticker. Verify that composition order matches move words, that 18 generator inverses give identity, and that each whole turn preserves the legal corner/edge coupling constraints. Supply at least one asymmetric, non-identity state test, not just the solved state.
3. **Independent targets G48.** From the 8 geometrically admitted omitted-corner/omitted-edge pair representatives, construct all 11 nonidentity stabilizer elements by tagged cubie permutations/orientations in the new coordinate conventions. Derive orientation with the independently generated P48 sticker normals and handedness; do **not** deserialize the archived `facelet_hex` as a source of truth. The 88 generated entries must contain 74 distinct full states, *after* they are independently produced. These counts are regression checks, not the generating algorithm.
4. **Cross-convention bridge.** Independently map each P48 state to canonical named original corner/edge positions and orientations. Only then compare against the archived 54-facelet state and the 41 representative class record. A mismatch in face-turn signs must be reported as a failure and repaired in the bridge or physical geometry with a replayed regression; never silently transform a target to make its digest match.
5. **Symmetry reduction.** Prove mechanically that every claimed proper/improper spatial transformation is a cube-graph automorphism of all 18 generators, and that inversion preserves the symmetric word metric. Preserve both the 88/74 origin IDs and the 41 class mappings. Retain an unsymmetrized sample that checks the same distance result before accepting the reduction.
6. **Exact distance solver.** Generate the complete P48 radius-six ball using legal normalized 18-HTM words, deduplicating by equality of *all* 48 slots, not a digest alone. For each 41 representative target, enumerate an exact radius-six goal ball and prove zero full-state intersections. Opposite-face commutation and same-face reduction must have separate exhaustive local rewrite tests.
7. **Negative controls.** (a) Insert a solved state: must intersect. (b) Insert a known short 12-or-less-move word: must intersect. (c) Flip one move-direction convention in one engine: bridge/roundtrip tests must fail. (d) Reuse the known 13-move edge-only physical witness: compare its full physical endpoint in both engines and confirm the independent solver does not return a ≤12 false positive.
8. **Evidence custody.** Save complete commands, compiler/runtime versions, unique state counts, goal-by-goal verdicts, exit codes, peak memory, SHA-256 of raw inputs/outputs and the P48 target generator, plus commit SHA. An interrupted run is **not** a passing run. CI checks must be read-only; never let `github-actions[bot]` author any commit.

## Gates

- **G0, model:** independent 48-sticker move construction and 18^2 composition/inverse tests pass, including arbitrary nonidentity states.
- **G1, targets:** independently constructed stabilizer target states cross-compare to archived physical endpoints; 88 entries, 74 unique, correct inverse and cube symmetry orbits. No distance claim.
- **G2, one full control:** exact P48 depth-six MITM runs on one known nontrivial target, a short positive control, and the 13-turn negative control.
- **G3, full proof:** every one of the 41 independent target classes has zero exact B6 intersection, with independently checked class coverage from the complete 156 valid layouts.
- **G4, publication:** external literature novelty audit and independent reviewer replay of custody assets. Only G3 can close the **physical** B6 upper-bound gate; G4 is necessary before submission claims.

## Explicit dependency graph

- Fresh B5 220/220 three-edge collision support -> B6 one-erasure edge lower bound (at least 11 edge sensors).
- Previously replayed B6 two-corner collision support -> B6 one-erasure corner lower bound (all 8 corners).
- B6 positive 16-sensor complete classification -> extension checks yielding all 12 robust 19-sensor layouts.
- **G3** -> independent B6 positive-layout HTM upper certificate -> removes the shared-54-facelet physical-model dependency from the previous branch.
- None of the above alone implies publication novelty or gives an exact shortest word for every B6 stabilizer element.

## Source baseline

- `scripts/cuberev-observation/b5_independent_48sticker_seed_search.cpp`
- `scripts/cuberev-observation/build_b6_stabilizer_goals.py`
- `scripts/cuberev-observation/emit_b6_41_mitm_inputs.py`
- `docs/0.28/evidence/B6_MITM_41_20261103.md`
- Paper draft `papers/0.28/RADIUS_RESTRICTED_CUBIE_OBSERVATION_DRAFT_01.md` remains **NOT SUBMISSION-READY**.

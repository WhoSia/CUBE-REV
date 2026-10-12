# CUBE-REV 0.24 P0 — Original Physical Whole-Cube Parity Gate and Exact Full-HTM/Half-Turn Domain Census

**Status: LOCAL ORIGINAL-FACELET NODE PASS; INDEPENDENT GO PROGRAM ADDED BUT EXTERNAL CI COMPLETION UNVERIFIED. No complete external PASS declared.** Program authority is the [researcher-approved active 0.24 charter](PROGRAM_CHARTER.md); the [previous proposed document](00_PROPOSED_PHYSICAL_CUBE_SEARCH_ARCHITECTURE_CHARTER.md) is retained verbatim and not quietly edited.

## Research question and source cohort

Does the six-generator exact half-turn-only source policy from 0.23 P3-R3B transfer to physically diverse, all-18-HTM short-distance states, and can a genuine Rubik cube invariant certify out-of-domain cases without unbounded search?

Construct every **original 54-sticker entire 3×3 physical cube** state reachable by 0..3 legal outer-face HTM rotations starting from solved. The six-face sticker order is URFDLB, with complete actual facelet positions, outward normals, and original face colors; all moves are true layer rotations of 90/180/270 degrees, with standard original centers, no synthetic state interpolation. The cohort contains 1+18+243+3240 = **3,502 distinct full physical states**. This is exhaustive over the exactly specified radius-three full-18 language, not a new human sample or the cherry-picked 62-state same-corner maximum fiber.

Independently enumerate original 54-sticker whole-cube states reachable by at most five of six true half turns H=(U2,R2,F2,D2,L2,B2), with shells 1/6/27/120/519/1932, total 2,605 different states. Compare **exact full sticker strings**, not corner-only projections. Exact full18 BFS shells are 1/18/243/3240.

## Structural theorem — corner permutation sign is a sound H-only negative gate

The original Rubik cube has eight identifiable physical corner cubies at the eight three-dimensional corner positions. Let \(\sigma_c(s)\in S_8\) denote the exact full cube's corner-position permutation in the fixed source frame, reconstructed from each cubie's authentic three sticker colors. Let \(\operatorname{sgn}(\sigma_c)\in\{-1,+1\}\) be its permutation sign.

Each legal 180-degree outer face rotation exchanges four affected corner cubies as **two disjoint swaps**, so its induced corner permutation has sign +1. Sign is multiplicative under permutation composition. By induction, **every cube state reached from solved by any word over all six half turns must have even corner permutation**, independent of word length:

\[
  \forall w\in H^\ast,\quad \operatorname{sgn}(\sigma_c(\mathrm{solved}\cdot w))=+1.
\]

Thus any state with odd corner permutation can be conclusively excluded from **the entire, unbounded half-turn subgroup**, using its real physical cubies alone. This is a necessary and **not sufficient** condition for membership; testing even corner parity is not a complete membership test.

One quarter outer-face turn induces a four-cycle on corners and therefore odd sign, showing that each of the twelve source-independent single-quarter-turn controls from 0.23 P3-R3B is impossible to solve with *any* half-turn-only word, not just within the earlier depth-five horizon. This is a strict improvement in the *proof scope of the negative gate*, not an invented group-theoretic invariant.

## Exact physical finite census

| Exact shortest distance in all 18 HTM | In half-turn radius<=5 | Even corner sign, outside half-turn radius<=5 | Odd corner sign, outside **whole** half-turn subgroup | All physical states |
|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 | 1 |
| 1 | 6 | 0 | 12 | 18 |
| 2 | 27 | 108 | 108 | 243 |
| 3 | 120 | 1440 | 1680 | 3240 |
| **Total** | **154** | **1548** | **1800** | **3502** |

Data produced by exhaustive original-54-facelet state enumeration; every duplicate state is merged by **complete 54-sticker string**. A separate test calculates the exact predecessor DAG: for every nonzero-depth physical state, all predecessor shortest-path multiplicities sum to the number of genuinely shortest words reaching the state under all eighteen moves.

These 1,548 even-sign states are **not within five H turns**. They may or may not be in the unbounded H subgroup. No source or document may combine them with the 1,800 provably nonmembers and call all 3,348 H-subgroup nonmembers. That stronger claim has not been proved.

As of this stage, the two implementations are [Node](https://github.com/WhoSia/CUBE-REV/blob/469e9cf07a633a87da300ffa0fdbbccc7230fc89/scripts/cuberev-024/p0_real_cube_parity_and_halfturn_domain.mjs) and [Go](https://github.com/WhoSia/CUBE-REV/blob/469e9cf07a633a87da300ffa0fdbbccc7230fc89/scripts/cuberev-024/p0_fullcube_parity_go/main.go), each deriving 54-sticker geometry and turn permutations independently. Neither reads hidden user human-solve archives. [New read-only independent CI](https://github.com/WhoSia/CUBE-REV/blob/469e9cf07a633a87da300ffa0fdbbccc7230fc89/.github/workflows/cuberev-024-P0-physical-halfturn-domain.yml) must complete successfully before the independent public CI status can become PASS.

## Why this advances cube search rather than just observation language

Previous P3-R3B 62-source policy was *always* within the special H-ball; an apparently perfect solver benchmark would misleadingly imply a generic policy. Here a complete source-independent physical ball demonstrates both the issue and an exact group-theoretic way to reject an H-only action contract. This is actual whole-cube algebra and bounded optimal solver geometry, not generic epistemology.

**Potential algorithmic improvement, not yet measured:** use an extremely cheap exact cubie corner-sign gate to avoid invoking an H-only candidate solver when parity is odd, while preserving a separate full18 fallback solver. Any claimed runtime or expansion advantage must be measured on equal physical scrambles with equal compute budgets and honest baselines. A parity gate in front of an H-only solver alone is not a general 3×3 solver and does not yield global optimal HTM length.

## Next P1 falsifiers

1. Freeze a source-independent full18 held-out scramble cohort beyond the trivial radius-three root ball, with exact move grammar, physical state SHA and negative controls. Compare two-sided geodesic/frontier expansions against baseline uniformly.
2. Compute H-subgroup membership via **exact physical invariants or certified subgroup coset classifier** with sound and complete proof in its stated scope. The 1,548 even-parity but bounded-failing states are the first explicit adversarial stress set.
3. Test parity-gated delegation to a half-turn H-path versus unrestricted 18HTM search. Claim no speed gain without measured expansions and runtime. Separate "cannot be solved by H" from "cannot be solved optimally by H" and "H length exceeds budget".
4. Bring back the original, public, source-authored FMC branch endpoints only after their source/normal-inverse-side, axis and original full cube replay is frozen; do not infer unrecorded human cognition.

## Safety and evidence provenance

All new Git commits need WhoSia author AND committer, no github-actions[bot] or github-action[bot]. Existing branch research/current only. Actions permissions contents read with no writebacks; original history, P7 exact path manifest, preserved 0.23 failures, real 2×2 source grammar HOLD and private 451 human trajectories remain unchanged. A finite original physical calculation does not become an independently completed GitHub Actions PASS merely because its code exists.

**Release status:** 0.24 ACTIVATED by user; P0 physical math locally source-independent Node demonstrated, independent Go and GitHub read-only CI await run-result readback; P1 not yet declared a performance advance.


### Closed P0 execution archival notice

The three old P0 one-off scripts/workflow were copied, read back and verified in the [Drive archive](https://docs.google.com/document/d/1sr1K8Qx5ugDFSEni-1iAfJExdqYbP5m3QKc2OPmSt8o/edit); exact original Git blob SHAs are listed there. The code links above deliberately use an immutable commit, while this scientific report and P0 successor physical computations remain.

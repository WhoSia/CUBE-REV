# CUBE-REV 0.24 P0-R1 — Real 3×3 Edge-Tetrad Orbits and Sound Half-Turn Subgroup Exclusion

**Substage status: original 54-sticker physical Node independent local exact computation PASS, independent Go source committed and external GitHub Actions final log not yet read; do not print external CI PASS without job inspection.** The active 0.24 whole-cube [charter](PROGRAM_CHARTER.md) and P0 [corner parity 3,502-state predecessor](P0_FULL_PHYSICAL_CUBE_PARITY_HDOMAIN_CENSUS.md) remain as precise history. The original 0.23 P3-R3B special 62-source-halfturn theorem is not extrapolated.

## Scientific question

Is corner permutation parity the sharpest inexpensive necessary invariant to reject a candidate solution whose allowed move alphabet is strictly the six true 180-degree outer face rotations H = U2,R2,F2,D2,L2,B2, or does **actual edge-piece geometry** give a stronger legal-move subgroup obstruction? How well does the necessary H-invariant classify genuinely different short full18 HTM states?

The independent original facelet program reconstructs the complete 54-sticker representation with true 3D outer-face unit normals, fixed original centers, six 9-sticker faces and physical 90/180/270 degree external turns. It enumerates **every distinct complete physical 3×3 state within all-18-HTM distance four**, totaling 1+18+243+3240+43239 = **46,741** states. No human traces are included. Independently enumerate the H-only six-generator physical radius-five ball, 1+6+27+120+519+1932 = **2,605** original facelet states.

## Structural theorem R1-A — Three preserved four-edge orbits

Each of the twelve authentic physical edge cubies is identified from its pair of original sticker colors, with canonical edge-position identification in the fixed source frame. Consider the permutation action induced by the six true half-turn generators on **edge positions**.

Direct original-sticker generator replay yields precisely three transitive edge-position orbit classes (sorted physical color-name pairs):

- **FB orbit:** BD, BU, DF, FU (the four UF/UB/DF/DB edge positions).
- **LR orbit:** DL, DR, LU, RU (the four UL/UR/DL/DR positions).
- **Middle-layer orbit:** BL, BR, FL, FR.

The generator action preserves each class **setwise**. Therefore every finite word over H preserves each edge cubie's original orbit label. This is a mathematical group-action invariant: no amount of additional half-turn searching can move an edge cubie from one tetrad to a different one.

**Proof:** Every H generator permutes the edge-position elements within its three induced connected orbit classes; the product of permutations preserving a subset also preserves that subset. Thus any H word preserves all three tetrad labels. The actual classes are derived from the original 54-sticker true edge transformation and independently checked in Node/Go, not postulated as generic observation labels.

**Sound exclusion:** If a whole-cube state has a physical edge cubie placed outside its original tetrad, its solution cannot consist solely of H moves, at **any** length, even though the unrestricted eighteen-move 3×3 cube remains solvable. No claim that orbit preservation alone is sufficient for general H membership: orientation, permutation and deeper group invariants may impose further constraints.

## Exact finite full18 radius-four experiment

Compare every original 54-sticker state in the complete all18 radius-four ball with the H radius-five ball. The following exact evidence emerged:

| Full18 exact geodesic depth | Physically preserves all three tetrad classes | Violates at least one class | Total |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 |
| 1 | 6 | 12 | 18 |
| 2 | 27 | 216 | 243 |
| 3 | 120 | 3120 | 3240 |
| 4 | 519 | 42,720 | 43,239 |
| **Total** | **673** | **46,068** | **46,741** |

**Within this exact enumerated full18 <=4 finite cohort ONLY**, every orbit-preserving state is found in the half-turn <=5 ball, and every orbit-violating state is outside it. The physical H-five intersection shell sizes are **1/6/27/120/519**; each positive has an executable original-facelet H-word certificate from goal BFS. This is finite-cohort equivalence, not a universal half-turn membership decision procedure.

Unlike the earlier parity-only court, the **46,068 orbit-violating states are globally excluded** from all H-only solutions, not merely beyond a chosen search horizon. Their exclusion holds because tetrad preservation is invariant under every possible H word, not because a breadth-first search timed out.

This is a real physical Rubik cube structural result, though subgroup orbit partitioning is classical group theory and **not claimed as invention of the mathematical technique**.

## Falsification contracts and competing baselines

**Primary scripts:**
- [Original 54-facelet independent JavaScript](../../scripts/cuberev-024/p0_r1_exact_edge_tetrad_orbit_d4.mjs): derives authentic sticker layer permutations independently, discovers edge tetrads from all H generator transitions, exhaustively intersects full18 radius4 vs H radius5.
- [Independent Go original 54-facelet engine](../../scripts/cuberev-024/p0_r1_edge_tetrad_go/main.go): does not share JavaScript physical code, independently computes generator edge orbits, all 46,741 real full18 states and 2,605 bounded H states.
- [Independent source-only GitHub Actions](../../.github/workflows/cuberev-024-P0-R1-edge-tetrad.yml): read-only source permission, no bot-written commits, aborts on any mismatched count or physical class.

**Critical negative controls:** the twelve legal one-quarter-turn physical states violate the edge tetrad invariant and must be excluded forever from H-only. More broadly 42,720 exact full18 depth-four states are orbit-violating even though they are physically soluble with short unrestricted move words. No solver may interpret these as "unreachable cube configurations."

**Honest algorithm metric:** an orbit check can disqualify an H-only search branch in O(12) edge identity operations, but this alone has *not* demonstrated faster globally exact all18 cube solving. P1 must compare full18 complete baseline search with a subgroup-aware search policy on the same held-out physical scrambles, with legal final solutions, number of expanded states, runtime and working-memory envelope. A group-theoretic certificate can save infeasible subgroup searches but must never unsoundly discard legal full18 solutions.

**Critical scope warning:** equality "orbit preserved iff within five H moves" is observed **only** on the complete all18 radius-four ball. It may fail at greater all18 distances; future independent search must attack this with hard adversarial states rather than promote it to a universal theorem.

## Next real cube P1

1. Seek an explicit real physical state outside full18 radius-four for which edge tetrads are preserved but H membership, H shortest length or full18 optimum differ. This is the first *falsifier*, not an administrative detail.
2. Design a sound source-independent H-only subgroup admission gate from multiple cubie constraints with provable necessary and sufficient scope. Compare it with parity-only and naive candidate H search, including costs.
3. Transfer to original authored FMC states only after physically reconstructing the original source stage and solving grammar; source's observed written word is not observed mental search.
4. Investigate exact full cube geodesic move DAGs and non-scalar admissible heuristics; prove improvements from counters and independent runtime, not just a new study title.

## Release, provenance and governance

0.24 ACTIVE; P0-R1 local physical Node computation passed; Go code and CI are committed but external Actions completion remains UNVERIFIED. Project remains research/current; all new commits by WhoSia author and committer, absolutely no GitHub Action bot contributor. New paths only via P7 exact-path actual Git blob SHA admission. Existing private 451 human records untouched, former 2×2 source frame HOLD and failures preserved. The previously proposed-only 0.24 charter is still historical, not overwritten. Do not promote this finite court to universal cube subgroup classification or human cognitive measurement.

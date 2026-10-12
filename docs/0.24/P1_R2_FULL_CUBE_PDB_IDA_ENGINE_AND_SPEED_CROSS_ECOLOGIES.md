# CUBE-REV 0.24 P1-R2 — Proof-Carrying Whole-Cube Search Engineering and Speedcubing Cross Heuristics: Six-Face Exact PDB Ensembles, Lazy Restricted-Solver Upper Bounds, Global 18-HTM IDA*, Frozen-Seed Physical Benchmarks and Source-Graded FMC Transfer

**Status:** 0.24 ACTIVE · P1-R2 ACTUAL ORIGINAL PHYSICAL CODE RUNTIME PASS (local code-source execution) · EXTERNAL GITHUB ACTIONS CONCLUSION PENDING. This is a real executable search engine, not a general fastest-solver claim or a measurement of human thought.

## 1. Origin and engineering course correction

The object is the actual whole 3×3 Rubik cube and its legal physical 18 HTM transitions. Prior 0.23 selected 62 special full-cubie states and found a limited H-halfturn optimal program. 0.24 P0/R1 found original three four-edge subgroup orbits; P1-R0 completely enumerated the true 663,552-state halfturn subgroup and found 192 true whole-cube states with global distance 5 but H-only distance 8/9; P1-R1 used certified H5 incumbents for the restricted exact global distance-five court. Do not turn these results into generic observation philosophy, retrospective human cognitive claims or technical-file management for its own sake.

This P1-R2 builds an actual full18 search machine with precomputed mathematically admissible cubie patterns, full original-sticker output replay, honest resource limits and speedcubing-stage experiments.

## 2. Actual complete 18 HTM search kernel

Source: [physical whole-cube PDB+IDA engine](../../scripts/cuberev-024/p1_r2_full18_pdb_ida_engine.mjs); reused proven [original sticker/cubie engine](../../scripts/cube/sticker-cube.mjs) and [existing exact Cross four-edge PDB](../../scripts/cuberev-013/cross4-pdb.mjs).

- Move space: all 18 actual 90/180/270 degree outer turns in HTM; states are all original 8 corners (CP/CO) and 12 edges (EP/EO), source inputs and outputs verified by complete 54-sticker replay.
- Each four-edge reference-face Cross PDB is an exact shortest-path quotient with **190,080 = 12P4 times 2^4** physical projected states. The U/D baseline uses two. The six-face version adds R/F/B/L, for four new distance tables totaling **760,320 stored single-byte entries**, apart from indexes/transitions and runtime overhead.
- Independently exact original orientation projection PDBs: **2,187** corner-orientation and **2,048** edge-orientation states, generated using the actual physical turn maps. The global heuristic is the **MAX** of U/D (or six reference-face) four-edge distances, CO distance, EO distance. Each is admissible under every legal turn, and their maximum is admissible. Never sum overlapping PDBs without a genuine cost partition.
- A true complete 18 HTM radius-four goal table of **46,741 original cubie states** provides exact solve suffixes. Outside this table the full distance is at least five.
- Genuine halfturn source-to-goal path from exact H5 / optional restricted H4+H5 meet-in-middle is an **upper-bound incumbent only**. A real H five-move solution outside the full18 radius-four ball implies exact full18 distance five by the lower/upper sandwich. Length eight/nine in H is never a full18 lower bound.
- Standard complete-resource IDA* iterates integer full18 cost bounds using only exact goal suffix distances and admissible physical PDB lower bounds. With finite node/time/depth caps it outputs HOLD or UNCERTIFIED_INCUMBENT rather than an invented global optimum; any OPTIMAL result has a complete bounded-exhaustion argument and exact source-sticker solution replay.
- Adjacent same-face turns are omitted because they consolidate/cancel into one HTM face action, while physically disjoint opposite faces commute and are ordered canonically. Hence no globally shortest legal word is lost through this generator grammar reduction.

**Actual debug history:** the early baseline without a halfturn incumbent accidentally used an undefined value where null was required; corrected and true source code rerun. A previous eager H9 upper-bound computation scanned 673 true halfturn states on P1-R0 5-vs-8/9 adversarial sources with no IDA node saving. The default was changed to CHEAP_H5: a small physical tetrad gate and direct actual H5 solution lookup; H9 remains opt-in and separately charged. Correctness never depends on a human source reconstruction or unverified phase assumption.

## 3. Independent same-engine performance test

One direct imported-source V8 code runtime test with real original project sticker-cube/Cross-PDB sources (test-only cryptographic hash stub used solely in irrelevant receipt fields, not physical transitions or solver proof) fully replayed original 54-sticker solutions. In the first six source scrambles, exact global shortest lengths agreed between two-face and six-face PDB variants. Representative node-call counts at original d18 6/7/8: **119→107, 69→45, 523→177, 3,644→1,334**. Both actual scramble D U R2 D U (5 vs H9) and D U R2 D' U (5 vs H8) returned true globally shortest five-move solutions rather than their suboptimal H words.

### Frozen 16-source heldout physical experiment

[Exact seeded runner](../../scripts/cuberev-024/p1_r2_seeded_heldout_engine_benchmark.mjs) generates **16 original legal full18 move words**, using fixed xorshift32 PRNG seed **0xC0BE24A1**, with exactly four generated words of each lengths 6,7,8,9 and no repeated adjacent face. The source words are synthetic legal original cube scrambles; their literal lengths are NOT assumed globally minimal (some collapse to d18 4,5,6,8).

Both benchmark arms have identical original physical engine, same R4 actual goal table, same lazy H5 incumbent, same full18 IDA implementation, max depth, node/time budgets and complete source-sticker output verification. The only intended intervention is two (U,D) versus six (U,R,F,D,L,B) reference-face admissible Cross-PDB bounds.

**Actual complete-source-code test result:** all **16/16** cases solved with proven same exact global optimum, source-sticker replay PASS. The two-cross arm used **246,089** IDA recursive entries; six-cross used **73,856**: **172,233 fewer, 69.988% reduction** in the specified call counter. **13 improved, three tied, none worsened** on this frozen source set. This is a limited concrete whole-cube search-engine improvement, not a universal speed-complexity theorem.

Explicitly measured building the four extra PDBs once was approximately **2.38 seconds in one local V8 run**; the source runner distinguishes this cold precomputation from reused warm solve calls. V8 runtime memoryUsage was stubbed for this evaluation, so NO empirical heap/RSS claim can be derived from it. Distance arrays contain 760,320 extra byte values but runtime maps and allocations cost more. Node CI is designed to emit real process heap/RSS. Additional projected PDB lookups may eat CPU time even if recursion decreases, so **69.99% less recursion does not mean 69.99% less wall time**.

## 4. Speedcubing: physical CFOP Cross-stage mechanics

[Physical 6-face Cross speedcubing court](../../scripts/cuberev-024/p1_r2_speedcubing_cross_pdb_court.mjs) uses authentic publicly posted World Cube Association **3×3 scrambles** from [Seoul Summer 2026](https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles) and [Seoul Winter 2026](https://www.worldcubeassociation.org/competitions/SeoulWinter2026/scrambles). Six exact four-edge Cross PDBs of 190,080 entries each were calculated under all 18 legal moves, with original physical Cross words verified by cubie projections and complete 54-sticker transformations. An independently implemented 24-oriented-edge-sticker BFS reproduced all three six-face vectors below, and the actual GitHub code was additionally executed against the inherited original sticker and cross4-PDB modules.

| Official event, round, group, scramble index | U | R | F | D | L | B | Minimum |
|---|---:|---:|---:|---:|---:|---:|---|
| Seoul Summer 2026, 3x3 Final A #1 | 5 | 7 | 5 | 6 | 6 | 6 | U / F |
| Seoul Summer 2026, 3x3 First A #1 | 6 | 6 | 7 | 7 | 7 | 7 | U / R |
| Seoul Winter 2026, 3x3 Final A #1 | 5 | 5 | 6 | 5 | 6 | 6 | U / R / D |

This is a meaningful **machine planning** heuristic axis: choose reference face, examine all optimal first moves, stage optimal Cross word and possible F2L lookahead. It does **NOT** measure actual human inspection, reconstruction, execution time, TPS, hand ergonomics or speedsolver cognition. Cross-only optimal does not imply that the full CFOP solve, FMC whole solve, or real human run is fastest. Exact source scramble text and 18 output regression values are fixed in the script.

Two runtime bugs were caught and repaired before accepting these results: (1) accessing the original face-turn transformation array with move-token strings instead of legal move indices and (2) wrong co/eo cubie propagation through move cp/ep arrays. The actual corrected GitHub code was rerun with original project PDB and all 18 public WCA Cross distances PASS. Preserve the bugs as diagnostic history rather than silently erasing the failures.

## 5. Real human-authored FMC / WCA full scramble transfer failure

[Real public WCA/FMC source-boundary court](../../scripts/cuberev-024/p1_r2_source_fmc_speed_boundary.mjs) gives the same 18 HTM IDA engine a strict **30,000-entry recursive call budget**, time and max depth caps, with two genuine long official WCA 3×3 scrambles (19 and 20 legal turns) and two existing public original Miao/Riabov human-authored normal-side EO+DR prefix words (35 source scramble/prefix tokens). **All four resulted in RESOURCE_CAP_HOLD with 30,001 recursive entry calls, none with a certified global whole-cube optimum**. These are research limitations, not claims the original cube is unsolvable or the person solved slowly.

Exact original cubie replay showed **Miao main and Riabov main source-distinct written prefixes land at the SAME entire cp/co/ep/eo physical cube state**. Their separate written sources are not two independent physical heldout test states. This duplicate is explicitly asserted in the source-boundary script. The existing private original 451 human 3×3 solve records were not read or published, and written retrospective FMC moves do not reveal actual process-state or intention.

## 6. What needs to be engineered next

A genuinely stronger complete 3×3 optimal solver for long states requires larger original-cubie PDB abstractions, memory-aware binary representations, bidirectional frontiers and/or source-sound subgroup phase decomposition with original global lower/upper certificates. Stronger speedcubing heuristics should add exact physical first F2L pair and lookahead cost under a declared metric; execution-time claims require genuine observed data and rights. Compare identical warm/cold precompute budget, physical legal-turn counts, tree recursive entries, peak RSS, wall time and solved certificate against actual solver baselines, including resource holds.

**Next proposed paragraph:** P1-R3 — Bi-Directional Cubie Search and Source-Attested Speedcubing Stage Opportunity: Stronger Admissible Pattern Abstractions, Complete-Solution Certificates, F2L Cross Preservation and Hardware-Calibrated Tradeoffs.

## 7. Exact source archival, governance and release

The superseded P0 one-off Node parity code, Go parity code and its obsolete workflow were archived in full as source-text with exact actual Git blob SHA values in the existing [Drive P0 source archive](https://docs.google.com/document/d/1sr1K8Qx5ugDFSEni-1iAfJExdqYbP5m3QKc2OPmSt8o/edit), source-readback matched separately for all three, then **removed from the active research/current Git tree**. They remain retrievable from immutable Git commit **469e9cf07a633a87da300ffa0fdbbccc7230fc89**. The historical evidence and scientific P0 report were NOT deleted, and P0-R1/P1-R0 reusable Node/Go kernels remain active. [Drive active-set archival ledger](https://docs.google.com/document/d/1OPuOHUHSLTXSaQOcKgJOrC1ebJ4z-HdKTLCC16InACI/edit) records the exact three-path retirement.

Dedicated [read-only Node22 full original cube and independent Go geometry CI](../../.github/workflows/cuberev-024-P1-R2-physical-ida-pdb-and-speedcubing.yml) runs the core full18 engine, exact official WCA 3x3 Cross stage, seeded 16-scramble source benchmark, real WCA/FMC HOLD cases and prior independent Go physical tetrad geometry. This is **NOT an independent Go reproduction of the full P1-R2 IDA search implementation**. No external completed GitHub Actions run is currently verified; therefore **EXTERNAL_CI_PENDING**, not independent PASS. All new Git author and committer identities must be human WhoSia only; github-actions[bot]/github-action[bot] are prohibited as contributors. Actions have contents read-only, no commits or pushes. Reconcile active G7-P7 exact-path allowlist and SHA after actual retirement, never create a broad wildcard exception. Preserve earlier CI failures, original restricted 2×2 reconstruction frame HOLD and all private human-source boundaries.

**Scientific conclusion, precisely delimited:** The genuine 18-HTM cubie PDB+IDA solver was executed on actual project physical sources, certified full-cube optimum for all 16 frozen generated inputs and reduced recursion 246,089→73,856 by using all six exact Cross projections. Separately, genuine official 3×3 competition scramble Cross-stage distances were verified for all six faces. Full-scramble WCA and source-authored FMC long-state optimum remains unproved and correctly held. Whole-program wall-clock acceleration beyond this cohort and human speedcuber cognitive mechanisms remain unestablished.

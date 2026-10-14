# CUBE-REV — Physical Rubik's Cube Search & Proof-Carrying Programs

**ACTIVE: CUBE-REV 0.25 — Proof-Carrying Physical Program Synthesis for the Rubik's Cube: Source-Complete Geodesic Certificates, Coset-Guided Solver Architectures, Adversarial FMC Prediction & Timed Speedcubing Mechanism Falsification.**

[0.25 formal research charter](docs/0.25/PROGRAM_CHARTER.md) · [Active research Notion](https://app.notion.com/p/3f7ef561cf9281ae8e94c46e9f916fdc) · [P7 exact active-file manifest](g7/p7/active-set-manifest.json).

**The scientific subject is the actual fixed-center 3×3 Rubik's Cube:** 54 original physical stickers, all 8 corner and 12 edge permutations and orientations, and 18 legal outer-face HTM moves. Group theory, TCS and formal verification serve actual physical cube solving. Source-authored FMC programs are distinguished from machine-generated paths and from unobserved human mental processes.

## Latest true physical solver engineering

**[0.25 P0-R5 — actual unrestricted whole 18HTM corner-prefilter solver engineering](docs/0.25/P0_R5_EXACT_CORNER_PREFILTER_FOR_WHOLE_CUBE_GLOBAL_BALL_CERTIFICATE.md):** [external physical original-cube CI SUCCESS #38513745705](https://github.com/WhoSia/CUBE-REV/actions/runs/38513745705). On the original WCA 3×3 and verified goal B6 of 8,240,087 full-cubie states, the exact entire-corner projection has 1,405,068 distinct states. Full source B7 complete: **120,213,368** source visits; **118,678,327** safely rejected on corner membership alone; **1,535,041** needed expensive full CP/CO/EP/EO lookups (**98.723% fewer full-state lookups**), zero true intersections. All normal-form descendants STILL explored; not a geodesic subtree prune or a wall-time speedup claim. Global interval **14≤d18≤18** preserved. [Original P1-R6 independent source compile regression SUCCESS #38513732158](https://github.com/WhoSia/CUBE-REV/actions/runs/38513732158). Go/C++ and Lean4 remain preferred scientific languages.

## P0-R6 — exact descendant pruning (external CI pending)

[Research theorem and limitations](docs/0.25/P0_R6_EXACT_ONE_STEP_DESCENDANT_PRUNING.md) · [original physical C++17 implementation](scripts/cuberev-025/p0_r6_one_step_descendant_cpp/main.cpp) · [read-only Actions workflow](.github/workflows/cuberev-025-P0-R6-descendant-pruning.yml).

**New implementation, NOT yet externally confirmed:** extend the entire exact B6 goal-side corner projection by one genuine reversible 18HTM move; at depth6 in a source B7 search, a node outside the extended exact corner envelope cannot have a B6-meeting one-step child. The C++ engine therefore skips **entire descendant branches**, not merely full-cubie lookups as P0-R5 did. It retains exact whole-cubie CP/CO/EP/EO equality checks where necessary, the same canonical source coverage, and the original official 54-sticker test. Real pruning counts, wall time, peak RAM, and completed CI outcome are **PENDING**, not PASS. No new 15+ global bound is claimed: **14≤d18(s)≤18** persists. The next attack needs genuinely coupled corner–edge admissibility and independent proof-carrying benchmark comparisons. P7 exact active paths: **769**.

## P0-R6A/R6B — complete-cover audit, measured performance, and attempted 14-move exclusion

**Code committed; external Actions success, actual pruning counts, measured wall time/RSS, and new lower15 remain UNVERIFIED.** [Full theorem, source-frontier and resource ledger](docs/0.25/P0_R6_EXACT_ONE_STEP_DESCENDANT_PRUNING.md) · [paired P0-R5/P0-R6 Actions court](.github/workflows/cuberev-025-P0-R6-descendant-pruning.yml) · [full-physical B8/B6 lower15 experimental court](.github/workflows/cuberev-025-P0-R6B-global-lower15-source8.yml) · [independent Go receipt auditor](scripts/cuberev-025/p0_r6_receipt_go/main.go).

A separate C++17 canonical-word dynamic program, run in the audit environment, independently counted original unpruned iterative source visits: radius6 **9,005,776**, radius7 **120,213,368**, radius8 **1,604,664,504**. These are recursive visit counts, not distinct cubie states; radius7 matches the previously certified P0-R5 count. P0-R6 now requires **actual visited + provably skipped immediate canonical children = baseline** before reporting a complete certificate. The paired Actions workflow also measures wall seconds and peak RSS for old/new algorithms on the same runner, subject to external completed logs; source access and numerical results cannot be inferred from empty PR-only run listings.

**The global lower15 challenge is specifically to exclude every solve of length ≤14, not length ≤13 (already excluded).** Exact physical B8(source) ∩ B6(solved) emptiness would certify **15≤d18(s)≤18**. The B8 experiment has a bounded time/memory envelope, and any timeout or hit means **NO LOWER15 CERTIFICATE**; it has not yet been observed to complete. Current certified bound stays **14≤d18(s)≤18**. P0-R6A uses only sound one-step projected corner descendant pruning; a true joint corner–edge admissible potential is still an independent open step.

## Original-cube benchmark and proof grade

The real [WCA Seoul Summer 2026 3×3 Final Group A scramble 1](https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles) is:

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

An independently physically verified complete **18 HTM solving word** is:

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

**Established unrestricted entire-cube distance: 14 ≤ d18(s) ≤ 18.** The lower bound comes from [0.24 P1-R6 real all-18HTM goal-radius6 / source-radius7 nonintersecting complete-cubie balls](docs/0.24/P1_R6_SOURCE_COMPLETE_FULL18_GLOBAL_BIDIRECTIONAL_CERTIFICATE_AND_025_GATE.md): **8,240,087** exact goal states, **120,213,368** source recursive entries (not distinct states), [actual CI success](https://github.com/WhoSia/CUBE-REV/actions/runs/38210864083). Independently authored Go physical full 54-sticker verification establishes a *weaker* source-complete lower11, not an independent lower14. **Global existence of 14–17-move solves remains OPEN; 18 is not proven optimal.**

## Active 0.25 science — physical original-cube TCS

**[P0-R1 — Real Schreier quotients and common Parikh-face saturation](docs/0.25/P0_R1_PHYSICAL_SCHREIER_PDB_PARIKH_SATURATION_AND_DUALITY.md).** Fully enumerated source-physical four-cubie PDBs: 3×190,080 edge and 2×136,080 corner states, source values [7,5,5,5,6]. Their naive sum 28 is invalid: one original legal U move already incurs total quotient distance 5 at physical cost 1. Common face-usage parity synchronization saturates and does not rule out any 17-move whole-cube source solve. [Go original-54-sticker PDB verifier](scripts/cuberev-025/p0_r1_physical_schreier_go/main.go) · [Independent C++ finite proof](scripts/cuberev-025/p0_r1_independent_physical_cpp/main.cpp).

**[P0-R2 — Full-corner 88,179,840-state geodesics and cost-partition duality](docs/0.25/P0_R2_FULL_CORNER_88M_AND_CERTIFIED_OPERATOR_COST_DUALITY.md).** Complete actual 8!·3⁷ oriented full-corner quotient, exact corner-only HTM diameter **11**, original WCA source corner bound **9**: independently enumerated in [Go](scripts/cuberev-025/p0_r2_full_corner_go/main.go) and [C++17 original 54-sticker geometry](scripts/cuberev-025/p0_r2_independent_full_corner_cpp/main.cpp). The mathematically sound cost-sharing rule is ∑ᵢ cᵢ(a)≤1 for EACH real face-turn action. The [Go 0–1 exact quotient source-PDB verifier](scripts/cuberev-025/p0_r2_operator_cost_go/main.go) evaluates 5×64 face-price masks and all **15,625** unit-cost face-owner assignments. Within this explicitly restricted integer class, the **unique optimal source lower bound is 7** (assign every face to E0): a complete negative design finding, *not* a claim about fractional costs or fully coupled corner-edge moves. [Lean 4 generic scaled cost-budget proof](formal/025/CostPartition.lean) · [externally completed SUCCESS Go/C++/Lean CI #38354902944](https://github.com/WhoSia/CUBE-REV/actions/runs/38354902944). The prior *unrestricted whole-cube* lower14 is not improved by either individual quotient.

**[P0-R3 — Exact continuous face-price pair no-go with ten real Rubik word certificates](docs/0.25/P0_R3_EXACT_CONTINUOUS_FACE_COST_PAIR_NO_GO_PHYSICAL_WORD_CERTIFICATE.md).** The initial [Go physical 7,290-point half-price test](https://github.com/WhoSia/CUBE-REV/actions/runs/38355226394) attained only source bound **7**. A stronger purely mathematical **ten-pair source-witness theorem** covers **ALL real continuous face-uniform two-pattern cost shares**: for each of the ten pairs among E0/E1/E2/C0/C1, two physically legal marked-cubie-solving words have face-wise count-envelope ≤7. Consequently the maximum weighted pair PDB admissible lower bound equals **exactly 7** for the WCA source, including all fractional prices in [0,1], not just the 0/½/1 grid. [P0-R3B nine shortest-pair witnesses](https://github.com/WhoSia/CUBE-REV/actions/runs/38355753083), [P0-R3C final nonshortest E2 path](https://github.com/WhoSia/CUBE-REV/actions/runs/38356018621), and [independent Node original 54-sticker checks on all twenty projected words](https://github.com/WhoSia/CUBE-REV/actions/runs/38356444729) all **CI SUCCESS**. [Actual word pairs and six-face counts in machine-readable source evidence](data/cuberev-025/p0_r3_continuous_face_price_ten_physical_word_pair_witness.json). **This is a source-specific impossibility of improving the tiny two-PDB face-price heuristic beyond seven, NOT the entire-cube 17-move shortest-path impossibility**. Three-plus-pattern cost sharing, non-face-uniform turn costs and true joint noncommutative corner-edge constraints remain open.

**[P0-R4 — Sharp continuous five-pattern operator-cost theorem on real original Rubik cubies](docs/0.25/P0_R4_EXACT_CONTINUOUS_FIVE_PATTERN_COST_NO_GO_SEVEN_ORIGINAL_CUBIE_WORD_CERTIFICATE.md).** Strengthens P0-R3's TWO-pattern exact face-cost7 to **ALL FIVE disjoint actual four-cubie PDBs simultaneously**, for every REAL continuous nonnegative face-uniform per-move cost allocation (each physical face f, f', f2 shares a cost, with total across patterns ≤1). The exact source-specific optimized PDB lower potential is **7**: universal UPPER7 is witnessed by [five ACTUAL separately legal source-projected face words](data/cuberev-025/p0_r4_five_real_cubie_projected_words_cap7.json) with identical seven-unit shared face-count envelope **URFDLB = [1,2,1,1,0,2]**. LOWER7 is attained by giving all six original face costs to the complete physical E0 four-edge PDB, source h=7. [Go exact complete 792 cap7 / 1287 cap8 face-budget physical verifier](scripts/cuberev-025/p0_r4_five_pattern_face_budget_go/main.go) and [independent original 54-sticker direct 20-cubie marker replay](scripts/cuberev-025/verify_p0_r4_five_real_face_budget_original_54sticker.mjs) both externally **SUCCESS in Actions #38370676066](https://github.com/WhoSia/CUBE-REV/actions/runs/38370676066)**, native Go proof #38370213103 earlier PASS. **These are FIVE different projected original legal words, NOT one complete 7 HTM cube solve**; the existing unrestricted physical 14≤d18(s)≤18 is unchanged. Per-generator nonuniform shares, coupled corner-edge actions and full source-frontier continuation remain OPEN.

**Next hard mathematical attack:** a sound coupled corner–edge quotient, genuinely noncommutative action-word synchronization, or a source-complete certificate cover that proves a new unrestricted source lower15+ / finds a shorter original whole-cube solution. Do not replace actual full-cube search with an easy projected graph or claim new global optimality from a PDB alone.

## Programme genealogy — preserved original science

| Generation | Physical theorem or explicitly open boundary |
|---|---|
| [0.24 P1-R7 scientific freeze](docs/0.24/P1_R7_SCIENTIFIC_FREEZE_AND_025_HANDOFF.md) | Verified physical 20→19→18 full-cube solving words; original DR subgroup interface; lower14 global search; historical depth11-vs13 error fixed; 17-solve problem OPEN |
| [0.23 real 62-state physical fiber](docs/0.23/P3_R3_ROBUST_FACE_OBSERVATION_ERROR_CORRECTION_AND_SOURCE_TRANSFER.md) | Source-authentic corner fiber / ideal read-error codes, limited human reconstruction inferences |
| [0.22 real human-authored FMC DR](docs/0.22/P8_R3_STREAMED_HTR_FIRST_CONTACT_DUAL_REVERSE_PDB_EXACT_PHASE2.md) | True physical authored program endpoint classes and exact DR group continuation; text/NISS interpretation holds |
| [0.19 finite original physical M*(5)=8](docs/0.19/P13_FINAL_EXACT_PHYSICAL_MSTAR5_EIGHT.md) | A different exact source-covering problem, not the full 3×3 shortest HTM distance |
| 0.11–0.21 historical mathematics | [Verbatim pre-0.19 README](archive/readme/README_RESEARCH_CURRENT_PRE_019_20261010.md) · [version-specific archive](archive/versions/) · full Git history and source Notion/Drive |

## Byte-exact original long README archives — verified BEFORE reduction

The previous **109,858-character / 242-source-line README**, Git blob **11f726c24f6bc032f2469f91f4dc60c5d7d3a92a**, remains [verbatim original GitHub Markdown](archive/readme/README_RESEARCH_CURRENT_FULL_PRE_P0R2_20261012.md) and a **byte-exact actual `.md` in [Google Drive / CUBE-REV / 80_ARCHIVE / README](https://drive.google.com/file/d/1QQ18TJ2Ary6xl4tD1iRX3ErdVx5HDHwi/view)**. The GitHub and Drive archives were separately fetched and their COMPLETE original text compared before deleting the old long prose from this active index. All older scientific materials, errors and sources remain in those archives and the version-specific research files; README shortening is not evidence deletion.

## Reproduction and source boundaries

Core computation **Go and C++17/C++20**; Lean 4 for formally typed proofs, JS/TS or Rust for separate physical and certificate checking. No Python-first scientific computation requirement. Native reproduction:

```bash
go run scripts/cuberev-025/p0_r2_operator_cost_go/main.go
go run scripts/cuberev-025/p0_r2_full_corner_go/main.go
g++ -std=c++17 -O3 scripts/cuberev-025/p0_r2_independent_full_corner_cpp/main.cpp -o /tmp/cuberev025-corners
/tmp/cuberev025-corners
cd formal/025 && lake build
```

The [P7 exact path/blob active manifest](g7/p7/active-set-manifest.json), not old allowed-path count snapshots, governs changes. **All new commit authors AND committers WhoSia; github-actions[bot] and github-action[bot] are prohibited contributors; GitHub Actions contents:read and no git writeback.** Source physical and mathematical claims only become external CI PASS upon exact completed run verification.

Protected human 451-case raw reconstructions are not authorized public data; Riabov Other #2 source uncertainty, original 2×2 unreported-y2 frame and rights-cleared BLE/video instrumentation remain typed conditions. A solver finding a word is not evidence a speedcuber executed or mentally considered that word.
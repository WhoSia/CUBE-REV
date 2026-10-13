# CUBE-REV 0.25 P0-R2 — Full-Corner Physical Geodesic Quotients & Certified Operator-Cost Duality: An 88,179,840-State Exact PDB, All-Face Cost-Partition Exhaustion and a Sharper Noncommutative Synchronization Obstruction

**2026-10-13 · original whole-3×3 physical PDB independently reproduced in Go/C++; Lean 4 generic cost-sharing theorem KERNEL PASS; exact native+Lean [GitHub Actions SUCCESS #38354902944](https://github.com/WhoSia/CUBE-REV/actions/runs/38354902944); [P7 repository audit SUCCESS #38354903102](https://github.com/WhoSia/CUBE-REV/actions/runs/38354903102).** This is a science substage in the researcher-approved [0.25 active program](PROGRAM_CHARTER.md), not a replacement for source-complete full18HTM search. **No new unrestricted global distance lower bound asserted**. The exact previously certified source interval remains **14≤d18(s)≤18**, from [P1-R6 0.24 external original-cubie full18 search success](../0.24/P1_R6_SOURCE_COMPLETE_FULL18_GLOBAL_BIDIRECTIONAL_CERTIFICATE_AND_025_GATE.md).

## 1. Actual original physical Rubik research source

The frozen public WCA Seoul Summer 2026 3×3 Final A scramble1 is the original fixed-center **20-turn** string:

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

An independently original-54-sticker verified **18-turn WHOLE CUBE complete solve** is:

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

A single corner or edge pattern is a sound *projection of actual 3×3 physical move dynamics*, **not a substitute for solving all 54 stickers**. A theoretical corner geodesic need not be a full-cube geodesic; pairwise or full-corner PDB lower bounds must be compared to the prior global14 whole-cube bound.

## 2. Exact new full-corner 8!×3^7 quotient, not eight independent corner PDBs

Track all eight labeled original corner cubies, every physical corner slot, and the real corner sticker orientation in the original fixed face frame. The corner twist-sum constraint removes one trit, giving exactly

\[
|Q_C|=8!\,3^7=88,179,840.
\]

Each actual legal original 18 HTM face generator induces a well-defined corner-permutation transition and corner-orientation transition. [Go primary original physical 54-sticker-derived engine](../../scripts/cuberev-025/p0_r2_full_corner_go/main.go) constructs original geometric oriented token actions, explicitly checks corner twists evolve additively, ranks full permutations by reversible Lehmer code, ranks the seven independent corner twists by base3, and builds **all 88,179,840 actually reachable labeled full-corner states** by exact unweighted BFS. Distances are exact **within the corner quotient**. It independently tests the actual public original WCA scramble and the genuine 18-turn completed word.

**Local Go exact finite full-corner result**:

| Exact corner-only HTM distance | Distinct oriented full-corner states |
|---:|---:|
| 0 | 1 |
| 1 | 18 |
| 2 | 243 |
| 3 | 2,874 |
| 4 | 28,000 |
| 5 | 205,416 |
| 6 | 1,168,516 |
| 7 | 5,402,628 |
| 8 | 20,776,176 |
| 9 | 45,391,616 |
| 10 | 15,139,616 |
| 11 | 64,736 |
| **Total** | **88,179,840** |

**Exact whole quotient diameter = 11 HTM**. **This WCA whole-cube source projects to corner-distance h_C(s)=9.** This is stronger than each previously isolated four-corner PDB (source estimates 5 and 6) and the three four-edge PDBs (7, 5, 5), but **h_C(s)=9 does not improve the independently proven unrestricted full-cube lower14**.

[Independently derived C++17 physical corner coordinates and BFS](../../scripts/cuberev-025/p0_r2_independent_full_corner_cpp/main.cpp) uses separately written physical original 54-position/normals plus genuine action-turn marker intertwinement on the public scramble, actual 18-move solve, and 256 source-independent legal test words, before filling all 88,179,840 corner states and checking the ENTIRE 12-layer histogram. It reproduces Go's exact diameter11 and source corner distance9; it is not a restatement of the Go output. Local Go ~31.5 s and 434,568 KiB peak RSS; independently C++ ~27.2 s and 433,536 KiB peak RSS in the same container. These are local execution receipts, not general CPU performance rankings. See [Go original finite receipt](../../data/cuberev-025/p0_r2_full_corner_go_receipt.txt) and [C++ independent finite receipt](../../data/cuberev-025/p0_r2_independent_cpp_receipt.txt).

**Homomorphism caveat:** a full-corner label-preserving action quotient has 88m possible corner states (of which each is compatible with at least one true whole cube if edge parity matches). It does NOT prove the full cube has 88m states or imply an unconstrained whole-cube search can end at the corner goal.

## 3. A precise cost-partition theorem — why P0-R1's naive addition was wrong

Let A be the complete 18 actual legal HTM face moves and π_i:G→Q_i five previously audited physical four-cubie projections (3 disjoint 4-edge patterns and 2 disjoint 4-corner patterns). For each i choose a nonnegative *per legal original action* price c_i(a), with

\[
\sum_{i=0}^{4} c_i(a) \le 1\qquad\forall a\in A.
\]

Let d_i^{c_i}(π_i(s),π_i(e)) denote exact shortest quotient path cost under that price function. The SAME real full-cube path w of length L induces one legal path in every quotient with cost Σ_{a∈w} c_i(a), so:

\[
\sum_i d_i^{c_i}(π_i(s),π_i(e))
\le \sum_{a\in w}\sum_i c_i(a)
\le L.
\]

Minimizing over all real original whole-cube solving words yields the **valid additive source lower bound**

\[
h_{\mathrm{CP}}(s)=\sum_i d_i^{c_i}(π_i(s),π_i(e))\le d_{18}(s).
\]

This is mathematically safe because operator cost is shared, **not simply counting the same legal move five times**. It also works with a finite integer scale D: Σ_i c_i(a)≤D implies Σ_i d_i^{c_i}≤D·d18(s). The [Lean 4 core proof source](../../formal/025/CostPartition.lean) proves the generic five-priced common-word scaled sum bound; **the Go/C++ real 54-sticker physics and quotient-distance premises remain separate executable proof obligations**, not silently claimed Lean formalizations of the Rubik group.

The unsplit P0-R1 source distances [7,5,5,5,6] sum to **28**, which is NOT a lower bound; the actual one-turn U move has quotient-distance sum **5** at original true HTM length **1**, a direct original cube counterexample.

## 4. Complete 0/1 face-owner finite optimization: a source-specific negative theorem

The first deliberately constrained cost-share grammar assigns the *entire* unit cost of each original face f∈{U,R,F,D,L,B}, uniformly to **one** of the five genuine four-cubie patterns. All three face variants f, f' and f2 have the same chosen owner. Exactly five possible owners per face give **5^6=15,625** cost shares; every share satisfies the per-action budget with equality.

[Go original geometric full quotient and zero–one weighted shortest-path verifier](../../scripts/cuberev-025/p0_r2_operator_cost_go/main.go) constructs complete 190,080- and 136,080-state physical Schreier graphs, fills exact unweighted distances with full 1-Lipschitz checks, then for every one of **5 × 64 = 320** face-mask subproblems evaluates exact 0–1 weighted source-to-goal quotient distance by true legal 18-generator 0–1 BFS (full state equality, not sampling). It then calculates and enumerates all 15,625 source cost shares; no optimization oracle or heuristic upper bound is substituted.

**Actual complete source-specific histogram:**

| Validly allocated source lower bound | Assignment count |
|---:|---:|
| 0 | 5,268 |
| 1 | 6,880 |
| 2 | 2,674 |
| 3 | 609 |
| 4 | 172 |
| 5 | 20 |
| 6 | 1 |
| 7 | **1** |
| Total | **15,625** |

**Exact restricted optimum = 7** for the frozen WCA source, achieved **uniquely** when all six face actions are assigned to the same E0 four-edge pattern: [U,R,F,D,L,B] owners = [0,0,0,0,0,0]. Thus this *exactly specified integer face-owner class* provides **no improvement even over the unsplit single-pattern max7**, let alone the existing unrestricted full-cube lower14. For the exact physical cost-partition class, the negative finite theorem is complete.

**Non-overclaim:** This does **NOT** prove that every fractional cost-share function, every non-face-uniform allocation across quarter/halfturn variants, every coupled-corner+edge quotient or every globally synchronized noncommutative action word must have lower bound at most7. The objective is concave piecewise-linear in action-cost weights, so its best value may occur in the INTERIOR of a face-price simplex; enumerating only extreme assignments is not an optimality certificate for fractional cost partition. Nor does the full-corner h9 obstruct larger coupled cubie constraints. The true hard question is to find a source-complete operator/word coupling retaining exact **relative turn order and the full cubie joint endpoint**.

## 5. Why this is mathematically harder than the prior complete 13-ball certificate

P1-R6's actual source-complete B6(goal)∩B7(source)=∅ was direct bidirectional coverage, explicitly certifying d18≥14. P0-R2 is not falsely upgraded to a 15- or 17-lower proof. It discovers and independently tests TWO physical quotient design limits:

1. **Full-corner state explosion**: a meaningful quotient already has 88,179,840 distinct states; a corner-only program can finish in 11 HTM even where the true whole-cube source requires at least14. A stronger bound must retain edge–corner coupling or source-dependent lookahead.
2. **Cost dual alone cannot automatically recover synchronization**: five projections may share costs safely, yet the entire studied 15,625-element integer face-owner class returns only source bound7. More general fractional action costs and joint ordering remain open.

The next scientific hypothesis should be **a genuinely coupled corner-edge quotient, or a certified full-cubie source-prefix cover using admissible downstream PDB bounds** that removes a nontrivial, counted region of complete original paths, with independently checkable coverage. Exact endpoint lookups are not enough if they forget noncommutative turn order. M*(5)'s idea of a proof cover is the methodological predecessor, not evidence that whole cube 17-turn nonexistence is already settled.

## 6. Reproduction contracts / source lineage

- Primary native computation is **Go**: exact physical source 54-sticker marker geometry, all five PDBs, 320 weighted subproblems, 15,625 face owner assignments and exact full-corner 88,179,840 BFS.
- Independent **C++17** reconstructs physical full 54-facelet sticker markers and the full-corner 88m group and its 12 exact spheres. Both use full physical legal 18 HTM and real frozen WCA source; this does not use a non-cube synthetic directed graph.
- **Lean 4** generic scaled five-cost joint-word arithmetic lemma is separately compiled by read-only CI if and only if an actual Lean job completes. No Lean proof of geometric physical equivalence or full17 cube impossibility asserted.
- JS/TS and Rust remain appropriate for future independent proof certificates and actual solver control; no Python-first computational architecture is adopted.
- Source receipts: [Go full corner](../../data/cuberev-025/p0_r2_full_corner_go_receipt.txt), [C++ full corner](../../data/cuberev-025/p0_r2_independent_cpp_receipt.txt), [Go weighted exhaustive face share](../../data/cuberev-025/p0_r2_operator_cost_go_receipt.txt). Each executable has expected-cardinality, physical original source and prior 18-word verification, plus/or equal-layer-count guards.
- **0.24 scientific predecessor is archived without erasure**. The exact former long README is independently preserved as [GitHub original Markdown](../../archive/readme/README_RESEARCH_CURRENT_FULL_PRE_P0R2_20261012.md) with original Git blob SHA \`11f726c24f6bc032f2469f91f4dc60c5d7d3a92a\`, plus a **byte-for-byte matching actual raw Markdown in Google Drive**: [CUBE-REV / 80_ARCHIVE / README](https://drive.google.com/file/d/1QQ18TJ2Ary6xl4tD1iRX3ErdVx5HDHwi/view). No previous science document is deleted, only a redundant long README synopsis may be slimmed after exact copy inspection.
- New scientific code commits must be human WhoSia author/committer only; GitHub Actions \`permissions: contents: read\`, no bots writing commits. New P0-R2 original Go/C++ plus Lean 4 Actions [#38354902944](https://github.com/WhoSia/CUBE-REV/actions/runs/38354902944) **COMPLETED SUCCESS** with both native and Lean jobs passing; readback was performed against actual job steps. Source head sha 783ebe2c75df12c23cbc3542f33da0e324723081. Read-only pipeline does not modify tracked files and never authors commits.

**P0-R2 verdict:** Verified physical **88,179,840** full-corner quotient, global corner diameter **11**, frozen-source corner h=**9**, and exact integer five-pattern face-owner cost partition optimum **7**, neither exceeding prior unrestricted whole3×3 lower **14**. This establishes a source-graded barrier for the specified quotient/budget class, not a general impossibility of full cube geodesic certification.

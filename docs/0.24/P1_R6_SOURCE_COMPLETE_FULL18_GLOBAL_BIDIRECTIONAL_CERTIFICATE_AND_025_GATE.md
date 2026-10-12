# CUBE-REV 0.24 P1-R6 — Global Geodesic Certification Beyond Phase Decomposition: Source-Complete 18-HTM Lower Bounds, Exact Whole-Cubie Bidirectional Search, Symmetry-Safe Proof Frontiers and Independent Checkers

**2026-10-12 · ACTIVE P1-R6 · LOCAL C++ AND INDEPENDENT GO PASS · EXTERNAL CI PENDING**

## Original Rubik cube target, not a restricted DR word problem

This concerns the same genuine [WCA Seoul Summer 2026 3×3 Final Group A scramble 1](https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles):

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

Previous P1-R5-R1 proved an actual legal **18 HTM complete whole 54-sticker solution** (independently original-physical C++ and Node replay):

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

Thus d18(s) ≤18. Its NISS + exact DR phase2 provenance is historically important but does NOT prove global minimality. The new P1-R6 removes every DR/HTR phase-choice assumption from its negative source-ball proof.

## Exact global source-to-goal meet-in-the-middle theorem

Let G be the full fixed-center 3×3 cube group, A the complete 18 HTM legal reversible face-turn generators, e the solved state, and s the actual original scrambled whole cube. Let B_r(e) be the set of all whole-cubie states reachable from identity within r legal turns. The source right-Cayley ball is B_t(s)=s B_t(e). Then:

\[
d_{18}(s,e)\le r+t\iff B_t(s)\cap B_r(e)\ne\varnothing.
\]

If a solution word has ≤r+t letters, split after at most t moves: the reached intermediate state is at most r legal moves from the goal. Conversely, an intersection joins two actual legal paths to yield a complete source solve of length≤r+t. This is source-complete over all original face turns and original full cubies. No NISS/DR, synthetic abstract nodes, mental-state inference, or subgroup-only certificate enters this equivalence.

**Actual result:**

\[
B_7(s)\cap B_6(e)=\varnothing
\quad\Longrightarrow\quad
\boxed{14\le d_{18}(s)\le18}.
\]

This is an UNRESTRICTED exclusion of all legal words length≤13 on the actual original cube, but DOES NOT exclude lengths14–17 or certify the 18 witness as minimum.

## Source-complete C++17 verifier and actual local reproducibility

[Original whole-cube C++17 exact global 6+7 verifier](../../scripts/cuberev-024/p1_r6_global_full18_bidir_cpp/main.cpp) reuses true legal original 54-facelet-derived cubie turns from the separately developed [P1-R3 physics kernel](../../scripts/cuberev-024/p1_r3_true_54_facelet_multiaxis_dr_cpp/main.cpp). It constructs a full BFS goal ball through depth6 using all 18 physical face moves. Cubie equality is **two exact 64-bit words**, each bitwise encoding all CP/CO (8 corner identities and twists) and all EP/EO (12 edge identities and flips). The packed keys are INJECTIVE on all valid cubie states and explicitly round-trip checked for 256 generated actual legal move states. A hash collision can at worst place different keys into the same hash bucket; full stored key equality prevents any dropped distinct states.

Complete goal sphere counts and cumulative counts:

| Depth | New distinct real full cubie states | Cumulative |
| ---: | ---: | ---: |
| 0 | 1 | 1 |
| 1 | 18 | 19 |
| 2 | 243 | 262 |
| 3 | 3,240 | 3,502 |
| 4 | 43,239 | 46,741 |
| 5 | 574,908 | 621,649 |
| 6 | **7,618,438** | **8,240,087** |

The exact 4/5/6 layer totals have executable regression assertions. The source-side complete 18 HTM DFS explores all candidate normal-form legal words at depth0…7, omitting only adjacent identical-face turns (can be combined or cancelled) and canonically ordering opposite disjoint commuting faces. Every shortest legal word has an equal-length representative in this language: thus these physical group reductions do NOT drop arbitrary solutions. No source-stabilizer quotient or unjustified 24-rotation symmetry reduction was used.

Source recursion entry counts for successive completed iterative-deepening bounds 0–7:

    1, 19, 262, 3,502, 46,756, 624,124, 8,331,112, 111,207,592

Sum **120,213,368** recursive entries, including repeated earlier depths; these are NOT 120 million independent cube positions. All depth0…7 bounds FINISHED; **zero actual whole-cubie intersections**. On a capped execution, the code emits an explicit nonzero RESOURCE_HOLD and must never return a negative certificate.

**Local final-version actual execution:** g++ 14.2 C++17 O3; full B6(goal) + B7(source), exit status 0, **81.59 seconds wall clock**, peak resident size **653,964 KiB (~638.6 MiB)**, zero resource holds. The local source SHA-256 is **e46476b5513a2e46fdc46236b209ac05c2e35e080935b18b7f90e2e9286c2e5e**. Local maximum memory/time are hardware-specific, not a universal solver performance claim. This is a programmatically REGENERABLE exact exhaustive proof, not an independently checked externally signed proof artifact.

## Genuinely independent Go original physical facelets

[Go full 54-sticker original-facelet geometric checker](../../scripts/cuberev-024/p1_r6_independent_54_facelet_go/main.go) independently constructs 54 sticker locations+normals, six original face colors, and all 18 legal face turn permutations. It does not import the C++ CP/CO/EP/EO representation or any prior cubie move tables; state equality is an exact 54-byte color pattern.

The Go complete whole-sticker goal balls through radius5 independently show 574,908 states at exact depth5 (621,649 cumulatively), replay the same official input+18 word to strictly solved original stickers, and find:

\[
B_5(s)\cap B_5(e)=\varnothing \Rightarrow d_{18}(s)\ge11.
\]

Source bound recursive calls in Go are [1,19,262,3502,46756,624124], all completed. Its independent local computation took around **0.692 seconds** on this environment. Go source SHA-256 **b6e6ae4cb53a09a884f0c1c7af78a05c1121b0137302d4f47a93318752065e45**. **Do not claim the Go model independently confirmed the stronger C++ lower14:** its independent source-complete proof is lower11 only.

[Read-only Github Actions source](../../.github/workflows/cuberev-024-P1-R6-full18-global-bidir-and-independent-facelets.yml) exercises the C++ original whole-cubie B6+B7 certificate, independently authored Go full original sticker B5+B5, and inherited Node original 18-word replay. Strict GitHub Actions read permissions; no code writes; no github-actions[bot]/github-action[bot] authors or committers. **External workflow result not yet confirmed.**

## M*(5), source-complete proof and the genuine unsolved geodesic

Older CUBE-REV M*(5)=8 was a separate finite exact-covering theorem with valid dual/integer and exhaustive residue proof layers; it is NOT an algorithm for whole-cube HTM optimum. The method to inherit is the insistence on defined universes, explicit admissible reductions, numerical coverage receipts and no false status upgrades.

This cube now has global interval **14–18**, and a constructive legal solution of length18. To prove d18(s)=18 one must still exclude EVERY legal whole-cube word of length14,15,16,17; a fully correct sufficient condition is B9(e) intersect B8(s) empty. Naively materializing huge additional whole-cube balls may exceed workstation memory, so P1-R7 should study source-safe cosets, true source stabilizers, external-memory compact path joins, stronger full-cubie admissible quotient lower bounds and independently checkable frontier-shard certificates. Anything conditional on DR first entry must remain a separate, subordinate proof grade. No mathematical claim d18=18 is made.

## 0.25 transition timing — conditional scientific gate, not an arbitrary deadline

**Recommendation: do NOT hold version 0.24 indefinitely until the entire 17-turn impossibility problem is resolved.** 0.24's original contract is a physically real executable Rubik search architecture: actual hard public WCA/FMC source transfer; full-sticker search witnesses; honest admissible lower bounds; independent replay; documented failures. It has progressed from a trivial 20-turn inverse to verified 19 and 18 moves, DR axis/phase-interface counterexamples, bounded negative courts, and NOW a source-complete full18 proof of lower14.

**Transition gate:** Complete the P1-R6 external CI readback and one short **P1-R7 0.24 scientific freeze and 0.25 design gate** to seal all live Git blob SHAs, reconcile historical false claims, benchmark actual RAM/hardware, preserve source rights, and freeze the exact open full-cube 17-turn certificate contract. Then **propose 0.25 in the next 1–2 research stages**, without waiting for an impractically large full17 proof. This is a recommendation, not a user-authorized version switch.

**Suggested 0.25 formal title:** CUBE-REV 0.25 — Proof-Carrying Physical Program Synthesis for the Rubik's Cube: Source-Complete Geodesic Certificates, Coset-Guided Search Architecture, Adversarial FMC Prediction & Timed Speedcubing Mechanism Falsification.

0.25's flagship remains the genuine full-cube 17-turn benchmark (known actual interval14–18), with an expanded, distinct real speedcubing Cross→F2L and rights-checked direct move/timestamp evidence axis, not AI guessing human thought from unrelated videos. TCS and group theory serve original Rubik's cube engineering; administrative tasks are supporting release hygiene.

**Status summary:** C++ full B6+B7 local PASS, independent Go physical B5+B5 local PASS, 18 original physical solution PASS; source files/CI/document committed, external Actions PASS unverified, no unapproved actual 0.25 activation.

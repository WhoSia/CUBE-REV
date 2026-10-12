# CUBE-REV 0.24 P1-R5-R1 — Dual-Sided Conway Interface Surgery for a Genuine 18-HTM Rubik's Cube Solution: NISS Premoves, Original DR Geometry, Exact Quotient Bounds and Independent Whole-Facelet Proof

**Scientific judgment, 2026-10-12:** A NEW full legal original 3×3 **18-HTM complete-cube solution** has been found for the unchanged actual public WCA Seoul Summer 2026 Final A1 twenty-turn scramble, independently physically replayed in the previous complete 54-sticker Node and C++17 cube kernels. The former reliable upper bound was 19, before that 20. Therefore **d18(s) ≤ 18 is CONSTRUCTIVELY PROVED**, while **d18(s) = 18 as unrestricted global minimum remains UNPROVED**. GitHub Actions has not yet produced a verified completed external job receipt, so local result should not be called external CI PASS.

## 1. Immutable original public physical source and newly discovered whole-cube word

Source: [World Cube Association, Seoul Summer 2026, 3×3 Final Group A scramble #1](https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles):

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

**NEW original fixed-frame 18 HTM entire original cube solution:**

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

Every action is a genuine legal 90/180/270 degree physical outer-face HTM move. Applying source then this word to the original complete 54-sticker cube gives all original corners and edges at solved identity with correct fixed color-center frame. This is a machine-discovered program, NOT an athlete's observed or source-authored solution. It is a new strictly shorter physical solve relative to previous 19 and original inverse-scramble20. No lower-bound certificate excludes 17 or fewer.

[Complete source-generating C++17 two-sided original physical search](../../scripts/cuberev-024/p1_r5_niss_two_premove_cpp/main.cpp); [independent previously maintained Node original physical 54-sticker proof](../../scripts/cuberev-024/p1_r5_independent_original_54_facelet_18_replay.mjs); [read-only exact positive and negative CI](../../.github/workflows/cuberev-024-P1-R5-conway-full18-boundary-and-niss.yml).

## 2. The exact dual-side group mechanism: genuine cube moves, not textual NISS fantasy

Let s be the fixed WCA scrambled complete cube group element; choose the TWO actual outer-face premoves:

    q = F R2

Construct a different computational planning source by applying q BEFORE the official original scramble: the legal whole cube group element is q*s. Use the ordinary original-frame U/D-axis DR search to find an actual legal completion x of q*s. This is a **counterfactual mathematical source transformation**, never an assertion a speedcuber rotated or premoved their physical puzzle.

The new C++17 solver obtains x in two genuine physical parts:

    DR arrival, 11 actual legal turns:
    p1 = F U F D' R' F' L' F' D' L B

    DR subgroup continuation, 6 actual legal turns:
    p2 = L2 F2 U2 L2 U F2

These are not synthetic abstract nodes; the actual q*s*p1 endpoint has zero corner/edge orientation and correct DR slice, independently checked against genuine 3D cubie movement. The exact real 967,680×2 phase2 quotient PDBs give a **lower bound 6** for this reached original cubie DR endpoint, and p2 gives a valid six-move upper bound. Thus six is the **exact shortest continuation IN THE STATED 10-move DR subgroup grammar for THIS reached state**. This does NOT certify that any whole-cube 18-move solution is globally minimum.

The identity of actual cube-group products proves:

    q*s*p1*p2 = identity
              implies
    s*p1*p2*q = identity.

Mapping back to the UNMODIFIED official source produces a raw original-frame move program of 11+6+2=19 HTM:

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F2 F R2

The suffix interface is **F2 F = F'**, a real same-face group power product. Replacing those two physical legal moves by one gives exactly the **18 HTM word above**, and strict original source 54-sticker replay proves both 19-raw and 18-normalized programs reach the same fixed original solved cube.

**Discovery mechanism:** previous P1-R4 found 20→19 at an INTERNAL DR stage boundary (B B2 = B'). Here 19→18 occurs at the EXTERNAL original-versus-inverse NISS interface (F2 F = F'), after changing the actual search starting group element to q*s. Both cases require respecting the group product metric across algorithmic phase boundaries. This is a source-conditioned constructive cube engineering result, not the invention of NISS, Kociemba two-phase, or basic power/commutation relations.

## 3. Why the 18 result was not found in the previous courts

The [preceding P1-R5 source-restricted negative courts](P1_R5_SOURCE_FULL18_TARGET_BOUNDED_CONWAY_TRACE_NISS_COURTS.md) remain **true ONLY inside their typed original source search grammars**:

- No q premoves: UD/FB/LR original source, phase1 depth7..13, raw two-phase length≤20 with full commutation+same-face-power trace closure. The recorded 1,064,982,678 phase1 recursive entries, 1,099,928 original DR contacts and 74 whole goal-reaching program words all completed without cut, but none gave ≤18. This does NOT exclude the NEW inverse-side q transformation.
- NISS ONE legal premove: all 18×3=54 source-frame combinations, depth≤12 (extended after the initial shallower depth11 court), **1,372,877,118** phase1 recursive entries, no ≤18 and NO resource cuts. It does not cover a TWO-move q such as F R2.
- NISS TWO legal premoves: all 243 canonical length-two actual 18HTM q words ×3 source-DR frames = 729 cases. At explicit depth≤10 the full physical search finished, 103,578,829 phase1 calls, no ≤18, no cuts. This new witness enters DR after **ELEVEN** phase1 moves. Increasing this bound to 11 exposes the actual q=F R2 / UD-axis source and constructs the 18 word. This is a **positive counterexample to promoting depth10 NISS2 non-discovery into an actual global lower bound**.
- LR-axis no-NISS phase1 depth14 resource experiment hit a roughly two-billion-recursion cap and did not finish. Its result is explicit PARTIAL_RESOURCE_HOLD and contributes NO global distance lower bound.

No negative experimental source file is silently deleted. The P1-R5 no-18 statement is a bounded-universe historical receipt and is now accompanied by this documented real positive 18 program. The scopes form a meaningful hierarchy: a more powerful original cube action-side language opens an authentic solution that the smaller languages could not generate in their budgets.

## 4. Independent original-physical proof and exact source dependencies

The C++17 source imports the previously independently built real original 54-sticker cubie/facelet engine and physically generated admissible PDBs; it checks q*s*stage1*stage2 is solved and s*raw19 and s*normalized18 are solved, plus actual DR membership and hDR=6 with an exact six-turn subgroup suffix. The completed local output states:

    NISS2_EXACT_DR_SUFFIX_PDB_SANDWICH LOWER 6 ACTUAL_WORD_LEN 6 TRUE_DR_MEMBER 1
    NISS2_ACTUAL_GROUP_FACTOR_CERTIFICATE P1_LEN 11 P2_LEN 6 SUFFIX_PREMOVES_LEN 2 RAW_LEN 19 TRACENORM_LEN 18
    NISS2_SOURCE_VERIFIED_COMPLETE_18_WITNESS F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2 LENGTH 18 PREMOVES F R2 AXIS UD

The separate inherited Node original cube engine (repository original source blob 966ae653c9d204a4418a017e11efce6ff3c9d669) reconstructs the identical official source physical 54-sticker state and independently verifies all original cubies and sticker positions/orientations, the raw and normalized equivalent solutions, and the original dual-side identity. Hash output in the local imported-source V8 test was stubbed only for cryptographic metadata, not for the cube geometry; real Node CI will compute actual SHA-256. These are two distinct physical code paths, **not two distinct athlete observations**. Actual complete external Actions receipt is still pending.

## 5. No premature 'God's distance 18' conclusion; relate rigor to earlier M*(5)

The observable source full-cube word is a valid UPPER-BOUND CERTIFICATE. It establishes exactly d18(s)≤18. To establish actual d18(s)=18, the remaining proof must exclude **every whole-cube legal 17-or-fewer sequence**, not just the prior original-source DR programming language or 783 finite premove tests. Under the symmetric actual 18-action Cayley graph, a correct global 17-distance-exclusion condition is:

    B_8(identity) ∩ s * B_9(identity) = empty.

This requires source-complete group ball intersection/coset data, or an equivalent verifiable admissible lower bound/proof partition for **ALL** 18HTM possible words. The group has vastly more states than the already large fixed 1,192-source observational dictionary family in the old 0.19 [M*(5)=8 complete covering proof](../0.19/P13_FINAL_EXACT_PHYSICAL_MSTAR5_EIGHT.md). The earlier result supplies a model for structured orbit/finite-case/dual-certificate accountability, but absolutely NOT an unrestricted 3×3 God-distance lower-bound fact.

Proposed next name: **CUBE-REV 0.24 P1-R6 — Global 17-HTM Exclusion and Proof-Carrying Dual-Coset Search for the Actual Rubik's Cube: Admissible Cubie PDB Refinement, Exact Bi-Sided Frontier Intersections, Group-Word Stabilizer Accounting and Independent Physical Certificates.** The next attempt should seek a legal 17-or-fewer whole-original-cube word OR construct a genuinely full-space negative certificate for such words; do not infer d18=18 from the completed but narrower source courts. Genuine speedcubing action observations require existing authorized move timestamps and cannot be invented from official scramble/source text alone. Private 451 solve records remain outside this public work. GitHub WhoSia human author and committer only; github-actions[bot]/github-action[bot] must not author or commit, workflows read-only; no general hardware/CI PASS claims without completed execution receipts.
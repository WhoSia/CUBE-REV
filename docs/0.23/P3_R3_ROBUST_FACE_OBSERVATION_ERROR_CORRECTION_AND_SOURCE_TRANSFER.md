# CUBE-REV 0.23 P3-R3 — Robust Physical Observation Codes & Human-Source Identifiability

**Provisional full name:** CUBE-REV 0.23 P3-R3 — Source-Calibrated Physical Observation and Algorithmic Robustness: Exact Six-Face Erasure Geometry, One-Error Correction Impossibility, Maximum 26-State Robust Subcodes, Human-Archive Positivity Barriers & Mechanism-Falsifiable Cross-Ecology Transfer.

**Status:** Combinatorial calculations locally cross-checked. Independent GitHub Actions completion, manifest reconciliation, and Notion final readback are separate release gates; do not claim external CI PASS before reading its actual conclusion. **CUBE-REV 0.23 remains ACTIVE.** Human cognition causal inference and literal public 2×2 source frame remain HOLD.

## Historical recovery from 26.md

The exact [Drive Chat Archive 26.md](https://drive.google.com/file/d/17-CmE97mrzmh_pqPLGMS_RFvV1jjlJk-/view) was reviewed for trajectory and research intent, not treated as scientific proof. The 0.22 P7 source court found that physically identical DR states can appear under distinct authentic written human words (Miao/Riabov). P8 then tested actual-source fixed-prefix full-cube completion and DR/HTR stage costs rather than treating recorded DR as the literal prefix of every submitted FMC final. The Pareto PDB rank reversal showed that independently admissible lower bounds can rank the real source-conditioned physical candidates backward. P3-R0/R1 then froze **62 different actual 3×3 complete cubies with identical full CP/CO**: one fixed corner-completion word suffices, but the exact whole-cube goal requires 62 distinct complete words and an ideal face-observation policy with four face reads in the noiseless all-state case.

P3-R2 shifted to real-source grammar and the private human record boundary. The public 2×2 athlete's literal scramble/reconstruction FAIL survives; a single extra unreported y2 frame among 24 orientations is only a compatible model-side conditional repair. From the private original 452-source archival ZIP, 451 unique 3×3 written reconstruction contents and 25,272 written next actions were retained; cumulative SAME vs DIFFERENT whole-cubie group common CP/CO comparator keys fall **181→120→43→9→0** under frame/stage/recent-action matching. Zero shared final support does not mean an estimated cognitive effect of zero.

The historical researcher's recurring instruction is decisive: remain on the **actual physical Rubik cube, legitimate moves, human-authored source candidates and falsifiable geometrical constraints**; do not retreat into detached epistemic scalar prose. This substage develops an exact *physical observation noise* falsifier while preserving every distinct source and proof grade. Chat messages are secondary historical records; verified GitHub fixtures, CI and Notion are the scientific authority.

## Frozen physical model and observation semantics

Use the unchanged P3-R1B [62×6 original nine-sticker face fixture](../../data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv). It was independently derived earlier from real original whole-cubie/54-sticker 3×3 transitions and represents 62 distinct source states in the actual all-18-HTM radius-five ball that share one complete corner CP/CO value. This P3-R3 computes *only* a finite code over those frozen physical faces; it does not independently replay the original Rubik cube.

Let S contain exactly these 62 source states. Each face observation O_f(s) is a **complete ordered nine-sticker color string** on U,R,F,D,L,B, not a human glance, bit, single sticker or working-memory chunk. The fixed six-symbol codeword for state s is (O_U(s),O_R(s),O_F(s),O_D(s),O_L(s),O_B(s)). For any fixed face subset Q, define d_Q(s,t) as the number of different **complete-face symbols** between two source states.

The new adversarial fault contract permits at most one **complete reported face symbol substitution** anywhere in the six symbols, or one **known erasure** (location explicitly reported). It does not model any measured human noise rate, allow unpriced remeasurement, change cube rotations or change the goal of exact full-cube identification. A corrupted reported string need not represent a physically reachable uncorrupted cube observation.

## Exact finite physical-face distance census

All 1,891 unordered source-state pairs (62 choose 2) have the following exact six-face Hamming distances:

| Different complete faces | Pair count |
|---:|---:|
| 0 | 0 |
| 1 | 0 |
| **2** | **142** |
| 3 | 216 |
| 4 | 390 |
| 5 | 400 |
| 6 | 743 |
| **Total** | **1,891** |

Thus the minimum full-six-face distance is **2**. Exhausting every one of the 64 fixed face subsets and all pairs gives the maximum attainable minimum pair distance at fixed face budget q=0,1,2,3,4,5,6 of **[0,0,0,0,1,1,2]**. The *only* fixed subset with minimum distance at least 2 is the complete six faces.

### Theorem R3-A — One arbitrary wrong complete-face report defeats 62-state certainty

Take any of the 142 pairs of truly distinct physical source states with two differing face symbols. A report agreeing with the first state on one differing face, with the second state on the other, and with both on all shared faces is exactly one-symbol-corrupted relative to **either** state. A decoder required to identify all 62 states with certainty under any one adversarial face substitution cannot do so. This impossibility survives adaptive ordering of the same six distinct face readings without independent remeasurement, since the adversary may commit to this identical face-indexed report.

### Theorem R3-B — Exactly six fixed distinct-face reads guarantee one marked-erasure recovery

A finite code corrects any single erasure of known location iff its minimum pairwise symbol distance is at least 2. The full six-face physical-source code meets this condition, but no proper fixed face subset does. Therefore **six is the exact minimum under the fixed non-repeated face-subset contract**. This conclusion does **not** establish a lower bound for all possible adaptive erasure policies or for repeated observations. The original P3-R1 noiseless adaptive and fixed complete-identification budget of four faces is intact because its fault assumption differs.

### Theorem R3-C — Maximum one-error-correctable frozen physical-state subcode is exactly 26

A subset T of the 62 physical states has guaranteed one-face-substitution correction iff every pair in T differs in **at least three complete face symbols**. Build the graph G with 62 physical-state vertices and edges joining source-state pairs differing in at most two complete face symbols. Exactly 142 such edges exist. A one-error-correctable subcode is exactly an independent set. Graph component sizes are **23,23,4,4,1,1,1,1,1,1,1,1**; full finite exact componentwise optimization gives

**Maximum robust source-subset cardinality alpha(G) = 26.**

This is an exact statement about the frozen set of 62 *genuine* whole-cubie source states and the specified six-symbol observation channel. It is **not** the number of people, retained solution algorithms, neurologic chunks, human recoverable states or a universal theorem for all 2×2/3×3 states.

## Independent algorithms and original-source verification boundaries

- [Node exact verifier](../../scripts/cuberev-023/verify-p3-r3-robust-face-observation.mjs): frozen original fixture structural/color validation, 1,891×64 pair comparisons, distance count and full componentwise exact minimum vertex-cover algorithm.
- [Go exact verifier](../../scripts/cuberev-023/p3_r3_robust_face_go/main.go): independent CSV loading, 64-partition exhaustive geometry and componentwise **minimum vertex cover**.
- [C++20 exact verifier](../../scripts/cuberev-023/p3_r3_robust_face_cpp/main.cpp): independent CSV loading and componentwise **maximum independent set** with explicit correctable 26-index witness, verifying every chosen pair differs in three or more faces.
- [Strict read-only Actions workflow](../../.github/workflows/cuberev-023-P3-R3-robust-face-error-code.yml): original GitHub fixture; source-only Node, Go and C++ checks; full branch bot-author/committer gate; no Actions git push/commit; repository contents read permission only.

Local Go/C++ source compilation and combinatorial tests used a **signature-equivalent synthetic CSV** (same original source equality relations on each face, but not a full physical-sticker reconstruction). The actual original fixture was directly re-evaluated separately using the live GitHub connector. The independent Actions run on the *real GitHub physical fixture*, not on the synthetic local surrogate. Do not misdescribe these combinatorial reproducibility audits as independent 54-sticker physical engine construction. Separate CI run and readback are required.

## Why this remains physical TCS rather than human psychology

The exact resource variable is a **whole-face observation symbol**. The earlier noiseless four-face policy, all-face single erasure optimum and all-face single wrong-report obstruction measure different mathematical tasks. Nor is the 26-state maximum a compression length theorem: earlier 62 different exact solving words are not 62 distinct source-programs. Any program or recognition-memory comparison needs a frozen representation language, action semantics and execution/query costs, not a free universal solver.

The 451 private human-written 3×3 solve records supply **no measured nine-sticker-face error process**, actual gaze, calibrated observation cost or fully supported final stage-conditioned comparison. No extra raw names, scrambles or trajectories are copied to the repository. WCA 2×2 outcome timing does not supply those variables. The conditional missing y2 source rotation is not a real player action. Human mechanism, behavioral economic System 1/System 2 interpretation, brain physiology and source-held-out selection remain **NOT IDENTIFIED**.

## Next stringent research court

1. Analyze **adaptive** minimax face selection with one explicitly marked erasure and **no repeated face**: can a five-query decision policy succeed despite the fixed-mask five-face obstruction? Do not prejudge the result.
2. Explicitly price face re-reads and bound errors; distinguish a static six-face code from an interactive fault-tolerant decision tree.
3. Compare minimal word dictionaries with **concretely specified and priced algorithm programs** without quietly equating a short generic solver with human learning.
4. Independently verify a second real 2×2 textual reconstruction under **source-authorized** frame notation; do not insert unreported orientation to rewrite original human evidence.
5. Maintain privacy-safe source-stratified negative controls and report empty common support without estimating a person-specific cognition effect.

## Governance

Active branch research/current; CUBE-REV 0.23 persists. GitHub author and committer identity must be **WhoSia, never github-actions[bot] or github-action[bot]**. Every new path needs its actual post-creation Git blob SHA in G7-P7 exact allowlist, and full audit is read-only. No history rewrite, source deletion, new human recruitment or data rights expansion. README stays concise, while Notion receives research decisions, this document full assumptions/proofs, and Drive preserves Chat Archive 26.md. Past CI failures remain visible; a historic bot-origin deployment commit on nondefault main remains a separate provenance issue and is NOT silently declared solved.

**External science/gov PASS is conditional on independent Actions success plus Notion/README/manifest reconciliation.**

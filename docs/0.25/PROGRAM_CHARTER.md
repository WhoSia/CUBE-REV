# CUBE-REV 0.25 — Proof-Carrying Physical Program Synthesis for the Rubik's Cube: Source-Complete Geodesic Certificates, Coset-Guided Solver Architectures, Adversarial FMC Prediction & Timed Speedcubing Mechanism Falsification

**Status: ACTIVE — formally researcher-approved on 2026-10-12.** Authorized opening after [CUBE-REV 0.24 P1-R7 Scientific Freeze](../0.24/P1_R7_SCIENTIFIC_FREEZE_AND_025_HANDOFF.md). **Current substage: P0-R6 physical certified source-complete frontier (B8 source vs B6 goal) CLOSED AS A GLOBAL LOWER15 CERTIFICATE; further 15–17 HTM geodesic search and solver-program benchmarking remain OPEN.** The original 0.25 opening-era charter below remains preserved as historical specification. Programme 0.24 is CLOSED AS RESEARCH-ARCHITECTURE BASELINE, not retroactively rewritten and not declared to have proved its hardest global optimality question.

**Canonical [Notion 0.25 active child research page](https://app.notion.com/p/3f7ef561cf9281ae8e94c46e9f916fdc).** This 0.25 page is the direct descendant of the preserved canonical 0.24 Notion page; archive history not deleted.

## 1. Actual research object, exact semantics and inherited source

We study the **real 3×3 Rubik's Cube**, fixed original 54 stickers, 8 corner permutations and twists, 12 edge permutations and flips, complete legal 18 outer-face HTM generator set, and source-graded actual human-authored FMC candidate programs. TCS and group theory serve EXECUTABLE solver engineering on genuine legal physical cube states; never substitute a small synthetic graph, generic 'observation authority' philosophy, or software governance for the original cube.

**Frozen common WCA global-distance test state:** official [WCA Seoul Summer 2026 3×3 Final Group A scramble 1](https://www.worldcubeassociation.org/competitions/SeoulSummer2026/scrambles):

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

**Physical completed witness, 18 HTM:**

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

The source and 18-turn word have independently been replayed on actual original 54-sticker cube implementations. The inherited WHOLE legal HTM state-distance fact is exactly:

    14 <= d18(s) <= 18

The LOWER14 is a source-COMPLETE all18 HTM ball-disjointness certificate, not a DR-constrained non-observation; [P1-R6 C++ full B6(goal)+B7(source) proof](../0.24/P1_R6_SOURCE_COMPLETE_FULL18_GLOBAL_BIDIRECTIONAL_CERTIFICATE_AND_025_GATE.md) enumerated 8,240,087 exact complete cubie goal states, searched 120,213,368 source recursive entries, and found no intersection. [Externally completed P1-R6 CI run #38210864083](https://github.com/WhoSia/CUBE-REV/actions/runs/38210864083) SUCCESS. Independently programmed Go original 54-sticker B5+B5 verified only LOWER11, not the stronger lower14. All unexamined lengths 14–17 remain OPEN. **0.25 must not describe 18 as optimal without an unrestricted d18>=18 lower certificate**.

## 2. P0 — Source-complete geodesic certificate contracts

**P0 title:** CUBE-REV 0.25 P0 — Physical-Cubie Quotient Proof Obligations & Bidirectional Witness Completeness: Exact State Codes, Source-Stabilizer Audits, Admissible Pattern Databases and Certified 17-Move Exclusion Frontiers.

Formally define G as the actual fixed-center whole-cube group and A the 18 legal HTM moves. Source s is the physical public cube above. A 17-or-shorter solution exists iff the exact genuine full-state balls B8(s) and B9(e) intersect. An independently replayed 17-word would refute a proposed lower18. A **complete sound exclusion** would prove B8(s) intersection B9(e) empty, or an equivalent complete proof with source-safe abstract lower bounds and independently checkable source-state coverage.

A high-value exact **admissible frontier cover alternative**, avoiding full B9 materialization, is: for EVERY actually reachable canonical source prefix u with |u|<=8, obtain a certified lower bound h(su) > 17-|u| to the original solved state; if coverage is complete and h<=true remaining shortest distance, all <=17 original whole-cube solves are impossible. Some strong projections may certify bins and other bins need exact search; missing bins are HOLD, not proof. No abstract projection may identify different whole cubie states as equal in a way that falsely asserts source-prefix completeness.

**Certificate object types required for P0:**
- SOURCE_CUBE: original public face word and the entire fixed-reference 54-sticker terminal state, canonical deterministic encoding CP/CO/EP/EO and independent recomputation.
- GENERATORS: exact 18 move permutations, physical layer coordinate convention, side-dependent turn notation and true facelet-to-cubie homomorphism checks.
- FRONTIER: exact prefix depth, parent/reference convention, full-state reversible keys, unique counts by layer and sound normal-form pruning rules, explicit resource/partial results.
- QUOTIENT: physical state-to-quotient projection, group-action or graph-homomorphism proof, edge cost/HTM preservation, admissible distance-to-solved PDB table SHA and independent consistency check.
- SYMMETRY: any action identifying states must preserve ALL legality, move costs, and the specific SOURCE–GOAL relation; source stabilizer / double coset action must have exact orbit multiplicities and no unsupported 24-fold division.
- COVER: disjoint/overlapping shard rule, proof every canonical source prefix is represented, a typed per-shard verified lower bound or exhaustive next-stage search, and an explicit complete union certificate.
- WITNESS: any found shorter full original 3×3 HTM word, strict 54-sticker replay and actual length normalization; a witness of <=17 takes precedence over all negative heuristics.
- EXECUTION: compiler/toolchain/hardware, wall time, peak RAM, disk, hash/record checksum, exact source commit, read-only CI with human authors, and independently authored verifier output.

**Hard gate P0→P1:** implement one useful EXACT sound quotient/coset pruning mechanism on original full cubies and attach a falsifiable held-out original WCA/FMC bench, or provide an actual new unrestricted lower-bound frontier. A plan or mathematical restatement alone is NOT a PASS.

## 3. P1 — Executable solver program synthesis

Build an actual C++20/Go/Rust/Lean-backed whole-cube solver architecture (JS/TS for independent physical replay where useful). Python is not the preferred research core. A program is not merely a sequence dictionary: it is a typed executable branching/search construction with legal HTM state transitions, phase-interface cost and verified target.

Attack the fundamental separation between choosing an intermediate subgroup and obtaining the globally best complete word. For selected physical DR/HTR axis choices, compute frontier labels containing actual full-cubie endpoint, true source prefix cost and admissible downstream cost; candidate transformations preserve all real 18 HTM legal moves. Obtain proof-bearing branch elimination, optimality-preserving transposition table invariants, actual hardware-calibrated memory/time, and compare without unfairly omitting the trivial inverse original source as a baseline. A P1 claim of faster/better search requires a matched full-source benchmark, no silently weaker puzzle, independent legal replay, and an honest memory cost.

**Prior art boundary:** Kociemba's two-phase family, IDA*, PDBs, ordinary HTM legal moves, fundamental group laws and generic meet-in-the-middle are not presented as CUBE-REV discoveries. Novel work must lie in a new actual physical solver program/certificate, source-general hardware gains, or a genuinely new sound pruning mechanism.

## 4. P2 — Adversarial genuine FMC authored-program prediction

Use only authorized public original WCA/FMC sources and source-original move strings. Preserve NISS frame semantics, opposite-face commuting word equivalence, actual physical endpoint identity, timestamp/word role and uncertain literal parsing separately. **Miao and Riabov distinct written words but SAME actual main EO+DR cubie endpoint** are NOT two independent physical confirmations. The historical exact nine-move DR suffix was established in 0.22 and reverified in 0.24; it is not a newly observed athlete solve. Source interpretation HOLD such as Riabov Other #2 and conditional 2×2 unreported y2 remains HOLD.

P2 predictions need a frozen source-independent training/test split or adversarial held-out literal program source; compare actual reachable candidate sets, exact downstream HTM geodesic opportunities and recorded submitted words where authorized, not psychological intention inferred from written reconstructions. Previous private 451 human reconstruction records are not public; do not copy or expose them. No observational causal claim without common support.

## 5. P3 — Actual speedcubing Cross→F2L and timed-move mechanistic falsification

Do NOT repeat the trivial isolated four-edge Cross minimum exercise. On official real 3×3 whole scramble states, compute exact six-face Cross planning and the cost of genuine Cross-preserving first F2L pair or justified non-preserving transitions; keep full CP/CO/EP/EO for continuations and physically replay all partial programs. Model alternative objectives separately: HTM, cube rotations, regrips if directly timed, stage interface costs and forward solve opportunity. A move-optimal staged plan need not minimize observed speed.

Use license/consent-cleared direct smartcube BLE move-and-timestamp traces if available rather than presuming a YouTube vision model can recover intention. Held-out measured data must identify the original solver cohort, sample size, clock uncertainty and source rights. Video AI is an optional measurement method, never the scientific center; camera reconstruction without rights or independent move verification stays non-evidence.

## 6. P4 — Cross-ecology falsification and source-general validity

Stress sound exact cube algorithms across truly independent WCA original scrambles, original FMC source-authored programs, and allowed timed direct move events. Report source-level overlap, geodesic class overlap, time/memory hardware conditions, source wording ambiguity and failed hypotheses. A local success on ONE official WCA cube is a benchmark, not evidence for general algorithm improvement across scrambles or human cognition.

## 7. Governance, history and first actual action

Predecessor [0.24 final P1-R7 historical scientific freeze](../0.24/P1_R7_SCIENTIFIC_FREEZE_AND_025_HANDOFF.md) is preserved. Keep 0.19 M*(5)=8 finite covering theorem distinct from 3×3 global HTM geodesics; inherit proof architecture (coverage, separation of upper witness and lower certificate), not confuse problem domains. Preserve 0.22 original DR/FMC work, 0.23 62-state actual cube observations and source holds, 0.24 20→19→18 evolution and all negative cases. No deletion of science code merely to shorten history; future retirement requires exact preserved archive and reproducible source.

GitHub branch research/current, P7 ACTIVE exact-path Git blob allowlist, all new commits author and committer WhoSia only, NO github-actions[bot]/github-action[bot] research contributor and NO Actions git writeback. Read-only CI proof-grade claims require a completed run on exact code; never claim a new P0 CI PASS from a charter commit.

**Immediate P0 first problem to execute:** design one source-complete, collision-free whole-cubie prefix frontier across depth 8, then identify an exact admissible quotient capable of proving a nontrivial portion of the 17-turn exclusion by source-bucket, with a second verifier checking coverage and lower-bound soundness. The initial 0.25 opening does not yet prove global 17-turn absence or new speedcubing effects.

**Formal name approved as written by the researcher.**


## 2026-10-14 — Research-status amendment (supersedes opening-era numeric boundary)

**The source-specific whole-original-cube certified distance has been strengthened from the 0.24 inherited 14≤d18(s)≤18 to the NEW 15≤d18(s)≤18.** This applies strictly to official WCA Seoul Summer 2026 Final A1 and unrestricted all 18 legal outer-face HTM moves, not every possible 3×3 original cube.

[0.25 P0-R6B full-original B6 goal / B8 source GitHub Actions #38518179172](https://github.com/WhoSia/CUBE-REV/actions/runs/38518179172) **completed SUCCESS**, checking 8,240,087 exact full complete-cubie goal states, original canonical cumulative source depth≤8 baseline 1,604,664,504 recursive calls, 222,915,288 visited and 1,381,749,216 soundly omitted calls (one-step exact full-corner projected descendant cutoffs), zero exact CP/CO/EP/EO meets; independently Go-audited exact count partition, real 54-sticker physical representation and preserved independent 18-turn witness, actual wall 73.46 s and peak RSS 1,111,372 KiB. This excludes all original solutions ≤14 and proves 15≤d18(s)≤18 conditional on the physically checked inherited normal-form completeness and the explicitly demonstrated safe pruning theorem. It is NOT end-to-end Lean4 kernel verification or a second independent Go full-B8 traversal. All lengths 15–17 remain open.

[0.25 P0-R6A paired CI #38518178965](https://github.com/WhoSia/CUBE-REV/actions/runs/38518178965) measured P0-R5 vs one-step P0-R6A physical B7; new R6A achieved 47.13% lower wall time with 55.40% higher RSS on a matched single runner. [0.25 P0-R6C paired CI #38518179313](https://github.com/WhoSia/CUBE-REV/actions/runs/38518179313) found stronger common-one-action corner-edge pruning but 12.38% higher wall time and 20.61% higher peak RAM compared with A in its own paired run. [0.25 P0-R6D paired CI #38518256469](https://github.com/WhoSia/CUBE-REV/actions/runs/38518256469) further used the same ordered actual legal two-turn word in both true corner and edge projections; C 9,005,784 vs D 674,679 visited full source B7 recursive calls, but 20.01 s vs 20.00 s wall time, about 1,340,256 vs 1,341,068 KiB RSS. Stronger pruning alone is NOT a faster solver. [Lean4 P0-R6C generic soundness theorem Actions #38517271238](https://github.com/WhoSia/CUBE-REV/actions/runs/38517271238) independently kernel-built, limited to generic projected necessary conditions and not the physical full-B8 proof.

**Amended formal gate:** P0 has now produced an actual new original physical global lower-bound certificate. Further P0 or P1 branches must benchmark whole-cube source/goal fidelity and trade-off in proof coverage vs wall/RSS, optimize ordered-pair lookup overhead, and pursue either an actual 15–17-move full solution or complete global lower16+ certificate. A complete B9(source) vs B6(goal) nonintersection would certify lower16; absent such a completed certificate, do not advance the bound. The opening-era descriptions of "global lower14 unchanged" or "P0 no experimental discovery yet" in the preserved historical text are superseded only for this exact source/claim.

All commit author and committer metadata WhoSia, GitHub Actions read-only with no bot-authored commits, Research OS source privacy and protected 451 human raw records unchanged. Exact P7 active paths **777 unique**, with R6D source/report/workflow newly admitted.

# CUBE-REV 0.24 — Physical Search Architecture for the Rubik's Cube: Exact Geodesic Frontiers, Subgroup-Aware Program Synthesis, Adversarial Human-Authored FMC Benchmarks & Proof-Carrying Solver Innovation

**Status: ACTIVE — researcher expressly authorized this exact title on 2026-10-12 KST.** Current substage: **P0 — Original-Cube Physical Baselines and Falsification Contracts (OPEN; GitHub Actions external CI outcome pending).** The [proposed 0.24 pre-activation charter](00_PROPOSED_PHYSICAL_CUBE_SEARCH_ARCHITECTURE_CHARTER.md) is preserved unchanged as the historical proposal. 0.23 remains a preserved predecessor; it is not silently rewritten as 0.24 work.

## Research object: the actual Rubik cube

Our subject is the whole real 3×3 Rubik cube, its 54 original oriented stickers / 8 corners / 12 edges, its eighteen outer-face HTM actions, exact move geodesics, group/subgroup boundaries and executable search algorithms. 0.19–0.23 are essential evidence, not licenses to turn the program into detached epistemology, document maintenance, arbitrary observation symbols, or unsupported cognitive psychology. TCS here means substantive complexity, algebraic search, sound heuristics, proof-carrying algorithms and falsifiable solver architecture on authentic physical whole-cube states.

**Inherited finite cohort, not a generalization:** the former CUBE-REV 0.23 P3-R3B source set is **62 distinct full cubie states** selected as the maximum same-corner CP/CO fiber in the original 18 HTM radius-five ball. All 62 happen to have true globally shortest full-cube words made solely from six half turns. The 3+2 MITM with 34 goal-side states and <=154 input-side states solves these **62 particular states**; this is *not* a universal 3×3 solver or a new invention of meet-in-middle. Earlier 0.23 human-source conclusions and failures survive intact: literal public 2×2 source mismatch remains HOLD, model-only y2 frame not a player action, original 451 private reconstructed 3×3 solves and 25,272 written action tokens stay private, strict human-source comparison support collapses to zero, psychological causality NOT IDENTIFIED.

## P0 — Independent physical baseline and domain falsification (OPEN)

Freeze legal 18 HTM, the actual whole 54-sticker center frame and complete solved condition. [Node original-facelet physical baseline](https://github.com/WhoSia/CUBE-REV/blob/469e9cf07a633a87da300ffa0fdbbccc7230fc89/scripts/cuberev-024/p0_real_cube_parity_and_halfturn_domain.mjs) and [independent Go original-facelet baseline](https://github.com/WhoSia/CUBE-REV/blob/469e9cf07a633a87da300ffa0fdbbccc7230fc89/scripts/cuberev-024/p0_fullcube_parity_go/main.go) independently enumerate complete **all18 radius<=3** physical states and **six-halfturn radius<=5** states. This is not the old 62-cube specially selected cohort. Exact source baseline:

- 18 HTM whole-cube BFS shells at depths 0/1/2/3: **1,18,243,3240**, total **3,502 distinct original 54-sticker states**.
- Six legal halfturns H={U2,R2,F2,D2,L2,B2} BFS shells through depth 5: **1,6,27,120,519,1932**; within the 3,502 full-18 states, exactly **154** lie in the bounded H ball.
- Every halfturn rotates four corners as a product of **two disjoint transpositions** and preserves corner-permutation sign. Thus every state reachable from solved by any number of these six halfturns has **even corner permutation**. Within the complete full18 radius-three cohort, exactly **1,800 states have odd corner sign** and are rigorously **outside the entire unbounded H subgroup**.
- The other **1,548 even-corner states** not reached by at most five halfturns are **ONLY proven outside H depth<=5**, NOT proven outside the entire H subgroup. Sign parity is a necessary, not sufficient, condition for H membership.

Per-exact-full18-depth source-census [bounded H5 / even outside bounded H5 / odd certified outside unbounded H]: d0=(1/0/0), d1=(6/0/12), d2=(27/108/108), d3=(120/1440/1680). All data come from original 54-sticker geometry and source-independent controls; neither published human-authored moves nor private 451 records are recoded as simulated player behavior. Note that corner sign is an exact structural *negative gate*, not an all-purpose H-membership oracle.

P0 independent-implementation local audit is preliminary; **external CI PASS must not be stated until a completed read-only GitHub Actions job is explicitly inspected**. [Dedicated read-only CI](https://github.com/WhoSia/CUBE-REV/blob/469e9cf07a633a87da300ffa0fdbbccc7230fc89/.github/workflows/cuberev-024-P0-physical-halfturn-domain.yml). Node and Go derive legal facelet moves independently rather than sharing a fixture or code. The full3 geodesic path counts are checked using true 18-move predecessor relations. No global solve optimality beyond fixed radius is claimed.

## P1 — Whole-cube geodesic frontiers and exact admissible search architecture (PLANNED)

Construct genuine full18 geodesic predecessor DAGs, physical HTR/DR subgroup/coset crossing lower bounds, and counterfactual perturbations on source-independent held-out scrambles and earlier FMC authored branches. Distinguish proven exact distance, admissible lower bound, bounded horizon failure and unverified resource HOLD. Investigate whether subgroup-aware *negative* exclusion gates plus full18 bounds save expansions without ever discarding an admissible globally optimal path.

## P2 — Innovative solver policy versus honest baselines (PLANNED)

Design and independently benchmark an actual physical search policy (possibly bidirectional A*/IDA*, subgroup-aware PDB, symmetry quotient or exact resource-bounded two-sided branch pruning). Baselines must use the same scramble cohorts, physical move metric, implementation/hardware, stopping rules and output conditions. Require proof-carrying original full 54-sticker solutions for every claimed solve; a selective cohort or a small static lookup table is not a performance revolution.

## P3 — Human-authored FMC ecology as adversarial source evidence (PLANNED)

Reuse rights-cleared genuine written FMC candidate words, documented NISS direction / axis / phase, and original physical cube replay. The competitor's written retrospective analysis is a **text artifact**; never infer unobserved consideration order, visual attention or brain activity. Source algebra may be tested against machine-generated continuation but is never conflated with an observed human continuation. The 451 private records stay private. New participant recruitment, new video analysis or VFMC require separate rights and approval gates.

## P4 — Formal structural theorems, held-out falsification and independent implementation (PLANNED)

Use Lean 4 for actual algebraic invariants / soundness where tractable, and source-independent Rust/Go/C++/Node implementations for physical cube state replay and search. Prove the scope of pruning admissibility and its negative counterexamples. Record expanded unique full states, peak memory, runtime, legal HTM solution length and verifier result. An observation-model theorem or report-only milestone is not sufficient for scientific completion.

## Governance and historical invariants

Work on the existing research/current branch, never create a per-stage branch or alter public deployment main. Git author AND committer **WhoSia** only, and **zero** github-actions[bot] / github-action[bot] code contributions. Workflow permissions repository contents read only; no auto-write or commits. Every newly tracked source/path needs exact-path admission and real post-creation Git blob SHA in G7/P7; never auto-expanding globs. README is a concise research index; Notion is the canonical narrative with append-only inherited genealogy; Drive archived conversations are archaeology, NOT independently verified science. No history rewriting or erasure of failed CI diagnostics. Proven previous source/data-rights holds stay visible.

**Release gate:** researcher acceptance ACTIVATES this 0.24 scientific charter now. It does not magically complete P0; label P0 external verification pending until independent live CI evidence arrives. The next deliverable must be a scientific P1 solver experiment, not an administrative checklist.

**Historical P0 closed-execution retirement (2026-10-12):** original P0 Node/Go and its source-only CI are archived in [Drive custody](https://docs.google.com/document/d/1sr1K8Qx5ugDFSEni-1iAfJExdqYbP5m3QKc2OPmSt8o/edit). The references above intentionally point to immutable previous Git code, not current active paths. Verified P0 numerical conclusions remain cited. Active exact physical cube kernels and richer P0-R1/P1-R0/P1-R1 proof-grade source code are retained.

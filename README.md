# CUBE-REV — research/current

> Active research branch. Historical execution scaffolds are intentionally pruned from this branch.

CUBE-REV studies exact reversible state spaces, search/representation geometry, and naturalistic human planning evidence. **CUBE-REV 0.16 — Active Information Geometry, Belief-State Control & the Limits of Reversible Inference — is OPEN (2026-10-09)**; predecessor **0.15 is CLOSED**. The 0.15 length-15 two-error code decision remains separately OPEN mathematically and is not misreported as solved in 0.16. Prior 0.14 and 0.13 are CLOSED, with historical behavior evidence retained as development rather than fresh replication. Prior 0.11 and 0.12 are CLOSED as constructive mathematical and measurement-identification studies, **not** as positive human method-effect findings. Historical Generation/P numbering remains in Notion and provenance receipts; the early G7-P7 narrative below is historical, not current live research status.

## CUBE-REV 0.16 — OPEN active information geometry and belief control (2026-10-09)

- **[0.16 canonical Notion](https://app.notion.com/p/3f4ef561cf928161b4bfc5960f97ae8a)** — new version; P0 constitution presealed before the results. Research question: when do partial-state belief summaries preserve action-dependent predictions and future decision risks? Do not conflate counterfactual experiment equivalence with a realized observation trajectory.
- **P0 exact 24-state future refinement:** using the immutable 0.15 tracked-UR orientation-bit automaton (24 states, all 18 HTM moves), Moore observation/action partitions have **2 → 6 → 24 → 24** classes across horizons 0–3; discrete by horizon 2, stable confirmed at 3. All possible pair-separating action tests need at most 2 turns; **no single realized 2-turn state-recovery guarantee is claimed**.
- **P0 belief sufficiency obstruction:** among all **66** equally likely two-position beliefs with known initial orientation, entropy=1 bit and prior MAP=1/2 for every belief, yet optimal one-action, one-read exact-state recovery success is **1 for 48 beliefs and 1/2 for 18**. Example slots {0,2}: best 1/2; {1,3}: 1 after F. With explicitly hypothetical BSC(0.05), the latter contrast is 0.50 versus 0.95. Full posterior belief sufficiency remains standard POMDP theory, not a novel CUBE-REV theorem.
- **P0 Blackwell counterexample:** in the **same twelve known-flip0 inputs**, F- and B-quarter-turn binary experiments are **incomparable** for BSC error ε<1/2: pairs (0,1) and (0,3) furnish opposite identical-output-law obstructions to any state-independent garbling. Do not promote this conditional comparison into an unconditional full24 order or universal scalar geometry.
- **Code and source authority:** `scripts/cuberev-016/active-belief-geometry.mjs` and `scripts/cuberev-016/test-active-belief-geometry.mjs` reuse the 0.15 sticker-cubie-generated action maps, assert the original frozen P3D 24-codeword receipt and the new P0 counts, and are registered in the exact active-set allowlist and **read-only** CI. A separately implemented physical 12-slot Python action oracle reproduces the same finite results. No original human reconstruction rows are committed or relabeled as independent validation.
- **P1 complete 4,095-belief census:** restrict to each nonempty uniformly weighted subset of the **12 initially flip-zero UR-edge positions**, exact known actions, one ideal orientation reading after each move, and 0/1 initial-state recovery. Across all 4,095 subset beliefs, optimal two-move adaptive policy and best fixed two-move sequence had **exactly equal Bayes success**: **12** supports gave one terminal history, **708** gave two, and **3,375** gave three; **no four-leaf policy exists** in this contract. This is a finite model-specific structural theorem, **not** general non-utility of adaptive experiments.
- **P1 horizon-specific sufficient summary:** for the exact recovery *value* at horizon ≤2, `(|S|, which of F/B/neither 4-slot groups S touches)` has only **43 realized classes** and predicts every optimal value; it is not necessarily a recursively sufficient posterior or a complete policy identifier. For h2, leaf count is 1 for |S|=1, 3 when all three groups appear, otherwise 2. Each nonempty leaf contributes exactly 1/|S| to noiseless MAP accuracy under the stipulated uniform belief. Noiseless adaptivity cannot help at h2 because a first F/B quarter turn leaves the branch it flips homogeneous under every possible second orientation read; other first actions produce no initial distinction.
- **P1 hypothetical BSC, one read only:** for any nonempty uniform support S, at ε in [0,.5] the optimal one-action read success is `1/|S|` when S lies within a single face-incidence category and `2(1−ε)/|S|` otherwise. All 4,095 supports and ε=0/.05/.20/.50 independently enumerated; **do not transfer** the noiseless two-action nonadaptivity claim to ε>0 or horizons≥3. Public `scripts/cuberev-016/two-step-belief-census.mjs` and `test-two-step-belief-census.mjs` run within the same exact active-set allowlist and read-only test workflow.
- **P2 — internal 0.16 subsection, NOT a distinct formal title:** all 4,095 nonempty uniform initial-flip-zero UR-slot beliefs, all 18 legal HTM turns and horizon three with one ideal binary orientation read per turn. Exact backwards-induction feedback policy versus **all 18³=5,832 fixed triples**: adapt/fixed terminal-history counts **(1,1):12, (2,2):76, (3,3):509, (4,3):2, (4,4):3496**; **exactly two** strict adaptivity witnesses, 12-bit support masks **170={1,3,5,7}** and **3840={8,9,10,11}**, each at **100% adaptive versus 75% best fixed** original-slot identification. C++20, independently implemented Python and separate Node exact finite courts agree. All 5,832 fixed triples induce only 254 distinct unlabeled partitions of initial positions.
- **P2 decision-sufficient-summary obstruction:** P1's horizon≤2 43-class summary `(|S|, occupied F/B/other slot types)` ceases to preserve **horizon-three adaptive or fixed optimum**: **9 of 43** categories each have differing adaptive values and 9 have differing fixed values; explicit equal-summary sets `S={0,1,2,3}` versus `S={0,1,3,5}` have adaptive 3 versus4 leaves. This does not establish minimal full-belief representation at h3.
- **P2 hypothetical BSC robustness (NOT measured human/device error):** for the precommitted two witnesses, when each of three observations is independently flipped at assumed ε=.05, exact finite Bayes optimization gives **90.25% optimal adaptive versus 69.94375% best fixed**, a **20.30625 percentage point gap**. At ε=.50 both are 25%. Only four frozen supports and six epsilon values were evaluated under noisy sensing, not all 4,095 supports. Crucial output convention: internal flip indicator `f` has actual P0 sensor report `o=1−f`; illustrative branching policies must use the correct sensor labels.
- **P2 executable custody:** public `scripts/cuberev-016/three-read-feedback-census.mjs` and `test-three-read-feedback-census.mjs`, strictly read-only Actions workflow registration and active-set admission. Private finite-reproduction ZIP in Library `/CUBE-REV/0.16/CUBE_REV_016_P2_THREE_READ_ADAPTIVE_ADVANTAGE_PRIVATE_20261009.zip` SHA-256 `72678dadcb87f932d958582eb8c98c77d28570098f7f170373f40041af687128`; clean extracted ZIP CRC, file SHA, C++/Python/Node and noisy-policy quick verifier PASS. Original reco.nz human source bodies are excluded.
- **Research boundary:** partial identifiability in an ideal mathematical sensor is not human mental representation, human-vision calibration, full 3×3 solve recovery, or cryptographic security. Classical antecedents: Smallwood–Sondik (1973, doi:10.1287/opre.21.5.1071), Blackwell (1953, doi:10.1214/aoms/1177729032). P1 must test **decision-dependent posterior equivalence** rather than assert entropy is a complete controller state.

## CUBE-REV 0.15 — CLOSED finite observability, fiber geometry and robust codes (2026-10-09)

- [0.15 canonical Notion](https://app.notion.com/p/3f3ef561cf928151a50be8d6c8155289) — **CLOSED**, terminal §§55–56. Original scope: finite observation/action-dynamics refinements, action-equivariant hidden fibers, information-limited single-history recovery and exact model-relative noisy diagnosis. Mathematical closure does NOT settle human cognition, full 3×3 state recovery, or all optimization questions.
- [0.14 terminal Notion](https://app.notion.com/p/3f3ef561cf9281449bc0eee1a2636c24) — CLOSED. Exact P5 counterexample: solved e and U turn share Kociemba Phase-1 G1 coset, yet their six-Cross-goal 18-action mathematical likelihoods and synthetic information values differ. No full-channel function on that coset can reproduce both.
- [P5 verified private math-only bundle](https://drive.google.com/file/d/1TUzop1YQEJvMf0lTZHZAz0hVQ6v6_nX4/view) SHA-256 `b017a02264474559cc4bfa49cc7c34a265a0f209572726ff495b318cd7e3c47a` — 15 file entries, six exact 190080-state PDBs, independent sticker audits, Python reproduction and theorem statement.
- The one-step minimal channel-sufficient refinement is defined by (Phase-1 coset, reference-action-normalized 18-action distance-change vectors for every goal); a transition-sufficient representation requires further finite-state partition refinement. **Do not** conflate coset sets with normal-subgroup quotient groups, mathematical toy distinguishing games with cryptographic security, or annotation-prediction with human latent intention.
- No new independent behavioral cohort. Human-authored `WhoSia` commits, public math code/tests and read-only CI only; original source traces private.
- **0.15 P0 exact automata result:** on the complete, closed **190,080-state four-D-Cross-edge** abstract system, exact full-18-action future-distance observational partitions have **9→153,252→190,077→190,080** classes at horizons 0–3. Thus all possible three-action response tables distinguish every abstract state, while two-action tables leave exactly three unresolved pairs. C++20 and independent JavaScript transition/partition engines agree for all **3,421,440** transitions.
- **0.15 P1 one actual history is a weaker experiment:** conditional on initial exact distance 6, 97,254 states are possible and each next distance has only three values; hence every observation-adaptive single-history protocol needs **≥11 turns** to guarantee recovery. The frozen nonadaptive xorshift32 seed 2026100901 first distinguishes all 190,080 states after **42 turns**, separately certified in C++ and JavaScript. This is a bound, NOT an optimal 42-turn claim.
- **0.15 P2 decision theory:** under an explicitly hypothetical uniform state prior, the frozen word gives uniform-prior MAP success 94.716% after 20 turns, 99.999474% after 40 turns (still one unresolved pair), 100% after 42. Prior-dependent accuracy is not worst-case identification or human memory.
- **0.15 P3A verified:** exact first-response minimax over the 97,254 radius-six Q4 states yields worst surviving cell 62,752 (best among 18 first moves), greater than 3^10=59,049. Thus the adaptive recovery bound is now **12 ≤ L* ≤ 42** on the 190,080-state D-Cross abstract observer. Exact two-action size-minimax leaves 39,649; that does not prove 12 turns suffice. Independent full sticker e vs U has identical D-Cross abstract coordinate.
- **0.15 P3B verified finite lift:** track original four D-Cross edges plus UR only: **3,041,280** reachable five-edge states, exact HTM diameter **9**, all **54,743,040** directed transitions inverse/triangle/projection checked. Every Q4 state has **16** distinct Q5 lifts, action-equivariantly; a D-Cross-distance-only adaptive observer cannot distinguish these, with uniform-Q5 exact recovery success ≤1/16 for any horizon. This additional UR edge resolves e/U, but the eleven-face-turn word `F U' F U F U F U' F' U' F2` leaves all five edge coordinates fixed while changing U-Cross exact distance 0→5.
- **P3B archive:** `/CUBE-REV/0.15/CUBE_REV_0.15_P3B_FIVE_EDGE_FIBER_PRIVATE_20261009.zip` in personal Library, SHA-256 `f1305383c2441ee5ccf4aee252fc494cc520f97bec49d187e352633e33bdbd75`; exact 3,041,280-byte PDB SHA-256 `9eb33ddb8d5d929a361faf683a44564457513274c6b2016f54a1256494843a05`. C++ cleanroom + independent Python tests PASS; public Node fiber module/test in `scripts/cuberev-015/`. Google Drive direct P3B custody NOT verified (Library ref is not accepted by Drive connector).

- **P3C/P3D:** tracked UR edge ideal intrinsic flip-bit tomography (24 coordinate hypotheses across 495 hidden fibers); exact BSC/Bayes, robust risk and Blackwell comparisons are **model-conditional**. No actual human orientation sensor is measured.
- **P3E–P3H — global one-error optimum:** for fixed nonadaptive all-18 HTM action alphabet with one ideal intrinsic-flip bit before and after every move and up to one *arbitrarily* corrupted read, **t_opt^(1)=13 HTM actions / 14 reads**. Exhaustive computer-assisted impossibility for t≤12; independent 24-hypothesis certificate for `F' L2 B' F' R B F' D' R2 F' B' U2 B` (all 276 pair distances≥3 and 360 disjoint radius-one received strings).
- **P3I — two-error global interval:** for up to TWO arbitrarily corrupted reads, a complete three-range finite court proves **t_opt^(2)≥15** (no t≤14), while independent full24 verification certifies `B' F' R B U2 F' R B F' D B L2 F' D B F` (16 HTM actions, 17 reads, min distance5 and **3,696** disjoint radius-two received strings), hence **15≤t_opt^(2)≤16**.
- **P3J terminal — length15 STILL OPEN:** all **75,844,044** prefix8 transitions passed a complete new necessary-condition census over **254** three-future-read equality masks (from all 18³=5,832 action triples); 61,454,140 eliminated and 14,389,904 survive. A separately encoded SMT model calibrates SAT on known t16 but did **not** resolve t15. This necessary filter is **not** a global t15 UNSAT proof. Its rigorously bounded result closes P3J execution, **not** the outstanding mathematical question.
- **P3F evidence boundary:** 452 historical reco.nz source IDs contained one exact-content duplicate; analysis of **451 unique reconstructions / 25,723 exact prefix-state rows** concerns only naturalistic cube-state occupancy and hypothetical sensor-noise priors, not measured human perception or new independent replication. No new reco.nz body acquisition; rights/robots gate remains HOLD.
- **Private reproducibility:** Library `/CUBE-REV/0.15/` retains P3C–P3J source/certificates, including `CUBE_REV_015_P3H_EXACT_OPTIMUM13_PRIVATE_20261009.zip`, `CUBE_REV_015_P3I_TWO_BIT_OPTIMUM_BOUND_20261009.zip`, and `CUBE_REV_015_P3J_FINITE_FRONTIER_PRIVATE_20261009.zip` (SHA-256 `f38db2686d5e32993e8eb76beb192508f87c7b871bc74ca348260032bef5f467`). Quick P3J verifier PASS; five original separate range jobs COMPLETE; a later bundled full reexecution timed out and is **not** claimed PASS. Original source-level human reconstruction traces are privately held, never publicly relicensed.
- **Deferred after 0.15:** length15 two-error SAT/UNSAT; Q4 single-history minimax (currently **12≤L*≤42**, not exact); scaled full-group partition and rights-cleared human studies. These are explicitly OPEN as separate investigations; **do not reopen 0.15 or invent new prospective subjects by default**.

- [0.15 P0–P2 mathematical reproducibility bundle](https://app.notion.com/p/3f3ef561cf928151a50be8d6c8155289) — canonical 0.15 Notion, sections 8–13, exact full finite-state receipts and independent source code in the private Library `/CUBE-REV/0.15/`. Original human observations are not used in these finite-state proofs. The public executors are `scripts/cuberev-015/future-distance-refinement.mjs` and `scripts/cuberev-015/single-history-observability.mjs`, with read-only regression tests.


## Closed-version READMEs — archived without rewriting

The 0.11–0.14 sections formerly embedded here are preserved **verbatim** at their original historical dates, with original source blob `e8fb9dba0cde096ab219566429b2fa51916711d1`:

- [0.11 archived README](archive/versions/0.11/README_HISTORY.md) — prior naturalistic reconstruction and scope/evidence limits.
- [0.12 archived README](archive/versions/0.12/README_HISTORY.md) — state-conditioned opportunity; CLOSED.
- [0.13 archived README](archive/versions/0.13/README_HISTORY.md) — subgoal-conditioned geometry; CLOSED.
- [0.14 archived README](archive/versions/0.14/README_HISTORY.md) — Cross-goal/channel sufficiency counterexample; CLOSED.

The current research focus is **0.16**; **0.15 is CLOSED** and retains its math certificates and explicit open problems above. Source-level human reconstruction content remains PRIVATE. No executable historical source files were removed by this README documentation-only migration.

## Historical scientific spine

### reco.nz — naturalistic reconstruction spine
Current P7 treats reco.nz as the core naturalistic human-solve source.

Active authority:
- frozen 12,941-row index population;
- bounded body acquisition only;
- max 10 solve bodies per run;
- no de-facto bulk mirror by chaining unlimited runs;
- raw public redistribution remains HOLD;
- annotations are preserved as measurements, not treated as latent cognition.

Current P7 campaign:
- 40 prospectively frozen solve bodies;
- 4 batches × 10;
- campaign complete: **40/40 acquisition + 40/40 exact replay**;
- exact move-prefix states across P7 campaign: **2,149**;
- private batch artifacts are sealed in Drive custody;
- P4 predecessor body corpus: 20 solves;
- combined body-level naturalistic corpus available to current analysis: **60 solves**;
- this campaign is CLOSED to further source contact. Any additional reco.nz body acquisition requires new source authority or a new prospective constitution.

### exact cube / search geometry
The reusable exact authority is kept independently of its historical generation labels:

`crates/cuberev-core/`
`crates/search-geometry-core/`
`scripts/cube/`

The search core contains the exact 3×3 cubie representation, phase-1 geometry, projected PDBs, phase-2 support, and five-rival planning representations used by G7.

### active reconstruction core

`core/reco/`
- reco.nz bounded-acquisition policy
- reconstruction method ontology
- frozen sampling geometry

`scripts/reco/`
- reco.nz HTML parsing
- reconstruction move/annotation lexing

### current phase

`g7/p7/`
- P7 preseal
- reco.nz campaign constitution/manifest
- current Court criteria and source boundaries

`scripts/g7-p7/`
- current bounded campaign selection/acquisition/tests

`.github/workflows/`
- only workflows that may still execute in P7 or its immediate successor should remain here.

## Current inference boundary

P7 may compare:
- naturalistic reconstruction trajectories;
- exact cube states and five-rival search geometry;
- WCA official attempt/scramble context;
- future authorized prospective participant behavior.

It must not equate reconstruction annotations with internal cognitive states, reconstruction frequencies with WCA frequencies, or computational representations with human representations without behavioral evidence.

## Repository active-set policy

Files belong on `research/current` only if they are one of:

1. **ACTIVE_CORE** — reusable executable code/schema used by current or immediate-next work;
2. **ACTIVE_PHASE** — current P7 constitution, manifests, tests, and workflows;
3. **ACTIVE_DATA_AUTHORITY** — current source/linkage definitions that are still consumed.

Closed-phase workflows, one-off materializers, phase-specific closure tests, and superseded prose are removed from the active branch after their authority is preserved.

Historical bytes remain recoverable through:
- Git history;
- archive branch `archive/pre-p7-active-prune-20261002`;
- GitHub Actions artifacts;
- Google Drive scientific custody receipts.

Drive archive ledger:
**CUBE-REV — Repository Active-Set Archive Ledger**

Latest blocking active-set receipt:
- tracked files: **42**
- allowed files: **42**
- unexpected files: **0**
- missing required active files: **0**
- workflow run: `37004765344` — SUCCESS
- audit artifact: `11224744123`
- artifact SHA-256: `b12d426c9448d3571e17527042700422a3ca415d18150c7b7b00088ff4a45f9e`
- Drive audit custody: `1r8E2AhjFpEHOQutmSWQS51ulZXNdBDvX`

The machine-readable exact allowlist lives at `g7/p7/active-set-manifest.json`. The blocking audit fails if any unexpected file enters the branch **or if any required active file disappears**.

## Rust workspace

```text
crates/
├─ cuberev-core/
└─ search-geometry-core/
```

Validation:

```bash
cargo fmt --all --check
cargo check --workspace
cargo test --workspace
```

## Naming doctrine

Stage suffixes are operation-sensitive, not lineage defaults.

Use `Court` only when live alternatives, fixed adjudication criteria, binding verdicts, and downstream authority changes are all present. Otherwise prefer the actual operation: `Campaign`, `Census`, `Compiler`, `Materialization`, `Replication`, `Gate`, `Audit`, `Validation`, `Seal`, etc.

G7-P7 retains `Court` because it independently satisfies that qualification. Future phase names must classify the operation before choosing the suffix.


## Active-set v2 prune

The active branch is now governed by an **exact-path allowlist**, not broad directory prefixes.

Verified active set after the second P7 prune:
- tracked files: **42**
- unexpected files permitted: **0**
- required active files may be missing: **0**
- calibration/web/annotation/legacy-registry island: **archive-only**
- reusable 3x3 phase-1 kernel: `crates/search-geometry-core/src/phase1.rs`

Historical bytes remain available through Git history, the sealed archive branch, Actions artifacts, and the Drive archive ledger. New temporary/debug files must be explicitly admitted to the manifest or the blocking audit fails.

Latest P7 reco-derived authority after the prune:
- workflow run: `37004765361` — SUCCESS
- artifact: `11224783937`
- artifact SHA-256: `e475e4f964e581889212cbfaa200fe58a886e62235bbd2007f831e4ab86e71fa`
- Drive custody: `1Tf_HL5px2aNYXVfE97RfdrpRicn5TBbM`
- science pipeline reproduced unchanged after the core rename/prune.

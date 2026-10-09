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
- **Internal P3 — horizon / feedback finite census (verified; NOT a separate formal title):** all 4,095 uniform nonempty known-flip0 initial-position beliefs, all 18⁴=104,976 fixed words (1,913 exact partition types) and all feedback policies at h4: **1,331 supports** have adaptive 6-leaf vs fixed 5-leaf strict advantage, while the other 2,764 tie. Full histogram `(adaptive,fixed)=(1,1):12,(2,2):66,(3,3):223,(4,4):901,(5,5):1562,(6,5):1331`. Independently replicated by C++, Python+NumPy, and Node; the h3 advantage was restricted to two supports, so the feedback value frontier changes sharply with horizon.
- **Internal P3 — entire 18⁵ horizon-five word census:** full 12 original flip0 positions give adaptive/fixed **8/7** distinguishable transcripts; full 24 position+flip hypotheses (no gratuitous initial observation) give **12/10**. Original four-position h3 witnesses become **4/4 at h4**; unknown-flip eight-state versions become **8/8 at h4/h5**. Thus feedback advantage can appear, disappear, and reappear as horizon and prior geometry change. Independent C++ and vectorized NumPy enumerated **all 1,889,568 fixed length-five words**, without negative heuristic inference.
- **Internal P3 — exact action/read cost frontier:** for either frozen P2 four-state h3 witness, allow optional branch stopping to both fixed and adaptive policies, utility `MAP_accuracy − (motion_cost + read_cost) × expected_number_of_turn_read_pairs`. Full rational policy-line enumeration yields strict adaptive gain **max(0,¼ − motion_cost − read_cost)**; threshold **¼**, exact. With one mandatory read per action, individual motion and sensor costs are mathematically unidentifiable; a genuine sensor-only read needs a separately stated experiment.
- **Scientific originality caveat:** feedback sensing advantage per se predates CUBE-REV: Nitinawarat–Atia–Veeravalli (2013, DOI `10.1109/TAC.2013.2261188`) give multihypothesis open-loop/causal contrasts; Golovin–Krause (2011, DOI `10.1613/JAIR.3278`) give *conditional* adaptive-submodular results, not a theorem automatically applicable to this cube model. New candidate paper contribution is the **exact action-equivariant cube-constrained transition/cost/uncertainty frontier**, not a human cognitive fact.
- **Public mathematics:** `scripts/cuberev-016/horizon-feedback-court.mjs`, `cost-frontier.mjs` and regression tests are admitted in `g7/p7/active-set-manifest.json` and registered to a read-only Actions workflow. Independent Python/C++ physical-model audits and SHA-fixed private P3 archive are tracked in the 0.16 canonical Notion; do not label remote CI PASS without a checked run.
- **Internal P4 exact support law:** For any of all 4,095 nonempty known-flip0 uniform position supports S at four actions, the adaptive-policy advantage occurs **if and only if** S contains **at least two** original edge slots in **each** of F={1,5,8,9}, B={3,7,10,11}, and neither={0,2,4,6}. In that case adaptive/fixed terminal-leaf optimum is **6/5**, otherwise they tie. Exactly **216 minimal six-slot witnesses** form a monotone antichain, whose supersets number **(6+4+1)^3=1,331**. Stronger: the optimal adaptive and fixed VALUES are constant within each of the **124 possible nonzero three-category COUNT triples** (not an all-horizon posterior sufficient statistic). This finite iff, antichain and count-type value rule are verified for all 4,095 S by separate C++20, Python/NumPy and Node physical-action replay. Constructive sufficient direction follows from first F then B category reads and P0 two-step pair-separability; converse is currently *computer-assisted exhaustive proof*, not a human handwritten theorem.
- **P4 math-only source/custody:** `scripts/cuberev-016/structural-support-court.mjs` plus `test-structural-support-court.mjs` admitted into exact allowlist/read-only workflow; independent 17-file clean-extracted audit in private Library `/CUBE-REV/0.16/CUBE_REV_016_P4_EXACT_SUPPORT_ANTICHAIN_PRIVATE_20261009.zip`, SHA-256 `9548aa868276408f0176e80472b0c828cad3965de3968c2f5c00de69936e445f` (CRC, SHA receipts, C++/Python/Node clean PASS). Paper-scope critique and prior art: [0.16 research note](docs/0.16/RESEARCH_SCOPE.md). This is NOT a claim of human perception or new general controlled-sensing adaptivity.
- **Internal P5 compact rank theorem (proof + 36-word construction certificate):** at four legal HTM turns, for any nonempty uniform subset S of original known-flip0 tracked-UR locations, let `(f,b,n)` count candidates in F={1,5,8,9}, B={3,7,10,11}, other={0,2,4,6}. Define `T5={(0,2,3),(2,0,3),(1,2,2),(2,1,2),(2,2,1)}`. The optimum fixed history count is **5** if the count triple dominates a member of T5; otherwise **4** for |S|≥4 meeting at least two groups; otherwise **min(|S|,3)**. Feedback adds **exactly one additional distinct history iff f,b,n≥2**. Geometric handwritten upper bounds + **36 frozen HTM words** verified on only 220+492+480=**1,192** small source bases replace the previous all4095-support×104976-word proof dependence. This is a *small finite constructive certificate*, not yet an entirely calculation-free human lower-bound proof. The optimal value rank fails submodularity (Q={0,2,3,4}, add F positions1 and5: ranks 4,4,4,5), ruling out a naive matroid-rank argument. [Full scope and research comparison](docs/0.16/RESEARCH_SCOPE.md); canonical 0.16 Notion §21. Private P5 proof ZIP in Library `/CUBE-REV/0.16/` SHA256 `e6f15e58c65fe9ed350d72b9dbce099203434a1ef3a8fbd060e5f2c7deb04c78`. The full remote CI outcome remains unverified unless a run receipt says otherwise.
- **Internal P7 — exact reversible diagnosis vs reset (new pure-math):** with initially UNKNOWN full 24 physical tracked-edge coordinate and one ideal orientation bit read AFTER each selected 18-HTM action (no free time0 read), the global optimum feedback diagnosis length is **8 turns**: optimal distinguishable source counts by horizon 0..8 are `1,2,4,6,8,12,16,20,24`. To send EVERY possible tracked-edge source physically to one common target coordinate requires exactly **10 adaptive turns**: h≤9 impossible, h=10 attains it via a 24-source physically replayed decision tree. Each known current single-edge coordinate is correctable to the target in ≤3 actions; no single fixed word can map two distinct states to a common target because the action maps are bijections. **Neither 8 nor10 is a full-cube solving or measured-human-memory threshold.**
- **Internal P7 — forgotten scramble-path information:** of all **104,976** legal four-token HTM action words from one known initial tracked-edge coordinate, exactly **26,584** return this SAME tracked-edge coordinate. Given only this one edge's final full position+flip and known starting edge, reconstructing the exact *historical word* requires a separate worst-case fixed auxiliary log of at least **15 bits**. This is not a lower bound when full-cube information, retained moves or other observations are supplied; if the entire original word is known it can always be inverted immediately.
- **Internal P7 — universal four-turn catalogue improved:** the P5/P6 small-basis separating-word catalogue had rigorous `24≤M*≤34`; an exact new 60-base/168-candidate weighted-dual necessary-reduction with independent complete 144-state integer exact-cover court excludes 24 words, raising the model-relative machine-assisted bound to **`25≤M*≤34`**. Integer 25 feasibility is OPEN. [Complete mathematical scope](docs/0.16/REVERSIBILITY_OBSERVABILITY_THEOREM.md); 0.16 canonical Notion §§23–25, portable original-automaton proof package retained privately.
- **Research boundary:** partial identifiability in an ideal mathematical sensor is not human mental representation, human-vision calibration, full 3×3 solve recovery, or cryptographic security. Classical antecedents: Smallwood–Sondik (1973, doi:10.1287/opre.21.5.1071), Blackwell (1953, doi:10.1214/aoms/1177729032). P1 must test **decision-dependent posterior equivalence** rather than assert entropy is a complete controller state.

## CUBE-REV 0.15 — CLOSED (mathematical predecessor)

- [0.15 terminal canonical Notion](https://app.notion.com/p/3f3ef561cf928151a50be8d6c8155289) — P0–P3J complete as a research version. All inherited 0.15 claims must be read under their stated finite-state/ideal-sensor contracts; no human perceptual or cryptographic inference.
- **Exact 1-error optimum:** tracked UR ideal orientation-bit recovery `t_opt^(1)=13` HTM actions (14 binary observations). **2-error global interval:** `15≤t_opt^(2)≤16`; length15 existence remains OPEN as a distinct mathematical problem, despite 0.15 being CLOSED.
- **Permanent historical README:** [0.15 exact original source prose](archive/versions/0.15/README_HISTORY.md), preserved before archival with predecessor source blob `04a5e54fe4fa17fef066e40446d3b28392843d8e`. Complete proof/custody receipts remain on 0.15 Notion and in private Library `/CUBE-REV/0.15/`.

## Closed-version READMEs — archived without rewriting

The 0.11–0.14 sections formerly embedded here are preserved **verbatim** at their original historical dates, with original source blob `e8fb9dba0cde096ab219566429b2fa51916711d1`:

- [0.11 archived README](archive/versions/0.11/README_HISTORY.md) — prior naturalistic reconstruction and scope/evidence limits.
- [0.12 archived README](archive/versions/0.12/README_HISTORY.md) — state-conditioned opportunity; CLOSED.
- [0.13 archived README](archive/versions/0.13/README_HISTORY.md) — subgoal-conditioned geometry; CLOSED.
- [0.14 archived README](archive/versions/0.14/README_HISTORY.md) — Cross-goal/channel sufficiency counterexample; CLOSED.
- [0.15 archived README](archive/versions/0.15/README_HISTORY.md) — finite state/UR sensor exact math; CLOSED.
- [G7 archived README](archive/versions/G7/README_HISTORY.md) — earlier reco.nz campaign/source-rights inference boundary.

The current research focus is **0.16**; **0.15 is CLOSED** and retains its math certificates and explicit open problems above. Source-level human reconstruction content remains PRIVATE. No executable historical source files were removed by this README documentation-only migration.

## Historical G7 / reco.nz source authority (archived)

- [Exact historical G7-P7 README excerpts](archive/versions/G7/README_HISTORY.md) — previously embedded data acquisition/provenance and inference limits, preserved verbatim. The historical contacts and rights gates are **not** a newly authorized data collection program.
- Current source policy remains `core/reco/reco-acquisition-policy.json`: `BOUNDED_ONLY_PENDING_RIGHTS`, verify current robots/terms before any new acquisition, and **no raw public redistribution**. Past 451 semantic-unique reconstructions are DEVELOPMENT ONLY, not independent confirmation.

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

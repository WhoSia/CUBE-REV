# CUBE-REV — research/current

> **Active programme: CUBE-REV 0.19 — Physical Origins of Observational Reconstructibility: Rubik's Cube Transition Invariants, Observation-Partition Geometry & the Structural Limits of State Identification.** Earlier reports are scientific provenance, not a substitute for the current proof status. This README is a short entrypoint rather than a historical phase log.

CUBE-REV studies exact identification in physically constrained reversible systems and the boundaries of transferring ideal observation models to human cognition. The current exact mathematics uses a **real 3×3 Rubik's Cube-derived tracked-edge sensor**; it does **not** claim to determine complete cube state, human memory capacity, or optimal speedsolving / FMC moves.

## Canonical research authority

- [**0.19 Notion — active version, research programme and receipts**](https://app.notion.com/p/3f4ef561cf92813d9edfff4911db39d2).
- [0.19 mathematical horizon and collision-hypergraph theory](docs/0.19/P5_EXACT_OBSERVABILITY_HORIZONS_COLLISION_PAIRS_AND_ADAPTIVITY.md).
- [0.19 L5 geometric symmetry, fractional optimum, integer gap](docs/0.19/P3_GEOMETRIC_SYMMETRY_EXACT_LP_GAP_AND_K7_METHOD.md) and [conditional integer dual cuts](docs/0.19/P4_CONDITIONAL_INTEGER_DUALS_AND_K7_HIGHER_ORDER_CUTS.md).
- [**0.18 exact physical four-turn theorem**](https://github.com/WhoSia/CUBE-REV/actions/runs/37958523951) — independently accepted two-component DRUP proofs of `M*(4)=34`, plus [independently replayed physical 34-word upper](https://github.com/WhoSia/CUBE-REV/actions/runs/37948949764). The fixed 0.18 oracle is [here](scripts/cuberev-018/export-mstar-physical.mjs). Four-slot and five-slot reduced components are 64×88 (minimum 7) and 334×80 (minimum 27). This is a **fixed model theorem**, not a universal cognitive constant.
- [0.18 canonical historical Notion](https://app.notion.com/p/3f4ef561cf9281ef9bb6ca82f8c80d06). The formal version's administrative CLOSED marker has not been independently confirmed here; mathematical proof completion and lifecycle change are separate.
- [Historical full root README snapshot before 0.19 cleanup](archive/readme/README_RESEARCH_CURRENT_PRE_019_20261010.md), preserving **all** earlier 0.16/0.17/0.18 wording exactly. Those embedded historical pending claims are *superseded*, not active.
- [Drive archive — superseded 0.18 status paragraphs, verbatim Markdown](https://drive.google.com/file/d/1Ny5Jr0HNYFD1FcVda6kaEyoNbmhuDJC9/view), SHA-256 `7bcd81d51c849905699af25d615f1e066ee283494087c78443e0d8e58382589a`. Google Drive custody folder: `CUBE-REV/90_RESEARCH_CURRENT_ARCHIVE`.

## Fixed physical model and what M*(L) means

- The tracked **UR edge** initially occupies one of 12 edge slots with intrinsic orientation zero. Legal actions are the 18 outer-face half-turn-metric tokens; the actual transition maps come from the sticker-based cube implementation.
- One fixed, **nonadaptive** word of length `L` produces its ordered orientation-bit history, one reading after each action. The source family consists of the **same frozen 1,192 permitted 3-, 4-, and 5-slot subsets** at every horizon.
- A dictionary covers a known source subset `A` when **at least one** selected word has an injective observation history on `A`. `M*(L)` is the **minimum number of words in the dictionary**, not the number of turns of a cube solve. Every dictionary entry has unit cost even if action execution/read costs differ in the real world.
- An unknown source subset, adaptive policy, lossy memory, human vision, noisy sensor, unresettable cube or non-unit experimental costs each require a different problem contract.

### Observation-length frontier — original frozen source family

| Number of observations / HTM actions L | Smallest fixed experiment dictionary | Evidence / boundary |
|---|---:|---|
| 0–3 | impossible (infinity) | Analytic four-slot-cut and F/B confinement argument |
| 4 | **34, exact** | Physical double quotient + independently checked DRUP for both components |
| 5 | **8, exact under freshly re-executed local finite proof** | P13 complete source-locked t=0..7 integer/orbit courts plus independently replayed 8-word full-original witness; new external CI receipt not yet checked |
| 6 | **4, exact under locally checked exhaustive proof** | Collision-hypergraph complete finite k3 exclusion + physically replayed 4-word upper; **new CI receipt pending** |
| 7 | **3, exact under recorded local computation** | Two-word collision theorem plus exhaustive physical rank bound and three replayed words |
| 8 | **2, exact under recorded local computation** | Physical rank<12 lower plus two complementary collision-pair words |
| 9 and higher | **1, exact under recorded local computation** | Actual 9-turn word separates all twelve initial slots; 8-turn obstruction |

The `L=6,7,8,9` values have independent **local** physical replays and a separate GitHub Actions reproducibility workflow, but **a completed, independently checked GitHub CI receipt for that new workflow has not been confirmed**. The separate `L=4` exact DRUP chain *has* completed external proof checking. Do not collapse these evidence grades.

- Fixed-word universal 12-state identification: first possible length **9**.
- Observation-dependent adaptive full-12-state identification: computed worst-case minimum **7** in the ideal 24-state belief-system recurrence (local replay; not a human result).
- Standard fractional set-cover optimum at L5: **16/3 exactly** (rational primal/dual proof), whereas the **now-completely-proved original physical integer optimum is eight fixed five-HTM words** (P13). Fractional experiment weights are **not fractional cube turns**.

**P6→P7 update — physical restricted perfect hashing:** [P6 preparatory kernel](docs/0.19/P6_RESTRICTED_PERFECT_HASH_COLLISION_KERNEL_AND_L6_THREE_COURT.md) introduced source-independent collision dominance and honestly left M*(6) open. [P7](docs/0.19/P7_EXACT_MSTAR6_FOUR_COLLISION_HYPERGRAPH_PROOF.md) subsequently proved the omitted low-rank cases cannot appear in any three-word solution and finished all exact integer and symmetry cases. **The current local complete finite theorem is M*(6)=4; P6's older OPEN status is historical.**

## CUBE-REV 0.19 — complete exact physical horizon profile (local proof closure)

For the **frozen 1,192 original admitted source subsets** of twelve initially intrinsic-flip-zero UR-edge positions, legal physical 18 HTM face actions, one flip-orientation observation after each fixed action, known resettable source subset and unit experimental-dictionary cost, the exact profile is now:

`M*(0..3)=infinity; M*(4)=34; M*(5)=8; M*(6)=4; M*(7)=3; M*(8)=2; M*(L>=9)=1.`

**P13 last gap, (L=5):** [final original-full proof and scope](docs/0.19/P13_FINAL_EXACT_PHYSICAL_MSTAR5_EIGHT.md) rules out every seven-word dictionary via the number `t=0..7` of words with seven distinct initial orientation histories. For `t=0`: 65 original-source integer duals and 9 complete physical residual branches (5,082 search nodes); for `t=1,2,3`: 374 integer-weight certificates; for `t=4`: 2,361 independently re-executed and complete 16-symmetry orbits (359,004 original-physical residual attempts); for `t=5,6,7`: 12,717 five-word orbits, 906,192 six-word subsets and 3,365,856 seven-word subsets. The same independently replayed frozen 18×24 physical action maps verify eight real five-HTM word witnesses covering **all 1,192 original source subsets**. [Machine-readable local closure receipt](docs/0.19/P13_EXACT_MSTAR5_EIGHT_LOCAL_FINITE_RECEIPT.json) and [exact source/witness proof compiler](scripts/cuberev-019/compile-P13-original-full-exact-eight.py).

**Single consolidated external certification gate (manually dispatched only):** [0.19 P13 full physical exact-eight finite CI](.github/workflows/cuberev-019-p13-exact-eight-consolidated-manual.yml) independently regenerates the frozen original 1,192-source physical instance, rechecks P12 445 integer dual cases, checks the P13 65+9 rank-seven-zero cases and the 374 rank-seven-one-to-three cases, exhausts all 2,361 four-high orbit representatives in 14 nonoverlapping chunks, verifies the 5/6/7-high cases, and replays the real eight-word upper. **No automatic push trigger; do not infer PASS from the committed workflow.** The exact theorem is locally complete; administrative CI promotion awaits an actual successful run receipt.\n\n**Different evidence grades must not be conflated:** the L4 value 34 has externally completed independent DRUP proof checking. The L5 result 8 and L6/L7/L8 results come from locally complete original-physics finite proofs, with source SHA, independently checked integer certificates, symmetry-group scope and reconstructible positive witnesses; **fresh external GitHub Actions/Lean/VeriPB kernel acceptance of P13 is not yet verified**. A workflow commit or solver timeout is never an external mathematical receipt.

**Restricted-vs-full integer/source-extension result:** original five-state-only source subfamily `R5` (480 sets) has exact locally proved `M*_R5(5)=7` (P12). Extending to the full 1,192 admitted original source subsets increases the minimum to **8: a certified integer source-extension cost of one complete experiment**. The corresponding ordinary fractional LP increases from `185/39` to `16/3`, a difference `23/39`; full-instance integer/fractional gap ratio is **3/2**. These are finite model-specific properties, not a universal perfect-hash bound or fractional Rubik turn counts.

**Control/sensor separation:** one preset full-12-hypothesis observation experiment first identifies all twelve starts at length **9**, whereas ideal fully adaptive minimax identification has locally proved worst-case depth **7**. This does **not** measure human cognition or full-cube state identification.

**Proof history and custody:** [P12 restricted-seven proof](docs/0.19/P12_EXACT_PHYSICAL_FIVE_SOURCE_SEVEN_BY_RANK_CERTIFICATES.md); [P13 pre-closure seven-versus-eight court](docs/0.19/P13_FULL_1192_SOURCE_K7_LAST_INTEGER_DECISION.md); [verbatim archived root README before P13 closure](archive/readme/README_RESEARCH_CURRENT_BEFORE_P13_EXACT_EIGHT_20261010.md). Older OPEN/UNKNOWN labels remain as historical records, not current proof status. [Google Drive original physical proof package](https://drive.google.com/file/d/1jzxgLyNaLcYYJ1OoeQW-Qxev36Tp2KMD/view), package SHA-256 `c84e020b47348e3f8c60ca9b180c365789bf89f2e937b20c5c44145a6a93929d`. A separately recomputed [49-file complete P13 case-court package](https://drive.google.com/file/d/1gJhhHSViXOEoQy6fskH0YgKQGKYatDpk/view) has ZIP SHA-256 `22e4bdef544b73117174c7311078af1baaabf0987de227039b570462e51720a4` and the [long-form original-source proof](docs/0.19/P13_EXACT_FULL_MSTAR5_EIGHT_FINITE_PROOF_CLOSURE.md).

## Research questions following mathematical closure

1. **Independent P13 external certification:** rerun/verify exact source-locked t0..7 and eight-word physical witnesses in CI or a separate proof kernel; verify actual receipt rather than inferring success from committed workflows.
2. **Structural rather than instance-specific theorems:** derive physically transported binary sensor cut bounds, full restricted-perfect-hash extension laws and proof-carrying quotient conditions beyond one edge of one cube.
3. **Sharp instance mechanisms:** explain `34→8→4→3→2→1`, the L5 integer-vs-LP gap, the 480→1,192 source extension penalty, and preset-9 vs adaptive-7 under identical observability contracts.
4. **Optional external validity:** FMC/WCA/reconstruction videos and human annotations are auxiliary data; no such dataset proves the deterministic finite HTM edge-state theorem.

**New exact 0.20 baseline — source-family extension and integrality gap:** The identical physical L5 word family requires **7** experiments for the original 480 five-element sources and **8** for all original 1,192 sources. The source-extension **integer cost is 1**. Exact fractional optima are **185/39** and **16/3=208/39**, so fractional extension costs **23/39** and the additive integrality gap grows from **88/39** to **8/3=104/39**, an exact increase of **16/39**. The integer/LP ratios are **273/185** and **3/2**, respectively. These are model-specific finite theorems and a proposed 0.20 research starting point, **not** universal laws.\n\n## 0.20 proposed formal name — not administratively opened

[**CUBE-REV 0.20 — preparatory research charter**](docs/0.20/PREPARATORY_CHARTER_NOT_ACTIVATED.md):

**Structural Laws of Action-Transported Observation: Physically Restricted Perfect-Hash Families, Collision-Hypergraph Obstructions & Certified Identification Horizons**

Mathematical 0.19 is **locally closed**; preserve its exact frozen physical scope and secure independent external verification receipts before administratively closing 0.19 and activating 0.20. The proposed 0.20 programme must produce an actual new theorem under explicit hypotheses and adversarial counterexamples, not merely another large finite cube enumeration. The charter is a **proposal**, not an already established 0.20 result.

## Reproducibility entrypoints

| Purpose | File / workflow |
|---|---|
| Original physical 4-turn oracle | [export-mstar-physical.mjs](scripts/cuberev-018/export-mstar-physical.mjs) |
| All real 5-turn observation partitions | [export-L5-physical.mjs](scripts/cuberev-019/export-L5-physical.mjs) |
| Exact physical L5 k7/k6 SAT + conditional cuts | [prove-L5-k7-k6.py](scripts/cuberev-019/prove-L5-k7-k6.py) |
| L5 proof-producing CI | [cuberev-019-l5-exact-court.yml](.github/workflows/cuberev-019-l5-exact-court.yml) |
| L5 five-source k5 exact local impossibility | [P9 standalone Python checker](scripts/cuberev-019/prove-L5-five-source-k5-impossibility.py) · [P9 CI](.github/workflows/cuberev-019-l5-five-source-k5-court.yml) |
| L5 exact restricted R5 minimum seven | [P12 physical theorem](docs/0.19/P12_EXACT_PHYSICAL_FIVE_SOURCE_SEVEN_BY_RANK_CERTIFICATES.md) · [integer dual validator](scripts/cuberev-019/verify-L5-R5-k6-integer-duals.py) · [high-rank finite checker](scripts/cuberev-019/verify-L5-R5-k6-high-rank-finite.py) · [P12 CI](.github/workflows/cuberev-019-r5-exact-seven-finite-court.yml) |
| Completed original full M*(5)=8 | [P13 final theorem](docs/0.19/P13_FINAL_EXACT_PHYSICAL_MSTAR5_EIGHT.md) · [local exact receipt](docs/0.19/P13_EXACT_MSTAR5_EIGHT_LOCAL_FINITE_RECEIPT.json) · [source-bound compiler](scripts/cuberev-019/compile-P13-original-full-exact-eight.py) |
| Historical P10 R5 seven-word physical witness + k6 SAT court | [P10 independent physical verifier](scripts/cuberev-019/verify-L5-seven-five-source-and-extension.py) · [P10 six-word SAT/DRUP court](scripts/cuberev-019/prove-L5-five-source-k6-SAT.py) · [P10 CI](.github/workflows/cuberev-019-r5-k6-exact-court.yml) |
| L5 six-word R5 rank/69-orbit/pair verifier | [P11 physical integer court](scripts/cuberev-019/verify-L5-R5-rank-symmetry-and-pair-cuts.py) · [P11 theorem](docs/0.19/P11_R5_K6_HIGH_RANK_RIGIDITY_AND_DUAL_PAIR_CUTS.md) |
| L5 order-independent exact fractional court | [P8 verifier](scripts/cuberev-019/verify-L5-order-invariant-LP.py) · [P8 CI](.github/workflows/cuberev-019-l5-fractional-court.yml) |
| L7/L8 full physical rank courts | [L7.cpp](scripts/cuberev-019/prove-fixed-horizon-L7.cpp) · [L8.cpp](scripts/cuberev-019/prove-fixed-horizon-L8.cpp) |
| L6 exact 4 proof + source regenerators | [P7 proof](docs/0.19/P7_EXACT_MSTAR6_FOUR_COLLISION_HYPERGRAPH_PROOF.md) · [L6 finite verifier](scripts/cuberev-019/prove-L6-three-impossibility.py) · [L6 CI](.github/workflows/cuberev-019-l6-exact-court.yml) |
| L6–L9 actual source-dictionary replay | [verify-L6-to-L9-dictionaries.py](scripts/cuberev-019/verify-L6-to-L9-dictionaries.py) |
| Adaptive horizon / 9-turn witness | [verify-universal-and-adaptive-horizon.mjs](scripts/cuberev-019/verify-universal-and-adaptive-horizon.mjs) |
| Horizon reproducibility CI | [cuberev-019-horizon-theorems.yml](.github/workflows/cuberev-019-horizon-theorems.yml) |

## Historical archive, source boundaries and repository policy

Previous mathematics and behavior-method research (`0.11–0.18`, G7, reco.nz) is documented in the [verbatim pre-0.19 README](archive/readme/README_RESEARCH_CURRENT_PRE_019_20261010.md), [version-specific historical README archive](archive/versions/), Git history, research Notion and Drive custody ledgers. **None of those earlier statements of what was OPEN or PENDING should overwrite the current theorem receipt**.

Human reconstruction records are not public raw-data redistribution authority: current acquisition rights/robots/terms must be verified before expansion; older reco.nz campaigns are development material, not independent validation of ideal-state observations. Preserve data provenance and explicit authority constraints.

Repository active-set changes must be reviewed against `g7/p7/active-set-manifest.json` and applicable CI; old '42 allowed files' and historical workflow successes are **historical snapshots, not live checks**. Never assume a newly added `scripts/cuberev-019/` file is admitted to every legacy blocking allowlist merely because it is committed.

Rust workspace: `crates/cuberev-core` and `crates/search-geometry-core`. Validate with `cargo fmt --all --check`, `cargo check --workspace`, `cargo test --workspace`.

Naming: use `Court` only for a real adjudication with live alternatives, explicit criteria and downstream authority consequences; otherwise prefer `Census`, `Proof`, `Audit`, `Validation`, `Materialization` or `Replication`. Internal P-stage names never replace the formal 0.19 version title.

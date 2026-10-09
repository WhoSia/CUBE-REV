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
| 5 | **integer in [7,8]** | **P12: exact seven-word minimum for original 480 five-state subfamily (445 independently integer-checked duals + complete high-rank case exhaustion);** full original 1,192-source k=7 unresolved. New external CI receipt pending. |
| 6 | **4, exact under locally checked exhaustive proof** | Collision-hypergraph complete finite k3 exclusion + physically replayed 4-word upper; **new CI receipt pending** |
| 7 | **3, exact under recorded local computation** | Two-word collision theorem plus exhaustive physical rank bound and three replayed words |
| 8 | **2, exact under recorded local computation** | Physical rank<12 lower plus two complementary collision-pair words |
| 9 and higher | **1, exact under recorded local computation** | Actual 9-turn word separates all twelve initial slots; 8-turn obstruction |

The `L=6,7,8,9` values have independent **local** physical replays and a separate GitHub Actions reproducibility workflow, but **a completed, independently checked GitHub CI receipt for that new workflow has not been confirmed**. The separate `L=4` exact DRUP chain *has* completed external proof checking. Do not collapse these evidence grades.

- Fixed-word universal 12-state identification: first possible length **9**.
- Observation-dependent adaptive full-12-state identification: computed worst-case minimum **7** in the ideal 24-state belief-system recurrence (local replay; not a human result).
- Standard fractional set-cover optimum at L5: **16/3 exactly** (rational primal/dual proof), whereas the true binary dictionary size remains integer 6, 7 or 8. Fractional experiment weights are **not fractional cube turns**.

**P6→P7 update — physical restricted perfect hashing:** [P6 preparatory kernel](docs/0.19/P6_RESTRICTED_PERFECT_HASH_COLLISION_KERNEL_AND_L6_THREE_COURT.md) introduced source-independent collision dominance and honestly left M*(6) open. [P7](docs/0.19/P7_EXACT_MSTAR6_FOUR_COLLISION_HYPERGRAPH_PROOF.md) subsequently proved the omitted low-rank cases cannot appear in any three-word solution and finished all exact integer and symmetry cases. **The current local complete finite theorem is M*(6)=4; P6's older OPEN status is historical.**

## Current research authority — 0.19 P13

- **Exact restricted five-source theorem:** `M*_R5(5)=7` on the original 480 permitted five-position source requirements. [P12 complete locally independent integer finite proof](docs/0.19/P12_EXACT_PHYSICAL_FIVE_SOURCE_SEVEN_BY_RANK_CERTIFICATES.md); [source-regenerating P12 Actions](.github/workflows/cuberev-019-r5-exact-seven-finite-court.yml). The new external CI PASS receipt is **not independently confirmed**.
- **Single unresolved full-original integer:** `M*(5) in {7,8}` for the **same frozen 1,192 original source sets**. Lower 7 is a rigorous consequence of the restricted R5 theorem; upper 8 is the previously independently replayed eight-real-word physical dictionary. [P13 exact decision and structural theorem](docs/0.19/P13_FULL_1192_SOURCE_K7_LAST_INTEGER_DECISION.md).
- **Physical k7 necessary conditions:** Every selected word must distinguish at least five initial hypotheses and have a *private admitted five-source witness*. At least **two** of the seven words must distinguish at least six initial positions (1,144 exact source-volume exclusions and 32 original-row integer dual certificates). The physical k7 core has **544 × 2,403** incidence; the 16 verified signed-coordinate **incidence** automorphisms permit **69 high-rank first-word orbit representatives**, preserving all 2,403 binary choices. The original source dual yields exactly **102,979** valid low-weight pair exclusions.
- **New rank-seven class courts:** All rank-seven-only seven-word combinations fail the restricted 480-source requirements; no full seven-word cover can contain **six** rank-seven words plus one rank-five/six word; and the five-rank-seven/two-lower case is excluded via **12,717** symmetry representatives and all physically realized original-rank lower words. The exactly-four-rank-seven branch is undergoing an additional strict duplicate-safe verification. These rank-class courts are **not** a full k7 negative proof.
- **Current honest decision status:** full original k7 physical SAT/UNSAT remains **UNKNOWN**. A 150-second HiGHS integer search and 110-second local heuristic search did not find a complete seven-word cover, but neither produces an impossibility certificate. The seven-word heuristic's best original coverage missed **four** requirements. [Independent P13 SAT/DRUP workflow](.github/workflows/cuberev-019-p13-full-k7-physical-proof.yml) is authored but successful runtime/UNSAT proof receipt **not yet independently confirmed**.
- **Previous proof stages:** [P8 exact fractional source geometry](docs/0.19/P8_ORDER_INVARIANT_FRACTIONAL_COST_AND_K6_DUAL_PAIR_COURT.md), [P9 physical R5 k5 impossibility](docs/0.19/P9_EXACT_FIVE_SOURCE_K5_UNSAT_AND_FULL_K6_RANK_GATE.md), [P10 seven restricted words and failed one-word extension](docs/0.19/P10_SEVEN_SOURCE_WITNESS_EXTENSION_OBSTRUCTION_AND_R5_K6_COURT.md), [P11 conditional rank rigidity](docs/0.19/P11_R5_K6_HIGH_RANK_RIGIDITY_AND_DUAL_PAIR_CUTS.md). Historical ROOT wording is preserved [verbatim before P13](archive/readme/README_RESEARCH_CURRENT_PRE_P13_20261010.md); the older P8–P11 research-stages are **superseded as decisions**, not erased from the record.

## Mathematical questions still active

1. **Finish 0.19 at L=5:** exhibit **seven actual 5-HTM words** covering all original 1,192 source subsets, or independently check a genuine full `k<=7` UNSAT proof for the exact source-locked CNF after auditing all physical, symmetry, rank and integer-dual reductions. Either outcome makes `M*(5)` exact; solver timeout remains UNKNOWN.
2. **Explain the structural horizon profile:** `M*(4)=34` independently DRUP-checked, `M*(6)=4` and `M*(7)=3`, `M*(8)=2`, `M*(L>=9)=1` under locally checked finite physical proofs. Distinguish preset universal identification horizon 9 from adaptive minimax 7 under the same *ideal* sensor.
3. **Understand source extension and integer obstructions:** Original full fractional LP `16/3`, restricted R5 fractional LP `185/39`, exact fractional source-family extension cost `23/39`. Neither fraction is an executable number of physical turns or dictionary words.
4. **Keep empirical transfer separate:** FMC/WCA/reconstruction video data are optional auxiliary validation material. The frozen orientation-bit oracle and source-family contract do not directly describe human memory, solving times, or full-cube reconstruction.

## Proposed next version, not yet activated

[**0.20 — preparatory mathematical charter**](docs/0.20/PREPARATORY_CHARTER_NOT_ACTIVATED.md): `Laws of Physically Constrained Identification: Restricted Perfect Hash Families, Action-Transported Observation Codes & Certified Covering Complexity`. **DO NOT OPEN 0.20** until original full-source `M*(5)` is solved with a physical seven-word positive proof or independently checked seven-word negative proof, and 0.19 evidence/limitations are sealed. This is a research proposal, not an achieved 0.20 theorem.

A numerical time limit is **UNKNOWN**, never UNSAT. A new proof-producing workflow commit is **not** an externally completed CI receipt.

## Reproducibility entrypoints

| Purpose | File / workflow |
|---|---|
| Original physical 4-turn oracle | [export-mstar-physical.mjs](scripts/cuberev-018/export-mstar-physical.mjs) |
| All real 5-turn observation partitions | [export-L5-physical.mjs](scripts/cuberev-019/export-L5-physical.mjs) |
| Exact physical L5 k7/k6 SAT + conditional cuts | [prove-L5-k7-k6.py](scripts/cuberev-019/prove-L5-k7-k6.py) |
| L5 proof-producing CI | [cuberev-019-l5-exact-court.yml](.github/workflows/cuberev-019-l5-exact-court.yml) |
| L5 five-source k5 exact local impossibility | [P9 standalone Python checker](scripts/cuberev-019/prove-L5-five-source-k5-impossibility.py) · [P9 CI](.github/workflows/cuberev-019-l5-five-source-k5-court.yml) |
| L5 exact restricted R5 minimum seven | [P12 physical theorem](docs/0.19/P12_EXACT_PHYSICAL_FIVE_SOURCE_SEVEN_BY_RANK_CERTIFICATES.md) · [integer dual validator](scripts/cuberev-019/verify-L5-R5-k6-integer-duals.py) · [high-rank finite checker](scripts/cuberev-019/verify-L5-R5-k6-high-rank-finite.py) · [P12 CI](.github/workflows/cuberev-019-r5-exact-seven-finite-court.yml) |
| Last original k7 decision | [P13 theorem](docs/0.19/P13_FULL_1192_SOURCE_K7_LAST_INTEGER_DECISION.md) · [no-solver 544×2403 builder](scripts/cuberev-019/prepare-L5-full-k7-physical-CNF.py) · [P13 Glucose4/DRUP court](scripts/cuberev-019/solve-L5-full-k7-physical-SAT.py) · [P13 gated CI](.github/workflows/cuberev-019-p13-full-k7-physical-proof.yml) |
| Historical P10 R5 seven-word physical witness + k6 SAT court | [P10 independent physical verifier](scripts/cuberev-019/verify-L5-seven-five-source-and-extension.py) · [P10 six-word SAT/DRUP court](scripts/cuberev-019/prove-L5-five-source-k6-SAT.py) · [P10 CI](.github/workflows/cuberev-019-r5-k6-exact-court.yml) |
| L5 six-word R5 rank/69-orbit/pair verifier | [P11 physical integer court](scripts/cuberev-019/verify-L5-R5-rank-symmetry-and-pair-cuts.py) · [P11 theorem](docs/0.19/P11_R5_K6_HIGH_RANK_RIGIDITY_AND_DUAL_PAIR_CUTS.md) |
| L5 order-independent exact fractional court | [P8 verifier](scripts/cuberev-019/verify-L5-order-invariant-LP.py) · [P8 CI](.github/workflows/cuberev-019-l5-fractional-court.yml) |
| L7/L8 full physical rank courts | [L7.cpp](scripts/cuberev-019/prove-fixed-horizon-L7.cpp) · [L8.cpp](scripts/cuberev-019/prove-fixed-horizon-L8.cpp) |
| L6 exact 4 proof + source regenerators | [P7 proof](docs/0.19/P7_EXACT_MSTAR6_FOUR_COLLISION_HYPERGRAPH_PROOF.md) · [L6 finite verifier](scripts/cuberev-019/prove-L6-three-impossibility.py) · [L6 CI](.github/workflows/cuberev-019-l6-exact-court.yml) |\n| L6–L9 actual source-dictionary replay | [verify-L6-to-L9-dictionaries.py](scripts/cuberev-019/verify-L6-to-L9-dictionaries.py) |
| Adaptive horizon / 9-turn witness | [verify-universal-and-adaptive-horizon.mjs](scripts/cuberev-019/verify-universal-and-adaptive-horizon.mjs) |
| Horizon reproducibility CI | [cuberev-019-horizon-theorems.yml](.github/workflows/cuberev-019-horizon-theorems.yml) |

## Historical archive, source boundaries and repository policy

Previous mathematics and behavior-method research (`0.11–0.18`, G7, reco.nz) is documented in the [verbatim pre-0.19 README](archive/readme/README_RESEARCH_CURRENT_PRE_019_20261010.md), [version-specific historical README archive](archive/versions/), Git history, research Notion and Drive custody ledgers. **None of those earlier statements of what was OPEN or PENDING should overwrite the current theorem receipt**.

Human reconstruction records are not public raw-data redistribution authority: current acquisition rights/robots/terms must be verified before expansion; older reco.nz campaigns are development material, not independent validation of ideal-state observations. Preserve data provenance and explicit authority constraints.

Repository active-set changes must be reviewed against `g7/p7/active-set-manifest.json` and applicable CI; old '42 allowed files' and historical workflow successes are **historical snapshots, not live checks**. Never assume a newly added `scripts/cuberev-019/` file is admitted to every legacy blocking allowlist merely because it is committed.

Rust workspace: `crates/cuberev-core` and `crates/search-geometry-core`. Validate with `cargo fmt --all --check`, `cargo check --workspace`, `cargo test --workspace`.

Naming: use `Court` only for a real adjudication with live alternatives, explicit criteria and downstream authority consequences; otherwise prefer `Census`, `Proof`, `Audit`, `Validation`, `Materialization` or `Replication`. Internal P-stage names never replace the formal 0.19 version title.

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
| 5 | **integer in [6,8]** | Physical eight-word cover + exact integer lower; **k=7 unresolved** |
| 6 | **4, exact under locally checked exhaustive proof** | Collision-hypergraph complete finite k3 exclusion + physically replayed 4-word upper; **new CI receipt pending** |
| 7 | **3, exact under recorded local computation** | Two-word collision theorem plus exhaustive physical rank bound and three replayed words |
| 8 | **2, exact under recorded local computation** | Physical rank<12 lower plus two complementary collision-pair words |
| 9 and higher | **1, exact under recorded local computation** | Actual 9-turn word separates all twelve initial slots; 8-turn obstruction |

The `L=6,7,8,9` values have independent **local** physical replays and a separate GitHub Actions reproducibility workflow, but **a completed, independently checked GitHub CI receipt for that new workflow has not been confirmed**. The separate `L=4` exact DRUP chain *has* completed external proof checking. Do not collapse these evidence grades.

- Fixed-word universal 12-state identification: first possible length **9**.
- Observation-dependent adaptive full-12-state identification: computed worst-case minimum **7** in the ideal 24-state belief-system recurrence (local replay; not a human result).
- Standard fractional set-cover optimum at L5: **16/3 exactly** (rational primal/dual proof), whereas the true binary dictionary size remains integer 6, 7 or 8. Fractional experiment weights are **not fractional cube turns**.

**P6→P7 update — physical restricted perfect hashing:** [P6 preparatory kernel](docs/0.19/P6_RESTRICTED_PERFECT_HASH_COLLISION_KERNEL_AND_L6_THREE_COURT.md) introduced source-independent collision dominance and honestly left M*(6) open. [P7](docs/0.19/P7_EXACT_MSTAR6_FOUR_COLLISION_HYPERGRAPH_PROOF.md) subsequently proved the omitted low-rank cases cannot appear in any three-word solution and finished all exact integer and symmetry cases. **The current local complete finite theorem is M*(6)=4; P6's older OPEN status is historical.**

**P8 — five-turn integer obstruction and exact source-specific fractional geometry:** [P8 theorem and proof protocol](docs/0.19/P8_ORDER_INVARIANT_FRACTIONAL_COST_AND_K6_DUAL_PAIR_COURT.md) proves, with **enumeration-order-invariant 1,192-bit physical coverage identities**, the full-source fractional LP optimum **16/3**, the five-source-only LP optimum **185/39**, and the exact incremental fractional cost **23/39** of the 64 mixed four-source requirements. The local independent verifier checks all 14,446 physical coverage types with exact rational arithmetic; [standalone P8 read-only CI](.github/workflows/cuberev-019-l5-fractional-court.yml) is authored but its external completed-run receipt is **not yet confirmed**. A six-word full dictionary must avoid **1,010** inadmissibly low-dual columns and **1,194,707** low-union column pairs among 1,877 eligible columns; these sound SAT cuts do **not** prove k6 UNSAT. The 480-five-source k5 subproblem is numerical HiGHS INFEASIBLE only, not independently proof-checked.

**P9 — exact five-state k5 exclusion:** [P9 complete finite proof](docs/0.19/P9_EXACT_FIVE_SOURCE_K5_UNSAT_AND_FULL_K6_RANK_GATE.md) now excludes any five physically realizable L5 words covering the 480 original five-position sources. Its source-locked standalone Python checker physically replays 14,938 partitions, reduces 3,344 original five-source coverage types to 2,023 undominated types, then uses exact dual weights and finite branching on just 396 eligible words (61,098 forbidden pairs; complete tree 1/50/163 nodes). This is a **locally complete computer-assisted impossibility proof**, not a claim of external CI PASS. Consequently any hypothetical full-source k6 dictionary uses six rank>=5 words: together with original full-source dual cuts, only **1,724 of 2,887** reduced words remain eligible, with **947,894** exact pair exclusions. The full k6 and k7 integer existence decisions are **still OPEN**. [P9 read-only CI](.github/workflows/cuberev-019-l5-five-source-k5-court.yml) and [standalone checker](scripts/cuberev-019/prove-L5-five-source-k5-impossibility.py). [P9 complete source-locked Drive evidence](https://drive.google.com/file/d/1F2C_yLs3szW8Ucro2Rnbr2hFYa0CJ3CV/view).

## Current active mathematical questions

1. **L6 complete finite theorem:** [P7 full proof](docs/0.19/P7_EXACT_MSTAR6_FOUR_COLLISION_HYPERGRAPH_PROOF.md) uses original physical source regeneration, a rank-gate excluding two-word coverage of all five-state demands, collision-edge inclusion dominance (53,528→18,813), a certified 172-row integer dual, 16 exact incidence symmetries and 19,110+297,872 exhaustive branch checks to prove **M*(6)=4**. The [read-only CI pipeline](.github/workflows/cuberev-019-l6-exact-court.yml) is written but its completed independent run is **not yet verified**.
2. **L5 exact 6/7/8 after P9 five-source k5 exclusion:** 1,889,568 physical 5-HTM words, 14,938 partitions, 544×2,887 exact all-k row/column quotient; 16 physical-incidence automorphisms yield 196 candidate first-column orbits; regular LP relaxation is exactly 16/3. The k6 conditional dual court excludes 191/196 first-word orbits; k7 has exact dual-derived 247,348 forbidden word pairs, while k6 has 1,194,707 separately verified low-union forbidden pairs and 1,010 sound singleton exclusions, **not** a proof of k7 UNSAT.
3. **Structure over the entire horizon:** transported four-slot flip cuts, F/B-only confinement, collision-pair geometry, observation refinement versus core size, feedback-versus-preset separation, integer covering gap and physical coordinate symmetry.
4. **Ontology transfer:** the ideal orientation-bit oracle is not a human perceptual protocol. FMC, WCA speed events, reco.nz reconstructions and video-coded actions may become *auxiliary* sources, not prerequisites for the current exact mathematics.

A time budget expiring is **UNKNOWN**, not UNSAT. Promote an exact negative result only with a proof trace validated against its actual CNF and with independent verification of any symmetry or weighted-cover cuts added to the CNF.

## Reproducibility entrypoints

| Purpose | File / workflow |
|---|---|
| Original physical 4-turn oracle | [export-mstar-physical.mjs](scripts/cuberev-018/export-mstar-physical.mjs) |
| All real 5-turn observation partitions | [export-L5-physical.mjs](scripts/cuberev-019/export-L5-physical.mjs) |
| Exact physical L5 k7/k6 SAT + conditional cuts | [prove-L5-k7-k6.py](scripts/cuberev-019/prove-L5-k7-k6.py) |
| L5 proof-producing CI | [cuberev-019-l5-exact-court.yml](.github/workflows/cuberev-019-l5-exact-court.yml) |
| L5 five-source k5 exact local impossibility | [P9 standalone Python checker](scripts/cuberev-019/prove-L5-five-source-k5-impossibility.py) · [P9 CI](.github/workflows/cuberev-019-l5-five-source-k5-court.yml) |
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

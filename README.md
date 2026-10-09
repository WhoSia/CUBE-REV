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
| 6 | **integer in [3,4]** | Actual four-word cover; **three-word feasibility unresolved** |
| 7 | **3, exact under recorded local computation** | Two-word collision theorem plus exhaustive physical rank bound and three replayed words |
| 8 | **2, exact under recorded local computation** | Physical rank<12 lower plus two complementary collision-pair words |
| 9 and higher | **1, exact under recorded local computation** | Actual 9-turn word separates all twelve initial slots; 8-turn obstruction |

The `L=7,8,9` values have independent **local** physical replays and a separate GitHub Actions reproducibility workflow, but **a completed, independently checked GitHub CI receipt for that new workflow has not been confirmed**. The separate `L=4` exact DRUP chain *has* completed external proof checking. Do not collapse these evidence grades.

- Fixed-word universal 12-state identification: first possible length **9**.
- Observation-dependent adaptive full-12-state identification: computed worst-case minimum **7** in the ideal 24-state belief-system recurrence (local replay; not a human result).
- Standard fractional set-cover optimum at L5: **16/3 exactly** (rational primal/dual proof), whereas the true binary dictionary size remains integer 6, 7 or 8. Fractional experiment weights are **not fractional cube turns**.

## Current active mathematical questions

1. **L6 three-versus-four:** model each word by the graph of pairs of starting positions that its complete output history fails to distinguish. For selected words `w_1,...,w_k`, the dictionary fails iff their collision graphs admit one edge each whose union fits in one permitted source set. This exact **collision-hypergraph criterion** exposes higher-order obstructions while retaining the original problem.
2. **L5 exact 6/7/8:** 1,889,568 physical 5-HTM words, 14,938 partitions, 544×2,887 exact all-k row/column quotient; 16 physical-incidence automorphisms yield 196 candidate first-column orbits; regular LP relaxation is exactly 16/3. The k6 conditional dual court excludes 191/196 first-word orbits; k7 has exact dual-derived 247,348 forbidden word pairs, **not** a proof of k7 UNSAT.
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
| L7/L8 full physical rank courts | [L7.cpp](scripts/cuberev-019/prove-fixed-horizon-L7.cpp) · [L8.cpp](scripts/cuberev-019/prove-fixed-horizon-L8.cpp) |
| L6–L9 actual source-dictionary replay | [verify-L6-to-L9-dictionaries.py](scripts/cuberev-019/verify-L6-to-L9-dictionaries.py) |
| Adaptive horizon / 9-turn witness | [verify-universal-and-adaptive-horizon.mjs](scripts/cuberev-019/verify-universal-and-adaptive-horizon.mjs) |
| Horizon reproducibility CI | [cuberev-019-horizon-theorems.yml](.github/workflows/cuberev-019-horizon-theorems.yml) |

## Historical archive, source boundaries and repository policy

Previous mathematics and behavior-method research (`0.11–0.18`, G7, reco.nz) is documented in the [verbatim pre-0.19 README](archive/readme/README_RESEARCH_CURRENT_PRE_019_20261010.md), [version-specific historical README archive](archive/versions/), Git history, research Notion and Drive custody ledgers. **None of those earlier statements of what was OPEN or PENDING should overwrite the current theorem receipt**.

Human reconstruction records are not public raw-data redistribution authority: current acquisition rights/robots/terms must be verified before expansion; older reco.nz campaigns are development material, not independent validation of ideal-state observations. Preserve data provenance and explicit authority constraints.

Repository active-set changes must be reviewed against `g7/p7/active-set-manifest.json` and applicable CI; old '42 allowed files' and historical workflow successes are **historical snapshots, not live checks**. Never assume a newly added `scripts/cuberev-019/` file is admitted to every legacy blocking allowlist merely because it is committed.

Rust workspace: `crates/cuberev-core` and `crates/search-geometry-core`. Validate with `cargo fmt --all --check`, `cargo check --workspace`, `cargo test --workspace`.

Naming: use `Court` only for a real adjudication with live alternatives, explicit criteria and downstream authority consequences; otherwise prefer `Census`, `Proof`, `Audit`, `Validation`, `Materialization` or `Replication`. Internal P-stage names never replace the formal 0.19 version title.

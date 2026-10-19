# CUBE-REV 0.27 — P10: Genuine External Optimal-18 Candidate, Independent Physical Replay and T2 Custody

## Scientific disposition (2026-10-19)
**NEW SOLVER-BACKED EXACT-18 RESULT**, not yet a stand-alone proof-carrying independently audited no-17 certificate. We verified the underlying GitHub job [#39192428399](https://github.com/WhoSia/CUBE-REV/actions/runs/39192428399) directly: `completed/success`, manual `workflow_dispatch`, existing `research/current`, evaluated commit `8383a2da8de3b168ebb317fd4f532ac73c38698d`, job ID `117867938199`. PyPy selftest PASS, exact pip install `RubikOptimal==1.1.0` PASS, full optimal invocation PASS, physical candidate verifier PASS, and raw ZIP artifact upload PASS.

**Original fixed WCA scramble (20 HTM):** `R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2`

**FRESH independent solver candidate (18 HTM):** `U' D' R2 F' D2 B' R F2 B U2 L2 U F U L U' F2 B2`

**Frozen earlier independent 18 HTM:** `F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2`

External solver literal: `U3 D3 R2 F3 D2 B3 R1 F2 B1 U2 L2 U1 F1 U1 L1 U3 F2 B2 (18f*)`. This third-party notation explicitly CLAIMS that length18 is optimal; this is not proof that the pruning algorithm is sound. It is a genuinely different solution from earlier, physically correct by both the external independent P9 Python original 54-site replay and a freshly compiled **actual original P11 native C++ P[18][54]** replay using 54 independent original sticker labels. The native replay additionally checked both solutions, 18 inverses and that the last candidate move is essential.

### Authentic iterative-deepening log and scope
| Iterative depth | generated nodes | solver search time (s) |
|---:|---:|---:|
| 14 | 160,140 | 0.15 |
| 15 | 2,116,713 | 0.93 |
| 16 | 27,618,042 | 10.81 |
| 17 | 360,731,937 | 140.08 |
| 18 | 690,564,941 | 279.50 |

Additional earlier depth counts (0–13 collectively): 12,930. The exact recorded total is **1,081,204,703 generated**, **431.52 seconds inside solver.search**. Depth17 exhausts only the solver's canonically reduced, projected-and-pruned nodes; depth18 ends when it finds one solution (NOT a completely exhausted depth18 forest). Initial large pruning-table generation is additional overhead, not included in the 431.52 second solver time.

### Source-level preliminary correctness review — NON-FORMAL
The published upstream `package_src/optimal/solver.py` (GitHub master read during this audit; not pinned binary hash of installed PyPI wheel) calls `search(...,togo)` with increasing target lengths. Pruning includes:
1. skipping same-face adjacent turns and one ordering of commuting opposite-face turns;
2. exact corner-distance lower bounds;
3. modulo-three distances to three rotated phase1x24 subgroups, with `pr.distance` reconstruction;
4. a further shortcut if all three nonzero subgroup distances are equal: `UD_dist1 + 1 >= togo`.

These are potential mathematical proof obligations. The first has standard HTM normalization. The other rules require verified coordinate tables and an admissibility derivation, especially the equal-three-axis extra step and the mod-three tables. The third-party result alone does not provide portable independently checked no-17 receipts, formally complete pruning certificates, or an exact installed wheel file SHA. DO NOT infer an independently certified exact-18 theorem solely from an `(18f*)` annotation or GitHub SUCCESS.

### Raw output evidence, original-byte T2 verification
Actions artifact ID `12160697402`, named `p9-independent-optimal-solver-execution`. Actually downloaded original ZIP **1,162 bytes SHA256 `be04cabe290432359410cf33372af351d8facd9761428ae09b34ce77a1b90cff`**, CRC PASS; its member `P9_EXTERNAL_OPTIMAL_PROBE_RAW.log` is **4,033 bytes SHA256 `de469b8558afbc9c9b43c4434dfc57aa581a0b535a489f3210398bcb72ea0e68`**. The exact Actions ZIP was uploaded into the existing Drive `10_CANONICAL_PROOF_COURTS` as [CUBEREV_027_P9_EXTERNAL_OPTIMAL_RUN39192428399_RAW.zip](https://drive.google.com/file/d/1WP1Vgd5J3lSgwZ7Mq4gyqy5atK7FzCfW/view), then actually downloaded afresh and SHA checked: **identical 1,162 raw bytes, BYTE_VERIFIED T2**. This ZIP is different from earlier #39087089460 lower17 proof and from P9 local two-subcourt original evidence, which are separately archived.

### Correct claim tiers
- **PROVEN by direct independent replay:** two distinct length18 physical solutions of the specified original fixed source; upper bound18; original geometry pinned to C++ P11 physical table.
- **STRONG solver-backed computational conclusion, conditional on the third-party algorithm:** RubikOptimal 1.1.0 reports and log traces an exhaustive depth17 *pruned* search with no solution, so exact optimum18 is currently independently *reported*, not fully checker-certified.
- **Independent earlier certificate:** external Go source-depth10+B6 original root full replay #39087089460 under recorded physical/canonical assumptions confirms lower17, not lower18. Only 2/243 source-depth11 second-prefix regions original P8/P9 native local checked.
- **OPEN for proof-carrying manuscript:** audit soundness and completeness of RubikOptimal pruning/normalization; hash the actual installed wheel and/or obtain second independent no17 computation or a portable small checker; finish physical canonical 16B/20B state bridge.

### Recommended next research
Stop low-yield further local perturbations of the old18 word. Focus on (A) mathematical soundness of optimal solver pruning, (B) second independent exact-distance oracle source at fixed WCA facelet state, (C) compact proof object for a complete no17 search that can be independently checked. *Proof-carrying optimality for this actual published WCA scramble*, not discovery of classical optimal solving/PDB itself, is the defensible manuscript innovation.

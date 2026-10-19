# CUBE-REV 0.27 — P14: Exact B6 checkpoint, complete disk-sharded one-sided B7 goal filter, independent exhaustive inclusion, and measured source-depth comparison

**2026-10-19; actual physical execution complete on T0.** Fixed original WCA source, frozen authentic 54-site P11 physical move table and verified old/new 18HTM upper witnesses unchanged. P13 B7 materialization resource HOLD superseded **only** for goal-side generation/inclusion; global source-depth10 exclusion remains OPEN, no independently certified d18(s)=18 theorem yet.

## A. Immutable full 54-labeled-sticker solved B6 checkpoint
- Original HTM BFS layer sizes **1, 18, 243, 3240, 43239, 574908, 7618438**, exact cumulative **8,240,087**.
- Raw full-physical states 54 bytes per entry, **444,964,698 bytes**, source filename `B6_exact_full54_checkpoint.bin` SHA-256 **`6c042ec76fbca07d6fdf0c1b90ccc7219ec0a007c6d344f27301ba8356f3952e`**. Real build WALL **18.61s**, peak **1,160,832 KiB**.
- **Independent physical checkpoint verifier**, separate compiled C++ source, checks every one of the 8,240,087 unique labeled states, layer-by-layer reachability and closure of every earlier BFS frontier against all eighteen moves: **11,189,682 real directed predecessor transitions**, all PASS. Real independent verifier WALL **13.76s**, peak **1,168,896 KiB**. It does not just trust total state count or source producer PASS.

## B. Actual resumable B6-to-B7 generator, disk partitioning and merge
- Nine independently committed, immutable batches of source B6 offsets `0,1000000,...,8000000`, final batch 240,087. Each batch outputs **64 partitioned raw 64-bit fingerprint shards** via a staging directory and atomic final rename, refuses completed-output overwrite or uncleared incomplete state. Source uses physical 54-site transformations, no third-party PDB.
- Every B6 state contributes its own fingerprint and all 18 legal neighbor fingerprints: exactly **8,240,087×19 = 156,561,653** generated; **1,252,493,224 bytes** across source shard files. Physical emission time per 1m batch ~2.2–3.9 sec, final 240k ~0.66sec, peak stage memory ~62,848 KiB.
- Bounded per-partition exact sort and dedup independently completed all **64 final sorted/strictly unique partitions**, **109,043,123 fingerprint entries**, **872,344,984 bytes**, merge WALL **27.41sec**, peak **70,356KiB**. Hash collisions, if any, are safe false positives; we do NOT rely on collision resistance for the direction of the proof. A partition's hash bytes and source B6 bytes all pinned in machine-readable manifest; full raw 444MB B6 and 872MB B7 are T0 only, not falsely claimed Drive T2.

## C. Independent full inclusion audit — all 156,561,653 checks
A **separately compiled verifier** checks all 64 output partitions are correctly assigned, strictly sorted and duplicate-free; then replays original P11 54-site physical motions from **every checkpoint source B6 record** and checks that each required 64-bit fingerprint (self+18 moves) is actually included in the final goal filter. Real audit split into two disjoint source intervals to meet execution-bound caps:
- `[0,4,000,000)`: **76,000,000 required memberships PASS**, WALL 17.21sec.
- `[4,000,000,8,240,087)`: **80,561,653 required memberships PASS**, WALL 18.49sec.
**Total: 8,240,087 independent B6 source states, 156,561,653 actual obligation checks, complete PASS.** An initially attempted unsplit run timed out and does not count; an early split verifier incorrectly reread first-range states, was identified, discarded and **fixed with an actual source-file seek** before both final range receipts were recomputed. The final original source offsets are explicit and corroborated in logs. This lineage is important; do not silently attribute false two-range coverage to earlier intermediate receipts.
- Negative control physically removes solved state's required fingerprint: **REJECTED** by required membership test.
- Safe positive control adds an unrelated sorted fingerprint: **ACCEPTED** (109,043,124 entries). A correct one-sided superset verifier must not demand exact global cardinality, merely full required goal inclusion. The earlier exact-cardinality requirement was removed from the verifier (the **actual** output remains 109,043,123); proof safety correctly survives extra false positives.

## D. Same-host physical measured comparison, one identical canonical 4-action source prefix
Original fixed WCA source canonical prefix `14,1,4,7`; source-depth10+goal-B7 search and original C8/E6-pruned depth11+goal-B6 both actually run on this same container:
| Metric | source10+B7 | source11+B6 |
|---|---:|---:|
| Grammar virtual nodes in this 4-prefix | **6,802,324** | **90,800,620** |
| Actual visited nodes | **6,802,324** | **5,806,714** |
| Admissible projected omitted nodes | **0** | **84,993,906** |
| Physical meet / one-sided hash hits | **0** | **0** |
| Wall seconds | **7.50** with prebuilt B7 | **16.05** includes rebuilding B6/C8 |
| Peak KiB RAM | **853,640** | **1,218,560** |
| Depth10+goal B7 raw membership rate | ~907,745 tested nodes/sec | different C8/E6 traversal |

**A single cold-start wall comparison is NOT evidence of a 2× globally faster method.** P8 standalone rebuilds huge B6 and C8, whereas P14 assumes its goal-B7 filter already materialized; the P8 source DFS after setup is faster per physically visited node due to strong pruning. True relevant measurement is batched many-prefix runs with both exact goal resources preloaded, plus total one-time preprocessing. P14 does establish a self-contained, auditable **no-length≤17** result for this **one four-prefix sector** conditional on complete one-sided goal inclusion and exhaustive canonical DFA traversal.

## E. Global proof obligation and cost
The exact elementary symmetric split identity is **d(s,e)≤17 iff B10(s) ∩ B7(e) nonempty**, so one signed no-intersection would refute *all shorter lengths too*; no separate old16 lower-bound certificate required in final proof. Grammar-only global canonical masses are **264,501,924,112** nodes at source depth10, versus **3,530,695,794,832** at source depth11 (including ancestors), not actual visited counts. The complete 243 canonical second-prefix source sectors are still unexamined by this *new one-sided framework* (except the measured 4-prefix subset). Even the faster-looking 7.5s/sample implies significant total computation; never extrapolate it as a demonstrated global completion. Existing unrelated full historical P8/P9 two second-prefix source11 negative courts retain their own independent status.

## F. Durable research lineage, code custody and trust
Local T0 original assets `/mnt/data/cuberev027_p14/`: full immutable B6 raw checkpoint, all nine 64-shard B7 emission batches, 64 exact final B7 shards, compiled independent builders/checkers, real terminal logs; **the full large binary material is not yet independently sealed in Drive.**
- T2 verified **small complete reproducibility capsule** containing all C++ build/merge/audit/benchmark programs, P11 authentic physical move table, execution logs, independently computed entire sorted-shard SHA manifest and B6 checkpoint SHA: **24,803 bytes, SHA256 `5fb3c3b2519bb3e4965162d533d614fb725cc362e11911509fb4cf3d6884f75e`**, actually uploaded to Drive original `10_CANONICAL_PROOF_COURTS` folder as [P14 code/log/manifest bundle](https://drive.google.com/file/d/1rt3kGTuYFLRoam9t6VFMwxn4JoP6bBjK/view), downloaded raw again, 24,803 exact bytes and SHA matched local source. ZIP includes 19 files; giant originals explicitly excluded.
- Source version `research/current`, original WhoSia author+committer only, no bot commits. No GitHub Actions external B7 replay or first-root global sweep has yet run.

## P15 decision
Prioritize a persistent batch runner to amortize the prebuilt B7 full-goal filter across many real original source-depth10 prefixes (first 2-prefix closure with fail-closed complete grammar accounting); do not abandon C8/E6 acceleration until measured in comparable warm-start settings. Build a portable compact proof-carrier `{original WCA fixed source, B6 raw SHA, B7 shard hashes, independently checked inclusion receipts, source10 per-prefix exhaustive zero-hit receipts}`. For a complete published exact18 theorem, ensure the union of all correct canonical prefixes covers all <=10 source words with no lost representatives. An independently auditable global no17 proof remains OPEN.

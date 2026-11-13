# CUBE-REV 0.28 R14-P8.33 — Fresh independent P48 41-class B6 MITM re-execution

**Date:** 2026-11-13. **Branch:** `research/current`. **Scientific status:** independently authored C++ executor, fresh P48 geometry source generation, actual GitHub Actions PASS, ZIP re-download byte equality PASS. The `2026-10-30` historical B5 ZIP remains missing, but is not an input to this self-contained P48 route.

## 1. Question and exact claim

For persistent original-cubie full-position-and-orientation measurements on the legal 3x3 cube, each surviving B6 sixteen-tag layout has twelve legal pointwise stabilizer states, eleven of them nonidentity. Up to proper 24 cube rotations, the 156 positive candidate layouts reduce to eight geometric orbits; their 8×11=88 nontrivial stabilizer instances have 74 distinct P48 physical actions and 41 classes under full 48 spatial isometries and inversion. This finite quotient is regenerated and checked by `b6_independent_48sticker_goals.py` with 864 generator-covariance checks and 324 two-turn factor-transfer comparisons; the 41 target goal list and 18×20×24 factor table are generated anew.

**Exact machine question:** Is any of those 41 nonidentity target actions contained in the 12-HTM ball `B12`? If none is, all 156 candidate sets are injective on `B6`, provided the stabilizer-orbit coverage just stated. This is `distance >=13`, **not** a proof of `distance = 13`.

## 2. Distinct from prior November 4 computation

A new source `scripts/cuberev-observation/audit_r14_p833_fresh_b6_mitm.cpp` (human-committed, not the earlier `verify_b6_41_mitm_p48.cpp`) independently implements:
- 20 independent 24-value original-cubie factors packed into 12 edge and 8 corner components;
- generator table bijectivity, quarter-turn/inverse and square-half-turn algebra across all factors;
- deterministic half-turn-metric word normal form excluding consecutive same-face moves and ordering commuting opposite-face moves; this pruning preserves every reachable group element at equal or shorter length;
- complete 6-HTM ball construction with **8,331,112 normalized paths** and **8,240,087 distinct states**, plus solved/18 one-move positive controls;
- forward ≤6 from each target and intersection against the solved ≤6 ball, which is equivalent to membership in `B12`, by symmetry and midpoint decomposition.

41 targets × 8,331,112 query nodes = **341,575,592** attempted target-side search probes. All 41 have zero intersections; no early termination.

During an independent container rehearsal, 16 of 41 targets passed before execution was stopped by the tool runtime limit. This is NOT confused with a 41-target completed local replay; the authoritative **full** execution is the later GitHub Actions run below.

## 3. Completed remote CI and cryptographic comparison

The read-only [GitHub Actions run 43349579675](https://github.com/WhoSia/CUBE-REV/actions/runs/43349579675) completed SUCCESS:
- freshly `--emit`-generated `targets41.txt`, `b6_factor_table.hpp`, `raw_goal48.hex` SHA-256 all match their independently preserved Nov 4 source bytes;
- new C++ file compiles and runs all 41 targets;
- all 41 records contain `collision=0 probes=8331112`, IDs 0..40 exactly once;
- exactly 41 PASS and 0 FAIL; read-only repository working tree; artifact uploaded.

[Workflow](../../.github/workflows/cuberev-r14-p833-fresh-41-b6-mitm.yml) and [verifier](../../scripts/cuberev-observation/audit_r14_p833_fresh_b6_mitm.cpp).

Input hashes:
```
targets41.txt      363edfb2f25b267735f93895103125ba97e457c14937499955f4bf4e7bcdcba8
b6_factor_table.hpp 33ab96ee24228febc89740676078d7abb0967a468b3aba338e4e6ea75eb3a021
raw_goal48.hex      f73c09094a4ed327f4ab8f9295c3dd1cbdc139b312e3d52ea998591a3ff685b9
```

New receipt log SHA-256: `8aceb27a077bd2db9babbf6f139a423595fb0d87c2cea8553faee1b80a1de23c`.

GitHub artifact id `14002898391`, archive SHA-256 `3b58ca1abb93f4615c20d4e62ccedbe83b4f152b60a9e63ed400c3bcd86df0b1`, 2983 bytes, six files. Downloaded artifact was independently parsed in the execution environment; the three regenerated source files were checked **byte-for-byte** against the original historical GitHub artifact ZIP, and 41 output rows independently parsed. All six constituent files and their hashes are preserved.

Uploaded the complete **new** artifact ZIP to Drive [P8.33 independent 41-target proof bytes](https://drive.google.com/file/d/1wBw8zCFs4pBXzRMx2ONOCWCZDLZKZSec/view), Drive ID `1wBw8zCFs4pBXzRMx2ONOCWCZDLZKZSec` under `20_SECONDARY_DATA_FRONTIER`. After actual Drive re-download, SHA-256 matched the new GitHub artifact byte-for-byte; `cmp` PASS.

[Machine-readable experiment/custody data](../../data/0.28/R14_P833_20261113_FRESH_B6_41_TARGET_FULL_REPLAY_AND_DRIVE_SEAL.json).

## 4. Relationship to the B6 positive-layout proof

The generator itself demonstrates:
```
156 candidates = 8 proper-rotation layout orbits
8 layouts × 11 nonidentity stabilizer states = 88 target entries
88 entries = 74 distinct P48 physical transformations
74 actions = 41 distance-preserving symmetry/inversion classes
```
Because turn distance is invariant under legitimate 48 spatial conjugacies and inversion, **the 41 distance ≥13 decisions cover every nonidentity stabilizer element** of each of the 156 candidate layouts. The P8.33 full independent calculation is therefore a fresh, genuinely executed positive-side certificate, not just a replay of a historical success message.

The negative-side distinct 872 physical short-support masks, all 4689 excluded size-16 layouts, and the 15504 size-15 lower-bound check are preserved in the November 4 historical ZIP and pre-existing self-contained `verify_b6_complete_4845_p48.py`. Re-run that negative-side code with the fresh source in an equally sealed CI if requiring one self-contained current-date release bundle for journal submission.

## 5. Caution and strategic release gate

This is a **fresh run of 41 exact radius-twelve exclusions**, not an independently source-different physical model: the data generator is the same original 3D P48 source used in the earlier historical run (newly executed and SHA-compared), while the MITM implementation is independently authored. The generator's geometric assumptions, target enumeration and stabilizer quotient remain part of the mathematical code+proof package, not arbitrary trusted oracles. The 41 targets are not guaranteed to have exact word distance 13.

The 2026-10-30 B5 ZIP is still missing as an **historical custody item**, but cannot fairly be described as preventing reproducibility of the modern P48 proof, which regenerates physical P48 goals independently without that archive.

**Next:** replay and SHA-seal the P48 872-support negative/completeness court, bind both physical subproofs into C0.2 paper release evidence, and then prioritize the unrestricted 19-frame color feedback horizon. Never conflate tag sensor count with categorical observation frames.

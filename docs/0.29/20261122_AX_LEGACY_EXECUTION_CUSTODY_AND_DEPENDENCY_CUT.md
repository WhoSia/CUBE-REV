# AX — Closed execution retirement, dependent-code holds, and exact-byte recovery

**Date:** 2026-11-22. **Pre-retirement source HEAD:** `7904b9d2822aa58f61a5b4890f7f3cba7ea02184`.

**Authoritative source copy:** [Google Drive 42-file exact-source ZIP](https://drive.google.com/file/d/1iWDpLIFOwFfm-qg3Z7lInhmChOotP1jm/view) in [CUBE-REV 90_RESEARCH_CURRENT_ARCHIVE](https://drive.google.com/drive/folders/1xpUKiXclYvGGPMpE9dVDhp2lOc_YJzRS).

**GitHub Actions preseal:** [run #44927378295](https://github.com/WhoSia/CUBE-REV/actions/runs/44927378295), artifact `14716750792`; outer ZIP SHA-256 `097514a9d1ca1cbfba00166582434f5e4d4627233a8eaaf64c27c02d9dfb38fd`, exactly 36,903 bytes. Drive raw-file readback reproduced the entire ZIP byte-for-byte with the same SHA-256. The `MANIFEST.json` lists all 42 original file paths and each exact Git blob SHA, original size and SHA-256. All 42 files in `exact-sources.tar.gz` independently matched their manifest entries.

## Exact live-tree cut

- `scripts/cuberev-011/**`: 6 obsolete original code/tests;
- `scripts/cuberev-013/**`: 4 obsolete original code/tests;
- `scripts/cuberev-014/**`: 6 obsolete original code/tests;
- `scripts/cuberev-016/**`: 24 obsolete original code/tests, including **six Python files**;
- `.github/workflows/cuberev-011-face-word-regression.yml` and `.github/workflows/cuberev-016-small-core.yml`: 2 closed-stage CI declarations, no longer part of 0.29 primary Lean CI;
- `.github/workflows/cuberev-legacy-code-custody-one-shot.yml`: the temporary read-only archive workflow, retired after completing custody.

The two old workflows were the only non-archived workflow references to the 0.11/0.13/0.14/0.16 paths identified by direct code search. The search does not formally rule out dynamic filenames assembled at runtime: all source bytes remain recoverable under their pinned pre-retirement HEAD. Do **not** claim any retired legacy mathematical assertion is thereby reproduced by current Lean 0.29.

**Explicit HOLD:** `scripts/cuberev-015/**` remains tracked, since multiple later `cuberev-019` and `cuberev-020` workflows still reference that cohort. Likewise 0.29 frozen policy checkers, pinned inputs and current Lean targets are untouchable without demonstrated replacement and independent regression. This retirement preserves the exact historical code in Drive, instead of treating Python and C++ as universally dispensable.

## Evidence and links

Historic `docs/0.16/**` papers/receipts are retained as context; source links for any retired program should be pinned to the immutable [pre-retirement Git tree](https://github.com/WhoSia/CUBE-REV/tree/7904b9d2822aa58f61a5b4890f7f3cba7ea02184/scripts/cuberev-016) or restored from the Drive ZIP. Original source SHA, archive manifest and CI custody run allow exact-byte restoration. The P7 active-set allowlist is reconciled atomically with this deletion. No `github-actions[bot]` authored commits are permitted. The CI artifact's 90-day provider retention is not the canonical archive; Drive is.

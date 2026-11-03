# CUBE-REV GitHub branch-custody and readme-retirement audit — 2026-11-03

## Objective and actual disposition

The repo's REPOSITORY_POLICY.md requires a stable main, a single canonical research/current, and at most a justified release branch. The 2026-11-03 audit found an out-of-date research/current behind the actively developed research/observation-generalization. A **non-force fast-forward** was executed, in two explicitly verified non-destructive steps:

1. research/current: 4a2ff248146c1a0f6bd457b1f4c4d890c6492006 -> 7adbad07e10dc89ebdd8f182d8c48e57283394e4; expected prior SHA lease used.
2. research/current -> b0533697b1ea9c73cd8d4316a95864b2d1fb6f6f; all 0.28 evidence through the previous turn. The exact comparison research/current vs research/observation-generalization returned identical, 0 ahead/behind, at this checkpoint.
3. Subsequent current-only research/README/governance commits were made on research/current, so the former observation branch is now strictly an ancestor rather than the active branch. **No forced ref updates and no history rewriting.**

## Branch inventory, comparison and deletion decision

All branch heads were checked via GitHub REST and compared to the new canonical research/current after its initial 0.28 migration:

| Branch | Readback head at audit | Original comparison to research/current, relative ahead / behind | Action |
| --- | --- | --- | --- |
| main | a5b16ad3f64c7f3de31b891e439c40e902d582bf | diverged: current 1902 ahead, 13 unique to main | PRESERVE stable/deployment branch; never force-overwrite |
| research/current | new canonical active 0.28 lineage | current research source of truth | PRESERVE; continue commits only here |
| research/observation-generalization | b0533697b1ea9c73cd8d4316a95864b2d1fb6f6f | originally identical with research/current, later behind by canonical commits | CONTENT INTEGRATED; retiring the remote ref is still PENDING, because currently exposed GitHub connector lacks an authenticated branch delete-ref action. Never claim it was deleted. |
| paper1-m1.1-public-repro-rc | 51f0093e9f2e5c5938d5fca3ddf58e342cb330ce | diverged: current 1902 ahead, 28 unique to release branch | HOLD release-candidate branch until Paper1 publication/rights maintenance and merge-base audit |
| archive/pre-p7-active-prune-20261002 | f9fb6e859ea0130aa3a0b0bb7994a7f7060a8183 | diverged: current 1902 ahead, 434 unique to archive branch | HOLD deletion until complete byte-level recovery validation, despite metadata-confirmed Drive ZIP below |
| archive-attribution-20261002 | 177c3f5fccb79d2602006c4937e3c9eccf7d805a | diverged: current 1902 ahead, 785 unique to archive branch | HOLD; separate unique commits have NOT been confirmed fully preserved |
| clean-attribution-20261002 | 52fc4a04c922ea0d39dd29cdf1ac6ebed5a196a1 | ancestor: zero unique commits to this branch, current ahead 1902 | RETIREMENT CANDIDATE; remote branch deletion is not available via connected GitHub actions |

**Why not blindly delete four branches:** additional unique commit histories in archived/deployment branches are not made recoverable merely by copying a README. GitHub history and the existing Drive archive must be checked by exact bundle and SHA before deleting those refs. A GitHub branch-ref delete action was NOT found among the connected GitHub operations; deletion must not be falsified or emulated by moving the ref to a different commit.

## Verified Drive archive assets and README retirement

- Existing primary full Git history ZIP: [CUBE-REV pre-P7 full history](https://drive.google.com/file/d/1VjWE0a7V13aBgZRZgngRUvqZVkkkKLG5/view), 59,126,859 bytes; existence and location verified by Google Drive metadata, *not* raw SHA-256 rechecked in this turn.
- Existing archive ledger: [Repository Active-Set Archive Ledger](https://docs.google.com/document/d/1OPuOHUHSLTXSaQOcKgJOrC1ebJ4z-HdKTLCC16InACI/edit).
- Original 133,848-character pre-rewrite README from Git blob bd643ceeef2f928efd89a0e54070aab424e8d88d was copied to [Drive 2026-11-03 README snapshot](https://docs.google.com/document/d/1wNsqPo3Iit14kDNkugY_84VmEtDMTSUnhLxzw_yNiJY/edit) and read back; exact original text recovered by dropping Google Docs' one additional terminal newline. Current README rewritten to 0.28 present-stage intro.
- Pre-2026-10-12 109,858-character GitHub archive file archive/readme/README_RESEARCH_CURRENT_FULL_PRE_P0R2_20261012.md was matched character-for-character to independently existing [Drive raw Markdown archive](https://drive.google.com/file/d/1QQ18TJ2Ary6xl4tD1iRX3ErdVx5HDHwi/view) before the *redundant live GitHub file* was removed by human author commit 4c12817a4c3b3543da22ea2ff165694770c11595. Its Git blob SHA 11f726c24f6bc032f2469f91f4dc60c5d7d3a92a is retained by Git object history.

## Critical P7 file allowlist reconciliation

After fast-forward, P7 exact active-only CI initially found 173 newly tracked exact files absent from the 916-path legacy manifest, and 1 listed retired README no longer on disk. The active-set manifest g7/p7/active-set-manifest.json was updated by an explicit non-truncated Git blob listing, **without wildcard admission**, to 1088 current file paths. A new reconciliation ledger records 173 path admissions and the 1 source-verified retirement; [CI run 41603098371](https://github.com/WhoSia/CUBE-REV/actions/runs/41603098371) succeeded. Subsequent new 0.28 paper/novelty documentation introduces new exact paths that must be admitted in a later manifest update; a temporarily failing path gate is not a scientific test failure and must NOT be disabled.

The observation GitHub Actions workflow was extended to run on canonical research/current (read-only checkout, no bot-author commits). The updated fixed-cover physical smoke and entire 156-sensor full-swap graph test passed [CI run 41602897588](https://github.com/WhoSia/CUBE-REV/actions/runs/41602897588). This is a Python/graph smoke, not a new 41-target physical MITM run.

## Next operations and stop conditions

1. Update P7 allowed_paths each time an intentional new paper/proof file is added; never disable the gate because tests are red.
2. Only the user with an authenticated GitHub delete-ref capability can actually remove merged obsolete branch refs. The most immediate candidates are research/observation-generalization and clean-attribution-20261002. Delete only the two explicitly confirmed no-unique-work refs, never main, release RC or 434/785-unique-commit archive refs on this evidence alone.
3. Verify the existing 59-MB full-history ZIP raw SHA and coverage, specifically whether the archive-attribution and release branches' unique commits are represented.
4. When all remote branch refs are stable, revisit REPOSITORY_POLICY.md and ensure future 0.28 commits land solely on research/current.
5. Do not confuse the number of files admitted to repository allowlist with number scientifically verified or required as long-term reproducibility sources.

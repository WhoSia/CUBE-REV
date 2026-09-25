# CUBE-REV branch retirement audit — P14

Status: non-destructive audit. No remote branch has been deleted by this audit.

## Target live topology

Keep as durable live branches:

- `main` — public canonical repository history/runtime surface.
- `research/data-spine` — active secondary-data registry, acquisition recipes, schemas, release compiler.
- `paper1-m1.1-public-repro-rc` — retain while Paper 1 external/submission closure remains active.

Temporary live branches; retire after preservation/merge or explicit supersession:

- `g3-p10-r1-cognitive-runtime`
- `g3-p11-rstp-navigation`
- `paper1-m1.0-brm-zenodo-rc`

## Tier D — delete after full-history bundle verification

These are execution/staging/smoke branches whose scientific value is already represented by later stages or receipts. They do not merit independent long-term remote refs once the full Git history bundle is verified.

- `agent/calibration-0711`
- `cube-rev-0.10.5-r1.3-main-staging`
- `cube-rev-0.10.5-r1.4-live-collector-canary`
- `cube-rev-0.10.5-r1.7-raw-route-preflight`
- `cube-rev-0.10.5-r1.7-state-engine-smoke`
- `cube-rev-0.10.5-r1.7-state-engine-smoke2`
- `cube-rev-0.10.5-r1.11-execution-trigger`

Additional staging/smoke/canary branches should be treated the same after the inventory script confirms no active PR depends on them.

## Tier C — preserve in one full-history Git bundle, then remove remote refs

Historical developmental lineages are valuable as provenance but do not need to remain as dozens of visible remote branches.

Family A — `cube-rev-0.8.*`
- `cube-rev-0.8.5-participant-cognitive-mode`
- `cube-rev-0.8.5-recovery`
- `cube-rev-0.8.6-blinded-telemetry`
- `cube-rev-0.8.7-collector-shadow-gate`
- `cube-rev-0.8.8-immutable-submission-snapshot`
- `cube-rev-0.8.9-public-bank-minimization`
- `cube-rev-0.8.10-cross-version-migration`
- `cube-rev-0.8.11-atomic-migration-arbitration`
- `cube-rev-0.8.12-active-session-cas`
- `cube-rev-0.8.13-native-browser-live-factory`
- `cube-rev-0.8.14-custody-device-staging`
- `cube-rev-0.8.15-cognitive-mechanism-lattice`
- `cube-rev-0.8.16-minimal-trajectory-probes`
- `cube-rev-0.8.17-versioned-external-trajectory`
- `cube-rev-0.8.18-temporal-route-calibration`

Family B — old `cube-rev-0.10.5-r1.*` execution/science branches through the pre-data-spine era. Preserve the entire ref family in the bundle; do not keep each branch visible merely as historical navigation.

Family C — superseded research transfer/census refs after their unique objects are present in the bundle:
- `research/r1.23-crosswalk-rebuild`
- `research/r134-byte-transfer`
- `research/r135-archive-census`

## Tier B — keep a named archival pointer or tag if desired, otherwise bundle is sufficient

These have unusually high interpretive/provenance value and may deserve a compact tag even after branch deletion:

- `cube-rev-0.7.22-public-snapshot`
- endpoint of the 0.8 lineage (`cube-rev-0.8.18-temporal-route-calibration`)
- final R1 manuscript/science bridge state (`cube-rev-0.10.5-r1.15-manuscript-bridge` or its verified superseding final seal)
- G3 cognitive runtime certification head
- G3 RSTP navigation certification head

Do not retain both branch and archival tag indefinitely unless the ref is genuinely active.

## Required preservation receipt before deletion

Create a mirror clone and immutable bundle before deleting any historical remote refs:

```bash
git clone --mirror https://github.com/WhoSia/CUBE-REV.git CUBE-REV.git
cd CUBE-REV.git
git show-ref > ../CUBE-REV_PRE_P14_refs.txt
git bundle create ../CUBE-REV_PRE_P14_FULL_HISTORY.bundle --all
git bundle verify ../CUBE-REV_PRE_P14_FULL_HISTORY.bundle
sha256sum ../CUBE-REV_PRE_P14_FULL_HISTORY.bundle ../CUBE-REV_PRE_P14_refs.txt > ../CUBE-REV_PRE_P14_SHA256.txt
```

Store the bundle, refs inventory and checksum file under Google Drive `20_SECONDARY_DATA_FRONTIER/00_REGISTRY_AND_LICENSES/REPOSITORY_ARCHIVE/` (or a sibling project-provenance folder). The bundle is the preservation authority; branch deletion is only UI/ref cleanup.

## Remote deletion procedure

After bundle verification and Drive upload:

```bash
git push origin --delete <branch-name>
```

For batches, first review the generated deletion list. Never use a wildcard deletion command directly against `origin`.

GitHub UI alternative: repository → **Branches** → locate branch → trash/delete icon. Do not delete `main`, `research/data-spine`, or an active Paper 1 branch.

## PR rule

Before deleting a branch that is the head of an open PR, either merge it or close the PR with a pointer to the superseding commit/tag/bundle receipt. Current G3 PR branches should remain until this is done.

## Success criterion

The normal visible repository should converge toward approximately:

1. `main`
2. `research/data-spine`
3. one active Paper 1 branch while needed
4. at most one or two genuinely active execution branches

Everything else should be recoverable from the Drive Git bundle and compact provenance receipts rather than exposed as permanent remote branches.

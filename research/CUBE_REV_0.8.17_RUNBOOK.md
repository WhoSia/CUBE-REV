# CUBE-REV 0.8.17 runbook

## Reproduce

```bash
python analysis/external_trajectory_snapshot_0_8_17.py \
  --fixtures research/CUBE_REV_0.8.17_EXTERNAL_TRAJECTORY_FIXTURE_PACK.json \
  --probe-registry research/CUBE_REV_0.8.16_TRAJECTORY_PROBE_REGISTRY.json \
  --outdir artifacts/0.8.17

python tests/external_trajectory_snapshot_0.8.17.test.py \
  --analysis analysis/external_trajectory_snapshot_0_8_17.py \
  --artifact-dir artifacts/0.8.17 \
  --fixtures research/CUBE_REV_0.8.17_EXTERNAL_TRAJECTORY_FIXTURE_PACK.json \
  --probe-registry research/CUBE_REV_0.8.16_TRAJECTORY_PROBE_REGISTRY.json
```

## Source refresh rule

A later WCA export or changed reconstruction page never silently replaces this snapshot. Create a new snapshot version, retain the previous fixture and manifest, record retrieval date and source URL, rerun notation/STM/linkage gates, and compare estimands across snapshots.

## Adding a public reconstruction

Transcribe only visible scramble, move notation, stage labels, result and reported STM/TPS. Retain source URL and retrieval date in the source record. Do not copy private comments, account data or hidden endpoints. Run unsupported-token rejection and STM conformance before inclusion.

## Smart-cube/timer data

Accept only an explicit owner export or intentionally shared link. Store consent scope and revocation status separately. Do not join to named public reconstructions unless the owner expressly authorizes the linkage.

## Promotion boundary

This version certifies a small external research fixture and partial local grammar support only. It does not authorize bulk ingestion, participant deployment, named-person inference or ecological equivalence claims.

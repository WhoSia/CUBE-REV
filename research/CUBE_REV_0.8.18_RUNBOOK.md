# CUBE-REV 0.8.18 runbook

## Deterministic build

```bash
python analysis/minimal_trajectory_probes_0_8_16.py \
  --bank cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json \
  --outdir /tmp/cr0816 \
  --family-count 6 \
  --sessions-per-mechanism 360 \
  --seed 8162026

python analysis/temporal_route_calibration_0_8_18.py \
  --fixtures research/CUBE_REV_0.8.18_PUBLIC_TIMESTAMP_FIXTURE_PACK.json \
  --synthetic-trajectories /tmp/cr0816/simulated_trajectories.jsonl \
  --outdir /tmp/cr0818
```

## Contract court

```bash
python tests/temporal_route_calibration_0.8.18.test.py \
  --analysis analysis/temporal_route_calibration_0_8_18.py \
  --fixtures research/CUBE_REV_0.8.18_PUBLIC_TIMESTAMP_FIXTURE_PACK.json \
  --synthetic-trajectories /tmp/cr0816/simulated_trajectories.jsonl \
  --artifact-dir /tmp/cr0818
```

Expected markers:

```text
CR0818_TEMPORAL_CALIBRATION_PASS fixtures=3 events=164 trajectories=3600 js_before=0.292674 js_after=0.254332 consent=HOLD
CR0818_TEMPORAL_ROUTE_CALIBRATION_PASS 28/28
```

## Future consented owner export

Do not place a private export in a public branch. Create a consent capsule, hash the unchanged raw export, run a format-specific parser in a private custody environment and commit only an approved deidentified fixture or aggregate result. Sequence-counter and state-continuity claims require the corresponding raw fields; they may not be inferred from a clean timestamp sequence.

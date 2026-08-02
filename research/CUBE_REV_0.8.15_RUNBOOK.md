# CUBE-REV 0.8.15 Runbook

## Purpose

Reproduce the offline synthetic identifiability audit for:

**CUBE-REV 0.8.15 — Cognitive Mechanism-axis Lattice, Strategy-transition Signatures & Identifiability-constrained Hypothesis Registry**

This runbook does not authorize participant deployment, a human mechanism label, or modification of the current bank and schedules.

## Fixed inputs

```text
cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json
cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json
```

The analysis reads the inherited 28 stimuli and 24 schedules. They are inputs, not 0.8.15 outputs.

## Environment

```text
Python 3.11+
standard library only
```

## Syntax check

```bash
python -m py_compile analysis/cognitive_mechanism_lattice_0_8_15.py
python -m py_compile tests/mechanism_lattice_0.8.15.test.py
```

## Full execution

```bash
rm -rf artifacts/0.8.15
python analysis/cognitive_mechanism_lattice_0_8_15.py \
  --bank cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json \
  --config cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json \
  --outdir artifacts/0.8.15 \
  --sessions-per-mechanism 240 \
  --seed 8152026
```

Expected marker:

```text
CR0815_MECHANISM_LATTICE_PASS sessions=2640 planning=IDENTIFIABLE switch=IDENTIFIABLE open_closed=NON_IDENTIFIABLE capacity=NON_IDENTIFIABLE rotational_pairs=1
```

## Determinism check

Run into two independent directories:

```bash
rm -rf /tmp/cr0815-a /tmp/cr0815-b
python analysis/cognitive_mechanism_lattice_0_8_15.py \
  --bank cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json \
  --config cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json \
  --outdir /tmp/cr0815-a --sessions-per-mechanism 240 --seed 8152026
python analysis/cognitive_mechanism_lattice_0_8_15.py \
  --bank cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json \
  --config cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json \
  --outdir /tmp/cr0815-b --sessions-per-mechanism 240 --seed 8152026

diff -ru /tmp/cr0815-a /tmp/cr0815-b
```

Expected: no diff.

## Test suite

```bash
python tests/mechanism_lattice_0.8.15.test.py
```

Expected marker:

```text
CR0815_MECHANISM_LATTICE_TEST_PASS deterministic=true positive_controls=2 negative_controls=2 stimuli=28 schedules=24
```

The test uses 120 sessions per mechanism for speed and runs the model twice. It must verify:

- byte-identical outputs across reruns;
- 28 stimuli and 24 schedules;
- 27 rotational orbits and exactly one repeated pair;
- horizon audit counts;
- both positive controls above the declared threshold;
- both negative controls near chance and classified non-identifiable;
- registry rules and forbidden claims.

## Static research-output check

The committed mechanism-axis registry must exactly equal the generated registry:

```bash
cmp artifacts/0.8.15/CUBE_REV_0.8.15_MECHANISM_AXIS_REGISTRY.json \
    research/CUBE_REV_0.8.15_MECHANISM_AXIS_REGISTRY.json
```

The full result, horizon audit, orientation audit, schedule audit, and synthetic session feature rows remain CI artifacts. Their decisive statistics are pinned in the decision packet and checked directly by CI rather than copied into a second repository source of truth.

## Required interpretations

### Positive controls

`IDENTIFIABLE` means the deliberately separated synthetic generators leave distinct current features under this bank, heuristic, and classifier. It must never be rewritten as evidence that real participants use the named mechanism.

### Negative controls

`NON_IDENTIFIABLE` is a pass when the two latent generators are intentionally observationally identical. A classifier that reliably separates them is a leakage or implementation failure.

### Horizon annotation

The horizon values maximize a solved-sticker score with no consecutive same-face expansion. They are transparent stimulus annotations, not optimal solve distance and not an asserted participant utility.

## Protected files and paths

0.8.15 must not change:

```text
index.html
collector-config.js
js/collector-client.js
participant-cognitive-mode-0.8.14.html
unsupported-browser-0.8.14.html
cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json
cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json
```

Any change is a blocking scope violation.

## Stop conditions

Stop and issue `NO_GO` for 0.8.15 when:

- deterministic outputs differ;
- either negative control exceeds the synthetic identifiability threshold;
- a positive control falls below its threshold without explanation;
- the cube rotation audit does not yield 24 proper rotations;
- bank or schedule counts differ from 28 and 24;
- a report equates synthetic labels with human latent states;
- trialwise confidence or another reactive measurement is added without a separate reactivity design;
- a protected participant, bank, Collector, or production file changes.

## Output inventory

```text
artifacts/0.8.15/CUBE_REV_0.8.15_MECHANISM_AXIS_REGISTRY.json
artifacts/0.8.15/mechanism_identifiability_result.json
artifacts/0.8.15/horizon_stimulus_audit.json
artifacts/0.8.15/orientation_pair_audit.json
artifacts/0.8.15/schedule_balance_audit.json
artifacts/0.8.15/simulated_session_features.jsonl
```

The JSONL file contains synthetic session-level features only. It must not be mistaken for participant data or merged into a human cohort.

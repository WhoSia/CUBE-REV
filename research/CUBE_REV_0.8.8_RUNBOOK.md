# CUBE-REV 0.8.8 Rerun Runbook

## Purpose

This runbook makes the 0.8.8 certification resumable if a chat response, browser session, or external connector call is interrupted.

## Checkpoint A — branch identity

```text
base: cube-rev-0.8.7-collector-shadow-gate
head: cube-rev-0.8.8-immutable-submission-snapshot
```

Required 0.8.8 files:

- `cognitive/COGNITIVE_MODE_CONFIG_0.8.8.json`
- `cognitive/PARTICIPANT_STIMULUS_BANK_0.8.8.json`
- `cognitive/TELEMETRY_SCHEMA_0.8.8.json`
- `js/participant-cognitive-mode-0.8.8.js`
- `participant-cognitive-mode-0.8.8.html`
- `tests/immutable_snapshot_contract_0.8.8.test.js`
- `research/CUBE_REV_0.8.8_VALIDATION_REPORT.md`
- `research/CUBE_REV_0.8.8_DECISION_PACKET.json`

## Checkpoint B — executable contract

From the repository root, run:

```bash
node tests/immutable_snapshot_contract_0.8.8.test.js
```

Required marker:

```text
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

Any other exit or marker is a blocking `HOLD`.

## Checkpoint C — syntax

```bash
node --check js/participant-cognitive-mode-0.8.8.js
node --check tests/immutable_snapshot_contract_0.8.8.test.js
```

Extract the inline script from `participant-cognitive-mode-0.8.8.html` and run `node --check` on the extracted file, or perform an equivalent browser parse check.

## Checkpoint D — frozen collector diff

Compare the 0.8.7 base and 0.8.8 head. The following paths must not occur in the changed-file list:

```text
collector-config.js
js/collector-client.js
```

## Checkpoint E — participant route smoke test

Serve the repository over HTTP rather than opening the page through `file://`.

Verify:

1. start creates one stable anonymous token and one of 24 sequences;
2. refresh restores the same sequence and cursor;
3. the task reaches post-task after 28 responses;
4. submission snapshot is created once;
5. simulated receipt loss exposes retry without changing the exported snapshot;
6. duplicate recovery produces the received state;
7. corrupted local state is quarantined and not silently resumed.

## Checkpoint F — external gates

The following require owner or live-environment execution and stop automatic continuation:

- live collector health and POST smoke test;
- Factory import and condition reconstruction;
- production default-entry change;
- mobile and desktop owner walkthrough.

## Promotion rule

Promote beyond the research branch only if checkpoints B–E pass and the external gates are explicitly authorized. Otherwise preserve the branch and decision packet as a reviewable `HOLD` artifact.

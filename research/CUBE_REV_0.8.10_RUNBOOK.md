# CUBE-REV 0.8.10 Rerun Runbook

## Purpose

This runbook allows the 0.8.10 certification to be resumed after a chat timeout, browser interruption, or connector failure without reconstructing the research history from memory.

## Checkpoint A — branch and stack identity

```text
base: cube-rev-0.8.9-public-bank-minimization
head: cube-rev-0.8.10-cross-version-migration
pull request: #9
```

The following frozen files must not appear in the version diff:

```text
collector-config.js
js/collector-client.js
```

## Checkpoint B — required implementation files

```text
scripts/build_0_8_10_assets.js
js/asset-pins-0.8.10.js
js/public-asset-verifier-0.8.10.js
js/participant-cognitive-mode-0.8.10.js
js/cross-version-migration-0.8.10.js
participant-cognitive-mode-0.8.10.html
tests/cross_version_resume_hash_pin_0.8.10.test.js
cognitive/PARTICIPANT_STIMULUS_BANK_0.8.10.json
cognitive/COGNITIVE_MODE_CONFIG_0.8.10.json
research/CUBE_REV_0.8.10_ASSET_MANIFEST.json
research/CUBE_REV_0.8.10_VALIDATION_REPORT.md
research/CUBE_REV_0.8.10_DECISION_PACKET.json
```

## Checkpoint C — deterministic asset build

From the repository root:

```bash
node scripts/build_0_8_10_assets.js
```

Required marker:

```text
CR0810_ASSET_BUILD_PASS stimuli=28 choices=504
```

The resulting pins must be:

```text
manifest  7961e5b36320c303b1784f5f35fa915042c13e25a3fc716242f4e70ccb97df81
bank      38b706b0dbf6735ac6cefb34289aa6fe36dcf8252552ed22ee9c7be4af55ed89
config    040ded0ea10cbdd794e924b35ac09be9e4c25dbf707727be03e38929db5ab54d
parent    00b9c255dd050638020e9436fb01911d8e50f886595d4dd14bc529ded906813a
crosswalk 90c54b51052fc27c436d8701797e5b2aa95e19ec28a7f63bbd50db41192748f0
```

Any mismatch is a blocking `HOLD` and must not be fixed by manually editing the pins.

## Checkpoint D — executable contracts

```bash
node tests/cross_version_resume_hash_pin_0.8.10.test.js
node tests/public_bank_minimization_0.8.9.test.js
node tests/immutable_snapshot_contract_0.8.8.test.js
```

Required markers:

```text
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

## Checkpoint E — syntax and participant-route parse

```bash
node --check scripts/build_0_8_10_assets.js
node --check js/public-asset-verifier-0.8.10.js
node --check js/participant-cognitive-mode-0.8.10.js
node --check js/cross-version-migration-0.8.10.js
node --check tests/cross_version_resume_hash_pin_0.8.10.test.js
```

Extract the non-empty inline script from `participant-cognitive-mode-0.8.10.html` and run `node --check` on it, or use the exact workflow implementation in `.github/workflows/build-0.8.10-migration.yml`.

## Checkpoint F — migration cases

Manually or programmatically verify the following cases before any promotion:

1. no legacy source creates one fresh 0.8.10 session;
2. an unfinished 0.8.8 session resumes at the same cursor with the same token, session, sequence, and schedule;
3. each migrated 0.8.8 display choice resolves to the certified opaque code;
4. an unfinished 0.8.9 session preserves the existing opaque responses exactly;
5. a 0.8.8 or 0.8.9 `READY_TO_SUBMIT` state without a snapshot migrates and can seal a 0.8.10 snapshot;
6. a sealed legacy state remains byte-identical and returns its original retry route;
7. injected failure after target write removes the target and leaves the source unchanged;
8. an invalid legacy source is quarantined;
9. simultaneous valid 0.8.8 and 0.8.9 sources are quarantined as a conflict;
10. an impossible status/cursor/post-task shape is rejected even after legacy integrity recomputation;
11. a valid target is resumed without a second migration;
12. a target with a mismatched asset binding is quarantined.

## Checkpoint G — GitHub Actions evidence

Authoritative successful execution:

```text
migration workflow run: 30740724909
migration job:         91477556949
baseline workflow run: 30740724897
head checked out:       ffc86d6a29ca6888fd7a0749fbee8e04e4420676
```

The generated public assets were previously materialized by `github-actions[bot]` in:

```text
900dbbb509329ea0da8c99968dd95e7b2945c8c1
```

Later report-only commits do not require regenerated assets unless the builder, parent artifacts, bank, config, manifest, or pin module changes.

## Checkpoint H — browser smoke test

Serve the repository over HTTP. Do not use `file://`.

Verify at minimum:

- asset verification completes before any state access;
- a bank/config/manifest mismatch blocks startup without changing local storage;
- 0.8.8 and 0.8.9 unfinished sessions resume at the expected item;
- sealed legacy sessions expose the correct original-version link;
- an invalid or conflicting source shows a blocking message and is not replaced by a fresh session;
- post-migration refresh resumes the 0.8.10 target;
- the final sealed payload includes `asset_binding` and `migration_provenance` when applicable.

## External stop gates

The following are not authorized by this version and require owner/live-environment input:

- live Collector health and POST smoke test;
- live Factory reconstruction with the protected private crosswalk;
- mobile and desktop owner walkthrough;
- production default-entry replacement;
- final custody decision for the private crosswalk.

## Known internal hold

Do not claim multi-tab atomicity. `localStorage` does not provide a compare-and-swap transaction across tabs. Concurrent upgrade arbitration, stale-writer fencing, and restart reconciliation of every `PREPARED` journal interleaving belong to CUBE-REV 0.8.11.

## Promotion rule

0.8.10 may remain an internally certified stacked research PR when checkpoints C–G pass. It must not become the production default until the external stop gates are explicitly executed and the multi-tab migration boundary is addressed or knowingly accepted.

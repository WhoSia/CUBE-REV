# CUBE-REV 0.8.13 Rerun Runbook

## Purpose

This runbook resumes CUBE-REV 0.8.13 after a chat timeout, browser interruption, expired workflow artifact, or partial GitHub connector failure without reconstructing the implementation history from memory.

## Checkpoint A — stack identity

```text
base: cube-rev-0.8.12-active-session-cas
head: cube-rev-0.8.13-native-browser-live-factory
draft pull request: #12
production default entry: unchanged
```

Frozen files that must not occur in the 0.8.13 diff:

```text
collector-config.js
js/collector-client.js
```

## Checkpoint B — required implementation

```text
participant-cognitive-mode-0.8.13.html
js/participant-cognitive-mode-0.8.13.js
js/active-session-cas-0.8.13.js
js/public-asset-verifier-0.8.13.js
js/asset-pins-0.8.13.js
scripts/build_0_8_13_assets.js
scripts/make_synthetic_snapshot_0_8_13.js
scripts/live_collector_probe_0_8_13.mjs
tests/native_multi_window_0.8.13.spec.js
tests/transport_session_bridge_0.8.13.py
tests/factory_reconstruction_0.8.13.py
factory/cognitive_snapshot_adapter_0_8_13.py
cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json
cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json
research/CUBE_REV_0.8.13_ASSET_MANIFEST.json
research/CUBE_REV_0.8.13_LIVE_COLLECTOR_EVIDENCE.json
research/CUBE_REV_0.8.13_VALIDATION_REPORT.md
research/CUBE_REV_0.8.13_DECISION_PACKET.json
```

Temporary materializers, patch scripts, staging chunks, and live-send workflows must not remain in the final tree.

## Checkpoint C — deterministic asset build

From the repository root:

```bash
node scripts/build_0_8_13_assets.js
```

Required marker:

```text
CR0813_ASSET_BUILD_PASS stimuli=28 choices=504 manifest=810847fe11ffcb6c17cb7a87b6951579ada128035f3f4ffc8a281478b3ece506
```

Required committed raw identities:

```text
public bank  c6b522d3060105401feb4773a2860d70853ab8cdf2edba75b72bb5b52bb6d510
public config 44aa314b85d6eacb84d7b0fb02b866c9fb3970824e3c3de54f371dbea92bdeff
manifest      810847fe11ffcb6c17cb7a87b6951579ada128035f3f4ffc8a281478b3ece506
pin module    966642169e0af785ef0a9e2ebb047615b941d636affd03bb08e0c85f0c1a0644
```

A mismatch is a blocking HOLD. Do not manually edit the pin values to match a changed file.

## Checkpoint D — syntax

```bash
node --check scripts/build_0_8_13_assets.js
node --check scripts/make_synthetic_snapshot_0_8_13.js
node --check scripts/live_collector_probe_0_8_13.mjs
node --check js/public-asset-verifier-0.8.13.js
node --check js/participant-cognitive-mode-0.8.13.js
node --check js/active-session-cas-0.8.13.js
node --check tests/native_multi_window_0.8.13.spec.js
python -m py_compile factory/cognitive_snapshot_adapter_0_8_13.py tests/factory_reconstruction_0.8.13.py tests/transport_session_bridge_0.8.13.py
```

Extract the one non-empty inline script from `participant-cognitive-mode-0.8.13.html` and run `node --check` on it.

## Checkpoint E — native browser execution

Install the pinned Playwright test dependency and Chromium:

```bash
npm install --no-save @playwright/test@1.55.0
npx playwright install --with-deps chromium
npx playwright test tests/native_multi_window_0.8.13.spec.js --workers=1 --reporter=line
```

Required markers:

```text
CR0813_NATIVE_MULTI_WINDOW_PASS cursor=2 conflict_count=1 pagehide_persisted=true
CR0813_LEASE_EXPIRY_AMBIGUITY_PASS posts=2 generation=2 status=SUBMITTED bridge=DETERMINISTIC_LEGACY_SESSION_BRIDGE_V1
```

Required delayed-receipt invariants:

- two POSTs;
- one transport session ID;
- one scientific session ID;
- different 24-hex nonces;
- identical payload bytes, SHA-256, and FNV checksum;
- 28 compatibility trials and 28 inner responses;
- terminal receipt set contains `stored` and `duplicate`;
- final lease generation is 2;
- final state is `SUBMITTED`;
- immutable snapshot hash and retry ID do not change.

## Checkpoint F — transport bridge parity

The browser artifact must contain `artifacts/0.8.13/native_snapshot.json`.

```bash
python tests/transport_session_bridge_0.8.13.py
```

Required outcome:

```text
CR0813_TRANSPORT_BRIDGE_PARITY ... "passed":true
```

The outer envelope, `data_submission`, and Python recomputation must agree on:

- transport session ID;
- original scientific session ID;
- `IDENTITY_SESSION_V1` or `DETERMINISTIC_LEGACY_SESSION_BRIDGE_V1`.

The verifier is read-only. It must not assign to envelope fields. The canonical envelope is frozen, while `collectorWorkingCopy()` is mutable and isolated from the canonical envelope.

## Checkpoint G — Factory reconstruction

```bash
node scripts/make_synthetic_snapshot_0_8_13.js artifacts/0.8.13/live_synthetic_snapshot.json
python factory/cognitive_snapshot_adapter_0_8_13.py artifacts/0.8.13/native_snapshot.json --outdir artifacts/0.8.13/native_factory
python factory/cognitive_snapshot_adapter_0_8_13.py artifacts/0.8.13/live_synthetic_snapshot.json --outdir artifacts/0.8.13/synthetic_factory
python tests/factory_reconstruction_0.8.13.py
```

Required markers:

```text
CR0813_FACTORY_RECONSTRUCTION_PASS responses=28 root=collector_compatibility_envelope outputs=5
CR0813_FACTORY_RECONSTRUCTION_PASS responses=28 root=inner_scientific_snapshot outputs=5
CR0813_FACTORY_ADAPTER_TEST_PASS inner_rows=28 wrapper_rows=28 tamper_cases=5 bridge=IDENTITY_SESSION_V1
```

For the native wrapper:

```text
raw SHA-256      57a959fd5d746e615f4e072c580d9d620b37999deaf470265e62af7edf03b40e
inner SHA-256    3601b323d98d8570af7bf9bf58a35611c9519607145e789108b1f2c8f15dbde6
analysis ZIP     42ace938ea1b4ca265240304ef4fe9e2fe68ec2f0db5acb85a459e3b6b0050d6
response rows    28
blocking QC      0
analysis eligible true
```

The five tamper cases must remain rejected.

## Checkpoint H — inherited contracts

```bash
node tests/active_session_cas_0.8.12.test.js
node -r ./js/atomic-migration-commit-authority-0.8.11.js tests/atomic_migration_arbitration_0.8.11.test.js
node tests/cross_version_resume_hash_pin_0.8.10.test.js
node tests/public_bank_minimization_0.8.9.test.js
node tests/immutable_snapshot_contract_0.8.8.test.js
```

Required markers:

```text
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

## Checkpoint I — authoritative CI evidence

Primary executable certification:

```text
head:                   96df4e1e870b1fa41126c5b8b0299d06e43bd517
certification run:      30750150463
certification job:      91502629004
baseline run:           30750150466
result:                 SUCCESS
artifact ID:            8834172208
artifact ZIP SHA-256:   e2ac90081b0136221526e48cef4ed4b10c30bdda16af550252c079863fc37d25
artifact bytes:         48977
```

The artifact upload must contain 22 files, including native browser evidence, delayed receipt evidence, transport parity, raw inputs, Factory outputs, manifests, and both analysis ZIPs.

## Checkpoint J — live Collector evidence

Do not automatically re-run the live probe. The one-time live workflow was removed after success.

Authoritative evidence:

```text
workflow run:           30747246961
collector ID:           CUBE-REV-0712-MAIN
protocol:               receipt-v2
expected version:       0.7.12
file name:              CR-20260802110000-0813a0b0c0d0.json
envelope SHA-256:       6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3
FNV checksum:           f795cd8e
bytes:                  21227
inner snapshot SHA-256: 446ab20ec570140f810bcbe91660b089585f1416db5b29852f7bf6946881e2ba
receipt A:              CR0712-RCP-1C74B563
receipt B:              CR0712-RCP-953ECF13
terminal statuses:      duplicate, duplicate
```

The synthetic session is excluded from human-cohort analysis. A new live probe requires explicit justification because repeated valid nonces would create additional receipt traffic even though dedup should converge.

## Checkpoint K — stored raw custody HOLD

Search the connected Drive for:

```text
CR-20260802110000-0813a0b0c0d0.json
0813a0b0c0d0
```

If the exact raw file becomes available:

1. download it without reserialization;
2. compute raw SHA-256 and compare with the recorded envelope identity when applicable;
3. run `cognitive_snapshot_adapter_0_8_13.py` directly on it;
4. require 28 rows, zero blocking QC, matching transport/scientific identity, and exact compatibility projection;
5. update the decision from `HOLD_LIVE_STORED_RAW_FACTORY_RETRIEVAL` to PASS only after this execution.

Current connected Drive search returned no exact result. Do not infer raw custody from the receipt alone.

## External stop gates

0.8.13 does not authorize:

- production `index.html` replacement;
- merging the stacked PR chain;
- human participant rollout;
- mobile or cross-browser deployment claims;
- removal of the synthetic exclusion marker;
- modification of the Collector endpoint or client.

## Promotion rule

0.8.13 is complete as a research version when checkpoints C–J pass and the stored-raw custody limitation remains explicitly marked. Production promotion remains `NO_GO` until an owner-controlled staging and device walkthrough stage resolves the remaining custody and deployment gates.

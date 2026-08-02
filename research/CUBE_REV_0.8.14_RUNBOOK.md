# CUBE-REV 0.8.14 Runbook

## Purpose

This runbook reproduces the automated portions of:

**CUBE-REV 0.8.14 — Stored-raw Custody Replay, Cross-device Browser Matrix & Controlled Staging Cutover Gate**

It also defines the exact external evidence required to clear the three remaining promotion blocks.

## Safety boundary

The runbook must not:

- modify production `index.html`;
- modify `collector-config.js`;
- modify `js/collector-client.js`;
- send additional live synthetic submissions unless separately authorized;
- infer stored-byte equality from a `duplicate` receipt;
- enable Firefox or WebKit active execution without new repeated evidence;
- merge PR #12 or PR #13;
- deploy the staging ZIP automatically.

The 0.8.13 erratum is authoritative for all live-Collector payload and receipt claims.

## Fixed identities

```text
branch
cube-rev-0.8.14-custody-device-staging

parent
cube-rev-0.8.13-native-browser-live-factory

parent rollback target
6c127f86704b29ed4d884acc19a28407578753c2

certified executable head
b5712e1d30f2e0b0cc0b411fdca811d4c6158992

certification workflow
30753219920

baseline workflow
30753219950

evidence artifact
8835133893
```

## Automated rerun

### 1. Checkout

```bash
git fetch origin
git checkout cube-rev-0.8.14-custody-device-staging
git reset --hard origin/cube-rev-0.8.14-custody-device-staging
```

### 2. Verify protected files

```bash
git fetch origin cube-rev-0.8.13-native-browser-live-factory

git diff --name-only \
  origin/cube-rev-0.8.13-native-browser-live-factory...HEAD \
  | grep -E '^(index\.html|collector-config\.js|js/collector-client\.js)$'
```

Expected: no output.

Any output is a blocking failure.

### 3. Build the deterministic staging route

```bash
mkdir -p artifacts/0.8.14
python scripts/build_participant_route_0_8_14.py
```

Expected marker:

```text
CR0814_PARTICIPANT_ROUTE_BUILD_PASS ... active=CHROMIUM_ONLY firefox=FAIL_CLOSED webkit=FAIL_CLOSED
```

Required files:

```text
participant-cognitive-mode-0.8.14.html
unsupported-browser-0.8.14.html
artifacts/0.8.14/participant_route_build_manifest.json
```

The generated route is a staging candidate only. Do not copy it over the repository's production `index.html` outside a separately authorized deployment ceremony.

### 4. Reconstruct the archival live submission

```bash
node scripts/make_synthetic_snapshot_0_8_13.js \
  artifacts/0.8.14/live_synthetic_snapshot.json

node scripts/reconstruct_live_envelope_0_8_14.mjs \
  artifacts/0.8.14/live_synthetic_snapshot.json \
  artifacts/0.8.14/archival_live_envelope.json \
  artifacts/0.8.14/archival_reconstruction_evidence.json \
  . archival-live-head
```

Required identity:

```text
bytes    16217
sha256   6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9
fnv1a32  c8cda746
```

Expected marker:

```text
CR0814_RUNTIME_PINNED_RECONSTRUCTION_PASS class=archival-live-head
```

### 5. Observe the final 0.8.13 runtime candidate

```bash
node scripts/reconstruct_live_envelope_0_8_14.mjs \
  artifacts/0.8.14/live_synthetic_snapshot.json \
  artifacts/0.8.14/final_runtime_envelope.json \
  artifacts/0.8.14/final_reconstruction_evidence.json \
  . final-0.8.13-head
```

Observed certified identity:

```text
bytes    16503
sha256   9763af8e0c6e9de29728d5fedd4290c8bf3b8bb086bb14d014ea482d0397447a
fnv1a32  771bf949
```

This is an observation of the final runtime, not evidence of the Drive-stored file.

### 6. Audit live-evidence lineage

```bash
python scripts/audit_live_evidence_lineage_0_8_14.py
```

Expected marker:

```text
CR0814_LIVE_EVIDENCE_LINEAGE_AUDIT_PASS inconsistency=true ... erratum_required=true
```

Required governing document:

```text
research/CUBE_REV_0.8.13_ERRATUM_FROM_0.8.14.md
```

Do not replace the archival values with the later 0.8.13 ledger values.

### 7. Evaluate exact stored-raw custody

Without an owner-authorized raw export:

```bash
python scripts/custody_replay_0_8_14.py
```

Expected marker:

```text
CR0814_STORED_RAW_CUSTODY_HOLD direct_raw=false ...
```

A HOLD is the correct result when the raw file is absent.

### 8. Build the provenance-preserving archival Factory input

```bash
python factory/archival_live_bridge_0_8_14.py \
  artifacts/0.8.14/archival_live_envelope.json \
  --derived artifacts/0.8.14/archival_live_factory_input.json \
  --report artifacts/0.8.14/archival_live_factory_bridge.json
```

Expected marker:

```text
CR0814_ARCHIVAL_FACTORY_BRIDGE_PASS ... scientific_unchanged=true
```

Required identities:

```text
source SHA-256
6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9

derived SHA-256
5627d14d7ca654f99b91cefcbeb6f6f31a8588a9809b819653fb69c437e9d0c0

scientific snapshot SHA-256 before and after
5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83
```

Then run the final Factory:

```bash
python factory/cognitive_snapshot_adapter_0_8_13.py \
  artifacts/0.8.14/archival_live_factory_input.json \
  --outdir artifacts/0.8.14/archival_live_factory

python factory/cognitive_snapshot_adapter_0_8_13.py \
  artifacts/0.8.14/final_runtime_envelope.json \
  --outdir artifacts/0.8.14/final_runtime_factory
```

Both must reconstruct 28 rows with no blocking QC finding.

### 9. Install browser engines

```bash
npm install --no-save @playwright/test@1.55.0
npx playwright install --with-deps chromium firefox webkit
```

### 10. Execute the browser policy matrix

```bash
node tests/cross_device_browser_matrix_0.8.14.mjs
```

Expected final marker:

```text
CR0814_CROSS_DEVICE_POLICY_MATRIX_PASS active_cells=2 fail_closed_cells=4 active_races=8 ... active_policy=CHROMIUM_ONLY
```

Required policy:

| Profile | Required result |
|---|---|
| Chromium desktop | four repeated active races pass |
| Chromium Pixel 7 emulation | four repeated active races pass |
| Firefox desktop | fail closed before runtime boot |
| Firefox compact viewport | fail closed before runtime boot |
| WebKit desktop | fail closed before runtime boot |
| WebKit iPhone emulation | fail closed before runtime boot |

For each fail-closed profile:

```text
runtime test hooks absent
begin control absent
cube-rev storage keys = 0
state mutation authorized = false
```

The test also repeats six parent-route diagnostic races in Firefox, desktop WebKit, and iPhone WebKit emulation. These diagnostics are evidence for the support policy; they are not active staging sessions.

### 11. Re-run inherited contracts

```bash
npx playwright test tests/native_multi_window_0.8.13.spec.js \
  --workers=1 --reporter=line

node tests/active_session_cas_0.8.12.test.js
node -r ./js/atomic-migration-commit-authority-0.8.11.js \
  tests/atomic_migration_arbitration_0.8.11.test.js
node tests/cross_version_resume_hash_pin_0.8.10.test.js
node tests/public_bank_minimization_0.8.9.test.js
node tests/immutable_snapshot_contract_0.8.8.test.js
```

Required markers:

```text
CR0813_NATIVE_MULTI_WINDOW_PASS
CR0813_LEASE_EXPIRY_AMBIGUITY_PASS
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

### 12. Build the deterministic staging candidate

```bash
python scripts/build_staging_candidate_0_8_14.py
```

Certified candidate:

```text
file count        22
fingerprint       0b8ae0679a6033b8cd4862ef6de81fe2f1ee8fde8b7bfd1ff3dee7616722fc32
ZIP SHA-256       80db6740754297b51b87c6542a4ef6d5f3958f5da2c0e4ce65989a1768c78520
ZIP bytes         68054
```

The ZIP packages the generated staging route as its internal `index.html`; it does not modify the repository production entry.

### 13. Evaluate cutover

```bash
python scripts/evaluate_cutover_gate_0_8_14.py
cat artifacts/0.8.14/cutover_gate.json
```

Expected result while external gates remain unresolved:

```text
CONTROLLED_STAGING_CANDIDATE_PASS_PRODUCTION_CUTOVER_NO_GO
```

Required blocking gates:

```text
exact_stored_raw_custody_replay
physical_device_walkthrough
owner_acceptance_walkthrough
```

Any automated `GO` before all three are satisfied is a certification failure.

## External Gate A — Exact stored raw export

This gate requires owner-authorized access to the Collector-owned Drive file:

```text
CR-20260802110000-0813a0b0c0d0.json
```

Place the unmodified export at:

```text
custody/CR-20260802110000-0813a0b0c0d0.json
```

Do not rename and reserialize the JSON. Preserve the exact downloaded bytes.

Run:

```bash
python scripts/custody_replay_0_8_14.py \
  --raw custody/CR-20260802110000-0813a0b0c0d0.json
```

The script will:

- hash the exact raw bytes;
- compare them with all known candidate identities;
- retain a previously unknown identity rather than forcing a match;
- run Factory on the exact raw file;
- write `artifacts/0.8.14/custody/custody_replay_report.json`.

A raw identity that matches none of the three candidates is not automatically invalid. It may show that an earlier, currently unrecovered submission created the file. Preserve and report it.

## External Gate B — Physical Chromium-family walkthrough

At minimum, use:

- one desktop Chrome or Edge installation;
- one Android Chrome or Edge installation.

The walkthrough must use a separately authorized staging URL built from the candidate, not production `index.html`.

Required checks:

1. visible version is CUBE-REV 0.8.14;
2. staging warning is visible;
3. 28-response flow completes;
4. reload resumes without response loss;
5. two-window same-position race yields one winner and conflict evidence;
6. pagehide/background transition preserves existing response bytes;
7. retry after an ambiguous submission does not create a second scientific snapshot;
8. no production route or Collector source was modified;
9. evidence includes browser version, OS version, device model, UTC/KST timestamps, screenshots, and exported local evidence JSON.

Firefox and Safari/WebKit must remain blocked during this version. Testing them physically may inform a later repair version but does not authorize 0.8.14 activation.

## External Gate C — Owner acceptance

Owner acceptance is a distinct decision after evidence review. It must state:

```text
- exact stored-raw custody result reviewed
- physical Chromium desktop walkthrough reviewed
- physical Android Chromium walkthrough reviewed
- Firefox/WebKit fail-closed policy accepted
- 0.8.13 erratum accepted as governing live evidence
- rollback plan reviewed
- staging-only deployment scope accepted
- production cutover remains separately authorized
```

Acceptance must not be inferred from silence or from approval to conduct research. It requires an explicit acceptance record for the deployment ceremony.

## Rollback

The current rollback target is:

```text
6c127f86704b29ed4d884acc19a28407578753c2
```

For artifact-only staging, rollback means removing the staging route or restoring the parent bytes. Production is already untouched.

Do not use a rollback action that deletes raw evidence, errata, audit reports, or custody artifacts.

## Stop conditions

Stop and issue `NO_GO` when any of the following occurs:

- protected production or Collector files differ;
- archival reconstruction no longer matches its exact fingerprint;
- scientific snapshot changes during archival bridging;
- a Chromium active race returns dual `RESPONSE_APPLIED`;
- a blocked engine boots the runtime or creates state;
- inherited contracts regress;
- staging bundle is nondeterministic;
- exact raw bytes are modified before hashing;
- an unresolved custody, physical-device, or owner-acceptance gate is treated as passed.

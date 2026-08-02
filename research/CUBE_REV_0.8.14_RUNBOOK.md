# CUBE-REV 0.8.14 Runbook

## Purpose

This runbook reproduces the automated portions of:

**CUBE-REV 0.8.14 — Stored-raw Custody Replay, Cross-device Browser Matrix & Controlled Staging Cutover Gate**

It also defines the evidence required to clear the three remaining promotion blocks.

## Safety boundary

Do not:

- modify production `index.html`;
- modify `collector-config.js` or `js/collector-client.js`;
- send another live synthetic submission without separate authorization;
- infer stored-byte equality from a `duplicate` receipt;
- enable Firefox or WebKit active execution without new repeated evidence;
- use the parent test's fixed 1,400ms wait as the 0.8.14 lease Gate;
- merge PR #12 or PR #13;
- deploy the staging ZIP automatically.

The 0.8.13 erratum governs all live-Collector payload and receipt claims.

## Fixed identities

```text
branch
cube-rev-0.8.14-custody-device-staging

parent
cube-rev-0.8.13-native-browser-live-factory

rollback target
6c127f86704b29ed4d884acc19a28407578753c2

certified executable head
25371c6479e074d3c7d0ad3501beffeb08f28cfb

certification workflow
30754439979

certification job
91514086682

baseline workflow
30754439978

evidence artifact
8835501173

artifact ZIP SHA-256
c81b46125916aadb9be55085a68bedf70a3bfbfbb5991e85d54096061660e093
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

Expected: no output. Any output is blocking.

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

The generated route is staging-only. Do not copy it over production `index.html` outside a separately authorized ceremony.

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

### 5. Observe the final 0.8.13 runtime candidate

```bash
node scripts/reconstruct_live_envelope_0_8_14.mjs \
  artifacts/0.8.14/live_synthetic_snapshot.json \
  artifacts/0.8.14/final_runtime_envelope.json \
  artifacts/0.8.14/final_reconstruction_evidence.json \
  . final-0.8.13-head
```

Certified observation:

```text
bytes    16503
sha256   9763af8e0c6e9de29728d5fedd4290c8bf3b8bb086bb14d014ea482d0397447a
fnv1a32  771bf949
```

This is not evidence of the Drive-stored file.

### 6. Audit live-evidence lineage

```bash
python scripts/audit_live_evidence_lineage_0_8_14.py
```

Expected:

```text
CR0814_LIVE_EVIDENCE_LINEAGE_AUDIT_PASS inconsistency=true ... erratum_required=true
```

Required governing document:

```text
research/CUBE_REV_0.8.13_ERRATUM_FROM_0.8.14.md
```

### 7. Evaluate exact stored-raw custody

Without an owner-authorized export:

```bash
python scripts/custody_replay_0_8_14.py
```

Expected:

```text
CR0814_STORED_RAW_CUSTODY_HOLD direct_raw=false ...
```

A HOLD is correct when the raw file is absent.

### 8. Build the archival Factory bridge

```bash
python factory/archival_live_bridge_0_8_14.py \
  artifacts/0.8.14/archival_live_envelope.json \
  --derived artifacts/0.8.14/archival_live_factory_input.json \
  --report artifacts/0.8.14/archival_live_factory_bridge.json
```

Expected:

```text
CR0814_ARCHIVAL_FACTORY_BRIDGE_PASS ... scientific_unchanged=true
```

Required identities:

```text
source SHA-256
6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9

derived SHA-256
5627d14d7ca654f99b91cefcbeb6f6f31a8588a9809b819653fb69c437e9d0c0

scientific snapshot SHA-256
5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83
```

Then run Factory on both known candidates:

```bash
python factory/cognitive_snapshot_adapter_0_8_13.py \
  artifacts/0.8.14/archival_live_factory_input.json \
  --outdir artifacts/0.8.14/archival_live_factory

python factory/cognitive_snapshot_adapter_0_8_13.py \
  artifacts/0.8.14/final_runtime_envelope.json \
  --outdir artifacts/0.8.14/final_runtime_factory
```

Both must reconstruct 28 rows with zero blocking QC.

### 9. Install browser engines

```bash
npm install --no-save @playwright/test@1.55.0
npx playwright install --with-deps chromium firefox webkit
```

### 10. Execute the browser policy matrix

```bash
node tests/cross_device_browser_matrix_0.8.14.mjs
```

Expected:

```text
CR0814_CROSS_DEVICE_POLICY_MATRIX_PASS active_cells=2 fail_closed_cells=4 active_races=8 ... active_policy=CHROMIUM_ONLY
```

Required policy:

| Profile | Required result |
|---|---|
| Chromium desktop | four active races pass |
| Chromium Pixel 7 emulation | four active races pass |
| Firefox desktop | fail closed before runtime boot |
| Firefox compact viewport | fail closed before runtime boot |
| WebKit desktop | fail closed before runtime boot |
| WebKit iPhone emulation | fail closed before runtime boot |

Each blocked profile must have no runtime hook, no begin control, zero `cube-rev*` storage keys, and `state_mutation_authorized=false`.

### 11. Re-run parent serialization and dynamic persisted-expiry takeover

Run only the parent serialization scenario from the 0.8.13 file:

```bash
npx playwright test tests/native_multi_window_0.8.13.spec.js \
  --grep 'native Chromium Web Locks serialize two pages without response loss' \
  --workers=1 --reporter=line
```

Then run the final 0.8.14 lease Gate:

```bash
npx playwright test tests/lease_expiry_dynamic_0.8.14.spec.js \
  --workers=1 --reporter=line
```

The dynamic suite must:

1. read the persisted `submission_control.lease_expires_at`;
2. wait until that timestamp plus 250ms;
3. open a fresh second page;
4. repeat in four fresh browser contexts;
5. produce exactly eight POSTs;
6. keep each iteration's payload pair byte-, SHA-, checksum-, and session-identical;
7. finish every iteration at generation 2 and `SUBMITTED`;
8. preserve 28 responses and the snapshot/retry identity.

Required marker:

```text
CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false
```

Required artifact:

```text
artifacts/0.8.14/dynamic_lease_expiry_evidence.json
```

Expected margins in the certified run were 252, 252, 252, and 253ms. Exact margins may vary slightly, but every second page must open after persisted expiry. The delayed generation-1 owner may log `STALE_SUBMISSION_LEASE` after generation 2 confirms; this is expected fencing.

Do not use a successful rerun of the old fixed-delay scenario as a substitute.

### 12. Re-run inherited state and migration contracts

```bash
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
CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

### 13. Build the staging candidate

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

The ZIP contains the generated staging route as its internal `index.html`; repository production `index.html` remains untouched.

### 14. Evaluate cutover

```bash
python scripts/evaluate_cutover_gate_0_8_14.py
cat artifacts/0.8.14/cutover_gate.json
```

Expected:

```text
CONTROLLED_STAGING_CANDIDATE_PASS_PRODUCTION_CUTOVER_NO_GO
```

Required automated lease field:

```text
dynamic_persisted_lease_expiry_repetition = true
fixed_delay_lease_test_used_for_gate = false
```

Required blockers:

```text
exact_stored_raw_custody_replay
physical_device_walkthrough
owner_acceptance_walkthrough
```

Any automated `GO` before all three are satisfied is a certification failure.

## External Gate A — Exact stored raw export

Required file:

```text
CR-20260802110000-0813a0b0c0d0.json
```

Place the unmodified export at:

```text
custody/CR-20260802110000-0813a0b0c0d0.json
```

Do not rename, pretty-print, or reserialize it. Run:

```bash
python scripts/custody_replay_0_8_14.py \
  --raw custody/CR-20260802110000-0813a0b0c0d0.json
```

The script hashes exact bytes, compares all known candidates, retains an unknown identity rather than forcing a match, runs Factory, and writes the custody report.

## External Gate B — Physical Chromium walkthrough

Minimum:

- one desktop Chrome or Edge installation;
- one Android Chrome or Edge installation.

Use a separately authorized staging URL, not production.

Required checks:

1. visible version and staging warning;
2. 28-response completion;
3. reload resume without loss;
4. two-window one-winner/conflict behavior;
5. pagehide/background preservation;
6. ambiguous retry without a second scientific snapshot;
7. browser/OS/device/timestamps/screenshots and exported evidence.

Firefox and WebKit remain blocked in 0.8.14.

## External Gate C — Owner acceptance

Acceptance must explicitly confirm review of:

- exact stored-raw result;
- physical desktop Chromium walkthrough;
- physical Android Chromium walkthrough;
- Firefox/WebKit fail-closed policy;
- 0.8.13 erratum;
- dynamic persisted-expiry lease evidence;
- rollback plan;
- staging-only scope;
- separate production-cutover authority.

Research approval or silence is not deployment acceptance.

## Rollback

Rollback target:

```text
6c127f86704b29ed4d884acc19a28407578753c2
```

For artifact-only staging, remove the staging route or restore parent bytes. Do not delete raw evidence, errata, audit reports, or custody artifacts.

## Stop conditions

Stop with `NO_GO` if:

- a protected production or Collector file changes;
- archival reconstruction misses its fingerprint;
- the scientific snapshot changes during bridging;
- a Chromium race returns dual `RESPONSE_APPLIED`;
- a blocked engine boots runtime or creates state;
- the dynamic lease suite uses a fixed delay, misses any of four iterations, or fails to reach generation 2;
- inherited contracts regress;
- the staging bundle is nondeterministic;
- raw bytes are modified before hashing;
- an unresolved custody, physical-device, or owner-acceptance Gate is treated as passed.

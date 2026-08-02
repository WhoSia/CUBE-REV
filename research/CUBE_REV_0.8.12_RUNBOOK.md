# CUBE-REV 0.8.12 Certification Runbook

## Purpose

This runbook reproduces the executable certification for:

**CUBE-REV 0.8.12 — Active-session Multi-tab Write Serialization, Revision CAS & Response-loss Prevention Certification**

It also defines the still-unexecuted owner walkthrough for native multi-window browser behavior and the later live Collector/Factory gate.

## Fixed identities

```text
repository: WhoSia/CUBE-REV
branch: cube-rev-0.8.12-active-session-cas
certified materialized head: 1d308b4c7038e9af2ffcf0928cc94df44a45237b
parent branch: cube-rev-0.8.11-atomic-migration-arbitration
parent head: 48a22dbf14d210dbf833fb0a8d597c9d32c5c91e
participant route: participant-cognitive-mode-0.8.12.html
active storage key: cube-rev-cognitive-mode-0812-v1
active write lock: cube-rev-session-write-0812-exclusive-v1
collector contract: 0.7.12
```

The branch may contain later documentation-only commits. Before attributing an executable result to another head, rerun the full workflow and record the new head and run IDs.

## Required environment

- Git 2.40 or newer;
- Node.js 22;
- a clean repository checkout;
- no changes to `collector-config.js` or `js/collector-client.js`;
- for native browser walkthrough, a secure same-origin HTTP origin with Web Locks and `localStorage` enabled.

## Repository checkout

```bash
git clone https://github.com/WhoSia/CUBE-REV.git
cd CUBE-REV
git fetch origin cube-rev-0.8.12-active-session-cas
git checkout --detach 1d308b4c7038e9af2ffcf0928cc94df44a45237b
git status --short
```

Expected result:

```text
working tree clean
```

## Deterministic asset rebuild

```bash
node scripts/build_0_8_12_assets.js
```

Required marker:

```text
CR0812_ASSET_BUILD_PASS stimuli=28 choices=504
```

The builder must recreate:

```text
cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json
cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json
research/CUBE_REV_0.8.12_ASSET_MANIFEST.json
js/asset-pins-0.8.12.js
```

After rebuilding, confirm that no generated file differs from the certified tree:

```bash
git diff --exit-code -- \
  cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json \
  cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json \
  research/CUBE_REV_0.8.12_ASSET_MANIFEST.json \
  js/asset-pins-0.8.12.js
```

## Active-session CAS suite

```bash
node tests/active_session_cas_0.8.12.test.js
```

Required marker:

```text
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
```

Any lower number, uncaught exception, timeout, or missing marker is a blocking failure.

## Inherited contract suite

```bash
node -r ./js/atomic-migration-commit-authority-0.8.11.js \
  tests/atomic_migration_arbitration_0.8.11.test.js
node tests/cross_version_resume_hash_pin_0.8.10.test.js
node tests/public_bank_minimization_0.8.9.test.js
node tests/immutable_snapshot_contract_0.8.8.test.js
```

Required markers:

```text
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

## Syntax checks

```bash
node --check scripts/build_0_8_12_assets.js
node --check js/public-asset-verifier-0.8.12.js
node --check js/participant-cognitive-mode-0.8.12.js
node --check js/active-session-cas-0.8.12.js
node --check tests/active_session_cas_0.8.12.test.js
```

Extract and check the participant page's only inline script:

```bash
node - <<'NODE'
const fs=require('fs');
const html=fs.readFileSync('participant-cognitive-mode-0.8.12.html','utf8');
const blocks=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)]
  .map(x=>x[1]).filter(x=>x.trim());
if(blocks.length!==1)throw new Error(`INLINE_SCRIPT_COUNT:${blocks.length}`);
for(const required of [
  'active-session-cas-0.8.12.js',
  'participant-cognitive-mode-0.8.12.js',
  'atomic-migration-commit-authority-0.8.11.js'
])if(!html.includes(required))throw new Error(`REQUIRED_SCRIPT_MISSING:${required}`);
fs.writeFileSync('/tmp/cube-rev-0812-inline.js',blocks[0]);
NODE
node --check /tmp/cube-rev-0812-inline.js
```

## Asset identity verification

Expected canonical SHA-256 values:

```text
manifest: c9abbf5c1057bb0e02795fc0d3ab1095c9ce115943b1f89cb825ac8a9ed35af6
public bank: fc76841350cd8937e576c701995ff64bcfbc02f6f7b50977b8946f8299a712a8
public config: 1d04467c3ad2390f2e9784973bd026c1b77b8a72919fedd09070ff048b6d0701
parent 0.8.11 manifest: ef6a767d079fcf63c24f9cab4032ae2175beac3345ce91f89dc72d01b6155d7f
private crosswalk: 90c54b51052fc27c436d8701797e5b2aa95e19ec28a7f63bbd50db41192748f0
```

Verify canonical parsed-object hashes:

```bash
node - <<'NODE'
const fs=require('fs'),crypto=require('crypto');
function h(path){
  const x=JSON.parse(fs.readFileSync(path,'utf8'));
  return crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');
}
const expected={
  'research/CUBE_REV_0.8.12_ASSET_MANIFEST.json':'c9abbf5c1057bb0e02795fc0d3ab1095c9ce115943b1f89cb825ac8a9ed35af6',
  'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json':'fc76841350cd8937e576c701995ff64bcfbc02f6f7b50977b8946f8299a712a8',
  'cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json':'1d04467c3ad2390f2e9784973bd026c1b77b8a72919fedd09070ff048b6d0701'
};
for(const [p,e] of Object.entries(expected)){
  const a=h(p);console.log(a,p);if(a!==e)throw new Error(`HASH_MISMATCH:${p}`);
}
NODE
```

Expected raw generated-file SHA-256 values:

```text
86a4cd5c3bb6c261ee9b27957521aaa43b56858f9a59ae5502533e2b863beac2  cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json
4ade0ebc0e2b197ad32bbe908fd9eed5af3dd1b7e0b980d89e6e9478d57d2d3  cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json
325ea5c22388d60aca2d967ae0d275c62764e77f00d15f541b8af1809f21954f  js/asset-pins-0.8.12.js
accbb491d1556584ed72e9768d73535159c709695411c9ae33db7d83a4769a37  research/CUBE_REV_0.8.12_ASSET_MANIFEST.json
```

Verify with:

```bash
sha256sum \
  cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json \
  cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json \
  js/asset-pins-0.8.12.js \
  research/CUBE_REV_0.8.12_ASSET_MANIFEST.json
```

## Participant minimization check

```bash
! grep -E '"(state_id|rotation_id|face_map|choice_canonical|canonical_move|pair_id|member_id|probe_name|diagnostic_class|branch_count|branch_level|decision_class|distance)"[[:space:]]*:' \
  cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json
```

Verify active-session policy identities:

```bash
grep -F '"active_write_lock_required":true' cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json
grep -F '"revision_policy":"STRICT_MONOTONIC_INCREMENT_BY_ONE_V1"' cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json
grep -F '"submission_policy":"LEASE_TOKEN_SINGLE_NETWORK_OWNER_V1"' cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json
```

## Frozen Collector check

```bash
git fetch origin cube-rev-0.8.11-atomic-migration-arbitration
git diff --name-only \
  origin/cube-rev-0.8.11-atomic-migration-arbitration...HEAD
```

The output must not contain:

```text
collector-config.js
js/collector-client.js
```

A changed Collector file invalidates the 0.8.12 certification scope and requires a separate Collector-contract version and end-to-end recertification.

## GitHub Actions evidence

Final executable run:

```text
workflow run: 30744215283
job: 91486924237
baseline run: 30744215295
conclusion: success
```

Final generated-asset artifact:

```text
artifact ID: 8832320785
name: cube-rev-0.8.12-verified-assets
size: 12368 bytes
ZIP SHA-256: e610874e978c8955f1fa3d169943f4792bcd29168e5eca754cad400b2324f2dd
```

The artifact expires after seven days. The Git tree and recorded canonical/raw hashes remain the durable evidence after expiry.

# Native browser multi-window walkthrough

## Status

This section is a required future owner-observed procedure. It was not executed during 0.8.12 and must not be reported as passed until completed against an exact deployed commit.

## Preparation

1. Serve the exact branch or immutable deployment over HTTPS or localhost.
2. Record browser name and full version, OS version, device, deployment URL, Git commit SHA, and local time.
3. Open developer tools in both windows.
4. Clear only the CUBE-REV test origin's storage before the fresh-session case.
5. Preserve screenshots or exported storage evidence for every blocking anomaly.
6. Do not use production participant data for this walkthrough.

## Case A — concurrent initialization

1. Open `participant-cognitive-mode-0.8.12.html` in Window A and Window B.
2. Press start in both as close together as possible.
3. Verify both windows converge to the same session ID, sequence, cursor, and latest revision.
4. Verify only one 0.8.12 target is present.
5. Verify no replacement 0.8.11 source was created or modified.

Pass condition:

```text
one 0.8.12 lineage; no duplicate session; revision remains valid
```

## Case B — different responses to the same trial

1. Pause both windows on the same cursor and revision.
2. In Window A choose one move.
3. In Window B choose a different move.
4. Confirm both nearly simultaneously.
5. Inspect the final stored state and conflict journal.

Pass conditions:

- cursor advances exactly once;
- one response is stored at that position;
- the other attempt cannot overwrite it;
- one conflict-evidence record contains the losing attempted response;
- both windows eventually display the same next cursor and latest revision.

## Case C — response versus telemetry race

1. Put both windows on the same trial.
2. Hide or background Window B to generate visibility telemetry.
3. Confirm a response in Window A during the telemetry transition.
4. Return to Window B.

Pass conditions:

- the response survives;
- the telemetry event survives;
- cursor advances exactly once;
- state revision increases once per committed operation;
- no response array is replaced by an older copy.

## Case D — concurrent telemetry

1. Generate distinct visibility or lifecycle events in both windows from the same displayed revision.
2. Reopen both windows and inspect the latest state.

Pass conditions:

- both event IDs are present exactly once;
- responses and cursor are unchanged;
- two successful events correspond to two serialized revision increments.

## Case E — post-task race

1. Complete all 28 trials.
2. Keep both windows open at the post-task screen.
3. Enter different post-task answers.
4. Submit both nearly simultaneously.

Pass conditions:

- only one scientific post-task value becomes authoritative;
- the stale post-task cannot overwrite the winner;
- session moves to `READY_TO_SUBMIT` once;
- no response or cursor changes.

The UI may present a blocking or refresh result to the losing window. Silent overwrite is a failure.

## Case F — concurrent snapshot sealing

1. Reach `READY_TO_SUBMIT` in both windows.
2. Trigger submission in both windows.
3. Inspect `submission_snapshot`, `submission_snapshot_hash`, `snapshot_sealed_at`, and retry ID.

Pass conditions:

- one immutable snapshot is sealed;
- repeated sealing is idempotent;
- both windows reference the same snapshot hash and retry ID;
- no response or post-task field changes after sealing.

## Case G — concurrent submission lease

1. Delay the Collector endpoint or use a controlled non-production test endpoint.
2. Trigger submission in both windows.
3. Inspect lease token, owner, generation, expiry, and attempt count.

Pass conditions:

- one window owns the active lease;
- the other receives an in-flight state and does not start a second immediate request;
- only the active lease token can merge Collector metadata or confirm submission;
- a foreign token is rejected without revision mutation.

## Case H — owner closes before completion

1. Let Window A claim a submission lease.
2. Close or terminate Window A before receipt confirmation.
3. Before lease expiry, try from Window B.
4. After lease expiry, retry from Window B.

Expected behavior:

- before expiry, Window B does not become owner;
- after expiry, Window B may claim generation `g + 1`;
- snapshot hash and retry ID remain unchanged;
- old lease token can no longer update local state.

This case does not prove that Window A's already-issued remote request was cancelled. Record server receipts to determine whether both network requests completed.

## Case I — pagehide durability observation

1. Generate a known current revision.
2. Close a window immediately after a pagehide-producing action.
3. Reopen the route and inspect whether the event was committed.
4. Repeat with normal close, reload, browser process termination, mobile backgrounding if available, and OS sleep.

Interpretation:

- a missing pagehide event does not permit loss of a response or cursor rollback;
- reliable pagehide telemetry itself remains HOLD unless the event is consistently durable under the tested conditions;
- never claim universal durability from one browser/device run.

## Case J — storage-event convergence

1. Keep both windows visible.
2. Commit operations alternately in A and B.
3. Confirm the non-writing window receives and adopts only higher valid revisions.

Pass conditions:

- revision never decreases in either window;
- invalid or lower storage events are ignored;
- both windows converge to the same current state after activity stops.

# Live Collector gate

## Prerequisites

- explicit owner approval for the test endpoint;
- non-production test participant/session identity;
- exact deployed 0.8.12 commit recorded;
- receipt-v2 Collector endpoint and deployment version recorded;
- ability to inspect the received raw payload and receipt.

## Required cases

1. One normal snapshot submission.
2. Network interruption followed by retry with the same retry ID.
3. Delayed first request longer than 120 seconds, followed by lease takeover and second retry.
4. First request completing after the second request has begun.
5. Duplicate receipt or already-stored response.
6. Client close immediately after POST but before local confirmation.

Required evidence:

- number of actual HTTP attempts;
- number of Collector rows or stored payloads;
- receipt codes and checksums;
- whether duplicate attempts converge to one scientific payload identity;
- exact retry ID and snapshot hash;
- final local status and receipt state.

Promotion requires evidence that repeated attempts cannot create analytically distinct scientific submissions for one immutable snapshot.

# Live Factory gate

For every Collector payload generated by the live gate:

1. Import the exact raw payload through the actual Factory path.
2. Verify `CUBE-REV 0.8.12` and the cognitive-mode schema are recognized.
3. Verify all 28 opaque responses are reconstructed in order.
4. Verify session, sequence, snapshot hash, asset binding, and retry identity remain available.
5. Verify auxiliary transmission metadata is not treated as scientific response content.
6. Verify duplicate retries collapse to one scientific submission identity or are explicitly linked as retries.
7. Verify no condition identity is inferred solely from a display-version string.

Any missing response, changed order, split retry identity, or accidental interpretation of conflict/Collector metadata as participant response is a blocking Factory failure.

# Promotion rules

## Internal executable promotion

Already satisfied for the deterministic simulation scope:

```text
PASS-ACTIVE-SESSION-REVISION-CAS
PASS-RESPONSE-LOSS-PREVENTION-MATRIX
```

## Browser promotion

Requires owner-observed native cases A–J with recorded environment and evidence. A browser-specific pass must name the browser and version; it is not a universal browser certification.

## End-to-end promotion

Requires live Collector and Factory evidence, including the lease-expiry ambiguity case.

Until both browser and end-to-end gates pass:

```text
DEFAULT-CUTOVER-NO_GO
```

Production `index.html` and the frozen Collector must remain unchanged.

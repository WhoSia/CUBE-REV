# CUBE-REV 0.8.12 Validation Report

## Official title

**CUBE-REV 0.8.12 — Active-session Multi-tab Write Serialization, Revision CAS & Response-loss Prevention Certification**

## Official decision

> **PASS-ACTIVE-SESSION-REVISION-CAS / PASS-MULTI-TAB-RESPONSE-SERIALIZATION-SIMULATION / PASS-STALE-SCIENTIFIC-WRITE-REJECTION / PASS-TELEMETRY-MERGE-ON-LATEST / PASS-RESPONSE-CONFLICT-EVIDENCE / PASS-IMMUTABLE-SNAPSHOT-CONTINUITY / PASS-SUBMISSION-LEASE-ARBITRATION-SIMULATION / PASS-RESPONSE-LOSS-PREVENTION-MATRIX / HOLD-NATIVE-MULTI-WINDOW-BROWSER / HOLD-PAGEHIDE-DURABILITY / HOLD-LEASE-EXPIRY-NETWORK-AMBIGUITY / HOLD-LIVE-COLLECTOR / HOLD-LIVE-FACTORY / DEFAULT-CUTOVER-NO_GO**

## Problem closed by this version

CUBE-REV 0.8.11 serialized initialization, migration, restart reconciliation, rollback, and target-resume arbitration. Once two 0.8.11 tabs had both entered the active task, however, each tab could retain an older in-memory copy of the same `localStorage` state. A later response, telemetry event, post-task form, snapshot seal, or Collector status update could therefore overwrite a newer revision written by another tab.

CUBE-REV 0.8.12 replaces those independent whole-object writes with one active-session operation dispatcher. Every operation executes under a dedicated same-origin exclusive Web Lock, reads the latest valid state inside that lock, applies a type-specific revision policy, increments the revision exactly once when a mutation succeeds, reseals the complete state, and verifies the stored result immediately after writing.

The version also separates the immutable scientific submission snapshot from mutable transmission-control metadata. One tab may own the Collector network attempt through a lease token, while later receipt, retry, and diagnostic metadata remain outside the frozen scientific envelope.

## Architecture

### Dedicated active-session write lock

All 0.8.12 operations use the exclusive lock:

```text
cube-rev-session-write-0812-exclusive-v1
```

The lock covers:

- unfinished 0.8.11 to 0.8.12 conversion;
- response writes;
- visibility and lifecycle telemetry;
- post-task writes;
- immutable snapshot sealing;
- submission lease claim and release;
- Collector auxiliary metadata merge;
- submission confirmation;
- state refresh and resume telemetry.

If a Web Locks-compatible manager is unavailable, 0.8.12 returns `LOCK_UNAVAILABLE` before creating or changing 0.8.12 scientific state. It does not use a best-effort `localStorage` mutex as a substitute.

### Revisioned state contract

The active state schema is:

```text
CR0812-RESUME-STATE-1
```

Every valid state contains:

- a monotonically increasing integer `revision`;
- a bounded mutation history;
- the assigned 28-item schedule and cursor;
- ordered opaque responses;
- telemetry events with event IDs;
- post-task data;
- an optional immutable submission snapshot and its hash;
- submission lease and receipt-control metadata;
- 0.8.11 source provenance and asset binding;
- an integrity checksum over the current state.

A successful mutation moves exactly from revision `r` to `r + 1`. The mutation journal records the mutation ID, operation type, prior revision, next revision, timestamp, outcome, and resulting integrity.

Mutation IDs are idempotency keys. Replaying the same completed mutation ID returns `IDEMPOTENT_REPLAY` without incrementing the revision again.

### Strict scientific-write CAS

Responses, post-task data, and snapshot sealing require an `expected_revision` supplied by the tab. The dispatcher rereads the current state under the lock and compares the supplied revision with the stored revision.

- An exact match permits further operation-specific validation.
- A stale future-trial response is rejected as `STALE_REVISION` without changing state.
- A stale post-task or snapshot operation is rejected without changing state.
- The participant route may retry once only when the stale revision was caused by a mergeable telemetry update and the scientific cursor or phase has not changed.

The expected cursor and stimulus are also checked for response operations. A tab cannot move the cursor backward, skip a trial, or write a response for a different scheduled stimulus.

### One-winner response conflict policy

When two tabs answer the same trial from the same starting revision, the exclusive lock linearizes the writes.

The first valid response:

- is appended at the current cursor;
- increments the cursor;
- increments the revision;
- records response telemetry.

The later response sees that its expected position is already occupied.

- If it is byte-equivalent at the scientific response level, the operation returns `RESPONSE_ALREADY_APPLIED` without another mutation.
- If it differs, the winning response remains unchanged and the losing attempted response is written to a separate bounded conflict-evidence journal.
- The losing response never replaces the winner and never advances or reverses the cursor.

The conflict journal is intentionally outside the scientific state so preserving evidence does not modify the selected response or the immutable submission envelope.

### Telemetry merge policy

Visibility, page lifecycle, and other telemetry are commutative append operations rather than strict scientific choices. They still execute under the exclusive lock, but a stale expected revision does not cause data loss.

The dispatcher:

1. reads the latest state;
2. rejects an already-seen event ID without another revision;
3. appends a new event to the latest telemetry array;
4. increments the revision exactly once;
5. leaves responses, cursor, post-task data, and snapshot bytes unchanged.

Two concurrent telemetry events from the same starting revision therefore both survive as two serialized revisions.

### Immutable scientific snapshot continuity

Snapshot sealing is permitted only after 28 responses and a saved post-task form. It freezes a scientific envelope containing:

- participant and session identity;
- sequence and ordered opaque responses;
- telemetry present at sealing time;
- post-task data;
- scientific completion timestamps;
- scientific revision at sealing;
- asset binding;
- migration and active-session provenance;
- participant-UI blinding declarations.

The envelope is hashed and stored as `submission_snapshot`. Later telemetry, lease state, Collector diagnostics, retry attempts, and receipt information may change the outer state revision but do not modify the snapshot or its hash.

After sealing:

- response and post-task mutations are rejected before input parsing;
- repeated seal attempts are idempotent;
- export always returns the stored immutable snapshot;
- submission retries reuse one stable retry identity derived from session ID and snapshot hash.

### Submission lease arbitration

The immutable snapshot is transmitted through the unchanged 0.7.12 Collector client. A separate lease contract determines which tab may own the live network attempt.

A lease contains:

- lease token;
- tab owner ID;
- monotonically increasing lease generation;
- expiration time;
- attempt counter;
- stable retry ID.

While a lease is active, another tab receives `SUBMISSION_IN_FLIGHT` and cannot become a network owner. Only the current lease token may merge Collector metadata, release the attempt, or confirm submission. A stale token is rejected without changing state.

On a failed attempt, the lease may be released while the immutable snapshot and retry ID remain unchanged. After the configured 120-second expiry, a later tab may claim a new generation.

This lease controls current local ownership, but cannot cancel an already-issued remote request. If the first request remains alive beyond lease expiry and a second owner retries, both requests may eventually reach the Collector. Receipt-v2 retry identity and server-side duplicate handling are therefore still required; this was not live-certified in 0.8.12.

### 0.8.11 continuity

An unfinished valid 0.8.11 state is converted into revision 1 of 0.8.12 while preserving:

- participant token;
- session ID;
- sequence and complete schedule;
- cursor and response prefix;
- telemetry and post-task phase;
- migration epoch and provenance;
- original 0.8.11 source bytes.

The target records the source storage key, integrity, revision, and migration timestamp. The 0.8.11 source is not deleted or rewritten.

A sealed or submitted 0.8.11 state is not converted. It remains on the original 0.8.11 route so the already-frozen payload can be retried without reversioning.

## Adversarial iterations

### Iteration 1 — snapshot authority ordering

The first CI run reached the post-seal response gate and failed with:

```text
UNKNOWN_RESPONSE_FIELD:position
```

The test intentionally attempted a response after snapshot sealing. The original dispatcher sanitized the supplied response object before checking the sealed-state authority. A stored response object contains `position` and `recorded_at`, which are forbidden as participant input fields, so input validation failed before the stronger `SNAPSHOT_ALREADY_SEALED` rule was reached.

The dispatcher was corrected so snapshot authority is tested before parsing response or post-task input. Once sealed, scientific mutation is rejected independently of the shape of the attempted input.

### Iteration 2 — gate accounting

The next run completed every functional gate, but the final assertion still expected 26 gates. During implementation, stale post-task rejection and expired-lease takeover had been promoted to separate gates, making the executable matrix 28 gates. The suite and terminal marker were corrected to 28/28 rather than deleting either test.

## Executed certification

### Final materialized-tree run

- branch head: `1d308b4c7038e9af2ffcf0928cc94df44a45237b`;
- active-session CAS workflow run: `30744215283` — **SUCCESS**;
- certification job: `91486924237` — **SUCCESS**;
- baseline/calibration workflow run: `30744215295` — **SUCCESS**;
- runner: Ubuntu 24.04;
- Node.js: `22.23.1`;
- workflow permission: repository contents read-only.

Required terminal markers:

```text
CR0812_ASSET_BUILD_PASS stimuli=28 choices=504
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

The final job also passed syntax checks for the builder, verifier, revisioned state module, CAS dispatcher, test suite, and participant inline script. It verified required script loading, active-write policy identities, public-bank minimization, and absence of `collector-config.js` and `js/collector-client.js` from the 0.8.12 diff.

### Artifact custody

The read-only final workflow exported the generated assets as:

```text
artifact ID: 8832320785
artifact name: cube-rev-0.8.12-verified-assets
artifact ZIP SHA-256: e610874e978c8955f1fa3d169943f4792bcd29168e5eca754cad400b2324f2dd
artifact size: 12368 bytes
```

The public bank is materialized in Git as blob:

```text
e75d62cf98fc148bd2b8f1485e1731149e144f69
```

## Twenty-eight executable gates

1. Build and verify the 28-stimulus, 24-sequence, 504-choice-code 0.8.12 bundle and active-session policies.
2. Reject a public config whose revision policy differs from the pinned config.
3. Fail closed without changing storage when no active-session lock manager is available.
4. Convert a partially completed valid 0.8.11 session while preserving cursor, responses, identity, and source bytes.
5. Serialize two concurrent conversion attempts so one upgrades and the other resumes the same target.
6. Apply one valid response and advance revision and cursor exactly once.
7. Treat replay of the same mutation ID as idempotent.
8. Serialize two different responses for one trial so one wins and one produces conflict evidence.
9. Reject a stale response aimed at the current unfilled position.
10. Merge stale telemetry onto the latest revision without changing the cursor.
11. Deduplicate a telemetry event by event ID without another revision.
12. Preserve two concurrent distinct telemetry events as two serialized revisions.
13. Complete the remaining 28-item schedule without cursor loss or reordering.
14. Reject a stale post-task write.
15. Apply one valid post-task write and enter `READY_TO_SUBMIT`.
16. Seal one valid immutable scientific snapshot and stable retry ID.
17. Append post-seal telemetry without changing the snapshot hash.
18. Reject a response after snapshot sealing before response-input parsing.
19. Make repeated snapshot sealing idempotent.
20. Serialize two concurrent submission claims so only one lease owner is selected.
21. Reject Collector metadata from a stale or foreign lease token.
22. Merge allow-listed Collector auxiliary metadata from the active lease owner.
23. Release a failed lease without changing the immutable snapshot.
24. Reclaim the same snapshot under a later lease generation.
25. Confirm submission only from the current lease owner and preserve the exported snapshot.
26. Make repeated confirmation idempotent after `SUBMITTED`.
27. Quarantine an invalid active state rather than automatically creating a replacement session.
28. Permit a new owner after lease expiry while incrementing the lease generation and preserving the snapshot.

## Materialized asset identities

| Artifact | Canonical SHA-256 |
|---|---|
| 0.8.12 manifest | `c9abbf5c1057bb0e02795fc0d3ab1095c9ce115943b1f89cb825ac8a9ed35af6` |
| 0.8.12 public bank | `fc76841350cd8937e576c701995ff64bcfbc02f6f7b50977b8946f8299a712a8` |
| 0.8.12 public config | `1d04467c3ad2390f2e9784973bd026c1b77b8a72919fedd09070ff048b6d0701` |
| parent 0.8.11 manifest | `ef6a767d079fcf63c24f9cab4032ae2175beac3345ce91f89dc72d01b6155d7f` |
| parent 0.8.11 public bank | `77df943d6f5bb039ff2ed0761fa28866915bd1110dab1b27d6524a63cbea43e8` |
| parent 0.8.11 public config | `89c1aa968637a7e6431c8d765729349c53e6af97178e93bdaceeef9433f22adf` |
| protected private crosswalk | `90c54b51052fc27c436d8701797e5b2aa95e19ec28a7f63bbd50db41192748f0` |

Canonical parsed-object identities, raw artifact-file hashes, Git blob identities, and the artifact ZIP digest are recorded as separate evidence layers and are not conflated.

## Evidence boundary

### Certified

- exclusive serialization in a deterministic asynchronous lock-manager simulation;
- strict expected-revision CAS for responses, post-task writes, and snapshot sealing;
- exactly-one revision increment per successful mutation;
- idempotent replay by mutation ID;
- one-winner response conflict handling with separate loser evidence;
- no cursor rollback or stale scientific overwrite in the tested matrix;
- telemetry append-merge against the latest valid revision;
- telemetry event deduplication;
- immutable scientific snapshot continuity across later telemetry and transmission metadata changes;
- one active local submission lease owner in the simulated concurrency model;
- stale lease-token rejection, release, expiry, and generation takeover;
- preservation of unfinished 0.8.11 identity and source bytes;
- non-conversion of sealed 0.8.11 payloads;
- inherited 0.8.11, 0.8.10, 0.8.9, and 0.8.8 contracts;
- frozen Collector source and configuration.

### Not certified

- owner-observed operation in two actual browser windows using the browser's native Web Locks scheduler;
- every browser's tab suspension, background throttling, private-mode, storage eviction, and process-kill behavior;
- completion of an asynchronous `pagehide` telemetry transaction before the browser terminates the page;
- cancellation of an already-issued Collector request when a local lease expires;
- absence of duplicate remote delivery when an old request completes after another tab has reclaimed an expired lease;
- live receipt-v2 Collector behavior and server-side retry deduplication;
- live Factory reconstruction and normalization;
- production default-entry replacement;
- cryptographic origin authentication when page, pins, and assets could be replaced together.

Web Locks plus revision validation provide serialized browser-origin operations, but `localStorage` remains non-transactional storage rather than an ACID database. The post-write verification detects many failures but cannot prove durability across every OS or browser termination point.

## Next boundary

The remaining correctness boundary is now empirical and end-to-end rather than another local state-machine gap. The next version should execute the route in two native browser windows, force suspension and closure at response, snapshot, and lease boundaries, inject Collector delays longer than the lease timeout, verify receipt-v2 duplicate behavior, and reconstruct the resulting payload through the actual Factory without changing the frozen Collector contract.

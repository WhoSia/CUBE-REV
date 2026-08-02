# CUBE-REV 0.8.11 Validation Report

## Official title

**CUBE-REV 0.8.11 — Atomic Migration Journal, Multi-tab Upgrade Arbitration & Downgrade-safe Rollback Certification**

## Official decision

> **PASS-ATOMIC-MIGRATION-JOURNAL / PASS-MULTI-TAB-UPGRADE-ARBITRATION-SIMULATION / PASS-MONOTONIC-FENCING-EPOCH / PASS-CRASH-RECONCILIATION / PASS-DOWNGRADE-MUTATION-QUARANTINE / PASS-DOWNGRADE-SAFE-ROLLBACK / HOLD-LIVE-MULTI-WINDOW-BROWSER / HOLD-ACTIVE-SESSION-WRITE-SERIALIZATION / HOLD-LIVE-COLLECTOR / HOLD-LIVE-FACTORY / DEFAULT-CUTOVER-NO_GO**

## Problem closed by this version

CUBE-REV 0.8.10 could migrate one valid 0.8.8 or 0.8.9 source and preserve its assignment, but its journal and `localStorage` writes were not protected by an exclusive cross-tab coordinator. Two tabs could therefore enter the upgrade path concurrently, and a browser interruption between target write, archive write, and final journal commit required an explicit deterministic reconciliation policy. A stale legacy tab could also continue writing its preserved source after a newer target had become authoritative.

CUBE-REV 0.8.11 closes the initialization, migration, restart-reconciliation, and downgrade-fencing boundary at the executable-contract level.

## Architecture

### Web Locks fail-closed arbitration

The participant route requires an exclusive same-origin lock named:

```text
cube-rev-migration-0811-exclusive-v1
```

Asset verification occurs before the migration coordinator is invoked. Scientific state initialization, legacy-source selection, migration, journal reconciliation, rollback decision, and target resume then occur inside one exclusive lock callback. If a Web Locks-compatible `request()` contract is unavailable, the route returns `LOCK_UNAVAILABLE` before reading, creating, migrating, or mutating scientific state.

This policy deliberately favors preservation over compatibility. It does not fall back to a best-effort `localStorage` mutex whose atomicity cannot be established.

### Monotonic fencing epoch and owner token

Every lock acquisition increments `cube-rev-migration-0811-epoch-v1` and writes an active owner record containing:

- a monotonically increasing epoch;
- an owner token;
- acquisition and release status;
- acquisition and release timestamps.

Every critical journal, target, archive, fence, or quarantine write verifies the active owner immediately before and after mutation. An older owner fails with `STALE_MIGRATION_OWNER` and cannot advance a newer transaction.

The epoch is also embedded in migrated 0.8.11 state as `upgrade_epoch` and in `migration_provenance.migration_epoch`.

### Atomic journal phases

The journal state machine is:

```text
PREPARED
  → TARGET_WRITTEN
  → ARCHIVE_WRITTEN
  → FENCE_WRITTEN
  → COMMITTED
```

Terminal alternatives are:

```text
ROLLED_BACK
ROLLED_BACK_TO_LEGACY
```

The journal stores enough evidence to reconcile a restart without generating a new assignment:

- transaction ID and transaction epoch;
- source version, schema, storage key, session ID, integrity, fingerprint, and exact raw text;
- target storage key and initial target integrity;
- archive key;
- phase timestamps;
- last writer epoch and owner token;
- rollback or downgrade evidence when applicable.

### Authority boundary at `FENCE_WRITTEN`

The authority transition is intentionally placed at `FENCE_WRITTEN`, not merely at the later `COMMITTED` marker.

Before the fence:

- source mutation means the legacy session progressed concurrently;
- the target is not adopted;
- the target is removed;
- the evidence is rolled back or quarantined.

After the fence:

- the 0.8.11 target is authoritative;
- a later write by an already-open legacy page is classified as downgrade mutation;
- the mutated source is quarantined;
- the valid target remains resumable.

This prevents a stale lower-version tab from replacing a newer committed lineage.

### Committed target identity versus mutable target integrity

The first CI run exposed an important design error: after `COMMITTED`, an ordinary resume telemetry event changes the target's valid local integrity. Comparing every later target to the initial target integrity therefore falsely classified normal progress as target loss and attempted legacy rollback.

The corrected policy distinguishes two stages:

- before authority, the newly written target must match its initial recorded integrity exactly;
- after `COMMITTED`, the target must be currently valid under the 0.8.11 schema and asset binding, and must match the journal by migration epoch, source provenance, source integrity, source storage key, and session identity. It is not required to retain the initial integrity after valid responses or telemetry are appended.

This correction was discovered by the adversarial test suite rather than assumed away.

### Multi-version ancestry selection

The coordinator validates possible sources from 0.8.8, 0.8.9, and 0.8.10.

A valid 0.8.10 source is preferred only when every preserved lower-version source is a proven ancestor. The proof requires:

- matching participant token, session ID, sequence ID, and complete schedule;
- lower cursor not exceeding the higher cursor;
- exact equality of the common response prefix for stimulus, displayed choice, latency, position, and recorded timestamp;
- 0.8.10 migration provenance naming the lower storage key and lower source integrity.

An unrelated 0.8.10 state and a lower source are therefore not ranked merely by version number; they produce `ANCESTRY_CONFLICT` and are quarantined.

### Crash reconciliation

On entry under the exclusive lock, the coordinator examines the journal, target, source, exact archive, and downgrade fence.

- `PREPARED` with no target rolls back and re-enters source selection.
- `PREPARED` with a valid matching orphan target advances to `TARGET_WRITTEN`.
- `TARGET_WRITTEN` validates target identity and source stability, then writes or verifies the exact archive.
- `ARCHIVE_WRITTEN` validates target, source, and archive, then writes the authority fence.
- `FENCE_WRITTEN` validates the authoritative target/archive pair and completes the commit; post-fence source mutation is quarantined without discarding the target.
- `COMMITTED` resumes a currently valid target whose epoch, provenance, and session identity match the journal.
- If a committed target is absent or invalid while source and archive remain byte-identical, the journal becomes `ROLLED_BACK_TO_LEGACY` and returns the original version route without rewriting the source.
- If target loss and source divergence occur together, automatic rollback is forbidden and the evidence is quarantined.

### Sealed legacy non-rewrite

A source containing an immutable submission snapshot, or marked `SUBMITTED`, is never migrated. The participant is returned to the corresponding 0.8.8, 0.8.9, or 0.8.10 route for retry of the original sealed payload.

## Executed certification

### Final materialized-tree run

- branch head: `e20b320cd69694fe37026a67c798647af9dd1ef5`;
- atomic-migration workflow run: `30742046107` — **SUCCESS**;
- certification job: `91481063097` — **SUCCESS**;
- baseline/calibration workflow run: `30742046089` — **SUCCESS**;
- runner: Ubuntu 24.04;
- Node.js: `22.23.1`;
- workflow permissions: repository contents read-only.

Required terminal markers:

```text
CR0811_ASSET_BUILD_PASS stimuli=28 choices=504
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

The job also passed syntax checks for the builder, verifier, participant runtime, atomic coordinator, committed-authority policy, test suite, and participant inline script. It verified that the participant page loads the committed-authority policy, that the generated public bank contains no forbidden internal metadata fields, and that `collector-config.js` and `js/collector-client.js` are absent from the 0.8.11 diff.

### Artifact custody

The read-only workflow exported the verified generated assets as artifact:

```text
artifact ID: 8831602344
artifact name: cube-rev-0.8.11-verified-assets
artifact ZIP SHA-256: 9c977c39e5a38b7b1776a1736aa75f949449a2620cdc895119cfce6223422341
```

The artifact's public-bank bytes were inserted into Git as blob `85f7407eb2535dbc2a44a9b20108a3d86b3cb793`; the repository reports the same blob SHA after materialization.

## Twenty-three executable gates

1. Build and verify the 28-stimulus, 24-sequence, 504-choice-code 0.8.11 bundle and atomic policy fields.
2. Reject a config mutation that disables the required Web Locks policy.
3. Fail closed without changing storage when no lock manager is available.
4. Create one fresh 0.8.11 session under an exclusive lock.
5. Serialize two concurrent fresh-session initializations so one creates and the other resumes the same session.
6. Migrate an unfinished 0.8.8 source, preserve assignment, preserve source bytes, and commit the journal.
7. Migrate an unfinished 0.8.9 source without changing its opaque responses.
8. Migrate an unfinished valid 0.8.10 source.
9. Prefer a 0.8.10 descendant when its preserved 0.8.8 source is proven as its ancestor.
10. Quarantine an unrelated 0.8.10 state coexisting with a lower-version source.
11. Refuse to rewrite a sealed 0.8.10 snapshot and return its original route.
12. Reject a stale owner after a newer fencing epoch has been acquired.
13. Recover from a crash after `PREPARED` without creating a new assignment.
14. Complete a matching orphan transaction after a crash at `TARGET_WRITTEN`.
15. Complete a matching orphan transaction after a crash at `ARCHIVE_WRITTEN`.
16. Complete a matching authoritative transaction after a crash at `FENCE_WRITTEN`.
17. Resume a valid committed target after a crash immediately after `COMMITTED`, including subsequent valid telemetry mutations.
18. Remove an invalid pre-fence target, record rollback, and remigrate from the preserved source.
19. Roll back to the original legacy route when a committed target is lost but source and archive remain exact.
20. Quarantine a post-commit downgrade-source mutation while retaining the valid target.
21. Block automatic legacy rollback when target loss and source divergence coexist.
22. Abort and remove the target when the legacy source changes before the authority fence.
23. Serialize two concurrent migrations so one commits and the later tab resumes the same target and epoch.

## Materialized asset identities

| Artifact | Canonical SHA-256 |
|---|---|
| 0.8.11 manifest | `ef6a767d079fcf63c24f9cab4032ae2175beac3345ce91f89dc72d01b6155d7f` |
| 0.8.11 public bank | `77df943d6f5bb039ff2ed0761fa28866915bd1110dab1b27d6524a63cbea43e8` |
| 0.8.11 public config | `89c1aa968637a7e6431c8d765729349c53e6af97178e93bdaceeef9433f22adf` |
| parent 0.8.10 manifest | `7961e5b36320c303b1784f5f35fa915042c13e25a3fc716242f4e70ccb97df81` |
| protected private crosswalk | `90c54b51052fc27c436d8701797e5b2aa95e19ec28a7f63bbd50db41192748f0` |

Raw artifact-file SHA-256 values are separately recorded in the decision packet and runbook. Canonical JSON identities and raw file-byte identities are not conflated.

## Evidence boundary

### Certified

- exclusive-lock serialization in a deterministic asynchronous lock-manager simulation;
- one-winner fresh initialization and one-winner migration under concurrent calls;
- monotonically increasing fencing epochs and stale-owner rejection;
- deterministic reconciliation of the tested crash positions;
- pre-fence source-divergence rollback;
- post-fence downgrade mutation quarantine;
- committed-target authority under valid later state evolution;
- exact-source/archive rollback to a legacy route after target loss;
- refusal to roll back automatically when target loss and source divergence coexist;
- ancestry-aware preference for a valid 0.8.10 descendant;
- sealed legacy snapshot non-rewrite;
- inherited 0.8.10, 0.8.9, and 0.8.8 contracts;
- frozen Collector source and configuration.

### Not certified

- an owner-observed test using two actual browser windows or tabs and the browser's native Web Locks scheduler;
- behavior in every browser implementation, suspension policy, private-mode policy, storage eviction regime, or OS process-kill timing;
- serialization of every participant response write after initialization. Once multiple 0.8.11 tabs are actively displaying the task, their later `record`, telemetry, post-task, and submission mutations are not yet protected by revision compare-and-swap;
- immediate prevention of writes from a legacy page that was already open before the fence. Such a write is detected and quarantined on the next 0.8.11 arbitration, not synchronously blocked inside the old page;
- cryptographic origin authentication if page, pins, and assets can be replaced together;
- live Collector POST and receipt behavior;
- live Factory reconstruction;
- production default-entry replacement.

`localStorage` remains non-transactional. Web Locks serialize the coordinator, while the fencing epoch detects stale coordinator ownership. This is stronger than a best-effort lock but is not equivalent to an ACID database transaction across every browser and process failure.

## Next boundary

The remaining internal correctness boundary is no longer migration arbitration; it is active-session write concurrency after migration. The next version should serialize or compare-and-swap every scientific state mutation, attach an expected revision to each operation, reject stale-tab writes, merge telemetry without losing responses, preserve immutable snapshot identity, and prove that concurrent response/submission attempts converge without overwriting a later revision.

# CUBE-REV 0.8.8 Validation Report

## Official title

**CUBE-REV 0.8.8 — Immutable Submission Snapshot Sealing, Receipt-loss Retry Identity & Tamper-quarantine Certification**

## Scope

This version closes the unresolved receipt-loss boundary from CUBE-REV 0.8.7 without changing the production collector source, collector configuration, or collector protocol version.

The participant application remains versioned as `CUBE-REV 0.8.8`, while collector health and POST compatibility remain pinned to the verified `0.7.12` receipt-v2 contract.

## Implemented contract

1. Scientific responses, pre-seal telemetry, post-task answers, and participant-facing condition metadata are copied into a dedicated submission snapshot only after the session reaches `READY_TO_SUBMIT`.
2. The snapshot is assigned a stable hash and is thereafter the only object exported to the collector.
3. Submission attempts, failures, retries, receipt metadata, and other transport-side mutations are stored outside the scientific snapshot.
4. A retry after server-side storage and receipt loss therefore serializes the same snapshot and produces the same collector checksum.
5. Invalid resume state, sequence drift, top-level corruption, or snapshot/hash disagreement is removed from the active storage key and preserved under a quarantine key.
6. New sessions retain the 24-sequence stable anonymous-token assignment and cannot enter the retired legacy fixed-set selector path.

## Executed validation gates

The executable Node contract suite now covers eight gates:

1. pre-completion snapshot sealing is rejected;
2. repeated sealing is idempotent and post-seal telemetry cannot mutate the payload;
3. receipt-loss retry preserves checksum identity;
4. concurrent calls through one collector client collapse to one in-flight POST;
5. collector checksum mismatch remains failed and unconfirmed;
6. top-level state corruption is quarantined;
7. snapshot mutation is quarantined even when the outer integrity value is recomputed;
8. sequence/schedule drift is quarantined rather than silently reassigned.

Expected terminal marker:

```text
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

An independent reconstruction of the branch runtime and shadow collector contract reproduced the pass marker before this report was committed.

## Evidence boundary

### Certified

- retry-stable scientific serialization within the 0.8.8 client runtime;
- stable FNV-1a collector checksum across receipt-loss retry when the collector returns the checksum of the stored payload;
- local corruption and inconsistent-state quarantine;
- preservation of the 0.7.12 collector interface;
- no silent sequence reassignment during resume validation.

### Not certified

- cryptographic resistance to an active attacker who can rewrite both browser state and all integrity fields;
- live production collector behavior;
- browser/device compatibility beyond static/runtime contract execution;
- automatic replacement of the repository default `index.html` entry;
- Factory ingestion of the new payload in a live end-to-end run.

The current FNV-based integrity fields are contract and corruption detectors, not cryptographic signatures. The term `tamper-quarantine` in this version means detected inconsistent local mutation under the specified state contract.

## File-level safety result

CUBE-REV 0.8.8 adds only cognitive-mode configuration, participant stimulus data, participant runtime/page, telemetry schema, and contract tests on top of the 0.8.7 branch. It does not modify:

- `collector-config.js`
- `js/collector-client.js`

## Decision

> **PASS-IMMUTABLE-SNAPSHOT / PASS-RETRY-IDENTITY / PASS-LOCAL-QUARANTINE / HOLD-LIVE-COLLECTOR / DEFAULT-CUTOVER-NO_GO**

The 0.8.8 branch is suitable for review as a stacked research and participant-route PR. It is not yet authorized as the production default entry.

## Next research boundary

The public participant stimulus bank still carries internal `state_id`, `rotation_id`, and `face_map` fields. These are not prominently shown in the UI, but they weaken source-level blinding and exceed the minimum rendering payload. The next version should minimize public stimulus metadata, move canonicalization to an opaque response code or private analysis crosswalk, and certify that Factory reconstruction remains possible without exposing internal identifiers to participants.

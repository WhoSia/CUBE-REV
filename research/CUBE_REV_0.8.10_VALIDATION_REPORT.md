# CUBE-REV 0.8.10 Validation Report

## Official title

**CUBE-REV 0.8.10 — Cross-version Resume Migration, Assignment Continuity & Public-asset Hash-pinning Certification**

## Official decision

> **PASS-CROSS-VERSION-MIGRATION / PASS-ASSIGNMENT-CONTINUITY / PASS-PUBLIC-ASSET-HASH-PINNING / PASS-SOURCE-PRESERVATION / PASS-SEALED-LEGACY-NONREWRITE / HOLD-MULTI-TAB-ATOMICITY / HOLD-LIVE-COLLECTOR / HOLD-LIVE-FACTORY / DEFAULT-CUTOVER-NO_GO**

## Problem closed by this version

CUBE-REV 0.8.9 introduced a participant-minimized public bank and opaque choice codes, but it also introduced a new local-storage schema. Without an explicit migration contract, an unfinished 0.8.8 or 0.8.9 session could be abandoned, silently restarted, or reassigned when entering a newer participant route. In addition, the browser previously checked asset shape and version but did not bind the exact manifest, bank, and config bytes to an embedded SHA-256 pin set before state loading.

CUBE-REV 0.8.10 closes those two boundaries at the executable-contract level.

## Architecture

### Pinned public-asset bundle

A deterministic builder derives a 0.8.10 bank, config, manifest, and pin module from the certified 0.8.9 public artifacts. The parent 0.8.9 bank and config are first recomputed under the same canonicalization contract and compared with their recorded SHA-256 identities. The 0.8.10 route then loads the manifest, bank, and config as text, canonicalizes each parsed JSON object with `JSON.stringify`, recomputes SHA-256, and compares the results with `js/asset-pins-0.8.10.js` before any local session is read or migrated.

The binding is copied into the 0.8.10 local state and into the immutable scientific submission snapshot. A state created under one bank/config binding is therefore not resumed under a different verified bundle.

### Cross-version migration

The migration kernel accepts one valid legacy source from either:

- `cube-rev-cognitive-mode-0808-v1`; or
- `cube-rev-cognitive-mode-0809-v1`.

Only an unsealed state in `IN_PROGRESS`, `POST_TASK`, or `READY_TO_SUBMIT` may be transformed.

The following values are preserved exactly:

- anonymous participant token;
- session identifier;
- sequence identifier;
- complete 28-item schedule;
- cursor and response order;
- displayed choice;
- latency and recorded timestamp;
- creation time;
- post-task response, when already present.

For 0.8.8 responses, the displayed move is resolved against the certified public bank and replaced by the corresponding opaque choice code. Participant-side `state_id`, `rotation_id`, `face_map`, and canonical-move fields are not copied into the 0.8.10 response.

### Source preservation and rollback

The source storage value is never deleted or rewritten. Before target construction, the kernel records a `PREPARED` migration journal. After the target is written, the runtime rereads and validates it, checks assignment continuity, verifies that the source raw text is unchanged, archives an exact source copy under a migration-specific key, and then records `COMMITTED`.

If an error occurs after journal preparation or after target write, the target is removed, the source is retained byte-for-byte, and the journal becomes `ROLLED_BACK`.

### Sealed legacy non-rewrite

A legacy state containing a submission snapshot, or marked `SUBMITTED`, is not converted. The 0.8.10 route directs the participant to the matching 0.8.8 or 0.8.9 page so that the original sealed payload remains the retry identity. This prevents a completed scientific envelope from being re-versioned after sealing.

### Additional state-machine validation

The migration kernel does not rely only on the legacy runtime checksum and schedule validator. It independently verifies that:

- `IN_PROGRESS` means fewer than 28 responses and no post-task object;
- `POST_TASK` means exactly 28 responses and no post-task object yet;
- `READY_TO_SUBMIT` means exactly 28 responses and a post-task object;
- a sealed state is complete and is either `READY_TO_SUBMIT` or `SUBMITTED`;
- `SUBMITTED` without a snapshot is impossible.

This blocks an impossible state whose outer FNV integrity was recomputed successfully.

## Executed certification

### GitHub Actions

- migration certification workflow run: `30740724909` — **SUCCESS**;
- baseline/calibration workflow run: `30740724897` — **SUCCESS**;
- certification job: `91477556949` — **SUCCESS**;
- runner: Ubuntu 24.04, Node.js `22.23.1`.

The job log emitted all required terminal markers:

```text
CR0810_ASSET_BUILD_PASS stimuli=28 choices=504
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

It also completed syntax checks for the builder, verifier, runtime, migration kernel, test suite, and inline participant-page script; verified that the generated public bank contains none of the forbidden internal metadata keys; and confirmed that neither `collector-config.js` nor `js/collector-client.js` occurs in the 0.8.10 diff.

## Thirteen contract gates

1. Build and verify the exact 28-stimulus, 24-sequence, 504-choice-code pinned bundle.
2. Reject a public bank whose sticker data changed without a matching pin update.
3. Preserve assignment across ordinary 0.8.10 reload.
4. Migrate an unfinished 0.8.8 session while preserving token, sequence, schedule, cursor, order, latency, timestamps, source raw text, and exact archive; repeated entry resumes the target rather than migrating twice.
5. Migrate a complete unsealed 0.8.8 `READY_TO_SUBMIT` session, preserve post-task data, and seal a 0.8.10 snapshot bound to the verified assets.
6. Migrate an unfinished 0.8.9 opaque-code session without changing its responses.
7. Refuse to rewrite a sealed 0.8.8 snapshot and return the 0.8.8 retry route.
8. Refuse to rewrite a sealed 0.8.9 snapshot and return the 0.8.9 retry route.
9. Roll back target state after an injected post-write failure while retaining the source and recording `ROLLED_BACK`.
10. Quarantine a legacy source with assignment/sequence inconsistency.
11. Quarantine rather than choose between simultaneous valid 0.8.8 and 0.8.9 sources.
12. Reject an impossible legacy status/cursor/post-task shape even when its outer legacy integrity is recomputed.
13. Quarantine an existing 0.8.10 target whose asset binding disagrees with the verified bundle, even when its outer state integrity is recomputed.

## Materialized asset identities

| Artifact | SHA-256 |
|---|---|
| 0.8.10 asset manifest | `7961e5b36320c303b1784f5f35fa915042c13e25a3fc716242f4e70ccb97df81` |
| 0.8.10 public bank | `38b706b0dbf6735ac6cefb34289aa6fe36dcf8252552ed22ee9c7be4af55ed89` |
| 0.8.10 public config | `040ded0ea10cbdd794e924b35ac09be9e4c25dbf707727be03e38929db5ab54d` |
| parent 0.8.9 manifest | `00b9c255dd050638020e9436fb01911d8e50f886595d4dd14bc529ded906813a` |
| protected private crosswalk | `90c54b51052fc27c436d8701797e5b2aa95e19ec28a7f63bbd50db41192748f0` |

The generated pinned assets were committed by `github-actions[bot]` in commit `900dbbb509329ea0da8c99968dd95e7b2945c8c1`.

## Evidence boundary and limitations

### Certified

- deterministic migration of one valid unsealed 0.8.8 or 0.8.9 source;
- exact assignment and response-history continuity under the tested contracts;
- 0.8.8 display-choice conversion to the certified opaque-code namespace;
- source non-mutation, exact source archival, and injected-failure rollback;
- sealed legacy snapshot non-rewrite;
- participant-bank/config/manifest drift detection before local-state access;
- asset-binding persistence into local state and immutable submission snapshot;
- inherited 0.8.9 public-bank and 0.8.8 immutable-snapshot regressions;
- unchanged Collector source and configuration.

### Not certified

- true atomic arbitration between multiple tabs that start migration concurrently;
- reconciliation of every possible browser crash between target write, archive write, and final journal commit;
- cryptographic origin authentication if an attacker can rewrite the participant page, embedded pin module, and public assets together;
- live production Collector behavior;
- live Factory reconstruction with the protected crosswalk;
- mobile/desktop browser walkthrough;
- replacement of the production default `index.html`.

The FNV values used for local state and migration source fingerprints remain deterministic corruption and contract indicators, not cryptographic signatures. SHA-256 pinning detects partial or accidental deployment drift under the pinned page; it does not constitute a complete software supply-chain signature.

## Next boundary

The remaining internal engineering boundary is concurrent-upgrade and crash reconciliation. The next version should use a same-origin exclusive migration lock where available, introduce a fenced journal epoch, reconcile `PREPARED` journals against target/source/archive state after restart, prevent stale tabs from committing, and certify downgrade-safe rollback without mutating the preserved legacy source.

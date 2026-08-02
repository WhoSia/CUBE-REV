# CUBE-REV 0.8.9 Validation Report

## Official title

**CUBE-REV 0.8.9 — Public-bank Identifier Minimization, Opaque Choice-code Encoding & Private-crosswalk Factory Reconstruction Certification**

## Problem closed by this version

CUBE-REV 0.8.8 hid diagnostic labels from the visible interface, but its participant-downloadable stimulus bank still carried `state_id`, `rotation_id`, and `face_map`. The browser also computed `choice_canonical` directly. Those fields were convenient for analysis but exceeded the minimum participant rendering contract and weakened source-level blinding.

CUBE-REV 0.8.9 separates the participant artifact from the analysis identity layer.

## Architecture

### Participant-facing public bank

Each public stimulus contains only:

- an opaque `stimulus_id`;
- sticker colors required for rendering;
- a map from each of the 18 display moves to an opaque response code.

It does not contain state identifiers, rotations, face maps, canonical moves, diagnostic labels, pair/member identifiers, branch metadata, or distance metadata.

### Opaque response encoding

For 28 stimuli and 18 display moves per stimulus, the deterministic builder creates 504 globally unique response codes of the form:

```text
CR9C-<16 lowercase hexadecimal characters>
```

The participant payload records `stimulus_id`, `choice_display`, and `choice_code`; it does not record `choice_canonical`, `state_id`, or `rotation_id`.

### Private analysis crosswalk

The builder separately generates a crosswalk classified as:

```text
DO_NOT_DEPLOY_PARTICIPANT_SIDE
```

The crosswalk restores state, rotation, display choice, and canonical choice for Factory analysis. Its output path and filename pattern are excluded through `.gitignore`, and CI fails if a private crosswalk path becomes tracked.

### Factory reconstruction

The reconstruction tool accepts only a CUBE-REV 0.8.9 opaque-code payload and a private crosswalk. It rejects:

- unknown stimulus/code pairs;
- payload-version mismatches;
- response-encoding mismatches;
- display choices that disagree with the private code mapping.

## Executed certification

The 0.8.9 GitHub Actions workflow completed successfully. Its certification job executed:

1. deterministic public/private artifact generation;
2. private-crosswalk ignore and tracked-file checks;
3. the eight-gate 0.8.9 contract suite;
4. the inherited eight-gate 0.8.8 immutable-snapshot suite;
5. Node syntax checks for builder, Factory reconstruction, runtime, and tests;
6. static scans proving the generated participant bank contains no forbidden metadata keys.

The repository baseline/calibration workflow also completed successfully on the same stacked PR revision.

Required 0.8.9 test marker:

```text
CR0809_PUBLIC_BANK_CERT_PASS 8/8
```

The generated manifest records:

- 28 stimuli;
- 24 counterbalanced sequences;
- 504 unique opaque choice codes;
- SHA-256 identities for the public bank, public config, and private crosswalk.

## Eight contract gates

1. exact stimulus, schedule, and opaque-code cardinalities;
2. absence of all forbidden participant-side metadata keys;
3. exact preservation of state/rotation/face-map information in the private crosswalk;
4. exact preservation of all 24 parent schedules;
5. participant-runtime rejection of internal response fields;
6. full Factory reconstruction of all 28 responses;
7. rejection of display/code disagreement;
8. repository ignore coverage for private crosswalk outputs.

## Scientific and security interpretation

This version improves source-level blinding and minimizes participant-delivered metadata. It does not make the cube states cryptographically secret: the sticker pattern must remain visible to perform the task, and a sufficiently motivated analyst may infer properties from the rendered state itself.

The public manifest contains a hash of the private crosswalk so that the analysis artifact can later be identity-checked. A cryptographic hash does not expose the crosswalk contents under ordinary preimage-resistance assumptions, but access control for the private crosswalk remains an operational requirement.

## Collector and compatibility boundary

Unchanged files:

- `collector-config.js`
- `js/collector-client.js`

The application payload reports `CUBE-REV 0.8.9`; collector health and POST compatibility remain pinned to the verified `0.7.12` receipt-v2 contract.

## Decision

> **PASS-PUBLIC-BANK-MINIMIZATION / PASS-OPAQUE-CHOICE-ENCODING / PASS-PRIVATE-OUTPUT-EXCLUSION / PASS-FACTORY-RECONSTRUCTION-CONTRACT / HOLD-LIVE-FACTORY / HOLD-LIVE-COLLECTOR / DEFAULT-CUTOVER-NO_GO**

## Remaining gates

The following were not performed and remain external or owner-authorized gates:

- live Factory ingestion using the protected private crosswalk;
- live collector submission from the 0.8.9 participant route;
- mobile and desktop browser walkthrough;
- replacement of the production default `index.html` entry;
- policy and storage decision for custody of the private crosswalk.

## Next boundary

The 0.8.9 runtime uses a new storage schema and key. An in-progress 0.8.8 session would therefore not automatically resume in 0.8.9. The next version should certify cross-version migration without mutating an already sealed 0.8.8 snapshot, and should bind the loaded public bank/config to the manifest hashes before task execution.

# CUBE-REV 0.8.13 Live-evidence Erratum

## Issued by

**CUBE-REV 0.8.14 — Stored-raw Custody Replay, Cross-device Browser Matrix & Controlled Staging Cutover Gate**

## Status

This erratum supersedes the live-Collector payload-identity and receipt-code statements in:

- `research/CUBE_REV_0.8.13_VALIDATION_REPORT.md`;
- `research/CUBE_REV_0.8.13_DECISION_PACKET.json`;
- `research/CUBE_REV_0.8.13_LIVE_COLLECTOR_EVIDENCE.json`;
- the live-evidence section of pull request #12.

The native Chromium, active-session CAS, deterministic transport bridge, local delayed-receipt emulator, inherited-contract, and non-live Factory results of 0.8.13 are not revoked by this erratum.

## Why the correction is required

The preserved GitHub Actions artifact from the actual one-time live Collector workflow does not contain the payload identities later written into the 0.8.13 evidence ledger.

The authoritative archival execution is:

| Field | Preserved value |
|---|---|
| workflow run | `30747246961` |
| workflow head | `70e68aa2a768972d31882e0f1c2a483cfd9ca9bc` |
| artifact ID | `8833272340` |
| artifact ZIP SHA-256 | `c046f432a4eaa075fbc8c2e7ffafd4b363f3aa5ef79d204a0a5544472f920575` |
| snapshot bytes | `6481` |
| snapshot SHA-256 | `5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83` |
| submitted envelope bytes | `16217` |
| submitted envelope SHA-256 | `6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9` |
| submitted envelope FNV-1a32 | `c8cda746` |
| receipt status | `duplicate`, `duplicate` |
| preserved receipt code | `BZLWG-S8PJCN`, `BZLWG-S8PJCN` |
| referenced file name | `CR-20260802110000-0813a0b0c0d0.json` |

CUBE-REV 0.8.14 reconstructed the archival submission independently from the exact live-workflow envelope-construction code and reproduced all three envelope identities exactly:

```text
bytes    16217
sha256   6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9
fnv1a32  c8cda746
```

## Values withdrawn from the 0.8.13 live claim

The following later-committed values are not present in the preserved live workflow artifact and are therefore withdrawn as evidence of that live submission:

```text
envelope bytes    21227
envelope SHA-256  6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3
envelope FNV      f795cd8e
snapshot SHA-256  446ab20ec570140f810bcbe91660b089585f1416db5b29852f7bf6946881e2ba
receipt codes     CR0712-RCP-1C74B563 / CR0712-RCP-953ECF13
```

The final 0.8.13 runtime was also executed against the fixed snapshot during the 0.8.14 audit. It produced a third identity:

```text
envelope bytes    16503
envelope SHA-256  9763af8e0c6e9de29728d5fedd4290c8bf3b8bb086bb14d014ea482d0397447a
envelope FNV      771bf949
```

Consequently, the withdrawn 21,227-byte identity is explained by neither the preserved live commit nor the final 0.8.13 head. It must not be attributed to the live Collector execution unless a separate artifact with an exact provenance chain is later recovered.

## Corrected interpretation of the live execution

### Retained as PASS

- the production Apps Script endpoint returned a healthy receipt-v2 contract;
- valid engineering-only synthetic POST requests reached the endpoint;
- two distinct submission nonces received terminal `duplicate` receipts;
- both preserved receipts referenced the same session-derived file name;
- the submitted synthetic record was explicitly excluded from the human cohort.

### Not established

- which historical request originally created the stored file;
- whether the stored Drive bytes equal the preserved 16,217-byte submission;
- whether the stored Drive bytes equal either later reconstructed candidate;
- the SHA-256, byte count, or FNV checksum of the exact stored Drive file;
- Factory reconstruction of the exact stored Drive bytes.

The Collector deduplicates by session-derived file identity. A `duplicate` receipt proves convergence to an existing file name; it does not prove that the newly posted bytes equal the already stored bytes.

## Factory correction

The preserved live envelope predates the explicit transport-identity fields required by the final 0.8.13 Factory adapter. CUBE-REV 0.8.14 therefore:

1. preserves the 16,217-byte archival source unchanged;
2. accepts it only after exact SHA-256, byte-count, and FNV verification;
3. creates a separately hashed derived compatibility copy;
4. adds only explicit identity-session metadata that was semantically implicit because the outer and inner session IDs were already identical;
5. verifies that the scientific snapshot bytes are unchanged;
6. runs the final Factory on the derived copy.

This establishes a provenance-preserving archival conversion. It is not a substitute for retrieving and replaying the exact Drive-stored raw file.

## Revised 0.8.13 boundary

The corrected live portion of the 0.8.13 decision is:

> **PASS-LIVE-COLLECTOR-ENDPOINT-AND-RECEIPT-V2-DUPLICATE-CONVERGENCE / HOLD-LIVE-SUBMISSION-TO-STORED-BYTE-EQUALITY / HOLD-LIVE-STORED-RAW-IDENTITY / HOLD-LIVE-STORED-RAW-FACTORY-REPLAY**

The broader 0.8.13 decision remains production `NO_GO`.

## Scientific impact

No human-participant record was used in the live probe. The affected session was an engineering-only synthetic record with explicit cohort-exclusion markers. The correction changes the evidential interpretation and custody claim, not a human-data estimate or scientific result.

## Promotion consequence

PR #12 must not be merged or used as a production-cutover authority on the basis of its original live-custody wording. CUBE-REV 0.8.14 is the governing evidence-reconciliation layer. Production promotion remains blocked until exact stored-raw retrieval, physical-device walkthrough, and owner acceptance are completed.

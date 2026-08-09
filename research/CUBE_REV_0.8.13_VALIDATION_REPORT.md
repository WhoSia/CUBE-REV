# CUBE-REV 0.8.13 Validation Report

## Official title

**CUBE-REV 0.8.13 — Native Multi-window Browser Execution, Lease-expiry Network Ambiguity & Live Collector–Factory Reconstruction Certification**

## Official decision

> **PASS-NATIVE-MULTI-WINDOW-BROWSER / PASS-ACTIVE-SESSION-WEB-LOCKS-CAS / PASS-LEASE-EXPIRY-TWO-DELIVERY-CONVERGENCE / PASS-DETERMINISTIC-SCIENTIFIC-TO-TRANSPORT-SESSION-BRIDGE / PASS-LIVE-COLLECTOR-RECEIPT-V2-DEDUP / PASS-COLLECTOR-FACTORY-COMPATIBILITY-CONTRACT / PASS-FACTORY-RECONSTRUCTION / PASS-FACTORY-TAMPER-REJECTION / PASS-INHERITED-CONTRACTS / HOLD-LIVE-STORED-RAW-FACTORY-RETRIEVAL / HOLD-PAGEHIDE-DURABILITY / DEFAULT-CUTOVER-NO_GO**

## Problem closed by this version

CUBE-REV 0.8.12 certified active-session revision CAS and submission-lease arbitration under a deterministic simulated lock manager. It did not establish that the same contract survives a real browser implementation of `navigator.locks`, two same-origin pages, browser `storage` events, a lease that expires while the first network delivery is unresolved, the production Apps Script Collector receipt-v2 endpoint, and a Factory adapter that reconstructs the opaque cognitive response rows without treating compatibility metadata as scientific data.

CUBE-REV 0.8.13 closes those executable boundaries while keeping the production default route and frozen Collector files unchanged.

## Architecture

### Native two-page browser execution

The Playwright harness launches Chromium 140 and opens two pages under one browser context and one HTTP origin. Both pages use the browser's native Web Locks API, shared `localStorage`, and actual `storage` events. No synthetic lock manager is substituted in this suite.

The first scenario creates a same-position response race. Exactly one response is committed, the losing response is retained as conflict evidence, both pages converge to the same revision, and a simultaneous response/telemetry race preserves both the response and the telemetry event. A real `pagehide` event is also dispatched before one page closes; the previously committed response bytes remain unchanged.

### Lease-expiry network ambiguity

The second scenario completes 28 responses, saves post-task data, seals one immutable scientific snapshot, and starts a submission with a one-second test lease. The first receipt is intentionally delayed for five seconds. After lease expiry, the second page obtains generation 2 and delivers the same compatibility envelope with another 24-hex nonce.

Observed result:

- two POST deliveries;
- one transport session ID;
- one scientific session ID;
- one compatibility-envelope SHA-256;
- one Collector checksum;
- two distinct nonces;
- second receipt reaches `duplicate` first;
- delayed first receipt later reaches `stored`;
- final local state is `SUBMITTED` at lease generation 2;
- 28 responses and the immutable snapshot hash remain unchanged.

### Scientific and transport session identities

Legacy scientific sessions such as `CR0811-...` do not satisfy the existing Collector's `CR-YYYYMMDDhhmmss-12hex` transport format. The runtime therefore preserves the scientific ID inside `cognitive_snapshot.session_id` and deterministically derives a transport-only ID from:

```text
scientific session ID | participant token | sequence ID
```

and the scientific start timestamp. The outer compatibility envelope and `data_submission` both record the transport ID, original scientific ID, and bridge policy. The Python Factory independently recomputes the same identity and rejects any mismatch.

The final native evidence produced:

```text
scientific: CR0811-20260802133308-5460d2f9
transport:  CR-20260802133308-9dcf2acb9ecf
policy:     DETERMINISTIC_LEGACY_SESSION_BRIDGE_V1
```

### Canonical envelope and mutable Collector working copy

The canonical compatibility envelope is recursively frozen after internal identity checks. The existing 0.7.12 Collector client mutates `data_submission` while adding transport metadata, so the participant route supplies a deep-cloned mutable working copy to the client while retaining the canonical envelope for scientific and Factory identity checks.

A read-only verifier checks the top-level transport ID, `data_submission.transport_session_id`, original scientific ID, bridge policy, and inner snapshot identity. It no longer rewrites those fields.

This separation was required because an earlier verifier compatibility shim attempted to overwrite the frozen envelope's `session_id`, producing repeated submission failures and lease generations. The final implementation removes that mutation path.

### Collector compatibility envelope

The external result file uses the existing Collector-facing identity:

```text
project: CUBE-REV
version: 0.7.12
session_id: transport session ID
trials: 28 compatibility projections
data_submission: compatibility and transport metadata
cognitive_snapshot: immutable 0.8.13 scientific snapshot
```

Each compatibility trial is a one-to-one projection of position, stimulus ID, displayed move, opaque choice code, latency, and recorded timestamp. The inner snapshot remains the scientific source of truth.

### Factory reconstruction

The Factory adapter accepts either:

1. the inner `CR0813-COLLECTOR-PAYLOAD-1` snapshot; or
2. the complete 0.7.12 compatibility envelope.

It preserves the input bytes under `raw/`, performs blocking QC, and emits:

- `session_table.csv`;
- `trial_table.csv`;
- `telemetry_table.csv`;
- `qc_report.csv`;
- `interpreted_sessions.jsonl`;
- `analysis_manifest.json`;
- an analysis-ready ZIP.

For wrapper input it additionally requires exact equality between all 28 compatibility trials and the inner responses, verifies the deterministic transport bridge, and distinguishes `scientific_session_id` from `transport_session_id` in the session table.

## Executed certification

### Final GitHub Actions execution

- certification workflow run: `30750150463` — **SUCCESS**;
- certification job: `91502629004` — **SUCCESS**;
- baseline/calibration workflow run: `30750150466` — **SUCCESS**;
- certified code head: `96df4e1e870b1fa41126c5b8b0299d06e43bd517`;
- runner: Ubuntu 24.04.4;
- Node.js: `22.23.1`;
- Python: `3.11.15`;
- Chromium: `140.0.7339.16` through Playwright build 1187;
- workflow permission: repository contents read-only.

Required terminal markers:

```text
CR0813_ASSET_BUILD_PASS stimuli=28 choices=504 manifest=810847fe11ffcb6c17cb7a87b6951579ada128035f3f4ffc8a281478b3ece506
CR0813_NATIVE_MULTI_WINDOW_PASS cursor=2 conflict_count=1 pagehide_persisted=true
CR0813_LEASE_EXPIRY_AMBIGUITY_PASS posts=2 generation=2 status=SUBMITTED bridge=DETERMINISTIC_LEGACY_SESSION_BRIDGE_V1
CR0813_TRANSPORT_BRIDGE_PARITY ... "passed":true
CR0813_FACTORY_RECONSTRUCTION_PASS responses=28 root=collector_compatibility_envelope outputs=5
CR0813_FACTORY_RECONSTRUCTION_PASS responses=28 root=inner_scientific_snapshot outputs=5
CR0813_FACTORY_ADAPTER_TEST_PASS inner_rows=28 wrapper_rows=28 tamper_cases=5 bridge=IDENTITY_SESSION_V1
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
CR0813_NATIVE_FACTORY_CI_PASS
```

### Native delayed-receipt evidence

The two local-emulator deliveries were byte-identical:

| Field | Value |
|---|---|
| transport session | `CR-20260802133308-9dcf2acb9ecf` |
| scientific session | `CR0811-20260802133308-5460d2f9` |
| payload bytes | `21731` |
| payload SHA-256 | `57a959fd5d746e615f4e072c580d9d620b37999deaf470265e62af7edf03b40e` |
| Collector FNV checksum | `42c10379` |
| delivery 1 nonce | `8aaacf2731adcaa9de33d396` |
| delivery 2 nonce | `5fa9ed6128bae71d42b27021` |
| receipt order | second=`duplicate`, delayed first=`stored` |
| final lease generation | `2` |
| final status | `SUBMITTED` |

### Factory evidence

The native compatibility envelope reconstructed with zero blocking QC findings:

- raw/canonical envelope SHA-256: `57a959fd5d746e615f4e072c580d9d620b37999deaf470265e62af7edf03b40e`;
- inner snapshot canonical SHA-256: `3601b323d98d8570af7bf9bf58a35611c9519607145e789108b1f2c8f15dbde6`;
- analysis-ready ZIP SHA-256: `42ace938ea1b4ca265240304ef4fe9e2fe68ec2f0db5acb85a459e3b6b0050d6`;
- reconstructed response rows: 28;
- blocking QC count: 0;
- analysis eligible: true.

The independent synthetic inner-snapshot path also reconstructed 28 rows with zero blocking QC findings.

The negative matrix rejected:

1. an altered inner response position;
2. an altered compatibility choice code;
3. a mismatched outer transport session;
4. a mismatched original scientific session;
5. a mismatched transport policy.

### Final evidence artifact

- artifact ID: `8834172208`;
- artifact ZIP SHA-256: `e2ac90081b0136221526e48cef4ed4b10c30bdda16af550252c079863fc37d25`;
- compressed size: `48977` bytes;
- retained through 2026-08-16.

## Live Apps Script Collector execution

A fixed engineering-only synthetic envelope, explicitly marked `synthetic_live_cert=true` and `exclude_from_human_cohort=true`, was sent to the real Apps Script Collector. The live evidence recorded:

- Collector ID: `CUBE-REV-0712-MAIN`;
- protocol: `receipt-v2`;
- expected version: `0.7.12`;
- live workflow run: `30747246961`;
- external file name: `CR-20260802110000-0813a0b0c0d0.json`;
- envelope SHA-256: `6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3`;
- envelope FNV checksum: `f795cd8e`;
- envelope bytes: `21227`;
- inner snapshot SHA-256: `446ab20ec570140f810bcbe91660b089585f1416db5b29852f7bf6946881e2ba`;
- receipt A: `CR0712-RCP-1C74B563`;
- receipt B: `CR0712-RCP-953ECF13`;
- both receipts: `duplicate` to the same file identity.

Both final receipts are `duplicate` because an earlier contract-discovery attempt had already created the accepted file. The exact earlier request that first received `stored` was not isolated as the final certification event, so the report does not invent that attribution. The live result does establish that two distinct valid nonces over the same session and checksum converge to one Collector file identity.

## Materialized public-asset identities

| Artifact | raw SHA-256 |
|---|---|
| 0.8.13 public bank | `c6b522d3060105401feb4773a2860d70853ab8cdf2edba75b72bb5b52bb6d510` |
| 0.8.13 public config | `44aa314b85d6eacb84d7b0fb02b866c9fb3970824e3c3de54f371dbea92bdeff` |
| 0.8.13 asset manifest | `810847fe11ffcb6c17cb7a87b6951579ada128035f3f4ffc8a281478b3ece506` |
| 0.8.13 pin module | `966642169e0af785ef0a9e2ebb047615b941d636affd03bb08e0c85f0c1a0644` |

The deterministic rebuild compared every generated file byte-for-byte with the committed version and passed.

## Evidence boundary and limitations

### Certified

- actual Chromium two-page execution under one origin;
- native Web Locks serialization and browser storage-event convergence;
- one-winner response conflict handling without response loss;
- response/telemetry race preservation;
- one immutable snapshot delivered twice after lease expiry;
- stored/duplicate receipt convergence under delayed local receipt-v2 emulation;
- deterministic scientific-to-transport session bridge in JavaScript and Python;
- canonical frozen envelope plus isolated mutable Collector working copy;
- production Apps Script Collector health, valid POST, receipt polling, and duplicate convergence for an excluded synthetic session;
- Factory reconstruction of both wrapper and inner snapshot;
- exact 28-trial projection verification and five tamper rejections;
- all inherited 0.8.12 through 0.8.8 contracts;
- unchanged `collector-config.js` and `js/collector-client.js`;
- deterministic asset rebuild.

### Not certified

- direct retrieval of `CR-20260802110000-0813a0b0c0d0.json` through the connected Drive search and re-execution of the Factory on those exact stored bytes;
- guaranteed completion of asynchronous pagehide telemetry before every real browser or OS process termination;
- Chrome/Edge/Safari/Firefox cross-browser equivalence;
- storage eviction, private-mode lifetime, mobile browser suspension, or device power loss;
- human participant walkthrough;
- production default-entry replacement.

The Drive connector returned no result for the exact live file name or suffix, so direct stored-raw Factory replay remains an explicit HOLD rather than an inferred PASS. This does not negate the live Collector receipt evidence or the Factory compatibility tests, but it prevents claiming custody-complete end-to-end replay of the exact persisted bytes.

## Promotion boundary

0.8.13 is complete as a research and executable-certification version. It must remain a draft stacked PR and must not replace the production default entry. The next deployment-oriented stage must obtain the stored raw file or an owner-authorized export, run the Factory on that exact file, execute real desktop/mobile walkthroughs, and then decide whether the stacked 0.8.5–0.8.13 line is ready for controlled staging or requires compaction first.

# CUBE-REV 0.8.14 Validation Report

## Official title

**CUBE-REV 0.8.14 — Stored-raw Custody Replay, Cross-device Browser Matrix & Controlled Staging Cutover Gate**

## Official decision

> **PASS-ARCHIVAL-LIVE-SUBMITTED-BYTE-RECONSTRUCTION / PASS-0.8.13-EVIDENCE-LINEAGE-ERRATUM / PASS-PROVENANCE-PRESERVING-ARCHIVAL-FACTORY-BRIDGE / PASS-CHROMIUM-ONLY-CONTROLLED-STAGING-POLICY / PASS-FIREFOX-WEBKIT-FAIL-CLOSED / PASS-DYNAMIC-PERSISTED-LEASE-EXPIRY-TAKEOVER / PASS-DETERMINISTIC-STAGING-CANDIDATE / PASS-INHERITED-CONTRACTS / HOLD-EXACT-STORED-RAW-CUSTODY-REPLAY / HOLD-PHYSICAL-DEVICE-WALKTHROUGH / HOLD-OWNER-ACCEPTANCE / DEFAULT-CUTOVER-NO_GO**

## Executive finding

CUBE-REV 0.8.14 completed the automated research and controlled-staging work that could be performed without owner-only Drive access or physical-device interaction. It also found two material promotion blockers that were not visible in the original 0.8.13 seal.

First, the preserved GitHub Actions artifact from the actual live Collector workflow does not match the payload identities later committed into the 0.8.13 evidence ledger. The exact archival submission was reconstructed from the preserved snapshot and historical construction code, the discrepancy was documented in a formal erratum, and the unsupported later identity was withdrawn as evidence of that live execution.

Second, repeated two-page races showed that the 0.8.13 one-winner plus conflict-evidence contract was not consistently preserved in Firefox or WebKit. Native Web Locks serialized an explicit lock probe and final pages converged, but both callers sometimes returned `RESPONSE_APPLIED`, which can erase the losing response and its conflict evidence. The generated 0.8.14 staging route therefore activates only Chromium-family profiles and fails closed before scientific runtime boot on Firefox, WebKit, and unrecognized engines.

A third issue appeared during final sealing: the inherited 0.8.13 lease-expiry test depended on a fixed 1,400ms delay and an already-open second tab. One cleanup-head execution observed only the first POST, while an identical rerun passed. The rerun was not accepted as sufficient evidence. The final 0.8.14 Gate reads the persisted `lease_expires_at`, waits until that exact timestamp plus 250ms, opens a fresh second page, and repeats takeover four times.

The deterministic staging candidate is complete and production files remain untouched. Exact Drive-stored raw replay, physical-device walkthrough, and owner acceptance remain blocking gates, so production cutover is **NO_GO**.

## Final executable certification

The final executable evidence was produced at:

```text
certified executable head
25371c6479e074d3c7d0ad3501beffeb08f28cfb

0.8.14 workflow run
30754439979 — SUCCESS

certification job
91514086682 — SUCCESS

baseline/calibration workflow
30754439978 — SUCCESS
```

Final evidence artifact:

```text
artifact ID    8835501173
ZIP SHA-256    c81b46125916aadb9be55085a68bedf70a3bfbfbb5991e85d54096061660e093
compressed     202501 bytes
retention      through 2026-08-16
```

The workflow operated with repository contents read-only. No live synthetic submission was sent by 0.8.14.

## RAVEL closure

### Discover

The intended boundaries were:

1. retrieve and Factory-replay the exact Collector-stored raw file;
2. execute a cross-engine desktop/mobile browser matrix;
3. build and evaluate a controlled staging candidate.

The connected Drive identity could not read the Collector-owned file `CR-20260802110000-0813a0b0c0d0.json`. Rather than infer stored bytes from duplicate receipts, the audit recovered the preserved live-workflow artifact and separated submitted-byte evidence from stored-byte custody.

### Plan

The version was divided into independent Gates:

- archival submission reconstruction and evidence-lineage audit;
- provenance-preserving Factory conversion;
- repeated native browser policy matrix;
- persisted-expiry lease takeover certification;
- deterministic staging packaging and cutover evaluation.

A failure in one Gate could not be converted into a pass by weakening another.

### Execute

The branch `cube-rev-0.8.14-custody-device-staging` added:

- runtime-pinned archival live-envelope reconstruction;
- archival workflow evidence preservation;
- a lineage auditor and 0.8.13 erratum;
- an optional exact stored-raw replay path;
- a pinned archival-to-final-Factory bridge;
- a deterministic 0.8.14 participant staging route;
- repeated Chromium, Firefox, and WebKit two-page diagnostics;
- fail-closed unsupported-engine routing;
- a persisted-expiry lease test without fixed sleeps;
- deterministic staging ZIP construction and rollback metadata;
- a machine-evaluated production cutover Gate.

### Verify

The final workflow passed:

- exact archival submitted-byte reconstruction;
- 0.8.13 evidence-lineage inconsistency detection;
- archival Factory bridge and 28-row Factory reconstruction;
- six-cell browser policy matrix;
- eight repeated active Chromium races;
- four fail-closed profile checks;
- four persisted-expiry takeover iterations with eight POSTs;
- inherited 0.8.8–0.8.12 contracts;
- deterministic 22-file staging candidate build;
- protected-file and baseline checks.

### Iterate

The browser policy was narrowed as counterexamples appeared:

- all-engine active hypothesis: rejected;
- Firefox active: rejected;
- desktop WebKit active: rejected;
- iOS WebKit emulation active: rejected;
- final policy: Chromium-only active, Firefox/WebKit/unknown engines fail closed.

The custody claim was also narrowed:

- exact stored raw replay: not established;
- exact archival submitted-byte reconstruction: established;
- later 0.8.13 payload identity: unexplained and withdrawn as live evidence;
- provenance-preserving archival Factory conversion: established.

The lease Gate was strengthened:

- fixed 1,400ms wait: removed from the 0.8.14 promotion Gate;
- persisted expiry timestamp plus 250ms: adopted;
- already-open retry tab: replaced by a fresh second page;
- single pass: replaced by four fresh-context repetitions.

## Track A — Stored-raw custody and evidence lineage

### Authoritative archival execution

The preserved live workflow was:

| Field | Value |
|---|---|
| workflow run | `30747246961` |
| workflow head | `70e68aa2a768972d31882e0f1c2a483cfd9ca9bc` |
| artifact ID | `8833272340` |
| artifact ZIP SHA-256 | `c046f432a4eaa075fbc8c2e7ffafd4b363f3aa5ef79d204a0a5544472f920575` |
| session/file identity | `CR-20260802110000-0813a0b0c0d0` |
| responses/trials | 28 |

Exact preserved identities:

```text
snapshot bytes      6481
snapshot SHA-256    5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83

envelope bytes      16217
envelope SHA-256    6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9
envelope FNV-1a32   c8cda746
```

Independent replay reproduced all three envelope identities exactly:

```text
PASS_ARCHIVAL_LIVE_SUBMITTED_BYTE_RECONSTRUCTION
```

### Evidence-lineage discrepancy

The committed 0.8.13 ledger instead claimed:

```text
envelope bytes      21227
envelope SHA-256    6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3
envelope FNV-1a32   f795cd8e
snapshot SHA-256    446ab20ec570140f810bcbe91660b089585f1416db5b29852f7bf6946881e2ba
```

The final 0.8.13 runtime against the same fixed snapshot produced a third identity:

```text
envelope bytes      16503
envelope SHA-256    9763af8e0c6e9de29728d5fedd4290c8bf3b8bb086bb14d014ea482d0397447a
envelope FNV-1a32   771bf949
```

Thus the 21,227-byte identity was reproduced by neither the historical live commit nor the final 0.8.13 head. The committed receipt codes also differed from the preserved artifact. The audit returned:

```text
PASS_DETECTED_0_8_13_LIVE_EVIDENCE_LINEAGE_INCONSISTENCY_REQUIRES_ERRATUM
```

The governing correction is:

```text
research/CUBE_REV_0.8.13_ERRATUM_FROM_0.8.14.md
```

### Corrected live claim

Retained:

- the production endpoint exposed the expected receipt-v2 contract;
- valid engineering-only synthetic POSTs reached it;
- two distinct nonces received terminal `duplicate` receipts;
- both preserved receipts referenced the same session-derived filename;
- the record was excluded from human-cohort analysis.

Not established:

- which historical request created the file;
- equality between any submitted candidate and the stored Drive bytes;
- the stored file's byte count, SHA-256, or FNV checksum;
- Factory replay of the exact stored file.

A `duplicate` receipt proves convergence to an existing file identity, not equality with the pre-existing stored bytes.

### Exact stored raw status

The connected Drive account could not retrieve the raw file. The custody report therefore records three candidates without selecting one as the stored identity:

1. archival live submission: 16,217 bytes / `6aa9d1e3…` / `c8cda746`;
2. final runtime observation: 16,503 bytes / `9763af8e…` / `771bf949`;
3. withdrawn ledger claim: 21,227 bytes / `6aa9d1e38…` / `f795cd8e`.

Official result:

```text
HOLD_DIRECT_STORED_RAW_UNAVAILABLE_THREE_IDENTITY_CANDIDATES_RECORDED
```

## Track B — Provenance-preserving archival Factory bridge

The archival live envelope predates explicit transport-identity fields required by the final 0.8.13 Factory. The source was not edited in place. The bridge:

1. accepts only the exact archival source fingerprint;
2. preserves the 16,217-byte source unchanged;
3. creates a separately hashed derived compatibility copy;
4. adds only explicit identity-session metadata already implied by equal outer and inner session IDs;
5. verifies that the scientific snapshot is unchanged;
6. runs the final Factory on the derived copy.

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| archival source | `6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9` | 16,217 |
| derived Factory input | `5627d14d7ca654f99b91cefcbeb6f6f31a8588a9809b819653fb69c437e9d0c0` | 16,503 |
| scientific snapshot before/after | `5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83` | unchanged |

Result:

```text
PASS_PINNED_ARCHIVAL_LIVE_FACTORY_BRIDGE
```

Both the bridged archival envelope and the final-runtime observation reconstructed 28 response rows with zero blocking QC findings. This proves compatibility of the known candidate bytes, not identity with the unavailable Drive raw.

## Track C — Browser engine and device-emulation policy

### Contract

For two same-origin pages racing on the same position, the required result is:

```text
one caller: RESPONSE_APPLIED
one caller: RESPONSE_CONFLICT
one stored response
one conflict-evidence record
both pages converge
```

Final convergence alone is insufficient when both callers return `RESPONSE_APPLIED`, because the losing response and the fact of conflict may disappear from the scientific record.

### Parent-route diagnostics

The original 0.8.13 route was tested six times per non-Chromium profile.

| Engine profile | Dual applied | Correct winner/conflict | Final incoherence | Explicit lock probe serialized |
|---|---:|---:|---:|---|
| Firefox desktop | 5/6 | 1/6 | 0/6 | yes |
| WebKit desktop | 1/6 | 5/6 | 0/6 | yes |
| WebKit iPhone emulation | 2/6 | 4/6 | 0/6 | yes |

The lock probe serialized, but the read/write protocol did not consistently provide fresh one-winner semantics across those engines.

### Final policy

Active automated profiles:

- Chromium desktop;
- Chromium Pixel 7/Android emulation.

Fail-closed before runtime boot:

- Firefox desktop;
- Firefox compact/mobile viewport;
- WebKit desktop;
- WebKit iPhone emulation;
- unrecognized engines.

Each blocked profile was required to show:

- redirect to the unsupported-browser route;
- no scientific runtime hook;
- no begin control;
- zero `cube-rev*` local-storage keys;
- `state_mutation_authorized=false`.

### Active repetition

| Profile | Fresh races | Correct winner/conflict | Page convergence | Pagehide response preserved |
|---|---:|---:|---:|---:|
| Chromium desktop | 4 | 4 | 4 | 4 |
| Chromium Pixel 7 emulation | 4 | 4 | 4 | 4 |

Aggregate:

```text
active cells          2
fail-closed cells     4
active races          8/8 PASS
matrix cells          6/6 PASS
physical devices      not certified
```

Result:

```text
PASS_CONTROLLED_STAGING_BROWSER_POLICY_MATRIX
```

## Track D — Persisted-expiry lease takeover certification

### Why the inherited fixed-delay test was replaced

The original 0.8.13 delayed-receipt test waited a fixed 1,400ms and reused a second page that had already been open while page A was sending. On the 0.8.14 cleanup head, one execution observed only the first POST within the assertion window. An identical rerun passed, showing that retry alone could hide timing ambiguity.

The final 0.8.14 Gate uses persisted state as the clock authority:

1. page A completes 28 responses and seals one snapshot;
2. page A obtains generation 1 and sends;
3. the test reads `submission_control.lease_expires_at` from stored state;
4. it waits until that timestamp plus 250ms;
5. it opens a fresh page B;
6. page B obtains generation 2 and sends the same snapshot with another nonce;
7. page B confirms `duplicate` and reaches `SUBMITTED`;
8. the delayed generation-1 owner is fenced by `STALE_SUBMISSION_LEASE` when it later confirms.

Four fresh contexts were executed:

| Iteration | Margin after expiry | POSTs | Pair identity | Final generation | State |
|---:|---:|---:|---|---:|---|
| 1 | 252ms | 2 | identical | 2 | `SUBMITTED` |
| 2 | 252ms | 2 | identical | 2 | `SUBMITTED` |
| 3 | 252ms | 2 | identical | 2 | `SUBMITTED` |
| 4 | 253ms | 2 | identical | 2 | `SUBMITTED` |

Aggregate:

```text
iterations                         4/4 PASS
total POSTs                        8
fixed sleep used                   false
payload pairs identical            true
all final lease generations        2
terminal receipts per iteration    duplicate + stored
responses per snapshot             28
```

Different iterations had different session-specific hashes, as expected. Within each iteration the two deliveries were byte-, SHA-256-, checksum-, and session-identical and used distinct nonces.

Final marker:

```text
CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false
```

This is the 0.8.14 promotion Gate. The earlier fixed-delay 0.8.13 result remains historical evidence but is not the final cutover authority.

## Track E — Controlled staging candidate

The builder packages the generated 0.8.14 route as `index.html` inside an artifact-only candidate. It does not change repository production `index.html`.

| Field | Value |
|---|---|
| candidate files | 22 |
| fingerprint SHA-256 | `0b8ae0679a6033b8cd4862ef6de81fe2f1ee8fde8b7bfd1ff3dee7616722fc32` |
| ZIP SHA-256 | `80db6740754297b51b87c6542a4ef6d5f3958f5da2c0e4ce65989a1768c78520` |
| ZIP bytes | 68,054 |
| production entry modified | no |
| Collector config/client modified | no |
| automatic deployment authorized | no |

The candidate contains:

- the 0.8.14 gated entry;
- the unsupported-browser page;
- frozen Collector files;
- 0.8.13 scientific runtime and pinned assets;
- archival Factory bridge;
- 0.8.13 erratum and archival evidence;
- governing 0.8.14 browser policy;
- staging provenance and rollback plan.

Result:

```text
PASS_DETERMINISTIC_STAGING_CANDIDATE_BUILD
```

## Track F — Inherited contracts

The final workflow ran the parent Chromium serialization scenario, the dynamic persisted-expiry suite, and inherited state/migration contracts:

```text
CR0813_NATIVE_MULTI_WINDOW_PASS
CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

The fixed-delay second scenario in the parent 0.8.13 test file is no longer an 0.8.14 Gate. The baseline/calibration workflow also passed on the same executable head.

## Cutover Gate

Automated pass gates:

- archival submitted-byte reconstruction;
- final-runtime observation;
- evidence-lineage discrepancy detection and erratum;
- archival Factory bridge;
- Chromium-only browser policy matrix;
- eight repeated active Chromium races;
- four fail-closed profile checks;
- four dynamic persisted-expiry takeovers with eight POSTs;
- deterministic staging bundle;
- protected production entry and Collector files unchanged;
- inherited contracts and baseline.

Blocking gates:

```text
exact_stored_raw_custody_replay
physical_device_walkthrough
owner_acceptance_walkthrough
```

Final machine result:

```text
CONTROLLED_STAGING_CANDIDATE_PASS_PRODUCTION_CUTOVER_NO_GO
```

## Internal review committee

**Implementer:** Produced a deterministic staging candidate and reproducible automated suite without changing production or Collector sources.

**Skeptical reviewer:** Rejected three unsupported shortcuts: duplicate receipt as byte proof, later prose as stronger than preserved artifacts, and one successful non-Chromium run as engine certification.

**Evidence auditor:** Preserved the archival artifact as authoritative, published an erratum, and retained exact custody as HOLD.

**Browser-contract auditor:** Refused final-state convergence as a substitute for one-winner return semantics and conflict evidence.

**Timing auditor:** Replaced a fixed wait and lucky rerun with persisted-expiry timing and four fresh-context repetitions.

**Authority auditor:** No PR was merged, no staging artifact deployed, and no production route or Collector source changed.

## Limitations

Not certified:

- exact bytes of the Collector-owned Drive file;
- Factory execution on that exact file;
- real Chrome/Edge desktop hardware;
- real Android Chromium hardware;
- real Safari/WebKit or Firefox execution;
- browser suspension, OS kill, storage eviction, or power loss on physical devices;
- participant walkthrough;
- owner acceptance;
- deployment or rollback against a public staging URL.

## Promotion boundary

CUBE-REV 0.8.14 is complete as an automated research, evidence-reconciliation, browser-policy, lease-takeover, and staging-candidate version. It is not a production release.

Promotion requires exact stored-raw export or owner-authorized retrieval, physical Chromium-family walkthroughs, explicit owner acceptance, and a separately authorized staging deployment ceremony with rollback verification.

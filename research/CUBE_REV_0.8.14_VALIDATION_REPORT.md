# CUBE-REV 0.8.14 Validation Report

## Official title

**CUBE-REV 0.8.14 — Stored-raw Custody Replay, Cross-device Browser Matrix & Controlled Staging Cutover Gate**

## Official decision

> **PASS-ARCHIVAL-LIVE-SUBMITTED-BYTE-RECONSTRUCTION / PASS-0.8.13-EVIDENCE-LINEAGE-ERRATUM / PASS-PROVENANCE-PRESERVING-ARCHIVAL-FACTORY-BRIDGE / PASS-CHROMIUM-ONLY-CONTROLLED-STAGING-POLICY / PASS-FIREFOX-WEBKIT-FAIL-CLOSED / PASS-DETERMINISTIC-STAGING-CANDIDATE / PASS-INHERITED-CONTRACTS / HOLD-EXACT-STORED-RAW-CUSTODY-REPLAY / HOLD-PHYSICAL-DEVICE-WALKTHROUGH / HOLD-OWNER-ACCEPTANCE / DEFAULT-CUTOVER-NO_GO**

## Executive finding

CUBE-REV 0.8.14 did not merely extend 0.8.13. It audited whether 0.8.13's live-Collector evidence could support a custody-complete staging decision and found two promotion-blocking facts.

First, the preserved GitHub Actions artifact from the actual live workflow does not match the payload identities later committed into the 0.8.13 evidence ledger. The exact archival live submission was independently reconstructed, the mismatch was documented in a formal erratum, and the unexplained later identity was withdrawn as evidence of that live execution.

Second, the 0.8.13 active-session implementation did not preserve its one-winner plus conflict-evidence contract consistently in repeated Firefox and WebKit two-page races. Native Web Locks serialized an explicit lock probe, and the final pages converged, but both callers sometimes returned `RESPONSE_APPLIED`. Final convergence alone is insufficient because the losing choice and its conflict evidence can be lost. The controlled staging route therefore activates only Chromium-family profiles and fails closed before session boot on Firefox, WebKit, and unrecognized engines.

A deterministic staging candidate was built without changing production `index.html`, `collector-config.js`, or `js/collector-client.js`. Exact Drive-stored raw replay, physical-device walkthrough, and owner acceptance remain blocking gates, so production cutover is `NO_GO`.

## RAVEL closure

### Discover

The version began with three intended boundaries:

1. retrieve the exact Collector-stored raw file and replay it through Factory;
2. execute a cross-engine desktop/mobile browser matrix;
3. construct a controlled staging candidate and evaluate cutover readiness.

The connected Drive search could not read the Collector-owned folder or locate the exact file `CR-20260802110000-0813a0b0c0d0.json`. Rather than infer the stored bytes from a duplicate receipt, the audit recovered the preserved live-workflow artifact and separated submitted-byte evidence from stored-byte custody.

### Plan

The work was divided into four independent gates:

- archival submission reconstruction and evidence-lineage audit;
- provenance-preserving Factory conversion;
- native engine/device-emulation policy matrix;
- deterministic staging packaging and explicit cutover evaluation.

A failure in one gate was not allowed to be converted into a pass by weakening another gate.

### Execute

The branch `cube-rev-0.8.14-custody-device-staging` added:

- runtime-pinned live-envelope reconstruction;
- exact archival workflow evidence preservation;
- an evidence-lineage auditor and 0.8.13 erratum;
- an optional exact stored-raw replay path;
- a pinned archival-to-final-Factory bridge that preserves source bytes and scientific snapshot bytes;
- a deterministic 0.8.14 participant staging route;
- repeated Chromium, Firefox, and WebKit two-page diagnostics;
- fail-closed unsupported-engine routing;
- deterministic staging ZIP construction and rollback metadata;
- a machine-evaluated production cutover gate.

### Verify

The final executable head was:

```text
b5712e1d30f2e0b0cc0b411fdca811d4c6158992
```

Final successful executions:

| Execution | Identifier | Result |
|---|---:|---|
| 0.8.14 custody/device/staging workflow | `30753219920` | SUCCESS |
| certification job | `91510832942` | SUCCESS |
| baseline/calibration workflow | `30753219950` | SUCCESS |
| evidence artifact | `8835133893` | uploaded |

The evidence artifact had:

```text
ZIP SHA-256  96e188a9e25c36481a8c442787b3ed2b7f2803f4308d1ceea09929df1f8a4932
size          195385 bytes
retention     through 2026-08-16
```

### Iterate

The browser policy was narrowed repeatedly as counterexamples appeared:

- initial all-engine active hypothesis: rejected;
- Firefox active: rejected after repeated dual-apply;
- desktop WebKit active: rejected after intermittent dual-apply;
- iOS WebKit emulation active: rejected after repeated testing exposed dual-apply;
- final policy: Chromium-only active, all Firefox/WebKit profiles fail closed.

The custody claim was also narrowed:

- exact stored raw replay: not established;
- exact archival submitted-byte reconstruction: established;
- later 0.8.13 payload identity: unexplained and withdrawn as live evidence;
- archival submitted envelope converted through a separately hashed provenance bridge: established.

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
| response/trial count | 28 |

The exact archival live-envelope construction was independently replayed from the preserved fixed snapshot and the live-probe construction code.

```text
snapshot bytes      6481
snapshot SHA-256    5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83

envelope bytes      16217
envelope SHA-256    6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9
envelope FNV-1a32   c8cda746
```

The replay matched all archival identities exactly and emitted:

```text
PASS_ARCHIVAL_LIVE_SUBMITTED_BYTE_RECONSTRUCTION
```

### Evidence-lineage discrepancy

The committed 0.8.13 live ledger had instead claimed:

```text
envelope bytes      21227
envelope SHA-256    6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3
envelope FNV-1a32   f795cd8e
snapshot SHA-256    446ab20ec570140f810bcbe91660b089585f1416db5b29852f7bf6946881e2ba
```

Executing the final 0.8.13 runtime against the same fixed snapshot produced a third identity:

```text
envelope bytes      16503
envelope SHA-256    9763af8e0c6e9de29728d5fedd4290c8bf3b8bb086bb14d014ea482d0397447a
envelope FNV-1a32   771bf949
```

Therefore, the committed 21,227-byte identity was reproduced by neither the actual live-workflow commit nor the final 0.8.13 head. Its receipt codes also differed from the preserved artifact. The lineage auditor returned:

```text
PASS_DETECTED_0_8_13_LIVE_EVIDENCE_LINEAGE_INCONSISTENCY_REQUIRES_ERRATUM
```

The formal correction is stored at:

```text
research/CUBE_REV_0.8.13_ERRATUM_FROM_0.8.14.md
```

### Corrected live claim

Retained:

- the production Apps Script endpoint exposed the expected receipt-v2 contract;
- valid engineering-only synthetic POSTs reached the endpoint;
- two distinct nonces received terminal `duplicate` receipts;
- both preserved receipts referenced the same session-derived filename;
- the record was excluded from human-cohort analysis.

Not established:

- which earlier request created the file;
- equality between any submitted candidate and the stored Drive bytes;
- the stored file's byte count, SHA-256, or FNV checksum;
- Factory replay of the exact stored file.

A duplicate receipt is a file-identity convergence result, not a stored-byte equality proof.

### Exact stored raw status

The connected Drive account could not retrieve the Collector-owned raw file. The custody report therefore records three candidate identities without selecting one as the stored identity:

1. archival live submission: 16,217 bytes / `6aa9d1e3…` / `c8cda746`;
2. final 0.8.13 runtime observation: 16,503 bytes / `9763af8e…` / `771bf949`;
3. withdrawn 0.8.13 ledger claim: 21,227 bytes / `6aa9d1e38…` / `f795cd8e`.

Official custody result:

```text
HOLD_DIRECT_STORED_RAW_UNAVAILABLE_THREE_IDENTITY_CANDIDATES_RECORDED
```

## Track B — Provenance-preserving archival Factory bridge

The archival live envelope predates the explicit identity-session fields required by the final 0.8.13 Factory adapter. Altering the raw source in place would have destroyed custody evidence. The 0.8.14 bridge instead performs the following sequence:

1. accepts only the exact archival source fingerprint;
2. preserves the 16,217-byte source unchanged;
3. creates a separately hashed derived compatibility copy;
4. adds only explicit identity-session metadata that was already semantically implied by identical outer and inner session IDs;
5. verifies the scientific snapshot bytes are unchanged;
6. runs the final Factory on the derived copy.

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| archival source | `6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9` | 16,217 |
| derived Factory input | `5627d14d7ca654f99b91cefcbeb6f6f31a8588a9809b819653fb69c437e9d0c0` | 16,503 |
| scientific snapshot before and after | `5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83` | unchanged |

The bridge returned:

```text
PASS_PINNED_ARCHIVAL_LIVE_FACTORY_BRIDGE
```

Both the bridged archival envelope and the independently observed final-runtime envelope reconstructed 28 response rows through the final Factory with no blocking QC finding. This proves compatibility of the known candidate bytes, not identity with the unavailable Drive-stored raw file.

## Track C — Cross-engine and device-emulation matrix

### Scientific contract under test

For two same-origin pages racing to answer the same position, the required result is:

```text
one caller: RESPONSE_APPLIED
one caller: RESPONSE_CONFLICT
one stored response
one conflict-evidence record
both pages converge
```

A final converged state is not enough when both callers return `RESPONSE_APPLIED`, because the losing answer and the fact of conflict may disappear from the research record.

### Parent-route diagnostic

The original 0.8.13 participant route was tested in six fresh browser contexts per non-Chromium engine profile.

| Engine profile | Dual `RESPONSE_APPLIED` | Correct one-winner/conflict | Final incoherence | Explicit lock probe serialized |
|---|---:|---:|---:|---|
| Firefox desktop | 5/6 | 1/6 | 0/6 | yes |
| WebKit desktop | 1/6 | 5/6 | 0/6 | yes |
| WebKit iPhone emulation | 2/6 | 4/6 | 0/6 | yes |

Earlier independent runs had already observed dual-apply in each family. The final repetition confirmed that it was not a single lucky or unlucky execution.

The explicit lock probe serialized in all three profiles. The evidence therefore does not support the claim that native Web Locks were entirely absent. It shows that the current 0.8.13 read/write protocol did not consistently provide fresh one-winner semantics across these engines despite lock serialization.

### Final controlled-staging policy

The generated route `participant-cognitive-mode-0.8.14.html` applies a browser gate before scientific runtime boot.

Active automated profiles:

- Chromium desktop;
- Chromium Pixel 7 emulation.

Fail-closed profiles:

- Firefox desktop;
- Firefox compact/mobile viewport;
- WebKit desktop;
- WebKit iPhone 14 emulation;
- unrecognized engines.

Fail-closed verification required all of the following:

- redirect to `unsupported-browser-0.8.14.html`;
- no scientific runtime test hook;
- no begin control;
- no `cube-rev*` local-storage key;
- `state_mutation_authorized=false`.

### Active Chromium repetition

Each active profile executed four fresh-context same-position races and pagehide checks.

| Profile | Race repetitions | One-winner/conflict | Final page convergence | Pagehide response bytes preserved |
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

Matrix result:

```text
PASS_CONTROLLED_STAGING_BROWSER_POLICY_MATRIX
```

This is an automated engine/device-emulation policy certification, not a claim about real Android, iPhone, iPad, or desktop hardware.

## Track D — Controlled staging candidate

The deterministic staging builder packages the generated 0.8.14 route as `index.html` inside an artifact-only candidate. It does not change the repository's production `index.html`.

Staging identities:

| Field | Value |
|---|---|
| candidate files | 21 |
| candidate fingerprint SHA-256 | `254b6d327c3d4713d0b2b923fc2bcdaebe4a0c5b1ffbb7407de9cabecb4e2c59` |
| staging ZIP SHA-256 | `0dba4a7f5b36a93084e327fc4b462cbfb760b14fed64d65b5093e7c6d42980bc` |
| staging ZIP bytes | 66,618 |
| production default entry modified | no |
| Collector config/client modified | no |
| automatic deployment authorized | no |

The candidate includes:

- the 0.8.14 gated staging entry;
- the fail-closed unsupported-browser page;
- the frozen Collector files;
- the 0.8.13 scientific runtime and pinned assets;
- the archival Factory bridge;
- the 0.8.13 erratum and archival evidence record;
- staging provenance and rollback plan.

Result:

```text
PASS_DETERMINISTIC_STAGING_CANDIDATE_BUILD
```

## Track E — Inherited contracts

The final workflow re-executed the parent native Chromium suite and all inherited contracts:

```text
CR0813_NATIVE_MULTI_WINDOW_PASS
CR0813_LEASE_EXPIRY_AMBIGUITY_PASS
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

The baseline/calibration workflow also completed successfully on the same head.

## Cutover gate

Machine-evaluated pass gates:

- archival live submitted-byte reconstruction;
- final-runtime observation;
- evidence-lineage discrepancy detection;
- published 0.8.13 erratum;
- provenance-preserving archival Factory bridge;
- Chromium active-execution policy;
- Firefox fail-closed policy;
- WebKit fail-closed policy;
- eight repeated active-profile races;
- four fail-closed profile checks;
- deterministic staging bundle;
- production entry untouched;
- Collector untouched.

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

### Implementer

The version produced a deployable-in-principle staging candidate while leaving production and Collector files untouched. It also built a deterministic restart path for every automated gate.

### Skeptical reviewer

The version rejected three initially attractive but unsupported conclusions: that a duplicate receipt proves byte equality, that the 0.8.13 committed live hash came from the preserved live run, and that WebKit mobile emulation could remain active after one successful pass.

### Evidence auditor

The preserved workflow artifact was treated as stronger evidence than later prose. The discrepancy was not hidden or overwritten; it was promoted into a formal erratum and a blocking custody boundary.

### Browser-contract auditor

Final-state convergence was not accepted as a substitute for one-winner return semantics and conflict preservation. Firefox and WebKit were blocked before state creation rather than allowed with a warning after the fact.

### Authority auditor

No production route, Collector client, or Collector configuration was changed. No PR was merged. The staging candidate is an artifact and draft-PR object only.

## Limitations

Not certified in 0.8.14:

- exact bytes of the Collector-owned Drive file;
- Factory execution on that exact stored file;
- real Chrome/Edge desktop hardware;
- real Android Chrome/Edge hardware;
- real Safari/iOS or Firefox execution;
- browser background suspension, OS kill, storage eviction, or device power loss on physical devices;
- participant walkthrough;
- owner acceptance;
- production deployment or rollback rehearsal against a public staging URL.

## Promotion boundary

CUBE-REV 0.8.14 is complete as an automated research, evidence-reconciliation, browser-policy, and staging-candidate version. It is not a production release.

The next promotion attempt must not treat the staging ZIP as self-authorizing. It requires exact stored-raw export or owner-authorized retrieval, physical Chromium-family walkthroughs, owner acceptance, and an explicit deployment ceremony with rollback verification.

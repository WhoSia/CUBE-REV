# CUBE-REV 0.8.5 Recovery Checkpoint

## Version

**CUBE-REV 0.8.5 — Participant-facing Cognitive Mode Integration, Legacy Fixed-set Retirement & Resume-safe UX Certification**

## Recovery verdict

- Durable research completion currently ends at **CUBE-REV 0.8.4**.
- The participant-facing repository baseline on `main` remains **v0.7.22**.
- The 0.8.5 title, objectives, and operating constraints were specified, but no durable 0.8.5 implementation/certification artifact was found before the interrupted response.
- Therefore 0.8.5 is resumed from **RECOVERED-SCOPE / IMPLEMENTATION-NOT-YET-CERTIFIED**, not from a claimed completed state.

## Parent evidence recovered from 0.8.0–0.8.4

1. **0.8.0** established the Bayesian robustness/protocol-lock layer with a 128,000-row simulation program across N=4 and N=8 designs.
2. **0.8.1** identified fixed-seed retrievability risk and downgraded unsupported cases rather than silently treating them as valid.
3. **0.8.2** rebuilt weak-prior robustness outputs after raw-data integrity concerns, using a smaller independently auditable simulation package.
4. **0.8.3** applied a wrong-operator robustness gate. Irreversible main-result validity did not pass; weighted fallback and context-sensitive Bayesian endpoints were retained as restricted evidence.
5. **0.8.4** refined the first official-run architecture: two collectors with N=4 each, total N=8; fixed-seed baseline retained; cognitive/energy-aware extensions kept observational; owner dry-run, resume simulation, CPU-stress checks, participant form schema, log-contract validation, and a 0.8.5 decision packet were produced.

## User-authorized operating constraints recovered at the interruption boundary

1. The new UI syntax and JSON must remain compatible with the existing Collector/Factory path.
2. `collector-config.js`, the Collector endpoint, and the transport implementation are frozen unless a separate explicit migration is authorized.
3. All participant-visible and participant-payload UI version labels must move together to `0.8.5`; however, the research condition must not be inferred from a display version string because Factory compression may erase that distinction.
4. Research-critical condition identifiers must therefore be explicit additive fields.
5. When additional data are needed, the participant UI may be iteratively changed and committed so that the intended randomized condition appears as the ordinary/default experience.
6. Resume must preserve the original assignment and must never silently rerandomize a participant.

## 0.8.5 target invariants

### I-1. Collector freeze

No change to:

- `collector-config.js`
- Collector endpoint semantics
- queue/retry transport semantics in `js/collector-client.js`

The integration layer may only add fields to the application payload before submission.

### I-2. Factory-safe condition identity

Every new-session payload must carry an additive object equivalent to:

```json
{
  "research_condition": {
    "schema_version": "cube-rev.cognitive-mode/1",
    "condition_id": "<catalog-defined-id>",
    "assignment_id": "<stable-id>",
    "assignment_strategy": "<strategy-version>",
    "assignment_source": "new",
    "resume_locked": true,
    "legacy_fixed_set_retired": true
  }
}
```

The exact cognitive-mode catalog and allocation weights must be imported from the recovered 0.8.5 decision packet; they must not be guessed or hard-coded from memory.

### I-3. Resume-safe assignment

Assignment resolution order:

1. Read a valid persisted 0.8.5 assignment bound to the stable session identifier.
2. If the session is a recognized legacy session, execute the explicit legacy migration policy.
3. For a genuinely new session, allocate once, persist atomically, then render.
4. If persistence fails, use a documented deterministic fallback keyed by a stable non-sensitive session identifier; record `assignment_source = deterministic_fallback`.
5. On every resume, verify that the reconstructed condition equals the first persisted condition. A mismatch is a blocking contract failure, not a warning.

### I-4. Legacy fixed-set retirement

- New sessions must not enter the legacy fixed-set path.
- Resumed legacy sessions must remain interpretable and must not be rewritten as if they had been randomized under 0.8.5.
- Migration provenance must be explicit, for example `assignment_source = legacy_resumed` or `legacy_migrated`, according to the final policy.
- Historical payloads remain immutable.

### I-5. Version consistency

The following must agree:

- visible UI version
- runtime/application version
- payload UI version
- local persistence schema version
- QA fixture expected version

Collector/transport versioning is independently frozen and must not be cosmetically rewritten.

## Required implementation modules

1. `js/cognitive-mode-assignment.js`
   - catalog validation
   - one-time assignment
   - deterministic fallback
   - serialization and validation
2. `js/resume-contract.js`
   - resume-state validation
   - legacy recognition/migration
   - mismatch blocking and audit event generation
3. participant UI integration
   - participant-safe presentation
   - no research jargon required from participants
   - ordinary/default-flow randomization
4. additive payload bridge
   - attach `research_condition`
   - preserve all pre-existing fields and transport calls
5. certification harness
   - fresh session, reload, crash/restart, duplicate tabs, storage denial, partial/corrupt state, legacy resume, queue retry, and Factory-normalized payload tests

## Minimum certification matrix

| Test family | Required cases | Pass criterion |
|---|---:|---|
| Version consistency | all UI/runtime/payload/persistence locations | exact 0.8.5 agreement; Collector version untouched |
| New-session assignment | repeated clean sessions | valid catalog member; exactly one assignment per session |
| Resume identity | reload/crash/restart | zero condition changes |
| Duplicate-tab race | concurrent startup | one canonical assignment or explicit blocking failure |
| Storage degradation | unavailable/quota/corruption | deterministic documented fallback; provenance logged |
| Legacy retirement | new and legacy sessions | no new legacy entry; old sessions remain interpretable |
| Payload compatibility | baseline/stress/both and pause-resume | pre-existing payload fields preserved; additive fields accepted |
| Queue/retry | offline then recovery | condition identity invariant across retransmission |
| Factory normalization | compressed/normalized export | research condition remains separately recoverable |
| N=8 pilot balance | final catalog-dependent allocation | prespecified balance rule satisfied or deviation explicitly audited |

## Promotion gate

0.8.5 may be marked complete only when all of the following exist:

- exact cognitive-mode catalog and allocation rule recovered and frozen;
- implementation diff against v0.7.22;
- machine-readable schema and migration policy;
- automated certification report with zero resume-identity violations;
- proof that Collector configuration and transport files are unchanged;
- owner dry-run evidence for fresh, resumed, and degraded-storage paths;
- explicit `PASS`, `HOLD`, or `FAIL` verdict.

Until then the official verdict is:

> **RECOVERED-SCOPE / HOLD-IMPLEMENTATION / NOT CERTIFIED FOR PARTICIPANT DEPLOYMENT**

## Immediate continuation order

1. Recover and inspect `CUBE_REV_0805_DECISION_PACKET_v01.md` from the 0.8.4 research package.
2. Freeze the exact cognitive-mode catalog, allocation weights, legacy migration rule, and research-field names.
3. Implement the assignment and resume-contract modules without changing Collector-side code.
4. Integrate all UI/payload version labels as 0.8.5.
5. Run the certification matrix and produce a signed decision packet.

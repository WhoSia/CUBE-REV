#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
VALIDATION=ROOT/'research/CUBE_REV_0.8.14_VALIDATION_REPORT.md'
DECISION=ROOT/'research/CUBE_REV_0.8.14_DECISION_PACKET.json'
RUNBOOK=ROOT/'research/CUBE_REV_0.8.14_RUNBOOK.md'

OLD_IDS={
 'b5712e1d30f2e0b0cc0b411fdca811d4c6158992':'25371c6479e074d3c7d0ad3501beffeb08f28cfb',
 '30753219920':'30754439979',
 '91510832942':'91514086682',
 '30753219950':'30754439978',
 '8835133893':'8835501173',
 '96e188a9e25c36481a8c442787b3ed2b7f2803f4308d1ceea09929df1f8a4932':'c81b46125916aadb9be55085a68bedf70a3bfbfbb5991e85d54096061660e093',
 '195385':'202501',
}

# Validation report
v=VALIDATION.read_text(encoding='utf-8')
for old,new in OLD_IDS.items():
    if old not in v: raise SystemExit(f'VALIDATION_ID_PRECONDITION_MISSING:{old}')
    v=v.replace(old,new)
old_decision='> **PASS-ARCHIVAL-LIVE-SUBMITTED-BYTE-RECONSTRUCTION / PASS-0.8.13-EVIDENCE-LINEAGE-ERRATUM / PASS-PROVENANCE-PRESERVING-ARCHIVAL-FACTORY-BRIDGE / PASS-CHROMIUM-ONLY-CONTROLLED-STAGING-POLICY / PASS-FIREFOX-WEBKIT-FAIL-CLOSED / PASS-DETERMINISTIC-STAGING-CANDIDATE / PASS-INHERITED-CONTRACTS / HOLD-EXACT-STORED-RAW-CUSTODY-REPLAY / HOLD-PHYSICAL-DEVICE-WALKTHROUGH / HOLD-OWNER-ACCEPTANCE / DEFAULT-CUTOVER-NO_GO**'
new_decision='> **PASS-ARCHIVAL-LIVE-SUBMITTED-BYTE-RECONSTRUCTION / PASS-0.8.13-EVIDENCE-LINEAGE-ERRATUM / PASS-PROVENANCE-PRESERVING-ARCHIVAL-FACTORY-BRIDGE / PASS-CHROMIUM-ONLY-CONTROLLED-STAGING-POLICY / PASS-FIREFOX-WEBKIT-FAIL-CLOSED / PASS-DYNAMIC-PERSISTED-LEASE-EXPIRY-TAKEOVER / PASS-DETERMINISTIC-STAGING-CANDIDATE / PASS-INHERITED-CONTRACTS / HOLD-EXACT-STORED-RAW-CUSTODY-REPLAY / HOLD-PHYSICAL-DEVICE-WALKTHROUGH / HOLD-OWNER-ACCEPTANCE / DEFAULT-CUTOVER-NO_GO**'
if v.count(old_decision)!=1: raise SystemExit(f'VALIDATION_DECISION_COUNT:{v.count(old_decision)}')
v=v.replace(old_decision,new_decision)
execute_anchor='- a machine-evaluated production cutover gate.\n'
execute_new='- a machine-evaluated production cutover gate;\n- a persisted-lease-expiry takeover harness that reads the stored expiry timestamp instead of relying on a fixed delay.\n'
if v.count(execute_anchor)!=1: raise SystemExit('VALIDATION_EXECUTE_ANCHOR')
v=v.replace(execute_anchor,execute_new)
iterate_anchor='- archival submitted envelope converted through a separately hashed provenance bridge: established.\n\n## Track A — Stored-raw custody and evidence lineage'
iterate_new='- archival submitted envelope converted through a separately hashed provenance bridge: established.\n\nThe lease test was also tightened after a cleanup-head execution exposed a timing assumption. The inherited 0.8.13 test waited a fixed 1,400ms before asking an already-open second tab to retry. One execution observed only the first POST, while an identical rerun passed. The pass on rerun was not accepted as sufficient evidence. The 0.8.14 gate now reads the persisted `lease_expires_at`, waits until that exact timestamp plus a 250ms margin, opens a fresh second page, and repeats the takeover four times.\n\n## Track A — Stored-raw custody and evidence lineage'
if v.count(iterate_anchor)!=1: raise SystemExit('VALIDATION_ITERATE_ANCHOR')
v=v.replace(iterate_anchor,iterate_new)
track_anchor='## Track D — Controlled staging candidate'
lease_section='''## Track D — Persisted-expiry lease takeover certification

The original 0.8.13 delayed-receipt test used a fixed `1400ms` wait and a second page that had already been open while the first delivery was pending. On the 0.8.14 cleanup head, one execution saw only the first POST within the assertion window; the identical workflow rerun passed. This was treated as a harness-control ambiguity, not as evidence that the first failure could be ignored.

The final 0.8.14 lease gate therefore uses the persisted state as its clock authority:

1. page A completes 28 responses and seals one immutable snapshot;
2. page A obtains generation 1 and sends the first delivery;
3. the test reads `submission_control.lease_expires_at` from stored state;
4. it waits until that timestamp plus 250ms;
5. only then does it open a fresh page B and request submission;
6. page B obtains generation 2 and sends the same snapshot with another nonce;
7. page B confirms the duplicate receipt and reaches `SUBMITTED`;
8. the delayed generation-1 owner is fenced by `STALE_SUBMISSION_LEASE` when it later attempts confirmation.

Four fresh browser contexts were executed:

| Iteration | Margin after persisted expiry | POSTs | Pair payload identity | Final generation | Final state |
|---:|---:|---:|---|---:|---|
| 1 | 252ms | 2 | identical | 2 | `SUBMITTED` |
| 2 | 252ms | 2 | identical | 2 | `SUBMITTED` |
| 3 | 252ms | 2 | identical | 2 | `SUBMITTED` |
| 4 | 253ms | 2 | identical | 2 | `SUBMITTED` |

Aggregate evidence:

```text
iterations                         4/4 PASS
total POSTs                        8
fixed sleep used                   false
payload pairs identical            true
all final lease generations        2
terminal receipts per iteration    duplicate + stored
responses per snapshot             28
```

The four iterations had different session-specific payload hashes, as expected, but each iteration's two deliveries were byte-, SHA-256-, checksum-, and session-identical while using distinct nonces.

Final marker:

```text
CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false
```

This dynamic persisted-expiry result is the 0.8.14 promotion Gate. The earlier fixed-delay `CR0813_LEASE_EXPIRY_AMBIGUITY_PASS` remains historical 0.8.13 evidence but is not used as the final 0.8.14 cutover authority.

## Track E — Controlled staging candidate'''
if v.count(track_anchor)!=1: raise SystemExit('VALIDATION_TRACK_D_ANCHOR')
v=v.replace(track_anchor,lease_section)
v=v.replace('## Track E — Inherited contracts','## Track F — Inherited contracts')
old_inherited='''The final workflow re-executed the parent native Chromium suite and all inherited contracts:

```text
CR0813_NATIVE_MULTI_WINDOW_PASS
CR0813_LEASE_EXPIRY_AMBIGUITY_PASS
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

The baseline/calibration workflow also completed successfully on the same head.'''
new_inherited='''The final workflow re-executed the parent Chromium serialization scenario, the new dynamic persisted-expiry takeover suite, and all inherited state/migration contracts:

```text
CR0813_NATIVE_MULTI_WINDOW_PASS
CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

The baseline/calibration workflow also completed successfully on the same executable head. The fixed-delay second scenario from the parent 0.8.13 file is no longer a 0.8.14 Gate; it was replaced by the persisted-expiry suite above.'''
if v.count(old_inherited)!=1: raise SystemExit('VALIDATION_INHERITED_ANCHOR')
v=v.replace(old_inherited,new_inherited)
gate_anchor='- four fail-closed profile checks;\n- deterministic staging bundle;'
gate_new='- four fail-closed profile checks;\n- four repeated persisted-expiry lease takeovers with eight byte-paired deliveries;\n- deterministic staging bundle;'
if v.count(gate_anchor)!=1: raise SystemExit('VALIDATION_GATE_ANCHOR')
v=v.replace(gate_anchor,gate_new)
VALIDATION.write_text(v,encoding='utf-8')

# Decision packet
obj=json.loads(DECISION.read_text(encoding='utf-8'))
obj['schema_version']='CR0814-DECISION-PACKET-2'
obj['decision'].insert(obj['decision'].index('PASS_DETERMINISTIC_STAGING_CANDIDATE'),'PASS_DYNAMIC_PERSISTED_LEASE_EXPIRY_TAKEOVER')
cert=obj['certification']
cert.update({'executable_head':'25371c6479e074d3c7d0ad3501beffeb08f28cfb','workflow_run':30754439979,'job':91514086682,'baseline_workflow_run':30754439978})
cert['evidence_artifact'].update({'artifact_id':8835501173,'zip_sha256':'c81b46125916aadb9be55085a68bedf70a3bfbfbb5991e85d54096061660e093','compressed_bytes':202501})
obj['lease_expiry_certification']={
 'schema_version':'CR0814-DYNAMIC-LEASE-EXPIRY-EVIDENCE-1',
 'timing_policy':'READ_PERSISTED_LEASE_EXPIRES_AT_THEN_OPEN_SECOND_PAGE_AFTER_250MS_MARGIN',
 'fixed_sleep_used':False,
 'iteration_count':4,
 'passed_iterations':4,
 'total_posts':8,
 'expiry_margins_ms':[252,252,252,253],
 'all_payload_pairs_identical':True,
 'all_final_generations_two':True,
 'all_final_states':'SUBMITTED',
 'response_count_per_snapshot':28,
 'terminal_receipts_per_iteration':['duplicate','stored'],
 'stale_generation_one_confirmation':'REJECTED_WITH_STALE_SUBMISSION_LEASE',
 'marker':'CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false',
 'result':'PASS_DYNAMIC_PERSISTED_LEASE_EXPIRY_REPEATED'
}
obj['inherited_contracts']['cr0813_lease_expiry_ambiguity']='HISTORICAL_PASS_NOT_USED_AS_0_8_14_FINAL_GATE'
obj['inherited_contracts']['cr0814_dynamic_persisted_lease_expiry']='4/4 PASS; 8 POSTS; FIXED_SLEEP_FALSE'
obj['cutover_gate']['dynamic_persisted_lease_expiry_repetition']=True
DECISION.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Runbook
r=RUNBOOK.read_text(encoding='utf-8')
for old,new in OLD_IDS.items():
    if old not in r: raise SystemExit(f'RUNBOOK_ID_PRECONDITION_MISSING:{old}')
    r=r.replace(old,new)
old_step='''### 11. Re-run inherited contracts

```bash
npx playwright test tests/native_multi_window_0.8.13.spec.js \\
  --workers=1 --reporter=line

node tests/active_session_cas_0.8.12.test.js
node -r ./js/atomic-migration-commit-authority-0.8.11.js \\
  tests/atomic_migration_arbitration_0.8.11.test.js
node tests/cross_version_resume_hash_pin_0.8.10.test.js
node tests/public_bank_minimization_0.8.9.test.js
node tests/immutable_snapshot_contract_0.8.8.test.js
```

Required markers:

```text
CR0813_NATIVE_MULTI_WINDOW_PASS
CR0813_LEASE_EXPIRY_AMBIGUITY_PASS
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```
'''
new_step='''### 11. Re-run parent serialization, dynamic lease expiry, and inherited contracts

The 0.8.14 lease Gate must not use the parent test's fixed 1,400ms delay. It reads the persisted lease expiry and opens a fresh second page only after the stored timestamp plus 250ms.

```bash
npx playwright test tests/native_multi_window_0.8.13.spec.js \\
  --grep 'native Chromium Web Locks serialize two pages without response loss' \\
  --workers=1 --reporter=line

npx playwright test tests/lease_expiry_dynamic_0.8.14.spec.js \\
  --workers=1 --reporter=line

node tests/active_session_cas_0.8.12.test.js
node -r ./js/atomic-migration-commit-authority-0.8.11.js \\
  tests/atomic_migration_arbitration_0.8.11.test.js
node tests/cross_version_resume_hash_pin_0.8.10.test.js
node tests/public_bank_minimization_0.8.9.test.js
node tests/immutable_snapshot_contract_0.8.8.test.js
```

Required markers:

```text
CR0813_NATIVE_MULTI_WINDOW_PASS
CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false
CR0812_ACTIVE_SESSION_CAS_PASS 28/28
CR0811_ATOMIC_MIGRATION_PASS 23/23
CR0810_MIGRATION_HASH_PIN_PASS 13/13
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

Required dynamic evidence file:

```text
artifacts/0.8.14/dynamic_lease_expiry_evidence.json
```

It must report four passed iterations, eight total POSTs, identical payload pairs, generation 2 in every final state, and `fixed_sleep_used=false`. A delayed generation-1 owner may log `STALE_SUBMISSION_LEASE` after generation 2 has confirmed; that is the expected fencing result.
'''
if r.count(old_step)!=1: raise SystemExit(f'RUNBOOK_STEP_COUNT:{r.count(old_step)}')
r=r.replace(old_step,new_step)
stop_anchor='- inherited contracts regress;\n- staging bundle is nondeterministic;'
stop_new='- inherited contracts regress;\n- the dynamic persisted-expiry suite does not pass all four iterations or uses a fixed delay;\n- staging bundle is nondeterministic;'
if r.count(stop_anchor)!=1: raise SystemExit('RUNBOOK_STOP_ANCHOR')
r=r.replace(stop_anchor,stop_new)
RUNBOOK.write_text(r,encoding='utf-8')

# Postconditions
for p in [VALIDATION,DECISION,RUNBOOK]:
    text=p.read_text(encoding='utf-8')
    if 'CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=4/4 posts=8 fixed_sleep=false' not in text:
        raise SystemExit(f'DYNAMIC_MARKER_MISSING:{p}')
for old in OLD_IDS:
    if old in VALIDATION.read_text(encoding='utf-8') or old in RUNBOOK.read_text(encoding='utf-8'):
        raise SystemExit(f'OLD_ID_REMAINS:{old}')
print('CR0814_DYNAMIC_LEASE_FINAL_DOC_PATCH_PASS files=3')

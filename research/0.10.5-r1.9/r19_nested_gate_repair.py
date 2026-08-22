#!/usr/bin/env python3
from pathlib import Path
import json, hashlib

BASE=Path('research/0.10.5-r1.9/evidence-nested-no-leak')
AUDIT=BASE/'NESTED_NO_LEAK_AUDIT.json'
ROWS=BASE/'NESTED_NO_LEAK_ATTEMPT_ROWS.json'
NAPKIN=Path('research/0.10.5-r1.9/NAPKIN_INTENT_AND_PREREGISTRATION.json')
OLD=Path('research/0.10.5-r1.9/evidence-familywise-development/ATTEMPT_FAMILYWISE_NULL_PREREG_SEAL.json')
OUT=Path('/tmp/r19nestedr3'); OUT.mkdir(parents=True,exist_ok=True)

def sha_bytes(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def stable(x):
    if isinstance(x,dict): return '{'+','.join(json.dumps(k)+':'+stable(x[k]) for k in sorted(x))+'}'
    if isinstance(x,list): return '['+','.join(stable(v) for v in x)+']'
    return json.dumps(x,separators=(',',':'),ensure_ascii=False)
def sem_sha(x): return hashlib.sha256(stable(x).encode()).hexdigest()

a=json.loads(AUDIT.read_text()); rows=json.loads(ROWS.read_text())['rows']; n=json.loads(NAPKIN.read_text()); old=json.loads(OLD.read_text())
assert a['status']=='HOLD_NESTED_CALIBRATION'
assert a['checks']['primary_health_band'] and a['checks']['watch_health_band']
assert a['checks']['outer_test_fold_excluded_from_local_and_family_reference']
assert a['checks']['future_fresh_outcomes_seen_false']
assert old['future_fresh_outcomes_seen'] is False
assert n['attempt_level_familywise_null']['minimum_supported_conditioning_n']==300
assert n['attempt_level_familywise_null']['minimum_global_attempt_reference_n']==1000

ok=[r for r in rows if r.get('familywise_ok')]
levels={}
violations=[]
for r in ok:
    level=r['familywise_level']; nn=int(r['familywise_n'])
    levels.setdefault(level,[]).append(nn)
    minimum=1000 if level=='GLOBAL' else 300
    if nn<minimum: violations.append({'key':f"{r['result_id']}:{r['attempt_number']}",'level':level,'n':nn,'required':minimum})
level_summary={k:{'attempts':len(v),'min_n':min(v),'max_n':max(v),'required_min':1000 if k=='GLOBAL' else 300} for k,v in sorted(levels.items())}
checks={
  'nested_familywise_attempts_ge_1200':len(ok)>=n['attempt_level_familywise_null']['minimum_crossfit_state_certified_attempts'],
  'primary_health_band':0.003<=a['primary_empirical_exceedance']<=0.02,
  'watch_health_band':0.025<=a['watch_empirical_exceedance']<=0.08,
  'all_non_global_conditioning_refs_ge_300':all(v['min_n']>=300 for k,v in level_summary.items() if k!='GLOBAL'),
  'all_global_refs_ge_1000':all(v['min_n']>=1000 for k,v in level_summary.items() if k=='GLOBAL'),
  'no_reference_size_violations':len(violations)==0,
  'outer_test_fold_excluded_from_all_reference_construction':a['checks']['outer_test_fold_excluded_from_local_and_family_reference'],
  'fresh_outcomes_unread':old['future_fresh_outcomes_seen'] is False,
}
status='PASS_NESTED_NO_LEAK_READINESS_EXACT_PREREG_GATE' if all(checks.values()) else 'HOLD_NESTED_EXACT_PREREG_GATE'
repair={
 'schema_version':'CR0105R19-NESTED-EXACT-PREREG-GATE-REPAIR-1','status':status,
 'role':'OPERATIONAL_GATE_REPAIR_USING_PREOUTCOME_PREREGISTERED_SUPPORT_THRESHOLDS',
 'r2_hold_reason':'R2 implementation incorrectly required familywise_n>=1000 at every conditioning level, while the frozen NAPKIN requires n>=300 for non-global conditioning and n>=1000 only for global.',
 'scientific_definition_changed':False,'fresh_vintage_read_before_repair':False,
 'nested_attempts':len(ok),'primary_empirical_exceedance':a['primary_empirical_exceedance'],'watch_empirical_exceedance':a['watch_empirical_exceedance'],
 'level_support':level_summary,'violations':violations,'checks':checks,'human_observations':0
}
seal={
 'schema_version':'CR0105R19-ATTEMPT-FAMILYWISE-NULL-PREREG-SEAL-R3-1',
 'status':'SEALED_FOR_FUTURE_FRESH_VINTAGE_R3_NESTED_EXACT_PREREG_GATE' if status.startswith('PASS') else 'HOLD_NOT_SEALABLE',
 'supersedes_initial_seal_sha256':old['seal_sha256'],
 'r2_nested_audit_sha256':sha_bytes(AUDIT),
 'r2_nested_rows_sha256':sha_bytes(ROWS),
 'napkin_file_sha256':sha_bytes(NAPKIN),
 'repair_semantic_sha256':sem_sha(repair),
 'nested_dependency_rule':a['dependency_rule'],
 'familywise_support_gate':{'non_global_min_n':300,'global_min_n':1000},
 'primary_alpha':n['attempt_level_familywise_null']['primary_familywise_alpha'],
 'watch_alpha':n['attempt_level_familywise_null']['secondary_watch_alpha'],
 'nested_calibration':{'attempts':len(ok),'primary_empirical_exceedance':a['primary_empirical_exceedance'],'watch_empirical_exceedance':a['watch_empirical_exceedance'],'level_support':level_summary},
 'future_scoring_rule':n['attempt_level_familywise_null']['future_familywise_p'],
 'future_fresh_outcomes_seen':False,'human_observations':0
}
seal['seal_sha256']=sem_sha(seal)
(OUT/'NESTED_EXACT_PREREG_GATE_REPAIR.json').write_text(json.dumps(repair,indent=2)+'\n')
(OUT/'ATTEMPT_FAMILYWISE_NULL_PREREG_SEAL_R3.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps({'status':status,'seal_sha256':seal['seal_sha256'],'nested_attempts':len(ok),'primary':a['primary_empirical_exceedance'],'watch':a['watch_empirical_exceedance'],'level_support':level_summary,'checks':checks},indent=2))
if not status.startswith('PASS'): raise SystemExit(20)

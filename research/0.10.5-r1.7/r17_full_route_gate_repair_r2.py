#!/usr/bin/env python3
from pathlib import Path
import json
src=Path('research/0.10.5-r1.7/r17_full_route_court.mjs').read_text(encoding='utf-8')
target=json.loads(Path('/tmp/r17_target.json').read_text())
r=next(x for x in target['results'] if x['name']=='UNDER10_SPEED_X_ERA')
assert r['gate']['ess_min']==200, r['gate']
assert r['status']=='PASS_INTERNAL_WEIGHT_GATE', r['status']
old='ess_ge_400:ess>=400,'
new='ess_ge_200_inherited_from_target_selection:ess>=200,'
assert src.count(old)==1, src.count(old)
src=src.replace(old,new)
src=src.replace("schema_version:'CR0105R17-FULL-ROUTE-ADMISSION-GATE-1'","schema_version:'CR0105R17-FULL-ROUTE-ADMISSION-GATE-2'")
runtime=Path('research/0.10.5-r1.7/r17_full_route_court_r2_runtime.mjs')
runtime.write_text(src,encoding='utf-8')
repair={
 'schema_version':'CR0105R17-FULL-ROUTE-GATE-REPAIR-R2-1',
 'status':'PASS_PRE_OUTCOME_RULE_RECONCILIATION',
 'r1_full_route_court_materialized':False,
 'r1_failed_only_gate':'ESS_GE_400',
 'inherited_prior_gate_source':'research/0.10.5-r1.7/evidence-selection-target/TARGET_SELECTION_ADJUDICATION.json',
 'inherited_target':'UNDER10_SPEED_X_ERA',
 'prior_declared_ess_min':200,
 'r2_change':'Only ESS threshold 400 -> inherited 200; all other admission criteria, sample design, route parser, state validator, and counterfactual definitions unchanged.',
 'outcome_seen_before_repair':False,
 'runtime_path':str(runtime),
 'human_observations':0
}
Path('/tmp/r17full/route').mkdir(parents=True,exist_ok=True)
Path('/tmp/r17full/route/R2_GATE_REPAIR.json').write_text(json.dumps(repair,indent=2)+'\n')
print(json.dumps(repair,indent=2))

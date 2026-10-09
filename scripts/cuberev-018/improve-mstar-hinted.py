#!/usr/bin/env python3
"""CUBE-REV 0.18: integer set-cover search with an independently proved
34-word Rubik witness as a full CP-SAT hint.  An incumbent smaller than34
is an UPPER bound ONLY after separate physical HTM word replay.  A solver
bound/status without an independently verified UNSAT certificate is NOT
a new mathematical lower bound.
"""
import json,sys,time,hashlib
from pathlib import Path
from ortools.sat.python import cp_model

if len(sys.argv)!=4:
    raise SystemExit("Usage: improve-mstar-hinted.py <physical_instance.json> <physical_34_hints.json> <output_dir>")
instance=Path(sys.argv[1])
d=json.loads(instance.read_text())
h=json.loads(Path(sys.argv[2]).read_text())
assert d['schema']=='cube-rev.018.cube-physical-mstar-maximal-v1'
assert d['counts']['bases']==1192 and d['counts']['maximal']==1323
columns=[int(x['mask'],16) for x in d['candidates']]
seed=list(map(int,h['candidates']))
assert len(seed)==h['newCount']==34
assert all(0<=j<1323 for j in seed) and len(set(seed))==34
union=0
for j in seed:union|=columns[j]
assert union.bit_count()==1192

model=cp_model.CpModel()
x=[model.NewBoolVar(f'w{j}') for j in range(1323)]
for base_index in range(1192):
    hits=[x[j] for j,col in enumerate(columns) if (col>>base_index)&1]
    assert hits
    model.Add(sum(hits)>=1)
sumx=sum(x)
model.Add(sumx<=34)
model.Add(sumx>=30)  # independently verified original k29 UNSAT, not a solver guess
model.Minimize(sumx)
seedset=set(seed)
for j in range(1323):model.AddHint(x[j],1 if j in seedset else 0)
solver=cp_model.CpSolver()
solver.parameters.max_time_in_seconds=175.0
solver.parameters.num_search_workers=2
solver.parameters.random_seed=20261009
solver.parameters.log_search_progress=False
output=Path(sys.argv[3]);output.mkdir(parents=True,exist_ok=True)
t=time.monotonic()
status=solver.Solve(model)
secs=time.monotonic()-t
status_name=solver.StatusName(status)
receipt={
 'status':status_name,
 'source_sha256':hashlib.sha256(instance.read_bytes()).hexdigest(),
 'n_variables':1323,'n_coverage_constraints':1192,
 'lower_side_external_drup_k29':30,
 'upper_seed_exact_replayed':34,
 'seed_count':len(seed),
 'wall_seconds':round(secs,3),
 'ortools_version':__import__('ortools').__version__,
 'best_bound_numeric_solver_only':float(solver.BestObjectiveBound()) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None,
 'theorem_lower_bound_promotion':False
}
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    chosen=[j for j in range(1323) if solver.Value(x[j])]
    assert len(chosen)<=34
    cover=0
    for j in chosen:cover|=columns[j]
    assert cover.bit_count()==1192
    receipt['incumbent_words']=len(chosen)
    (output/'sat_witness.json').write_text(json.dumps({
        'schema':'cube-rev.018.cpsat-cube-upper-witness-v1',
        'k':len(chosen),'indices':chosen,
        'words':[d['candidates'][j]['word'] for j in chosen],
        'requires_independent_HTM_replay':True
    },indent=2)+'\n')
    print('MSTAR_018_HINTED_CP_SAT_UPPER_WITNESS_PENDING_PHYSICAL_REPLAY',
          len(chosen),'status',status_name,flush=True)
else:
    print('MSTAR_018_HINTED_CP_SAT_NO_NEW_UPPER',status_name,flush=True)
(output/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('MSTAR_018_HINTED_CP_SAT_RECEIPT',json.dumps(receipt,sort_keys=True),flush=True)

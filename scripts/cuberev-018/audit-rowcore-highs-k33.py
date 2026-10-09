#!/usr/bin/env python3
"""Independent numerical HiGHS check of Cube M-star k=33 on equivalent row core.

This supplies a SECOND integer-optimization result, not a portable logical
UNSAT proof. It never promotes the exact mathematical theorem status.
All original physical 1323 maximal actions remain decision variables.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import csr_matrix, vstack

p=argparse.ArgumentParser()
p.add_argument('--physical',required=True)
p.add_argument('--core',required=True)
p.add_argument('--output',required=True)
p.add_argument('--seconds',type=float,default=35)
a=p.parse_args()
physical=Path(a.physical)
raw=physical.read_bytes()
d=json.loads(raw)
core=json.loads(Path(a.core).read_text())
assert d['counts']=={
    'literal':104976,'partitions':1913,
    'coverageTypes':1477,'maximal':1323,'bases':1192
}
assert core['physical_input_sha256']==hashlib.sha256(raw).hexdigest()
retained=list(map(int,core['retained_row_indices']))
assert len(retained)==398 and len(set(retained))==398
masks=[int(c['mask'],16) for c in d['candidates']]
rows=[]; cols=[]
for j,mask in enumerate(masks):
    for i,original in enumerate(retained):
        if mask>>original&1:
            rows.append(i)
            cols.append(j)
A=csr_matrix((np.ones(len(rows),dtype=np.float64),(rows,cols)),
             shape=(398,1323))
assert A.getnnz(axis=0).min()>=0
assert A.getnnz(axis=1).min()>0
t=time.monotonic()
ans=milp(c=np.ones(1323),integrality=np.ones(1323,dtype=int),
         bounds=Bounds(0,1),
         constraints=[
             LinearConstraint(A,np.ones(398),np.inf),
             LinearConstraint(np.ones((1,1323)),[-np.inf],[33])
         ],
         options={'time_limit':a.seconds,'mip_rel_gap':0,'disp':False})
duration=time.monotonic()-t
r={
 'model':'exact 1192 original physical cube source constraints, reduced to 398 equivalent clauses',
 'num_maximal_physical_columns':1323,
 'physical_sha256':hashlib.sha256(raw).hexdigest(),
 'target_dictionary_size_at_most':33,
 'solver':'scipy.optimize.milp / HiGHS',
 'scipy_version':__import__('scipy').__version__,
 'status_code':int(ans.status),
 'message':str(ans.message),
 'run_seconds':round(duration,3),
 'important_scope':'Numerical integer solver status, NOT a portable independently checked DRUP certificate',
 'scientific_exact_theorem_approved':False
}
if ans.status==2:
 print('CUBE_REV_018_NUMERICAL_HIGHS_K33_INFEASIBLE_NOT_DRUP_PROOF',
       json.dumps(r,sort_keys=True),flush=True)
elif ans.status==0:
 selected=np.flatnonzero(ans.x>.5).tolist()
 cover=0
 for j in selected:cover|=masks[j]
 assert cover.bit_count()==1192
 r['feasible_dictionary_size']=len(selected)
 r['candidate_words']=[d['candidates'][j]['word'] for j in selected]
 print('CUBE_REV_018_NUMERICAL_K33_POSSIBLE_REPLAY_REQUIRED',len(selected),
       flush=True)
else:
 print('CUBE_REV_018_NUMERICAL_HIGHS_K33_UNKNOWN',ans.status,flush=True)
out=Path(a.output)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(r,indent=2)+'\n')

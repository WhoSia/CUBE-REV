#!/usr/bin/env python3
"""CUBE-REV 0.18 — deterministic Boolean SMT-LIB cross-solver regression.

Reconstruct both exact all-k Cube reductions from the frozen actual
sticker-derived 1192x1323 physical incidence. Emit plain Boolean
coverage clauses and an SMT-LIB at-most-k predicate for one of the
two independent Cube components.

This is a solver input, NOT an UNSAT proof. Any Z3, CVC5, etc. outcome
is evidence but not independently checked DRUP/LRAT.
"""
import argparse
import hashlib
import json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--physical',required=True)
p.add_argument('--slot',type=int,choices=[4,5],required=True)
p.add_argument('--k',type=int,required=True)
p.add_argument('--output',required=True)
a=p.parse_args()
raw=Path(a.physical).read_bytes()
data=json.loads(raw)
assert data['schema']=='cube-rev.018.cube-physical-mstar-maximal-v1'
assert data['counts']=={
 'literal':104976,'partitions':1913,
 'coverageTypes':1477,'maximal':1323,'bases':1192}
masks=[int(c['mask'],16) for c in data['candidates']]
assert len(masks)==1323
supports=[0]*1192
for col,mask in enumerate(masks):
    while mask:
        low=mask&-mask
        supports[low.bit_length()-1]|=1<<col
        mask ^=low
rows=[]
for i in sorted(range(1192),key=lambda j:(supports[j].bit_count(),j)):
    if not any((supports[x]&~supports[i])==0 for x in rows):
        rows.append(i)
assert len(rows)==398
for i in range(1192):
    assert any((supports[j]&~supports[i])==0 for j in rows)
projected=[sum(1<<i for i,r in enumerate(rows) if z>>r&1)
           for z in masks]
u={}
for j,z in enumerate(projected):
    u.setdefault(z,j)
assert len(u)==361
keep=[]
for mask,j in sorted(u.items(),key=lambda t:(-t[0].bit_count(),t[1])):
    if not any((mask&~x)==0 for x,_ in keep):
        keep.append((mask,j))
assert len(keep)==168
for mask in projected:
    assert any((mask&~v)==0 for v,_ in keep)
target=[i for i,r in enumerate(rows)
        if data['bases'][r].bit_count()==a.slot]
partbits=sum(1<<i for i in target)
candidates=[(mask,j) for mask,j in keep if mask&partbits]
expected=(64,88,6) if a.slot==4 else (334,80,26)
assert (len(target),len(candidates),a.k)==expected
assert all((mask&partbits)==mask for mask,j in candidates)
lines=[
 '; CUBE-REV 0.18 — REAL 3x3 Rubik 18-HTM physical source set-cover',
 '; '+json.dumps({'source_sha256':hashlib.sha256(raw).hexdigest(),
      'component_source_slots':a.slot,'rows':len(target),
      'actual_four_HTM_words':len(candidates),'k':a.k},sort_keys=True),
 '; Status UNSAT is not a portable independently checked proof.',
 '(set-logic QF_FD)',
]
lines.extend(f'(declare-const x{i} Bool)' for i in range(len(candidates)))
for row in target:
    incident=[f'x{j}' for j,(mask,original) in enumerate(candidates)
              if mask>>row&1]
    assert incident
    lines.append('(assert (or '+' '.join(incident)+'))')
lines.append('(assert ((_ at-most '+str(a.k)+') '+
             ' '.join(f'x{j}' for j in range(len(candidates)))+'))')
lines.extend(['(check-sat)','(exit)'])
dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text('\n'.join(lines)+'\n')
print('CUBE_REV_018_COMPONENT_BOOLEAN_SMT2_SOURCE_PASS',
      json.dumps({'slot':a.slot,'rows':len(target),
       'columns':len(candidates),'k':a.k,
       'smt2_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},
       sort_keys=True),flush=True)

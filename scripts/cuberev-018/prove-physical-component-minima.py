#!/usr/bin/env python3
"""Exact real Rubik M* component UNSAT courts.

Prove: the 334-source/80-word five-slot component has no 26-word
dictionary, and the 64-source/88-word four-slot component has no 6-word
dictionary. With independently certified full physical 34-word witness,
their disjointness and the two proof traces imply M* == 34.

Every graph edge is checked from the actual 18-HTM physical incidence.
The solver never relies on historical P6 168-class assumptions.
"""
import argparse
import hashlib
import json
from pathlib import Path

from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose4

p=argparse.ArgumentParser()
p.add_argument('--physical',required=True)
p.add_argument('--rows',required=True)
p.add_argument('--columns',required=True)
p.add_argument('--components',required=True)
p.add_argument('--output',required=True)
p.add_argument('--conflicts',type=int,default=2500000)
a=p.parse_args()
src=Path(a.physical)
raw=src.read_bytes()
d=json.loads(raw)
rfile=Path(a.rows).read_bytes()
cfile=Path(a.columns).read_bytes()
qfile=Path(a.components).read_bytes()
r=json.loads(rfile)
c=json.loads(cfile)
q=json.loads(qfile)
assert d['counts']=={
  'literal':104976,'partitions':1913,
  'coverageTypes':1477,'maximal':1323,'bases':1192
}
assert r['physical_input_sha256']==hashlib.sha256(raw).hexdigest()
assert c['physical_sha256']==hashlib.sha256(raw).hexdigest()
assert c['row_core_sha256']==hashlib.sha256(rfile).hexdigest()
assert q['physical_sha256']==hashlib.sha256(raw).hexdigest()
assert q['row_certificate_sha256']==hashlib.sha256(rfile).hexdigest()
assert q['column_certificate_sha256']==hashlib.sha256(cfile).hexdigest()
assert len(r['retained_row_indices'])==398
assert len(c['representative_original_candidate_ids'])==168
original=[int(x['mask'],16) for x in d['candidates']]
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
results=[]
# Prove the tiny four-slot component first, preserving its DRUP receipt even
# if the harder five-slot k26 search later hits its conflict budget.
for component in sorted(q['components'], key=lambda c:c['source_rows']):
    slot=component['slot_count']
    k=26 if slot==5 else 6
    rows=component['original_source_row_indices']
    reps=component['original_maximal_HTM_column_indices']
    assert (slot,len(rows),len(reps),k) in (
        (5,334,80,26),(4,64,88,6))
    assert len(set(rows))==len(rows)
    assert len(set(reps))==len(reps)
    assert all(d['bases'][i].bit_count()==slot for i in rows)
    cnf=CNF()
    for row in rows:
        literals=[j+1 for j,rep in enumerate(reps)
                  if original[rep]>>row&1]
        assert literals, ('Cube source unsupported in block',slot,row)
        cnf.append(literals)
    vpool=IDPool(start_from=len(reps)+1)
    cnf.extend(CardEnc.atmost(
        lits=list(range(1,len(reps)+1)),bound=k,
        encoding=EncType.seqcounter,vpool=vpool).clauses)
    stem=f'cube_{slot}slot_k{k}'
    path=out/f'{stem}.cnf'
    cnf.to_file(str(path))
    record={
       'slot_group':slot,'k':k,'cube_physical_source_rows':len(rows),
       'original_4HTM_word_candidates':len(reps),
       'state':'SOLVER_PENDING',
       'input_physical_sha256':hashlib.sha256(raw).hexdigest(),
       'component_certificate_sha256':hashlib.sha256(qfile).hexdigest(),
       'cnf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
       'cnf_variables':cnf.nv,'cnf_clauses':len(cnf.clauses),
       'conflict_budget':a.conflicts,
       'accepted_math_claim':False
    }
    print('CUBE_REV_018_INDEPENDENT_COMPONENT_CNF',
          json.dumps(record,sort_keys=True),flush=True)
    with Glucose4(bootstrap_with=cnf.clauses,with_proof=True) as solver:
        solver.conf_budget(a.conflicts)
        ans=solver.solve_limited(expect_interrupt=False)
        if ans is False:
            proof=solver.get_proof()
            assert proof and proof[-1].strip()=='0'
            proof_path=out/f'{stem}.drup'
            proof_path.write_text('\n'.join(proof)+'\n')
            record['state']='UNSAT_EXTERNAL_DRUP_CHECK_PENDING'
            record['proof_sha256']=hashlib.sha256(proof_path.read_bytes()).hexdigest()
            record['proof_lines']=len(proof)
            print('CUBE_REV_018_COMPONENT_UNSAT_TRACE_EMITTED',slot,k,len(proof),
                  flush=True)
        elif ans is True:
            values=set(solver.get_model())
            indices=[reps[i] for i in range(len(reps)) if i+1 in values]
            assert len(indices)<=k
            covered=0
            for i in indices:covered |=original[i]
            assert all(covered>>row&1 for row in rows)
            record['state']='COMPONENT_SAT_WITNESS_REQUIRES_FRESH_PHYSICAL_REPLAY'
            record['witness_original_indices']=indices
            print('CUBE_REV_018_COMPONENT_SAT_CONTRADICTS_NUMERICAL_OBSTRUCTION',
                  slot,k,flush=True)
        else:
            record['state']='UNKNOWN_CONFLICT_BUDGET'
            print('CUBE_REV_018_COMPONENT_UNKNOWN',slot,k,flush=True)
    (out/f'{stem}.receipt.json').write_text(json.dumps(record,indent=2)+'\n')
    results.append(record)
(out/'all_components.receipt.json').write_text(json.dumps(
    {'status':'INCOMPLETE_UNTIL_BOTH_EXTERNAL_DRUP_PROOFS_VERIFIED',
     'components':results},indent=2)+'\n')

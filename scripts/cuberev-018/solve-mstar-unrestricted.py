#!/usr/bin/env python3
"""CUBE-REV 0.18: independent unrestricted original k-word SAT court.
NO P6 dual cuts, NO forced-heavy condition, NO excluded zero-weight words.
Exactly the physical 1192 cover clauses over ALL 1323 maximal candidates
and an unweighted <=k cardinality constraint. Any UNSAT must be DRUP
checked externally before changing the scientific lower bound.
The 60-positive dual-only model is a separately expected SAT control.
"""
import argparse,hashlib,json
from pathlib import Path
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose4

p=argparse.ArgumentParser()
p.add_argument('--instance',required=True)
p.add_argument('--out',required=True)
p.add_argument('--k',type=int,default=25)
p.add_argument('--target',choices=['full','dual'],default='full')
p.add_argument('--conflicts',type=int,default=600000)
args=p.parse_args()
assert 24<=args.k<=34 and args.conflicts>=1
data=json.loads(Path(args.instance).read_text())
assert data['schema']=='cube-rev.018.cube-physical-mstar-maximal-v1'
assert data['counts']['maximal']==1323 and data['counts']['bases']==1192
bases=list(map(int,data['bases']))
bitsets=[int(x['mask'],16) for x in data['candidates']]
assert len(bitsets)==1323 and len(bases)==1192
selected_bases=list(range(1192)) if args.target=='full' else sorted(
    bases.index(int(b)) for b,w in data['dual'] if int(w)>0)
assert len(selected_bases)==(1192 if args.target=='full' else 60)
cnf=CNF()
for i in selected_bases:
    clause=[j+1 for j,m in enumerate(bitsets) if m>>i&1]
    assert clause,('basis_uncovered',i)
    cnf.append(clause)
vpool=IDPool(start_from=1324)
cnf.extend(CardEnc.atmost(lits=list(range(1,1324)),bound=args.k,
                          encoding=EncType.seqcounter,vpool=vpool).clauses)
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
cnf_file=out/'original_cover.cnf'
cnf.to_file(str(cnf_file))
receipt={'mode':'UNRESTRICTED_FULL_1192' if args.target=='full' else 'DUAL_ONLY_60_CONTROL',
         'k':args.k,'solver':'PySAT Glucose4 DRUP',
         'physical_instance_sha256':hashlib.sha256(Path(args.instance).read_bytes()).hexdigest(),
         'cnf_sha256':hashlib.sha256(cnf_file.read_bytes()).hexdigest(),
         'cnf_variables':cnf.nv,'cnf_clauses':len(cnf.clauses),
         'original_variables':1323,'original_base_clauses':len(selected_bases),
         'conflict_budget':args.conflicts,'state':'NOT_SOLVED',
         'independent_certificate':False}
print('MSTAR_PLAIN_CNF',json.dumps(receipt,sort_keys=True),flush=True)
with Glucose4(bootstrap_with=cnf.clauses,with_proof=True) as sol:
    sol.conf_budget(args.conflicts)
    result=sol.solve_limited(expect_interrupt=False)
    if result is False:
        proof=sol.get_proof()
        assert proof and proof[-1].strip()=='0'
        proof_path=out/'original_cover.drup'
        proof_path.write_text('\n'.join(proof)+'\n')
        receipt['state']='UNSAT_PROOF_PENDING_EXTERNAL_CHECK'
        receipt['proof_sha256']=hashlib.sha256(proof_path.read_bytes()).hexdigest()
        receipt['proof_lines']=len(proof)
        print('MSTAR_PLAIN_UNSAT_NEEDS_INDEPENDENT_CHECK',args.target,args.k,len(proof),flush=True)
    elif result is True:
        model=set(sol.get_model())
        chosen=[j for j in range(1323) if j+1 in model]
        assert len(chosen)<=args.k
        union=0
        for j in chosen:union|=bitsets[j]
        assert all((union>>i)&1 for i in selected_bases)
        wordlist=[data['candidates'][j]['word'] for j in chosen]
        (out/'sat_witness.json').write_text(json.dumps(
            {'target':args.target,'k':args.k,'words':wordlist,'indices':chosen,
             'replay_required_for_full_court':args.target=='full'},indent=2)+'\n')
        receipt['state']='SAT_WITNESS_FOUND_PENDING_ACTION_REPLAY'
        receipt['nwords']=len(chosen)
        print('MSTAR_PLAIN_SAT_WITNESS',args.target,args.k,len(chosen),flush=True)
    else:
        receipt['state']='UNKNOWN_CONFLICT_BUDGET'
        print('MSTAR_PLAIN_UNKNOWN',args.target,args.k,args.conflicts,flush=True)
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')

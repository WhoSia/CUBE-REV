#!/usr/bin/env python3
"""0.18 Cube-only structural obstruction at k=33 for all c(w)=20 masks.

This is the frozen physical 18-HTM 1,192-source problem, projected
ONLY to the 162 inclusion-maximal four-action word masks with
original rational dual numerator mass c=20. It is a restricted
subproblem. Its UNSAT entails that any full k33 dictionary must
include at least one c(w)<20 word; NOT that k33 is impossible.
"""
import argparse
import hashlib
import json
from pathlib import Path

from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose4

p = argparse.ArgumentParser()
p.add_argument('--instance',required=True)
p.add_argument('--out',required=True)
p.add_argument('--conflicts',type=int,default=1200000)
args = p.parse_args()
raw=Path(args.instance).read_bytes()
data=json.loads(raw)
assert data['counts']=={
 'literal':104976,'partitions':1913,
 'coverageTypes':1477,'maximal':1323,'bases':1192
}
orig=[i for i,w in enumerate(data['candidates']) if int(w['mass'])==20]
assert len(orig)==162
masks=[int(data['candidates'][i]['mask'],16) for i in orig]
assert len(set(masks))==162
union=0
for mask in masks:union|=mask
assert union.bit_count()==1192, "physical full-source coverage missing from mass20 subfamily"
cnf=CNF()
for b in range(1192):
 clause=[j+1 for j,mask in enumerate(masks) if mask>>b&1]
 assert clause, f'ORIGINAL_SOURCE_{b}_UNREACHABLE'
 cnf.append(clause)
pool=IDPool(start_from=163)
cnf.extend(CardEnc.atmost(
 lits=list(range(1,163)),bound=33,
 encoding=EncType.seqcounter,vpool=pool).clauses)
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
cnf_path=out/'mass20_k33_original_1192.cnf'
cnf.to_file(str(cnf_path))
r={'state':'NOT_STARTED','k':33,
   'source_sha256':hashlib.sha256(raw).hexdigest(),
   'cnf_sha256':hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
   'number_original_1323_candidates':1323,
   'subfamily_exact_mass20_candidates':162,
   'number_original_sources':1192,
   'cnf_variables':cnf.nv,'cnf_clauses':len(cnf.clauses),
   'conflict_budget':args.conflicts,
   'mathematical_scope':'ONLY ALL-33-WORDS-c20. Full unrestricted k33 remains undecided.'}
print('MSTAR33_MASS20_RESTRICTED_CNF_GENERATED',json.dumps(r,sort_keys=True),flush=True)
with Glucose4(bootstrap_with=cnf.clauses,with_proof=True) as sat:
 sat.conf_budget(args.conflicts)
 ans=sat.solve_limited(expect_interrupt=False)
 if ans is False:
  proof=sat.get_proof()
  assert proof and proof[-1].strip()=='0'
  path=out/'mass20_k33_original_1192.drup'
  path.write_text('\n'.join(proof)+'\n')
  r['state']='UNSAT_NEEDS_EXTERNAL_DRUP_VERIFICATION'
  r['proof_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
  r['proof_lines']=len(proof)
  print('MSTAR33_MASS20_SUBFAMILY_UNSAT_UNVERIFIED',len(proof),flush=True)
 elif ans is True:
  vals=set(sat.get_model())
  selected=[j for j in range(162) if j+1 in vals]
  assert len(selected)<=33
  verify=0
  for j in selected:verify|=masks[j]
  assert verify.bit_count()==1192
  witness={'k':len(selected),'words':[data['candidates'][orig[j]]['word'] for j in selected],
   'selected_original_indices':[orig[j] for j in selected]}
  (out/'sat_witness.json').write_text(json.dumps(witness,indent=2)+'\n')
  r['state']='SAT_NEEDS_INDEPENDENT_PHYSICAL_HTM_REPLAY'
  print('MSTAR33_MASS20_SUBFAMILY_SAT_WITNESS',len(selected),flush=True)
 else:
  r['state']='UNKNOWN_CONFLICT_BUDGET'
  print('MSTAR33_MASS20_SUBFAMILY_UNKNOWN_NOT_AN_OBSTRUCTION',flush=True)
(out/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')

#!/usr/bin/env python3
"""CUBE-REV 0.18: proof-producing global Rubik k33 SAT over 398x168.

Do not treat 168 as an arbitrary candidate cut: the verifier reconstructs
every original one of 1323 full-physical Rubik columns, every one of the
1192 original source rows, and BOTH all-cardinality quotient witnesses.
Only then does it solve the equivalent unstrengthened <=33 cover CNF.
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
p.add_argument('--output',required=True)
p.add_argument('--conflicts',type=int,default=3000000)
a=p.parse_args()
source=Path(a.physical)
physical_raw=source.read_bytes()
physical=json.loads(physical_raw)
rows=json.loads(Path(a.rows).read_text())
cols=json.loads(Path(a.columns).read_text())
assert physical['counts']=={
 'literal':104976,'partitions':1913,
 'coverageTypes':1477,'maximal':1323,'bases':1192
}
assert rows['physical_input_sha256']==hashlib.sha256(physical_raw).hexdigest()
assert cols['physical_sha256']==hashlib.sha256(physical_raw).hexdigest()
assert cols['row_core_sha256']==hashlib.sha256(Path(a.rows).read_bytes()).hexdigest()
original=[int(c['mask'],16) for c in physical['candidates']]
keep_rows=list(map(int,rows['retained_row_indices']))
map_rows=list(map(int,rows['removed_row_implication_witnesses']))
keep_cols=list(map(int,cols['representative_original_candidate_ids']))
map_cols=list(map(int,cols['dominator_original_id_for_each_original_candidate']))
assert len(keep_rows)==398 and len(map_rows)==1192
assert len(keep_cols)==168 and len(map_cols)==1323
assert len(set(keep_cols))==168
original_supports=[0]*1192
for j,m in enumerate(original):
    while m:
        low=m&-m
        original_supports[low.bit_length()-1] |=1<<j
        m ^=low
for row,r in enumerate(map_rows):
    assert r in keep_rows and (original_supports[r]&~original_supports[row])==0
projected=[sum(1<<i for i,r in enumerate(keep_rows) if m>>r&1)
           for m in original]
for j,dom in enumerate(map_cols):
    assert dom in keep_cols and (projected[j]&~projected[dom])==0
# Ensure all remaining constraints are covered by at least one
# of the true legal face-action representatives.
cnf=CNF()
for original_row in keep_rows:
    lits=[i+1 for i,j in enumerate(keep_cols)
          if original[j]>>original_row&1]
    assert lits,("Missing source",original_row)
    cnf.append(lits)
pool=IDPool(start_from=169)
cnf.extend(CardEnc.atmost(
    lits=list(range(1,169)),bound=33,
    encoding=EncType.seqcounter,vpool=pool).clauses)
out=Path(a.output)
out.mkdir(parents=True,exist_ok=True)
cnf_file=out/'cube_original_398x168_k33.cnf'
cnf.to_file(str(cnf_file))
receipt={
  'problem':'CUBE-REV_018_REAL_3x3_HTM_MSTAR_K33_DOUBLE_QUOTIENT',
  'state':'NOT_YET_SOLVED',
  'physical_sha256':hashlib.sha256(physical_raw).hexdigest(),
  'row_certificate_sha256':hashlib.sha256(Path(a.rows).read_bytes()).hexdigest(),
  'column_certificate_sha256':hashlib.sha256(Path(a.columns).read_bytes()).hexdigest(),
  'cnf_sha256':hashlib.sha256(cnf_file.read_bytes()).hexdigest(),
  'equivalent_full_original_source_rows':1192,
  'equivalent_full_original_maximal_word_candidates':1323,
  'reduced_original_source_rows':398,
  'reduced_actual_HTM_words':168,
  'k':33,
  'sat_variables':cnf.nv,
  'sat_clauses':len(cnf.clauses),
  'conflict_budget':a.conflicts,
  'exact_mathematical_optimum_certified':False,
  'warning':'UNSAT requires independent DRUP check; SAT requires full Rubik HTM move replay.'
}
print('CUBE_REV_018_398_X_168_PHYSICAL_K33_CNF_READY',
      json.dumps(receipt,sort_keys=True),flush=True)
with Glucose4(bootstrap_with=cnf.clauses,with_proof=True) as sat:
    sat.conf_budget(a.conflicts)
    ans=sat.solve_limited(expect_interrupt=False)
    if ans is False:
        proof=sat.get_proof()
        assert proof and proof[-1].strip()=='0'
        path=out/'cube_original_398x168_k33.drup'
        path.write_text('\n'.join(proof)+'\n')
        receipt['state']='UNSAT_EXPLICIT_DRUP_NEEDS_EXTERNAL_CHECK'
        receipt['proof_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        receipt['proof_lines']=len(proof)
        print('CUBE_REV_018_398X168_K33_UNSAT_DRUP_EMITTED',
              len(proof),flush=True)
    elif ans is True:
        values=set(sat.get_model())
        subset=[keep_cols[i] for i in range(168) if i+1 in values]
        assert len(subset)<=33
        union=0
        for i in subset:union|=original[i]
        assert union.bit_count()==1192
        words=[physical['candidates'][j]['word'] for j in subset]
        (out/'sat_witness.json').write_text(json.dumps(
            {'schema':'cube-rev.018.exact-double-reduction-k33-sat',
             'k':len(subset),'indices':subset,'words':words},indent=2)+'\n')
        receipt['state']='SAT_ALL1192_BITSET_PASS_INDEPENDENT_HTM_REPLAY_PENDING'
        receipt['witness_size']=len(subset)
        print('CUBE_REV_018_398X168_K33_SAT_MOVE_REPLAY_PENDING',
              len(subset),flush=True)
    else:
        receipt['state']='UNKNOWN_SAT_CONFLICT_BUDGET'
        print('CUBE_REV_018_398X168_K33_UNKNOWN_NO_THEOREM',flush=True)
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')

#!/usr/bin/env python3
"""Exact physical full-1192-source <=7 SAT/DRUP court for CUBE-REV 0.19.
Requires validated P12 R5=7 and independently integer-audited P13 >=2 high.
SAT must replay actual physical 5HTM word histories. UNSAT must be checked
against emitted exact CNF with an *independent* external drat-trim checker.
A conflict budget expiry means UNKNOWN, NEVER UNSAT.
"""
import argparse,json,hashlib,time
from pathlib import Path
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Glucose4
P=argparse.ArgumentParser()
for x in ('physical','maps','prepared','output'):P.add_argument('--'+x,required=True)
P.add_argument('--conflicts',type=int,default=10000000)
P.add_argument('--exact-high-count',type=int,choices=range(2,8),default=None,help='Optional disjoint high-rank-count branch. UNSAT excludes only this branch until every t=2..7 is checked.')
a=P.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest();bases=json.loads(raw)['bases']
try:maps=json.loads(Path(a.maps).read_text())
except ValueError:maps=[list(map(int,l.split())) for l in Path(a.maps).read_text().splitlines()]
assert len(maps)==18 and all(len(x)==24 and len(set(x))==24 for x in maps)
d=json.loads(Path(a.prepared).read_text());assert d['frozen_physical_sha256']==sha
assert d['original_requirement_count']==1192 and d['original_all_k_reduced_row_count']==544
assert d['selected_full_original_k7_physical_column_count']==2403
assert d['first_high_count']==69 and d['rank_at_least_6_minimum_for_k7']==2
assert d['dual_derived_forbidden_pair_count']==102979
rows=d['source_core_row_indices'];proj=list(map(lambda s:int(s,16),d['candidate_core_cover_hex']))
cols=list(map(lambda s:int(s,16),d['candidate_original_source_cover_hex']))
ranks=d['candidate_partition_ranks'];words=d['candidate_move_words'];high=[i+1 for i,k in enumerate(ranks) if k>=6]
assert len(rows)==544 and len(cols)==len(proj)==len(words)==len(ranks)==2403
assert sum(r==5 for r in ranks)==1355 and len(high)==1048
assert len(set(d['first_high_representative_1based']))==69
assert all(ranks[z-1]>=6 for z in d['first_high_representative_1based'])
assert all(len(w)==5 and all(0<=i<18 for i in w) for w in words)
for j,(w,mask) in enumerate(zip(words,cols)):
 st=[2*i for i in range(12)];bits=[0]*12
 for t,act in enumerate(w):
  st=[maps[act][s] for s in st];bits=[o|((st[i]&1)<<t) for i,o in enumerate(bits)]
 blocks={}
 for i,b in enumerate(bits):blocks[b]=blocks.get(b,0)|(1<<i)
 bs=tuple(blocks.values())
 orig=sum(1<<i for i,a in enumerate(bases) if all((a&b).bit_count()<=1 for b in bs))
 assert orig==mask and len(bs)==ranks[j],('PHYSICAL_ORIGINAL_WITNESS_REPLAY_FAIL',j)
 assert proj[j]==sum(1<<i for i,row in enumerate(rows) if orig>>row&1)
print('P13_ORIGINAL_PHYSICAL_ALL_2403_WORD_REPRESENTATIVES_REPLAY_PASS',flush=True)

cnf=CNF();start=time.monotonic();N=len(proj)
for j in range(544):
 clause=[i+1 for i,c in enumerate(proj) if (c>>j)&1]
 assert clause
 cnf.append(clause)
cnf.append(d['first_high_representative_1based'])
for pair in d['dual_derived_forbidden_pair_literals']:
 assert len(pair)==2 and all(-N<=x<=-1 for x in pair)
 cnf.append(pair)
pool=IDPool(start_from=N+1)
cnf.extend(CardEnc.atleast(lits=high,bound=2,encoding=EncType.totalizer,vpool=pool).clauses)
cnf.extend(CardEnc.atmost(lits=list(range(1,N+1)),bound=7,encoding=EncType.seqcounter,vpool=pool).clauses)
if a.exact_high_count is not None:
 cnf.extend(CardEnc.equals(lits=high,bound=a.exact_high_count,encoding=EncType.totalizer,vpool=pool).clauses)
stem='P13_full_original_k7_physical'+(f'_high{a.exact_high_count}' if a.exact_high_count is not None else '')
cnff=out/(stem+'.cnf');cnf.to_file(str(cnff))
cnfsha=hashlib.sha256(cnff.read_bytes()).hexdigest()
print('P13_FULL_ORIGINAL_SOURCE_SEVEN_CNF_READY',json.dumps({'variables':cnf.nv,'clauses':len(cnf.clauses),'cnf_sha256':cnfsha,'seconds':round(time.monotonic()-start,1)}),flush=True)
receipt={'schema':'cube-rev.019.P13.full-original-L5-k7-SAT-proof-protocol.v1','state':'UNKNOWN',
 'physical_sha256':sha,'input_kernel_sha256':hashlib.sha256(Path(a.prepared).read_bytes()).hexdigest(),
 'cnf_sha256':cnfsha,'cnf_variables':cnf.nv,'cnf_clauses':len(cnf.clauses),
 'cover_rows_original_544':544,'real_word_choices':N,'cardinality_at_most':7,
 'at_least_two_high_rank_words_proven_by_P13_integer_court':True,
 'representative_high_orbit_clause_size':69,'sound_original_dual_pair_conflicts':102979,
 'conflict_budget':a.conflicts,'high_rank_exactly':a.exact_high_count,
 'independent_external_unsat_proof_check':'NOT_YET'}
try:
 with Glucose4(bootstrap_with=cnf.clauses,with_proof=True) as solver:
  solver.conf_budget(a.conflicts)
  answer=solver.solve_limited(expect_interrupt=False)
  if answer is True:
   sol=set(solver.get_model());selected=[i for i in range(N) if i+1 in sol]
   original=0
   for i in selected:original|=cols[i]
   assert len(selected)<=7 and original==(1<<1192)-1
   five=[i for i,b in enumerate(bases) if b.bit_count()==5];private=[]
   for i in selected:
    private_rows=[row for row in five if (cols[i]>>row)&1 and sum((cols[j]>>row)&1 for j in selected)==1]
    assert private_rows,('P12_PRIVATE_R5_WITNESS_FAIL',i)
    private.append(private_rows[0])
   witness={'selected_actual_five_HTM_action_indices':[words[i] for i in selected],
    'selected_full_physical_source_cover_hex':[hex(cols[i]) for i in selected],
    'original_all_1192_source_union_count':original.bit_count(),
    'selected_reduced_column_indices':selected,'private_five_source_witness_original_indices':private}
   (out/('P13_SEVEN_FULL_SOURCE_PHYSICAL_SAT_WITNESS.json' if a.exact_high_count is None else stem+'.sat_witness.json')).write_text(json.dumps(witness,indent=2)+'\n')
   receipt['state']='SAT_SEVEN_REAL_PHYSICAL_WORDS_INDEPENDENTLY_REPLAYED'
   print('CUBE_REV_019_P13_PHYSICAL_SEVEN_FULL_SOURCE_SAT_WITNESS_PASS',flush=True)
  elif answer is False:
   proof=solver.get_proof();assert proof
   proof_path=out/(stem+'.drup')
   proof_path.write_text('\n'.join(proof)+'\n')
   receipt['state']='UNSAT_DRUP_EMITTED_EXTERNAL_CHECK_PENDING'
   receipt['drup_sha256']=hashlib.sha256(proof_path.read_bytes()).hexdigest()
   print('CUBE_REV_019_P13_K7_UNSAT_PROOF_EMITTED_NOT_YET_INDEPENDENTLY_VERIFIED',flush=True)
  else:
   receipt['state']='UNKNOWN_CONFLICT_BUDGET_EXHAUSTED'
   print('CUBE_REV_019_P13_SEVEN_FULL_SOURCE_STILL_UNKNOWN',flush=True)
finally:
 receipt['elapsed_seconds']=round(time.monotonic()-start,2)
 (out/('P13_full_original_k7_SAT_decision_receipt.json' if a.exact_high_count is None else stem+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
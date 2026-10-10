#!/usr/bin/env python3
"""Independent receipt compiler for the original full CUBE-REV 0.19 L5 optimum.

Does NOT call SAT/LP: checks frozen source SHA, P12 seven lower, fresh four
rank-seven case coverage, verified t=0, t=1-3 and t=5-7 receipts, then
independently replays the concrete 8-word physical cover against all original
1192 requirement bitmasks via the 18x24 physical HTM edge automaton.

Each exclusion certificate remains a separate inspectable file; this checker
binds their scope/sha/case partition and positive witness into a theorem claim.
"""
import argparse,json,hashlib,math
from pathlib import Path
P=argparse.ArgumentParser()
for x in ('physical','maps','p12','t0','t123','t4','t567','output'):P.add_argument('--'+x,required=True)
a=P.parse_args()
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
sources=json.loads(raw)['bases'];assert len(sources)==1192
r5=[i for i,z in enumerate(sources) if z.bit_count()==5];assert len(r5)==480

def read(path):return json.loads(Path(path).read_text())
p12,t0,t123,t4,t567=[read(getattr(a,name)) for name in ('p12','t0','t123','t4','t567')]
assert p12['source_original_sha256']==sha
assert p12['physical_dictionary_minimum']==7
assert p12['result']=='CUBE_REV_019_R5_PHYSICAL_EXACT_SEVEN_INDEPENDENT_FINITE_COURTS_PASS'
assert t0['physical_source_sha256']==sha
assert t0['result']=='P13_T0_NO_RANK7_WORD_SEVEN_ORIGINAL_SOURCE_COVER_IMPOSSIBLE_FINITE_PROOF_PASS'
assert t0['integer_residual_dual_cases_verified']==65
assert t0['rank6_first_word_orbit_representatives']==74
assert t0['remaining_cases_fully_exhausted']==9 and t0['remaining_case_nodes']==5082
assert t123['source_sha256']==sha
assert t123['result']=='CUBE_REV_019_P13_ALL_374_RAW_PHYSICAL_RANK7_1_2_3_INTEGER_DUAL_ORBITS_PASS'
assert t123['verified_conditional_integer_certificates']==374
assert {int(k):v['representatives'] for k,v in t123['orbit_summary'].items()}=={1:3,2:44,3:327}
assert t4['physical_source_sha256']==sha
assert t4['result']=='P13_T4_ALL_2361_ORBITS_FRESH_INDEPENDENT_COMPLETE_PASS'
assert t4['rechecked_orbits']==2361 and t4['rechecked_first_low_trials']==359004
assert t567['source_sha256']==sha
assert t567['state']=='CUBE_REV_019_P13_ORIGINAL_SEVEN_RANK7_COUNT_5_6_7_ALL_EXCLUDED_INTEGER_PASS'
assert t567['rank7_count5_symmetry_reps']==12717
assert t567['rank7_count6_original_combinations']==math.comb(32,6)==906192
assert t567['rank7_count7_original_combinations']==math.comb(32,7)==3365856
assert t567['rank7_count7_best_original_five_covered']<480

mtext=Path(a.maps).read_text()
try:maps=json.loads(mtext)
except ValueError:maps=[list(map(int,l.split())) for l in mtext.splitlines() if l.strip()]
assert len(maps)==18 and all(len(a)==24 and len(set(a))==24 for a in maps)
A=[f+s for f in 'URFDLB' for s in ('',"'",'2')]
assert len(A)==18
words=["F' B' L F B","F' B' R F B","F' B' D F B","F L2 B' D2 F", "F U2 B R2 F","F' B' U F B","F B L F B","F B R F B"]
assert len(words)==8 and all(len(w.split())==5 for w in words)
covered=0;rank_list=[];masks=[]
for w in words:
 states=[2*i for i in range(12)];hist=[0]*12
 for t,action in enumerate(w.split()):
  nextidx=A.index(action)
  states=[maps[nextidx][s] for s in states]
  hist=[v|((states[i]&1)<<t) for i,v in enumerate(hist)]
 outmask=0
 for j,req in enumerate(sources):
  observations=[hist[i] for i in range(12) if req>>i&1]
  if len(observations)==len(set(observations)):outmask|=1<<j
 covered|=outmask;rank_list.append(len(set(hist)));masks.append(outmask)
 assert outmask.bit_count()>=0
assert covered==(1<<1192)-1,('EIGHT_WORD_SOURCE_COVER_BROKEN',covered.bit_count())
# Existence of eight words, absence of <=6 from P12 original R5 subset,
# and exhaustive rank7 count 0..7 for exactly 7 words imply M*=8.
receipt={
 'schema':'cube-rev.019.P13.original-1192-source-exact-L5-integer-eight.compiled-finite-receipt.v1',
 'result':'CUBE_REV_019_P13_ORIGINAL_FULL_1192_PHYSICAL_MSTAR5_EXACT_EIGHT_LOCAL_FINITE_PROOF_PASS',
 'frozen_original_physical_sha256':sha,
 'source_requirements':1192,'five_source_subfamily':480,'word_length':5,
 'exact_minimum':8,'independent_external_CI':'NOT_YET_CHECKED',
 'local_case_split':{
  'rank7_count_0':{'first_rank6_orbits':74,'integer_duals':65,'independent_finite_branches':9,'branch_nodes':5082},
  'rank7_counts_1_2_3':{'conditioned_original_source_integer_dual_courts':374,'orbit_reps':{'1':3,'2':44,'3':327}},
  'rank7_count_4':{'symmetry_orbits_checked':2361,'original_rank7_quadruples':35960,'first_low_cases_checked':359004},
  'rank7_counts_5_6_7':{'rank7_five_orbits':12717,'rank7_six_subsets':906192,'rank7_seven_subsets':3365856}},
 'physical_eight_word_witness':words,
 'witness_partition_ranks':rank_list,
 'witness_individual_original_requirements_covered':[m.bit_count() for m in masks],
 'witness_union_all_1192':covered.bit_count(),
 'input_receipt_sha256':{n:hashlib.sha256(Path(getattr(a,n)).read_bytes()).hexdigest() for n in ('p12','t0','t123','t4','t567')},
 'proof_scope':'Fixed original 1192 source subsets, tracked UR edge at one of 12 original zero-flip positions, 18 physical HTM actions, full cumulative flip history after each of five preset actions; dictionary unit cost, fixed nonadaptive words, known resettable source family.',
 'not_claimed':'Formal Lean/Coq proof, external DRUP/PB kernel acceptance, result for full Rubik cube states or humans.'}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['result'],'original_physical',sha,'witness_union',covered.bit_count(),flush=True)
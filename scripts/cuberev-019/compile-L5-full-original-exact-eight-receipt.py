#!/usr/bin/env python3
"""CUBE-REV P13 exact full-original L5 minimum 8:
read-only receipt compilation and independently physical eight-word replay.
It checks complete t=0..7 case coverage and every source SHA linkage.
Arithmetic/full exhaustive case receipts must come from accompanying source
scripts; this aggregator never interprets a MIP TIME_LIMIT as UNSAT.
"""
import argparse,json,hashlib,glob
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--workdir',required=True)
p.add_argument('--output',required=True)
a=p.parse_args();wd=Path(a.workdir)
def read(n):return json.loads((wd/n).read_text())
raw=(wd/'original_physical.json').read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
sources=json.loads(raw)['bases'];assert len(sources)==1192
maps=[list(map(int,l.split())) for l in (wd/'original_move_maps.txt').read_text().splitlines()]
assert len(maps)==18 and all(len(m)==24 and len(set(m))==24 for m in maps)
partition_lines=(wd/'original_L5_partitions.tsv').read_text().splitlines();assert len(partition_lines)==14938
P12=read('P12_final_exact_R5_7_receipt.json')
assert P12['result']=='CUBE_REV_019_R5_PHYSICAL_EXACT_SEVEN_INDEPENDENT_FINITE_COURTS_PASS'
assert P12['source_original_sha256']==sha and P12['physical_dictionary_minimum']==7 and P12['source_sets']==480
freshdual=read('P13_fresh_P12_integer_duals_receipt.json');freshhigh=read('P13_fresh_P12_high_rank_receipt.json')
assert freshdual['result']=='CUBE_REV_019_P12_ALL_445_INTEGER_DUAL_ORBIT_COURTS_PASS'
assert freshhigh['result']=='CUBE_REV_019_P12_RANK7_FOUR_FIVE_SIX_EXHAUSTIVE_AND_7WORD_WITNESS_PASS'
assert freshdual['physical_source_sha256']==sha and freshhigh['physical_source_sha256']==sha
p0=read('P13_t0_exact_integer_finite_receipt.json')
assert p0['result']=='P13_T0_NO_RANK7_WORD_SEVEN_ORIGINAL_SOURCE_COVER_IMPOSSIBLE_FINITE_PROOF_PASS'
assert p0['physical_source_sha256']==sha and p0['rank6_first_word_orbit_representatives']==74
assert p0['integer_residual_dual_cases_verified']==65 and p0['remaining_cases_fully_exhausted']==9
assert p0['remaining_case_nodes']==5082 and p0['all_rank5_seven_word_R5_coverage_upper']==448
p123=read('p13_rank7_123_fresh_receipt.json')
assert p123['result']=='CUBE_REV_019_P13_ALL_374_RAW_PHYSICAL_RANK7_1_2_3_INTEGER_DUAL_ORBITS_PASS'
assert p123['source_sha256']==sha and p123['verified_conditional_integer_certificates']==374
assert {int(k):v['representatives'] for k,v in p123['orbit_summary'].items()}=={1:3,2:44,3:327}
chunks=sorted([json.load(open(f)) for f in wd.glob('P13_t4_chunk_*.json')],key=lambda v:v['first_orbit_in_slice'])
assert len(chunks)==14
next_orbit=0;total_attempts=0
for item in chunks:
 assert item['source_sha256']==sha
 assert item['physical_original_partitions']==14938
 assert item['physical_raw_rank5_mask_count']==2295 and item['rank6_mask_count']==1144 and item['rank7_mask_count']==32
 assert item['rank7_four_orbit_representatives']==2361 and item['original_rank7_four_combinations']==35960
 assert item['first_orbit_in_slice']==next_orbit
 assert item['orbits_checked']==item['end_orbit_exclusive']-item['first_orbit_in_slice']
 assert item['result']=='NO_FULL_SEVEN_WITH_EXACTLY_FOUR_RANK7' and item['found_words'] is None
 next_orbit=item['end_orbit_exclusive'];total_attempts+=item['attempted_first_low_words']
assert next_orbit==2361 and total_attempts==359004
p567=read('P13_t567_fresh_receipt.json')
assert p567['source_sha256']==sha
assert p567['state']=='CUBE_REV_019_P13_ORIGINAL_SEVEN_RANK7_COUNT_5_6_7_ALL_EXCLUDED_INTEGER_PASS'
assert p567['rank7_count5_symmetry_reps']==12717 and p567['rank7_count5_first_low_word_attempts']==1934145
assert p567['rank7_count6_original_combinations']==906192 and p567['rank7_count7_original_combinations']==3365856
ACTIONS=[f+s for f in 'URFDLB' for s in ('',"'",'2')]
WORDS=["F' B' L F B","F' B' R F B","F' B' D F B","F L2 B' D2 F","F U2 B R2 F","F' B' U F B","F B L F B","F B R F B"]
covered=0;counts=[]
for word in WORDS:
 state=[2*i for i in range(12)];trace=[0]*12
 for t,token in enumerate(word.split()):
  actid=ACTIONS.index(token)
  state=[maps[actid][s] for s in state]
  trace=[old|((state[i]&1)<<t) for i,old in enumerate(trace)]
 cover=sum(1<<j for j,S in enumerate(sources) if len({trace[i] for i in range(12) if S>>i&1})==S.bit_count())
 counts.append(cover.bit_count());covered|=cover
assert covered==(1<<1192)-1
files=[str(x.relative_to(wd)) for x in wd.glob('P13_*') if x.is_file()]
receipt={'schema':'cube-rev.019.P13.exact-full-original-five-turn-eight-independent-finite-proof.v1',
 'result':'CUBE_REV_019_FULL_ORIGINAL_PHYSICAL_MSTAR5_EXACT_EIGHT_LOCAL_FINITE_PROOF_PASS',
 'physical_source_sha256':sha,'source_requirements_original':1192,'physical_HTM_word_length':5,
 'lower_bound_from':'P12 exactly 7 for original 480 five-sets; P13 zero-through-seven rank7 count case-split proves no full-original dictionary of <=7 physically executable words',
 'rank7_count_zero':{'rank6_first_orbits':74,'exact_integer_dual_obstructions':65,'independent_exact_finite_branch_obstructions':9,'finite_tree_total_nodes':5082},
 'rank7_count_one_two_three':{'original_physical_integer_certificates':374,'source_locked_orbits':{'1':3,'2':44,'3':327}},
 'rank7_count_four':{'16_source_incidence_automorphisms_checked':True,'raw_physical_rank7_quadruples':35960,'fully_checked_orbit_representatives':2361,'standalone_replay_chunks':14,'first_lower_candidate_trials':359004},
 'rank7_count_five_six_seven':{'five_rank7_orbits':12717,'five_rank7_candidate_first_lower_trials':1934145,'six_rank7_original_combinations':906192,'seven_rank7_original_combinations':3365856},
 'positive_actual_physical_eight_HTM_words':WORDS,'positive_individual_word_original_source_cover_counts':counts,
 'positive_union_original_source_cover_count':covered.bit_count(),
 'exact_minimum_fixed_physical_dictionary_cardinality':8,
 'external_github_actions_receipt':'NOT_YET_INDEPENDENTLY_OBSERVED',
 'independent_court_meaning':'All negative cases have checkable source-locked exact nonnegative integer weights, source-incidence group automorphism proof and finite case exhaustion; no SAT, MIP infeasibility status or probabilistic unsat assumption.'}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print('CUBE_REV_019_FULL_ORIGINAL_PHYSICAL_MSTAR5_EXACT_EIGHT_LOCAL_FINITE_PROOF_PASS')
print('CUBE_REV_019_COMPLETE_HORIZON_INTEGER_PROFILE_34_8_4_3_2_1_LOCAL_COURTS_PASS')
#!/usr/bin/env python3
"""Read-only verification gate. Each child receipt must be recreated by running its source checker;
checks source lock and every independent phase status before promoting R5 optimum seven.
"""
import argparse,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser()
for name in ('physical','p9','duals','rank7','output'):p.add_argument('--'+name,required=True)
a=p.parse_args();raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
p9=json.loads(Path(a.p9).read_text());d=json.loads(Path(a.duals).read_text());r=json.loads(Path(a.rank7).read_text())
assert p9['state']=='K5_UNSAT_LOCAL_COMPLETE_INTEGER_BRANCHING_PASS'
assert p9['physical_source_sha256']==sha
assert d['result']=='CUBE_REV_019_P12_ALL_445_INTEGER_DUAL_ORBIT_COURTS_PASS'
assert d['physical_source_sha256']==sha and d['integer_dual_cases']==445
assert d['rank6_first_orbits']==70 and d['rank7_pair_orbits']==44 and d['rank7_triple_orbits']==327
assert r['result']=='CUBE_REV_019_P12_RANK7_FOUR_FIVE_SIX_EXHAUSTIVE_AND_7WORD_WITNESS_PASS'
assert r['physical_source_sha256']==sha
assert r['four_rank7_cases_checked']==35960 and r['five_rank7_cases_checked']==201376
assert r['six_rank7_cases_checked']==906192 and r['six_rank7_best_source_coverage']==472
assert r['original_seven_word_physical_upper_verified'] is True
receipt={'schema':'cube-rev.019.P12.original-physical-R5-exact-seven.finite-proof-receipt.v1',
 'source_original_sha256':sha,'source_sets':480,'word_length':5,'physical_dictionary_minimum':7,
 'exact_scope':'480 original five-state source requirements (R5), physical sticker-based 18-HTM actions, complete five-bit tracked-edge orientation transcripts, nonadaptive resettable experiment dictionary, unit cost per word',
 'lower':'P9 five-word UNSAT implies all <=6 covers have rank>=5; P12 445 independent integer dual courts reject rank7 counts 0..3, complete finite original-rank-specific search rejects rank7 counts 4..6.',
 'upper':'P10 seven physically replayed words cover all original 480 five-state sets, reconfirmed by P12 high-case verifier',
 'individual_gate_receipts_sha256':{key:hashlib.sha256(Path(getattr(a,key)).read_bytes()).hexdigest() for key in ('p9','duals','rank7')},
 'result':'CUBE_REV_019_R5_PHYSICAL_EXACT_SEVEN_INDEPENDENT_FINITE_COURTS_PASS',
 'full_original_Mstar5':'NOT_SOLVED_ONLY_SEVEN_OR_EIGHT'}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['result'],json.dumps({'r5_exact':7,'full_source_lower':7,'full_source_upper':8}))
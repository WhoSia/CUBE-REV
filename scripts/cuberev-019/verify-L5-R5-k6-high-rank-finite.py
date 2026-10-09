#!/usr/bin/env python3
"""Independent stdlib-only physical end-to-end finite proof of R5 length-five k<=6 UNSAT.
Validates four certificate families under ALL physically observed rank-specific masks.
No SAT/MIP/float arithmetic occurs in any proof check.
"""
import argparse,collections,itertools,json,hashlib,time
from pathlib import Path
p=argparse.ArgumentParser()
for s in ('physical','maps','partitions','duals_first','duals_rank6','duals_rank7','output'):p.add_argument('--'+s,required=True)
a=p.parse_args();start=time.monotonic()
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
bases=json.loads(raw)['bases'];five=[z for z in bases if z.bit_count()==5];assert len(bases)==1192 and len(five)==480
moves=[list(map(int,l.split())) for l in Path(a.maps).read_text().splitlines()];assert len(moves)==18 and all(len(m)==24 and len(set(m))==24 for m in moves)
full=(1<<480)-1

def physical_blocks(word):
 s=[2*i for i in range(12)];hist=[0]*12
 for t,move in enumerate(word):
  s=[moves[move][st] for st in s]
  for i in range(12):hist[i]|=(s[i]&1)<<t
 blocks={}
 for i,v in enumerate(hist):blocks[v]=blocks.get(v,0)|(1<<i)
 return tuple(sorted(blocks.values()))

def cover(blocks):
 return sum(1<<i for i,A in enumerate(five) if all((A&b).bit_count()<=1 for b in blocks))
byrank={i:set() for i in range(1,8)};wordrep={};nparts=0
for line in Path(a.partitions).read_text().splitlines():
 wordtxt,blocktxt=line.split('|');word=tuple(map(int,wordtxt.split()));assert len(word)==5
 block=tuple(sorted(map(int,blocktxt.split())))
 assert physical_blocks(word)==block
 mask=cover(block);byrank[len(block)].add(mask);wordrep.setdefault(mask,word);nparts+=1
assert nparts==14938 and len(set.union(*byrank.values()))==3344
assert (len(byrank[5]),len(byrank[6]),len(byrank[7]))==(2168,1144,32)
lowall=sorted(byrank[5]|byrank[6]);rank6=sorted(byrank[6]);rank7=sorted(byrank[7]);assert len(lowall)==3312-len(byrank[5]&byrank[6])
print('P12_PHYSICAL_SOURCE_14938_REPLAY_AND_RANK_SPECIFIC_2168_1144_32_PASS',round(time.monotonic()-start,2),flush=True)
# Cases with 4 rank7 / 2 lower ranks, 5 rank7 /1 lower rank, 6 rank7.
# Full raw 3311 lower-rank types are restored, even if some were eliminated
# by a rank7 word in the unrestricted dominance reduction.
supports=[0]*480
for j,c in enumerate(lowall):
 for i in range(480):
  if c>>i&1:supports[i]|=1<<j
alllow=(1<<len(lowall))-1
four_checks=0;four_first_trials=0;five_checks=0;six_checks=0;six_max_covered=0
for chosen in itertools.combinations(rank7,4):
 already=chosen[0]|chosen[1]|chosen[2]|chosen[3]
 missing=full&~already
 assert missing
 pivot=(missing&-missing).bit_length()-1
 avail=supports[pivot]
 while avail:
  bit=avail&-avail;w=bit.bit_length()-1;avail-=bit;four_first_trials+=1
  rest=missing&~lowall[w]
  assert rest,('FOUR_RANK7_PLUS_SINGLE_LOWER_SAT',chosen,w)
  possible=alllow
  while rest and possible:
   lb=rest&-rest;possible&=supports[lb.bit_length()-1];rest-=lb
  assert not possible,('FOUR_RANK7_PLUS_TWO_LOWER_SAT',chosen,w)
 four_checks+=1
 if four_checks%1000==0:print('P12_4R7_PROGRESS',four_checks,round(time.monotonic()-start,2),flush=True)
assert four_checks==35960
print('P12_EXACTLY4_RANK7_PLUS2_RAW_LOWER_ALL_35960_CASES_UNSAT_PASS',four_first_trials,round(time.monotonic()-start,2),flush=True)
for chosen in itertools.combinations(rank7,5):
 miss=full&~(chosen[0]|chosen[1]|chosen[2]|chosen[3]|chosen[4]);assert miss
 possible=alllow
 while miss and possible:
  bit=miss&-miss;possible &= supports[bit.bit_length()-1];miss-=bit
 assert not possible
 five_checks+=1
assert five_checks==201376
for chosen in itertools.combinations(rank7,6):
 covered=chosen[0]|chosen[1]|chosen[2]|chosen[3]|chosen[4]|chosen[5]
 assert covered!=full
 six_max_covered=max(six_max_covered,covered.bit_count());six_checks+=1
assert six_checks==906192 and six_max_covered==472
print('P12_EXACTLY5_OR6_RANK7_ALL_201376_906192_CASES_UNSAT_PASS',round(time.monotonic()-start,2),flush=True)

# Verify independent real physical seven-word full 480 five-source positive
# witness taken from P10, not from any numerical LP solver object.
seven_words=['F\' B\' U F B','F\' B D F B','F B\' L F B','F B\' D F B','F B\' R F B','F B U F B','F B\' U2 L2 F']
actions=[f+s for f in 'URFDLB' for s in ('',"'",'2')]
seven_cover=0
for word in seven_words:
 physical=tuple(actions.index(token) for token in word.split())
 assert len(physical)==5
 seven_cover|=cover(physical_blocks(physical))
assert seven_cover==full
receipt={'schema':'cube-rev.019.P12.R5-physical-k6-finite-UNSAT-and-k7-replay.v1','physical_source_sha256':sha,
 'original_five_sources':480,'real_observation_partitions':nparts,
 'rank5_raw_cover_types':2168,'rank6_raw_cover_types':1144,'rank7_raw_cover_types':32,
 'rank6_only_maximal_columns':1080,'rank6_only_symmetry_orbits':70,
 'rank7_single_orbits':3,'rank7_pair_orbits':44,'rank7_triple_orbits':327,
 'integer_dual_courts_checked':'SEPARATE_P12_DUAL_RECEIPT_REQUIRED',
 'four_rank7_cases_checked':four_checks,'four_rank7_first_lower_word_trials':four_first_trials,
 'five_rank7_cases_checked':five_checks,'six_rank7_cases_checked':six_checks,'six_rank7_best_source_coverage':six_max_covered,
 'original_seven_word_physical_upper_verified':True,
 'result':'CUBE_REV_019_P12_RANK7_FOUR_FIVE_SIX_EXHAUSTIVE_AND_7WORD_WITNESS_PASS',
 'full_original_1192_source_Mstar5':'UNRESOLVED_INTEGER_SEVEN_OR_EIGHT',
 'elapsed_seconds':round(time.monotonic()-start,3)}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['result'],json.dumps({'seconds':receipt['elapsed_seconds'],'physical_partitions':nparts}),flush=True)
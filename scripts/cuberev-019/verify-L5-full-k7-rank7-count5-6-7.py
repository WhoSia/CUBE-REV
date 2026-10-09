#!/usr/bin/env python3
"""No-SAT original physical L5 full-source k7 rank7-count 5/6/7 exclusion.
Exact original 1192-bit incidence; group closure on ALL physical rank5/6/7
coverage types is asserted prior to any five-rank7 orbit reduction.
"""
import argparse,hashlib,json,time
from pathlib import Path
from itertools import combinations,product
from collections import Counter
p=argparse.ArgumentParser()
for name in ('physical','partitions','output'):p.add_argument('--'+name,required=True)
a=p.parse_args();start=time.monotonic()
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
src=json.loads(raw)['bases'];assert len(src)==1192
full=(1<<1192)-1;fivemask=sum(1<<i for i,b in enumerate(src) if b.bit_count()==5)
physical={5:{},6:{},7:{}};N=0
for line in Path(a.partitions).read_text().splitlines():
 word,blocks=line.split('|');b=list(map(int,blocks.split()));N+=1
 if len(b) not in physical:continue
 cover=sum(1<<i for i,A in enumerate(src) if all((A&z).bit_count()<=1 for z in b))
 physical[len(b)].setdefault(cover,tuple(map(int,word.split())))
assert N==14938 and tuple(len(physical[k]) for k in (5,6,7))==(2295,1144,32)
low=list(physical[5])+list(physical[6]);hi=list(physical[7]);assert len(low)==3439 and len(hi)==32
# Case t=7: all seven chosen physical words rank7; original 480 and all1192 audited.
t7cases=0;t7maxall=0;t7maxfive=0
for chosen in combinations(range(32),7):
 t7cases+=1;union=0
 for i in chosen:union|=hi[i]
 t7maxall=max(t7maxall,union.bit_count());t7maxfive=max(t7maxfive,(union&fivemask).bit_count())
assert t7cases==3365856 and t7maxall==1188 and t7maxfive==476
print('P13_ALL_3365856_SEVEN_RANK7_PHYSICAL_CASES_FAIL_FIVE_SOURCE',flush=True)
# Support for any physically realized L5 rank5/6 word on full original rows.
support=[0]*1192
for j,m in enumerate(low):
 while m:
  b=m&-m;support[b.bit_length()-1]|=1<<j;m-=b
alllow=(1<<len(low))-1
# Case t=6: exactly one low-rank word remains. Intersect original R5 supports,
# then original complete 1192 source supports. No unsound global-rank domination.
t6cases=0;t6five_possible=0
for chosen in combinations(range(32),6):
 t6cases+=1;union=0
 for i in chosen:union|=hi[i]
 rem=fivemask&~union;possible=alllow
 while rem and possible:
  b=rem&-rem;possible&=support[b.bit_length()-1];rem-=b
 if not possible:continue
 t6five_possible+=1
 rem=full&~union
 while rem and possible:
  b=rem&-rem;possible&=support[b.bit_length()-1];rem-=b
 assert not possible,('FULL_SAT_SIX_RANK7_ONE_LOWER',chosen)
assert t6cases==906192 and t6five_possible==16
print('P13_ALL_906192_SIX_RANK7_ONE_REAL_LOWER_CASES_NO_FULL_SOURCE_PASS',flush=True)
# All 16 signed-coordinate incidence automorphisms, including improper
# relabelings, preserve R and the ORIGINAL rank5+rank6, rank7 families.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,-1),(1,0,-1),(-1,0,1),(-1,-1,0),(0,1,1),(0,-1,1),(1,0,1)]
# Reorder of coordinate list irrelevant, but must contain each of the twelve real slots
# at their FROZEN slot indices; reconstruct exactly the frozen canonical sequence.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
coord_index={v:i for i,v in enumerate(coords)};source_index={v:i for i,v in enumerate(src)}
high_index={m:i for i,m in enumerate(hi)};low_set=set(low);maps=[];hist=Counter()
for axes in ((0,1,2),(1,0,2)):
 for signs in product((-1,1),repeat=3):
  position_permutation=[coord_index[tuple(signs[k]*pt[axes[k]] for k in range(3))] for pt in coords]
  source_permutation=[]
  for b in src:
   transformed=sum(1<<position_permutation[k] for k in range(12) if (b>>k)&1)
   assert transformed in source_index
   source_permutation.append(source_index[transformed])
  def T(mask):
   out=0
   while mask:
    bit=mask&-mask;out|=1<<source_permutation[bit.bit_length()-1];mask-=bit
   return out
  assert all(T(m) in low_set for m in low),'RANK5OR6_PHYSICAL_CLOSURE_FAIL'
  assert all(T(m) in high_index for m in hi),'RANK7_PHYSICAL_CLOSURE_FAIL'
  maps.append([high_index[T(m)] for m in hi])
assert len(maps)==16
# Case t=5: choose five rank7 masks plus two ANY rank5/rank6 original masks.
visited=set();orbit_reps=[]
for chosen in combinations(range(32),5):
 if chosen in visited:continue
 orbit={tuple(sorted(g[i] for i in chosen)) for g in maps}
 assert chosen in orbit and visited.isdisjoint(orbit)
 visited.update(orbit);orbit_reps.append(chosen);hist[len(orbit)]+=1
assert len(visited)==201376 and len(orbit_reps)==12717 and hist==Counter({16:12455,8:262})
print('P13_FIVE_RANK7_TWO_LOWER_SAFE_12717_SYMMETRY_REPRESENTATIVES_PASS',flush=True)

def rarest_support(target):
 best=None;size=len(low)+1
 while target:
  bit=target&-target;c=support[bit.bit_length()-1];n=c.bit_count()
  if n<size:best=c;size=n
  target-=bit
 return best
trials=0
for chosen in orbit_reps:
 union=0
 for j in chosen:union|=hi[j]
 missing=full&~union
 candidates=rarest_support(missing)
 while candidates:
  bit=candidates&-candidates;i=bit.bit_length()-1;candidates-=bit;trials+=1
  rem=missing&~low[i]
  assert rem,('UNEXPECTED_ONE_LOWER_FULL_ORIGINAL_COVER',chosen,i)
  candidate_two=alllow
  while rem and candidate_two:
   b=rem&-rem;candidate_two&=support[b.bit_length()-1];rem-=b
  assert not candidate_two,('FULL_SEVEN_WITH_FIVE_RANK7_AND_TWO_LOWER',chosen,i)
assert trials==1934145,(trials)
print('P13_FIVE_RANK7_TWO_LOWER_COMPLETE_SYMMETRY_FINITE_UNSAT_PASS',trials,flush=True)
receipt={'state':'CUBE_REV_019_P13_ORIGINAL_SEVEN_RANK7_COUNT_5_6_7_ALL_EXCLUDED_INTEGER_PASS',
 'source_sha256':sha,'real_L5_observation_partition_count':N,'rank5_original_full_cover_types':2295,
 'rank6_original_full_cover_types':1144,'rank7_original_full_cover_types':32,
 'rank7_count7_original_combinations':t7cases,'rank7_count7_best_full_original_covered':t7maxall,
 'rank7_count7_best_original_five_covered':t7maxfive,
 'rank7_count6_original_combinations':t6cases,'rank7_count6_allow_R5_completion_by_one_lower':t6five_possible,
 'rank7_count5_original_combinations':201376,'rank7_count5_symmetry_reps':12717,
 'rank7_count5_first_low_word_attempts':trials,'physical_16_incidences_preserve_all_raw_candidate_ranks':True,
 'theorem':'Any full-original 7-word dictionary uses no more than four rank7 words',
 'remaining_rank7_counts':[0,1,2,3,4], 'not_claimed':'NO overall original k7 UNSAT conclusion',
 'time_seconds':round(time.monotonic()-start,2)}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['state'],json.dumps({'t5_reps':12717,'t6_R5_possible':t6five_possible,'t7_five_max':t7maxfive}),flush=True)
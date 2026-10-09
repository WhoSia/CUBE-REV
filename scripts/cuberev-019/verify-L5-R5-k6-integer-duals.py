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
# Full 16-element signed coordinate incidence symmetry, some transforms not physical moves.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
pos={v:i for i,v in enumerate(coords)};index={v:i for i,v in enumerate(five)};group=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in itertools.product((-1,1),repeat=3):
  ps=[pos[tuple(signs[k]*point[axes[k]] for k in range(3))] for point in coords]
  src=[index[sum(1<<ps[k] for k in range(12) if (A>>k)&1)] for A in five]
  assert len(set(src))==480
  group.append(src)
assert len(group)==16

def trans(m,g):
 out=0
 while m:
  bit=m&-m;out|=1<<g[bit.bit_length()-1];m-=bit
 return out
for class_n in (5,6,7):
 col=byrank[class_n]
 for g in group:
  assert all(trans(m,g) in col for m in col)

def maxima(candidates):
 k=[]
 for m in sorted(candidates,key=lambda v:(-v.bit_count(),v)):
  if not any(m&~n==0 for n in k):k.append(m)
 return k
# Within-rank source-specific dominance does not change the rank count
# and is safe for the all-rank6 subproblem only.
max6=maxima(byrank[6]);assert len(max6)==1080

def orbits(candidates):
 remaining=set(candidates);reps=[]
 while remaining:
  seed=min(remaining);orb={trans(seed,g) for g in group}
  assert seed in orb and orb<=remaining
  remaining-=orb;reps.append(seed)
 return reps
rank6reps=orbits(max6);rank7reps=orbits(rank7)
assert len(rank6reps)==70 and len(rank7reps)==3
print('P12_RANK_PRESERVING_SYMMETRY_70_AND_3_FIRST_ORBITS_PASS',round(time.monotonic()-start,2),flush=True)

# Exact nonnegative integer mass on original 480 requirement coordinates.
# Existence of a word in given rank class implies its score <= max over
# entire raw physically realized (NOT only globally undominated) class.
def score(mask,positive):
 return sum(w for i,w in positive if mask>>i&1)

def verify_certificate(entries,candidate_masks,budget,selected_union=0):
 positive=[(int(i),int(w)) for i,w in entries]
 assert positive and all(0<=i<480 and w>0 and not (selected_union>>i&1) for i,w in positive)
 assert len({i for i,w in positive})==len(positive)
 W=sum(w for i,w in positive)
 C=max(score(c,positive) for c in candidate_masks)
 assert W>budget*C,(W,budget,C)
 return W,C,W-budget*C

first=json.loads(Path(a.duals_first).read_text());assert first['original_source_sha256']==sha
basecert=first['certificates'][0];assert basecert['type']=='nonseventh_at_least_one_rank5'
weight=basecert['source_row_weight'];C5=max(score(m,weight) for m in byrank[5]);C6=max(score(m,weight) for m in byrank[6]);W=sum(w for i,w in weight)
assert C6>=C5 and W>C5+5*C6
# If any rank5 selected and no rank7, remaining <=5 are rank5 or6:
# budget <=C5+5*C6. All six rank6-only handled by first-word branch.
first_rank7={int(c['selected_first_word_original480_cover_hex'],16):c for c in first['certificates'] if c['type']=='first_rank7_rest_rank6'}
assert set(first_rank7)==set(rank7reps)
for rep,c in first_rank7.items():
 y=c['source_row_weight'];C=max(score(m,y) for m in lowall)
 assert sum(w for i,w in y)>5*C and all(not rep>>i&1 for i,w in y)
print('P12_NO_RANK7_WITH_RANK5_AND_ONE_RANK7_CONDITIONAL_INTEGER_DUALS_PASS',round(time.monotonic()-start,2),flush=True)

six=json.loads(Path(a.duals_rank6).read_text());assert six['physical_source_sha256']==sha
r6d={int(c['fixed_raw_rank6_orbit_representative_mask_hex'],16):c for c in six['certificates']}
assert set(r6d)==set(rank6reps) and len(r6d)==70
for rep,c in r6d.items():
 assert c['strict_gap']==verify_certificate(c['positive_480_source_row_integer_weights'],rank6,5,rep)[2]
print('P12_ALL_70_PHYSICAL_RANK6_ONLY_CONDITIONAL_INTEGER_DUALS_PASS',round(time.monotonic()-start,2),flush=True)

# Pair/triple rank7 orbit representatives cover ALL 32C2 and 32C3
# possible distinct rank7 selections by exact group incidence equivalence.
seven=json.loads(Path(a.duals_rank7).read_text());assert seven['original_source_sha256']==sha
family={2:set(itertools.combinations(rank7,2)),3:set(itertools.combinations(rank7,3))}
pair_reps={2:set(),3:set()}
for c in seven['certificates']:
 fixed=tuple(sorted(int(x,16) for x in c['selected_rank7_coverage_masks_hex']))
 n=len(fixed);assert n in (2,3) and fixed in family[n]
 pair_reps[n].add(fixed)
 pre=0
 for m in fixed:pre|=m
 valid=verify_certificate(c['positive_original_480_source_weights'],lowall,6-n,pre)
 assert c['total_weight']==valid[0] and c['maximum_one_raw_rank5_6_word_weight']==valid[1] and c['exact_integer_gap']==valid[2]
for n in (2,3):
 leftovers=set(family[n])
 for fixed in pair_reps[n]:
  orbit={tuple(sorted(trans(m,g) for m in fixed)) for g in group}
  assert fixed in orbit and orbit<=leftovers
  leftovers-=orbit
 assert not leftovers
assert len(pair_reps[2])==44 and len(pair_reps[3])==327
print('P12_ALL_44_PAIR_AND_327_TRIPLE_RANK7_SYMMETRY_DUALS_PASS',round(time.monotonic()-start,2),flush=True)

duals_receipt={'result':'CUBE_REV_019_P12_ALL_445_INTEGER_DUAL_ORBIT_COURTS_PASS',
 'physical_source_sha256':sha,'original_five_sources':480,
 'real_L5_partitions':nparts,'raw_rank5_types':2168,'raw_rank6_types':1144,
 'rank6_first_orbits':70,'rank7_first_orbits':3,'rank7_pair_orbits':44,'rank7_triple_orbits':327,
 'integer_dual_cases':1+3+70+44+327,
 'proof_rule':'All candidate word capacities checked by exact integer weighted sums over every REAL physically realized rank-specific coverage mask.',
 'elapsed_seconds':round(time.monotonic()-start,3)}
Path(a.output).write_text(json.dumps(duals_receipt,indent=2)+'\n')
print(duals_receipt['result'],duals_receipt['elapsed_seconds'],flush=True)
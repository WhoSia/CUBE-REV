#!/usr/bin/env python3
"""CUBE-REV 0.19 P13. Independent *integer-only* finite verifier for the
LAST original-1192-source L5/k7 subcase t=0 (NO rank-seven word).
Input: physical source, 14,938 witnessed physical partitions, 3 sealed
conditional integer certificate shards. No SAT/LP/MIP dependency.
Proof: 16 group automorphisms; all 74 first-rank6 orbits; 65 exact
original-row residual integer weighted covers; 9 exact <=6 bitset-search
obstructions (5,082 finite branch nodes). No solver statuses trusted.
"""
import argparse,hashlib,json,time
from pathlib import Path
from itertools import product
from collections import Counter
parser=argparse.ArgumentParser()
for name in ('physical','partitions','cert0','cert1','cert2','nine','output'):parser.add_argument('--'+name,required=True)
a=parser.parse_args();t0=time.monotonic()
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
source=json.loads(raw)['bases'];assert len(source)==1192
byrank={5:set(),6:set()};partitions=0
for line in Path(a.partitions).read_text().splitlines():
 word,ps=line.split('|');parts=list(map(int,ps.split()));partitions+=1
 assert len(word.split())==5
 if len(parts) not in byrank:continue
 assert len(set(parts))==len(parts) and sum(v.bit_count() for v in parts)==12
 if parts:
  s=0
  for v in parts:assert not s&v;s|=v
  assert s==4095
 mask=sum(1<<i for i,src in enumerate(source) if all((src&b).bit_count()<=1 for b in parts))
 byrank[len(parts)].add(mask)
assert partitions==14938 and len(byrank[5])==2295 and len(byrank[6])==1144
low=sorted(byrank[5]|byrank[6]);assert len(low)==3439
# Independently prove that an all-rank5 seven-word dictionary cannot cover
# original R5: one physical rank5 word separates at most 64 of 480 five-sets.
five_rows=sum(1<<i for i,b in enumerate(source) if b.bit_count()==5)
assert five_rows.bit_count()==480
max_rank5_five_cover=max((mask&five_rows).bit_count() for mask in byrank[5])
assert max_rank5_five_cover==64 and 7*max_rank5_five_cover==448<480
six=byrank[6]
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
ci={v:i for i,v in enumerate(coords)};si={v:i for i,v in enumerate(source)}
group=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in product((-1,1),repeat=3):
  perm=[ci[tuple(signs[k]*pos[axes[k]] for k in range(3))] for pos in coords]
  grp=[si[sum(1<<perm[j] for j in range(12) if S>>j&1)] for S in source]
  assert len(set(grp))==1192
  group.append(grp)
assert len(group)==16
def transform(mask,g):
 r=0
 while mask:
  bit=mask&-mask;r|=1<<g[bit.bit_length()-1];mask-=bit
 return r
for g in group:
 assert {transform(m,g) for m in byrank[5]}==byrank[5]
 assert {transform(m,g) for m in byrank[6]}==byrank[6]
# Within-rank-six raw physical column set has all 1144 original masks maximal;
# still explicitly verify no two rank-six types dominate each other.
rank6_max=[]
for mask in sorted(six,key=int.bit_count,reverse=True):
 assert not any(mask&~other==0 for other in rank6_max)
 rank6_max.append(mask)
assert len(rank6_max)==1144
seen=set();reps=[]
for mask in sorted(six):
 if mask in seen:continue
 orbit={transform(mask,g) for g in group}
 assert orbit<=six and not (orbit&seen)
 seen.update(orbit);reps.append(mask)
assert len(seen)==1144 and len(reps)==74
assert all(m in six for m in reps)
print('P13_T0_ORIGINAL_1192_SOURCES_RANK5_2295_RANK6_1144_16_GROUP_74_FIRST_WORD_ORBITS_PASS',flush=True)

shards=[json.loads(Path(getattr(a,x)).read_text()) for x in ('cert0','cert1','cert2')]
for sh in shards:
 assert sh['physical_sha256']==sha and sh['original_sources']==1192
 assert sh['raw_rank5_cover_types']==2295 and sh['raw_rank6_cover_types']==1144
 assert sh['rank6_first_word_orbits']==74
 assert sh['low_original_cover_types']==3439
 assert sh['real_physical_partitions']==14938
assert [v['processed_orbit_indices'] for v in shards]==[list(range(0,24)),list(range(24,49)),list(range(49,74))]
certs=[v for sh in shards for v in sh['exact_integer_certificates']]
unresolved=[v for sh in shards for v in sh['open_cases']]
assert len(certs)==65 and len(unresolved)==9
assert {int(z['representative_mask_hex'],16) for z in certs+unresolved}==set(reps)
assert {z['index'] for z in unresolved}=={9,12,15,22,24,44,69,70,72}
# Independent exact integer certificate check for 65 branches.
cert_gaps=[]
for c in certs:
 first=int(c['representative_mask_hex'],16)
 weights={int(k):int(w) for k,w in c['weights_original_row'].items()}
 assert weights and all(0<=j<1192 and w>0 and not(first>>j&1) for j,w in weights.items())
 W=sum(weights.values());B=max(sum(w for i,w in weights.items() if m>>i&1) for m in low)
 assert W==c['W'] and B==c['B'] and W>6*B
 cert_gaps.append(W-6*B)
print('P13_T0_65_ORIGINAL_SOURCE_INTEGER_WEIGHT_PROOFS_PASS','minimum_gap',min(cert_gaps),flush=True)
nine=json.loads(Path(a.nine).read_text())
assert nine['source_sha256']==sha
records=nine['records'];assert len(records)==9
assert {c['index'] for c in unresolved}=={r['first_orbit'] for r in records}
all_sources=(1<<1192)-1
summary=[]
for q,rec in enumerate(records):
 orb=rec['first_orbit'];first=int(rec['first_coverage_hex'],16)
 assert reps[orb]==first and first in six
 assert first==int(next(v['representative_mask_hex'] for v in unresolved if v['index']==orb),16)
 weights={int(k):int(v) for k,v in rec['rows_weights'].items()}
 assert weights and all(0<=r<1192 and v>0 and not(first>>r&1) for r,v in weights.items())
 W=sum(weights.values());B=max(sum(v for r,v in weights.items() if m>>r&1) for m in low)
 assert W==rec['W'] and B==rec['B'] and W>5*B
 T=W-5*B
 assert T==rec['remaining_six_per_word_threshold'] and T>0
 # A 6-word residual cover forces each selected word to cover >= W-5B
 # original-source weighted mass: other five can contribute at most 5B.
 elig=sorted(m for m in low if sum(v for r,v in weights.items() if m>>r&1)>=T)
 assert len(elig)<250
 assert sum(m in byrank[5] for m in elig)==rec['eligible_rank5_words']
 assert sum(m in byrank[6] for m in elig)==rec['eligible_rank6_words']
 # Every physically realized rank-five/rank-six word not eligible is
 # proven unusable in any 6-word completion; no solver-orbit dropping.
 remain=all_sources&~first
 support=[0]*1192
 for j,m in enumerate(elig):
  x=m&remain
  while x:
   b=x&-x;support[b.bit_length()-1]|=1<<j;x-=b
 assert all(support[i] for i in range(1192) if remain>>i&1)
 seen_subproblems=set();nodes_by_depth=[0]*7;proof_nodes=0
 def impossible(residual,budget):
  nonlocal_dummy=0
  # Return True iff there is NO covering dictionary with <=budget
  # additional columns; a successful cover is fatal to our theorem.
  nonlocal_vars=None
  if residual==0:return False
  if budget==0:return True
  key=(residual,budget)
  if key in seen_subproblems:return True
  seen_subproblems.add(key);nodes_by_depth[6-budget]+=1
  # Upper bound on cardinality coverage: even the best budget words
  # cannot exceed the SUM of budget individual original-source gains.
  contributions=sorted(((residual&m).bit_count() for m in elig),reverse=True)
  if sum(contributions[:budget])<residual.bit_count():return True
  # Similarly for ANY nonnegative original-row integer dual weights:
  # total residual dual demand cannot exceed top budget individual
  # weighted residual contributions.
  missing_weight=sum(v for r,v in weights.items() if residual>>r&1)
  capacities=sorted((sum(v for r,v in weights.items() if residual>>r&1 and m>>r&1) for m in elig),reverse=True)
  if sum(capacities[:budget])<missing_weight:return True
  # Exact AND/OR cover proof: select a missing source with the fewest
  # physically executable distinguishing words, and split over ALL
  # candidates that cover that source, not a truncated sample.
  min_options=len(elig)+1;choice=0;x=residual
  while x:
   bit=x&-x;rr=bit.bit_length()-1;x-=bit
   opts=support[rr];num=opts.bit_count()
   if num<min_options:choice=opts;min_options=num
   if min_options==1:break
  if not choice:return True
  options=[];z=choice
  while z:
   bit=z&-z;j=bit.bit_length()-1;z-=bit
   options.append(((residual&elig[j]).bit_count(),j))
  options.sort(reverse=True)
  for _,j in options:
   if not impossible(residual&~elig[j],budget-1):return False
  return True
 assert impossible(remain,6),('UNEXPECTED_REAL_PHYSICAL_SEVEN_WORD_COVER',orb)
 count=sum(nodes_by_depth)
 summary.append({'first_orbit_index':orb,'eligible_rank5_6_word_types':len(elig),'proof_branch_nodes':count,'branch_nodes_by_depth':nodes_by_depth,'original_frozen_dual_weight':W,'max_physical_low_word_weight':B,'necessary_minimum_weight_per_selected_residual_word':T})
 print('P13_T0_RANK6_ORBIT_FINITE_UNSAT_PASS',orb,'cols',len(elig),'nodes',count,flush=True)
assert [r['proof_branch_nodes'] for r in summary]==[958,732,1006,344,274,462,284,453,569]
assert sum(r['proof_branch_nodes'] for r in summary)==5082
receipt={'schema':'cube-rev.019.P13.original-full-1192-source-rank7zero-no-seven-word-independent-int-certificate','result':'P13_T0_NO_RANK7_WORD_SEVEN_ORIGINAL_SOURCE_COVER_IMPOSSIBLE_FINITE_PROOF_PASS',
 'physical_source_sha256':sha,'original_source_requirements':1192,'physical_partition_representatives':14938,'rank5_original_cover_types':2295,'rank6_original_cover_types':1144,'all_rank5_seven_word_R5_coverage_upper':448,'rank6_first_word_orbit_representatives':74,'integer_residual_dual_cases_verified':65,'dual_strict_min_gap':min(cert_gaps),'remaining_cases_fully_exhausted':9,'remaining_case_nodes':5082,'remaining_branch_results':summary,
 'proof_contract':'Any full <=7 cover with rank7-count0 must choose rank6 first, because seven rank5 words cover at most 448 of the original 480 five-source demands. Full 16-way original incidence symmetries allow one of 74 rank6 representatives. Each of 65 reps is excluded by W>6*max(original physical low-word weight). Each of 9 residual reps uses original source integer weight threshold W-5B to remove physically impossible selections and independently checks every branch from the rarest missing source. P12 five-source minimum7 and P13 >=2 high are external prerequisites; this standalone verifier does not re-prove them.'}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print('CUBE_REV_019_P13_RANK7_ZERO_ALL_74_ORBITS_65_INTEGER_DUALS_9_FINITE_BRANCHES_PASS',flush=True)
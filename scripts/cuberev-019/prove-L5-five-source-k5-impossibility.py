#!/usr/bin/env python3
"""CUBE-REV 0.19 P9: SAT-free complete finite k<=5 five-source proof.
Original real 5-HTM sticker-derived maps, all 14938 physical partitions,
480 frozen five-position requirements and a rationally audited integer dual.
No SciPy/MIP/SAT, only exact Python integers and finite exhaustive branching.
"""
import argparse, collections, hashlib, json, time
from pathlib import Path
p=argparse.ArgumentParser()
for s in ('physical','maps','partitions','dual','output'):p.add_argument('--'+s,required=True)
a=p.parse_args();start=time.time()
raw=Path(a.physical).read_bytes();source_sha=hashlib.sha256(raw).hexdigest()
assert source_sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
source=json.loads(raw);bases=source['bases'];assert len(bases)==1192
five=[(idx,int(mask)) for idx,mask in enumerate(bases) if mask.bit_count()==5]
assert len(five)==480
maps=[list(map(int,s.split())) for s in Path(a.maps).read_text().splitlines()]
assert len(maps)==18 and all(len(m)==24 and len(set(m))==24 for m in maps)
cert=json.loads(Path(a.dual).read_text());assert cert['physical_source_sha256']==source_sha
weights={int(k):int(v) for k,v in cert['dual_original_source_rows_scaled'].items()}
assert set(weights).issubset(set(i for i,_ in five))
assert len(weights)==80 and sum(weights.values())==1480 and cert['dual_common_denom']==312
w=[weights.get(i,0) for i,_ in five];weighted=[(j,weight) for j,weight in enumerate(w) if weight]
full=(1<<480)-1

def mass(c):
 return sum(weight for j,weight in weighted if (c>>j)&1)

def actual_blocks(word):
 s=[2*j for j in range(12)];h=[0]*12
 for t,x in enumerate(word):
  s=[maps[x][v] for v in s]
  h=[v|((s[j]&1)<<t) for j,v in enumerate(h)]
 d={}
 for j,v in enumerate(h):d[v]=d.get(v,0)|(1<<j)
 return tuple(sorted(d.values()))

unique={} ; lines=0
for line in Path(a.partitions).read_text().splitlines():
 wtext,btext=line.split('|');word=tuple(map(int,wtext.split()))
 assert len(word)==5 and all(0<=z<18 for z in word)
 blocks=tuple(sorted(map(int,btext.split())))
 assert blocks==actual_blocks(word),'Physical transcript lineage broken'
 cover=0
 for k,(_,source_mask) in enumerate(five):
  if all((source_mask&block).bit_count()<=1 for block in blocks):cover|=1<<k
 unique.setdefault(cover,word)
 lines+=1
assert lines==14938 and len(unique)==3344
print('P9_REAL_CUBE_14938_TRANSCRIPTS_3344_FIVE_SOURCE_COVER_TYPES_PASS',round(time.time()-start,2),flush=True)
rawmax=sorted(unique,key=lambda x:(-x.bit_count(),x))
maxima=[]
for cover in rawmax:
 if not any(cover&~stronger==0 for stronger in maxima):maxima.append(cover)
assert len(maxima)==2023
assert max(map(mass,maxima))==312
candidate=sorted((m for m in maxima if mass(m)>=232),key=lambda x:(-x.bit_count(),x))
assert len(candidate)==396 and len(set(candidate))==396
assert all(unique[m] for m in candidate)
print('P9_K5_DUAL_2023_SOURCE_NATIVE_MAXIMA_TO_396_ELIGIBLE_PASS',flush=True)
N=len(candidate)
# Necessary for <=5-cover: every pair's weighted union must be >=1480-3*312 =544.
adj=[0]*N; pairs=0
for i in range(N):
 for j in range(i+1,N):
  if mass(candidate[i]|candidate[j])>=544:
   adj[i]|=1<<j;adj[j]|=1<<i;pairs+=1
assert pairs==17112 and N*(N-1)//2-pairs==61098
print('P9_EXACT_DUAL_PAIR_CUT_61098_FORBIDDEN_17112_ALLOWED_PASS',flush=True)
support=[0]*480
for i,col in enumerate(candidate):
 x=col
 while x:
  lb=x&-x;k=lb.bit_length()-1
  support[k]|=1<<i;x-=lb
# Sound complete DPLL branching on a currently uncovered row. All partial
# columns must satisfy necessary k5 pair cuts and the original 480-row demand.
counts=collections.Counter()
def prove(selected_union, available, nremaining, level):
 counts['nodes_'+str(level)]+=1
 already=mass(selected_union)
 if already+nremaining*312<1480:
  counts['dual_prune_'+str(level)]+=1;return False
 missing=full & ~selected_union
 if missing==0:
  counts['SAT_found']+=1;return True
 if nremaining==0 or available.bit_count()<nremaining:
  counts['cardinality_prune_'+str(level)]+=1;return False
 pivot=None;options=None;min_count=N+1
 rr=missing
 while rr:
  lb=rr&-rr;j=lb.bit_length()-1;rr-=lb
  z=support[j]&available;n=z.bit_count()
  if n<min_count:
   pivot=j;options=z;min_count=n
   if n<=1:break
 if min_count==0:
  counts['uncovered_row_prune_'+str(level)]+=1;return False
 # Stronger valid upper estimate: top nremaining weighted new contributions.
 additions=[];q=available
 while q:
  lb=q&-q;i=lb.bit_length()-1;q-=lb
  additions.append(mass(candidate[i]&missing))
 additions.sort(reverse=True)
 if already+sum(additions[:nremaining])<1480:
  counts['optimistic_dual_prune_'+str(level)]+=1;return False
 while options:
  lb=options&-options;i=lb.bit_length()-1;options-=lb
  new_union=selected_union|candidate[i]
  if mass(new_union)+(nremaining-1)*312<1480:
   counts['incremental_dual_prune_'+str(level)]+=1;continue
  if prove(new_union, (available&adj[i])&~lb, nremaining-1,level+1):return True
 return False
assert not prove(0,(1<<396)-1,5,0),'A FIVE-WORD COVER EXISTS: DO NOT CLAIM UNSAT!'
# The standalone verifier's returned UNSAT is exact under its audited masks,
# integer-dual budget, physically generated candidates and dominance proof.
receipt={'schema':'cube-rev.019.P9.physical-five-source-k5-exact-finite-proof.v1',
 'state':'K5_UNSAT_LOCAL_COMPLETE_INTEGER_BRANCHING_PASS',
 'physical_source_sha256':source_sha,'source_sets_original':1192,
 'five_source_sets':480,'real_five_HTM_word_count':18**5,
 'physical_observation_partition_count':lines,'distinct_five_source_cover_types':3344,
 'five_source_maximal_cover_types':2023,'k5_dual_eligible_maximal_columns':396,
 'dual_weight_total':1480,'dual_capacity_per_word':312,
 'k5_each_selected_word_minimum_weight':232,'k5_each_selected_pair_minimum_weighted_union':544,
 'forbidden_pair_choices':61098,'allowed_pair_choices':17112,
 'complete_branch_counts':dict(counts),'seconds':round(time.time()-start,4),
 'conclusion':'Five real 5-HTM physical words cannot cover all 480 original admitted five-position source subsets.',
 'logical_scope':'A complete source-locked finite k5 five-only proof; no inference yet about k6 or k7 feasibility for the full 1192 source family.'}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print('CUBE_REV_019_L5_480_FIVE_SOURCE_K5_EXACT_FINITE_UNSAT_PASS',json.dumps({'nodes':{k:v for k,v in counts.items() if k.startswith('nodes_')},'seconds':receipt['seconds']}),flush=True)
#!/usr/bin/env python3
"""Actual physical P48 9E5C fully observed suffix, counterexample search with exact parity constraints.
No state cardinality / parity count is used as an equivalence key without a sound inverse query map.
"""
from itertools import permutations,product
from collections import defaultdict,Counter
from functools import lru_cache
from pathlib import Path
import json,random
# Physical orientation words matching P5.1, independent lattice reconstruction.
F={'U':(0,1,0),'D':(0,-1,0),'R':(1,0,0),'L':(-1,0,0),'F':(0,0,1),'B':(0,0,-1)}
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
S=tuple((p,F[f]) for p in product((-1,0,1),repeat=3) if sum(x!=0 for x in p) in (2,3) for f in 'URFDLB' if dot(p,F[f])==1)
idx={q:i for i,q in enumerate(S)};pieces={}
for p in sorted({x for x,n in S}):
 a=[idx[(p,n)] for n in F.values() if dot(p,n)==1]
 if len(a)==2:a.sort(key=lambda j:0 if abs(S[j][1][1]) else 1 if abs(S[j][1][2]) else 2)
 else:
  a.sort(key=lambda j:0 if abs(S[j][1][1]) else 1 if abs(S[j][1][0]) else 2)
  if det(*(S[j][1] for j in a))==-1:a[1],a[2]=a[2],a[1]
 pieces[p]=tuple(a)
E=tuple(p for p in sorted(pieces) if len(pieces[p])==2)
C=tuple(p for p in sorted(pieces) if len(pieces[p])==3)
face={i:next(f for f,n in F.items() if n==S[i][1]) for i in range(48)}
Ewords=tuple(''.join(face[z] for z in pieces[p]) for p in E)
Cwords=tuple(''.join(face[z] for z in pieces[p]) for p in C)
assert len(Ewords)==12 and len(Cwords)==8

def par(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def sector(words,nfix,r):
 ans=[[],[]];n=len(words)-nfix
 for perm in permutations(range(n)):
  for orient in product(range(r),repeat=n-1):
   angles=orient+((-sum(orient))%r,)
   s=''.join(words[:nfix])+''.join(words[nfix+perm[i]][(j+angles[i])%r] for i in range(n) for j in range(r))
   ans[par(perm)].append(s)
 return ans
edge=sector(Ewords,9,2);corner=sector(Cwords,5,3)
assert [len(z) for z in edge]==[12,12] and [len(z) for z in corner]==[27,27]
# Components each parity product; output 648 ordered state word pairs.
X=[(ew,cw,p) for p in range(2) for ew in edge[p] for cw in corner[p]]
assert len(X)==648 and len(set((e,c) for e,c,p in X))==648
FULL=(1<<648)-1
# Precalculate every local sticker/color outcome mask for literal 648 states.
colors='URFDLB'
slotmask={}
for sector in (0,1):
 for q in range(24):
  for col in colors:
   slotmask[sector,q,col]=sum(1<<i for i,s in enumerate(X) if s[sector][q]==col)

@lru_cache(None)
def paritycount(mask):
 return (mask&((1<<324)-1)).bit_count(),(mask>>324).bit_count()

@lru_cache(None)
def invariant(mask):
 hist=Counter()
 # Include all 576 spatial queries, retain partitions but forget location (permutation invariant).
 for eq,cq in product(range(24),repeat=2):
  p=tuple(sorted(((mask&slotmask[0,eq,a]&slotmask[1,cq,b]).bit_count() for a,b in product(colors,repeat=2)),reverse=True))
  hist[tuple(k for k in p if k)]+=1
 return tuple(sorted(hist.items()))

readable=tuple([(0,q) for q in range(18,24)]+[(1,q) for q in range(15,24)])
# A sampled pool of ACTUALLY reachable mixed observation histories, with differing true states.
rng=random.Random(20261109)
by_mask={FULL:()}
for target in range(648):
 samples=(list(range(1<<15)) if target==0 else [rng.getrandbits(15) for _ in range(160)])
 for bits in samples:
  mask=FULL;readings=[]
  for i,(sector,q) in enumerate(readable):
   if bits>>i&1:
    col=X[target][sector][q];mask &=slotmask[sector,q,col];readings.append((sector,q,col))
  assert mask>>target&1
  by_mask.setdefault(mask,tuple(readings))
print('reachable distinct masks',len(by_mask),flush=True)
# To guard against fake aliases, classify by posterior cardinality AND counts of parity in both sectors.
classes=defaultdict(list)
classes_full=defaultdict(list)
@lru_cache(None)
def full_sector_counts(readings):
 eR=[(q,c) for sec,q,c in readings if sec==0]
 cR=[(q,c) for sec,q,c in readings if sec==1]
 ep=[sum(all(ee[q]==c for q,c in eR) for ee in edge[p]) for p in range(2)]
 cp=[sum(all(cc[q]==c for q,c in cR) for cc in corner[p]) for p in range(2)]
 return (*ep,*cp)
for m in by_mask:
 n=m.bit_count()
 if 2<=n<=324:
  classes[(n,*paritycount(m))].append(m)
  classes_full[(n,*full_sector_counts(by_mask[m]))].append(m)

# First compare cheap distribution of number of distinct color outcomes across all 576 q.
@lru_cache(None)
def cheap(mask):
 hist=Counter()
 for eq,cq in product(range(24),repeat=2):
  count=sum(bool(mask&slotmask[0,eq,a]&slotmask[1,cq,b]) for a,b in product(colors,repeat=2))
  hist[count]+=1
 return tuple(sorted(hist.items()))

found=None
for key,ms in sorted(classes.items(),key=lambda kv:(-len(kv[1]),kv[0])):
 if len(ms)<2:continue
 a=ms[0];a_sig=cheap(a)
 for b in ms[1:]:
  if cheap(b)!=a_sig:
   found=(key,a,b);break
 if found:break
if not found:
 for key,ms in sorted(classes.items(),key=lambda kv:(-len(kv[1]),kv[0])):
  if len(ms)<2:continue
  a=ms[0];a_sig=invariant(a)
  for b in ms[1:]:
   if invariant(b)!=a_sig:found=(key,a,b);break
  if found:break


found_full=None
for key,ms in sorted(classes_full.items(),key=lambda kv:(-len(kv[1]),kv[0])):
 if len(ms)<2:continue
 a=ms[0];a_sig=cheap(a)
 for b in ms[1:]:
  if cheap(b)!=a_sig:found_full=(key,a,b);break
 if found_full:break
if not found_full:
 for key,ms in sorted(classes_full.items(),key=lambda kv:(-len(kv[1]),kv[0])):
  if len(ms)<2:continue
  a=ms[0];a_sig=invariant(a)
  for b in ms[1:]:
   if invariant(b)!=a_sig:found_full=(key,a,b);break
  if found_full:break

@lru_cache(None)
def optimal(mask):
 if mask.bit_count()<=1:return 0
 result=1000
 for eq,cq in product(range(24),repeat=2):
  children=[mask&slotmask[0,eq,a]&slotmask[1,cq,b] for a,b in product(colors,repeat=2)]
  children=[m for m in children if m]
  if len(children)>1:
   result=min(result,1+max(optimal(m) for m in children))
  if result==1:break
 return result

# No unrestricted depth-gap search: identical one-step partitions can differ without differing Bellman values.
depth_difference=None

def entry(mask):
 return {'count':mask.bit_count(),'parity_joint_counts':paritycount(mask),'readings':by_mask[mask],'optimal_remaining_depth':optimal(mask) if mask.bit_count()<=8 else None,'sector_parity_counts':full_sector_counts(by_mask[mask]),'branch_count_histogram':cheap(mask),'full_partition_histogram':[[list(k),v] for k,v in invariant(mask)],'mask_hex':hex(mask)}
receipt={'result':'R14_P83_648_MIXED_HISTORY_INVARIANT_COURT_PASS',
 'physical_basis':'9 completely observed edges and 5 completely observed corners, full 648 valid parity-matched states; independent P5.1 lattice-derived sticker ordering',
 'complete_state_count':648,'candidate_partial_facelets':15,'exhaustive_target0_patterns':32768,'other_targets':647,'other_target_samples_each':160,
 'realizable_distinct_posterior_masks':len(by_mask),'same_population_and_joint_parity_classes':len(classes),'same_full_four_sector_counts_classes':len(classes_full),'counterexample_found':bool(found),'four_sector_counterexample_found':bool(found_full),'same_four_sector_counts_different_exact_depth_found_up_to_8_candidates':bool(depth_difference),'exact_depth_difference':({'matching_four_parity_counts':depth_difference[0],'A':entry(depth_difference[1]),'B':entry(depth_difference[2])} if depth_difference else None),'four_sector_counterexample':({'matching_four_parity_counts':found_full[0],'A':entry(found_full[1]),'B':entry(found_full[2]),'unequal_576_query_partition_multisets':invariant(found_full[1])!=invariant(found_full[2])} if found_full else None),
 'counterexample':({'matching_scalar_and_parity':found[0], 'A':entry(found[1]), 'B':entry(found[2]),'unequal_all_576_query_partition_multisets':invariant(found[1])!=invariant(found[2])} if found else None),
 'limitations':'Both histories physical and reachable from the fully observed 9E5C suffix. Class key parity joint counts is not guaranteed to match all four sector completion counts; full 576 partition invariant difference refutes any observation-action permutation equivalence, not necessarily distinct Bellman depth. No full 20-frame result.'}
p=Path(__file__).with_name('R14_P83_648_MIXED_HISTORY_INVARIANT_RECEIPT.json');p.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='counterexample'},indent=2),flush=True)
if depth_difference:print('DEPTH_DIFFERENCE',depth_difference[0],by_mask[depth_difference[1]],by_mask[depth_difference[2]],flush=True)
if found_full:print('FOUR_SECTOR_COUNTEREXAMPLE',found_full[0],by_mask[found_full[1]],by_mask[found_full[2]],optimal(found_full[1]),optimal(found_full[2]),flush=True)
if found: print('COUNTEREXAMPLE',found[0],by_mask[found[1]],by_mask[found[2]],'distinct',len(invariant(found[1])),len(invariant(found[2])),flush=True)

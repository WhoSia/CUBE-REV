from pathlib import Path
import argparse, hashlib
from itertools import product,combinations
import json,time,collections
args=argparse.ArgumentParser()
for name in ('physical','partitions','output'): args.add_argument('--'+name,required=True)
a=args.parse_args()
start=time.monotonic();physical=Path(a.physical).read_bytes();sha=hashlib.sha256(physical).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
src=json.loads(physical)['bases'];assert len(src)==1192;full=(1<<1192)-1
# Physical original source-cover masks keyed directly to a real length-5 word.
byrank={5:{},6:{},7:{}};partition_count=0
for line in Path(a.partitions).read_text().splitlines():
 w,raw=line.split('|');b=list(map(int,raw.split()));rank=len(b);partition_count+=1
 if rank not in byrank:continue
 c=sum(1<<i for i,A in enumerate(src) if all((A&part).bit_count()<=1 for part in b))
 byrank[rank].setdefault(c,tuple(map(int,w.split())))
assert partition_count==14938
low=sorted(set(byrank[5])|set(byrank[6]));hi=sorted(byrank[7]);assert len(hi)==32 and len(low)==3439
# Construct and verify entire 16-element source-incidence group incl improper maps.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
idx={v:i for i,v in enumerate(coords)};bindex={v:i for i,v in enumerate(src)};groups=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in product((-1,1),repeat=3):
  perm=[idx[tuple(signs[k]*pt[axes[k]] for k in range(3))]for pt in coords]
  rowperm=[bindex[sum(1<<perm[i] for i in range(12) if b>>i&1)]for b in src]
  groups.append(rowperm)
assert len(groups)==16
hi_index={v:i for i,v in enumerate(hi)};low_set=set(low);high_maps=[]
for g in groups:
 # Full ORIGINAL source incidence closure for every *rank constrained* candidate.
 def transform(m):
  out=0
  while m:
   bit=m&-m;out|=1<<g[bit.bit_length()-1];m-=bit
  return out
 assert all(transform(m) in low_set for m in low), 'LOW_RANK_PHYSICAL_INCIDENCE_NOT_CLOSED'
 assert all(transform(m) in hi_index for m in hi), 'HIGH_RANK_PHYSICAL_INCIDENCE_NOT_CLOSED'
 high_maps.append([hi_index[transform(m)]for m in hi])
print('P13_FIVE_RANK7_PHYSICAL_SOURCE_16_INCIDENCE_AUTOMORPHISMS_ALL_RAW_RANKS_PASS',round(time.monotonic()-start,1),flush=True)
# Full original seven-word cover with exactly FOUR rank7 words and THREE rank5/6 words.
visited=set();reps=[];hist=collections.Counter()
for rep in combinations(range(32),4):
 if rep in visited:continue
 orbit={tuple(sorted(g[i]for i in rep)) for g in high_maps}
 assert rep in orbit and visited.isdisjoint(orbit)
 visited.update(orbit);reps.append(rep);hist[len(orbit)]+=1
assert sum(size*count for size,count in hist.items())==35960
print('P13_FOUR_RANK7_ORBITS',len(reps),dict(hist),'seconds',round(time.monotonic()-start,1),flush=True)
support=[0]*1192
for j,m in enumerate(low):
 while m:
  lb=m&-m;support[lb.bit_length()-1]|=1<<j;m-=lb
universe=(1<<len(low))-1

def rarest_options(m):
 best_count=len(low)+1;best=0
 while m:
  bit=m&-m;row=bit.bit_length()-1;sz=support[row].bit_count()
  if sz<best_count:best_count=sz;best=support[row]
  m-=bit
 return best

def two_cover(m):
 if m==0:return (0,1)
 # Every actual second word covering some missing rare row is examined.
 first=rarest_options(m)
 while first:
  lb=first&-first;j=lb.bit_length()-1;first-=lb
  rest=m&~low[j]
  if rest==0:return j,0 if j!=0 else 1
  possibles=universe
  while rest and possibles:
   bit=rest&-rest;possibles&=support[bit.bit_length()-1];rest-=bit
  if possibles:
   # Duplicate words are permitted by the test: no hidden minimality assumption.
   return j,(possibles&-possibles).bit_length()-1
 return None

attempts=0;found=None
for count,selected in enumerate(reps):
 union=0
 for i in selected:union|=hi[i]
 missing=full&~union
 first=rarest_options(missing)
 while first:
  lb=first&-first;i=lb.bit_length()-1;first-=lb;attempts+=1
  rest=missing&~low[i]
  if not rest:
   j=0 if i!=0 else 1;k=1 if j!=1 and i!=1 else 2
   found=(selected,i,j,k);break
  other=two_cover(rest)
  if other is not None:
   found=(selected,i,*other);break
 if found:break
 if count%500==0:print('P13_FOUR_R7_PROGRESS',count,'orbits',len(reps),'trials',attempts,'elapsed',round(time.monotonic()-start,1),flush=True)
if found:
 selected,i,j,k=found
 allcover=0
 for n in selected:allcover|=hi[n]
 allcover|=low[i]|low[j]|low[k];assert allcover==full
 word=[byrank[7][hi[n]] for n in selected]+[byrank[5].get(low[t],byrank[6].get(low[t])) for t in (i,j,k)]
 print('P13_PHYSICAL_FULL_ORIGINAL_K7_SAT_FOUR_RANK7',word,flush=True)
result={'schema':'cube-rev.019.P13.four-rank7-three-rank5or6-complete-orbit-census',
 'source_sha256':sha,'physical_original_partitions':partition_count,'physical_raw_rank5_mask_count':len(byrank[5]),'rank6_mask_count':len(byrank[6]),'rank7_mask_count':len(hi),
 'original_rank7_four_combinations':35960,'rank7_four_orbit_representatives':len(reps),
 'orbit_size_histogram':dict(hist),'orbits_checked':len(reps) if not found else count+1,
 'attempted_first_low_words':attempts,'result':'PHYSICAL_SEVEN_FULL_SAT' if found else 'NO_FULL_SEVEN_WITH_EXACTLY_FOUR_RANK7',
 'found_words':[list(w) for w in word] if found else None,'seconds':time.monotonic()-start}
Path(a.output).write_text(json.dumps(result,indent=2))
print('P13_FOUR_R7_THREE_LOWER_CENSUS',json.dumps(result),flush=True)
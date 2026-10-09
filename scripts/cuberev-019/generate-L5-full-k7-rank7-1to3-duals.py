#!/usr/bin/env python3
"""Explore source-locked real physical residual LP for t=1,2,3 selected rank7 words.
HiGHS floats are ONLY suggestions; each emitted integer dual is separately
checked by exact integer arithmetic over ALL raw physical rank5/6 words.
"""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
from scipy.optimize import linprog
from scipy.sparse import csc_matrix
import numpy as np,json,hashlib,time,argparse
argparser=argparse.ArgumentParser()
for key in ('physical','partitions','prepared','output'):argparser.add_argument('--'+key,required=True)
a=argparser.parse_args()
start=time.monotonic();raw=Path(a.physical).read_bytes();src=json.loads(raw)['bases'];sha=hashlib.sha256(raw).hexdigest();assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
core=json.loads(Path(a.prepared).read_text())['source_core_row_indices'];assert len(core)==544
byrank={5:{},6:{},7:{}}
for line in Path(a.partitions).read_text().splitlines():
 w,parts=line.split('|');b=list(map(int,parts.split()));rank=len(b)
 if rank not in byrank:continue
 mask=sum(1<<j for j,x in enumerate(src) if all((x&t).bit_count()<=1 for t in b))
 byrank[rank].setdefault(mask,tuple(map(int,w.split())))
low=sorted(set(byrank[5])|set(byrank[6]));hi=sorted(byrank[7]);assert len(low)==3439 and len(hi)==32
corepos={src_idx:j for j,src_idx in enumerate(core)};row=[];col=[]
for j,mask in enumerate(low):
 for i,orig in enumerate(core):
  if mask>>orig&1:row.append(i);col.append(j)
A=csc_matrix((np.ones(len(row),dtype=np.int64),(row,col)),shape=(544,len(low)))
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
ci={v:i for i,v in enumerate(coords)};si={v:i for i,v in enumerate(src)};hi_index={v:i for i,v in enumerate(hi)};ls=set(low);maps=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in product((-1,1),repeat=3):
  perm=[ci[tuple(signs[j]*a[axes[j]] for j in range(3))] for a in coords]
  g=[si[sum(1<<perm[i] for i in range(12) if b>>i&1)]for b in src]
  def trans(m):
   z=0
   while m:
    bit=m&-m;z|=1<<g[bit.bit_length()-1];m-=bit
   return z
  assert all(trans(x) in ls for x in low)
  assert all(trans(x) in hi_index for x in hi)
  maps.append([hi_index[trans(x)]for x in hi])
assert len(maps)==16
certs=[];orbit_hist={};worst=[]
for t in (1,2,3):
 visited=set();reps=[];hist=Counter()
 for item in combinations(range(32),t):
  if item in visited:continue
  orb={tuple(sorted(g[i]for i in item))for g in maps}
  assert item in orb and visited.isdisjoint(orb)
  visited.update(orb);reps.append(item);hist[len(orb)]+=1
 assert len(visited)=={1:32,2:496,3:4960}[t]
 orbit_hist[t]={'representatives':len(reps),'histogram':dict(hist)}
 print('P13_RANK7_ORBITS',t,len(reps),dict(hist),flush=True)
 t_min=1e99
 for k,indices in enumerate(reps):
  high=0
  for i in indices:high|=hi[i]
  remain=[j for j,orig in enumerate(core) if not (high>>orig)&1]
  lp=linprog(np.ones(len(low)),A_ub=-A[remain],b_ub=-np.ones(len(remain)),bounds=(0,None),method='highs',options={'time_limit':5})
  assert lp.success,('LP_FAILED',t,indices,lp.message)
  t_min=min(t_min,lp.fun)
  if lp.fun<=7-t+1e-7:
   print('P13_POTENTIAL_LP_BARRIER_FAIL',t,indices,lp.fun,flush=True)
   worst.append({'t':t,'indices':indices,'LP':lp.fun});continue
  y=-lp.ineqlin.marginals
  nums=[max(0,round(float(v)*1000000)) for v in y]
  weights=np.zeros(544,dtype=np.int64)
  for j,wt in zip(remain,nums):weights[j]=wt
  total=int(weights.sum());B=int((A.T@weights).max())
  if total<=(7-t)*B:
   print('P13_ROUNDING_FAILED',t,indices,lp.fun,total,B,flush=True)
   worst.append({'t':t,'indices':indices,'LP':lp.fun,'W':total,'B':B});continue
  certs.append({'rank7_count':t,'rank7_physical_32mask_indices':list(indices),'rank7_original_source_coverage_masks_hex':[hex(hi[i]) for i in indices],'positive_original_1192_row_weights':[[int(core[j]),int(w)] for j,w in enumerate(weights) if w],
  'total':total,'max_one_raw_physical_rank5or6_word_weight':B,'exact_integer_gap':total-(7-t)*B})
  if (k+1)%50==0:print('P13_R7_COND_DUAL_PROGRESS',t,k+1,'of',len(reps),'elapsed',round(time.monotonic()-start,1),flush=True)
 print('P13_RANK7_MIN_RESIDUAL_FRACTIONAL_LOWER',t,t_min,'budget',7-t,'elapsed',round(time.monotonic()-start,1),flush=True)
result={'schema':'cube-rev.019.P13.original-full-R-k7-conditional-rank7-one-two-three-integer-dual-court-v2-physical-mask-keyed',
 'physical_source_sha256':sha,'raw_rank5_full_source_types':len(byrank[5]),'raw_rank6_full_source_types':len(byrank[6]),'raw_rank7_full_source_types':32,
 'group_size':16,'orbit_profile':orbit_hist,'expected_integer_certificates':sum(orbit_hist[t]['representatives'] for t in (1,2,3)),
 'certificates':certs,'uncertified_cases':worst,'status':'EXACT_INTEGER_CANDIDATES_CHECKED_ALL' if not worst else 'SOME_UNCERTIFIED_CASES'}
file=Path(a.output);file.write_text(json.dumps(result,separators=(',',':'))+'\n');print('P13_RANK7_ONE_TWO_THREE_COMPLETE',len(certs),'uncertified',len(worst),'seconds',time.monotonic()-start,flush=True)
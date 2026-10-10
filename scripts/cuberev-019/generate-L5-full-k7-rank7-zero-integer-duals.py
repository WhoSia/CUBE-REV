#!/usr/bin/env python3
"""P13 original-1192 physical case t=0: source-locked conditional LP to int dual.
Numerical LP generates candidates; integer verifier only certifies cases W>6*C.
Rank6 first-word representatives use within-rank6 dominance, not all-rank.
"""
import json,hashlib,time,os
from pathlib import Path
from itertools import product
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import numpy as np
p=Path(os.environ.get('P13_DATA_ROOT',Path(__file__).parent))
raw=(p/'original_physical.json').read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
source=json.loads(raw)['bases'];N=len(source)
byrank={5:set(),6:set()};npartition=0
for line in (p/'original_L5_partitions.tsv').read_text().splitlines():
 w,rest=line.split('|');parts=list(map(int,rest.split()));r=len(parts);npartition+=1
 if r not in byrank:continue
 cover=sum(1<<i for i,b in enumerate(source) if all((b&part).bit_count()<=1 for part in parts))
 byrank[r].add(cover)
assert npartition==14938 and [len(byrank[k]) for k in (5,6)]==[2295,1144]
low=byrank[5]|byrank[6]
assert len(low)==3439
def maxima(items):
 keep=[]
 for c in sorted(items,key=int.bit_count,reverse=True):
  if not any(c&~k==0 for k in keep):keep.append(c)
 return keep
low_max=maxima(low);rank6_max=maxima(byrank[6]);print('WITHIN FULL R6 MAX',len(rank6_max),flush=True)
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
ci={v:i for i,v in enumerate(coords)};si={v:i for i,v in enumerate(source)};groups=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in product((-1,1),repeat=3):
  perm=[ci[tuple(signs[k]*pos[axes[k]] for k in range(3))]for pos in coords]
  g=[si[sum(1<<perm[j] for j in range(12) if s>>j&1)]for s in source]
  groups.append(g)
def transform(mask,g):
 result=0
 while mask:
  bit=mask&-mask;result|=1<<g[bit.bit_length()-1];mask-=bit
 return result
assert len(groups)==16
for g in groups:
 assert {transform(v,g) for v in byrank[5]}==byrank[5]
 assert {transform(v,g) for v in byrank[6]}==byrank[6]
 assert {transform(v,g) for v in rank6_max}==set(rank6_max)
seen=set();reps=[]
for m in sorted(rank6_max):
 if m in seen:continue
 orb={transform(m,g) for g in groups}
 assert orb<=set(rank6_max) and not (orb&seen)
 seen|=orb;reps.append(m)
print('TRUE ORBITS',len(reps),flush=True)
print('P13_T0_BASE_RESTORED_2295_RANK5_1144_RANK6_74_FIRST_RANK6_ORBITS_PASS',flush=True)
# LP residual optimization with all low physical word types (nondominated within same low family).
ri=[];cj=[]
for j,col in enumerate(low_max):
 while col:
  bit=col&-col;ri.append(bit.bit_length()-1);cj.append(j);col-=bit
matrix=csr_matrix((np.ones(len(ri)),(ri,cj)),shape=(N,len(low_max)))
start=time.monotonic();certs=[];open_branches=[];counts=[]
begin=int(os.environ.get("P13_BEGIN", "0"));end=int(os.environ.get("P13_END",str(len(reps))))
for q,first in enumerate(reps):
 if not begin<=q<end:continue
 missing=np.fromiter((not (first>>i&1) for i in range(N)),count=N,dtype=bool)
 rows=np.flatnonzero(missing)
 problem=linprog(np.ones(len(low_max)), A_ub=-matrix[rows], b_ub=-np.ones(len(rows)),bounds=(0,None),method='highs',options={'time_limit':8})
 assert problem.status==0,(q,problem.status,problem.message)
 positive=np.maximum(0,-problem.ineqlin.marginals)
 # NOTE: only integer arithmetic after candidate proposal. Floor safe, no tolerance assumption.
 D=10**7
 weights={int(rows[k]):int(np.floor(y*D)) for k,y in enumerate(positive) if int(np.floor(y*D))>0}
 W=sum(weights.values())
 C=max(sum(w for r,w in weights.items() if col>>r&1) for col in low)
 rec={'representative_mask_hex':hex(first),'first_rank':6,'residual_lp_numerical':float(problem.fun),'W':W,'B':C,'weights_original_row':{str(k):v for k,v in weights.items()}}
 if W>6*C:certs.append(rec)
 else:open_branches.append({'representative_mask_hex':hex(first),'index':q,'lp':float(problem.fun),'integer_ratio':W/C if C else None})
 counts.append({'idx':q,'num':float(problem.fun),'weight_ratio':W/C,'certified':W>6*C})
 if q%10==0:print('FIRST_RANK6_ORBIT',q,'NUM_LP',round(problem.fun,7),'EXACT_CERT',W>6*C,'time',round(time.monotonic()-start,1),flush=True)
result={'schema':'cube-rev.019.P13.t0-rank7-zero-frozen-original-source-residual-integer-dual.v1','physical_sha256':sha,'original_sources':1192,'real_physical_partitions':14938,'raw_rank5_cover_types':2295,'raw_rank6_cover_types':1144,'low_original_cover_types':len(low),'rank6_within_class_maximals':len(rank6_max),'rank6_first_word_orbits':len(reps),'processed_orbit_indices':list(range(begin,end)),'exact_integer_certificates':certs,'open_cases':open_branches,'method':'Each certified first-rank6 physical word masks covered source rows; integer nonnegative residual weights W strictly exceed 6 times maximum low-physical-word weight B. All 3439 original rank5+rank6 cover types checked. All first word orbits include 16 explicitly checked original source incidence relabelings. Conditional LP only proposes certificates.'}
(p/f'P13_t0_conditional_integer_duals_{begin}_{end}.json').write_text(json.dumps(result,indent=2)+'\n')
(p/f'P13_t0_LP_diagnostics_{begin}_{end}.json').write_text(json.dumps(counts,indent=2)+'\n')
print('P13_T0_FINAL',len(certs),'certified of 70, open',len(open_branches),'time',time.monotonic()-start,flush=True)
print('OPEN',json.dumps(open_branches),flush=True)
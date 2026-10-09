#!/usr/bin/env python3
"""Generate candidate integer dual weights with SciPy LP; do NOT trust solver status as theorem.
Proof is established only by separate standard-library P12 physical original-source validator.
"""
"""Generate rational-candidate -> integer-verified P12 duals for six-word rank5/6 family.
Never use HiGHS 'infeasible' as proof. Output source-indexed positive integer weights
and check all 2023 physical maximal masks (full rank-specific cover capacities).
"""
import json,itertools,collections,time,hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_array,csr_array,hstack,vstack
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--physical',required=True)
ap.add_argument('--partitions',required=True)
ap.add_argument('--output',required=True)
args=ap.parse_args()
root=Path(args.partitions).parent;out=Path(args.output);out.mkdir(parents=True,exist_ok=True);raw=Path(args.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest();five=[r for r in json.loads(raw)['bases'] if r.bit_count()==5]; assert len(five)==480
bycover={}
for line in Path(args.partitions).read_text().splitlines():
 _,bl=line.split('|');blocks=tuple(map(int,bl.split()));m=sum(1<<j for j,A in enumerate(five) if all((A&b).bit_count()<=1 for b in blocks));bycover.setdefault(m,blocks)
assert len(bycover)==3344
keep=[]
for m in sorted(bycover,key=lambda x:(-x.bit_count(),x)):
 if not any(m&~x==0 for x in keep):keep.append(m)
assert len(keep)==2023
rank={m:len(bycover[m]) for m in keep};r5=[m for m in keep if rank[m]==5];r6=[m for m in keep if rank[m]==6];r7=[m for m in keep if rank[m]==7]
assert (len(r5),len(r6),len(r7))==(975,1016,32)
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)];pos={v:i for i,v in enumerate(coords)};find={v:i for i,v in enumerate(five)}
perms=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in itertools.product((-1,1),repeat=3):
  p=[pos[tuple(signs[j]*a[axes[j]] for j in range(3))] for a in coords];perms.append([find[sum(1<<p[j] for j in range(12) if A>>j&1)] for A in five])
def transform(mask,pm):
 r=0
 while mask:
  t=mask&-mask;r|=1<<pm[t.bit_length()-1];mask-=t
 return r
reps={5:[],6:[],7:[]};unseen=set(keep)
while unseen:
 a=min(unseen);o={transform(a,p) for p in perms};assert o<=unseen and a in o and all(rank[v]==rank[a] for v in o);unseen-=o;reps[rank[a]].append(a)
assert list(map(len,(reps[5],reps[6],reps[7])))==[68,66,3]
# Index rows into 0..479 (each row original five-source index)
def row_index(m):
 while m:
  t=m&-m;yield t.bit_length()-1;m-=t

def csr_columns(cols):
 rr=[];cc=[]
 for j,m in enumerate(cols):
  for i in row_index(m):rr.append(i);cc.append(j)
 A=coo_array((np.ones(len(rr)),(np.array(rr,dtype=np.int32),np.array(cc,dtype=np.int32))),shape=(480,len(cols))).tocsr();A.indices=A.indices.astype(np.int32);A.indptr=A.indptr.astype(np.int32)
 return A
Ar6=csr_columns(r6); Ar5=csr_columns(r5)
Adual=vstack([Ar5.T,Ar6.T],format='csr')
coeff=coo_array((-np.ones(len(r5)+len(r6)),(np.arange(len(r5)+len(r6),dtype=np.int32),np.r_[np.zeros(len(r5),dtype=np.int32),np.ones(len(r6),dtype=np.int32)])),shape=(len(r5)+len(r6),2)).tocsr()
B=hstack([Adual,coeff],format='csr');B.indices=B.indices.astype(np.int32);B.indptr=B.indptr.astype(np.int32)
row=csr_array(np.r_[np.zeros(480),[1.,5.]].reshape(1,-1))
D=vstack([B,row],format='csr');D.indices=D.indices.astype(np.int32);D.indptr=D.indptr.astype(np.int32)

rs=linprog(np.r_[-np.ones(480),[0.,0.]],A_ub=D,b_ub=np.r_[np.zeros(len(r5)+len(r6)),1],bounds=[(0,None)]*482,method='highs')
assert rs.status==0 and -rs.fun>1.01
weights=np.maximum(0,np.rint(rs.x[:480]*10**8)).astype(np.int64)
W=int(weights.sum());c5=int((Ar5.T.astype(np.int64)@weights).max());c6=int((Ar6.T.astype(np.int64)@weights).max())
assert c6>=c5 and W>c5+5*c6
cert=[{'type':'nonseventh_at_least_one_rank5','source_row_weight':[[int(i),int(w)] for i,w in enumerate(weights) if w>0], 'total':W,'capacity_rank5':c5,'capacity_rank6':c6,'strict_gap':W-c5-5*c6,'candidate_rank5':len(r5),'candidate_rank6':len(r6), 'implication':'No 6-word R5 dictionary using only rank5/6 with at least one rank5 word.'}]
print('P12_NO_RANK7_WITH_LOW_CERT_PASS',{'total':W,'C5':c5,'C6':c6,'gap':W-c5-5*c6,'support':int(np.count_nonzero(weights))},flush=True)
# R6 first-word fix, remaining 5 R6; also R7 one-word fix with rest R6
for category in (6,7):
 for v in reps[category]:
  uncovered=[i for i in range(480) if not (v>>i)&1]
  res=linprog(np.ones(1016),A_ub=-Ar6[uncovered,:],b_ub=-np.ones(len(uncovered)),bounds=(0,None),method='highs')
  assert res.status==0 and res.fun>5.1,(category,res.status,res.fun)
  dual=np.maximum(0,np.rint((-res.ineqlin.marginals)*10**7)).astype(np.int64)
  allweights=np.zeros(480,dtype=np.int64);allweights[uncovered]=dual
  tot=int(allweights.sum());cap=int((Ar6.T.astype(np.int64)@allweights).max())
  assert tot>5*cap and cap>0
  cert.append({'type':'first_rank6_rest_rank6' if category==6 else 'first_rank7_rest_rank6',
    'selected_first_word_original480_cover_hex':hex(v),
    'selected_first_word_output_rank':category,
    'source_row_weight':[[int(i),int(w)] for i,w in enumerate(allweights) if w>0],
    'total':tot,'capacity_rank6':cap,'strict_gap':tot-5*cap,
    'implication':'After this first physical word, five other rank6-only experiments cannot cover all 480 sources.'})
 print('P12_CONDITIONAL_CLASS',category,'count',len(reps[category]),flush=True)
assert len(cert)==70
outp={'schema':'cube-rev.019.P12.physical-R5-sixword-no-rank7-integer-duals.v1',
 'original_source_sha256':sha,'real_L5_partitions':14938,'distinct_R5_cover_masks':3344,
 'rank5_columns':975,'rank6_columns':1016,'rank7_columns':32,
 'signed_incidence_group_order':16,'first_rank6_orbits':66,'first_rank7_orbits':3,
 'certificates':cert,'conclusion':'Any physically realizable six-word cover of R5 must contain at least one rank7 word. Further, if all six have rank>=6, at least two must have rank7.'}
outfile=out/'P12_rank_sensitive_integer_duals.json';outfile.write_text(json.dumps(outp,indent=1)+'\n');print('P12_ALL_70_INTEGER_COURTS_PASS',len(cert),outfile.stat().st_size,'SHA',hashlib.sha256(outfile.read_bytes()).hexdigest(),flush=True)

raw6=set()
for ln in Path(args.partitions).read_text().splitlines():
 _,txt=ln.split('|');bb=tuple(map(int,txt.split()))
 if len(bb)==6:raw6.add(sum(1<<i for i,A in enumerate(five) if all((A&v).bit_count()<=1 for v in bb)))
assert len(raw6)==1144
max6=[]
for v in sorted(raw6,key=lambda x:(-x.bit_count(),x)):
 if not any(v&~s==0 for s in max6):max6.append(v)
assert len(max6)==1080
rem=set(max6);reps6=[]
while rem:
 v=min(rem);orb={transform(v,p) for p in perms};assert v in orb and orb<=rem;rem-=orb;reps6.append(v)
assert len(reps6)==70
A=csr_columns(sorted(raw6))
rs=[]
for j,v in enumerate(reps6):
 miss=[i for i in range(480) if not (v>>i)&1]
 res=linprog(np.ones(A.shape[1]),A_ub=-A[miss,:],b_ub=-np.ones(len(miss)),bounds=(0,None),method='highs')
 rs.append((v, res.fun if res.fun is not None else -1))
print('raw rank6 70 orbit conditional LP min',min(v for _,v in rs),'max',max(v for _,v in rs),'all>5',all(v>5+1e-6 for _,v in rs))
# Convert all 70 residual LP results into independently checkable integer duals
import hashlib
certs=[]
raw6list=sorted(raw6)
for j,(v,rawobj) in enumerate(rs):
 miss=[i for i in range(480) if not v>>i&1]
 res=linprog(np.ones(len(raw6list)),A_ub=-A[miss,:],b_ub=-np.ones(len(miss)),bounds=(0,None),method='highs')
 w=np.zeros(480,dtype=np.int64);w[miss]=np.maximum(0,np.rint(-res.ineqlin.marginals*10**7)).astype(np.int64)
 W=int(w.sum());C=int((A.T.astype(np.int64)@w).max()); assert W>5*C,(j,W,C)
 certs.append({'fixed_raw_rank6_orbit_representative_mask_hex':hex(v),'positive_480_source_row_integer_weights':[[int(i),int(x)] for i,x in enumerate(w) if x],
 'total_weight':W,'raw_rank6_max_capacity':C,'strict_gap':W-5*C})
output={'schema':'cube-rev.019.P12.original-raw-rank6-only-six-word-conditional-integer-duals.v1',
 'physical_source_sha256':sha,'original_rank6_physical_cover_types':1144,
 'rank6_only_maximal_cover_types':1080,'rank6_only_first_word_orbits':70,'group_order':16,
 'certificates':certs,
 'meaning':'After any rank6-only first word relabeled by a verified automorphism to a representative, the other five raw rank6 physical words cannot cover the remaining original 480 five-state requirements.'}
p=out/'P12_raw_rank6_70_integer_duals.json';p.write_text(json.dumps(output,separators=(',',':'))+'\n')
print('P12_SEVENTY_ORIGINAL_PHYSICAL_RANK6_ONLY_INTEGER_DUALS_PASS',hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size,flush=True)

from itertools import combinations
from scipy.sparse import hstack
out=Path('/mnt/data/cuberev019_p11')
rawr={5:set(),6:set()}
for ln in Path(args.partitions).read_text().splitlines():
 _,txt=ln.split('|');blocks=tuple(map(int,txt.split()))
 if len(blocks) in rawr:
  cm=sum(1<<i for i,A in enumerate(five) if all((A&b).bit_count()<=1 for b in blocks))
  rawr[len(blocks)].add(cm)
raw_columns=sorted(rawr[5]|rawr[6]);assert len(rawr[5])==2168 and len(rawr[6])==1144
Aa=csr_columns(raw_columns)
cert=[]
for qty in (2,3):
 family={tuple(sorted(t)) for t in combinations(r7,qty)}
 orbits=[];unseen=set(family)
 while unseen:
  first=min(unseen);orb={tuple(sorted(transform(v,p) for v in first)) for p in perms};assert first in orb and orb<=unseen
  unseen-=orb;orbits.append((first,len(orb)))
 assert (qty,len(orbits)) in ((2,44),(3,327))
 print('P12_ENUMERATED_RANK7_SYMMETRY_ORBITS',qty,len(orbits),flush=True)
 for q,(selection,orbitsize) in enumerate(orbits):
  first_union=0
  for m in selection:first_union|=m
  missing=[i for i in range(480) if not first_union>>i&1]
  res=linprog(np.ones(len(raw_columns)),A_ub=-Aa[missing,:],b_ub=-np.ones(len(missing)),bounds=(0,None),method='highs')
  assert res.status==0 and res.fun>(6-qty)+0.5,(qty,q,res.status,res.fun)
  wv=np.zeros(480,dtype=np.int64)
  wv[missing]=np.maximum(0,np.rint((-res.ineqlin.marginals)*10**7)).astype(np.int64)
  W=int(wv.sum());Cc=int((Aa.T.astype(np.int64)@wv).max());gap=W-(6-qty)*Cc
  assert gap>0,(qty,q,gap)
  cert.append({'selected_rank7_coverage_masks_hex':[hex(int(m)) for m in selection],
   'orbit_size':orbitsize,'remaining_rank5_6_word_budget':6-qty,
   'positive_original_480_source_weights':[[int(i),int(w)] for i,w in enumerate(wv) if w>0],
   'total_weight':W,'maximum_one_raw_rank5_6_word_weight':Cc,'exact_integer_gap':gap})
  if q%70==0:print('progress conditional rank7',qty,q,'of',len(orbits),'gap',gap,flush=True)
print('P12_FINISHED_RANK7_CONDITIONAL_INTEGER_CERTIFICATES',len(cert),flush=True)
assert len(cert)==371
pack={'schema':'cube-rev.019.P12.R5-rank7-conditioned-exact-integer-duals.v1',
 'original_source_sha256':sha,'original_real_five_move_partitions':14938,
 'original_R5_rank5_coverage_types':len(rawr[5]),'original_R5_rank6_coverage_types':len(rawr[6]),
 'rank7_physically_possible_masks':len(r7),'rank7_pair_orbits':44,'rank7_triple_orbits':327,
 'certificate_rule':'For each rank7 subset T, assign nonnegative integer weights to source rows not already covered by T; if their total exceeds (6-|T|) times maximal single candidate rank5/6 weight, completion is impossible.',
 'certificates':cert}
p=out/'P12_rank7_pair_triple_integer_duals.json';p.write_text(json.dumps(pack,separators=(',',':'))+'\n');print('SHA',hashlib.sha256(p.read_bytes()).hexdigest(),'BYTES',p.stat().st_size,flush=True)
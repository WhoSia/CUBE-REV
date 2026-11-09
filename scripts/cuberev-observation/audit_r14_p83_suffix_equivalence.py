#!/usr/bin/env python3
"""Exact physical 10E6C suffix falsification court. Never equate partition invariants with Bellman values."""
from itertools import product
from collections import defaultdict, Counter
from functools import lru_cache
from pathlib import Path
import json, hashlib
F={'U':(0,1,0),'D':(0,-1,0),'R':(1,0,0),'L':(-1,0,0),'F':(0,0,1),'B':(0,0,-1)}
order='URFDLB'
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
slots=tuple((p,F[f]) for p in product((-1,0,1),repeat=3) if sum(x!=0 for x in p) in (2,3) for f in order if dot(p,F[f])==1)
index={q:i for i,q in enumerate(slots)}
pieces={}
for p in sorted({x for x,n in slots}):
 ids=[index[(p,n)] for n in F.values() if dot(p,n)==1]
 if len(ids)==2:ids.sort(key=lambda i:0 if abs(slots[i][1][1]) else 1 if abs(slots[i][1][2]) else 2)
 else:
  ids.sort(key=lambda i:0 if abs(slots[i][1][1]) else 1 if abs(slots[i][1][0]) else 2)
  if det(*(slots[i][1] for i in ids))==-1:ids[1],ids[2]=ids[2],ids[1]
 pieces[p]=tuple(ids)
E=tuple(p for p in sorted(pieces) if len(pieces[p])==2)
C=tuple(p for p in sorted(pieces) if len(pieces[p])==3)
face={i:next(f for f,n in F.items() if n==slots[i][1]) for i in range(48)}
e=tuple(''.join(face[j] for j in pieces[p]) for p in E)
c=tuple(''.join(face[j] for j in pieces[p]) for p in C)
X=[]
for sign,a,b in product((0,1),range(2),range(3)):
 ee=''.join(e[:10])+''.join(e[10+(j^sign)][(s+(a if j==0 else -a))%2] for j in range(2) for s in range(2))
 cc=''.join(c[:6])+''.join(c[6+(j^sign)][(s+(b if j==0 else -b))%3] for j in range(2) for s in range(3))
 X.append((ee,cc,sign))
assert len(X)==12 and len(set((ee,cc) for ee,cc,_ in X))==12
FULL=(1<<12)-1
# Every query partition as 36 literal output masks, flattened into 576 actions.
QS=tuple(product(range(24),repeat=2));A=[]
for qe,qc in QS:
 d=defaultdict(int)
 for i,(ee,cc,_) in enumerate(X):d[ee[qe]+cc[qc]]|=1<<i
 A.append(tuple(d.values()))
assert len(A)==576
@lru_cache(None)
def partition_hist(mask):
 return tuple(sorted(Counter(tuple(sorted(((mask&cell).bit_count() for cell in cells if mask&cell),reverse=True)) for cells in A).items()))
@lru_cache(None)
def optimal(mask):
 if mask.bit_count()<=1:return 0
 return 1+min(max(optimal(mask&g) for g in p if mask&g) for p in A if any((mask&g)!=mask for g in p if mask&g))
# Whole suffix: for all targets and all subsets of the 10 unread original source slots, collect reachable beliefs.
readable=tuple([('E',20),('E',21),('E',22),('E',23)]+[('C',j) for j in range(18,24)])
by_mask={}
for target in range(12):
 for subset in range(1<<len(readable)):
  mask=FULL;readings=[]
  for j,(sec,q) in enumerate(readable):
   if subset>>j&1:
    sym=X[target][0 if sec=='E' else 1][q]
    readings.append((sec,q,sym))
    mask &= next(g for g in (A[0][0],) if False) if False else FULL
    mask &= sum(1<<k for k,x in enumerate(X) if x[0 if sec=='E' else 1][q]==sym)
  if not mask:raise AssertionError
  by_mask.setdefault(mask,tuple(readings))
print('masks',len(by_mask), 'sizes',Counter(k.bit_count() for k in by_mask),flush=True)
# Pair with equal posterior populations and equal sign-stratified completion counts but different full 576-query multisets.
classes=defaultdict(list)
for mask,readings in by_mask.items():
 classes[(mask.bit_count(),sum(bool(mask>>i&1) for i in range(6)),sum(bool(mask>>i&1) for i in range(6,12)))].append(mask)
found=None;depth_pair=None;fingerprint_sets=defaultdict(set)
for key,masks in sorted(classes.items(),reverse=True):
 if key[0]<=1:continue
 sigs=defaultdict(list)
 for mask in masks:
  p=partition_hist(mask);sigs[p].append(mask);fingerprint_sets[key].add(p)
 if len(sigs)>1 and found is None:
  a,b=[next(iter(v)) for v in list(sigs.values())[:2]]
  found=(key,a,b)
 for a in masks:
  for b in masks:
   if a>=b:continue
   if optimal(a)!=optimal(b):depth_pair=(key,a,b);break
  if depth_pair:break
 if depth_pair:break

def desc(item):
 if item is None:return None
 key,a,b=item;out={'class':key,'A':{'mask':a,'observations':by_mask[a],'optimal_remaining':optimal(a),'partition_histogram':[[list(k),v] for k,v in partition_hist(a)]},'B':{'mask':b,'observations':by_mask[b],'optimal_remaining':optimal(b),'partition_histogram':[[list(k),v] for k,v in partition_hist(b)]}}
 return out
receipt={'result':'R14_P83_EXACT_REACHABLE_SUFFIX_BELIEF_CLASSES_PASS','legal_suffix_states':12,'spatial_paired_queries':576,'possible_suffix_facelet_constraints':10,'actual_realizable_beliefs':len(by_mask),'equal_posterior_parity_classes':len(classes),'any_nonisomorphic_under_query_relabeling_invariant':found is not None,'fingerprint_counterexample':desc(found),'exact_depth_counterexample':desc(depth_pair),'depth_histogram':dict(Counter(str(optimal(mask)) for mask in by_mask)), 'limitations':'Search only inside 10E6C fully observed suffix on independently generated P48 geometry. Different aggregate 576 partition multisets proves no observation query/outcome bijection, but does not assert general physical group orbit or root 20-frame theorem.'}
p=Path(__file__).with_name('R14_P83_SUFFIX_BELIEF_EQUIVALENCE_RECEIPT.json');p.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in receipt.items() if 'counterexample' not in k},indent=2),flush=True)

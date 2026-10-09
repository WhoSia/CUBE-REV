#!/usr/bin/env python3
"""Fully independent, no LP/SAT, physical-source-locked integer validation.
Covers ALL rank-seven t=1,2,3 symmetry orbits against ALL physically realized
rank5/rank6 full-original source-coverage masks in original 1192 coordinates.
"""
import argparse,hashlib,json,time
from collections import Counter
from itertools import combinations,product
from pathlib import Path

p=argparse.ArgumentParser()
for n in ('physical','partitions','certificates','output'):p.add_argument('--'+n,required=True)
a=p.parse_args();start=time.monotonic()
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
src=json.loads(raw)['bases'];assert len(src)==1192
byrank={5:set(),6:set(),7:set()};partition_count=0
for ln in Path(a.partitions).read_text().splitlines():
 word,rawparts=ln.split('|');parts=tuple(map(int,rawparts.split()))
 assert len(word.split())==5
 assert len(set(parts))==len(parts) and sum(x.bit_count() for x in parts)==12
 union=0
 for x in parts:assert not union&x;union|=x
 assert union==4095
 partition_count+=1
 if len(parts) not in byrank:continue
 c=0
 for i,A in enumerate(src):
  if all((A&part).bit_count()<=1 for part in parts):c|=1<<i
 byrank[len(parts)].add(c)
assert partition_count==14938
assert {i:len(x) for i,x in byrank.items()}=={5:2295,6:1144,7:32}
low=sorted(byrank[5]|byrank[6]);hi=sorted(byrank[7]);assert len(low)==3439
# Validate full original-source incidence automorphism, not geometric guess.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
coord_index={x:i for i,x in enumerate(coords)};src_index={v:i for i,v in enumerate(src)}
hi_index={v:i for i,v in enumerate(hi)};group=[];low_by_rank=[byrank[5],byrank[6]]
def transform(m,row_perm):
 z=0
 while m:
  bit=m&-m;z|=1<<row_perm[bit.bit_length()-1];m-=bit
 return z
for axes in ((0,1,2),(1,0,2)):
 for signs in product((-1,1),repeat=3):
  perm=[coord_index[tuple(signs[k]*pos[axes[k]] for k in range(3))] for pos in coords]
  row_perm=[]
  for A in src:
   j=sum(1<<perm[i] for i in range(12) if A>>i&1)
   assert j in src_index
   row_perm.append(src_index[j])
  assert len(set(row_perm))==1192
  # Check rank-class-specific raw physical closure: every low type, every high type.
  for rank_cls in low_by_rank:
   assert {transform(mask,row_perm) for mask in rank_cls}==rank_cls
  assert {transform(mask,row_perm) for mask in hi}==set(hi)
  group.append(tuple(hi_index[transform(mask,row_perm)] for mask in hi))
assert len(group)==16
cert=json.loads(Path(a.certificates).read_text())
assert cert['physical_source_sha256']==sha
assert cert['expected_integer_certificates']==374 and not cert['uncertified_cases']
assert len(cert['certificates'])==374
assert cert['raw_rank5_full_source_types']==2295 and cert['raw_rank6_full_source_types']==1144 and cert['raw_rank7_full_source_types']==32
cert_by_mask={}
for z in cert['certificates']:
 masks=tuple(sorted(int(h,16) for h in z['rank7_original_source_coverage_masks_hex']))
 assert len(masks)==z['rank7_count']==len(set(masks))
 assert all(m in hi_index for m in masks)
 assert masks not in cert_by_mask
 cert_by_mask[masks]=z

# For each original row, list actual physically realizable low-rank columns that cover it.
row_support=[0]*1192
for j,m in enumerate(low):
 while m:
  bit=m&-m;row_support[bit.bit_length()-1]|=1<<j;m-=bit

cert_checked=0;orbit_summary={}
for t in (1,2,3):
 visited=set();hist=Counter();count=0;min_gap=None
 for cand in combinations(range(32),t):
  if cand in visited:continue
  orbit={tuple(sorted(g[i] for i in cand)) for g in group}
  assert cand in orbit and not (visited&orbit)
  visited.update(orbit);hist[len(orbit)]+=1;count+=1
  key=tuple(sorted(hi[i] for i in cand))
  assert key in cert_by_mask,(t,cand)
  z=cert_by_mask.pop(key)
  assert sorted(int(x,16) for x in z['rank7_original_source_coverage_masks_hex'])==list(key)
  high_union=0
  for mask in key:high_union|=mask
  weights=z['positive_original_1192_row_weights']
  assert weights and all(len(pair)==2 for pair in weights)
  seen_rows=set();W=0;score=[0]*len(low)
  for original_row,weight in weights:
   original_row=int(original_row);weight=int(weight)
   assert 0<=original_row<1192 and original_row not in seen_rows and weight>0
   assert not (high_union>>original_row&1),'CERT_WEIGHT_ON_ALREADY_COVERED_ROW'
   seen_rows.add(original_row);W+=weight
   support=row_support[original_row]
   while support:
    bit=support&-support;score[bit.bit_length()-1]+=weight;support-=bit
  B=max(score)
  assert W==z['total'] and B==z['max_one_raw_physical_rank5or6_word_weight']
  gap=W-(7-t)*B
  assert gap==z['exact_integer_gap'] and gap>0,(t,cand,gap)
  min_gap=gap if min_gap is None else min(gap,min_gap)
  cert_checked+=1
 assert len(visited)=={1:32,2:496,3:4960}[t]
 assert count=={1:3,2:44,3:327}[t]
 orbit_summary[str(t)]={'representatives':count,'orbit_histogram':dict(hist),'minimum_integer_gap':min_gap}
 print('CUBE_REV_019_P13_RANK7_RAW_SOURCE_DUAL_VERIFIED',t,count,'min_gap',min_gap,'seconds',round(time.monotonic()-start,1),flush=True)
assert not cert_by_mask and cert_checked==374
receipt={'result':'CUBE_REV_019_P13_ALL_374_RAW_PHYSICAL_RANK7_1_2_3_INTEGER_DUAL_ORBITS_PASS','source_sha256':sha,
         'partition_representatives_replayed':partition_count,'original_source_rows':len(src),
         'raw_rank5_full_source_types':2295,'raw_rank6_full_source_types':1144,'raw_rank7_full_source_types':32,
         'verified_incidence_automorphisms':16,'verified_conditional_integer_certificates':374,
         'orbit_summary':orbit_summary,'proof':'Exact physical original-source-cover plus independent source-indexed integer weighted residual mass > (7-t)*single-low-column capacity',
         'seconds':time.monotonic()-start}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['result'],flush=True)
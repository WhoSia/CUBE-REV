#!/usr/bin/env python3
"""Rebuild source-locked entire physical 5-HTM k7 set-cover kernel.
Pure Python, no SAT, no LP, no scipy. Any SAT/UNSAT still needs external proof.
Input source/move/partition files from frozen 0.18/0.19 sticker-derived exporters.
"""
from pathlib import Path
from itertools import product
import argparse,hashlib,json,time
from functools import reduce
P=argparse.ArgumentParser()
for name in ('physical','maps','partitions','p13_gate','dual','output'):P.add_argument('--'+name,required=True)
a=P.parse_args()
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
bases=json.loads(raw)['bases'];assert len(bases)==1192
move_data=Path(a.maps).read_text().strip()
try:
 maps=json.loads(move_data)
except ValueError:
 maps=[list(map(int,l.split()))for l in move_data.splitlines()]
assert len(maps)==18 and all(len(a)==24 and len(set(a))==24 for a in maps)
GATE=json.loads(Path(a.p13_gate).read_text());assert GATE['status']=='CUBE_REV_019_P13_R5_K7_AT_LEAST_TWO_HIGH_RANK_PHYSICAL_INTEGER_PASS' and GATE['original_physical_source_sha256']==sha
start=time.monotonic()
def obs(word):
 states=[2*i for i in range(12)];codes=[0]*12
 for k,x in enumerate(word):
  states=[maps[x][s]for s in states]
  codes=[c|((states[j]&1)<<k)for j,c in enumerate(codes)]
 cls={}
 for j,c in enumerate(codes):cls[c]=cls.get(c,0)|(1<<j)
 return tuple(sorted(cls.values()))

def cover(blocks):
 return sum(1<<i for i,base in enumerate(bases) if all((base&b).bit_count()<=1 for b in blocks))

real={};partitions=0
for line in Path(a.partitions).read_text().splitlines():
 p,b=line.split('|');word=tuple(map(int,p.split()));blocks=tuple(map(int,b.split()));assert len(word)==5
 assert obs(word)==blocks,('ORIGINAL_PHYSICAL_ORACLE_MISMATCH',word)
 assert len(blocks)==len(set(blocks)) and sum(z.bit_count() for z in blocks)==12
 fullmask=cover(blocks)
 real.setdefault(fullmask,{'word':word,'blocks':blocks})
 partitions+=1
assert partitions==14938 and len(real)==14446
print('P13_ORIGINAL_PHYSICAL_14938_PARTITIONS_14446_COLUMN_TYPES_PASS',round(time.monotonic()-start,2),flush=True)

def maximal(masks):
 keep=[]
 for m in sorted(masks,key=int.bit_count,reverse=True):
  if not any((m&~q)==0 for q in keep):keep.append(m)
 return keep

allmax=maximal(real);assert len(allmax)==8807
full=(1<<1192)-1;assert reduce(int.__or__,allmax,0)==full
S=[0]*1192
for j,mask in enumerate(allmax):
 one=1<<j
 while mask:
  bit=mask&-mask;S[bit.bit_length()-1]|=one;mask-=bit
assert all(S)
core=[]
for i in sorted(range(1192),key=lambda k:S[k].bit_count()):
 if not any((S[parent]&~S[i])==0 for parent in core):core.append(i)
assert len(core)==544
assert sum(bases[i].bit_count()==5 for i in core)==480
assert sum(bases[i].bit_count()==4 for i in core)==64
projected={}
for src in allmax:
 projection=sum(1<<j for j,i in enumerate(core) if (src>>i)&1)
 projected.setdefault(projection,src)
projected_masks=maximal(projected);assert len(projected_masks)==2887
candidates=[(mask,projected[mask]) for mask in projected_masks]
rankall=[len(real[o]['blocks']) for _,o in candidates]
from collections import Counter
assert Counter(rankall)==Counter({4:484,5:1355,6:1016,7:32}),Counter(rankall)
actual=[(p,o)for (p,o),r in zip(candidates,rankall) if r>=5];assert len(actual)==2403
ranks=[len(real[o]['blocks']) for p,o in actual]
print('P13_ALL_K_544x2887_AND_P12_K7_RANK_544x2403_PASS',round(time.monotonic()-start,2),flush=True)

# Check full 16-element automorphism closure on the full original source
# and on all FULL 8807 physically realized maximal coverage types.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
cidx={c:i for i,c in enumerate(coords)};bidx={b:i for i,b in enumerate(bases)}
orig_set=set(allmax);coreidx={k:i for i,k in enumerate(core)}
rankedidx={p:i for i,(p,o) in enumerate(actual)}
automorphisms=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in product((-1,1),repeat=3):
  perm=[cidx[tuple(signs[k]*pt[axes[k]] for k in range(3))]for pt in coords]
  srcperm=[]
  for b in bases:
   z=sum(1<<perm[j] for j in range(12) if b>>j&1)
   assert z in bidx
   srcperm.append(bidx[z])
  ck=[coreidx[srcperm[j]] for j in core]
  # Exact raw physical-source 8807 inclusion-maximal column closure
  for m in allmax:
   transformed=0
   while m:
    bit=m&-m;transformed|=1<<srcperm[bit.bit_length()-1];m-=bit
   assert transformed in orig_set,('BAD_PHYSICAL_INCIDENCE_AUTOMORPHISM',axes,signs)
  colperm=[]
  for j,(proj,original) in enumerate(actual):
   q=proj;z=0
   while q:
    bit=q&-q;z|=1<<ck[bit.bit_length()-1];q-=bit
   assert z in rankedidx
   dest=rankedidx[z];assert ranks[dest]==ranks[j]
   colperm.append(dest)
  automorphisms.append(colperm)
assert len(automorphisms)==16
unseen=set(range(len(actual)));orbits=[];first_high=[]
while unseen:
 j=min(unseen);orbit={g[j]for g in automorphisms};assert orbit<=unseen
 unseen-=orbit;orbits.append((j,len(orbit),ranks[j]))
 if ranks[j]>=6:first_high.append(j+1)
assert len(orbits)==164 and len(first_high)==69,(len(orbits),len(first_high))
print('P13_16_FULL_PHYSICAL_AUTOMORPHISMS_164_RANKED_ORBITS_69_HIGH_FIRST_ORBITS_PASS',round(time.monotonic()-start,2),flush=True)

# The genuine FULL original 70-row dual gives W=384 and per-word <=72;
# k=7, choose t=2 => U(two selected) >= W-5B = 24.
# All 2403 projected columns retain the exact 1192-source physical cover.
prior=json.loads(Path(a.dual).read_text())
assert prior['denominator']==72 and prior['max_column_weight_numerator']==72 and prior['sum_row_weight_numerator']==384
weights={int(k):int(v)for k,v in prior['selected_original_rows_weights_numerator'].items()}
assert len(weights)==70 and sum(weights.values())==384
scores=[sum(v for k,v in weights.items() if o>>k&1)for p,o in actual]
assert max(scores)==72
small=[i for i,s in enumerate(scores) if s<24]
conflicts=[]
for z,i in enumerate(small):
 for j in small[z+1:]:
  shared=sum(w for k,w in weights.items() if (actual[i][1]&actual[j][1])>>k&1)
  if scores[i]+scores[j]-shared<24:conflicts.append([-(i+1),-(j+1)])
assert len(conflicts)==102979,(len(conflicts))
print('P13_REAL_PHYSICAL_K7_DUAL_PAIR_CUTS_102979_PASS',round(time.monotonic()-start,2),flush=True)

out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
material={'schema':'cube-rev.019.P13.full-original-physical-L5-k7-source-locked-sat-instance.v1',
 'frozen_physical_sha256':sha,'original_requirement_count':1192,'source_core_row_indices':core,
 'original_physical_partition_count':14938,'full_physical_coverage_types':14446,
 'original_all_k_reduced_row_count':544,'original_all_k_maximal_column_count':2887,
 'selected_full_original_k7_physical_column_count':2403,
 'candidate_core_cover_hex':[hex(p)for p,o in actual],
 'candidate_original_source_cover_hex':[hex(o)for p,o in actual],
 'candidate_move_words':[list(real[o]['word']) for p,o in actual],
 'candidate_partition_ranks':ranks,'first_high_representative_1based':first_high,
 'first_high_count':69,'physical_group_order':16,'rank_at_least_6_minimum_for_k7':2,
 'full_original_70_weight_dual_mass':384,'dual_max_single_physical_word':72,
 'dual_derived_forbidden_pair_count':102979,'dual_derived_forbidden_pair_literals':conflicts,
 'proved_properties_only':'Input is SAT/UNSAT EQUIVALENT to original physical full 1192-source <=7 iff P12 R5 exact 7 and this P13 >=2 high theorem have been independently validated. This file itself asserts no SAT/UNSAT result.'}
(out/'P13_full_k7_physical_kernel.json').write_text(json.dumps(material,separators=(',',':'))+'\n')
receipt={'state':'P13_SOURCE_LOCKED_FULL_K7_SAT_PREPARATION_PASS','physical_source_sha256':sha,
 'full_original_requirements':1192,'full_physical_partitions':14938,'all_k_irredundant_rows':544,
 'all_k_reduced_columns':2887,'rank4_excluded_columns':484,'physical_k7_columns':2403,
 'at_least_two_rank6_words_required':True,'physical_incidence_symmetries_checked':16,
 'rank_eligible_column_orbits':164,'high_first_word_orbits':69,
 'necessary_dual_pair_conflicts':102979,
 'result':'UNKNOWN_SAT_UNSAT_NOT_CHECKED','elapsed_seconds':round(time.monotonic()-start,2)}
(out/'P13_full_k7_preparation_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('CUBE_REV_019_P13_SOURCE_LOCKED_FULL_K7_544x2403_PREPARED_NOT_DECIDED',json.dumps(receipt),flush=True)
#!/usr/bin/env python3
"""CUBE-REV 0.19 P11: independently check exact physical k6 rank gate,
symmetry orbits, and source-dual 747883 pair incompatibility clauses.
Only immutable physical 480-source masks, actual edge move actions and integers.
Proves VALID necessary conditions; does not prove k6 UNSAT.
"""
import argparse,itertools,json,hashlib,collections,time
from pathlib import Path
ap=argparse.ArgumentParser()
for x in ('physical','maps','partitions','dual','output'):ap.add_argument('--'+x,required=True)
a=ap.parse_args();t0=time.monotonic()
raw=Path(a.physical).read_bytes();sha=hashlib.sha256(raw).hexdigest()
assert sha=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
base=json.loads(raw)['bases'];five=[int(x) for x in base if int(x).bit_count()==5];assert len(base)==1192 and len(five)==480
maps=[list(map(int,line.split())) for line in Path(a.maps).read_text().splitlines()];assert len(maps)==18 and all(len(m)==24 and len(set(m))==24 for m in maps)
cert=json.loads(Path(a.dual).read_text());assert cert['physical_source_sha256']==sha
origweights={int(k):int(v) for k,v in cert['dual_original_source_rows_scaled'].items()}
weighted=[(j,origweights[i]) for j,i in enumerate(k for k,b in enumerate(base) if int(b).bit_count()==5) if i in origweights]
assert len(weighted)==80 and sum(w for j,w in weighted)==1480 and cert['dual_common_denom']==312
full=(1<<480)-1

def physical_blocks(word):
 s=[2*i for i in range(12)];h=[0]*12
 for i,a in enumerate(word):
  s=[maps[a][z] for z in s]
  for j in range(12):h[j]|=(s[j]&1)<<i
 d={}
 for j,z in enumerate(h):d[z]=d.get(z,0)|(1<<j)
 return tuple(sorted(d.values()))

def five_cover(bl):
 return sum(1<<j for j,v in enumerate(five) if all((v&b).bit_count()<=1 for b in bl))

byrank=collections.defaultdict(set);all_masks=set(); representatives={};rawpartitions=0
for ln in Path(a.partitions).read_text().splitlines():
 wtxt,btxt=ln.split('|');word=tuple(map(int,wtxt.split()))
 assert len(word)==5 and all(0<=m<18 for m in word)
 block=tuple(sorted(map(int,btxt.split())))
 assert block==physical_blocks(word)
 mask=five_cover(block);rank=len(block)
 byrank[rank].add(mask);all_masks.add(mask);representatives.setdefault(mask,word)
 rawpartitions+=1
assert rawpartitions==14938 and len(all_masks)==3344
assert {k:len(v) for k,v in byrank.items()}=={1:1,2:1,3:1,4:1,5:2168,6:1144,7:32}, {k:len(v) for k,v in byrank.items()}
assert all(m==0 for k in (1,2,3,4) for m in byrank[k])
assert max(m.bit_count() for m in byrank[5])==64
assert max(m.bit_count() for m in byrank[6])==132
assert sorted(collections.Counter(m.bit_count() for m in byrank[7]).items())==[(100,16),(168,16)]
# Full-physical raw partition test (NOT merely source-reduced maximal columns)
rank7_audit=[]
for m in byrank[7]:
 uncovered=full&~m
 max_gain=max((c&uncovered).bit_count() for c in byrank[5])
 assert (m.bit_count(),max_gain) in ((100,64),(168,48))
 assert 5*max_gain<uncovered.bit_count()
 rank7_audit.append((m.bit_count(),max_gain))
assert 132+5*64<480
# Therefore a six-word full five-source cover requires >=2 words with output rank>=6.

# Reconstruct all-k maximal original five-only coverage family.
ordered=sorted(all_masks,key=lambda m:(-m.bit_count(),m))
retained=[]
for m in ordered:
 if not any(m&~x==0 for x in retained):retained.append(m)
assert len(retained)==2023
rank_map={m:len(physical_blocks(representatives[m])) for m in retained}
assert collections.Counter(rank_map.values())=={5:975,6:1016,7:32}
lookup=set(retained)
# Incidence-only cube coordinate automorphisms; all source permutations
# and physically realized maximal coverage masks must be validated.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
pos={v:i for i,v in enumerate(coords)}
assert len(pos)==12
five_index={v:i for i,v in enumerate(five)}
actions=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in itertools.product((-1,1),repeat=3):
  perm=[pos[tuple(signs[k]*v[axes[k]] for k in range(3))] for v in coords]
  ps=[]
  for v in five:
   t=sum(1<<perm[i] for i in range(12) if (v>>i)&1)
   assert t in five_index
   ps.append(five_index[t])
  assert len(set(ps))==480
  actions.append(ps)
assert len(actions)==16

def transform(mask,perm):
 t=0
 while mask:
  bit=mask&-mask;t|=1<<perm[bit.bit_length()-1];mask-=bit
 return t
for perm in actions:
 for m in retained:
  m2=transform(m,perm)
  assert m2 in lookup
  assert rank_map[m]==rank_map[m2],('RANK_NOT_PRESERVED_BY_PHYSICAL_SYMMETRY',rank_map[m],rank_map[m2])
remaining=set(retained);orb_count=collections.Counter();high_orbit_reps=[]
while remaining:
 base=min(remaining);orb={transform(base,perm) for perm in actions}
 assert base in orb and orb<=remaining
 rr=rank_map[base]
 assert all(rank_map[v]==rr for v in orb)
 orb_count[rr]+=1
 if rr>=6:high_orbit_reps.append(base)
 remaining-=orb
assert orb_count=={5:68,6:66,7:3} and len(high_orbit_reps)==69

# R5 dual necessary union inequality for k<=6, t=2:
# 1480 -(6-2)*312 = 232.
# Each illegal pair produces a sound binary SAT clause !x_i OR !x_j.
parts=[[(p,w) for p,w in weighted[k:k+10]] for k in range(0,80,10)]
tables=[]
for row in parts:tables.append([sum(w for i,(_,w) in enumerate(row) if (m>>i)&1) for m in range(1<<len(row))])
bits=[];individual_mass=[]
for m in retained:
 u=sum(1<<i for i,(r,w) in enumerate(weighted) if (m>>r)&1)
 bits.append(u)
 score=sum(tab[(u>>(10*k))&1023] for k,tab in enumerate(tables))
 individual_mass.append(score)
assert max(individual_mass)==312
forbidden=0
for i in range(len(retained)):
 for j in range(i+1,len(retained)):
  union=bits[i]|bits[j]
  total=sum(tab[(union>>(10*k))&1023] for k,tab in enumerate(tables))
  if total<232:forbidden+=1
assert forbidden==747883,forbidden
receipt={'schema':'cube-rev.019.P11.five-only-physical-rank-symmetry-k6-cut.v1',
 'physical_source_sha256':sha,'real_L5_words':18**5,'replayed_L5_partitions':rawpartitions,
 'distinct_R5_cover_types':3344,'all_k_maximal_R5_cover_types':2023,
 'rank5_masks':len(byrank[5]),'rank6_masks':len(byrank[6]),'rank7_masks':len(byrank[7]),
 'max_covered_R5_sources_rank5':64,'max_covered_R5_sources_rank6':132,
 'rank7_original_source_count_vs_rank5_max_gain':sorted(set(rank7_audit)),
 'theorem':'Every full 480-five-source six-word dictionary must include at least TWO real words of output partition rank >=6.',
 'physical_incidence_symmetries_checked':16,'maximal_column_orbits_by_rank':dict(orb_count),
 'safe_high_rank_first_column_orbit_representatives':69,
 'r5_dual_total_weight':1480,'r5_single_word_max_weight':312,
 'r5_k6_two_word_min_union':232,
 'r5_k6_forbidden_pair_count':forbidden,
 'r5_k6_remaining_pair_count':2023*2022//2-forbidden,
 'result':'CUBE_REV_019_P11_R5_RANK_AND_SYMMETRY_INTEGER_PAIR_GATE_PASS',
 'new_integer_Mstar5_value':'NOT_ESTABLISHED',
 'elapsed_seconds':round(time.monotonic()-t0,3)}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['result'],json.dumps({k:receipt[k] for k in ('safe_high_rank_first_column_orbit_representatives','r5_k6_forbidden_pair_count','elapsed_seconds')}),flush=True)
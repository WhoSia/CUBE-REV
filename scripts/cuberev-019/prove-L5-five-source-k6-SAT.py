#!/usr/bin/env python3
"""CUBE-REV 0.19 P10: physically sealed 480-five-source k<=6 SAT/DRUP court.
Preprocessing can be locally audited WITHOUT any SAT package (--prepare-only).
Solver UNSAT must pass separately pinned drat-trim; numerical MIP is not a proof.
"""
import argparse, hashlib, itertools, json, time
from pathlib import Path
p=argparse.ArgumentParser()
for x in ('physical','maps','partitions','output'):p.add_argument('--'+x,required=True)
p.add_argument('--prepare-only',action='store_true')
p.add_argument('--conflicts',type=int,default=30000000)
a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
raw=Path(a.physical).read_bytes();source_hash=hashlib.sha256(raw).hexdigest()
assert source_hash=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
bases=json.loads(raw)['bases'];assert len(bases)==1192
five=[(j,r) for j,r in enumerate(bases) if r.bit_count()==5];assert len(five)==480
maps=[list(map(int,z.split())) for z in Path(a.maps).read_text().splitlines()]
assert len(maps)==18 and all(len(g)==24 and len(set(g))==24 for g in maps)

def physical_blocks(word):
 s=[2*j for j in range(12)];h=[0]*12
 for t,x in enumerate(word):
  s=[maps[x][v] for v in s];h=[v|((s[j]&1)<<t) for j,v in enumerate(h)]
 b={}
 for j,v in enumerate(h):b[v]=b.get(v,0)|(1<<j)
 return tuple(sorted(b.values()))

def cover_five(bl):
 return sum(1<<j for j,(_,r) in enumerate(five) if all((r&b).bit_count()<=1 for b in bl))

actual={};partition_count=0
for line in Path(a.partitions).read_text().splitlines():
 wtext,btext=line.split('|');word=tuple(map(int,wtext.split()))
 assert len(word)==5 and all(0<=v<18 for v in word)
 bl=tuple(sorted(map(int,btext.split())))
 assert bl==physical_blocks(word),'physical orbit mismatch'
 m=cover_five(bl);actual.setdefault(m,word);partition_count+=1
assert partition_count==14938 and len(actual)==3344
keep=[]
for m in sorted(actual,key=lambda z:(-z.bit_count(),z)):
 if not any(m&~c==0 for c in keep):keep.append(m)
assert len(keep)==2023
idx={m:i for i,m in enumerate(keep)}
# Prove group acts on original five-source set and every physically realized
# inclusion-maximal coverage mask, before adding ANY symmetry-break clause.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),(1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),(1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
pos={c:i for i,c in enumerate(coords)};source_index={mask:i for i,(_,mask) in enumerate(five)}
actions=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in itertools.product((-1,1),repeat=3):
  perm=[pos[tuple(signs[k]*point[axes[k]] for k in range(3))] for point in coords]
  src_perm=[]
  for _,r in five:
   target=sum(1<<perm[i] for i in range(12) if r>>i&1)
   assert target in source_index
   src_perm.append(source_index[target])
  assert len(set(src_perm))==480
  for m in keep:
   t=0
   while m:
    bit=m&-m;j=bit.bit_length()-1;t|=1<<src_perm[j];m-=bit
   assert t in idx, 'false physical-source symmetry'
  actions.append(src_perm)
assert len(actions)==16
remaining=set(keep);reps=[];sizes=[]
while remaining:
 m=min(remaining);orbit=set()
 for perm in actions:
  t=0;v=m
  while v:
   bit=v&-v;j=bit.bit_length()-1;t|=1<<perm[j];v-=bit
  orbit.add(t)
 assert orbit<=remaining and m in orbit
 remaining-=orbit;reps.append(idx[m]+1);sizes.append(len(orbit))
assert len(reps)==137
# Source positive witness is independently replayed in a standalone physical court.
known_seven=[(7,16,0,6,15),(7,15,9,6,15),(6,16,12,6,15),(6,16,9,6,15),(6,16,3,6,15),(6,15,0,6,15),(6,16,2,14,6)]
positive=0
for word in known_seven:positive|=cover_five(physical_blocks(word))
assert positive==(1<<480)-1
receipt={'schema':'cube-rev.019.P10.R5-k6-physical-SAT-court.v1','source_sha256':source_hash,
 'physical_five_turn_words':18**5,'real_partitions':partition_count,'five_source_cover_types':len(actual),
 'inclusion_maximal_five_source_columns':len(keep),'symmetry_group_order':len(actions),
 'distinct_column_orbits':len(reps),'witness_seven_word_upper_verified':True,
 'k6_decision':'UNKNOWN_PREPARED_NOT_EXTERNALLY_CERTIFIED',
 'note':'Numerical HiGHS 7-optimal status is diagnostic only; a DRUP-verifiable k6 negative certificate has not yet been emitted.'}
(out/'R5_k6_preparation.json').write_text(json.dumps(receipt,indent=2)+'\n')
# Write deterministic fully physical witnesses for run review. These are
# representatives of inclusion-maximal projected R5 columns, not original
# 1192-source cover-equivalent columns.
(out/'R5_five_source_reduced_cover_masks_hex.tsv').write_text(''.join(f'{m:x}\t{list(actual[m])}\n' for m in keep))
print('CUBE_REV_019_P10_R5_3344_TO_2023_PHYSICAL_COVER_COLUMNS_16_SYMMETRIES_137_ORBITS_PASS',flush=True)
if a.prepare_only:
 print('CUBE_REV_019_P10_R5_K6_PREPARE_ONLY_NO_SAT_OR_UNSAT_CLAIM',flush=True)
 raise SystemExit(0)
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Glucose4
cnf=CNF();cnf.append(reps) # sound: globally relabel nonempty dictionary to contain one representative
for j in range(480):
 clause=[i+1 for i,m in enumerate(keep) if m>>j&1];assert clause;cnf.append(clause)
pool=IDPool(start_from=len(keep)+1)
cnf.extend(CardEnc.atmost(lits=list(range(1,len(keep)+1)),bound=6,encoding=EncType.seqcounter,vpool=pool).clauses)
fn=out/'R5_k6_physical_with_sound_symmetry.cnf';cnf.to_file(str(fn))
receipt['cnf_sha256']=hashlib.sha256(fn.read_bytes()).hexdigest()
receipt['cnf_variables']=cnf.nv;receipt['cnf_clauses']=len(cnf.clauses)
started=time.monotonic()
with Glucose4(bootstrap_with=cnf.clauses,with_proof=True) as solver:
 solver.conf_budget(a.conflicts)
 answer=solver.solve_limited(expect_interrupt=False)
 receipt['solver_elapsed_seconds']=round(time.monotonic()-started,3)
 if answer is True:
  selected=[j for j in range(len(keep)) if j+1 in set(solver.get_model())]
  assert len(selected)<=6
  checks=0
  for j in selected:checks|=cover_five(physical_blocks(actual[keep[j]]))
  assert checks==(1<<480)-1
  receipt['k6_decision']='SAT_PHYSICAL_SIX_WORD_WITNESS_REPLAYED'
  receipt['selected_five_move_ids']=[actual[keep[j]] for j in selected]
  print('CUBE_REV_019_P10_K6_R5_SAT_PHYSICAL_REPLAY_PASS',flush=True)
 elif answer is False:
  proof=solver.get_proof();assert proof and proof[-1].strip()=='0'
  pf=out/'R5_k6_physical.drup';pf.write_text('\n'.join(proof)+'\n')
  receipt['k6_decision']='UNSAT_DRUP_EMITTED_EXTERNAL_VERIFICATION_PENDING'
  receipt['drup_sha256']=hashlib.sha256(pf.read_bytes()).hexdigest()
  print('CUBE_REV_019_P10_K6_R5_UNSAT_EXTERNAL_DRUP_CHECK_PENDING',flush=True)
 else:
  receipt['k6_decision']='UNKNOWN_SOLVER_CONFLICT_BUDGET'
  print('CUBE_REV_019_P10_K6_R5_UNKNOWN_CONFLICT_BUDGET',flush=True)
(out/'R5_k6_preparation.json').write_text(json.dumps(receipt,indent=2)+'\n')
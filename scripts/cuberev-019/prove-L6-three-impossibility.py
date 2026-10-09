#!/usr/bin/env python3
"""CUBE-REV 0.19 P7, no-SAT exact finite proof of M*(6)>=4.
Inputs: fully physical original source, move maps, enumerated L6 rank>=5 word
partitions, collision-refinement kernel TSV, rank<=7 integer dual receipt.
Separate 4-word physical dictionary replay gives the matching upper bound.
"""
import argparse, collections, hashlib, itertools, json, time
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser()
for x in ('physical','maps','partitions','kernel','dominance','dual','output'):
 p.add_argument('--'+x,required=True)
a=p.parse_args();start=time.time();physical=Path(a.physical).read_bytes()
assert hashlib.sha256(physical).hexdigest()=='9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1'
req=json.loads(physical)['bases'];assert len(req)==1192
maps=json.loads(Path(a.maps).read_text());assert len(maps)==18
assert all(len(m)==24 and len(set(m))==24 for m in maps)
flip={6,7,15,16}
assert len([r for r in req if r.bit_count()==5])==480
index={m:i for i,m in enumerate(req)}
# Exact original 1192-source collision failure incidence for any pair.
pair_source={}
for i in range(12):
 for j in range(i+1,12):
  m=(1<<i)|(1<<j)
  pair_source[i,j]=sum(1<<k for k,b in enumerate(req) if b&m==m)
def pattern(z):return tuple((z>>(4*i))&15 for i in range(12))
def signature(labels):
 q={};n=0;z=0
 for i,v in enumerate(labels):
  if v not in q:q[v]=n;n+=1
  z|=q[v]<<(4*i)
 return z
def physical_partition(word):
 state=[2*i for i in range(12)];trace=[0]*12
 for t,act in enumerate(word):
  state=[maps[act][v] for v in state]
  trace=[v|((state[i]&1)<<t) for i,v in enumerate(trace)]
 return signature(trace)
def collision(z):
 label=pattern(z);lo=hi=bad=0;pair=0
 for i in range(12):
  for j in range(i+1,12):
   if label[i]==label[j]:
    if pair<64:lo|=1<<pair
    else:hi|=1<<(pair-64)
    bad|=pair_source[i,j]
   pair+=1
 return lo,hi,bad
origin={};source_sha=hashlib.sha256(Path(a.partitions).read_bytes()).hexdigest()
for line in Path(a.partitions).read_text().splitlines():
 z,*word=map(int,line.split());word=tuple(word)
 assert len(word)==6 and sum(w in flip for w in word) in (3,4,5)
 assert z==physical_partition(word),'L6 partition does not agree with real edge oracle'
 assert len(set(pattern(z)))>=5
 assert z not in origin
 origin[z]=(word,len(set(pattern(z))),collision(z))
assert len(origin)==53528
print('L6_PHYSICAL_RANK5_53528_SOURCE_LINEAGE_PASS',round(time.time()-start,2),flush=True)
# The input C++ kernel derives the collision-subset order, not a numerical
# MILP dominance hypothesis. Verify every original source word is covered
# by an incumbent with <= collision edge set via a packed index check.
keep=[]
for line in Path(a.kernel).read_text().splitlines():
 z,*word=map(int,line.split());assert z in origin
 assert origin[z][0]==tuple(word)
 keep.append(z)
assert len(keep)==18813 and len(set(keep))==18813
source_counts=collections.Counter(len(set(pattern(z))) for z in origin)
assert source_counts=={5:25821,6:23439,7:4072,8:152,9:44}
retained_counts=collections.Counter(len(set(pattern(z))) for z in keep)
assert retained_counts=={5:6096,6:9889,7:2632,8:152,9:44}
# Enumerate 16 exact action-incidence signed-coordinate relabelings.
coords=[(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),
        (1,-1,0),(0,-1,1),(-1,-1,0),(0,-1,-1),
        (1,0,1),(-1,0,1),(-1,0,-1),(1,0,-1)]
pos={c:i for i,c in enumerate(coords)}
G=[]
for axes in ((0,1,2),(1,0,2)):
 for signs in itertools.product((-1,1),repeat=3):
  G.append(tuple(pos[tuple(signs[k]*coord[axes[k]] for k in range(3))]
                 for coord in coords))
assert len(G)==16
reqset=set(req)
for g in G:
 for b in req:
  t=sum(1<<g[i] for i in range(12) if b>>i&1)
  assert t in reqset
 for z in origin:
  old=pattern(z);new=[None]*12
  for i,v in enumerate(g):new[v]=old[i]
  assert signature(new) in origin,'signed relabeling does not preserve actual L6 physical partitions'
print('L6_FULL_53528_BY_16_PHYSICAL_SYMMETRY_CLOSED_PASS',round(time.time()-start,2),flush=True)
# No three-word dictionary may use an experiment whose output rank<5:
# separate C++ exhaustive two-word 480-five-source court rules out covering
# all five-sets with the other two rank>=5 words. The other flip-count cases
# have output rank<=4 analytically (F/B confinement and 2^q bound).
# The pair check MUST be run in the same CI workflow before this script.
# Independently check all 53,528 original-column to retained-column
# collision-edge inclusion witnesses emitted by the separate C++ kernel.
# This takes O(53528) rather than rerunning its dominance discovery loop.
seen_witnesses=set();keep_set=set(keep)
for line in Path(a.dominance).read_text().splitlines():
 child,parent=map(int,line.split())
 assert child in origin and parent in keep_set and child not in seen_witnesses
 seen_witnesses.add(child)
 clo,chi=origin[child][2][:2];plo,phi=origin[parent][2][:2]
 assert plo&~clo==0 and phi&~chi==0
assert seen_witnesses==set(origin)
print('L6_ALL_53528_TO_18813_DOMINANCE_REPLAY_PASS',round(time.time()-start,2),flush=True)
rows=[(z,*origin[z]) for z in keep] # z, word, rank, (lo,hi,bad)
N=len(rows);H={i for i,(_,w,r,c) in enumerate(rows) if r>=8};low=[i for i in range(N) if i not in H]
assert len(H)==196 and len(low)==18617
# Check independently rounded INTEGER (not floating LP) positive dual
# on the 480 original five-element source constraints after dominance.
cert=json.loads(Path(a.dual).read_text())
if 'positive_source_row_index_weight' in cert:
 fives=[int(r) for r,w in cert['positive_source_row_index_weight']]
 weights=[int(w) for r,w in cert['positive_source_row_index_weight']]
 assert len(fives)==172 and len(set(fives))==172
else:
 fives=cert['five_row_original_indices'];weights=cert['weights']
assert len(fives)==len(weights) and all(req[i].bit_count()==5 for i in fives)
W=sum(weights);lowmax=max(sum(w for i,w in zip(fives,weights) if not((rows[j][3][2]>>i)&1)) for j in low)
assert W==3126804 and lowmax==1000010 and W>3*lowmax
print('L6_K3_ALL_LOW_INTEGER_DUAL_UNSAT_PASS',W,lowmax,round(time.time()-start,2),flush=True)
# Precompute each core-row's sets of candidate words that distinguish it.
B=np.frombuffer(b''.join(row[3][2].to_bytes(149,'little') for row in rows),dtype=np.uint8).reshape(N,149)
cover=1-np.unpackbits(B,axis=1,bitorder='little')[:,:1192].T
pack=np.packbits(cover,axis=1,bitorder='little')
good=[int.from_bytes(bytes(v),'little') for v in pack]
freq=[v.bit_count() for v in good];allcols=(1<<N)-1;alllow=sum(1<<i for i in low)
def third_for_pair(i,j,allowed):
 residual=rows[i][3][2]&rows[j][3][2]
 needed=[]
 while residual:
  bit=residual&-residual;needed.append(bit.bit_length()-1);residual-=bit
 needed.sort(key=lambda r:freq[r])
 possibles=allowed
 for r in needed:
  possibles &= good[r]
  if not possibles:return None
 if possibles:return (possibles&-possibles).bit_length()-1
 return None
# If a three-word cover contains >=2 rank>=8 words, check all 19110 pairs.
allhigh=sorted(H);checked_twohigh=0
for t,i in enumerate(allhigh):
 for j in allhigh[t+1:]:
  witness=third_for_pair(i,j,allcols)
  assert witness is None,('THREE_COVER_WITH_TWO_HIGH',i,j,witness)
  checked_twohigh+=1
assert checked_twohigh==19110
print('L6_K3_AT_LEAST_TWO_HIGH_PHYSICAL_UNSAT_PASS',checked_twohigh,round(time.time()-start,2),flush=True)
# A solution with exactly one high word must be globally relabelable so that
# the selected high word is in one of 16 high-column G-orbit representatives.
code_idx={z:i for i,z in enumerate(keep)}
todo=set(H);reps=[]
while todo:
 s=min(todo);z=keep[s];orbit=[]
 for g in G:
  old=pattern(z);new=[None]*12
  for i,v in enumerate(g):new[v]=old[i]
  z2=signature(new)
  assert z2 in code_idx and code_idx[z2] in H
  orbit.append(code_idx[z2])
 orbit=set(orbit);assert orbit<=todo;todo-=orbit;reps.append(s)
assert len(reps)==16 and len(H)==196
count=0
for j,hi in enumerate(reps):
 for lo in low:
  witness=third_for_pair(hi,lo,alllow)
  assert witness is None,('THREE_COVER_WITH_ONE_HIGH',hi,lo,witness)
  count+=1
 print('L6_ORBIT_FIRST_K3_EXCLUDED',j+1,'of',len(reps),round(time.time()-start,2),flush=True)
assert count==16*18617==297872
receipt={'result':'CUBE_REV_019_L6_K3_FINITE_UNSAT_LOCAL_PASS',
 'scope':'source-locked 18-HTM physical L6 observation, 1192 original requirements, nonadaptive 3-word dictionary',
 'physical_sha256':hashlib.sha256(physical).hexdigest(),
 'all_rank5_partition_sha256':source_sha,'full_rank5_candidates':len(origin),
 'collision_inclusion_kernel_candidates':N,'full_symmetry_group':len(G),
 'rank8_or_9_columns':len(H),'high_orbit_representatives':len(reps),
 'verified_integer_dual_total':W,'verified_integer_dual_max_low_word':lowmax,
 'k3_at_least_two_high_pairs_checked':checked_twohigh,
 'k3_exactly_one_high_second_word_cases_checked':count,
 'verification_note':'Preceding same-CI two-word five-source gate and independent 4-word physical upper replay REQUIRED for M*(6)=4 promotion',
 'elapsed_seconds':round(time.time()-start,3)}
Path(a.output).write_text(json.dumps(receipt,indent=2)+'\n')
print('CUBE_REV_019_L6_K3_NO_THREE_WORDS_LOCAL_FINITE_PROOF_PASS',json.dumps(receipt),flush=True)
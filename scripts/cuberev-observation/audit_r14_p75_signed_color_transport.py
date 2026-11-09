#!/usr/bin/env python3
"""Exact color-action transport for parity-even, flip-even 6-edge residual game.
Not a full Rubik P48 symmetry. No source receipt dependencies.
"""
from itertools import permutations,product,combinations
from collections import Counter, defaultdict
from functools import reduce
from operator import xor
from pathlib import Path
import json,hashlib
T=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
PAIRS=(('U','D'),('R','L'),('F','B'))
canon={frozenset(e):e for e in T}
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
autos=[]
for perm in permutations(range(3)):
 for flips in product((0,1),repeat=3):
  d={}
  for j,(a,b) in enumerate(PAIRS):d[a],d[b]=PAIRS[perm[j]][flips[j]],PAIRS[perm[j]][1-flips[j]]
  autos.append(d)
assert len(autos)==48

def labelmap(L,c):
 Lp=tuple(sorted(canon[frozenset(c[x] for x in e)] for e in L))
 tau=[];eps=[]
 for e in L:
  w=''.join(c[x] for x in e); z=canon[frozenset(w)]
  tau.append(Lp.index(z));eps.append(0 if w==z else 1)
 return Lp,tuple(tau),tuple(eps)

def transform_word(w,L,c):
 Lp,tau,eps=labelmap(L,c);n=len(L)
 # Canonical spatial permutation is odd iff source-order map is odd.
 sig=list(range(n))
 if parity(tau):sig[0],sig[1]=sig[1],sig[0]
 # Canonical single spatial-slot flip absorbs total induced label orientation parity.
 delta=[0]*n;delta[0]=sum(eps)%2
 original=''.join(c[t] for t in w)
 transformed=''.join(original[2*sig[i]+(s^delta[i])] for i in range(n) for s in range(2))
 return Lp,transformed,tuple(2*sig[i]+(s^delta[i]) for i in range(n) for s in range(2))

def states(L):
 n=len(L)
 for p in permutations(range(n)):
  if parity(p):continue
  for f in product((0,1),repeat=n-1):
   ff=f+(sum(f)%2,)
   yield ''.join(L[p[i]][s^ff[i]] for i in range(n) for s in range(2))

six=list(combinations(T,6));groups=defaultdict(list)
for L in six:
 r=min(labelmap(L,c)[0] for c in autos);groups[r].append(L)
assert len(groups)==30 and sum(map(len,groups.values()))==924
# Exhaust the ENTIRE state space for a carefully chosen nontrivial 48-member orbit:
rep=next(r for r,g in sorted(groups.items()) if len(g)==48)
words=tuple(states(rep));base=set(words);assert len(base)==11520
for c in autos:
 target=labelmap(rep,c)[0]
 translated={transform_word(w,rep,c)[1] for w in words}
 assert len(translated)==11520
 assert translated==set(states(target)),(target,len(translated))
# Check ALL 924 subset-coordinate transforms on deterministic legal samples, and
# all 48*30 corresponding pair-query maps / parity corrections.
num_sample=0;all_pair_maps=set();seen_perm_parities=Counter();seen_flip_parities=Counter()
for L in six:
 examples=list(__import__('itertools').islice(states(L),4))
 assert len(examples)==4
 for c in autos:
  Lt,tau,eps=labelmap(L,c);seen_perm_parities[parity(tau)]+=1;seen_flip_parities[sum(eps)%2]+=1
  for w in examples:
   dest,z,qmap=transform_word(w,L,c)
   assert dest==Lt and len(qmap)==12 and set(qmap)==set(range(12))
   # independent recovery of target source permutation + orientations
   ps=[];fs=[]
   for i in range(6):
    piece=z[2*i:2*i+2]
    ids=[j for j,e in enumerate(Lt) if frozenset(e)==frozenset(piece)]
    assert len(ids)==1
    ps.append(ids[0]);fs.append(0 if piece==Lt[ids[0]] else 1)
   assert parity(ps)==0 and sum(fs)%2==0
   for qq in range(12):assert z[qq]==c[w[qmap[qq]]]
   num_sample+=1
  all_pair_maps.add(tuple(qmap))
# transport arbitrary facelet observation history, with new color outputs c[old].
receipt={"result":"R14_P75_SIGNED_SOURCE_COLOR_COVARIANCE_PASS",
 "domain":"Six-edge parity-even permutation and even total flip, edge-only color words; not full P48",
 "all_edge_type_sets":len(six),"graph_orbits":len(groups),"color_graph_automorphisms":len(autos),
 "exhaustive_48_automorphisms_one_orbit_state_set_checks":48,
 "states_per_exhaustive_check":11520,"direct_924_by_48_by_4_word_samples":num_sample,
 "source_permutation_parity_counts":dict(seen_perm_parities),"source_orientation_parity_counts":dict(seen_flip_parities),
 "distinct_spatial_query_permutations_observed":len(all_pair_maps),
 "construction":"source label-index permutation tau; spatial permutation sig with parity(sig)=parity(tau); side flip delta with sum(delta)=sum(label color-order inversions) modulo 2; target query (i,s) observes source (sig(i),s xor delta_i); colors relabeled via c",
 "proof":"p'=tau o p o sigma, so sign p'=sign tau + sign p + sign sigma=0; f'=old f + source epsilon + spatial delta, so sum f'=0; observable word covariant at every facelet; finite bijection has explicit inverse via unique p,f reconstruction.",
 "limitation":"does not imply deterministic coordinate-index tie-break is invariant; transport the representative policy, do not assume same query-index selection; no physical mixed corner sector lift."}
p=Path(__file__).with_name('R14_P75_SIGNED_COLOR_TRANSPORT_RECEIPT.json');p.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(receipt['result'],num_sample,flush=True)

#!/usr/bin/env python3
"""Independent checker for R14-P7 certificate and lower-collision receipts.
Reconstructs orientation/parity legality; never imports certificate generator.
"""
from itertools import permutations, product, combinations
from math import comb
import json,sys
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('R14_P7_CERTIFICATE_RESULTS.json')
w=Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).with_name('R14_P7_COLLISION_CERTIFICATES.json')
r=json.loads(p.read_text());led=json.loads(w.read_text())
assert r['result']=='R14_P7_INDIVIDUAL_CERTIFICATES_PASS'
assert r['legal_micro_states']==648 and r['query_pairs']==54
assert r['individual_min_certificate_histogram']=={'2':648}
assert r['known_exact_global_minimax']==4
assert len(r['residual_courts'])==len(led)==3
for row,proof in zip(r['residual_courts'],led):
    L=row['types']; n=len(L); depth=row['target_certificate_length'];solved=''.join(L)
    assert L==proof['types'] and proof['n']==n
    states=[]
    for p in permutations(range(n)):
        even=(sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2)==0
        if not even:continue
        for prefix in product((0,1),repeat=n-1):
            o=prefix+(sum(prefix)%2,)
            word=''.join(L[p[i]][(j+o[i])%2] for i in range(n) for j in range(2))
            states.append(word)
    assert len(states)==row['legal_states'] and len(set(states))==len(states)
    subset=row['certificate_sticker_slots']
    assert len(subset)==depth and len(set(subset))==depth
    assert sum(all(st[z]==solved[z] for z in subset) for st in states)==1
    proofs=proof['witnesses']
    assert len(proofs)==comb(2*n,depth-1)==proof['all_k_minus_1_read_sets']
    seen=set()
    for wit in proofs:
        positions=tuple(wit['read_slots'])
        assert positions not in seen and len(positions)==depth-1
        seen.add(positions)
        perm=wit['permutation']; o=wit['edge_flip']
        assert sorted(perm)==list(range(n)) and sum(o)%2==0
        assert sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2==0
        word=''.join(L[perm[i]][(j+o[i])%2] for i in range(n) for j in range(2))
        assert word==wit['alternative_word'] and word!=solved
        assert all(word[z]==solved[z] for z in positions)
        # Independently reconstruct alternating permutation cycles
        visited=set(); cycles=[]
        for k in range(n):
            if k in visited: continue
            cyc=[];v=k
            while v not in visited:
                visited.add(v);cyc.append(v);v=perm[v]
            if len(cyc)>1:cycles.append(cyc)
        assert cycles==wit['nontrivial_cycles']
    print(f'VERIFIED residual n={n}: {len(states)} states, k={depth}, {len(proofs)} complete k-1 collisions')
print('R14_P7_INDEPENDENT_CERTIFICATE_REPLAY_PASS')
core_path=Path(sys.argv[3]) if len(sys.argv)>3 else Path(__file__).with_name('R14_P7_DISTILLED_HARDNESS_CORES.json')
cores=json.loads(core_path.read_text())
assert len(cores)==3
for row in cores:
    n=row['n'];L=row['types'];k=next(z['target_certificate_length']-1 for z in r['residual_courts'] if z['remaining_cubies']==n)
    target=''.join(L)
    all_sets=set(combinations(range(2*n),k)); covered=set()
    for witness in row['witnesses']:
        p=witness['permutation'];o=witness['orientation'];word=witness['word']
        assert sorted(p)==list(range(n)) and sum(o)%2==0 and sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2==0
        assert word==''.join(L[p[i]][(j+o[i])%2] for i in range(n) for j in range(2)) and word!=target
        equal=[i for i in range(2*n) if word[i]==target[i]]
        new={s for s in combinations(equal,k) if s not in covered}
        assert len(new)==witness['newly_covered_subsets']
        covered.update(new)
    assert covered==all_sets
    print(f'VERIFIED n={n} concise obstruction nucleus: {len(row["witnesses"])} alternate states cover all {len(all_sets)} short read plans')
print('R14_P7_DISTILLED_HARDNESS_CORES_PASS')
# Independent microgame audit: prove all 648 target states possess a 2-pair
# certificate by exhaustive signature grouping, without relying on producer.
def parity2(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def micro_words(types,r):
    out=[]
    for p in permutations(range(3)):
        for prefix in product(range(r),repeat=2):
            o=prefix+((-sum(prefix))%r,)
            out.append((''.join(types[p[i]][(j+o[i])%r] for i in range(3) for j in range(r)),parity2(p)))
    return out
micro=[(e,c) for e,ep in micro_words(('UR','UF','UL'),2) for c,cp in micro_words(('URF','UFL','ULB'),3) if ep==cp]
assert len(micro)==648
certified=set()
for es in combinations(range(6),2):
    for cs in combinations(range(9),2):
        d={}
        for idx,(e,c) in enumerate(micro):
            sig=tuple(e[i] for i in es)+tuple(c[j] for j in cs)
            d.setdefault(sig,[]).append(idx)
        certified.update(v[0] for v in d.values() if len(v)==1)
assert len(certified)==648
# Test the 54 possible single paired queries TARGET-BY-TARGET, rather than
# misusing the aggregate 648 > 36 information bound.
single_certified=set()
for ei in range(6):
    for ci in range(9):
        buckets={}
        for ix,(e,c) in enumerate(micro):
            buckets.setdefault((e[ei],c[ci]),[]).append(ix)
        single_certified.update(group[0] for group in buckets.values() if len(group)==1)
assert not single_certified, 'Some micro targets have one-read certificates'
print('R14_P7_ALL_648_MICRO_STATE_CERTIFICATES_LENGTH_EXACTLY_TWO_PASS')

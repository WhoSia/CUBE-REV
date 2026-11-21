#!/usr/bin/env python3
"""Executable *end-to-end* upper-policy audit for CUBE-REV 0.29.

This is an independent finite proof audit, **not** a Lean theorem. It connects
canonicalization of 11 first edge colors, 8 adaptive reads, final corner parity,
inverse coordinate transport, and actual fixed-probe face-turn execution.
No search engine or exporter is imported, and the frozen policy remains immutable.
"""
import argparse
import hashlib
import json
from pathlib import Path
from random import Random
from itertools import permutations
from collections import Counter

if not __debug__:
    raise RuntimeError('This proof audit uses assertions; Python -O/-OO is forbidden.')

from verify_19_policy_certificate import COLORS, LABELS, assignments, permutation_parity
from audit_r029_w_transport_all_prefixes import (
    symmetries, count_vectors, expected_prefix, permute_vector, relabel_sign,
    CORNERS, corner_pair_decoder,
)
from audit_r029_w_joint_routes import table, follow, composed_path
from audit_r029_w_corner_geometric_decoder import geometry

HERE = Path(__file__).resolve().parent
EXPECTED_SHA = '80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227'
CANONICAL_CORNERS = (0,1, 6,7, 9,10, 18,19, 21,22, 12,13, 3,4)
# Last three fresh corner colors are at frames 12, 13, and 19.
CORNER_SCHEDULE = CANONICAL_CORNERS[:11] + CANONICAL_CORNERS[11:13] + (21,)*5 + CANONICAL_CORNERS[13:]
assert len(CORNER_SCHEDULE) == 19 and len(set(CORNER_SCHEDULE)) == 14


def policy(path):
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED_SHA, digest
    data = json.loads(raw)
    assert data['first_slots'] == 11 and data['remaining_budget'] == 8
    return {r['prefix']:r['nodes'] for r in data['representatives']}


def walk(nodes, word):
    """Return leaf index and complete 8-query (possibly padded) schedule."""
    index = 0
    addresses = []
    for _ in range(8):
        node = nodes[index]
        kind = node[0]
        if kind == 'leaf':
            addresses.append(0)  # legal padding read; ignored by decoder
        elif kind == 'repeat':
            addresses.append(0)
            index = node[1]
        else:
            assert kind == 'read' and 0 <= node[1] < 13
            q = node[1]
            addresses.append(q)
            assert word[q] in node[2], (index,q,word[q])
            index = node[2][word[q]]
    assert nodes[index][0] == 'leaf'
    return index, tuple(addresses)


def leaf_decoder(prefix, nodes):
    leaves = {}
    for word, sign in assignments(prefix):
        leaf,_ = walk(nodes, word)
        key = leaf,sign
        assert key not in leaves, ('same-sign collision',prefix,key)
        leaves[key] = word
    return leaves


def route_info(original, maps, rep):
    counts = tuple(original.count(c) for c in COLORS)
    canonical = min(permute_vector(counts,m) for m in maps)
    m = next(m for m in maps if permute_vector(counts,m)==canonical)
    order = tuple(sorted(range(11),key=lambda i: COLORS.index(m[original[i]])))
    prefix = expected_prefix(canonical)
    assert prefix in rep
    assert ''.join(m[original[i]] for i in order) == prefix
    correction = permutation_parity(order+(11,)) ^ relabel_sign(m)
    inv = {v:k for k,v in m.items()}
    assert len(inv)==6
    return original,prefix,m,inv,order,correction


def forward(word, m,order):
    return ''.join(m[word[i]] for i in order) + ''.join(m[c] for c in word[11:])


def recover(prefix, canonical_word, inv, order):
    originals = ['']*11
    for i,idx in enumerate(order):
        originals[idx] = inv[canonical_word[i]]
    return ''.join(originals) + ''.join(inv[c] for c in canonical_word[11:])


def check_all_orbits(policies, maximal=None, start_vector=0):
    maps = symmetries()
    cache={p:leaf_decoder(p,nodes) for p,nodes in policies.items()}
    assert len(cache)==52
    total=0
    route_counts=Counter()
    corrections=Counter()
    completed_vectors=0
    for vector_index,counts in enumerate(count_vectors()):
        if vector_index < start_vector: continue
        original,rep,m,inv,order,correction = route_info(expected_prefix(counts),maps,policies)
        leaves=cache[rep]
        for word,sign in assignments(original):
            normalized=forward(word,m,order)
            leaf,reads = walk(policies[rep],normalized)
            assert leaves[leaf, sign^correction] == normalized, ('wrong leaf',rep,normalized)
            recovered = recover(original,leaves[leaf,sign^correction],inv,order)
            assert recovered==word, ('wrong inverse', original,word,recovered)
            assert len(reads)==8
            route_counts[len(set(reads))]+=1
            total+=1
        corrections[correction]+=1
        completed_vectors+=1
        if maximal is not None and completed_vectors>=maximal:
            break
    return {'status':'PASS','vectors':completed_vectors,'start_vector':start_vector,'reconstructed_edge_records':total,
            'representatives':len(cache),'edge_read_frames':19,
            'corner_distinct_read_positions':14,
            'canonical_sign_correction_vector_count':dict(sorted(corrections.items())),
            'distinct_read_address_histogram':dict(sorted(route_counts.items()))}


def decode_corners(state, observed):
    """Reconstruct all 24 corner colors from the fourteen actual observations."""
    table = corner_pair_decoder()
    pieces=[]
    orientations=[]
    restored=[]
    for p in (0,2,3,6,7,4,1):
        a,b=(observed[3*p+j] for j in (0,1))
        cubie,twist,word = table[a+b]
        assert cubie not in pieces
        pieces.append(cubie)
        orientations.append(twist)
        restored.append((p,word))
    (remaining,)=set(CORNERS)-set(pieces)
    remaining_twist=(-sum(orientations))%3
    restored.append((5, remaining[remaining_twist:]+remaining[:remaining_twist]))
    bypos=dict(restored)
    corners=''.join(bypos[i] for i in range(8))
    assert corners == ''.join(state[24:]), (corners,''.join(state[24:]))
    orderedpieces=[next(cubie for cubie in CORNERS if frozenset(cubie)==frozenset(bypos[i])) for i in range(8)]
    sign=permutation_parity([CORNERS.index(c) for c in orderedpieces])
    return corners,sign


def check_physical(policies, trials=400):
    """Run all nineteen frames on legal scrambles at the FIXED real probes."""
    maps=symmetries()
    generators=geometry()
    routes=table()
    cached={p:leaf_decoder(p,n) for p,n in policies.items()}
    start=tuple(''.join(LABELS+CORNERS))
    assert len(start)==48
    rng=Random(20261121)
    ccounts=Counter()
    pe,pc=0,21 # DL[1] / DLB[1], two physically fixed probes
    for i in range(trials):
        state=start
        for _ in range(rng.randrange(10,95)):
            t=rng.randrange(12)
            state=tuple(state[generators[t][j]] for j in range(48))
        current=state
        prior=()
        observations={}
        first=[]
        for frame in range(11):
            te=2*frame
            tc=CORNER_SCHEDULE[frame]
            step=composed_path(routes,pe,pc,te,tc,prior)
            current=tuple(current[follow(generators,step,j)] for j in range(48))
            assert current[pe]==state[te] and current[24+pc]==state[24+tc]
            first.append(current[pe]); observations[tc]=current[24+pc]
            prior=tuple((x^1 for x in reversed(routes[24*pe+pc])))+tuple(routes[24*te+tc])
        original=''.join(first)
        counts=tuple(original.count(c) for c in COLORS)
        prefix,rep,m,inv,order,correction=route_info(original,maps,policies)
        assert prefix == original and sorted(original,key=COLORS.index) == list(expected_prefix(counts))
        nodes=policies[rep]
        index=0
        for frame in range(11,19):
            node=nodes[index]
            if node[0]=='leaf':q=0
            elif node[0]=='repeat':
                q=0;index=node[1]
            else:q=node[1]
            te=(2*order[q]+1) if q<11 else 2*11+(q-11)
            tc=CORNER_SCHEDULE[frame]
            step=composed_path(routes,pe,pc,te,tc,prior)
            current=tuple(current[follow(generators,step,j)] for j in range(48))
            assert current[pe] == state[te] and current[24+pc] == state[24+tc]
            observations[tc]=current[24+pc]
            prior=tuple((x^1 for x in reversed(routes[24*pe+pc])))+tuple(routes[24*te+tc])
            if node[0]=='read':
                response=m[current[pe]]
                assert response in node[2],(frame,response,index)
                index=node[2][response]
        assert nodes[index][0]=='leaf'
        corners,original_sign=decode_corners(state,observations)
        recovered_normalized=cached[rep][index,original_sign^correction]
        recovered_second=recover(original,recovered_normalized,inv,order)
        restored_edge=''.join(''.join([first[j],recovered_second[j]]) for j in range(11))+recovered_second[11:]
        assert restored_edge == ''.join(state[:24]),(i,restored_edge,''.join(state[:24]))
        assert corners == ''.join(state[24:])
        ccounts[original_sign]+=1
    return {'status':'PASS','geometric_physical_scrambles':trials,
            'fixed_probes':['DL[1]','DLB[1] (raw slot 45)'],
            'full_48_sticker_reconstructions':trials,
            'corner_parity_counts':dict(sorted(ccounts.items()))}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--certificate',type=Path,required=True)
    p.add_argument('--output',type=Path)
    p.add_argument('--max-vectors',type=int,default=None)
    p.add_argument('--start-vector',type=int,default=0)
    p.add_argument('--physical-trials',type=int,default=400)
    args=p.parse_args()
    policies=policy(args.certificate)
    total=check_all_orbits(policies,args.max_vectors,args.start_vector)
    physical=check_physical(policies,args.physical_trials)
    receipt={'status':'PASS','policy_sha256':EXPECTED_SHA,'all_orbits':total,'physical_replay':physical,
             'scope':'independent exhaustive finite abstract policy audit and randomized end-to-end geometric replay; NOT a universal Lean proof'}
    if args.output:args.output.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(receipt,indent=2,ensure_ascii=False))


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Independent finite negative-control tests for deterministic BN.2 bubble parity.

NOT a Lean proof; uses the same interface but an independent Python model.
"""
from __future__ import annotations
from itertools import permutations
from random import Random

COLORS='BDFLRU'
COLLATION='URFDLB'
EDGES=['DL','BL','FL','UL','DB','DF','UB','UF','DR','BR','FR','UR']
OPPOSITE={'B':'F','F':'B','D':'U','U':'D','L':'R','R':'L'}
EDGE_INDEX={frozenset(x):i for i,x in enumerate(EDGES)}


def parity(seq):
    return sum(a>b for i,a in enumerate(seq) for b in seq[i+1:])%2


def valid_symmetries():
    for images in permutations(COLORS):
        sigma=dict(zip(COLORS,images))
        if all(sigma[OPPOSITE[c]]==OPPOSITE[sigma[c]] for c in COLORS):
            yield sigma


def relabeled_edge_index(sigma,source_id):
    original=EDGES[source_id]
    shifted=''.join(sigma[c] for c in original)
    return EDGE_INDEX[frozenset(shifted)]


def relabel_oriented(sigma,oriented):
    source=oriented//2
    flip=oriented%2
    observed=''.join(sigma[c] for c in EDGES[source][flip:]+EDGES[source][:flip])
    dest=relabeled_edge_index(sigma,source)
    if observed==EDGES[dest]: return 2*dest
    if observed==EDGES[dest][::-1]: return 2*dest+1
    raise AssertionError('invalid gauge-orientation mapping')


def frozen_ranks(sigma,original):
    return [COLLATION.index(sigma[EDGES[x//2][x%2]]) for x in original[:11]]


def bubble_path(ranks):
    assert len(ranks)==11
    ids=list(range(11)); path=[]
    for _ in range(11):
        for i in range(10):
            a,b=ids[i:i+2]
            if (ranks[b],b) <= (ranks[a],a):
                ids[i],ids[i+1]=b,a
                path.append(i)
    return ids,path


def check(sigma,original):
    assert len(original)==12
    assert sorted(x//2 for x in original)==list(range(12))
    labels=[x//2 for x in original]
    edge_relabel=[relabeled_edge_index(sigma,i) for i in range(12)]
    assert sorted(edge_relabel)==list(range(12))
    ranks=frozen_ranks(sigma,original)
    order,path=bubble_path(ranks)
    sorted_order=sorted(range(11),key=lambda i:(ranks[i],i))
    assert order==sorted_order
    assert all(0<=i<10 for i in path)
    assert parity(order)==len(path)%2
    relabeled=[relabel_oriented(sigma,x) for x in original]
    normalized=relabeled[:]
    for i in path:normalized[i],normalized[i+1]=normalized[i+1],normalized[i]
    assert normalized[-1]==relabeled[-1]
    normalized_parity=parity([x//2 for x in normalized])
    corrected=(parity(labels)+parity(edge_relabel)+parity(order))%2
    assert normalized_parity==corrected,(normalized_parity,corrected,sigma,original,path)
    # Stronger: the whole actual bubble path has exactly the expected parity.
    assert parity([x//2 for x in normalized])==(parity(labels)+parity(edge_relabel)+len(path))%2


def main():
    rng=Random(20261123)
    sigmas=list(valid_symmetries())
    assert len(sigmas)==48, len(sigmas)
    test_words=[]
    for _ in range(256):
        perm=list(range(12));rng.shuffle(perm)
        test_words.append([2*x+rng.randrange(2) for x in perm])
    test_words.append([2*i for i in range(12)])
    test_words.append([2*(11-i)+1 for i in range(12)])
    for sigma in sigmas:
        for word in test_words:check(sigma,word)
    print(f'PASS BN.2: {len(sigmas)} center-color gauges × {len(test_words)} complete oriented edge words = {len(sigmas)*len(test_words)} cases')
    print('PASS eleven-pass actual bubble trace, repeated-color stable sorting, fixed twelfth position')
    print('PASS combined induced-edge gauge parity plus stable-slot parity for all tested cases')
    print('CAVEAT: computational testing is not a Lean theorem or a certified exhaustive cube-state proof')

if __name__=='__main__':main()

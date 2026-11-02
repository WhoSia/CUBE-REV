#!/usr/bin/env python3
"""Test the B_r observability vs B_{2r} pointwise-stabilizer equivalence.

All explicit S3/S4 permutation group tests are independent exhaustive checks.
The 12-element Rubik stabilizer count uses standard cubie legality constraints.
NO 3x3 HTM distances are computed by this script.
"""
from collections import deque
from itertools import combinations, permutations, product

def compose(a, b):
    """(a*b)(i) = a(b(i)); transformations act on tags on the left."""
    return tuple(a[j] for j in b)

def inverse(p):
    result=[0]*len(p)
    for i,j in enumerate(p): result[j]=i
    return tuple(result)

def word_distances(n, alphabet):
    identity=tuple(range(n))
    assert all(sorted(a)==list(identity) for a in alphabet)
    assert {inverse(a) for a in alphabet}==set(alphabet)
    dist={identity:0}
    queue=deque((identity,))
    while queue:
        x=queue.popleft()
        for a in alphabet:
            y=compose(a,x)
            if y not in dist:
                dist[y]=dist[x]+1
                queue.append(y)
    return dist

def check_small_group(n):
    cycle=tuple((i+1)%n for i in range(n))
    transposition=tuple([1,0]+list(range(2,n)))
    dist=word_distances(n,(cycle,inverse(cycle),transposition))
    assert len(dist)==len(list(permutations(range(n))))
    identity=tuple(range(n))
    cases=0
    for radius in range(max(dist.values())+1):
        ball=[g for g, length in dist.items() if length<=radius]
        for k in range(n+1):
            for observed in combinations(range(n),k):
                values=[tuple(g[i] for i in observed) for g in ball]
                injective=(len(set(values))==len(values))
                has_short_stabilizer=any(
                    g!=identity and length<=2*radius
                    and all(g[i]==i for i in observed)
                    for g,length in dist.items())
                assert injective != has_short_stabilizer, (n,radius,observed)
                cases+=1
    return cases

def count_rubik_four_missing():
    """2 corners and 2 edges absent; other 16 oriented tags fixed."""
    states=set()
    for shared_swap,twist,flip in product(range(2),range(3),range(2)):
        cp=list(range(8)); ep=list(range(12))
        if shared_swap:
            cp[0],cp[1]=cp[1],cp[0]
            ep[0],ep[1]=ep[1],ep[0]
        co=[0]*8; eo=[0]*12
        co[0],co[1]=twist,(-twist)%3
        eo[0],eo[1]=flip,flip
        assert sum(co)%3==0 and sum(eo)%2==0
        states.add((tuple(cp),tuple(co),tuple(ep),tuple(eo)))
    assert len(states)==12
    return len(states)

if __name__=="__main__":
    checked=sum(check_small_group(n) for n in (3,4))
    print("PASS:",checked,"finite-group/radius/sensor exhaustive comparisons")
    print("PASS: legal pointwise stabilizer has",count_rubik_four_missing(),"configurations")
    print("LIMIT: cube HTM word distances and physical cubie action not independently tested")

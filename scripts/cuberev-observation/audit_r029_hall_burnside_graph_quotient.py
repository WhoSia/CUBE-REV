#!/usr/bin/env python3
"""Independent Hall/Burnside audit of 11-edge color-prefix orbit geometry.

A graph-theoretic support test (Hall matching) and signed-cycle Burnside
classification, cross-checked against independent dynamic programming.
No frozen policy certificate, exporter, search engine or other module imported.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import permutations, combinations
import json

COLORS = 'URFDLB'
EDGES = tuple(map(frozenset, ('DL','BL','FL','UL','DB','DF','UB','UF','DR','BR','FR','UR')))
PAIR_NAMES = ('UD','RL','FB')
OPPOSITES = {frozenset(p) for p in PAIR_NAMES}
EXPECTED = {
    ((1,0),(1,0),(1,0)):(1,1362),
    ((1,0),(1,0),(1,1)):(3,252),
    ((1,0),(1,1),(1,1)):(3,46),
    ((1,0),(2,0)):(6,34),
    ((1,0),(2,1)):(6,6),
    ((1,1),(1,1),(1,1)):(1,0),
    ((1,1),(2,0)):(6,0),
    ((1,1),(2,1)):(6,0),
    ((3,0),):(8,0),
    ((3,1),):(8,0),
}

def graph_check(edges=EDGES):
    assert len(edges)==12 and len(set(edges))==12
    assert all(len(e)==2 and e<=set(COLORS) and e not in OPPOSITES for e in edges)
    assert all(sum(c in e for e in edges)==4 for c in COLORS)

def vectors(total,k):
    if k==1:
        yield (total,)
    else:
        for head in range(total+1):
            for tail in vectors(total-head,k-1):
                yield (head,)+tail

def hall(v,edges=EDGES):
    if len(v)!=6 or min(v)<0 or sum(v)!=11:
        return False
    for mask in range(64):
        subset={c for i,c in enumerate(COLORS) if mask>>i&1}
        if sum(v[i] for i in range(6) if mask>>i&1)>sum(bool(e&subset) for e in edges):
            return False
    return True


def four_hall_families(v):
    """Four irredundant inequality families, using only K_{2,2,2} structure.

    For eleven edge reads, all four-or-more-color Hall cuts are automatic,
    and the same-opposite-pair doubleton cut follows from singleton cuts.
    """
    if len(v)!=6 or min(v)<0 or sum(v)!=11:
        return (False, False, False, False)
    n=dict(zip(COLORS,v))
    singletons=all(n[x]<=4 for x in COLORS)
    nonopposite_pairs=all(n[a]+n[b]<=7
        for a,b in combinations(COLORS,2) if frozenset((a,b)) not in OPPOSITES)
    opposite_pair_plus_one=all(n[a]+n[b]+n[c]<=10
        for pair in PAIR_NAMES for a,b in [tuple(pair)] for c in COLORS if c not in pair)
    one_from_each_pair=all(n[a]+n[b]+n[c]<=9
        for a in PAIR_NAMES[0] for b in PAIR_NAMES[1] for c in PAIR_NAMES[2])
    return (singletons,nonopposite_pairs,opposite_pair_plus_one,one_from_each_pair)

def hall_fast(v):
    return len(v)==6 and min(v)>=0 and sum(v)==11 and all(four_hall_families(v))

def independent_dp():
    all_vectors=set()
    for omitted in EDGES:
        prior={(0,)*6}
        for edge in EDGES:
            if edge==omitted:
                continue
            nxt=set()
            for v in prior:
                for color in edge:
                    new=list(v);new[COLORS.index(color)]+=1;nxt.add(tuple(new))
            prior=nxt
        all_vectors |= prior
    return all_vectors

def group():
    for seq in permutations(COLORS):
        g=dict(zip(COLORS,seq))
        if {frozenset(g[c] for c in pair) for pair in OPPOSITES}==OPPOSITES:
            yield g

def act(g,v):
    result=[0]*6
    for i,color in enumerate(COLORS):
        result[COLORS.index(g[color])]=v[i]
    return tuple(result)

def sign(xs):
    return sum(xs[i]>xs[j] for i in range(len(xs)) for j in range(i+1,len(xs)))%2

def pair_action(g):
    where={c:i for i,p in enumerate(PAIR_NAMES) for c in p}
    return tuple(where[g[p[0]]] for p in PAIR_NAMES)

def edge_action(g):
    return tuple(EDGES.index(frozenset(g[c] for c in edge)) for edge in EDGES)

def signed_cycle(g):
    pair=pair_action(g)
    swap=[int(g[p[0]]==PAIR_NAMES[pair[i]][1]) for i,p in enumerate(PAIR_NAMES)]
    seen=set();cycles=[]
    for i in range(3):
        if i in seen:
            continue
        cyc=[];j=i
        while j not in seen:
            seen.add(j);cyc.append(j);j=pair[j]
        cycles.append((len(cyc),sum(swap[j] for j in cyc)%2))
    return tuple(sorted(cycles))

def verify():
    graph_check()
    universe=list(vectors(11,6))
    assert len(universe)==4368
    supported={v for v in universe if hall(v)}
    reduced={v for v in universe if hall_fast(v)}
    assert len(supported)==1362 and reduced==supported
    # Each of the four cut families is logically necessary; removing it
    # produces exactly these false positives among the 4,368 histograms.
    independent_family_failures=Counter()
    for v in universe:
        checks=four_hall_families(v)
        for idx in range(4):
            if all(flag for j,flag in enumerate(checks) if j!=idx) and not checks[idx]:
                independent_family_failures[idx]+=1
    assert independent_family_failures=={0:468,1:120,2:12,3:72}
    assert independent_dp()==supported, 'Independent omitted-edge DP disagrees with Hall'
    G=list(group())
    assert len(G)==48 and all(all(act(g,v) in supported for v in supported) for g in G)
    assert all(sign(edge_action(g))==sign(pair_action(g)) for g in G)
    classes=defaultdict(list)
    for g in G:
        classes[signed_cycle(g)].append(sum(act(g,v)==v for v in supported))
    assert len(classes)==len(EXPECTED)
    for key,fixes in classes.items():
        assert len(set(fixes))==1 and (len(fixes),fixes[0])==EXPECTED[key]
    assert set(classes)==set(EXPECTED)
    fixed_sum=sum(len(v)*v[0] for v in classes.values())
    assert fixed_sum==2496
    reps={min(act(g,v) for g in G) for v in supported}
    assert len(reps)==fixed_sum//48==52
    orbit=Counter();stabilizer=Counter()
    for rep in reps:
        o=len({act(g,rep) for g in G})
        s=sum(act(g,rep)==rep for g in G)
        assert o*s==48
        orbit[o]+=1;stabilizer[s]+=1
    assert dict(orbit)=={6:3,12:10,24:27,48:12}
    assert dict(stabilizer)=={8:3,4:10,2:27,1:12}
    # Mandatory negative controls: missing graph edge, impossible demand,
    # and a deliberately corrupted fixed-point class must be detected.
    try:
        graph_check(EDGES[:-1])
        raise RuntimeError('Missing-edge graph mutation escaped')
    except AssertionError:
        pass
    assert not hall((4,4,4,0,0,0))
    wrong=dict(EXPECTED);wrong[((1,0),(2,0))]=(6,35)
    assert any((len(rows),rows[0])!=wrong[k] for k,rows in classes.items())
    return {
        'status':'PASS','method':'Hall matching plus Burnside signed-cycle classes',
        'graph':'K_{2,2,2}','edges':12,'first_reads':11,
        'supported_count_vectors':len(supported),'color_symmetries':len(G),
        'all_nonnegative_histograms':len(universe),
        'reduced_hall_family_count':4,
        'reduced_hall_family_independence':dict(sorted(independent_family_failures.items())),
        'signed_cycle_classes':len(classes),'burnside_fix_sum':fixed_sum,
        'orbits':len(reps),'orbit_size_histogram':dict(sorted(orbit.items())),
        'stabilizer_histogram':dict(sorted(stabilizer.items())),
        'class_fixed_counts':[{'signed_cycle_type':list(k),'size':len(classes[k]),
           'fixed':classes[k][0]} for k in sorted(classes)],
        'independent_DP':'PASS','mutations':'REJECTED',
        'edge_sign_formula':'sign(induced 12-edge permutation) = sign(3-pair permutation)',
        'scope':'finite combinatorial audit; NOT the global 19-frame Lean theorem'
    }

if __name__=='__main__':
    assert __debug__, 'Optimized Python discards assertions and is forbidden'
    print(json.dumps(verify(),indent=2,ensure_ascii=False))

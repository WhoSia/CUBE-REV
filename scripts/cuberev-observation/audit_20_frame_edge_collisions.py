#!/usr/bin/env python3
"""Complete 20-frame fixed-color collision audit for legal 48-facelet cubes.

Enumerates all C(24,4)=10,626 missing edge-facelet masks and emits two
distinct legal P48 states having identical observed edge colors and identical
full corners. This proves a nonadaptive, NOT adaptive, frame lower bound.
"""
from collections import Counter
from itertools import combinations, product

FACES = {'U': (0,1,0), 'R': (1,0,0), 'F': (0,0,1),
         'D': (0,-1,0), 'L': (-1,0,0), 'B': (0,0,-1)}
SLOTS = tuple((p,FACES[f]) for p in product((-1,0,1),repeat=3)
              if sum(v!=0 for v in p) in (2,3)
              for f in 'URFDLB' if sum(p[i]*FACES[f][i] for i in range(3))==1)
def det(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))
PIECES={}
for p in sorted({p for p,n in SLOTS}):
    ids=[i for i,(q,n) in enumerate(SLOTS) if q==p]
    if len(ids)==2:
        ids.sort(key=lambda i:0 if abs(SLOTS[i][1][1]) else 1 if abs(SLOTS[i][1][2]) else 2)
    else:
        ids.sort(key=lambda i:0 if abs(SLOTS[i][1][1]) else 1 if abs(SLOTS[i][1][0]) else 2)
        if det(*(SLOTS[i][1] for i in ids))==-1:ids[1],ids[2]=ids[2],ids[1]
    PIECES[p]=tuple(ids)
EDGES=tuple(p for p in PIECES if len(PIECES[p])==2)
CORNERS=tuple(p for p in PIECES if len(PIECES[p])==3)
EDGE_SLOTS=tuple(i for p in EDGES for i in PIECES[p])
U_EDGES=tuple(p for p in EDGES if p[1]==1)
SOURCE_COLOR=tuple(next(f for f,n in FACES.items() if n==normal) for p,normal in SLOTS)
assert len(SLOTS)==48 and len(EDGES)==12 and len(CORNERS)==8 and len(U_EDGES)==4
assert all(SOURCE_COLOR[PIECES[p][0]]=='U' for p in U_EDGES)

def parity(seq):
    return sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))%2

def collision(omitted):
    hidden={p:tuple(i for i in PIECES[p] if i in omitted) for p in EDGES}
    shape=tuple(sorted((len(v) for v in hidden.values() if v),reverse=True))
    assert shape in ((2,2),(2,1,1),(1,1,1,1))
    full=[p for p in EDGES if len(hidden[p])==2]
    partial=[p for p in EDGES if len(hidden[p])==1]
    labels_a={p:p for p in EDGES};labels_b={p:p for p in EDGES}
    flips_a={p:0 for p in EDGES};flips_b={p:0 for p in EDGES}
    if shape==(2,2):
        for p in full:flips_b[p]=1
    else:
        targets=([partial[0],partial[1],full[0]] if full else partial[:3])
        sources=U_EDGES[:3]
        for j,p in enumerate(targets):
            labels_a[p]=sources[j]
            labels_b[p]=sources[(j+1)%3]
        rest_dest=[p for p in EDGES if p not in targets]
        rest_src=[p for p in EDGES if p not in sources]
        for p,s in zip(rest_dest,rest_src):labels_a[p]=labels_b[p]=s
        for p in partial:
            if p not in targets:continue
            read=next(i for i in PIECES[p] if i not in omitted)
            assert labels_a[p] in U_EDGES and labels_b[p] in U_EDGES
            flips_a[p]=flips_b[p]=PIECES[p].index(read)
        adjustable=full[0] if full else next(p for p in EDGES if p not in targets)
        flips_a[adjustable]=sum(flips_a.values())%2
        flips_b[adjustable]=sum(flips_b.values())%2
    assert set(labels_a.values())==set(EDGES) and set(labels_b.values())==set(EDGES)
    assert sum(flips_a.values())%2==sum(flips_b.values())%2==0
    idx={p:i for i,p in enumerate(EDGES)}
    pa=parity([idx[labels_a[p]] for p in EDGES])
    pb=parity([idx[labels_b[p]] for p in EDGES])
    assert pa==pb
    a=[-1]*48;b=[-1]*48
    for p in EDGES:
        for j,src in enumerate(PIECES[labels_a[p]]):a[src]=PIECES[p][(j+flips_a[p])%2]
        for j,src in enumerate(PIECES[labels_b[p]]):b[src]=PIECES[p][(j+flips_b[p])%2]
    corner_labels=list(CORNERS)
    if pa:corner_labels[0],corner_labels[1]=corner_labels[1],corner_labels[0]
    for dest,source in zip(CORNERS,corner_labels):
        for j,src in enumerate(PIECES[source]):
            a[src]=b[src]=PIECES[dest][j]
    assert sorted(a)==sorted(b)==list(range(48)) and a!=b
    ia=[0]*48;ib=[0]*48
    for src,dst in enumerate(a):ia[dst]=src
    for src,dst in enumerate(b):ib[dst]=src
    observed=set(EDGE_SLOTS)-set(omitted)
    assert all(SOURCE_COLOR[ia[s]]==SOURCE_COLOR[ib[s]] for s in observed)
    assert all(a[src]==b[src] for p in CORNERS for src in PIECES[p])
    return shape

def main():
    histogram=Counter()
    for omitted in combinations(EDGE_SLOTS,4):
        histogram[collision(frozenset(omitted))]+=1
    assert histogram=={(2,2):66,(2,1,1):2640,(1,1,1,1):7920}
    print('20_FRAME_FIXED_EDGE_COLLISION_ALL_OMISSIONS_PASS 10626/10626')
    for shape,count in sorted(histogram.items()):
        print('EDGE_OMISSION_PATTERN', '+'.join(map(str,shape)),count)
    from math import factorial
    edge_states_given_corners=factorial(12)*(2**10)
    assert 6**15 < edge_states_given_corners <= 6**16
    print('ADAPTIVE_COLOR_EDGE_ORACLE_INFORMATION_LOWER_16_PASS', edge_states_given_corners, 6**15)
    print('EXACT_NONADAPTIVE_21_LOWER_PASS; adaptive optimum bounded 16..21')

if __name__=='__main__':main()

# R7 oracle upper bound on histories for an adaptive one-edge-color probe.
from functools import lru_cache
@lru_cache(None)
def color_capacity(t,m,p,c):
    if t==0:return 1
    ans=color_capacity(t-1,m,p,c)
    if m<12:
        z=0
        for i,x in enumerate(c):
            if x<4:
                d=list(c);d[i]+=1
                z+=color_capacity(t-1,m+1,p,tuple(sorted(d)))
        ans=max(ans,z)
    if p<m:ans=max(ans,4*color_capacity(t-1,m,p+1,c))
    return ans

def r7_audit():
    from math import factorial
    v=color_capacity(16,0,0,(0,)*6)
    from itertools import product
    from math import prod
    c12=sum(factorial(12)//prod(factorial(x) for x in cs)
            for cs in product(range(5),repeat=6) if sum(cs)==12)
    assert c12==1706720400
    assert v==c12*4**4==436920422400
    assert color_capacity(15,0,0,(0,)*6)==109230105600
    assert color_capacity(17,0,0,(0,)*6)==1747681689600
    assert v<factorial(12)*2**10
    print("R7_ADAPTIVE_COLOR_LOWER_17_PASS",v)

if __name__=='__main__':r7_audit()

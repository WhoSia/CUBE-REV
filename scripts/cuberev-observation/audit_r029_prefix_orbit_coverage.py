#!/usr/bin/env python3
"""Independent exact finite 11-color histogram/orbit coverage audit.

Reconstructs `NineteenReadData.rawWords`, `counts` and 48 color maps
without using the frozen JSON certificate. Does *not* prove that
`matchingFrozenRoot` accepts every original ordered transcript or that
full state-belief membership transports correctly.
"""
from itertools import permutations,product
from collections import defaultdict
EDGES=['DL','BL','FL','UL','DB','DF','UB','UF','DR','BR','FR','UR']
COLORS='BDFLRU'; COLL='URFDLB'
OPPOSITE=dict(B='F',F='B',D='U',U='D',L='R',R='L')
idx={c:i for i,c in enumerate(COLORS)}
codes=[[idx[c] for c in s] for s in EDGES]
coll_codes=[idx[c] for c in COLL]

def counts(v):return tuple(v.count(c) for c in coll_codes)
vec=set()
choices=0
for omitted in range(12):
    keep=[i for i in range(12) if i!=omitted]
    for bits in product([0,1],repeat=11):
        vec.add(counts([codes[i][b] for i,b in zip(keep,bits)]))
        choices+=1
assert choices==24576
assert len(vec)==1362, len(vec)
sym=[]
for images in permutations(COLORS):
    mp=dict(zip(COLORS,images))
    if all(mp[OPPOSITE[c]]==OPPOSITE[mp[c]] for c in COLORS):
        sym.append(tuple(idx[mp[c]] for c in COLORS))
assert len(sym)==48

def action(hist,sigma):
    out=[0]*6
    for color,new in enumerate(sigma):
        out[coll_codes.index(new)]+=hist[coll_codes.index(color)]
    return tuple(out)

classes=defaultdict(list)
for v in sorted(vec):
    orbit_rep=min(action(v,s) for s in sym)
    classes[orbit_rep].append(v)
assert len(classes)==52, len(classes)
assert sum(map(len,classes.values()))==1362
assert set(k for k in classes)==set(classes.keys())
for representative, members in classes.items():
    assert set(members)==set(action(representative,s) for s in sym)
    assert len(members)*sum(action(representative,s)==representative for s in sym)==48

# Full signed-histogram orbit classification; correction = induced twelve-edge
# relabel sign + stable eleven-slot color block-sort sign.
try:
    from audit_r029_executable_bubble_sign import relabeled_edge_index, parity
except ModuleNotFoundError:
    from check_executable_bubble_sign import relabeled_edge_index, parity
unsafe=0
signed_orbits=0
for rep in classes:
    color_counts={COLL[i]:rep[i] for i in range(6)}
    sign_unsafe=False
    for s in sym:
        if action(rep,s)!=rep:continue
        name_sigma=dict(zip(COLORS,(COLORS[x] for x in s)))
        char=parity([relabeled_edge_index(name_sigma,i) for i in range(12)])
        inv=0
        for i,a in enumerate(COLL):
            for b in COLL[i+1:]:
                if COLL.index(name_sigma[a])>COLL.index(name_sigma[b]):
                    inv+=color_counts[a]*color_counts[b]
        if (char+inv)%2:sign_unsafe=True
    unsafe+=int(sign_unsafe)
    signed_orbits+=(1 if sign_unsafe else 2)
assert unsafe==24,(unsafe,signed_orbits)
assert signed_orbits==80,signed_orbits
print('PASS 12 omitted-edge choices × 2^11 first-color assignments = 24576 raw configurations')
print(f'PASS {len(vec)} distinct feasible 11-color histograms; {len(classes)} orbits under 48 legal color maps')
print(f'PASS combined position+gauge parity: {unsafe} unsafe stabilizer orbits; {signed_orbits} signed histogram orbits')
print('CAVEAT: histogram coverage does not prove ordered-prefix root matching nor statewise membership')

#!/usr/bin/env python3
"""R14-P8.13: complete inclusion-wise minimal B6 sensor-size spectrum.

The structural geometry is independently coded here from six coordinate
face normals. No imports from existing cube project checker modules.

**Conditional theorem:** 16-tag B6-positive classification (156 layouts)
and its complete 4845-set physical negative court are inherited, as are
the short triple-edge and nonadjacent-corner collision certificates.
This executable checks their finite geometry CONSEQUENCES; it does not
rerun any 18-HTM word-metric physical distance proof.
"""
from collections import Counter
from itertools import combinations, product
import json

FACES = {"U":(0,1,0),"R":(1,0,0),"F":(0,0,1),
         "D":(0,-1,0),"L":(-1,0,0),"B":(0,0,-1)}
EDGES = ("UR","UF","UL","UB","DR","DF","DL","DB","FR","FL","BL","BR")
CORNERS = tuple(product((-1,1),repeat=3))
def midpoint(name):
    return tuple(FACES[name[0]][i]+FACES[name[1]][i] for i in range(3))
def endpoints(edge):
    m=midpoint(edge)
    i=m.index(0)
    return frozenset(tuple(v if j!=i else z for j,v in enumerate(m))
                     for z in (-1,1))
ENDS = {e:endpoints(e) for e in EDGES}
C = frozenset(("C",p) for p in CORNERS)
E = frozenset(("E",p) for p in EDGES)
OMEGA = C|E

def allowed(h,a,b):
    assert a!=b
    co=ENDS[h]
    opposite=frozenset(tuple(-v for v in p) for p in co)
    other=next(e for e in EDGES if ENDS[e]==opposite)
    near={e for e in EDGES if e!=h and bool(ENDS[e]&co)}
    far={e for e in EDGES if e!=other and bool(ENDS[e]&opposite)}
    parallel={e for e in EDGES if midpoint(e).index(0)==midpoint(h).index(0)
              and e not in (h,other)}
    first=sorted(co)[0]
    return ((a in near and b in near and ((first in ENDS[a])!=(first in ENDS[b])))
            or (a in far and b in far and bool(set(a)&set(b)))
            or (a==other and b in far) or (b==other and a in far)
            or ({a,b}==parallel))

PAIRS={h:frozenset(frozenset((a,b)) for a,b in combinations(EDGES,2)
                       if allowed(h,a,b)) for h in EDGES}
assert all(len(v)==13 for v in PAIRS.values())

# Exactly one or more physically B6-positive size-16 core pairs for
# EVERY one of the 66 possible omitted-edge pairs. This allows all
# 1C+2E 17-tag positives to be proven by pure stabilizer inclusion.
pair_multiplicity=Counter()
for a,b in combinations(EDGES,2):
    pair=frozenset((a,b))
    pair_multiplicity[sum(pair in PAIRS[h] for h in EDGES)]+=1
assert sum(pair_multiplicity.values())==66
assert pair_multiplicity=={1:24,2:6,3:24,4:12}
assert 0 not in pair_multiplicity

positive16=frozenset(frozenset({("C",p) for p in ENDS[h]}|
                    {("E",e) for e in pair})
                    for h in EDGES for pair in PAIRS[h])
assert len(positive16)==156
assert len(OMEGA)==20

def adjacent(corner_set):
    return any(ENDS[h]==corner_set for h in EDGES)

# The predicates for >=17 observed sensors are consequences of legal
# whole-cubie stabilizers AND historically certified short support
# obstructions; their validity is not obtained by assuming every
# three-omission pattern has a valid 16-omission extension.
def identifying_omissions(omitted):
    co=frozenset(p for typ,p in omitted if typ=="C")
    ee=frozenset(p for typ,p in omitted if typ=="E")
    if len(omitted)==4:
        return omitted in positive16
    if len(omitted)==3:
        return ((len(co)==2 and len(ee)==1 and adjacent(co))
                or (len(co)==1 and len(ee)==2))
    if len(omitted)==2:
        return len(co)<2 or adjacent(co)
    if len(omitted)<=1:
        return True
    raise ValueError("This gate only classifies layouts with >=16 observed tags")

def positive_set(k):
    return frozenset(frozenset(q) for q in combinations(OMEGA,k)
                     if identifying_omissions(frozenset(q)))

P={k:positive_set(k) for k in range(5)}
assert [len(P[k]) for k in range(5)]==[1,20,174,672,156]
# Each B6 positive 17 must remain positive upon adding an observed tag.
for omitted in P[3]:
    for tag in omitted:
        assert omitted-{tag} in P[2]
# Minimal identifying sensor designs correspond to MAXIMAL allowed
# omissions: there is no identifying immediate superset of the omitted set.
minimal={}
for k in range(5):
    minimal[k]=frozenset(q for q in P[k] if
        not any(q|{tag} in P.get(k+1,frozenset())
                for tag in OMEGA-q))
assert {k:len(minimal[k]) for k in range(5)}=={0:0,1:0,2:0,3:276,4:156}

# Split the 276 genuine minimal-17 layouts into two geometrically
# distinguishable strata.
hist=Counter()
for q in minimal[3]:
    hist[(sum(t=="C" for t,_ in q),sum(t=="E" for t,_ in q))]+=1
assert hist=={(2,1):12,(1,2):264}
assert 156+276==432
assert all(not any(a<b for a in minimal[3] for b in minimal[4]) for _ in (0,))

print(json.dumps({
    "status":"R14_P813_COMPLETE_MINIMAL_B6_SIZE_SPECTRUM_GEOMETRIC_PASS",
    "proof_dependency":"inherited 156 positive+4689 negative physical 16-sensor certificates and short-support obstructions",
    "positive_observation_count":{"16":156,"17":672,"18":174,"19":20,"20":1},
    "minimal_identifying_count":{"16":156,"17":276,"18":0,"19":0,"20":0},
    "minimal_17_types":{"two_corners_one_edge":12,"one_corner_two_edges":264},
    "total_minimal":432,"minimal_size_spectrum":[16,17],
    "edge_pair_core_coverage":dict(sorted(pair_multiplicity.items())),
    "fresh_independent_physical_18htm_mitm":False,
    "lean_kernel_verdict":"NOT_RUN_BY_THIS_SCRIPT"
},sort_keys=True))

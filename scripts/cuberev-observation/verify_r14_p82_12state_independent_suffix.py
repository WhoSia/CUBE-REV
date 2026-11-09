#!/usr/bin/env python3
"""Independent 12-state parity-matched suffix enumeration and literal query profiles.
Read saved P8.2 digest; no imports of its DP, graph or state transition code.
"""
import json,hashlib
from itertools import product
from pathlib import Path
H=Path(__file__).resolve().parent
z=json.loads((H/'R14_P82_MIXED_P48_SUCCESSOR_PARTITIONS_RECEIPT.json').read_text())
row=next(r for r in z['prefixes'] if r['prefix']=='ten_edge_six_corner_completed')
# Cube source labels in 3D P5.1 spatial coordinate ordering, derived from
# face normals via independent deterministic cubic lattice generation.
from itertools import product as cart
F={'U':(0,1,0),'D':(0,-1,0),'R':(1,0,0),'L':(-1,0,0),'F':(0,0,1),'B':(0,0,-1)}
order='URFDLB'
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
slots=tuple((p,F[f]) for p in cart((-1,0,1),repeat=3) if sum(x!=0 for x in p) in (2,3) for f in order if dot(p,F[f])==1)
S={x:i for i,x in enumerate(slots)}
pieces={}
for p in sorted({p for p,n in slots}):
    ids=[S[(p,n)] for n in F.values() if dot(p,n)==1]
    if len(ids)==2:ids.sort(key=lambda i:0 if abs(slots[i][1][1]) else 1 if abs(slots[i][1][2]) else 2)
    else:
        ids.sort(key=lambda i:0 if abs(slots[i][1][1]) else 1 if abs(slots[i][1][0]) else 2)
        if det(*(slots[i][1] for i in ids))==-1:ids[1],ids[2]=ids[2],ids[1]
    pieces[p]=tuple(ids)
E=tuple(p for p in sorted(pieces) if len(pieces[p])==2)
C=tuple(p for p in sorted(pieces) if len(pieces[p])==3)
face={i:next(f for f,n in F.items() if n==slots[i][1]) for i in range(48)}
e=tuple(''.join(face[j] for j in pieces[p]) for p in E)
c=tuple(''.join(face[j] for j in pieces[p]) for p in C)
assert len(e)==12 and len(c)==8
# Constrain the first 10 E and first 6 C to their solved labels and orientation.
# Suffix permutations use same odd/even permutation parity; the pair twists
# sum to zero modulo their sector arity.
X=[]
for sign, a, b in product((0,1),range(2),range(3)):
    ee=e[:10]+tuple(e[10+ (j^sign)][(s+ (a if j==0 else -a))%2] for j in range(2) for s in range(2))
    cc=c[:6]+tuple(c[6+ (j^sign)][(s+ (b if j==0 else -b))%3] for j in range(2) for s in range(3))
    # Above mixes a tuple of strings with 4/6 char strings. Rebuild literal chars.
    edge=''.join(e[:10])+''.join(ee[10:])
    corner=''.join(c[:6])+''.join(cc[6:])
    assert len(edge)==24 and len(corner)==24
    X.append((edge,corner))
assert len(X)==12 and len(set(X))==12
profiles=[]
for qi,qj in product(range(24),repeat=2):
    groups={}
    for edge,corner in X:
        pair=edge[qi]+corner[qj]
        groups[pair]=groups.get(pair,0)+1
    profiles.append(sorted(groups.values(),reverse=True))
dig=hashlib.sha256(json.dumps(profiles,separators=(',',':')).encode()).hexdigest()
assert dig==row['partition_sha256'],(dig,row['partition_sha256'])
assert min(max(x) for x in profiles)==row['best_max_child']==2
assert sum(1 for r in profiles if max(r)==2)==row['max_child_tied_actions']
receipt={'result':'R14_P82_INDEPENDENT_12STATE_ALL_576_PHYSICAL_PARTITIONS_PASS',
         'independently_enumerated_legal_suffix_states':12,
         'all_action_signatures':576,'checked_literal_color_outputs':6912,
         'partition_sha256':dig,
         'min_worst_child':2,
         'scope':'P5.1 lattice sticker ordering independently reconstructed; exact 10E6C solved-prefix 12-state conditional suffix only; not full 20-frame Bellman.'}
(H/'R14_P82_INDEPENDENT_12STATE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['result'],dig)

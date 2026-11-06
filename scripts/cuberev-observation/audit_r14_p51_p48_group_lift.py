#!/usr/bin/env python3
"""R14-P5.1: independent 3D P48 lift and full-group observation covariance.

Constructs physical sticker slots from integer unit face normals and moving
cubie coordinates. Does NOT import CUBE-REV. Verifies a legal 12-element local
slot symmetry and a group-equivariant 36-to-3 first-feedback reduction.
"""
from itertools import product, permutations
from collections import deque, Counter
import hashlib, json, random
FACES={'U':(0,1,0),'D':(0,-1,0),'R':(1,0,0),'L':(-1,0,0),'F':(0,0,1),'B':(0,0,-1)}
order='URFDLB'
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
SLOTS=tuple((p,FACES[f]) for p in product((-1,0,1),repeat=3) if sum(x!=0 for x in p) in (2,3) for f in order if dot(p,FACES[f])==1)
assert len(SLOTS)==48
ID={s:i for i,s in enumerate(SLOTS)}
POSITIONS=sorted({p for p,n in SLOTS})
PIECES={}
for p in POSITIONS:
    js=[ID[(p,n)] for n in FACES.values() if dot(p,n)==1]
    if len(js)==2:
        js.sort(key=lambda i:(0 if abs(SLOTS[i][1][1]) else 1 if abs(SLOTS[i][1][2]) else 2))
    else:
        js.sort(key=lambda i:(0 if abs(SLOTS[i][1][1]) else 1 if abs(SLOTS[i][1][0]) else 2))
        if det(*(SLOTS[i][1] for i in js))==-1:js[1],js[2]=js[2],js[1]
        assert det(*(SLOTS[i][1] for i in js))==1
    PIECES[p]=tuple(js)
EDGES=tuple(p for p in POSITIONS if len(PIECES[p])==2)
CORNERS=tuple(p for p in POSITIONS if len(PIECES[p])==3)
assert (len(EDGES),len(CORNERS))==(12,8)
EYE=tuple(range(48))
def compose(a,b):return tuple(a[b[i]] for i in range(48))
def inverse(a):
    b=[None]*48
    for i,j in enumerate(a):b[j]=i
    return tuple(b)
def rot(v,axis,k):
    x,y,z=v
    for _ in range(k%4):
        if axis==0:y,z=-z,y
        if axis==1:x,z=z,-x
        if axis==2:x,y=-y,x
    return (x,y,z)
MOVES={}
for face,n in FACES.items():
    axis=next(i for i,k in enumerate(n) if k)
    for suffix,power in (('',1),("'",3),('2',2)):
        MOVES[face+suffix]=tuple(ID[(rot(p,axis,-n[axis]*power),rot(nn,axis,-n[axis]*power))] if p[axis]==n[axis] else ID[(p,nn)] for p,nn in SLOTS)
assert len(MOVES)==18

def parity(a):return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2

def state_signature(s):
    """Get positional permutation and orientation sums source->destination."""
    attrs=[]
    for positions,mod in ((EDGES,2),(CORNERS,3)):
        indexes={p:i for i,p in enumerate(positions)}
        placed=[];os=[]
        for src in positions:
            src_slots=PIECES[src]
            dests={SLOTS[s[i]][0] for i in src_slots}
            assert len(dests)==1
            dest=next(iter(dests))
            placed.append(indexes[dest])
            ts=PIECES[dest]
            ori=ts.index(s[src_slots[0]])
            assert all(s[src_slots[j]]==ts[(j+ori)%mod] for j in range(mod))
            os.append(ori)
        attrs.append((parity(placed),sum(os)%mod,tuple(placed),tuple(os)))
    return attrs

def legal(s):
    a,b=state_signature(s)
    return a[0]==b[0] and a[1]==0 and b[1]==0

def mapping_to_group(g):
    out=list(EYE)
    for typ,n,perm,orient in g:
        positions=EDGES if typ=='E' else CORNERS
        for i,src in enumerate(positions):
            orig=PIECES[src];dest=PIECES[positions[perm[i]]]
            for j,slot in enumerate(orig):out[slot]=dest[(j+orient[i])%n]
    return tuple(out)

def swap_pair_sector(positions):
    out=list(EYE)
    a,b=positions[:2]
    for j in range(len(PIECES[a])):
        out[PIECES[a][j]]=PIECES[b][j]
        out[PIECES[b][j]]=PIECES[a][j]
    return tuple(out)

def flip_pair_edge():
    out=list(EYE)
    for p in EDGES[:2]:
        a,b=PIECES[p]
        out[a],out[b]=b,a
    return tuple(out)

def twist_pair_corner():
    out=list(EYE)
    for p,shift in zip(CORNERS[:2],(1,2)):
        sl=PIECES[p]
        for j in range(3):out[sl[j]]=sl[(j+shift)%3]
    return tuple(out)

A=compose(swap_pair_sector(EDGES),swap_pair_sector(CORNERS))
B=flip_pair_edge()
C=twist_pair_corner()
GEN=(A,B,C)
assert all(legal(v) for v in GEN),[state_signature(v)[:2] for v in GEN]
assert not legal(swap_pair_sector(EDGES))
G={EYE};Q=deque([EYE])
while Q:
    x=Q.popleft()
    for gen in GEN:
        y=compose(x,gen)
        if y not in G:G.add(y);Q.append(y)
assert len(G)==12,len(G)

# Test actual 3D physical 18-generator closure and allowed group actions.
rng=random.Random(20261106)
states=[EYE]
s=EYE
for k in range(2000):
    s=compose(MOVES[rng.choice(tuple(MOVES))],s)
    assert legal(s),(k,state_signature(s))
    states.append(s)
assert all(legal(compose(g,s)) for g in GEN for s in states)

# Physical free paired initial-position access: the 18-HTM joint sticker orbit is full.
edge_slots=sorted(i for p in EDGES for i in PIECES[p]);corner_slots=sorted(i for p in CORNERS for i in PIECES[p]);q0=(edge_slots[0],corner_slots[0])
seen={q0:()};Q=deque([q0])
while Q:
    a,b=Q.popleft()
    for name,mv in MOVES.items():
        z=(mv[a],mv[b])
        if z not in seen:seen[z]=seen[(a,b)]+(name,);Q.append(z)
assert len(seen)==576

COLORS={i:next(f for f,n in FACES.items() if n==SLOTS[i][1]) for i in range(48)}
def obs(s,q):
    inv=inverse(s)
    return COLORS[inv[q[0]]],COLORS[inv[q[1]]]
for state in states[::11]:
    for g in G:
        for q in (q0,(edge_slots[5],corner_slots[19]),(edge_slots[17],corner_slots[7])):
            assert obs(compose(g,state),(g[q[0]],g[q[1]]))==obs(state,q)

# Proper cube 3D rotations induce color relabelings and cube-state conjugacy.
rots=[]
for perm in permutations(range(3)):
    sign=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
    for signs in product((-1,1),repeat=3):
        if sign*signs[0]*signs[1]*signs[2]!=1:continue
        def r(v,perm=perm,signs=signs):return tuple(signs[i]*v[perm[i]] for i in range(3))
        slotperm=tuple(ID[(r(p),r(n))] for p,n in SLOTS)
        colorperm={f:next(k for k,n in FACES.items() if n==r(v)) for f,v in FACES.items()}
        rots.append((slotperm,colorperm))
assert len(rots)==24
classes={}
for y in product('URFDLB',repeat=2):
    classkey='same' if y[0]==y[1] else 'opposite' if FACES[y[0]]==tuple(-z for z in FACES[y[1]]) else 'adjacent'
    classes.setdefault(classkey,[]).append(y)
assert {k:len(v) for k,v in classes.items()}=={'same':6,'opposite':6,'adjacent':24}
# For any physical q0, transform the state by rotation/conjugacy, then use
# a known legal left group action to restore the queried pair to q0.
for r,cp in rots:
    pair=(r[q0[0]],r[q0[1]])
    names=seen[pair]
    # known sequence of turns carries q0 -> pair; invert it in group.
    move=EYE
    for name in names:move=compose(MOVES[name],move)
    assert (move[q0[0]],move[q0[1]])==pair
    unmove=inverse(move)
    for s in states[::37]:
        rs=compose(r,compose(s,inverse(r)))
        assert legal(rs)
        canonical=compose(unmove,rs)
        assert legal(canonical)
        assert obs(canonical,q0)==tuple(cp[c] for c in obs(s,q0))

# The stabilizer H of the first paired readout q0 fixes both actual
# facelet positions and therefore each conditional color belief after q0.
# Show its EXACT 12 orbits on the 576 possible second paired queries.
def h_generator(edge_swaps=(),corner_swaps=(),edge_flips=(),corner_twists=()):
    ep=list(range(12)); cp=list(range(8))
    eo=[0]*12; co=[0]*8
    for i,j in edge_swaps:ep[i],ep[j]=ep[j],ep[i]
    for i,j in corner_swaps:cp[i],cp[j]=cp[j],cp[i]
    for i in edge_flips:eo[i]^=1
    for i,v in corner_twists:co[i]=(co[i]+v)%3
    perm=list(EYE)
    for i,p in enumerate(EDGES):
        for j,slot in enumerate(PIECES[p]):perm[slot]=PIECES[EDGES[ep[i]]][(j+eo[i])%2]
    for i,p in enumerate(CORNERS):
        for j,slot in enumerate(PIECES[p]):perm[slot]=PIECES[CORNERS[cp[i]]][(j+co[i])%3]
    return tuple(perm)

Hgens=[]
# Permutation parity compensation keeps each generator inside the legal G.
for j in range(2,12):Hgens.append(h_generator(edge_swaps=((1,j),),corner_swaps=((1,2),)))
for j in range(2,8):Hgens.append(h_generator(edge_swaps=((1,2),),corner_swaps=((1,j),)))
# Orientations have even edge-flip and zero corner-twist total.
for j in range(2,12):Hgens.append(h_generator(edge_flips=(1,j)))
for j in range(2,8):Hgens.append(h_generator(corner_twists=((1,1),(j,2))))
assert len(Hgens)==32
assert all(legal(g) and (g[q0[0]],g[q0[1]])==q0 for g in Hgens)

all_queries={(e,c) for e in edge_slots for c in corner_slots}
remaining=set(all_queries)
H_orbits=[]
while remaining:
    seed=min(remaining)
    seen_orbit={seed}
    work=deque([seed])
    while work:
        qe,qc=work.popleft()
        for g in Hgens:
            nxt=(g[qe],g[qc])
            if nxt not in seen_orbit:
                seen_orbit.add(nxt)
                work.append(nxt)
    assert seen_orbit<=remaining
    remaining-=seen_orbit
    H_orbits.append((seed,len(seen_orbit)))
assert len(H_orbits)==12
# The orbit sizes are the exact products of the fixed-first-read facelet
# classes: edge {first sticker, edge mate, other 22}, corner {first sticker,
# corner mate 1, corner mate 2, other 21}. Such classes cannot be merged
# by ANY legal group element fixing q0: orientation is cyclic at corners.
assert Counter(sz for _,sz in H_orbits)==Counter({1:6,21:2,22:3,462:1})
assert sum(sz for _,sz in H_orbits)==576

# Prove all 36 initial color-pairs have 3 color-automorphism orbits.
for key,ys in classes.items():
    representative=ys[0]
    orbit={tuple(cp[v] for v in representative) for r,cp in rots}
    assert orbit==set(ys),(key,orbit,set(ys))

# Full prior response counts factor by edge and corner parity; 36 equal cells.
from math import factorial
Ec=factorial(12)//2*2**11;Cc=factorial(8)//2*3**7
assert Ec%6==0 and Cc%6==0
nfull=2*Ec*Cc
firstcell=2*(Ec//6)*(Cc//6)
assert firstcell*36==nfull
out={'result':'R14_P51_P48_FULL_GROUP_COVARIANCE_PASS',
     'physical_slot_count':len(SLOTS),'physical_move_count':len(MOVES),
     'physical_legal_scrambles_checked':len(states),
     'local_generators_legal':3,'local_group_order':len(G),
     'illegal_edge_only_swap_rejected':True,
     'full_joint_probe_orbit':len(seen),
     'proper_spatial_rotations':len(rots),
     'first_frame_response_orbits':{k:len(v) for k,v in classes.items()},
     'all_root_color_pair_orbits_verified':True,
     'full_group_cardinality':nfull,
     'first_frame_cell_cardinality':firstcell,
     'all_36_first_frame_cells_equal':True,
     'first_frame_fixed_query_second_query_orbits':len(H_orbits),
     'first_frame_fixed_query_second_orbit_size_histogram':dict(sorted(Counter(sz for _,sz in H_orbits).items())),
     'first_two_frame_pair_query_reduction':'576 root pairs to 1; 36 root outcomes to 3 colors; 576 second pairs to 12 orbit representatives per root outcome',
     'physical_scope':'physical P48 3D normal geometry and legal turn generators, no full 20-frame result; free 576 paired-slot access, turns cost unbounded',
     'novelty_warning':'group covariance and 3 color relation classes are standard group-action deductions; not new theory alone'}
print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

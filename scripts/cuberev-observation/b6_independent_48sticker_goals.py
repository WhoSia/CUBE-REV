#!/usr/bin/env python3
"""Source-independent B6 P48 stabilizer-goal enumerator.

Physical sticker slots are generated from 3D positions and unit normals.
No historical 54-facelet moves, precomputed B6-goal records or positivity
flags are imported. This verifies goal geometry, NOT HTM distance >= 13.
"""
from collections import Counter
from itertools import combinations, permutations, product

FACES = {"U":(0,1,0),"R":(1,0,0),"F":(0,0,1),
         "D":(0,-1,0),"L":(-1,0,0),"B":(0,0,-1)}
EDGE_NAMES = ("UR","UF","UL","UB","DR","DF","DL","DB","FR","FL","BL","BR")

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def det(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

SLOTS = tuple((p,FACES[f]) for p in product((-1,0,1),repeat=3)
              if sum(v!=0 for v in p) in (2,3)
              for f in "URFDLB" if dot(p,FACES[f])==1)
assert len(SLOTS)==len(set(SLOTS))==48
SLOT_ID={slot:i for i,slot in enumerate(SLOTS)}

def make_cubies():
    cubies={}
    for p in set(p for p,n in SLOTS):
        ids=[SLOT_ID[(p,n)] for n in FACES.values() if dot(p,n)==1]
        if len(ids)==3:
            ids.sort(key=lambda i:0 if abs(SLOTS[i][1][1])==1 else 1 if abs(SLOTS[i][1][0])==1 else 2)
            if det(*(SLOTS[i][1] for i in ids))==-1:
                ids[1],ids[2]=ids[2],ids[1]
            assert det(*(SLOTS[i][1] for i in ids))==1
        else:
            assert len(ids)==2
            ids.sort(key=lambda i:0 if abs(SLOTS[i][1][1])==1 else 1 if abs(SLOTS[i][1][2])==1 else 2)
        cubies[p]=tuple(ids)
    return cubies

PIECES=make_cubies()
CORNERS=tuple(sorted(p for p in PIECES if len(PIECES[p])==3))
EDGE_POS=tuple(sorted(p for p in PIECES if len(PIECES[p])==2))
assert (len(CORNERS),len(EDGE_POS))==(8,12)
EDGE_POSITION={e:tuple(FACES[e[0]][i]+FACES[e[1]][i] for i in range(3)) for e in EDGE_NAMES}
assert set(EDGE_POSITION.values())==set(EDGE_POS)

def spatial():
    out=[]
    for perm in permutations(range(3)):
        parity=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        for signs in product((-1,1),repeat=3):
            def R(v,perm=perm,signs=signs):
                return tuple(signs[i]*v[perm[i]] for i in range(3))
            p=bytes(SLOT_ID[(R(v),R(n))] for v,n in SLOTS)
            out.append((parity*signs[0]*signs[1]*signs[2],p,R))
    assert len(out)==48 and len({p for _,p,_ in out})==48
    return out
SPATIAL=spatial()

def inverse(s):
    out=[0]*48
    for i,j in enumerate(s):out[j]=i
    return bytes(out)
def compose(a,b):
    return bytes(a[b[i]] for i in range(48))
def conjugate(s,p):
    return compose(p,compose(s,inverse(p)))

def rotate(v,axis,k):
    x,y,z=v
    for _ in range(k%4):
        if axis==0:y,z=-z,y
        elif axis==1:x,z=z,-x
        else:x,y=-y,x
    return x,y,z

def moves():
    result={}
    for face,n in FACES.items():
        ax=next(i for i,v in enumerate(n) if v)
        for suffix,power in (("",1),("'",3),("2",2)):
            data=[]
            for p,normal in SLOTS:
                if p[ax]==n[ax]:
                    p=rotate(p,ax,-n[ax]*power)
                    normal=rotate(normal,ax,-n[ax]*power)
                data.append(SLOT_ID[(p,normal)])
            result[face+suffix]=bytes(data)
    assert len(result)==18
    return result
MOVES=moves()

def word(s):
    result=bytes(range(48))
    for token in s.split():
        result=compose(MOVES[token],result)
    return result

def edge_ends(edge):
    m=EDGE_POSITION[edge]
    return frozenset(p for p in CORNERS if all(p[i]==m[i] for i in range(3) if m[i]!=0))

def valid_pairs(core):
    center=EDGE_POSITION[core]
    opposite=next(e for e in EDGE_NAMES if EDGE_POSITION[e]==tuple(-x for x in center))
    ends=edge_ends(core)
    opposite_ends=edge_ends(opposite)
    near={e for e in EDGE_NAMES if e!=core and edge_ends(e)&ends}
    far={e for e in EDGE_NAMES if e!=opposite and edge_ends(e)&opposite_ends}
    parallel={e for e in EDGE_NAMES if EDGE_POSITION[e].index(0)==center.index(0) and e not in (core,opposite)}
    anchor=min(ends)
    result=set()
    for a,b in combinations(EDGE_NAMES,2):
        accept=(
            (a in near and b in near and ((anchor in edge_ends(a))!=(anchor in edge_ends(b))))
            or (a in far and b in far and bool(set(a)&set(b)))
            or (a==opposite and b in far)
            or (b==opposite and a in far)
            or ({a,b}==parallel)
        )
        if accept:result.add(frozenset((a,b)))
    assert len(result)==13
    return result

def layout_orbits():
    all_pairs={(e,p) for e in EDGE_NAMES for p in valid_pairs(e)}
    assert len(all_pairs)==156
    inverse_edge={p:e for e,p in EDGE_POSITION.items()}
    remaining=set(all_pairs)
    result=[]
    while remaining:
        e,pair=min(remaining,key=lambda item:(EDGE_NAMES.index(item[0]),tuple(sorted(item[1]))))
        orbit=set()
        for sign,p,R in SPATIAL:
            if sign!=1:continue
            orbit.add((inverse_edge[R(EDGE_POSITION[e])],
                       frozenset(inverse_edge[R(EDGE_POSITION[x])] for x in pair)))
        assert orbit<=remaining
        remaining-=orbit
        result.append(orbit)
    assert len(result)==8
    assert sorted(map(len,result))==[12,12,12,24,24,24,24,24]
    return result

def target(core,missing_edges,sw,tw,fl):
    absent_c=sorted(edge_ends(core))
    absent_e=sorted(EDGE_POSITION[e] for e in missing_edges)
    s=list(range(48))
    for (x,y),swap,twist,mod in ((absent_c,sw,tw,3),(absent_e,sw,fl,2)):
        first,second=PIECES[x],PIECES[y]
        for i in range(mod):
            s[first[i]]=(second if swap else first)[(i+twist)%mod]
            s[second[i]]=(first if swap else second)[(i-twist)%mod]
    result=bytes(s)
    assert sorted(result)==list(range(48))
    return result

def generate():
    targets=[]
    for orbit in layout_orbits():
        h,pair=min(orbit,key=lambda x:(EDGE_NAMES.index(x[0]),tuple(sorted(x[1]))))
        for swap,twist,flip in product(range(2),range(3),range(2)):
            if (swap,twist,flip)!=(0,0,0):
                targets.append(target(h,pair,swap,twist,flip))
    assert len(targets)==88
    states=set(targets)
    assert len(states)==74
    remaining=set(states)
    classes=[]
    while remaining:
        seed=min(remaining)
        orbit={conjugate(seed,p) for sign,p,R in SPATIAL}
        orbit|={inverse(state) for state in tuple(orbit)}
        contained=orbit&states
        remaining-=contained
        classes.append(contained)
    assert len(classes)==41
    assert Counter(map(len,classes))==Counter({1:17,2:19,3:1,4:4})
    return targets,states,classes

def audit():
    eye=bytes(range(48))
    for token,m in MOVES.items():
        inv=token if token.endswith("2") else token[:-1] if token.endswith("'") else token+"'"
        assert compose(m,MOVES[inv])==eye
    one=set(MOVES.values())
    for sign,p,R in SPATIAL:
        for move in MOVES.values():
            assert conjugate(move,p) in one
    known="L F R' F' L' U2 R U R U' R2 U2 R"
    assert word(known)==target("DL",frozenset(("UF","UR")),0,0,1)
    goals,states,classes=generate()
    print("PASS P48 18 HTM, 864 generator conjugation checks, known physical 13-HTM control")
    print("PASS 156 geometrical layouts, 8 proper-rotation layout orbits")
    print("PASS 88 nonidentity goal entries, 74 unique full states, 41 classes")
    print("PASS class size histogram:",dict(sorted(Counter(map(len,classes)).items())))
    print("LIMIT: no radius-six MITM distance or historical B6-positive uniqueness checked")
    return goals,states,classes

if __name__=="__main__":
    audit()

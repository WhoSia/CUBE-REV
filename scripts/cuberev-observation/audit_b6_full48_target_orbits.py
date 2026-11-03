#!/usr/bin/env python3
"""Quotient 88 B6 stabilizer goals by all 48 cube symmetries and inversion.

python audit_b6_full48_target_orbits.py HISTORICAL_B1_B5_ARCHIVE.zip

Depends on build_b6_stabilizer_goals.py and verify_b6_geometric_rule.py.
Does NOT supply any new Rubik HTM word-length lower bounds.
"""
import hashlib
import itertools
import math
import sys
import zipfile
from collections import Counter
from pathlib import Path
from build_b6_stabilizer_goals import main as make_goals
from verify_b6_geometric_rule import EDGE_NAMES, valid_pairs

SHA256 = "002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94"
CLASS41_SHA = "c3dbf41177e16d8d0cb0cd76b433304e14f9cdac4a14f205d6231dc9dd8abc1e"


def main(archive):
    assert hashlib.sha256(Path(archive).read_bytes()).hexdigest()==SHA256
    data=make_goals(archive)
    with zipfile.ZipFile(archive) as z:
        context={"__name__":"verified_cube","__file__":"independent_b4.py"}
        exec(compile(z.read("independent_b4.py"),"independent_b4.py","exec"),context)
    E=context["E"];F=context["F"];N=context["N"];loc=context["loc"]
    slots=context["slots"];start=context["START"];A=context["A"];turn=context["turn"]
    assert E==EDGE_NAMES

    def parity(p):
        return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))

    rotations=[]
    for p in itertools.permutations(range(3)):
        for signs in itertools.product((-1,1),repeat=3):
            determinant=parity(p)*math.prod(signs)
            def R(v,p=p,signs=signs):
                return tuple(signs[i]*v[p[i]] for i in range(3))
            face_map={i:F.index(next(f for f in F if N[f]==R(N[F[i]]))) for i in range(6)}
            edge_map={i:E.index(next(e2 for e2 in E if set(e2)==set(F[face_map[F.index(f)]] for f in e)))
                      for i,e in enumerate(E)}
            pos=[loc[(R(x),R(n))] for x,n in slots]
            inv=[0]*54
            for i,j in enumerate(pos):inv[j]=i
            rotations.append((determinant,face_map,edge_map,inv))
    assert len(rotations)==48

    def transport(state,rot):
        det,fm,em,inv=rot
        return bytes(fm[state[inv[j]]] for j in range(54))

    # Physical verification of each word-metric-preserving symmetry:
    # under reflection, a quarter face turn is mapped to an inverse turn.
    for rot in rotations:
        det,fm,em,inv=rot
        assert transport(start,rot)==start
        for i,token in enumerate(A):
            suffix=token[1:]
            if det==-1 and suffix!="2":suffix="" if suffix=="'" else "'"
            mapped=F[fm[F.index(token[0])]]+suffix
            assert transport(turn(start,i),rot)==turn(start,A.index(mapped))

    candidates={(h,pair) for h in E for pair in valid_pairs(h)}
    assert len(candidates)==156
    left=set(candidates);orbit_sizes=[]
    while left:
        h,pair=next(iter(left))
        orbit={(E[rot[2][E.index(h)]],frozenset(E[rot[2][E.index(e)]] for e in pair))
               for rot in rotations}
        assert orbit<=left
        left-=orbit
        orbit_sizes.append(len(orbit))
    assert sorted(orbit_sizes)==[12,24,24,24,24,48]

    targets=data["targets"]
    original={bytes.fromhex(t["facelet_hex"]) for t in targets}
    assert len(targets)==88 and len(original)==74
    by_descriptor={(tuple(t["omitted_edges"]),t["swap"],t["corner_twist"],t["edge_flip"]):
                   bytes.fromhex(t["facelet_hex"]) for t in targets}

    parent={s:s for s in original}
    def find(s):
        while parent[s]!=s:
            parent[s]=parent[parent[s]]
            s=parent[s]
        return s
    def union(a,b):
        x,y=find(a),find(b)
        if x!=y:parent[x]=y

    for t in targets:
        s=bytes.fromhex(t["facelet_hex"])
        sw,tw,fl=t["swap"],t["corner_twist"],t["edge_flip"]
        inv=by_descriptor[(tuple(t["omitted_edges"]),sw,tw if sw else (-tw)%3,fl)]
        union(s,inv)
    for s in original:
        for rot in rotations:
            other=transport(s,rot)
            if other in original:union(s,other)

    classes={}
    for s in original:
        classes.setdefault(find(s),set()).add(s)
    assert len(classes)==41
    class_minima=sorted(min(group) for group in classes.values())
    assert hashlib.sha256(b"".join(class_minima)).hexdigest()==CLASS41_SHA
    assert Counter(map(len,classes.values()))==Counter({1:17,2:19,3:1,4:4})

    print("PASS: 48 symmetries conjugate 18 HTM generators (864 physical checks)")
    print("PASS: 156 layouts => 6 full-48 orbits",sorted(orbit_sizes))
    print("PASS: 88 targets => 74 physical states => 41 HTM-distance classes")
    print("PASS: canonical 41-target digest",CLASS41_SHA)
    print("LIMIT: 41 lower-bound obligations not yet independently discharged")
    return classes


if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: audit_b6_full48_target_orbits.py HISTORICAL.zip")
    main(sys.argv[1])

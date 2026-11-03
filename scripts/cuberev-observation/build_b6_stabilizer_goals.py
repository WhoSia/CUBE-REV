#!/usr/bin/env python3
"""Generate 8 orbit representatives and 88 physical B6 stabilizer targets.

python build_b6_stabilizer_goals.py EXACT_B1_B5_SENSOR_CERTIFICATES.zip [output.json]

Uses archived 54-facelet cube engine and pre-existing B6 geometric criterion.
Constructs physical target STATES only: no HTM shortest-distance proof.
"""
import hashlib
import json
import random
import sys
import zipfile
from itertools import product
from pathlib import Path
from verify_b6_geometric_rule import EDGE_NAMES, ENDS, valid_pairs

SHA256 = "002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94"
PROVEN_13 = "L F R' F' L' U2 R U R U' R2 U2 R"


def det(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2


def main(archive, output=None):
    assert hashlib.sha256(Path(archive).read_bytes()).hexdigest()==SHA256
    with zipfile.ZipFile(archive) as z:
        c={"__name__":"cube_archive","__file__":"independent_b4.py"}
        exec(compile(z.read("independent_b4.py"),"independent_b4.py","exec"),c)
    start=c["START"]; E=c["E"]; corners=c["corner_xyz"]; slots=c["slots"]
    assert E==tuple(EDGE_NAMES) and len(corners)==8 and len(E)==12

    # Positive-handed cyclic ordering for corner stickers (U/D first);
    # for edges U/D first, otherwise F/B first. This fixes twist conventions.
    C=[]
    for inds in c["corner_slots"]:
        ids=sorted(inds,key=lambda i:0 if abs(slots[i][1][1])==1 else (1 if abs(slots[i][1][0])==1 else 2))
        if det(*(slots[i][1] for i in ids))<0:ids=[ids[0],ids[2],ids[1]]
        assert det(*(slots[i][1] for i in ids))==1
        C.append(ids)
    D=[]
    for inds in c["edge_slots"]:
        D.append(sorted(inds,key=lambda i:0 if abs(slots[i][1][1])==1 else (1 if abs(slots[i][1][2])==1 else 2)))
    csrc=[tuple(start[i] for i in ids) for ids in C]
    esrc=[tuple(start[i] for i in ids) for ids in D]
    cid={frozenset(x):i for i,x in enumerate(csrc)}
    eid={frozenset(x):i for i,x in enumerate(esrc)}
    assert len(cid)==8 and len(eid)==12

    def decode(state):
        cp=[];co=[];ep=[];eo=[]
        for ids in C:
            colors=tuple(state[i] for i in ids)
            j=cid[frozenset(colors)];orientation=colors.index(csrc[j][0])
            assert all(colors[k]==csrc[j][(k-orientation)%3] for k in range(3))
            cp.append(j);co.append(orientation)
        for ids in D:
            colors=tuple(state[i] for i in ids)
            j=eid[frozenset(colors)];orientation=colors.index(esrc[j][0])
            assert all(colors[k]==esrc[j][(k-orientation)%2] for k in range(2))
            ep.append(j);eo.append(orientation)
        assert sum(co)%3==0 and sum(eo)%2==0
        assert parity(cp)==parity(ep)
        return (tuple(cp),tuple(co),tuple(ep),tuple(eo))

    def encode(cp,co,ep,eo):
        assert sorted(cp)==list(range(8)) and sorted(ep)==list(range(12))
        assert sum(co)%3==0 and sum(eo)%2==0 and parity(cp)==parity(ep)
        state=bytearray(start)
        for pos,(tag,t) in enumerate(zip(cp,co)):
            for i,idx in enumerate(C[pos]):state[idx]=csrc[tag][(i-t)%3]
        for pos,(tag,f) in enumerate(zip(ep,eo)):
            for i,idx in enumerate(D[pos]):state[idx]=esrc[tag][(i-f)%2]
        out=bytes(state)
        assert decode(out)==(tuple(cp),tuple(co),tuple(ep),tuple(eo))
        return out

    identity=(tuple(range(8)),(0,)*8,tuple(range(12)),(0,)*12)
    assert decode(start)==identity
    # A deterministic 1000-turn physical sample and all 18^2 move pairs.
    rand=random.Random(20261103)
    state=start
    for _ in range(1000):
        state=c["turn"](state,rand.randrange(18))
        assert encode(*decode(state))==state
    one=[decode(c["turn"](start,i)) for i in range(18)]
    def combine(left,right):
        cp,co,ep,eo=left; p,t,e,f=right
        return (tuple(cp[p[i]] for i in range(8)),tuple((co[p[i]]+t[i])%3 for i in range(8)),
                tuple(ep[e[i]] for i in range(12)),tuple((eo[e[i]]+f[i])%2 for i in range(12)))
    for i in range(18):
        for j in range(18):
            assert decode(c["turn"](c["turn"](start,i),j))==combine(one[i],one[j])

    rotations=c["rotation_maps"]()
    eligible={(h,pair) for h in E for pair in valid_pairs(h)}
    assert len(eligible)==156
    left=set(eligible);orbits=[]
    while left:
        h,pair=min(left,key=lambda t:(E.index(t[0]),tuple(sorted(E.index(e) for e in t[1]))))
        orb={(E[emap[E.index(h)]],frozenset(E[emap[E.index(e)]] for e in pair))
             for _,emap,_,_ in rotations}
        assert orb<=left
        left-=orb
        orbits.append(orb)
    assert len(orbits)==8 and sorted(map(len,orbits))==[12,12,12,24,24,24,24,24]

    targets=[];representatives=[]
    for orbit in orbits:
        candidates=[x for x in orbit if x[0]=="DL"]
        assert candidates
        h,pair=min(candidates,key=lambda t:tuple(sorted(E.index(e) for e in t[1])))
        missed_c=sorted(corners.index(x) for x in ENDS[h])
        missed_e=sorted(E.index(e) for e in pair)
        assert len(missed_c)==len(missed_e)==2
        reps_entry={"h":h,"omitted_corner_indices":missed_c,
                    "omitted_corner_xyz":[corners[i] for i in missed_c],
                    "omitted_edges":sorted(pair),"orbit_size":len(orbit)}
        representatives.append(reps_entry)
        for swap,twist,flip in product(range(2),range(3),range(2)):
            cp=list(range(8));ep=list(range(12));co=[0]*8;eo=[0]*12
            if swap:
                i,j=missed_c;cp[i],cp[j]=cp[j],cp[i]
                i,j=missed_e;ep[i],ep[j]=ep[j],ep[i]
            i,j=missed_c;co[i]=twist;co[j]=(-twist)%3
            i,j=missed_e;eo[i]=eo[j]=flip
            phys=encode(cp,co,ep,eo)
            assert all(c["ev"](phys)[i]==c["ev"](start)[i] for i in range(12) if i not in missed_e)
            assert all(c["cv"](phys)[4*i:4*i+4]==c["cv"](start)[4*i:4*i+4]
                       for i in range(8) if i not in missed_c)
            assert (phys==start)==(swap==twist==flip==0)
            if phys==start:continue
            targets.append({**reps_entry,"swap":swap,"corner_twist":twist,"edge_flip":flip,
                            "facelet_hex":phys.hex(),"sha256":hashlib.sha256(phys).hexdigest()})
    assert len(targets)==88
    unique={a["facelet_hex"] for a in targets}
    assert len(unique)==74

    def invert(cp,co,ep,eo):
        pc=[0]*8;pe=[0]*12
        for i,x in enumerate(cp):pc[x]=i
        for i,x in enumerate(ep):pe[x]=i
        return (tuple(pc),tuple((-co[pc[i]])%3 for i in range(8)),
                tuple(pe),tuple((-eo[pe[i]])%2 for i in range(12)))
    inverses={}
    for t in targets:
        face=bytes.fromhex(t["facelet_hex"])
        inv=encode(*invert(*decode(face)))
        inverses[t["facelet_hex"]]=inv.hex()
        assert inv.hex() in unique
        assert encode(*invert(*decode(inv)))==face
    inverse_classes={tuple(sorted((h,inverses[h]))) for h in unique}
    assert len(inverse_classes)==65

    # Existing 13-turn two-edge flip must match the physical goal byte-for-byte.
    phys=start
    for a in PROVEN_13.split():phys=c["turn"](phys,c["A"].index(a))
    known=[t for t in targets if set(t["omitted_edges"])=={"UR","UF"}
           and t["swap"]==0 and t["corner_twist"]==0 and t["edge_flip"]==1]
    assert len(known)==1 and bytes.fromhex(known[0]["facelet_hex"])==phys

    result={"archive_sha256":SHA256,
            "representatives":sorted(representatives,key=lambda x:x["omitted_edges"]),
            "targets":sorted(targets,key=lambda x:(x["omitted_edges"],x["swap"],x["corner_twist"],x["edge_flip"])),
            "total_targets":88,"unique_target_states":74,"inverse_target_classes":65}
    if output:
        Path(output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS: 156 geometric-positive layouts split into 8 proper-rotation orbits")
    print("PASS: 88 physical target entries, 74 distinct, 65 inverse classes")
    print("PASS: 1000 physical facelet roundtrips and 324 move-composition identities")
    print("PASS: 13-HTM two-edge-flip witness equals generated target exactly")
    for item in result["representatives"]:
        print("REP DL omitted edges",item["omitted_edges"],"orbit",item["orbit_size"])
    print("LIMIT: no independent 3x3 HTM distance lower bounds were computed")
    return result


if __name__=="__main__":
    if len(sys.argv) not in (2,3):
        raise SystemExit("Usage: build_b6_stabilizer_goals.py HISTORICAL.zip [OUTPUT.json]")
    main(sys.argv[1],sys.argv[2] if len(sys.argv)==3 else None)

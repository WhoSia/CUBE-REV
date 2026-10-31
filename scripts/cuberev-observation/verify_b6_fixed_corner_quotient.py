#!/usr/bin/env python3
"""Burnside quotient of B6 16-tag layouts at one fixed omitted corner edge.

Usage: python verify_b6_fixed_corner_quotient.py PREVIOUS_B1_B5.zip
Uses inherited verified B6 positive representative indices [1,5,6,15,18,19,20,25].
This is a structural classification check, not an independent B6 full census.
"""
import json,sys,zipfile
assert len(sys.argv)==2
with zipfile.ZipFile(sys.argv[1]) as z:
    c=json.loads(z.read("b5_sixteen_layout_census.json"))
    scope={"__name__":"archived_cube"}
    exec(compile(z.read("independent_b4.py"),"independent_b4.py","exec"),scope)
reps=[]
for mask,size in c["valid_16_orbits"]:
    omitted=[i for i in range(8) if not (mask>>(12+i)&1)]
    xyz=scope["corner_xyz"]
    if sum(x!=y for x,y in zip(xyz[omitted[0]],xyz[omitted[1]]))==1:
        reps.append((mask,size))
assert len(reps)==27
success={1,5,6,15,18,19,20,25}
rotations=scope["rotation_maps"]()
def transport(mask,em,cm):
    return (sum(1<<em[i] for i in range(12) if mask>>i&1) |
            sum(1<<(12+cm[i]) for i in range(8) if mask>>(12+i)&1))
fixed_corner=(1<<12)|(1<<13)
possible=set();positive=set()
for j,(mask,size) in enumerate(reps):
    omitted=((1<<20)-1)^mask
    for _,em,cm,_ in rotations:
        mapped=transport(omitted,em,cm)
        if (mapped&(255<<12))==fixed_corner:
            edgepair=mapped&4095
            assert edgepair.bit_count()==2
            possible.add(edgepair)
            if j in success:positive.add(edgepair)
assert len(possible)==48
assert len(positive)==13
negative=possible-positive
assert len(negative)==35
stabilizer=[(em,cm) for _,em,cm,_ in rotations
            if {cm[0],cm[1]}=={0,1}]
assert len(stabilizer)==2
def orbits_by_burnside(items):
    fixed=sum(all(transport(m,em,cm)==m for em,cm in stabilizer)
              for m in items)
    return fixed,(len(items)+fixed)//2
assert orbits_by_burnside(positive)==(3,8)
assert orbits_by_burnside(negative)==(3,19)
assert len(positive)*12==156
assert len(negative)*12==420
print("PASS fixed adjacent omitted-corner pair: 48 B5-compatible omitted edge pairs")
print("PASS B6 positive 13 and negative 35 omitted edge pairs")
print("PASS stabilizer order2, fixed points 3+3")
print("PASS Burnside: positive 8 orbits, negative 19 orbits")
print("PASS 12 corner-edge choices * 13=156 positive global B6 layouts")

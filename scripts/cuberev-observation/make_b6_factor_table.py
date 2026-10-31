#!/usr/bin/env python3
"""Generate exact 20-cubie ×18-HTM transition table and B6 candidate masks.

Input: historical CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip
Usage: python make_b6_factor_table.py PATH_TO_ARCHIVE.zip
Outputs b6_factor_table.hpp and b6_candidate_reps.hpp in working directory.
This uses a locally trusted, provenance-audited source archive.
"""
import json,sys,zipfile
assert len(sys.argv)==2
with zipfile.ZipFile(sys.argv[1]) as z:
    source=z.read("independent_b4.py")
    census=json.loads(z.read("b5_sixteen_layout_census.json"))
scope={"__name__":"cuberev_b4_source","__file__":"independent_b4.py"}
exec(compile(source,"independent_b4.py","exec"),scope)
b=type("B4",(),scope)
states=[b.START];seen={b.START}
front=[b.START]
for d in range(1,4):
    following=[]
    for s in front:
        for a in range(18):
            t=b.turn(s,a)
            if t not in seen:seen.add(t);following.append(t)
    states.extend(following);front=following
assert len(states)==3502

corner_keys=[{} for _ in range(8)]
for s in states:
    corners=b.cv(s)
    for i in range(8):
        k=corners[4*i:4*i+4]
        corner_keys[i].setdefault(k,len(corner_keys[i]))
assert all(len(x)==24 for x in corner_keys)

moves=[[[255]*24 for _ in range(20)] for _ in range(18)]
for s in states:
    edges=b.ev(s);corners=b.cv(s)
    for a in range(18):
        t=b.turn(s,a);te=b.ev(t);tc=b.cv(t)
        for i in range(12):
            x,y=edges[i],te[i]
            assert moves[a][i][x] in (255,y)
            moves[a][i][x]=y
        for i in range(8):
            x=corner_keys[i][corners[4*i:4*i+4]]
            y=corner_keys[i][tc[4*i:4*i+4]]
            assert moves[a][12+i][x] in (255,y)
            moves[a][12+i][x]=y
assert all(all(all(v<24 for v in p) for p in a) for a in moves)
base_corner=b.cv(b.START)
start=list(b.ev(b.START))+[corner_keys[i][base_corner[4*i:4*i+4]] for i in range(8)]
with open("b6_factor_table.hpp","w") as f:
    f.write("#pragma once\n#include <cstdint>\nstatic constexpr uint8_t TABLE[18][20][24]={\n")
    for a in moves:
        f.write("{"+",".join("{"+",".join(map(str,p))+"}" for p in a)+"},\n")
    f.write("};\nstatic constexpr uint8_t START[20]={"+",".join(map(str,start))+"};\n")
reps=[]
for mask,size in census["valid_16_orbits"]:
    omitted=[i for i in range(8) if not (mask>>(12+i))&1]
    assert len(omitted)==2
    if sum(a!=b for a,b in zip(b.corner_xyz[omitted[0]],b.corner_xyz[omitted[1]]))==1:
        reps.append((mask,size))
assert len(reps)==27 and sum(k for m,k in reps)==576
with open("b6_candidate_reps.hpp","w") as f:
    f.write("#pragma once\n#include <cstdint>\n")
    f.write("static constexpr uint32_t REPS[27]={"+",".join(str(m) for m,k in reps)+"};\n")
    f.write("static constexpr uint8_t ORBIT_SIZES[27]={"+",".join(str(k) for m,k in reps)+"};\n")
print("PASS B3 3502 states, complete 18x20x24 transition table, B6 27 orbit reps")

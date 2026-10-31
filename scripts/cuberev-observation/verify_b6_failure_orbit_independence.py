#!/usr/bin/env python3
"""Audit independent physical 4-cubie collision-support rotation orbits.

Usage: python verify_b6_failure_orbit_independence.py PREVIOUS_B1_B5.zip
Run from the same directory as verify_b6_negative_witnesses.py.
This proves private coverage for THIS witness family only, not minimum
certificate size among all possible B6 physical collision witnesses.
"""
import ast,collections,itertools,json,sys,zipfile
from pathlib import Path
assert len(sys.argv)==2
with zipfile.ZipFile(sys.argv[1]) as z:
    ctx={"__name__":"archived_b4","__file__":"independent_b4.py"}
    exec(compile(z.read("independent_b4.py"),"independent_b4.py","exec"),ctx)
    census=json.loads(z.read("b5_sixteen_layout_census.json"))
# Do not execute the test module here; read its witness dictionary as literal data.
tree=ast.parse(Path(__file__).with_name("verify_b6_negative_witnesses.py").read_text())
assignment=next(n for n in tree.body if isinstance(n,ast.Assign)
                and any(isinstance(t,ast.Name) and t.id=="W" for t in n.targets))
W=ast.literal_eval(assignment.value)
assert len(W)==19
reps=[]
for mask,size in census["valid_16_orbits"]:
    omitted=[i for i in range(8) if not(mask>>(12+i)&1)]
    if sum(a!=b for a,b in zip(ctx["corner_xyz"][omitted[0]],
                               ctx["corner_xyz"][omitted[1]]))==1:
        reps.append((mask,size))
assert len(reps)==27

def replay(word):
    s=ctx["START"]
    for move in word.split():s=ctx["turn"](s,ctx["A"].index(move))
    return s

def support(a,b):
    ea,eb=ctx["ev"](a),ctx["ev"](b)
    ca,cb=ctx["cv"](a),ctx["cv"](b)
    return (sum(1<<i for i in range(12) if ea[i]!=eb[i]) |
            sum(1<<(12+i) for i in range(8) if ca[4*i:4*i+4]!=cb[4*i:4*i+4]))

def transport(mask,em,cm):
    return (sum(1<<em[i] for i in range(12) if mask>>i&1) |
            sum(1<<(12+cm[i]) for i in range(8) if mask>>(12+i)&1))
rotations=ctx["rotation_maps"]()
classes={}
for j,(u,v) in sorted(W.items()):
    x,y=replay(u),replay(v)
    assert x!=y
    m=support(x,y)
    assert m.bit_count()==4 and (m&reps[j][0])==0
    orbit=frozenset(transport(m,em,cm) for _,em,cm,_ in rotations)
    classes.setdefault(orbit,[]).append(j)
assert len(classes)==19
coverage={}
for orbit,indices in classes.items():
    hit={i for i,(m,_) in enumerate(reps) if any((s&m)==0 for s in orbit)}
    coverage[orbit]=hit
    assert len(indices)==1 and hit==set(indices),(indices,hit)
sizes=collections.Counter(map(len,classes))
assert sizes=={24:16,12:3},sizes
assert set.union(*coverage.values())==set(W)
assert sum(reps[i][1] for i in W)==420
print("PASS 19 distinct pure 2-edge+2-corner support rotation orbits")
print("PASS 16 orbits of size24 plus 3 orbits of size12")
print("PASS each witness orbit has exactly ONE private failed candidate orbit")
print("PASS all 19 failed B6 representative orbits, total 420 layouts")
print("LIMIT: does not show 19 is minimal among ALL possible collision certificates")

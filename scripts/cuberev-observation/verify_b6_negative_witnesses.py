#!/usr/bin/env python3
"""Independently replay all 19 negative B6 orbit witnesses in 54-facelet physics.

Usage: python verify_b6_negative_witnesses.py ARCHIVED_B1_B5_CERTIFICATES.zip
No B6 census is required for this negative part. Positive eight orbits are
certified separately by verify_b6_16_bases.cpp.
"""
import json,sys,zipfile
from types import SimpleNamespace
assert len(sys.argv)==2
with zipfile.ZipFile(sys.argv[1]) as z:
    scope={"__name__":"archived_b4","__file__":"independent_b4.py"}
    exec(compile(z.read("independent_b4.py"),"independent_b4.py","exec"),scope)
    census=json.loads(z.read("b5_sixteen_layout_census.json"))
b=SimpleNamespace(**scope)
reps=[]
for mask,sz in census["valid_16_orbits"]:
    absent=[i for i in range(8) if not((mask>>(12+i))&1)]
    if sum(x!=y for x,y in zip(b.corner_xyz[absent[0]],b.corner_xyz[absent[1]]))==1:
        reps.append((mask,sz))
assert len(reps)==27
W={
0:("L2 U2 B L' B' U2","L2 F R' F R F2"),
2:("U R2 F' U F R2","U B' D B' D' B2"),
3:("U2 R2 F' U F R2","U2 B' D B' D' B2"),
4:("F2 R2 U2 B U B'","F2 D' F' D R2 U'"),
7:("D L U2 R' F R","D B L' B' L2 U2"),
8:("U' R2 B U' B' R2","U' F D' F D F2"),
9:("U R2 B U' B' R2","U F D' F D F2"),
10:("R2 F2 U L' U' F2","R2 D R' D R D2"),
11:("U' F' D2 B R' B'","U' L' F L F2 D2"),
12:("B2 U' B U' B' U2","B2 R2 D' F D R2"),
13:("R L2 F U' F U","R B D' B' L2 F2"),
14:("U' F' D F' D' F2","U' L2 B' U B L2"),
16:("F L U' L U L2","F B2 R D' R' B2"),
17:("U D B D' B R2","U B2 R2 F' U' F"),
21:("R F' D F L2 B2","R L2 B' U B' U'"),
22:("D' R D' R D R2","D' B2 L U' L' B2"),
23:("F U' F U' F' U2","F L2 D' B D L2"),
24:("R D' L B2 R' U","R L' D' L2 B2 R'"),
26:("U R' B R' B' R2","U D2 L' F L D2"),
}
def play(word):
    s=b.START
    for move in word.split(): s=b.turn(s,b.A.index(move))
    return s
for i,(left,right) in W.items():
    x,y=play(left),play(right)
    assert x!=y
    ex,ey=b.ev(x),b.ev(y)
    cx,cy=b.cv(x),b.cv(y)
    diff={j for j in range(12) if ex[j]!=ey[j]}
    diff|={12+j for j in range(8) if cx[4*j:4*j+4]!=cy[4*j:4*j+4]}
    assert diff and all(not(reps[i][0]>>j&1) for j in diff),(i,diff)
    assert len(left.split())<=6 and len(right.split())<=6
assert len(W)==19 and sum(reps[i][1] for i in W)==420
positive=set(range(27))-set(W)
assert len(positive)==8 and sum(reps[i][1] for i in positive)==156
print("PASS 19 physically distinct B6 counterexample pairs in 54-sticker model")
print("PASS excluded 420 layouts, eight remaining orbit reps weight 156")
print("POSITIVE orbits need separate complete 8240087-state injectivity check")

#!/usr/bin/env python3
"""R14 P8.38: complete robust original-cubie pose-sensor design census.

Given physically replayed B6 and B7 support-mask witnesses, classify all 2^20
permanent original-tag layouts under adversarial loss of 0, 1, or 2 chosen tags.
Positive B6 verdicts rely on prior successful independent P8.33 41-target MITM.
No equivalence is claimed to fault-tolerant graph metric dimension, which measures
vertex distance signatures rather than original-cubie pose.
"""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def load(name,file):
    sp=importlib.util.spec_from_file_location(name,ROOT/file)
    m=importlib.util.module_from_spec(sp)
    with redirect_stdout(StringIO()):
        sp.loader.exec_module(m)
    return m
b6=load("b6p838","verify_b6_complete_4845_p48.py")
b7=load("b7p838","audit_r14_p830_independent_b7_pair_support_complete.py")
T=tuple(b6.EDGE_POS)+tuple(b6.CORNERS)
assert len(T)==len(set(T))==20
idx={t:i for i,t in enumerate(T)}
def mask(tags):
    return sum(1<<idx[t] for t in tags)
s6={mask(q) for f in (b6.triple_edge_obstructions,b6.two_corner_obstructions,b6.adjacent_b5_obstructions,b6.adjacent_b6_obstructions) for q in f()}
s7={mask(q) for q in b7.C|b7.E}
assert len(s6)==872 and len(s7)==94
N=1<<20
FULL=N-1
def bad_closure(supports):
    out=bytearray(N)
    for s in supports:out[s]=1
    for b in range(20):
        bit=1<<b
        for base in range(0,N,2*bit):
            for n in range(base+bit,base+2*bit):
                if out[n-bit]:out[n]=1
    return out
bad6=bad_closure(s6);bad7=bad_closure(s7)
hist={k:{0:Counter(),1:Counter(),2:Counter()} for k in ("B6","B7")}
witness={}
for S in range(N):
    omitted=FULL^S
    ones=[1<<i for i in range(20) if S&(1<<i)]
    size=len(ones)
    for label,bad in (("B6",bad6),("B7",bad7)):
        if bad[omitted]: continue
        hist[label][0][size]+=1
        if any(bad[omitted|b] for b in ones):continue
        hist[label][1][size]+=1
        if any(bad[omitted|ones[i]|ones[j]] for i in range(len(ones)) for j in range(i+1,len(ones))):
            continue
        hist[label][2][size]+=1
assert hist["B6"][0]=={16:156,17:672,18:174,19:20,20:1}
assert hist["B7"][0]=={18:96,19:20,20:1}
assert hist["B7"][1]=={20:1},hist["B7"][1]
assert not hist["B7"][2]
# Because some 18-subsets of the full 20 sensors are known B6-insufficient,
# even the full sensor set cannot survive arbitrary two deleted tags.
assert not hist["B6"][2]
print(json.dumps({
"status":"PASS",
"model":"persistent_original_cubie_full_pose; adversarial deletion",
"all_subsets":N,
"physical_B6_supports":len(s6),
"physical_B7_supports":len(s7),
"by_radius_and_max_failed_tags":{label:{str(k):dict(sorted(c.items())) for k,c in data.items()} for label,data in hist.items()},
"B7_one_fault_minimum_tags":20,
"B7_two_fault_possible":False,
"B6_two_fault_possible":False,
"depends_on_P833_positive_B6_distance_CI":True,
"unrestricted_19_color_frames_addressed":False},sort_keys=True))

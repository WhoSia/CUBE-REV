#!/usr/bin/env python3
"""CUBE-REV 0.27 first-root negative verifier. A completed Go run, not a saved C++ receipt, is required."""
import argparse,json,pathlib,re
p=argparse.ArgumentParser()
p.add_argument("root",type=int)
p.add_argument("log",type=pathlib.Path)
p.add_argument("expected",type=pathlib.Path)
a=p.parse_args()
s=a.log.read_text()
ref=json.loads(a.expected.read_text())
expected=ref["roots"][str(a.root)]
for marker in ("GO_INDEPENDENT_54_SITE_GEOMETRY_OK 54",
               "GO_INDEPENDENT_CORNER_C8_PASS 88179840",
               "GO_INDEPENDENT_FULL_GOAL_B6_PASS 8240087 E6 7672278",
               "GO_SOURCE_FIXED_PHYSICAL_18HTM_WITNESS_PASS"):
    assert marker in s, f"MISSING_PHYSICAL_PREMISE: {marker}"
pat=r"^GO_ROOT_RESULT root=(\d+) child=(-?\d+) jobs=(\d+) visits=(\d+) omitted=(\d+) hit=(\d+) full=(\d+) e6=(\d+) corner8=(\d+) corner7=(\d+) corner6=(\d+) virtual=(\d+)"
m=re.search(pat,s,re.M)
assert m, "NO_COMPLETED_ROOT"
root,child,jobs,visited,omitted,hit,full,e6,c8,c7,c6,virtual=map(int,m.groups())
def legal(a,b):
    return a//3!=b//3 and not(a//3>=3 and a//3-3==b//3)
children=[b for b in range(18) if legal(root,b)]
assert (root,child,jobs,hit)==(a.root,-1,len(children),0), "INCOMPLETE_ROOT"
for name,value in dict(virtual=virtual,visits=visited,omitted=omitted,full=full,e6=e6,corner8=c8,corner7=c7,corner6=c6,meets=hit).items():
    assert value==expected[name],f"COUNTER_MISMATCH_{name}_{value}_{expected[name]}"
assert visited+omitted==virtual
rows=re.findall(r"^GO_SECOND_CHILD root=(\d+) second=(\d+) visits=(\d+) omit=(\d+) full=(\d+) hit=(\d+) total=(\d+) expected=(\d+)",s,re.M)
assert sorted(int(row[1]) for row in rows)==children, "CHILDREN_NOT_EXACT"
assert all(int(row[0])==root and int(row[5])==0 and int(row[6])==int(row[7]) for row in rows)
assert sum(int(row[2]) for row in rows)+1==visited
assert sum(int(row[3]) for row in rows)==omitted
assert sum(int(row[4]) for row in rows)==full
print("ORIGINAL_WCA_GO_ROOT_PHYSICAL_RECOMPUTE_PASS",root,virtual,visited,omitted,full)

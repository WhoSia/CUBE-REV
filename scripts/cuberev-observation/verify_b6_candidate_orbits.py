#!/usr/bin/env python3
"""Audit B6 sixteen-tag candidate orbit bound from the prior exact B5 archive.

Usage:
  python verify_b6_candidate_orbits.py CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip

This is a read-only, bounded statement about PREEXISTING B5-valid 16-tag
layouts satisfying the B6 12-HTM pure-two-corner obstruction.
It is NOT a B6 positive- or negative-configuration census.
"""
import collections
import io
import json
import sys
import zipfile

assert len(sys.argv) == 2, "pass prior B1-B5 proof archive as sole argument"
archive = sys.argv[1]
with zipfile.ZipFile(archive) as z:
    census=json.loads(z.read("b5_sixteen_layout_census.json"))
    source=z.read("independent_b4.py").decode("utf-8")

# Coordinates are defined in the archived physical-code document, and
# are independently reconstructed from 8 cube corners here.
from itertools import product
corners=sorted(product((-1,1),repeat=3))
def distance(i,j):
    return sum(x!=y for x,y in zip(corners[i],corners[j]))
assert len(corners)==8
assert census["valid_16_designs"] == 1488
summary=collections.Counter()
orbit_sizes=collections.Counter()
reps=[]
for mask,size in census["valid_16_orbits"]:
    assert mask.bit_count()==16
    corner_omission=[i for i in range(8) if not (mask>>(12+i))&1]
    edge_omission=[i for i in range(12) if not (mask>>i)&1]
    assert len(corner_omission)==2 and len(edge_omission)==2
    d=distance(*corner_omission)
    summary[d]+=size
    if d==1:
        orbit_sizes[size]+=1
        reps.append(mask)
assert summary=={1:576,2:672,3:240},summary
assert orbit_sizes=={24:21,12:6},orbit_sizes
assert len(reps)==27
assert sum(k*v for k,v in orbit_sizes.items())==576
print("PASS B5 valid16, classified by omitted-corner cube distance",dict(summary))
print("PASS B6 necessary survivors: 576 in 27 proper-rotation orbits")
print("PASS B6 candidates: 21 orbits of size24 and 6 of size12")
print("NOT a B6 success check: 27 representative B6 collisions still OPEN")

#!/usr/bin/env python3
"""Exact full-cubie-factor minimum Hamming distance for EVERY 20-tag subset.

Assumes the separately physically certified B7 minimal support clutter:
all 28 corner pairs and 66 edge pairs, with no singleton legal support.
Does not reconstruct or enumerate all B7 states; not orientation-only readout.
"""
from itertools import combinations
from collections import Counter

C_masks=[sum(1<<i for i in pair) for pair in combinations(range(8),2)]
E_masks=[sum(1<<(8+i) for i in pair) for pair in combinations(range(12),2)]
assert len(C_masks)==28 and len(E_masks)==66
supports=C_masks+E_masks

counts=Counter()
for S in range(1<<20):
    observed_min=2
    for d in supports:
        observed_min=min(observed_min,(S&d).bit_count())
        if observed_min==0:break
    nC=(S&255).bit_count()
    nE=(S>>8).bit_count()
    predicted=min(max(0,nC-6),max(0,nE-10))
    assert observed_min==predicted,(S,observed_min,predicted)
    counts[observed_min]+=1

assert dict(counts)=={0:1048459,1:116,2:1},counts
print("PASS all 1,048,576 selected subsets")
print("PASS exact B7/global full-factor distance law:")
print("delta_r(S)=min(max(0,|S_C|-6),max(0,|S_E|-10)) for all r>=7")
print("counts for distances 0/1/2:",dict(sorted(counts.items())))

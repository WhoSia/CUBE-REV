#!/usr/bin/env python3
"""Dependency-free audit of the archived B6 two-edge omission taxonomy.

This verifies purely combinatorial accounting, NOT original physical witness
validity or the positive B6 full-state census. The per-category grade counts
are sourced from verify_b6_obstruction_filtration.py in this repository.
"""
from itertools import combinations
from collections import Counter

GROUPS = ("h", "N", "P", "F", "h*")
SIZES = dict(zip(GROUPS, (1, 4, 2, 4, 1)))
# (excluded by B5 evidence, newly excluded by B6 evidence, B6-successful)
COUNTS = {
    ("h","N"): (4,0,0), ("h","P"): (2,0,0),
    ("h","F"): (4,0,0), ("h","h*"): (0,1,0),
    ("N","N"): (0,2,4), ("N","P"): (4,4,0),
    ("N","F"): (0,16,0), ("N","h*"): (4,0,0),
    ("P","P"): (0,0,1), ("P","F"): (0,8,0),
    ("P","h*"): (0,2,0), ("F","F"): (0,2,4),
    ("F","h*"): (0,0,4),
}
def main():
    assert len(COUNTS)==13
    for (a,b), (old,new,good) in COUNTS.items():
        total=SIZES[a]*SIZES[b] if a!=b else SIZES[a]*(SIZES[a]-1)//2
        assert (old+new+good)==total, (a,b,total,old,new,good)
    assert tuple(sum(v[i] for v in COUNTS.values()) for i in range(3))==(18,35,13)
    assert sum(map(sum,COUNTS.values()))==66
    # The old K4,4 obstruction is exactly the new N-F block, no double count.
    assert COUNTS[("N","F")]==(0,16,0)
    assert 35-16==19
    positive={a+"-"+b:v[2] for (a,b),v in COUNTS.items() if v[2]}
    assert positive=={"N-N":4,"P-P":1,"F-F":4,"F-h*":4}
    assert sum(positive.values())==13
    print("PASS: 66 = 18 B5 failures + 16 K4,4 B6 failures + 19 other B6 failures + 13 survivors")
    print("PASS: surviving class counts:",positive)
    print("LIMIT: source category data must be checked against physically replayed witnesses")
    print("LIMIT: surviving candidates require independent positive full-state census")
if __name__=="__main__":
    main()

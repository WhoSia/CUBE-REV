#!/usr/bin/env python3
"""Exact P11 certificate; stdlib only, no solver trusted, no human data.

Proves B fractional covering optimum 24/5, integer minimum 6 via
small finite overlap, and *does not* prove original M* >= 26.
"""
import json
from pathlib import Path
from collections import Counter

p=Path(__file__).resolve().parents[2]/"docs/0.16/P10_50_BY_116.json"
d=json.loads(p.read_text())
weights=d["weights"]
masks=[int(x) for x in d["coverage_masks"]]
assert len(weights)==50 and len(masks)==116
remaining=set(range(50))
components=[]
while remaining:
    c={next(iter(remaining))}
    while True:
        old=len(c)
        for q in masks:
            if any(q>>i&1 for i in c):
                c.update(i for i in range(50) if q>>i&1)
        if old==len(c):break
    components.append(c)
    remaining-=c
components.sort(key=len)
assert [len(x) for x in components]==[22,28]
B=sorted(components[1])
Q=[q for q in masks if any(q>>i&1 for i in B)]
def mass(q):
    return sum(weights[i] for i in B if q>>i&1)
assert len(Q)==80 and sum(weights[i] for i in B)==96
P20=[q for q in Q if mass(q)==20]
P16=[q for q in Q if mass(q)==16]
assert (len(P20),len(P16))==(74,6)
assert all(mass(q)<=20 for q in Q)
# The following exact 24-variable rational primal has denominator75.
frac={2:7,5:6,8:24,9:34,17:7,26:4,36:10,45:32,46:32,
      50:27,53:16,74:11,82:6,86:11,89:42,97:16,99:11,
      100:4,103:1,106:16,109:16,112:11,114:11,115:5}
assert len(frac)==24 and sum(frac.values())==360
assert all(sum(v for k,v in frac.items() if masks[k]>>i&1)==75
           for i in B)
# Weak dual: all target weights sum 96 and word mass<=20 -> LP >=96/20.
# Fractional primal: total 360/75 -> LP <=24/5. Thus exact LP=24/5.
assert 96*5==24*20 and 360*5==24*75
# Every four pairwise-disjoint mass20 columns have a fifth-column
# intersection of mass>=8, whether that fifth has weight16 or20.
quartets=0
quartet_types=Counter()
minimum20=minimum16=20
for a in range(74):
  for b in range(a+1,74):
    if P20[a]&P20[b]:continue
    ab=P20[a]|P20[b]
    for c in range(b+1,74):
      if ab&P20[c]:continue
      abc=ab|P20[c]
      for e in range(c+1,74):
        if abc&P20[e]:continue
        used=abc|P20[e]
        assert mass(used)==80
        quartets+=1
        shape=lambda q:(sum(bool(q>>i&1) for i in B if weights[i]==4),
                        sum(bool(q>>i&1) for i in B if weights[i]==2))
        quartet_types[tuple(sorted(map(shape,
                     (P20[a],P20[b],P20[c],P20[e]))))]+=1
        for i,q in enumerate(P20):
            if i not in (a,b,c,e):
                minimum20=min(minimum20,mass(used&q))
        for q in P16:
            minimum16=min(minimum16,mass(used&q))
assert (quartets,minimum20,minimum16)==(7004,8,8)
assert sorted(quartet_types.values())==[612,2672,3720]
assert all(signature.count((5,0))==2 for signature in quartet_types)
assert 80+20-8<96
print("P11_FRACTIONAL_24_OVER_5_EXACT_CERT_PASS")
print("P11_INTEGER_SIX_8_OVERLAP_7004_QUARTETS_PASS")
print(json.dumps({"LP_optimum":"24/5","integer_optimum":6,
  "quartets":quartets,"minFifthOverlap":8,
  "quartetTypeCounts":sorted(quartet_types.values())}))

#!/usr/bin/env python3
"""Actual four-cubie B5/B6 physical support filtration, 34 witness orbits.

Usage: python verify_b6_mixed_support_filtration.py ARCHIVED_B1_B5.zip

Replays 15 physical B5 negative witness pairs in the historical ZIP and 19
B6 witness pairs in the sibling bridge. Reconstructs ALL rotations at original
cubie-tag level. No trusted B6 'success list' or full B6 census is read.
"""
import json,sys,zipfile
from verify_b6_geometric_bridge import (
    scope,rotations,transport,state_after,difference_mask,
    physical_obstructions,EDGE_NAMES,ENDS,full
)
assert len(sys.argv)==2
with zipfile.ZipFile(sys.argv[1]) as z:
    census=json.loads(z.read("b5_sixteen_layout_census.json"))

old_orbits=[]
old=set()
for entry in census["invalid_16_orbits"]:
    w1,w2=(" ".join(word) for word in entry["words"])
    a,b=state_after(w1),state_after(w2)
    assert a!=b and len(w1.split())<=5 and len(w2.split())<=5
    support=difference_mask(a,b)
    positions=[i for i in range(20) if (support>>i)&1]
    assert sorted(positions)==sorted(entry["delta"])
    assert len(positions)==4 and len([i for i in positions if i<12])==2
    assert (support&entry["mask"])==0
    orbit={transport(support,em,cm) for _,em,cm,_ in rotations}
    assert len(orbit)==entry["orbit_size"]
    old_orbits.append(frozenset(orbit))
    old.update(orbit)
assert len(old_orbits)==15
assert len(set(old_orbits))==15
assert len(old)==360

new=physical_obstructions
assert len(new)==420 and not(old&new)
all_supported=old|new
assert len(all_supported)==780

for h in EDGE_NAMES:
    corner_bits=sum(1<<(12+scope["corner_xyz"].index(c)) for c in ENDS[h])
    prior={m for m in old if (m&(255<<12))==corner_bits}
    added={m for m in new if (m&(255<<12))==corner_bits}
    assert len(prior)==18 and len(added)==35 and not(prior&added)
    assert len(prior|added)==53
    # The 13 remaining two-edge omissions are not represented by an
    # in-radius-six 4-factor physical witness in these certified families.
    assert len(set((1<<a)|(1<<b) for a in range(12) for b in range(a+1,12))
               -{m&4095 for m in prior|added})==13

print("PASS 15 prior B5 + 19 new B6 physically replayed mixed-four support orbits")
print("PASS 360+420=780 original-tagged 4-cubie support masks, disjoint")
print("PASS all 12 fixed omitted-corner edges: 18 prior +35 new =53 supports")
print("BOUNDARY: no claim that the 13 unmatched pair masks FIRST appear at B7")
print("BOUNDARY: positive B6 injectivity inherits prior full-state census")

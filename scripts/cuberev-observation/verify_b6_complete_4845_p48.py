#!/usr/bin/env python3
"""Independent P48 physical exclusion certificate for all 4,845 B6 16-tag sets.

This small checker is the negative/completeness half of an exact theorem.
The independent 41-goal P48 exact 12-HTM exclusion is the separate POSITIVE
certificate; do not claim this checker alone proves those 156 survivors good.
Physical word witnesses and spatial transports are replayed, not inferred
from hand-entered support masks or the historical 54-facelet engine.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
from b6_independent_48sticker_goals import (
    EDGE_NAMES, EDGE_POSITION, EDGE_POS, CORNERS, FACES, SPATIAL, valid_pairs,
)
from verify_b6_negative_19_pairs_p48 import SEEDS, physical_support, transform_word

# Nine NEW P48 B5 full-state MITM discoveries, not from the historical B5 ZIP.
# Every word is <=5 HTM; the source search can regenerate them independently.
B5_FOUR_SEEDS = (
 (("BL","DL"),"F2 U L U' F2","D2 R' D' R D'"),
 (("BL","DR"),"L2 F U' F U","B D' B' L2 F2"),
 (("BL","UR"),"L2 F U' F' L2","B D' B D B2"),
 (("BR","DL"),"D2 F2 U' R' U","L D L' D F2"),
 (("DB","DL"),"F2 R' D' R F2","L2 U L U' L"),
 (("DB","UL"),"D2 F' R F' R'","B' L B D2 F2"),
 (("DB","UR"),"D2 F' R F D2","B' L B' L' B2"),
 (("DL","DR"),"F L' F U2 B'","L' F2 U2 B' R'"),
 (("DL","FR"),"D2 B2 U R U'","L' D' L D' B2"),
)
TAGS=frozenset(EDGE_POS+CORNERS)

def ends(core):
    m=EDGE_POSITION[core]
    return frozenset(p for p in CORNERS
                     if all(p[i]==m[i] for i in range(3) if m[i]))

def physical_orbit(a,b,r,expected=None):
    if len(a.split())>r or len(b.split())>r:
        raise AssertionError("witness violates its declared B_r radius")
    base=physical_support(a,b)
    if expected is not None and base!=expected:
        raise AssertionError("actual original-tag difference != claimed support")
    orbit=set()
    for det,perm,R in SPATIAL:
        transported=physical_support(transform_word(a,det,R),
                                     transform_word(b,det,R))
        if transported!=frozenset(R(p) for p in base):
            raise AssertionError("P48 physical spatial transport failure")
        if det==1:
            orbit.add(transported)
    return frozenset(orbit)

def triple_edge_obstructions():
    path=(Path(__file__).resolve().parents[2]/
          "data/0.28/B5_13_ORBIT_INDEPENDENT_WORD_PAIR_WITNESSES_20261104.json")
    data=json.loads(path.read_text(encoding="utf-8"))
    assert len(data["witnesses"])==13
    result=set()
    for w in data["witnesses"]:
        orb=physical_orbit(w["left"],w["right"],5)
        assert all(len(d)==3 and d<=set(EDGE_POS) for d in orb)
        result.update(orb)
    assert result==set(map(frozenset,combinations(EDGE_POS,3)))
    return result

def two_corner_obstructions():
    words=("U2 R' B D2 B' R U2 R' B D2 B' R",
           "U' B2 U L' F2 L U' B2 U L' F2 L")
    result=set()
    def inverse(t):
        return t if t.endswith("2") else t[:-1] if t.endswith("'") else t+"'"
    for w in words:
        turns=w.split()
        assert len(turns)==12
        left=" ".join(inverse(t) for t in reversed(turns[6:]))
        right=" ".join(turns[:6])
        orb=physical_orbit(left,right,6)
        assert all(len(d)==2 and d<=set(CORNERS) for d in orb)
        result.update(orb)
    expected={frozenset(q) for q in combinations(CORNERS,2)
              if sum(a!=b for a,b in zip(*q))>=2}
    assert result==expected and len(result)==16
    return result

def adjacent_b5_obstructions():
    result=set()
    for pair,a,b in B5_FOUR_SEEDS:
        wanted=ends("DL")|frozenset(EDGE_POSITION[e] for e in pair)
        orb=physical_orbit(a,b,5,wanted)
        assert len(orb)==24
        assert not result.intersection(orb)
        result.update(orb)
    assert len(result)==216
    count=Counter(frozenset(d&set(CORNERS)) for d in result)
    assert len(count)==12 and set(count.values())=={18}
    return result

def adjacent_b6_obstructions():
    result=set()
    assert len(SEEDS)==19
    for a,b in SEEDS.values():
        orb=physical_orbit(a,b,6)
        assert all(len(d)==4 and len(d&set(CORNERS))==2 for d in orb)
        assert not result.intersection(orb)
        result.update(orb)
    assert len(result)==420
    count=Counter(frozenset(d&set(CORNERS)) for d in result)
    assert len(count)==12 and set(count.values())=={35}
    return result

def audit():
    triple=triple_edge_obstructions()
    corner=two_corner_obstructions()
    b5=adjacent_b5_obstructions()
    b6=adjacent_b6_obstructions()
    assert not b5&b6
    assert len(triple|corner|b5|b6)==872
    # Independent B6 16-sensor lower bound: each deleted five-tag set
    # contains a physical B5 three-edge OR B6 nonadjacent two-corner witness.
    for omitted5 in map(frozenset,combinations(TAGS,5)):
        assert any(d<=omitted5 for d in triple|corner)
    # Each selected support has a private four-tag excluded design:
    # no *other* member of THIS finite 872-support certificate kills it.
    # This establishes inclusion-wise irredundancy, not smallest certificate
    # over every possible physical short-support family.
    family=triple|corner|b5|b6
    for support in family:
        if support in triple:
            private=support|{CORNERS[0]}
        elif support in corner:
            private=support|set(EDGE_POS[:2])
        else:
            private=support
        assert len(private)==4
        assert sum(d<=private for d in family)==1
    grades=Counter()
    survivors=set()
    for omitted in map(frozenset,combinations(TAGS,4)):
        if any(s<=omitted for s in triple):
            grades["missing_3plus_edges"]+=1
        elif any(s<=omitted for s in corner):
            grades["nonadjacent_missing_corners"]+=1
        elif omitted in b5:
            grades["B5_adjacent_four"]+=1
        elif omitted in b6:
            grades["B6_adjacent_four"]+=1
        else:
            survivors.add(omitted)
    expected=Counter({"missing_3plus_edges":2255,
                      "nonadjacent_missing_corners":1798,
                      "B5_adjacent_four":216,
                      "B6_adjacent_four":420})
    assert grades==expected,grades
    positive={ends(h)|frozenset(EDGE_POSITION[e] for e in pair)
              for h in EDGE_NAMES for pair in valid_pairs(h)}
    assert len(positive)==156 and survivors==positive
    assert sum(grades.values())==4689 and sum(grades.values())+len(survivors)==4845
    print("P48_B6_ALL_4845_NEGATIVE_CLASSIFICATION_PASS")
    print("P48_B6_15_SENSOR_LOWER_BOUND_PASS all 15504 missing-five layouts obstructed")
    print("P48_B6_872_SUPPORT_KERNEL_IRREDUNDANT every support has a private witness")
    print("PHYSICAL_SUPPORTS edge3=220 corner2=16 B5adj4=216 B6adj4=420")
    print("EXCLUSION_PARTITION 2255+1798+216+420=4689; survivors=156")
    print("POSITIVE_DEPENDENCY independently completed P48 41/41 MITM required")
    return grades,survivors

if __name__=="__main__":
    audit()

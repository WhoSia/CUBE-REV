#!/usr/bin/env python3
"""B6 geometric criterion vs independent PHYSICAL four-cubie certificates.

Run in scripts/cuberev-observation:
  python verify_b6_geometric_bridge.py /path/to/EXACT_B1_B5_SENSOR_CERTIFICATES.zip

Reads the 2026-10-30 B5 source archive and 19 literal B6 word pairs from the
sibling negative-certificate checker; reconstructs all 420 failing layouts.
Uses NO hardcoded list of eight successful B6 orbit IDs. The separate historic
8.24-million-state B6 positive proof is still needed for sufficiency.
"""
import ast
import json
import sys
import zipfile
from pathlib import Path
from itertools import combinations
from verify_b6_geometric_rule import CORNERS, EDGE_NAMES, ENDS, admissible, valid_pairs

assert len(sys.argv)==2
with zipfile.ZipFile(sys.argv[1]) as z:
    census=json.loads(z.read("b5_sixteen_layout_census.json"))
    scope={"__name__":"b5_archived_source","__file__":"independent_b4.py"}
    exec(compile(z.read("independent_b4.py"),"independent_b4.py","exec"),scope)
assert tuple(scope["E"])==EDGE_NAMES
assert scope["corner_xyz"]==sorted(CORNERS)
rotations=scope["rotation_maps"]()
assert len(rotations)==24

def transport(mask,edge_permutation,corner_permutation):
    return (sum(1<<edge_permutation[i] for i in range(12) if mask>>i&1)
            |sum(1<<(12+corner_permutation[i]) for i in range(8)
                 if mask>>(12+i)&1))

def state_after(word):
    state=scope["START"]
    for token in word.split():
        state=scope["turn"](state,scope["A"].index(token))
    return state

def difference_mask(a,b):
    ea,eb=scope["ev"](a),scope["ev"](b)
    ca,cb=scope["cv"](a),scope["cv"](b)
    return (sum(1<<i for i in range(12) if ea[i]!=eb[i])
            |sum(1<<(12+i) for i in range(8)
                 if ca[4*i:4*i+4]!=cb[4*i:4*i+4]))

def parse_witnesses():
    source=Path(__file__).with_name("verify_b6_negative_witnesses.py")
    tree=ast.parse(source.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(
            isinstance(t,ast.Name) and t.id=="W" for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError("W literal dictionary not found")

full=(1<<20)-1
representatives=[]
for mask,size in census["valid_16_orbits"]:
    missing=[i for i in range(8) if not(mask>>(12+i)&1)]
    if (sum(a!=b for a,b in
            zip(scope["corner_xyz"][missing[0]],
                scope["corner_xyz"][missing[1]]))==1):
        representatives.append((mask,size))
assert len(representatives)==27
b5_eligible=set()
for mask,size in representatives:
    b5_eligible.update(transport(mask,em,cm) for _,em,cm,_ in rotations)
assert len(b5_eligible)==576

witnesses=parse_witnesses()
assert len(witnesses)==19
physical_obstructions=set()
individual=[]
for idx,(word_a,word_b) in witnesses.items():
    a,b=state_after(word_a),state_after(word_b)
    assert a!=b and len(word_a.split())<=6 and len(word_b.split())<=6
    support=difference_mask(a,b)
    assert support.bit_count()==4
    assert (support&representatives[idx][0])==0
    orbit={transport(support,em,cm) for _,em,cm,_ in rotations}
    individual.append(orbit)
    physical_obstructions.update(orbit)
assert len({frozenset(x) for x in individual})==19
assert len(physical_obstructions)==420
assert all(full^s in b5_eligible for s in physical_obstructions)
assert len(b5_eligible-{full^s for s in physical_obstructions})==156

predicted=set()
for core_edge in EDGE_NAMES:
    corners=ENDS[core_edge]
    corner_bits=sum(1<<(12+scope["corner_xyz"].index(c)) for c in corners)
    for pair in valid_pairs(core_edge):
        edge_bits=sum(1<<EDGE_NAMES.index(e) for e in pair)
        predicted.add(full^(corner_bits|edge_bits))
assert len(predicted)==156
assert predicted<=b5_eligible
assert predicted==b5_eligible-{full^s for s in physical_obstructions}

# Verify the geometric rule on every one of 576 archived candidate layouts
# rather than relying on the 13 pair labels for one selected cube edge.
for selected in b5_eligible:
    omitted=full^selected
    corners=frozenset(scope["corner_xyz"][i] for i in range(8)
                      if omitted>>(12+i)&1)
    core_edge=next(e for e in EDGE_NAMES if ENDS[e]==corners)
    absent=tuple(EDGE_NAMES[i] for i in range(12) if omitted>>i&1)
    assert len(absent)==2
    assert admissible(core_edge,*absent)==(selected in predicted)

# Extra audit of the fixed omitted corner pair: B5=48, B6=13+35.
fixbits=(1<<12)|(1<<13)
fixed={m for m in b5_eligible if full^m&((255)<<12)==fixbits}
assert len(fixed)==48
assert len(fixed&predicted)==13
assert len(fixed-predicted)==35
print("PASS 19 independent physical four-factor witness orbits, 420 failures")
print("PASS 576 B5-eligible B6 16-tag layouts partition into 420+156")
print("PASS four-case coordinate-free rule agrees on ALL 576 layouts")
print("PASS fixed corner edge: 48 admissible B5; 13 B6 geometric survivors")
print("BOUNDARY: 156 survivors' FULL B6 injectivity is inherited from prior B6 census")

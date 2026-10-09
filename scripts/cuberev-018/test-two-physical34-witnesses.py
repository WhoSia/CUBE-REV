#!/usr/bin/env python3
"""0.18 Rubik M-star two-witness provenance and overlap court.

Re-derive all claims from the fresh *physical cube* 1192x1323 incidence
matrix and two independent real HTM four-action certificates. No SAT/CP
solver output is trusted for the asserted cover, and no global k33
impossibility follows from two local k34 witnesses.
"""
import hashlib
import json
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
assert len(sys.argv)==2, "python test-two-physical34-witnesses.py physical.json"
raw = Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(raw).hexdigest() == (
    "9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1"
), "Original 18 HTM physical model changed; STOP and re-audit."
physical=json.loads(raw)
assert physical["counts"] == {
    "literal":104976,"partitions":1913,
    "coverageTypes":1477,"maximal":1323,"bases":1192
}
cols=physical["candidates"]
src=repo/"docs/0.18"
w1=json.loads((src/"P1_NEW_34_WORD_PHYSICAL_COVER_WITNESS.json").read_text())
w2=json.loads((src/"P2_CP_SAT_34_INDEPENDENT_HTM_PASS.json").read_text())
first=w1["selectedPhysicalMaximalIndices"]
second=w2["indices"]

def verify(label, chosen, words):
    assert len(chosen)==len(words)==len(set(chosen))==34
    assert all(0<=j<1323 for j in chosen)
    assert all(cols[j]["word"]==word for j,word in zip(chosen,words))
    masks=[int(cols[j]["mask"],16) for j in chosen]
    union=0
    for mask in masks:union|=mask
    assert union.bit_count()==1192
    unique=[]
    for i,mi in enumerate(masks):
        others=0
        for j,mj in enumerate(masks):
            if i!=j:others|=mj
        unique.append((mi&~others).bit_count())
    assert min(unique)>0
    print(f"{label} PASS coverage=1192 unique_total={sum(unique)} "
          f"unique_per_word={min(unique)}..{max(unique)}")
    return sum(unique)

a=verify("NEW34",first,w1["words"])
b=verify("CPSAT34",second,w2["words"])
assert a==174 and b==178
assert len(set(first)&set(second))==9
assert len(set(first)|set(second))==59
print("CUBE_REV_018_TWO_DISTINCT_REAL_CUBE_34_WITNESSES_PASS "
      "overlap=9 combined_candidates=59")
print("GLOBAL_K33_UNSAT_NOT_PROVEN")

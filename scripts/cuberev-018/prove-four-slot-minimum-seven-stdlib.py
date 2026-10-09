#!/usr/bin/env python3
"""CUBE-REV 0.18 — independent exhaustive certificate for the 4-slot Cube block.

This checker recomputes both all-k dominance quotients from the frozen
sticker-derived 18-HTM 1192x1323 physical instance. It uses a complete
memoized set-cover search, NOT a MIP solver and NOT an assumed SAT answer.

Result: the 64 original 4-slot conditions cannot be covered by <=6 of
the 88 physical four-move words; the separately real-HTM-replayed 34-word
dictionary contains exactly 7 matching words that cover all 64.

Scope: the 4-slot connected component ONLY. The 334x80 component must
still be independently certified at k=26 for global M*=34.
"""
import argparse
import hashlib
import json
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--physical',required=True)
p.add_argument('--witness',required=True)
args=p.parse_args()
raw=Path(args.physical).read_bytes()
d=json.loads(raw)
w=json.loads(Path(args.witness).read_text())
assert d["schema"]=="cube-rev.018.cube-physical-mstar-maximal-v1"
assert d["counts"]=={"literal":104976,"partitions":1913,
 "coverageTypes":1477,"maximal":1323,"bases":1192}
original=[int(x["mask"],16) for x in d["candidates"]]
supports=[0]*1192
for j,mask in enumerate(original):
    while mask:
        b=mask&-mask
        supports[b.bit_length()-1]|=1<<j
        mask ^=b
assert all(supports)
rows=[]
for i in sorted(range(1192),key=lambda j:(supports[j].bit_count(),j)):
    if any((supports[r]&~supports[i])==0 for r in rows):
        continue
    rows.append(i)
assert len(rows)==398
for i in range(1192):
    assert any((supports[r]&~supports[i])==0 for r in rows)
projected=[sum(1<<i for i,r in enumerate(rows) if mask>>r&1)
           for mask in original]
unique={}
for j,mask in enumerate(projected):
    unique.setdefault(mask,j)
assert len(unique)==361
antichain=[]
for mask,j in sorted(unique.items(),key=lambda z:(-z[0].bit_count(),z[1])):
    if not any((mask&~other)==0 for other,_ in antichain):
        antichain.append((mask,j))
assert len(antichain)==168
for mask in projected:
    assert any((mask&~other)==0 for other,_ in antichain)

four_rows=[i for i,r in enumerate(rows) if d["bases"][r].bit_count()==4]
five_rows=[i for i,r in enumerate(rows) if d["bases"][r].bit_count()==5]
assert len(four_rows)==64 and len(five_rows)==334
four_bits=sum(1<<i for i in four_rows)
five_bits=sum(1<<i for i in five_rows)
four_indices=[j for mask,j in antichain if mask&four_bits]
five_indices=[j for mask,j in antichain if mask&five_bits]
assert len(four_indices)==88 and len(five_indices)==80
assert set(four_indices).isdisjoint(five_indices)
for mask,j in antichain:
    assert bool(mask&four_bits)!=bool(mask&five_bits)
cols=[sum(1<<r for r,i in enumerate(four_rows)
          if original[j]>>i&1) for j in four_indices]
assert len(cols)==88
assert all(cols)
assert all(any(c>>r&1 for c in cols) for r in range(64))
assert Counter(c.bit_count() for c in cols)=={14:56,12:32}
incident=[[j for j,c in enumerate(cols) if c>>i&1] for i in range(64)]
initial=(1<<64)-1
states=branches=prunes=0
t=time.monotonic()

@lru_cache(None)
def possible(uncovered,remaining):
    global states,branches,prunes
    states+=1
    if uncovered==0:
        return True
    if remaining==0:
        return False
    # Optimistic union bound: overlapping source coverage is counted twice.
    # Hence this can only prune IMPOSSIBLE branches, never valid covers.
    score=sorted(((c&uncovered).bit_count() for c in cols),reverse=True)
    if sum(score[:remaining])<uncovered.bit_count():
        prunes+=1
        return False
    options=None
    for i in range(64):
        if uncovered>>i&1:
            new=[(j,cols[j]&uncovered) for j in incident[i]]
            # Even with an impossible assumption of remaining-1 repetitions
            # of the globally best word, the union must cover uncovered.
            new=[(j,mask) for j,mask in new
                 if mask.bit_count()+(remaining-1)*score[0]
                    >=uncovered.bit_count()]
            if options is None or len(new)<len(options):
                options=new
            if not new:
                return False
    options.sort(key=lambda x:x[1].bit_count(),reverse=True)
    for j,mask in options:
        branches+=1
        if possible(uncovered&~mask,remaining-1):
            return True
    return False

assert not possible(initial,6), "A <=6-word four-slot dictionary was found"
assert possible.cache_info().currsize==states
known=list(map(int,w["indices"]))
assert len(known)==34 and len(set(known))==34
selected=[j for j in known if j in four_indices]
assert len(selected)==7
union=0
for j in selected:
    union |=sum(1<<r for r,i in enumerate(four_rows)
               if original[j]>>i&1)
assert union==initial
print("CUBE_REV_018_FOUR_SLOT_MINIMUM_SEVEN_EXHAUSTIVE_PASS",
 json.dumps({"original_physical_sha256":hashlib.sha256(raw).hexdigest(),
 "original_rows":1192,"physical_candidates":1323,
 "core_rows":398,"core_columns":168,"component_rows":64,
 "component_columns":88,"k6_impossible":True,"k7_physical_upper":True,
 "explored_states":states,"branches":branches,"optimistic_prunes":prunes,
 "elapsed_seconds":round(time.monotonic()-t,3)},sort_keys=True),flush=True)
print("CUBE_REV_018_FIVE_SLOT_MINIMUM_27_NOT_PROVEN_BY_THIS_CHECKER")

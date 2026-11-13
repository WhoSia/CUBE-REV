#!/usr/bin/env python3
"""R14-P8.34 exact identification-family saturation census.

Exhaust all 2^20 persistent full-tag layouts by upward closure of
independently physically replayed B6 difference supports (872) and
P8.30 B7 two-tag difference supports (94).

The positive verdict for B6 support-free layouts DEPENDS on independent
P8.33 41-target >=13 HTM certification; this does not rerun MITM.
The P8.30 physical 720-case code is imported and executed again.
"""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def import_file(name,filename):
    spec=importlib.util.spec_from_file_location(name,HERE/filename)
    module=importlib.util.module_from_spec(spec)
    with redirect_stdout(StringIO()):
        spec.loader.exec_module(module)
    return module

b6=import_file("b6_supports", "verify_b6_complete_4845_p48.py")
b7=import_file("b7_supports", "audit_r14_p830_independent_b7_pair_support_complete.py")
tags=tuple(b6.EDGE_POS)+tuple(b6.CORNERS)
assert len(tags)==len(set(tags))==20
tag_idx={p:i for i,p in enumerate(tags)}
assert len(b7.C)==28 and len(b7.E)==66
assert set(b7.corners)==set(b6.CORNERS)
assert set(b7.edges)==set(b6.EDGE_POS)

def support_mask(tags_set):
    return sum(1<<tag_idx[p] for p in tags_set)

def upward_bad(supports):
    """Subsets of omitted tags containing any physically witnessed support."""
    bad=bytearray(1<<20)
    for s in supports:
        assert 0 < s < (1<<20)
        bad[s]=1
    for bit in range(20):
        b=1<<bit
        # Iterate only masks having the bit; propagates from their
        # immediate subset. Supports are indexed by ORIGINAL tag labels.
        for block in range(0,1<<20,2*b):
            for mask in range(block+b,block+2*b):
                if bad[mask-b]:
                    bad[mask]=1
    return bad

triple=b6.triple_edge_obstructions()
corner=b6.two_corner_obstructions()
b5=b6.adjacent_b5_obstructions()
b6mixed=b6.adjacent_b6_obstructions()
assert [len(x) for x in (triple,corner,b5,b6mixed)]==[220,16,216,420]
B6={support_mask(d) for group in (triple,corner,b5,b6mixed) for d in group}
assert len(B6)==872
B7={support_mask(d) for d in (b7.C|b7.E)}
assert len(B7)==94
bad6=upward_bad(B6)
bad7=upward_bad(B7)
total=(1<<20)-1
hist6=Counter()
hist7=Counter()
lost=Counter()
witness6=0
for selected in range(1<<20):
    omitted=total ^ selected
    good6=(bad6[omitted]==0)
    good7=(bad7[omitted]==0)
    c=(selected>>12).bit_count()
    e=(selected&((1<<12)-1)).bit_count()
    if good6:
        hist6[c+e]+=1
        assert c+e>=16
    if good7:
        hist7[c+e]+=1
        assert c>=7 and e>=11
    assert good7 == (c>=7 and e>=11)
    assert not good7 or good6
    if good6 and not good7:lost[c+e]+=1
    if not good6:witness6+=1

assert dict(hist6)=={16:156,17:672,18:174,19:20,20:1},hist6
assert dict(hist7)=={18:96,19:20,20:1},hist7
assert dict(lost)=={16:156,17:672,18:78},lost
assert sum(hist6.values())==1023
assert sum(hist7.values())==117
assert sum(lost.values())==906
assert witness6==(1<<20)-1023
print(json.dumps({
 "status":"PASS",
 "scientific_result":"ENTIRE_STATIC_IDENTIFYING_FAMILY_SATURATES_AT_B7",
 "model":"persistent_original_cubie_full_pose",
 "all_20_tag_subsets_checked":1<<20,
 "physically_replayed_b6_obstruction_masks":len(B6),
 "physically_replayed_b7_two_tag_supports":len(B7),
 "b6_identifying_designs_by_size":dict(sorted(hist6.items())),
 "b7_identifying_designs_by_size":dict(sorted(hist7.items())),
 "b6_to_b7_lost_designs_by_size":dict(sorted(lost.items())),
 "b6_identifying_designs_total":sum(hist6.values()),
 "b7_identifying_designs_total":sum(hist7.values()),
 "b6_to_b7_lost_total":sum(lost.values()),
 "global_family_equals_b7_family":True,
 "global_identifying_designs_total":117,
 "uses_p833_41_distance_positive_premise":True,
 "full_group_b7_bfs_executed":False,
 "color_frame_horizon_proved":False
},sort_keys=True))

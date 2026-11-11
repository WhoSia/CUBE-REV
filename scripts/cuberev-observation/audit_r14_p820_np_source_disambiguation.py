#!/usr/bin/env python3
"""R14-P8.20 RAW ARCHIVE REQUIRED: identify exactly which N-P four pairs
were B5-invalid, and which four first fail at B6, for every original
native edge. Do not infer identity from the coarse 4+4 category table.

Usage:
  python scripts/cuberev-observation/audit_r14_p820_np_source_disambiguation.py \
      /path/to/CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip

The imported historical bridge replays all 19 B6 6+6 word witnesses and
loads the original B5 54-facelet archive and its 27 orbit records. This
script has not been run if the historical ZIP is unavailable. Inputs are
read-only; no PDF or archive bytes are changed.
"""
from itertools import product
from collections import Counter
import json,sys

if len(sys.argv)!=2:
    raise SystemExit('Usage: '+sys.argv[0]+' ORIGINAL_B1_B5_SENSOR_CERTIFICATES.zip')

# This module validates the historical physical archive before exporting
# b5_eligible, and independently reconstructs 19 B6 support seed orbits.
from verify_b6_geometric_bridge import (
    EDGE_NAMES, ENDS, scope, b5_eligible, physical_obstructions, full
)
from verify_b6_geometric_rule import midpoint

def np_pairs(h):
    core=ENDS[h]
    near={e for e in EDGE_NAMES if e!=h and ENDS[e]&core}
    opposite=frozenset(tuple(-v for v in c) for c in core)
    star=next(e for e in EDGE_NAMES if ENDS[e]==opposite)
    parallel={e for e in EDGE_NAMES
              if midpoint(e).index(0)==midpoint(h).index(0)
              and e not in (h,star)}
    assert len(near)==4 and len(parallel)==2
    return tuple(sorted((n,p) for n,p in product(near,parallel)))

corner_order=scope['corner_xyz']
edge_index={e:i for i,e in enumerate(EDGE_NAMES)}
output=[]
for h in EDGE_NAMES:
    corners=ENDS[h]
    corners_bits=sum(1<<(12+corner_order.index(c)) for c in corners)
    prior,new=[],[]
    for e,f in np_pairs(h):
        omitted=corners_bits|(1<<edge_index[e])|(1<<edge_index[f])
        selected=full^omitted
        if selected not in b5_eligible:
            prior.append([e,f])
            assert omitted not in physical_obstructions
        else:
            assert omitted in physical_obstructions, (h,e,f)
            new.append([e,f])
    assert len(prior)==len(new)==4
    output.append({'native_core':h,'B5_physically_invalid_pairs':prior,
                   'first_B6_physically_invalid_pairs':new})
assert len(output)==12
print(json.dumps({
 'result':'R14_P820_RAW_B5_ARCHIVE_AND_B6_P48_NP_IDENTITIES_REPLAY_PASS',
 'source':'original B5 54-facelet ZIP + 19 literal 6+6 B6 P48 collision seeds',
 'native_core_edges':12,'prior_NP_invalid':48,'new_B6_NP_invalid':48,
 'all_pairs_classified':96,'per_core_pairs':output,
 'original_source_archive_required_and_read':True
},sort_keys=True))

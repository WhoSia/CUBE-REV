#!/usr/bin/env python3
"""Cross-check rank-one parity posterior identity on P5.1 physical P48 move/slot engine.
Depends explicitly on P5.1/P5.2 sources: NOT independent P48 geometry construction.
"""
import contextlib, io, sys, importlib.util, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE

def load(name, candidates):
    for p in candidates:
        if p.exists():
            spec=importlib.util.spec_from_file_location(name,p)
            module=importlib.util.module_from_spec(spec)
            sys.modules[name]=module
            spec.loader.exec_module(module)
            return module
    raise FileNotFoundError(f"Required P48 dependency {name} absent at: {candidates}")

with contextlib.redirect_stdout(io.StringIO()):
    p51=load('audit_r14_p51_p48_group_lift',(
        ROOT/'audit_r14_p51_p48_group_lift.py',
        Path('/mnt/data/CUBEREV_028_R14_P51_P48_GROUP_LIFT.py')))
    p52=load('audit_r14_p52_two_frame_p48_posteriors',(
        ROOT/'audit_r14_p52_two_frame_p48_posteriors.py',
        Path('/mnt/data/CUBEREV_028_R14_P52_TWO_FRAME_P48_POSTERIORS.py')))
from audit_r14_p8_parity_activation import count as own_count
# Above file has top-level execution; receipt writing is reproducible.
assert len(p52.edge_words)==12 and len(p52.corner_words)==8
qE=list(p52.edge_id);qC=list(p52.corner_id)
checks=0;all_first=True;free_involutions=0
for state in p51.states[::101][:10]:
    inv=p51.inverse(state)
    for depth in (1,2,3):
        er=[];cr=[];observed_edge_positions=set();observed_corner_positions=set()
        for t in range(depth):
            # 2 distinct geometric sticker spaces sampled independently, mixed within cubie
            eq=qE[(7*t+depth)%24];cq=qC[(11*t+depth)%24]
            el=p52.edge_id[eq];cl=p52.corner_id[cq]
            er.append((el,p51.COLORS[inv[eq]]));cr.append((cl,p51.COLORS[inv[cq]]))
            observed_edge_positions.add(el//2);observed_corner_positions.add(cl//3)
        e=own_count(p52.edge_words,2,tuple(er))
        c=own_count(p52.corner_words,3,tuple(cr))
        ee=p52.count(p52.edge_words,2,tuple(er))
        cc=p52.count(p52.corner_words,3,tuple(cr))
        assert (e,c)==(ee,cc)
        if 12-len(observed_edge_positions)>=2:assert e[0]==e[1]
        if 8-len(observed_corner_positions)>=2:assert c[0]==c[1]
        n=e[0]*c[0]+e[1]*c[1]
        assert n>0,('state physical read history cannot be impossible',depth)
        assert 2*n==(e[0]+e[1])*(c[0]+c[1])+(e[0]-e[1])*(c[0]-c[1])
        checks+=1
receipt={'result':'R14_P8_P48_DEPENDENT_GEOMETRY_DP_REGRESSION_PASS',
'existing_p48_3d_engine':'CUBEREV_028_R14_P51_P48_GROUP_LIFT.py',
'existing_p48_matching_dp':'CUBEREV_028_R14_P52_TWO_FRAME_P48_POSTERIORS.py',
'new_dp_vs_existing_dp_state_prefix_comparisons':checks,
'physical_scramble_source':'P5.1 2001 checked legal 18-HTM prefixes, subset re-used',
'count_and_rank_one_parity_conservation':'all PASS',
'scope':'P48-dependent regression of orientation-aware local color readings; shares imported physical geometry and DP interpretation, not independent physical 20-frame policy'}
with open(HERE/'R14_P8_P48_GEOMETRY_REGRESSION_RECEIPT.json','w') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2))

#!/usr/bin/env python3
"""Exact 576-action, 36-color successor census for physical P48 mixed color prefixes.
No full-cube state enumeration. P5.1 geometry dependency explicit. This computes
one-frame candidate-size partitions, NOT exact future Bellman depths.
"""
import contextlib, io, importlib.util, sys, json, hashlib
from functools import lru_cache
from pathlib import Path
from collections import Counter
from itertools import product
HERE=Path(__file__).resolve().parent
p51_path=HERE/'audit_r14_p51_p48_group_lift.py'
if not p51_path.exists():p51_path=Path('/mnt/data/CUBEREV_028_R14_P51_P48_GROUP_LIFT.py')
with contextlib.redirect_stdout(io.StringIO()):
    spec=importlib.util.spec_from_file_location('p51_p82',p51_path)
    p51=importlib.util.module_from_spec(spec);sys.modules[spec.name]=p51;spec.loader.exec_module(p51)
from audit_r14_p8_parity_activation import count
faces={i:next(f for f,n in p51.FACES.items() if n==p51.SLOTS[i][1]) for i in range(48)}
EW=tuple(''.join(faces[j] for j in p51.PIECES[p]) for p in p51.EDGES)
CW=tuple(''.join(faces[j] for j in p51.PIECES[p]) for p in p51.CORNERS)
eid={sp:2*i+s for i,p in enumerate(p51.EDGES) for s,sp in enumerate(p51.PIECES[p])}
cid={sp:3*i+s for i,p in enumerate(p51.CORNERS) for s,sp in enumerate(p51.PIECES[p])}
colors=tuple('URFDLB')

@lru_cache(None)
def counts(sector,readings):
    return count(EW if sector==0 else CW,2 if sector==0 else 3,readings)

def tally(prefix_name, er,cr):
    er=tuple(sorted(er));cr=tuple(sorted(cr))
    e0=counts(0,er);c0=counts(1,cr)
    before=e0[0]*c0[0]+e0[1]*c0[1]
    assert before>0,(prefix_name,e0,c0)
    edge_children={}
    corner_children={}
    for eq in range(24):
        for col in colors:
            rr=dict(er)
            if eq in rr and rr[eq]!=col:v=(0,0)
            else:rr[eq]=col;v=counts(0,tuple(sorted(rr.items())))
            edge_children[eq,col]=v
    for cq in range(24):
        for col in colors:
            rr=dict(cr)
            if cq in rr and rr[cq]!=col:v=(0,0)
            else:rr[cq]=col;v=counts(1,tuple(sorted(rr.items())))
            corner_children[cq,col]=v
    rows=[];signs=[]
    for eq,cq in product(range(24),repeat=2):
        vals=[];nonzero=0;positive_correction=0;negative_correction=0
        for a,b in product(colors,repeat=2):
            ee=edge_children[eq,a];cc=corner_children[cq,b]
            v=ee[0]*cc[0]+ee[1]*cc[1]
            if v:
                vals.append(v);nonzero+=1
                correction=(ee[0]-ee[1])*(cc[0]-cc[1])
                positive_correction+=correction>0;negative_correction+=correction<0
        assert sum(vals)==before,(prefix_name,eq,cq,sum(vals),before)
        rows.append({'edge_local':eq,'corner_local':cq,'max_child':max(vals),
                     'outcomes':nonzero,'squared_sum':sum(v*v for v in vals),
                     'partition_desc':sorted(vals,reverse=True),
                     'nonzero_positive_parity_correction_children':positive_correction,
                     'nonzero_negative_parity_correction_children':negative_correction})
    selections=sorted(rows,key=lambda v:(v['max_child'],v['outcomes'],v['squared_sum'],v['edge_local'],v['corner_local']))
    best=selections[0]
    same_max=[r for r in rows if r['max_child']==best['max_child']]
    distinct={tuple(r['partition_desc']) for r in same_max}
    partition_digest=hashlib.sha256(json.dumps([r['partition_desc'] for r in rows],separators=(',',':')).encode()).hexdigest()
    summary={'partition_sha256':partition_digest,'prefix':prefix_name,'edge_reads':len(er),'corner_reads':len(cr),
             'edge_positions_touched':len({q//2 for q,_ in er}),
             'corner_positions_touched':len({q//3 for q,_ in cr}),
             'edge_sign_counts':e0,'corner_sign_counts':c0,'posterior_states':before,
             'exact_actions':len(rows),'branch_conservation_checks':len(rows),
             'best_query':(best['edge_local'],best['corner_local']),
             'best_max_child':best['max_child'],'best_nonempty_color_outcomes':best['outcomes'],
             'max_child_tied_actions':len(same_max),'different_full_partitions_with_same_best_max':len(distinct),
             'actions_with_nonzero_parity_correction':sum(bool(r['nonzero_positive_parity_correction_children'] or r['nonzero_negative_parity_correction_children']) for r in rows),
             'best_partition':best['partition_desc'],
             'top_five_actions':[{k:v for k,v in row.items() if k!='partition_desc'} for row in selections[:5]]}
    return summary,rows

# Resolved reference state: use exact P5.1 physical orientation and color order.
solvedE=tuple((j,EW[j//2][j%2]) for j in range(24))
solvedC=tuple((j,CW[j//3][j%3]) for j in range(24))
cases=[('initial',(),()),
       ('mixed_two_partial',solvedE[:1]+solvedE[2:3],solvedC[:1]+solvedC[3:4]),
       ('ten_edge_six_corner_completed',solvedE[:20],solvedC[:18]),
       ('eleven_edge_seven_corner_completed',solvedE[:22],solvedC[:21]),
       ('partial_near_gate_11E_7C',tuple(solvedE[2*i] for i in range(11)),tuple(solvedC[3*i] for i in range(7)))]
results=[]
for name,er,cr in cases:
    summary,rows=tally(name,er,cr)
    results.append(summary)
    print(name,'belief=',summary['posterior_states'],'best_child=',summary['best_max_child'],'actions_corr=',summary['actions_with_nonzero_parity_correction'],flush=True)
receipt={'result':'R14_P82_EXACT_576_PHYSICAL_P48_NEXT_QUERY_PARTITIONS_PASS',
         'physical_geometry_dependency':str(p51_path),
         'model':'Full 12E8C physically ordered sticker slots; exact sign-resolved matching DP; one extra paired query, all 576 actions and all 36 color outcomes',
         'prefixes':results,'total_query_action_conservation_tests':sum(r['branch_conservation_checks'] for r in results),
         'limitations':'One-step 36-color branch cardinalities, not a global Bellman quotient, adaptive 20-frame decoder or universal 21 lower bound.'}
out=HERE/'R14_P82_MIXED_P48_SUCCESSOR_PARTITIONS_RECEIPT.json'
out.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print('RESULT',receipt['result'],flush=True)

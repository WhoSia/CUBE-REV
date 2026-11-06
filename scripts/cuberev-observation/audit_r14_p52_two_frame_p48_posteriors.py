#!/usr/bin/env python3
"""R14-P5.2: exact physical 3D-derived P48 two-frame posterior branch court.
Imports the active standalone P5.1 physical geometry and legal orbit checks.
Computes 3 root color relation classes x 12 second-query stabilizer orbits
using parity-preserving exact bitmask-matching counts, no 43e18 enumeration.
The immediate minimax residual cardinality is NOT a depth-20 optimal policy.
"""
from collections import Counter
from functools import lru_cache
from itertools import product
import contextlib, io, json, hashlib
with contextlib.redirect_stdout(io.StringIO()):
    from audit_r14_p51_p48_group_lift import PIECES,EDGES,CORNERS,SLOTS,FACES,q0,H_orbits,legal

face_color={i: next(f for f,n in FACES.items() if n==SLOTS[i][1]) for i in range(48)}
edge_words=tuple(''.join(face_color[i] for i in PIECES[p]) for p in EDGES)
corner_words=tuple(''.join(face_color[i] for i in PIECES[p]) for p in CORNERS)
assert len(set(map(frozenset,edge_words)))==12
assert len(set(map(frozenset,corner_words)))==8
assert all(len(t)==2 for t in edge_words) and all(len(t)==3 for t in corner_words)

edge_id={j:2*i+k for i,p in enumerate(EDGES) for k,j in enumerate(PIECES[p])}
corner_id={j:3*i+k for i,p in enumerate(CORNERS) for k,j in enumerate(PIECES[p])}

@lru_cache(None)
def count(types,mod,readings):
    n=len(types)
    wanted=dict(readings)
    if any(k==kk and v!=vv for k,v in readings for kk,vv in readings):return (0,0)
    options=[]
    for i in range(n):
        opts=[]
        for label,w in enumerate(types):
            for rot in range(mod):
                if all(w[(side+rot)%mod]==color for j,color in wanted.items() if j//mod==i for side in [j%mod]):
                    opts.append((label,rot))
        options.append(tuple(opts))
    @lru_cache(None)
    def dp(mask,pp,residue):
        i=mask.bit_count()
        if i==n:return (int(residue==0 and pp==0),int(residue==0 and pp==1))
        a=b=0
        for label,rot in options[i]:
            if mask>>label&1:continue
            inversion=(mask>>(label+1)).bit_count()&1
            u,v=dp(mask|1<<label,pp^inversion,(residue+rot)%mod)
            a+=u;b+=v
        return a,b
    return dp(0,0,0)

E0=edge_id[q0[0]];C0=corner_id[q0[1]]
row=[]
full=43252003274489856000
for title,first in [('same',('U','U')),('opposite',('U','D')),('adjacent',('U','R'))]:
    ce,cc=first
    efirst=count(edge_words,2,((E0,ce),))
    cfirst=count(corner_words,3,((C0,cc),))
    before=sum(efirst[p]*cfirst[p] for p in (0,1))
    assert before==full//36,(title,before)
    for rep,size in H_orbits:
        ei=edge_id[rep[0]];ci=corner_id[rep[1]]
        tally=Counter()
        for ecolor,ccolor in product('URFDLB',repeat=2):
            er=tuple(sorted({(E0,ce),(ei,ecolor)}))
            cr=tuple(sorted({(C0,cc),(ci,ccolor)}))
            E=count(edge_words,2,er)
            C=count(corner_words,3,cr)
            b=sum(E[p]*C[p] for p in (0,1))
            if b:tally[(ecolor,ccolor)]=b
        assert sum(tally.values())==before,(title,rep,sum(tally.values()),before)
        row.append({'root_relation':title,'root_response':first,'second_query_spatial':rep,'second_query_local_ids':[ei,ci],
                    'stabilizer_orbit_size':size,'nonempty_second_outcomes':len(tally),
                    'largest_posterior':max(tally.values()),
                    'worst_cell_fraction_of_first_posterior':f'{max(tally.values())}/{before}',
                    'outcome_sizes_descending':sorted(tally.values(),reverse=True)})
assert len(row)==36
best={}
for kind in ('same','opposite','adjacent'):
    choices=[r for r in row if r['root_relation']==kind]
    minworst=min(r['largest_posterior'] for r in choices)
    best[kind]=[r for r in choices if r['largest_posterior']==minworst]
assert all(best[k] for k in best)
receipt={
  'result':'R14_P52_EXACT_P48_TWO_FRAME_POSTERIORS_PASS',
  'full_initial_states':full,'first_posterior_states':full//36,
  'first_color_relation_classes':3,'second_query_stabilizer_orbits_per_first_class':12,
  'exact_query_classes_audited':len(row),'all_two_frame_branch_counts_sum_to_prior':True,
  'top_immediate_minimax_posterior_by_root_relation':{k:v[0]['largest_posterior'] for k,v in best.items()},
  'number_tied_immediate_optimal_orbits':{k:len(v) for k,v in best.items()},
  'best_query_representatives':{k:[x['second_query_local_ids'] for x in v] for k,v in best.items()},
  'rows':row,
  'scope_limit':'exact posterior cardinalities only, not exact future Bellman depth or globally optimal 20-frame cube decoder',
}
print(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2))

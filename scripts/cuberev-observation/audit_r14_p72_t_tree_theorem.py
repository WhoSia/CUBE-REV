#!/usr/bin/env python3
"""R14-P7.2 finite theorem: T-shaped edge graph iff deterministic one-step regret.
Uses published 495-row root minimax receipt as an EXPLICIT dependency;
independently recomputes exact relevant Bellman values and 12-state branch witnesses.
No physical full-cube adaptive-depth claim.
"""
from collections import Counter,defaultdict,deque
from functools import lru_cache
from itertools import permutations,product,combinations
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
TYPES=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
PAIRS=(('U','D'),('R','L'),('F','B'))
known=json.loads((HERE/'R14_P7_ALL_495_LOOKAHEAD_RESULTS.json').read_text())
assert known['result']=='R14_P7_ALL_495_TWO_STEP_LOOKAHEAD_PASS'
rows={frozenset(r['types']):r for r in known['rows']}
assert len(rows)==495
edges={frozenset(e):e for e in TYPES}
transforms=[]
for target in permutations(range(3)):
    for flips in product((0,1),repeat=3):
        f={}
        for i,(a,b) in enumerate(PAIRS):
            dest=PAIRS[target[i]]
            f[a],f[b]=dest[flips[i]],dest[1-flips[i]]
        transforms.append({t:edges[frozenset(f[z] for z in t)] for t in TYPES})
assert len(transforms)==48 and len({tuple(t[z] for z in TYPES) for t in transforms})==48

def canonical(L):return min(tuple(sorted(t[z] for z in L)) for t in transforms)
def degrees(L):return tuple(sorted(Counter(x for e in L for x in e).values(),reverse=True))
class_map=defaultdict(list)
for L,row in rows.items():
    class_map[canonical(L)].append(row)
assert len(class_map)==18
orbits=[]
for rep,rs in sorted(class_map.items()):
    d=Counter(v['exact'] for v in rs)
    g=Counter(v['greedy']-v['exact'] for v in rs)
    two=Counter(v['two_step']-v['exact'] for v in rs)
    assert len(d)==1 and len(g)==1 and two=={0:len(rs)}
    deg=degrees(rep)
    fail=next(iter(g))==1
    assert fail==(deg==(3,2,1,1,1)), (rep,fail,deg)
    orbits.append({'representative':rep,'size':len(rs),'degree_sequence':deg,
                   'exact_depth':next(iter(d)),'one_step_regret':next(iter(g)),
                   'two_step_regret':0})
assert sum(a['size'] for a in orbits)==495
assert sorted(a['size'] for a in orbits if a['one_step_regret']==1)==[24,48,48]
assert sum(degrees(L)==(3,2,1,1,1) for L in rows)==6*4*5==120

# Independent explicit 12-state local falsifiers (do not treat orbit covariance of
# the particular deterministic tie-break as automatic; it is checked on all 495 rows).
failures=[]
for O in orbits:
    if not O['one_step_regret']: continue
    L=O['representative']
    words=[]
    for p in permutations(range(4)):
        if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2:continue
        for z in product((0,1),repeat=3):
            flips=z+(sum(z)%2,)
            words.append(''.join(L[p[i]][(j+flips[i])%2] for i in range(4) for j in range(2)))
    assert len(set(words))==96
    cells=[{} for _ in range(8)]
    for i,w in enumerate(words):
        for q,c in enumerate(w):cells[q][c]=cells[q].get(c,0)|(1<<i)
    def kids(B,q):return [(y,v) for y,m in cells[q].items() if (v:=B&m)]
    @lru_cache(None)
    def D(B):
        if B.bit_count()==1:return 0
        return 1+min(max(D(z) for _,z in outcomes) for q in range(8) if len(outcomes:=kids(B,q))>1)
    @lru_cache(None)
    def V(B):
        if B.bit_count()==1:return 1
        return min(max(z.bit_count() for _,z in outcomes) for q in range(8) if len(outcomes:=kids(B,q))>1)
    def options(B):
        out=[]
        for q in range(8):
            cs=kids(B,q)
            if len(cs)<2:continue
            ns=[z.bit_count() for _,z in cs]
            g=(max(ns),sum(v*v for v in ns),q)
            l=(max(V(z) for _,z in cs),*g)
            out.append((g,l,1+max(D(z) for _,z in cs),q,cs))
        return out
    whole=(1<<96)-1; assert D(whole)==O['exact_depth']
    work=deque([(whole,[])]);seen=set()
    found=None
    while work:
        B,h=work.popleft()
        if B.bit_count()==1 or B in seen:continue
        seen.add(B)
        os=options(B)
        greedy=min(os,key=lambda e:e[0]); look=min(os,key=lambda e:e[1])
        if greedy[2]>D(B):
            found=(B,h,greedy,look)
            break
        for y,child in greedy[4]:work.append((child,h+[(greedy[3],y)]))
    assert found is not None
    B,h,g,l=found
    assert len(h)==2 and B.bit_count()==12 and D(B)==2 and g[2]==3 and l[2]==2
    # The greedy-selected 'four remaining states' observation cell has no
    # single facelet query whose outputs are all distinct.
    hard=[]
    for y,child in g[4]:
        if child.bit_count()!=4:continue
        possible=[q for q in range(8) if len(kids(child,q))==4]
        if not possible:
            hard.append({'outcome':y,'four_legal_states':[words[ix] for ix in range(96) if child>>ix&1],
                         'max_one_read_distinct_colors':max(len(kids(child,q)) for q in range(8))})
    assert hard
    assert all(len(kids(z,q))==z.bit_count() for _,z in l[4] for q in [next(q for q in range(8) if len(kids(z,q))==z.bit_count())])
    failures.append({'representative':L,'orbit_size':O['size'],'prefix':[{'facelet_slot':q,'color':y} for q,y in h],
      'remaining_candidate_states':B.bit_count(),'true_remaining_optimum':D(B),
      'greedy':{'facelet_slot':g[3],'immediate_score':g[0][:2], 'lookahead_score':g[1][0],
                'true_remaining_depth_if_chosen':g[2], 'color_branch_sizes':{y:z.bit_count() for y,z in g[4]},
                'unresolvable_four_state_color_branches':hard},
      'two_step':{'facelet_slot':l[3],'immediate_score':l[0][:2],'lookahead_score':l[1][0],
                  'true_remaining_depth_if_chosen':l[2], 'color_branch_sizes':{y:z.bit_count() for y,z in l[4]},
                  'each_next_branch_one_read_separable':all(any(len(kids(z,q))==z.bit_count() for q in range(8)) for y,z in l[4])}})

result={'result':'R14_P72_T_TREE_EXACT_REGRET_CHARACTERIZATION_PASS',
        'scope':'495 parity-conditioned four-edge 96-state residuals, fixed immediate maximum/sum-of-squares/query-index policy only',
        'edge_graph_color_automorphisms':48,'all_four_edge_sets':495,'graph_orbits':18,
        'one_step_failure_if_and_only_if_degree_sequence':[3,2,1,1,1],
        'failure_sets':120,'failure_orbit_sizes':[24,48,48],
        'two_step_optimal_all':495,'combinatorial_count_120':'6 central colors * 4 choices of three incident edges * 5 pendant extensions',
        'orbits':orbits,'three_exact_12_state_branch_witnesses':failures,
        'limitation':'Classification uses prior all-495 exact AND-OR receipt. Branch witnesses independently regenerate states and recompute AND-OR Bellman on 3 representatives. No universal five-edge result or full-cube horizon.'}
(HERE/'R14_P72_T_TREE_EXACT_REGRET_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('orbits','three_exact_12_state_branch_witnesses')},indent=2))
print('all three explicit T-graph local collision courts PASS')

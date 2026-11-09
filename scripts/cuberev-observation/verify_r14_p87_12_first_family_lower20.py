#!/usr/bin/env python3
"""Independent exact FROZENSET impossibility of seven extra edge queries
for the hard first-12-edge-facelet pattern, even with a FREE parity oracle.
This is a lower bound for the specified 12-first-scan strategy family ONLY,
not the unrestricted full 3x3x3 two-probe 19-frame problem.
"""
from functools import lru_cache
from collections import defaultdict
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
E=('DL','BL','FL','UL','DB','DF','UB','UF','DR','BR','FR','UR')
first='RRRFFFLLLBBB'
# Independent generator: DFS through physical unordered edge-color types,
# respecting orientation from the observed first color and even flip sum.
choices=[]
for c in first:
    choices.append([(j,word[1-rot],rot) for j,word in enumerate(E) for rot in (0,1) if word[rot]==c])
S=[[],[]]
def dfs(i,used,flip,types,second):
    if i==12:
        if flip==0:
            p=sum(types[j]>types[k] for j in range(12) for k in range(j+1,12))%2
            S[p].append(''.join(second))
        return
    for label,other,rot in choices[i]:
        if label not in used:
            dfs(i+1,used|{label},flip^rot,types+[label],second+[other])
dfs(0,set(),0,[],[])
assert [len(v) for v in S]==[1296,1296]
results=[]
for p in range(2):
    words=tuple(S[p]); qgroup=[]
    for q in range(12):
        out=defaultdict(set)
        for i,w in enumerate(words):out[w[q]].add(i)
        qgroup.append(tuple(map(frozenset,out.values())))
    @lru_cache(None)
    def win(B,k):
        if len(B)<=1:return True
        if k<=0 or len(B)>4**k:return False
        options=[]
        for q in range(12):
            children=tuple(B&x for x in qgroup[q] if B&x)
            if len(children)<2:continue
            largest=max(map(len,children))
            if largest>4**(k-1):continue
            options.append((largest,q,children))
        for _,q,children in sorted(options,key=lambda x:(x[0],x[1])):
            if all(win(z,k-1) for z in sorted(children,key=len,reverse=True)):
                return True
        return False
    B=frozenset(range(len(words)))
    w7=win(B,7);w8=win(B,8)
    assert (w7,w8)==(False,True)
    blocked=[]
    for q in range(12):
        outcomes=defaultdict(set)
        for i,w in enumerate(words):outcomes[w[q]].add(i)
        bad=[(c,len(z)) for c,z in outcomes.items() if not win(frozenset(z),6)]
        assert bad
        blocked.append({'first_extra_query':q,'adversarial_color':sorted(bad)[0][0],
                        'surviving_candidates':sorted(bad)[0][1]})
    results.append({'parity':p,'states':len(words),'seven_extra_query_decision_tree_possible':w7,
                    'eight_extra_query_decision_tree_possible':w8,
                    'twelve_root_query_obstructions':blocked,'cache_nodes':win.cache_info().currsize})
receipt={
 'result':'R14_P87_INDEPENDENT_FROZENSET_PARITY_ORACLE_LOWER20_FOR_12_FIRST_SCAN_PASS',
 'specific_first_12_edge_colors':first,
 'source_edge_types':E,
 'edge_orientation_total_even':True,
 'full_initial_even_flip_edges':2592,
 'unrestricted_edge_permutation_sign_stratum_sizes':[1296,1296],
 'even_if_common_corner_parity_revealed_free_after_frame12':True,
 'each_parity_seven_mate_queries_impossible':True,
 'each_parity_eight_mate_queries_sufficient':True,
 'family_lower_bound_frames':20,
 'twelve_first_observations':'one prescribed first-side sticker per each of 12 spatial edge positions',
 'not_a_global_lower_bound':'A different adaptive schedule of the FIRST 12 edge reads could conceivably finish in 18 or 19; no universal claim.',
 'strata':results}
(HERE/'R14_P87_INDEPENDENT_12_FIRST_HARD_LOWER_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['result'],'states',sum(len(s) for s in S),'cache_nodes',sum(x['cache_nodes'] for x in results))

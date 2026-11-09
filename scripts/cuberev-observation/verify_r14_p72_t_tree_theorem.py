#!/usr/bin/env python3
"""Independent check of P7.2 T-graph / one-step failure equivalence and three local branch proofs.
No imports from P7.2 producer or P7.1 producer.
"""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import json
D=Path(__file__).resolve().parent
old=json.loads((D/'R14_P7_ALL_495_LOOKAHEAD_RESULTS.json').read_text())
res=json.loads((D/'R14_P72_T_TREE_EXACT_REGRET_RECEIPT.json').read_text())
assert len(old['rows'])==495 and len(res['orbits'])==18 and len(res['three_exact_12_state_branch_witnesses'])==3
faces=('U','D','R','L','F','B')
colors={'U':'D','D':'U','R':'L','L':'R','F':'B','B':'F'}
labels=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
assert len(labels)==12
counts=Counter();bad=[]
for a in old['rows']:
    L=a['types'];deg=Counter(v for e in L for v in e)
    t=sorted(deg.values(),reverse=True)==[3,2,1,1,1]
    assert (a['greedy']>a['exact'])==t
    assert a['two_step']==a['exact']
    counts[(t,a['exact'],a['greedy'],a['two_step'])]+=1
    if t:bad.append(tuple(L))
assert len(bad)==120
# Count independently from the K_{2,2,2} graph without relying on all-495 rows:
all_t=[L for L in combinations(labels,4) if sorted(Counter(v for e in L for v in e).values(),reverse=True)==[3,2,1,1,1]]
assert len(all_t)==120 and set(all_t)==set(bad)
# For each central color: choose a three-edge star and a pendant to a NEW color.
construct=set()
for center in faces:
    neighbors=[x for x in faces if x!=center and x!=colors[center]]
    for three in combinations(neighbors,3):
        star=frozenset(next(e for e in labels if set(e)=={center,x}) for x in three)
        for attachment in three:
            for endpoint in faces:
                if endpoint in (center,*three):continue
                if endpoint==colors[attachment]:continue
                pendant=next(e for e in labels if set(e)=={attachment,endpoint})
                construct.add(star|{pendant})
assert len(construct)==120 and len(construct)==len(bad)
for witness in res['three_exact_12_state_branch_witnesses']:
    L=witness['representative']
    assert sorted(Counter(v for e in L for v in e).values(),reverse=True)==[3,2,1,1,1]
    words=[]
    for perm in permutations(range(4)):
        if sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))%2:continue
        for f in product((0,1),repeat=3):
            o=f+(sum(f)%2,)
            words.append(''.join(L[perm[i]][(j+o[i])%2] for i in range(4) for j in range(2)))
    assert len(set(words))==96
    curr=words
    for h in witness['prefix']:
        q=h['facelet_slot'];c=h['color']
        curr=[w for w in curr if w[q]==c]
    assert len(curr)==12
    greedy=witness['greedy'];two=witness['two_step']
    def bins(query):
        d={}
        for w in curr:d.setdefault(w[query],[]).append(w)
        return d
    bg=bins(greedy['facelet_slot']);bt=bins(two['facelet_slot'])
    assert {y:len(z) for y,z in bg.items()}==greedy['color_branch_sizes']
    assert {y:len(z) for y,z in bt.items()}==two['color_branch_sizes']
    assert max(map(len,bg.values()))==max(map(len,bt.values()))==4
    assert sum(len(v)**2 for v in bg.values())==36
    assert sum(len(v)**2 for v in bt.values())==48
    assert all(any(len(set(w[q] for w in child))==len(child) for q in range(8)) for child in bt.values())
    # The bad decision has an outcome whose 4 states cannot be split by ANY
    # single remaining facelet query; this is a concrete depth-2 impossibility.
    assert any(len(child)==4 and all(len(set(w[q] for w in child))<4 for q in range(8)) for child in bg.values())
    for record in greedy['unresolvable_four_state_color_branches']:
        assert set(record['four_legal_states'])==set(bg[record['outcome']])
        assert record['max_one_read_distinct_colors']<4
print('R14_P72_INDEPENDENT_T_TREE_120_EXACT_AND_3_BRANCH_WITNESSES_PASS')

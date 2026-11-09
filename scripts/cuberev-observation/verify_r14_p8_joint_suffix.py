#!/usr/bin/env python3
"""Independent exact-state test: 2 unread edge+2 unread corner positions, coupled parity.
Works in a small explicitly enumerated suffix of full 12E/8C labeling; exact minimax
for freely selectable one-edge/one-corner paired-facelet queries. Not a full P48 lift.
"""
from itertools import permutations,product
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
E=('BL','BR');C=('DBL','DRB')

def par(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def states(T,k):
    ret=[[],[]]
    for p in permutations(range(len(T))):
        for oo in product(range(k),repeat=len(T)):
            if sum(oo)%k:continue
            word=''.join(T[p[i]][(s+oo[i])%k] for i in range(len(T)) for s in range(k))
            ret[par(p)].append(word)
    return ret

es=states(E,2);cs=states(C,3)
assert list(map(len,es))==[2,2] and list(map(len,cs))==[3,3]
X=[(e,c,p) for p in range(2) for e in es[p] for c in cs[p]]
assert len(X)==12
Qs=list(product(range(4),range(6)))

# Direct frozenset Bellman minimax to check all complete policies.
@lru_cache(None)
def solve(B):
    if len(B)==1:return 0,None
    best=99;query=None
    for q in Qs:
        buckets={}
        for ix in B:
            e,c,_=X[ix];label=(e[q[0]],c[q[1]])
            buckets.setdefault(label,set()).add(ix)
        if len(buckets)==1:continue
        ds=[solve(frozenset(k))[0] for k in buckets.values()]
        D=1+max(ds)
        if D<best:best=D;query=q
    return best,query

full=frozenset(range(len(X)))
optimal,q0=solve(full)
assert optimal<6
hist=Counter();terminal=0
for target in range(len(X)):
    belief=full;steps=0
    while len(belief)>1:
        _,q=solve(belief)
        assert q is not None
        observed=(X[target][0][q[0]],X[target][1][q[1]])
        belief=frozenset(i for i in belief if (X[i][0][q[0]],X[i][1][q[1]])==observed)
        steps+=1
    assert belief==frozenset([target])
    hist[steps]+=1
    terminal+=1

# Exact parity oracle: the same 12 states, with the true parity exposed for free.
parity_depths=[]
for p in range(2):
    B=frozenset(i for i,x in enumerate(X) if x[2]==p)
    parity_depths.append(solve(B)[0])
# Complete first-query split profile, and verify posterior values by independent enumeration.
bucket=Counter((e[q0[0]],c[q0[1]]) for e,c,_ in X)
assert sum(bucket.values())==12
receipt={'result':'R14_P8_2E2C_COUPLED_PARITY_EXACT_MINIMAX_PASS',
'legal_suffix_states':len(X),'parity_strata_sizes':[6,6],
'joint_pair_queries':len(Qs),'optimal_worst_paired_reads':optimal,
'optimal_first_query':q0,
'first_query_outcomes':{''.join(k):v for k,v in sorted(bucket.items())},
'optimal_policy_all_state_replays':terminal,'policy_target_depth_histogram':dict(hist),
'free_parity_oracle_optimal_depths':parity_depths,
'scope':'Tiny 2E+2C known identities and orientation-sum reference, freely choosable paired facelet queries. Not full-cube 20-frame proof.'}
with open(Path(__file__).with_name('R14_P8_2E2C_COUPLED_SUFFIX_RECEIPT.json'),'w') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2))

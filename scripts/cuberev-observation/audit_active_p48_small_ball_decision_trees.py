#!/usr/bin/env python3
"""Exact B1/B2 adaptive versus nonadaptive ideal slot-query pilot.

Every query selects one initial edge slot and one initial corner slot; the
P48 96-position joint orbit lets two fixed physical probes address any such
pair by known HTM turns. Measured values equal full original-cubie factors of
the inverse cube state. Action costs are deliberately kept separate.
Fail closed on exhausted search budgets; do NOT infer a B6 adaptive optimum.
"""
from collections import defaultdict
from itertools import combinations
from b6_independent_48sticker_goals import MOVES, compose, inverse, factor_state
from active_p48_fixed_site_scan import joint_position_words

class BudgetExceeded(Exception):pass

def ball(radius):
    identity=bytes(range(48))
    seen={identity};frontier={identity};sizes=[1]
    for i in range(radius):
        nxt={compose(move,s) for s in frontier for move in MOVES.values()}
        frontier=nxt-seen
        seen.update(frontier)
        sizes.append(len(frontier))
    assert sizes==[1,18,243,3240][:radius+1],sizes
    return tuple(sorted(seen)),sizes

def observations(states):
    factors=[factor_state(inverse(s)) for s in states]
    queries=tuple((e,c) for e in range(12) for c in range(8))
    assert len(joint_position_words())==len(queries)==96
    rows=[tuple(f[e]*24+f[12+c] for f in factors) for e,c in queries]
    return factors,queries,rows

def nonadaptive_witness(factors,k):
    """Exhaust all k-edge/k-corner site selections, not arbitrary actions."""
    assert 0<=k<=3
    n=len(factors)
    for edges in combinations(range(12),k):
        for corners in combinations(range(8),k):
            slots=edges+tuple(12+c for c in corners)
            if len({tuple(f[i] for i in slots) for f in factors})==n:
                return edges,corners
    return None

def can_adapt(rows,depth,budget=200000):
    """Exact recursively partitioned belief-state decision, budget is a gate."""
    n=len(rows[0]); cache={};nodes=[0]
    def check(subset,k):
        if len(subset)<=1:return True
        if k==0:return False
        key=(subset,k)
        if key in cache:return cache[key]
        nodes[0]+=1
        if nodes[0]>budget:raise BudgetExceeded((k,len(subset),nodes[0]))
        if k==1:
            result=any(len({row[i] for i in subset})==len(subset) for row in rows)
            cache[key]=result;return result
        for row in rows:
            partitions=defaultdict(list)
            for i in subset:partitions[row[i]].append(i)
            if len(partitions)<=1:continue
            if all(check(tuple(g),k-1) for g in partitions.values()):
                cache[key]=True;return True
        cache[key]=False
        return False
    success=check(tuple(range(n)),depth)
    return success,nodes[0],len(cache)

def audit():
    records=[]
    for radius in (1,2):
        states,counts=ball(radius)
        factors,queries,rows=observations(states)
        nonadaptive=None
        for k in (1,2,3):
            if nonadaptive_witness(factors,k) is not None:
                nonadaptive=k;break
        if nonadaptive is None:raise AssertionError("no small nonadaptive certificate")
        adaptive=None
        for k in range(1,nonadaptive+1):
            verdict,nodes,cache=can_adapt(rows,k)
            if verdict:
                adaptive=k;break
        assert adaptive is not None and adaptive<=nonadaptive
        assert len(states)=={1:19,2:262}[radius]
        records.append((radius,len(states),adaptive,nonadaptive))
        print(f"ACTIVE_SMALL_B{radius}_EXACT states={len(states)} adaptive={adaptive} nonadaptive={nonadaptive}")
    print("BOUNDARY no B6 adaptive horizon determined from the B1/B2 pilot")
    return records

if __name__=="__main__":audit()

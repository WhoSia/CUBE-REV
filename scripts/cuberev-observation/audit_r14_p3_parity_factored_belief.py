#!/usr/bin/env python3
"""R14-P3: exact parity-factored posterior under adaptive dual facelet reads.

Finite orientation/permutation model with five edge types and three corner types.
This is an algebraic verification court, NOT a source-independent 48-sticker
geometric certification or a full-cube adaptive 20-frame solver.
"""
import hashlib
import itertools
import json
from collections import Counter, defaultdict

EDGES = ('UR', 'UF', 'UL', 'UB', 'FR')
CORNERS = ('URF', 'UFL', 'ULB')  # fixed cyclic signature convention

def parity(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1,len(p))) % 2

def make_edges():
    by = ([], [])
    for perm in itertools.permutations(range(5)):
        for flips in itertools.product(range(2), repeat=5):
            if sum(flips) % 2: continue
            val = ''.join(EDGES[perm[pos]][(side + flips[pos]) % 2]
                          for pos in range(5) for side in range(2))
            by[parity(perm)].append(val)
    assert [len(z) for z in by] == [960,960]
    return tuple(tuple(z) for z in by)

def make_corners():
    by = ([], [])
    for perm in itertools.permutations(range(3)):
        for twists in itertools.product(range(3), repeat=3):
            if sum(twists) % 3: continue
            val = ''.join(CORNERS[perm[pos]][(side+twists[pos])%3]
                          for pos in range(3) for side in range(3))
            by[parity(perm)].append(val)
    assert [len(z) for z in by] == [27,27]
    return tuple(tuple(z) for z in by)

def choose(history):
    if not history: return (0,0)
    if len(history)==1:
        return ((ord(history[0][0])+1)%10,(ord(history[0][1])+2)%9)
    return ((ord(history[0][0])+ord(history[-1][1])+3)%10,
            (ord(history[0][1])+ord(history[-1][0])+5)%9)

def transcript(e,c):
    h=()
    for _ in range(3):
        qi,qj=choose(h)
        h=h+((e[qi],c[qj]),)
    return h

def filtered_states(E,C,h):
    # Recover the exact query schedule from the realized adaptive transcript.
    eq,cq=[],[]
    sub=()
    for o in h:
        i,j=choose(sub)
        eq.append((i,o[0]));cq.append((j,o[1]))
        sub=sub+(o,)
    ee=tuple(tuple(e for e in E[p] if all(e[i]==color for i,color in eq))
             for p in (0,1))
    cc=tuple(tuple(c for c in C[p] if all(c[j]==color for j,color in cq))
             for p in (0,1))
    return ee,cc

def next_partition(E,C,ei,cj):
    histogram=Counter()
    for p in (0,1):
        ec=Counter(e[ei] for e in E[p])
        cc=Counter(c[cj] for c in C[p])
        for a,na in ec.items():
            for b,nb in cc.items(): histogram[(a,b)]+=na*nb
    return tuple(sorted(histogram.items()))

def main():
    E=make_edges();C=make_corners()
    total=sum(len(E[p])*len(C[p]) for p in (0,1))
    assert total==51840
    naive=(sum(map(len,E)))*(sum(map(len,C)))
    assert naive==2*total

    direct=Counter()
    for p in (0,1):
        for e in E[p]:
            for c in C[p]:
                direct[transcript(e,c)]+=1
    assert sum(direct.values())==total
    signatures=defaultdict(list)
    for h,n in direct.items():
        ee,cc=filtered_states(E,C,h)
        factored=sum(len(ee[p])*len(cc[p]) for p in (0,1))
        assert factored==n,(h,factored,n)
        sig=tuple(len(ee[p]) for p in (0,1))+tuple(len(cc[p]) for p in (0,1))
        signatures[sig].append((h,ee,cc))

    # Exact counterexample to cardinality-only representation sufficiency:
    # equal four parity-class marginal sizes, but different next-read partitions.
    counter=None
    for sig,items in signatures.items():
        if len(items)<2: continue
        for edge_slot in range(10):
            for corner_slot in range(9):
                partitions={}
                for h,ee,cc in items:
                    part=next_partition(ee,cc,edge_slot,corner_slot)
                    shape=tuple(sorted((n for _,n in part),reverse=True))
                    if len(shape)<2: continue
                    prev=partitions.get(shape)
                    if prev is None: partitions[shape]=(h,ee,cc)
                    if len(partitions)>=2:
                        (pa,ta),(pb,tb)=list(partitions.items())[:2]
                        counter={"signature":sig,"query":[edge_slot,corner_slot],
                                 "history_a":ta[0],"history_b":tb[0],
                                 "response_branch_sizes_a":pa,"response_branch_sizes_b":pb}
                        break
                if counter: break
            if counter: break
        if counter: break
    assert counter is not None, 'No cardinality aliasing witness found'
    assert tuple(counter['response_branch_sizes_a'])!=tuple(counter['response_branch_sizes_b'])

    payload={
        'result':'R14_P3_PARITY_FACTOR_BELIEF_PASS',
        'scope':'finite 5-edge/3-corner legal parity-linked residual algebra; not 48-sticker physical replay',
        'edge_states_by_permutation_parity':[len(x) for x in E],
        'corner_states_by_permutation_parity':[len(x) for x in C],
        'legal_joint_states':total,'naive_independent_joint_states':naive,
        'adaptive_frames':3,'observed_distinct_histories':len(direct),
        'all_histories_factorization_verified':True,
        'insufficient_marginal_cardinality_witness':counter,
        'initial_query_pairs':{'first':choose(())},
        'direct_histogram_sha256':hashlib.sha256('\n'.join(
            str((h,n)) for h,n in sorted(direct.items())).encode()).hexdigest()
    }
    print(json.dumps(payload,indent=2,ensure_ascii=False))

if __name__=='__main__': main()

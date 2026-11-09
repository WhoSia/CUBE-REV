#!/usr/bin/env python3
"""Exact joint-parity delayed-activation theorem; full 12E/8C six-color matching DP.
Finite checks do NOT assert a global mixed-prefix 20-frame policy.
"""
from itertools import permutations,product
from collections import Counter
from functools import lru_cache
import json, hashlib
from pathlib import Path

E=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
C=('URF','UFL','ULB','UBR','DFR','DLF','DBL','DRB')

def count(types,arity,observed):
    n=len(types);req={}
    for slot,col in observed:
        if slot in req and req[slot]!=col:return (0,0)
        assert 0<=slot<arity*n
        req[slot]=col
    opts=[]
    for pos in range(n):
        choices=[]
        for lab,word in enumerate(types):
            for twist in range(arity):
                if all(word[(side+twist)%arity]==req[arity*pos+side] for side in range(arity) if arity*pos+side in req):
                    choices.append((lab,twist))
        opts.append(choices)
    @lru_cache(None)
    def f(mask,sign,residue):
        i=mask.bit_count()
        if i==n:return (int(sign==0 and residue==0),int(sign==1 and residue==0))
        z=[0,0]
        for lab,twist in opts[i]:
            if mask&(1<<lab):continue
            pp=sign^((mask>>(lab+1)).bit_count()&1)
            child=f(mask|(1<<lab),pp,(residue+twist)%arity)
            z[0]+=child[0];z[1]+=child[1]
        return tuple(z)
    return f(0,0,0)

def full_position_prefix(types,arity,n_seen):
    return tuple((arity*i+s,types[i][s]) for i in range(n_seen) for s in range(arity))

def joint(e,c):return e[0]*c[0]+e[1]*c[1]

def exact_involution(types,arity,observed,position_a,position_b,samples=72):
    """Explicit prefix preserving, odd-permutation, residue-conserving position swap."""
    n=len(types); req=dict(observed)
    assert position_a!=position_b and all(pos not in (position_a,position_b) for pos in (s//arity for s in req))
    tested=0
    for p in permutations(range(n)):
        if tested>=samples:break
        for t0 in product(range(arity),repeat=n-1):
            tw=t0+((-sum(t0))%arity,)
            if any(types[p[slot//arity]][(slot%arity+tw[slot//arity])%arity]!=color for slot,color in observed):continue
            q=list(p);q[position_a],q[position_b]=q[position_b],q[position_a]
            # carry orientation together with cubie; sum unchanged
            u=list(tw);u[position_a],u[position_b]=u[position_b],u[position_a]
            assert sum(u)%arity==0
            assert all(types[q[slot//arity]][(slot%arity+u[slot//arity])%arity]==color for slot,color in observed)
            def par(a):return sum(a[i]>a[j] for i in range(n) for j in range(i+1,n))%2
            assert par(p)^par(q)==1
            tested+=1
            break
    return tested

if __name__ == "__main__":
    full_e=count(E,2,());full_c=count(C,3,())
    assert full_e==(490497638400,490497638400)
    assert full_c==(44089920,44089920)
    assert joint(full_e,full_c)==43252003274489856000
    
    rows=[]
    for ne,nc in ((0,0),(1,1),(6,4),(9,5),(10,6),(11,6),(10,7),(11,7),(12,8)):
        er=full_position_prefix(E,2,ne);cr=full_position_prefix(C,3,nc)
        ep=count(E,2,er);cp=count(C,3,cr)
        rows.append(dict(read_full_edge_positions=ne,read_full_corner_positions=nc,unread_edge_positions=12-ne,unread_corner_positions=8-nc,edge_parities=ep,corner_parities=cp,joint_legal=joint(ep,cp),independent_color_completion_sum=sum(ep)*sum(cp),parity_coupling_cost=sum(ep)*sum(cp)-joint(ep,cp),edge_balance=(ep[0]==ep[1]),corner_balance=(cp[0]==cp[1])))
    assert [r['joint_legal'] for r in rows[-5:]]==[12,3,2,1,1]
    assert all(r['edge_balance'] for r in rows if r['unread_edge_positions']>=2)
    assert all(r['corner_balance'] for r in rows if r['unread_corner_positions']>=2)
    
    # Strong independent check: parity balance under truly arbitrary partial reads.
    # Deterministic families with full and mixed, incl inconsistent histories.
    checks=[]
    for sector,types,arity in [('edge',E,2),('corner',C,3)]:
        n=len(types)
        patterns=[]
        for m in range(1,7):
            # diverse predetermined positions (not only prefix); each is partially read
            for salt in range(4):
                used=tuple(sorted({(i*7+salt*3)%n for i in range(m)}))
                rr=tuple((arity*pos+(i+salt)%arity,types[pos][(i+salt)%arity]) for i,pos in enumerate(used))
                patterns.append(rr)
        for rr in patterns:
            unread=[j for j in range(n) if all(slot//arity!=j for slot,_ in rr)]
            if len(unread)>=2:
                pp=count(types,arity,rr)
                assert pp[0]==pp[1],(sector,rr,pp)
                checks.append([sector,len(rr),len(unread),str(pp[0])])
    
    # Explicit involution on a mixed prefix, with 2 untouched in each sector;
    # ensure counts mirror the DP proof rather than only a heuristic argument.
    e_mixed=tuple((2*i,E[i][0]) for i in range(10))
    c_mixed=tuple((3*i,C[i][0]) for i in range(6))
    e_inv=exact_involution(E,2,e_mixed,10,11)
    c_inv=exact_involution(C,3,c_mixed,6,7)
    assert e_inv>0 and c_inv>0
    
    # Crucial: an oracle revealing permutation parity halves a sector posterior,
    # but the edge/corner parity COUPLING is not informative about total sizes
    # when either sector has two untouched slots.
    for row in rows:
        ep,cp=row['edge_parities'],row['corner_parities']
        if row['edge_balance'] or row['corner_balance']:
            assert 2*row['joint_legal']==row['independent_color_completion_sum']
    
    receipt={'result':'R14_P8_DELAYED_PARITY_ACTIVATION_DP_PASS',
     'theorem':'At least two completely unread spatial cubie positions in E (respectively C) induce a fixed-history color-preserving, orientation-sum-conserving, sign-reversing involution. Therefore E0=E1 (respectively C0=C1).',
     'joint_formula':'J=E0*C0+E1*C1; unrestricted sector product=(E0+E1)*(C0+C1)',
     'critical_distinct_position_gate':'To obtain a parity imbalance in BOTH sectors simultaneously, an observation history must touch >=11 of 12 edge positions AND >=7 of 8 corner positions; this gate is necessary, not sufficient.',
     'completely_observed_solved_prefixes':rows,
     'arbitrary_partial_prefix_balance_tests':len(checks),
     'explicit_involution_samples':{'edge':e_inv,'corner':c_inv},
     'full_group_states':joint(full_e,full_c),
     'scope':'Full edge and corner matching cardinalities with abstract cyclic corner ordering, no full P48 geometric mapping in this script, no universal 20-frame policy or 21 lower bound.'}
    with open(Path(__file__).with_name('R14_P8_DELAYED_PARITY_ACTIVATION_RECEIPT.json'),'w') as f:json.dump(receipt,f,indent=2,ensure_ascii=False)
    print(json.dumps({k:v for k,v in receipt.items() if k!='completely_observed_solved_prefixes'},indent=2,ensure_ascii=False))
    print('PREFIX_ROWS',json.dumps(rows))

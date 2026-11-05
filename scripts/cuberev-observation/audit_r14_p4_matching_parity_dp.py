#!/usr/bin/env python3
"""R14-P4: matching/parity DP counts exact legal states from partial colors.

Self-contained finite checker; separately enumerates 5-edge/3-corner
subcourt and verifies ALL adaptive three-pair transcripts. Also counts
full 12-edge/8-corner no-observation legal states without cube enumeration.
Corner triples use an abstract cyclic sticker convention, NOT independent
P48 geometry; remote physical correctness requires an additional oracle.
"""
import hashlib
import itertools
import json
from collections import Counter
from functools import lru_cache

EDGE_TYPES=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
CORNER_TYPES=('URF','UFL','ULB','UBR','DFR','DLF','DBL','DRB')


def matching_parity_counts(types, mod, readings=()):
    """Number of legal orientation-sum-zero assignments of each parity.

    Inversions introduced by assigning unused label j after a prefix mask:
    exactly the earlier selected labels k>j. Memo state (mask, inversion
    parity so far, orientation residue). Does not enumerate n! states.
    """
    n=len(types)
    if not all(len(t)==mod for t in types): raise ValueError('type arity')
    req={}
    for slot,color in readings:
        if not 0<=slot<n*mod: raise ValueError('slot range')
        if slot in req and req[slot]!=color: return (0,0)
        req[slot]=color
    permitted=[]
    for pos in range(n):
        opts=[]
        for j,t in enumerate(types):
            for ori in range(mod):
                if all(t[(side+ori)%mod]==req[pos*mod+side]
                       for side in range(mod) if pos*mod+side in req):
                    opts.append((j,ori))
        permitted.append(tuple(opts))

    @lru_cache(None)
    def dfs(mask, parity, residue):
        i=mask.bit_count()
        if i==n:
            return ((1,0) if parity==0 else (0,1)) if residue==0 else (0,0)
        c0=c1=0
        for j,ori in permitted[i]:
            if mask>>j&1:continue
            inversions=(mask>>(j+1)).bit_count()&1
            a,b=dfs(mask|1<<j,parity^inversions,(residue+ori)%mod)
            c0+=a;c1+=b
        return (c0,c1)
    return dfs(0,0,0)


def enumerate_explicit(types,mod):
    n=len(types)
    by=[[],[]]
    for perm in itertools.permutations(range(n)):
        inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2
        for orientations in itertools.product(range(mod),repeat=n):
            if sum(orientations)%mod:continue
            word=''.join(types[perm[i]][(side+orientations[i])%mod]
                         for i in range(n) for side in range(mod))
            by[inversions].append(word)
    return tuple(tuple(z) for z in by)


def adaptive_queries(hist):
    if not hist:return (0,0)
    if len(hist)==1:return ((ord(hist[0][0])+1)%10,(ord(hist[0][1])+2)%9)
    return ((ord(hist[0][0])+ord(hist[-1][1])+3)%10,
            (ord(hist[0][1])+ord(hist[-1][0])+5)%9)


def transcript(e,c):
    hist=()
    for _ in range(3):
        i,j=adaptive_queries(hist)
        hist=hist+((e[i],c[j]),)
    return hist


def get_readings(hist):
    e=[];c=[];prefix=()
    for a,b in hist:
        i,j=adaptive_queries(prefix)
        e.append((i,a));c.append((j,b))
        prefix=prefix+((a,b),)
    return tuple(e),tuple(c)


def posterior_count(er,cr):
    ep=matching_parity_counts(EDGE_TYPES[:4]+(EDGE_TYPES[8],),2,er)
    cp=matching_parity_counts(CORNER_TYPES[:3],3,cr)
    return ep[0]*cp[0]+ep[1]*cp[1],ep,cp


def main():
    full_edges=matching_parity_counts(EDGE_TYPES,2)
    full_corners=matching_parity_counts(CORNER_TYPES,3)
    assert full_edges==(490497638400,490497638400)
    assert full_corners==(44089920,44089920)
    legal_full=sum(full_edges[p]*full_corners[p] for p in range(2))
    assert legal_full==43252003274489856000

    E=enumerate_explicit(EDGE_TYPES[:4]+(EDGE_TYPES[8],),2)
    C=enumerate_explicit(CORNER_TYPES[:3],3)
    assert tuple(len(x) for x in E)==(960,960)
    assert tuple(len(x) for x in C)==(27,27)
    direct=Counter()
    for p in range(2):
        for e in E[p]:
            for c in C[p]: direct[transcript(e,c)]+=1
    assert len(direct)==2464 and sum(direct.values())==51840

    for hist,total in direct.items():
        er,cr=get_readings(hist)
        count,ep,cp=posterior_count(er,cr)
        assert count==total,(hist,count,total)
        assert sum(ep[p]*cp[p] for p in (0,1))==total

    # Independently test all six-color paired outcomes for every available
    # next facelet slot of the exact known count-aliasing counterexample.
    hist_a=(('U','U'),('U','U'),('F','F'))
    hist_b=(('R','U'),('F','U'),('R','L'))
    branches=[]
    for hist in (hist_a,hist_b):
        er,cr=get_readings(hist)
        cell_counts=Counter()
        for u in 'URFDLB':
            for v in 'URFDLB':
                n,_,_=posterior_count(er+((1,u),),cr+((0,v),))
                if n:cell_counts[(u,v)]=n
        assert sum(cell_counts.values())==72
        branches.append(sorted(cell_counts.values(),reverse=True))
    assert branches==[[20,20,20,12],[48,24]],branches

    receipt={
        'result':'R14_P4_EXACT_MATCHING_PARITY_DP_PASS',
        'full_edge_parity_counts':full_edges,
        'full_corner_parity_counts':full_corners,
        'full_legal_cube_state_count':legal_full,
        'finite_court_legal_states':51840,
        'finite_court_distinct_adaptive_histories':len(direct),
        'all_histories_match_bruteforce':True,
        'fixed_query_different_branch_sizes':branches,
        'factorization':'sum_p E_p(history)*C_p(history)',
        'matching_state':'(used_label_mask, permutation_parity, orientation_residue)',
        'computational_mode':'count completions without enumerating permutation states',
        'scope_limit':'abstract cyclic corner colors; no P48 replay, no global 20-frame theorem',
        'transcript_histogram_sha256':hashlib.sha256('\n'.join(
            str((h,n)) for h,n in sorted(direct.items())).encode()).hexdigest()
    }
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()

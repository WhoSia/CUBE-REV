#!/usr/bin/env python3
"""R14-P6: exact parity-factored mixed-color belief child counts and negative controls.

Small 3-edge/3-corner full enumeration is independent of the 48-sticker geometry.
Full P48 counts import the separately audited P51 geometric cubie ordering.
Every assertion is deterministic; pure stdlib.
"""
from collections import Counter
from functools import lru_cache
from itertools import permutations, product
import contextlib, io, json, random, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))


def parity(perm):
    return sum(perm[i]>perm[j] for i in range(len(perm)) for j in range(i+1,len(perm)))%2


def explicit_words(types, mod):
    n=len(types)
    groups=[[],[]]
    for p in permutations(range(n)):
        for orientation in product(range(mod),repeat=n-1):
            o=orientation+((-sum(orientation))%mod,)
            word=''.join(types[p[i]][(j+o[i])%mod] for i in range(n) for j in range(mod))
            groups[parity(p)].append(word)
    return groups


def matching_counts(types, mod, req):
    """Exact counts by permutation parity, with orientation sum 0.

    req maps spatial facelet slot IDs to literal six-color readings.
    A repeated identical reading is allowed; contradictory readings return zeros.
    """
    n=len(types)
    fixed={}
    for idx, col in req:
        assert 0 <= idx < n*mod
        if idx in fixed and fixed[idx]!=col:return (0,0)
        fixed[idx]=col
    allowed=[]
    for i in range(n):
        opts=[]
        for t,word in enumerate(types):
            for shift in range(mod):
                if all(word[(j+shift)%mod]==fixed[i*mod+j] for j in range(mod) if i*mod+j in fixed):
                    opts.append((t,shift))
        allowed.append(opts)

    @lru_cache(None)
    def dfs(used, p, residue):
        i=used.bit_count()
        if i==n:
            return (int(p==0),int(p==1)) if residue==0 else (0,0)
        a=b=0
        for label,shift in allowed[i]:
            if used>>label&1:continue
            aa,bb=dfs(used|1<<label,p^((used>>(label+1)).bit_count()&1),(residue+shift)%mod)
            a+=aa;b+=bb
        return (a,b)
    return dfs(0,0,0)


def joint_counts(E,C,er,cr):
    ep=matching_counts(E,2,er)
    cp=matching_counts(C,3,cr)
    return ep[0]*cp[0]+ep[1]*cp[1],ep,cp


def branch_counts(E,C,er,cr,q):
    out={}
    for a,b in product('URFDLB',repeat=2):
        n,_,_=joint_counts(E,C,er+((q[0],a),),cr+((q[1],b),))
        if n:out[(a,b)]=n
    before,_,_=joint_counts(E,C,er,cr)
    assert sum(out.values())==before, (before,sum(out.values()),q)
    return out


def small_court():
    E=('UR','UF','UL'); C=('URF','UFL','ULB')
    ee=explicit_words(E,2);cc=explicit_words(C,3)
    states=tuple((e,c) for p in (0,1) for e in ee[p] for c in cc[p])
    assert len(states)==648
    rng=random.Random(20261106)
    queries=tuple(product(range(6),range(9)))
    examples=0
    seen_histories=set()
    for _ in range(160):
        s=rng.choice(states)
        er=[];cr=[];query_sequence=[]
        for _ in range(3):
            q=rng.choice(queries)
            query_sequence.append(q)
            er.append((q[0],s[0][q[0]]));cr.append((q[1],s[1][q[1]]))
            key=(tuple(sorted(er)),tuple(sorted(cr)))
            if key in seen_histories:continue
            seen_histories.add(key)
            survivors=[z for z in states if all(z[0][i]==a for i,a in er) and all(z[1][j]==b for j,b in cr)]
            num,ep,cp=joint_counts(E,C,tuple(er),tuple(cr))
            assert num==len(survivors)
            qnext=rng.choice(queries)
            branches=branch_counts(E,C,tuple(er),tuple(cr),qnext)
            actual=Counter((z[0][qnext[0]],z[1][qnext[1]]) for z in survivors)
            assert branches==actual
            examples+=1
    # Negative control: beliefs of equal total size are NOT necessarily interchangeable.
    # Search for two reachable constraints with the same population and a different
    # next-paired-query (with fixed physical coordinates) branch partition.
    by_count={}
    for q1 in queries[::4]:
        for st in states[::11]:
            er=((q1[0],st[0][q1[0]]),);cr=((q1[1],st[1][q1[1]]),)
            n,_,_=joint_counts(E,C,er,cr)
            by_count.setdefault(n,[]).append((er,cr))
    counterexample=None
    for n, candidates in by_count.items():
        if len(candidates)<2:continue
        for q in queries:
            baseline={}
            for er,cr in candidates[:60]:
                sig=tuple(sorted(branch_counts(E,C,er,cr,q).values()))
                if baseline and sig not in baseline:
                    (prior_er,prior_cr),old=next(iter(baseline.values()))
                    counterexample={'equal_total':n,'query':q,'first':{'edge':prior_er,'corner':prior_cr,'sorted_child_sizes':old},'second':{'edge':er,'corner':cr,'sorted_child_sizes':sig}}
                    break
                baseline[sig]=((er,cr),sig)
            if counterexample:break
        if counterexample:break
    assert counterexample is not None
    return examples,counterexample


def full_p48_court():
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            from audit_r14_p51_p48_group_lift import PIECES, EDGES, CORNERS, SLOTS, FACES, q0, H_orbits
        except ModuleNotFoundError as exc:
            if exc.name != "audit_r14_p51_p48_group_lift":
                raise
            from CUBEREV_028_R14_P51_P48_GROUP_LIFT import PIECES, EDGES, CORNERS, SLOTS, FACES, q0, H_orbits
    color={i:next(f for f,n in FACES.items() if n==SLOTS[i][1]) for i in range(48)}
    E=tuple(''.join(color[i] for i in PIECES[p]) for p in EDGES)
    C=tuple(''.join(color[i] for i in PIECES[p]) for p in CORNERS)
    eid={slot:2*i+j for i,p in enumerate(EDGES) for j,slot in enumerate(PIECES[p])}
    cid={slot:3*i+j for i,p in enumerate(CORNERS) for j,slot in enumerate(PIECES[p])}
    root_e=((eid[q0[0]],'U'),); root_c=((cid[q0[1]],'U'),)
    parent,ep,cp=joint_counts(E,C,root_e,root_c)
    assert parent==1201444535402496000
    result=[]
    for pair,orbit_size in H_orbits:
        query=(eid[pair[0]],cid[pair[1]])
        branches=branch_counts(E,C,root_e,root_c,query)
        result.append({'query_local':query,'stabilizer_orbit_size':orbit_size,'number_of_next_color_pairs':len(branches),'worst_child':max(branches.values())})
    assert len(result)==12
    best=min(row['worst_child'] for row in result)
    assert best==41608468758528000
    return parent,result


def main():
    independent,counter=small_court()
    root,rows=full_p48_court()
    print(json.dumps({'result':'R14_P6_EXACT_SYMBOLIC_BELIEF_BRANCH_COURT_PASS',
       'independent_3edge_3corner_legal_states':648,
       'small_full_enumeration_histories_verified':independent,
       'equal_cardinality_alias_counterexample':counter,
       'full_p48_root_same_color_posterior':root,
       'full_p48_12_second_query_orbit_branch_profiles':rows,
       'best_second_query_one_step_worst_child':min(x['worst_child'] for x in rows),
       'scope':'exact cardinalities and successor color partitions, not complete Bellman policy or 20-frame proof',
       'geometry_dependency':'imports previously checked P51, so P48 geometry is NOT independently reconstructed'},indent=2,sort_keys=True))

if __name__=='__main__':main()

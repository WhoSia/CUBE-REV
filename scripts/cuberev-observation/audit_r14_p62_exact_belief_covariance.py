#!/usr/bin/env python3
"""R14-P6.2: exact miniature legal-group belief canonicalization audit.

This independent script rebuilds the 648-state 3E/3C game directly and reads
only the prior P6.1 finite certificate for a *separately replayed* policy.
It does not rely on cube P48 geometry or an unverified population heuristic.
"""
from collections import Counter
from itertools import permutations, product
from functools import lru_cache
from pathlib import Path
import json, hashlib, sys

EDGE=('UR','UF','UL'); CORNER=('URF','UFL','ULB')
def parity(a):
    return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2

def sector_words(types, r):
    out=[[],[]]
    for p in permutations(range(len(types))):
        for before in product(range(r),repeat=len(types)-1):
            o=before+((-sum(before))%r,)
            out[parity(p)].append(''.join(types[p[i]][(j+o[i])%r]
                                                 for i in range(len(types)) for j in range(r)))
    return out
E=sector_words(EDGE,2); C=sector_words(CORNER,3)
states=tuple((e,c) for p in (0,1) for e in E[p] for c in C[p])
assert len(states)==len(set(states))==648
lookup={z:i for i,z in enumerate(states)}
queries=tuple(product(range(6),range(9)))
query_id={q:i for i,q in enumerate(queries)}
cells=[]
for q in queries:
    m={}
    for i,(e,c) in enumerate(states):
        label=e[q[0]]+c[q[1]]
        m[label]=m.get(label,0)|(1<<i)
    cells.append(m)
FULL=(1<<648)-1

def children(B,qi):
    return {y:B&mask for y,mask in cells[qi].items() if B&mask}

@lru_cache(None)
def win(B,k):
    if B.bit_count()==1:return True
    if not k or B.bit_count()>36**k:return False
    for qi in range(54):
        sub=children(B,qi)
        if len(sub)<2:continue
        if max(v.bit_count() for v in sub.values())>36**(k-1):continue
        if all(win(v,k-1) for v in sorted(sub.values(),key=int.bit_count,reverse=True)):
            return True
    return False

def sector_maps(n,r):
    out=[[],[]]
    for p in permutations(range(n)):
        for prefix in product(range(r),repeat=n-1):
            o=prefix+((-sum(prefix))%r,)
            g=[None]*(n*r)
            for i in range(n):
                for j in range(r):
                    g[p[i]*r+(j+o[i])%r]=i*r+j
            out[parity(p)].append(tuple(g))
    return out
es=sector_maps(3,2);cs=sector_maps(3,3)
group=tuple((eg,cg) for p in (0,1) for eg in es[p] for cg in cs[p])
assert len(group)==len(set(group))==648
identity=(tuple(range(6)),tuple(range(9)))
gid={g:i for i,g in enumerate(group)}
assert identity in gid

def inverse(g):
    result=[]
    for p in g:
        q=[None]*len(p)
        for i,j in enumerate(p):q[j]=i
        result.append(tuple(q))
    return tuple(result)
def compose(g,h):
    return tuple(tuple(g[sector][h[sector][i]] for i in range(len(h[sector]))) for sector in (0,1))

# Rebuild all 648 transformations on the complete state set. This confirms
# legality and bijectivity rather than assuming that an index shuffle works.
state_maps=[]
for g in group:
    ig=inverse(g)
    image=[]
    for e,c in states:
        ne=''.join(e[ig[0][i]] for i in range(6))
        nc=''.join(c[ig[1][i]] for i in range(9))
        assert (ne,nc) in lookup, 'illegal purported spatial group action'
        image.append(lookup[(ne,nc)])
    assert len(set(image))==648
    state_maps.append(tuple(image))

@lru_cache(None)
def transform(B,gi):
    mapping=state_maps[gi]
    r=0
    while B:
        lsb=B&-B
        r|=1<<mapping[lsb.bit_length()-1]
        B^=lsb
    return r

def target_query(q,gi):
    g=group[gi]
    return query_id[(g[0][q[0]],g[1][q[1]])]

# Strong exact covariance, not a cardinality approximation. The initial
# observation colors remain LITERALLY unchanged under spatial left action.
# Build a canonical unaccelerated winning policy INDEPENDENTLY of P6.1
# receipt availability. This script is runnable by itself in clean CI.
@lru_cache(None)
def construct(B,budget):
    if B.bit_count()==1:return {'end': B.bit_length()-1}
    assert budget and win(B,budget)
    for qi in range(54):
        kids=children(B,qi)
        if len(kids)>1 and all(win(x,budget-1) for x in kids.values()):
            return {'q':qi,'branches':{y:construct(x,budget-1) for y,x in sorted(kids.items())}}
    raise AssertionError('no policy for winning state')
assert not win(FULL,3) and win(FULL,4)
policy=construct(FULL,4)
# If the independent P6.1 original certificate is provided next to this file,
# compare its complete tree, never silently require it for a clean checkout.
receipt_path=Path(__file__).with_name('CUBEREV_028_R14_P61_MICRO_EXACT_MINIMAX_RECEIPT.json')
if receipt_path.exists():
    receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    assert receipt['complete_depth4_policy_tree']==policy

def traverse(node,B,depth,records):
    assert B
    if 'end' in node:
        assert B.bit_count()==1 and states[node['end']]==states[B.bit_length()-1]
        records.append((B,depth,None))
        return
    qi=node['q']
    assert isinstance(qi,int) and 0<=qi<54
    records.append((B,depth,qi))
    nxt=children(B,qi)
    assert set(nxt)==set(node['branches'])
    for y,child in node['branches'].items():traverse(child,nxt[y],depth+1,records)
records=[]
traverse(policy,FULL,0,records)
assert len(records)==963
assert sum(B.bit_count() for B,d,q in records if q is None)==648
root_masks=[(FULL,0)]
for qi in range(54):
    root_masks.extend((b,qi) for b in children(FULL,qi).values())

# Pick nontrivial group elements (including an odd simultaneous sector swap),
# and check all realizable next outputs for all 54 actions at 300+ policy nodes.
interesting_g=[gid[identity]]
for g in group:
    if len(interesting_g)>=9:break
    gi=gid[g]
    if gi not in interesting_g and (g[0][0]!=0 or g[1][0]!=0):interesting_g.append(gi)
cov_checks=0
for B,d,qi_fixed in records:
    if qi_fixed is None:continue
    for gi in interesting_g:
        NB=transform(B,gi)
        assert NB.bit_count()==B.bit_count()
        for qi in range(54):
            qnew=target_query(queries[qi],gi)
            a=children(B,qi);b=children(NB,qnew)
            assert set(a)==set(b)
            for label,mask in a.items():
                assert transform(mask,gi)==b[label]
            cov_checks+=1

# Exact 648-group quotient over root-conditioned (and shallow policy) beliefs.
# Canonical representatives are MINIMAL TRANSFORMED FULL BITMASKS, never just
# same population. A witness g is retained for inverse-query transport.
canon_cache={}
canonical_orbits=0

def canonical(B):
    global canonical_orbits
    if B not in canon_cache:
        orbit={}
        for gi in range(len(group)):
            BB=transform(B,gi)
            orbit.setdefault(BB,gi)
        rep=min(orbit)
        rep_g=orbit[rep]
        # From B to rep: rep_g. For each orbit member g_i(B), transport
        # via rep_g * inverse(g_i).
        for BB,gi in orbit.items():
            transporter=compose(group[rep_g],inverse(group[gi]))
            witness=gid[transporter]
            assert transform(BB,witness)==rep
            canon_cache[BB]=(rep,witness)
        canonical_orbits+=1
    return canon_cache[B]

unique_masks={B for B,_,_ in records}|{B for B,_ in root_masks}
# All legal group transforms of any belief are guaranteed to be in orbit.
for B in unique_masks:
    rep,w=canonical(B)
    assert transform(B,w)==rep
    assert B.bit_count()==rep.bit_count()

# Independently test optimal Bellman values on all non-singleton policy beliefs
# against canonical representatives, with the original query reconstitution.
nonterminal={B for B,_,q in records if q is not None}
checked_values=0
for B in nonterminal:
    rep,w=canonical(B)
    original_depth=next(d for bb,d,q in records if bb==B and q is not None)
    budget=4-original_depth
    assert win(B,budget)==win(rep,budget)
    if budget:
        assert win(B,budget-1)==win(rep,budget-1)
    checked_values+=1

# Verify that a representative's winning query can always be returned to
# the originally indexed belief and that its every child is transported.
reconstitutions=0
for B in nonterminal:
    rep,w=canonical(B)
    budget=4-next(d for bb,d,q in records if bb==B and q is not None)
    winning_q=None
    for q in range(54):
        kids=children(rep,q)
        if len(kids)>1 and all(win(b,budget-1) for b in kids.values()):
            winning_q=q;break
    assert winning_q is not None
    inv_g=gid[inverse(group[w])]
    origin_q=target_query(queries[winning_q],inv_g)
    actual=children(B,origin_q)
    representative=children(rep,winning_q)
    assert set(actual)==set(representative)
    assert all(transform(b,w)==representative[y] for y,b in actual.items())
    assert all(win(b,budget-1) for b in actual.values())
    reconstitutions+=1

# Equal-cardinality negative control cannot be assumed equivalent:
# it may or may not be in same orbit, so test actual full state-set orbits.
def belief(er,cr):
    result=0
    for i,(e,c) in enumerate(states):
        if all(e[q]==col for q,col in er) and all(c[q]==col for q,col in cr):result|=1<<i
    return result
A=belief(((0,'U'),),((0,'U'),));B=belief(((0,'U'),),((4,'U'),))
assert A.bit_count()==B.bit_count()==108
fixed_a=sorted(b.bit_count() for b in children(A,0).values())
fixed_b=sorted(b.bit_count() for b in children(B,0).values())
assert fixed_a==[108] and fixed_b==[12,12,24,24,36]
# Whether this pair *is* equivalent under the verified spatial left group is
# determined by exact group action, without guessing from differing branches.
negative_equiv=canonical(A)[0]==canonical(B)[0]

# Find a genuine equal-size *non-orbit* pair, and preserve the distinguishable
# multiset of next-query branch-size partitions as a falsification witness.
by_pop={}
for mask in unique_masks|{A,B}:
    if mask.bit_count()>1:
        by_pop.setdefault(mask.bit_count(),{}).setdefault(canonical(mask)[0],mask)
nonorbit_pair=None
for pop,classes in sorted(by_pop.items(),reverse=True):
    if len(classes)<2:continue
    exemplar=list(classes.values())
    for i in range(min(len(exemplar),10)):
        for j in range(i+1,min(len(exemplar),20)):
            a,b=exemplar[i],exemplar[j]
            def action_profiles(mask):
                return sorted(tuple(sorted(child.bit_count() for child in children(mask,qi).values())) for qi in range(54))
            pa,pb=action_profiles(a),action_profiles(b)
            if pa!=pb:
                nonorbit_pair=(pop,a,b,pa,pb)
                break
        if nonorbit_pair:break
    if nonorbit_pair:break
assert nonorbit_pair is not None
pop,fa,fb,profiles_a,profiles_b=nonorbit_pair
assert canonical(fa)[0]!=canonical(fb)[0]
assert fa.bit_count()==fb.bit_count()==pop
# This invariant is insensitive to all legal query permutation actions and
# color-output relabels, but differs: it certifies genuine non-isomorphism.
unique_a=Counter(map(str,profiles_a)); unique_b=Counter(map(str,profiles_b))
profile_diff=sorted((k,unique_a[k],unique_b[k]) for k in unique_a.keys()|unique_b.keys() if unique_a[k]!=unique_b[k])

result={
 'result':'R14_P62_EXACT_ORBIT_COVARIANCE_AND_POLICY_TRANSPORT_PASS',
 'legal_states':648,'all_legal_spatial_group_elements':648,
 'all_query_actions':54,'policy_nodes_replayed':len(records),
 'policy_nonterminal_beliefs':len(nonterminal),
 'unique_policy_and_one_step_beliefs':len(unique_masks),
 'full_successor_covariance_action_checks':cov_checks,
 'canonical_distinct_belief_orbits':canonical_orbits,
 'all_policy_bellman_values_match_canonical':checked_values,
 'all_original_query_inversions_verified':reconstitutions,
 'full_prior_minimax_depth4':win(FULL,4) and not win(FULL,3),
 'population_alias_108_confirmed':True,
 'population_alias_is_spatially_equivalent':negative_equiv,
 'genuine_equal_population_nonisomorphic_pair':{'population':pop,'mask_a_hex':hex(fa),'mask_b_hex':hex(fb),'all_query_partition_multisets_differ':True,'first_partition_frequencies_that_differ':profile_diff[:5]},
 'note':'Miniature finite left-group quotient only; not a completed P48 full mixed belief quotient or h<=20 proof',
}
print(json.dumps(result,indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Stand-alone checker for the frozen CUBE-REV 19-frame upper policy.

Uses only the Python standard library; it does NOT import the search engine,
its EdgeGame, the exporter or the other Q scripts. It enumerates legal edge
assignments from twelve distinct labels, tests every nonempty color branch,
and checks at most one completion per permutation sign after frame 19.
"""
import argparse
from collections import Counter
from itertools import permutations, product
from math import factorial
from pathlib import Path
import hashlib, json

COLORS='URFDLB'
LABELS=('DL','BL','FL','UL','DB','DF','UB','UF','DR','BR','FR','UR')
OPPOSITES={frozenset(p) for p in ('UD','RL','FB')}


def permutation_parity(order):
    return sum(a>b for i,a in enumerate(order) for b in order[i+1:])%2


def assignments(prefix):
    """Construct all and only legal oriented edge arrays of this first-color record."""
    result=[]
    def rec(pos, unused, order, flip, mate):
        if pos==11:
            assert len(unused)==1
            label=next(iter(unused))
            last=LABELS[label][::-1] if flip else LABELS[label]
            result.append((mate+last,permutation_parity(order+(label,))))
            return
        first=prefix[pos]
        for label in sorted(unused):
            pair=LABELS[label]
            if first in pair:
                ori=pair.index(first)
                rec(pos+1,unused-{label},order+(label,),flip^ori,mate+pair[1-ori])
    rec(0,set(range(12)),(),0,'')
    assert len(set(result))==len(result)
    return result


def support_representatives():
    sym=[]
    for perm in permutations(COLORS):
        mp=dict(zip(COLORS,perm))
        if {frozenset(mp[c] for c in o) for o in OPPOSITES}==OPPOSITES:
            sym.append(mp)
    assert len(sym)==48
    supported=set()
    for omitted in LABELS:
        first=[edge for edge in LABELS if edge!=omitted]
        for row in product(*first):
            supported.add(tuple(row.count(c) for c in COLORS))
    assert len(supported)==1362
    reps=set()
    for vec in supported:
        transformed=[]
        for mp in sym:
            moved=[0]*6
            for i,c in enumerate(COLORS):
                moved[COLORS.index(mp[c])]=vec[i]
            transformed.append(tuple(moved))
        reps.add(min(transformed))
    assert len(reps)==52
    return {''.join(c*n for c,n in zip(COLORS,k)) for k in reps}


def verify_one(entry):
    prefix,nodes=entry['prefix'],entry['nodes']
    assert len(prefix)==11 and all(c in COLORS for c in prefix)
    words=assignments(prefix)
    reachable=set()
    # Bitsets are constructed here from independently enumerated words.
    masks=[{c:0 for c in COLORS} for _ in range(13)]
    signs=[0,0]
    for i,(word,sign) in enumerate(words):
        bit=1<<i
        signs[sign]|=bit
        for q,c in enumerate(word):masks[q][c]|=bit
    root=(1<<len(words))-1
    completed=0
    num_reads=0
    terminal_by_size=Counter()
    def visit(idx,belief,budget):
        nonlocal completed,num_reads
        assert 0<=idx<len(nodes) and idx not in reachable, (prefix,idx)
        reachable.add(idx)
        node=nodes[idx]
        assert isinstance(node,list)
        kind=node[0]
        if kind=='leaf':
            assert len(node)==1
            assert all((belief&s).bit_count()<=1 for s in signs), (prefix,idx,budget)
            terminal_by_size[belief.bit_count()]+=1
            completed+=belief.bit_count()
            return
        assert budget>0, (prefix,idx)
        if kind=='repeat':
            assert len(node)==2
            visit(node[1],belief,budget-1)
            return
        assert kind=='read' and len(node)==3, (prefix,idx,kind)
        q,children=node[1:]
        assert isinstance(q,int) and 0<=q<13
        assert isinstance(children,dict)
        actual={c:belief&masks[q][c] for c in COLORS if belief&masks[q][c]}
        # If only one color is possible, it is technically a legal read, but
        # not informative; this verifier permits it without weakening soundness.
        assert set(children)==set(actual), (prefix,idx,set(children),set(actual))
        num_reads+=1
        for c in sorted(actual):visit(children[c],actual[c],budget-1)
    visit(0,root,8)
    assert len(reachable)==len(nodes), (prefix,len(reachable),len(nodes))
    assert completed==len(words), (prefix,completed,len(words))
    return {"prefix":prefix,"candidates":len(words),"nodes":len(nodes),"read_nodes":num_reads,"leaf_by_candidate_count":dict(sorted(terminal_by_size.items()))}


def verify(path):
    raw=Path(path).read_bytes()
    payload=json.loads(raw)
    assert payload['schema']=='cuberev-0.29-upper-policy-v1'
    assert payload['first_slots']==11
    assert payload['remaining_budget']==8
    assert payload['sign_release']=='terminal'
    entries=payload['representatives']
    assert len(entries)==52 and len({p['prefix'] for p in entries})==52
    assert {p['prefix'] for p in entries}==support_representatives()
    rows=[verify_one(e) for e in entries]
    counts=Counter()
    for r in rows:
        counts.update(r['leaf_by_candidate_count'])
    receipt={"status":"PASS", "sha256":hashlib.sha256(raw).hexdigest(),
       "representatives":len(rows), "candidate_assignments":sum(r['candidates'] for r in rows),
       "policy_nodes":sum(r['nodes'] for r in rows),
       "leaf_multiplicities":dict(sorted(counts.items())),
       "coverage_prefix_vectors":1362,
       "verified": "every possible color of every policy query; each terminal belief <=1 assignment per sign"}
    assert receipt['candidate_assignments']==144736
    return receipt

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('policy',nargs='?',default=str(Path(__file__).with_name('upper-policy-certificate.json')))
    args=p.parse_args()
    print(json.dumps(verify(args.policy),indent=2,ensure_ascii=False))

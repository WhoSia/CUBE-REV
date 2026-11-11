#!/usr/bin/env python3
"""R14-P8.19: scoped B5->B6 16-tag phase transition, independently rebuilt
3D geometry + historically sourced category-level physical witness ledger.

This is an audit of earlier source-verified facts, not new physical
HTM witness replay. B5 N-P category has FOUR old and FOUR new failures:
the coarse ledger cannot identify which concrete four are B5-invalid.
"""
from collections import Counter
from itertools import combinations
from fractions import Fraction
import json

NORMAL={'U':(0,1,0),'D':(0,-1,0),'R':(1,0,0),'L':(-1,0,0),
        'F':(0,0,1),'B':(0,0,-1)}
EDGE=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
ORDER=('h','N','P','F','A')

def mid(e):
    return tuple(NORMAL[e[0]][i]+NORMAL[e[1]][i] for i in range(3))
def ends(e):
    m=mid(e);k=m.index(0)
    return frozenset(tuple(v if i!=k else t for i,v in enumerate(m))
                     for t in (-1,1))
END={e:ends(e) for e in EDGE}
def classes(h):
    co=END[h];opp=frozenset(tuple(-v for v in c) for c in co)
    antipode=next(e for e in EDGE if END[e]==opp)
    near={e for e in EDGE if e!=h and END[e]&co}
    far={e for e in EDGE if e!=antipode and END[e]&opp}
    parallel={e for e in EDGE if mid(e).index(0)==mid(h).index(0)
              and e not in (h,antipode)}
    d={'h':{h},'N':near,'P':parallel,'F':far,'A':{antipode}}
    assert [len(d[x]) for x in ORDER]==[1,4,2,4,1]
    assert set().union(*d.values())==set(EDGE)
    return d
def category(h,a,b):
    d=classes(h)
    x=next(k for k in ORDER if a in d[k])
    y=next(k for k in ORDER if b in d[k])
    return '-'.join(sorted((x,y),key=ORDER.index))
def b6_positive(h,a,b):
    d=classes(h);v=sorted(END[h])[0]
    return ((a in d['N'] and b in d['N']
             and ((v in END[a])!=(v in END[b])))
            or (a in d['F'] and b in d['F'] and bool(set(a)&set(b)))
            or (a in d['A'] and b in d['F'])
            or (b in d['A'] and a in d['F'])
            or ({a,b}==d['P']))

# PHYSICAL source: docs/0.28/B6_66_PARTITION_EVIDENCE_AUDIT.md
# (old B5 failure, new B6 failure, surviving B6 positive), per core.
# These old numbers are inputs verified by the existing P48/54-facelet
# witness chain, not independently reconstructed from this table.
EVIDENCE={
'h-N':(4,0,0),'h-P':(2,0,0),'h-F':(4,0,0),'h-A':(0,1,0),
'N-N':(0,2,4),'N-P':(4,4,0),'N-F':(0,16,0),
'N-A':(4,0,0),'P-P':(0,0,1),'P-F':(0,8,0),
'P-A':(0,2,0),'F-F':(0,2,4),'F-A':(0,0,4)
}
assert EVIDENCE['N-P']==(4,4,0)
results=[]
for h in EDGE:
    frequency=Counter(category(h,*pair) for pair in combinations(EDGE,2))
    assert set(frequency)==set(EVIDENCE)
    positive=Counter(category(h,*p) for p in combinations(EDGE,2)
                     if b6_positive(h,*p))
    for cls,(old,new,survive) in EVIDENCE.items():
        assert frequency[cls]==old+new+survive,(h,cls)
        assert positive[cls]==survive,(h,cls)
    assert sum(a for a,b,c in EVIDENCE.values())==18
    assert sum(b for a,b,c in EVIDENCE.values())==35
    assert sum(c for a,b,c in EVIDENCE.values())==13
    results.append((h,48,13,35))
assert len(results)==12
assert len(set((x[1],x[2],x[3]) for x in results))==1
assert Fraction(13,48)+Fraction(35,48)==1
if __name__=='__main__':
    print(json.dumps({
      'status':'R14_P819_B5_B6_PHYSICAL_LEDGER_GEOMETRY_CROSSCHECK_PASS',
      'scope':'historically certified per-type B5/B6 physical counts; new geometric B6 candidate reconstruction only',
      'native_core_edges':12,'per_core_candidate_edge_pairs':66,
      'per_core_prior_B5_negative':18,'per_core_B5_valid':48,
      'per_core_new_B6_negative':35,'per_core_B6_valid':13,
      'B5_valid_16_sensors_in_adjacent_corners_sector':576,
      'B6_valid_16_sensors':156,'B5_to_B6_lost_16_sensors':420,
      'B5_to_B6_retained_fraction':str(Fraction(13,48)),
      'B5_to_B6_lost_fraction':str(Fraction(35,48)),
      'new_near_far_failure_count':192,
      'other_new_failure_count':228,
      'near_parallel_8_pair_split':{'old_B5_failures':4,'new_B6_failures':4},
      'historical_category_ledger':EVIDENCE,
      'actual_original_P48_witnesses_rerun':False,
      'B5_near_parallel_individual_identity_verified':False
    },sort_keys=True))

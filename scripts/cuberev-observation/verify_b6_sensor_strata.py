#!/usr/bin/env python3
"""B6 necessary cardinality strata under certified small-radius supports.

Proved assumptions only: B5 pure 3-edge supports cover all C(12,3);
B6 pure 2-corner supports include all pairs at cube distances 2 and 3.
This code DOES NOT check any candidate against all actual B6 states.
"""
from itertools import product,combinations
from collections import Counter
C=list(product((0,1),repeat=3))
def dist(a,b): return sum(x!=y for x,y in zip(a,b))
corners_by_size=Counter()
for m in range(1<<8):
    chosen={i for i in range(8) if (m>>i)&1}
    if all(i in chosen or j in chosen for i,j in combinations(range(8),2)
           if dist(C[i],C[j])>=2):
        corners_by_size[len(chosen)]+=1
assert corners_by_size==Counter({6:12,7:8,8:1})
edges_by_size={n:sum(1 for omitted in combinations(range(12),12-n))
               for n in (10,11,12)}
assert edges_by_size=={10:66,11:12,12:1}
strata={}
for total in (16,17,18):
    strata[total]={}
    for nc,count in corners_by_size.items():
        ne=total-nc
        if ne in edges_by_size:
            strata[total][(nc,ne)]=count*edges_by_size[ne]
assert strata[16]=={(6,10):792}
assert strata[17]=={(6,11):144,(7,10):528}
assert strata[18]=={(6,12):12,(7,11):96,(8,10):66}
assert sum(strata[17].values())==672
print("PASS B6 necessary-only 16-tag strata",strata[16])
print("PASS B6 necessary-only 17-tag strata",strata[17],"total=672")
print("PASS B6 necessary-only 18-tag strata",strata[18],"total=174")
print("LIMIT: 16-tag B5 refinement 576 is inherited; NONE are certified B6 successes")

#!/usr/bin/env python3
"""Explicit universal 2-read adversary over all 32 hard edge triples, both known parities."""
from itertools import combinations,permutations,product
from collections import defaultdict,Counter
from pathlib import Path
import json
T=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
def sign(p):return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2
def words(types,par):
 return sorted({''.join(types[perm[i]][s^o[i]] for i in range(3) for s in range(2)) for perm in permutations(range(3)) if sign(perm)==par for o in ((0,0,0),(0,1,1),(1,0,1),(1,1,0))})
rows=[]
for triple in combinations(T,3):
 degree=tuple(sorted(Counter(''.join(triple)).values(),reverse=True))
 if degree not in ((3,1,1,1),(2,2,2)):continue
 for par in range(2):
  states=words(triple,par);assert len(states)==12
  for q0 in range(6):
   response=defaultdict(list)
   for word in states:response[word[q0]].append(word)
   candidates=[]
   for color,post in sorted(response.items()):
    failures=[]
    for q1 in range(6):
     bins=defaultdict(list)
     for w in post:bins[w[q1]].append(w)
     pair=next((a[:2] for a in bins.values() if len(a)>1),None)
     if pair is None:break
     failures.append({'second_facelet':q1,'collision':pair,'second_color':pair[0][q1]})
    if len(failures)==6:candidates.append((color,post,failures))
   assert candidates,(triple,par,q0)
   color,post,failures=candidates[0]
   assert all(all(w[q0]==color for w in f['collision']) and len(set(f['collision']))==2 for f in failures)
   rows.append({'triple':triple,'graph_degrees':degree,'known_permutation_parity':par,'first_facelet':q0,'adversarial_first_color':color,'surviving_states':len(post),'six_second_query_collision_pairs':failures})
assert len(rows)==32*2*6
receipt={'result':'R14_P83_EXPLICIT_384_ROOT_ADVERSARIES_PASS','hard_source_triples':32,'parities_per_triple':2,'first_queries_per_parity':6,'first_query_adversary_certificates':384,'explicit_second_query_collision_pairs':384*6,'certificates':rows,'scope':'For each hard triple and known permutation parity, no 2-read adaptive exact decoder; each first query has a response branch where every second read has at least one indistinguishable legal state pair. Does not imply full 20-frame global lower.'}
Path(__file__).with_name('R14_P83_384_ROOT_ADVERSARIES_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS',receipt['first_query_adversary_certificates'],'root',receipt['explicit_second_query_collision_pairs'],'pair witnesses')

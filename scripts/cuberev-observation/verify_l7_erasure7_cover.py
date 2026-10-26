#!/usr/bin/env python3
import json,itertools
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
P=Path(__file__).resolve().parents[2]/'docs/observation-generalization/L7_ERASURE1_7_WORD_COVER.json'
def verify():
 words=json.loads(P.read_text())['words'];assert len(words)==7
 moves=edge_transitions(); hit=set()
 for word in words:
  s=signatures(moves,tuple(ACTIONS.index(a) for a in word))
  for r in (3,4):
   for group in itertools.combinations(range(12),r):
    if all((s[i]^s[j]).bit_count()>=2 for i,j in itertools.combinations(group,2)):
     hit.add(sum(1<<i for i in group))
 assert len(hit)==715
 return {'status':'PASS','words':7,'covered':715,'global_optimum_proven':False}
if __name__=='__main__':print(json.dumps(verify()))

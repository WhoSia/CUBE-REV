#!/usr/bin/env python3
"""Independent literal verification of all 384 root obstructions and 2304 second-query pair collisions."""
import json
from pathlib import Path
from itertools import permutations,product
T=Path(__file__).with_name('R14_P83_384_ROOT_ADVERSARIES_RECEIPT.json')
d=json.loads(T.read_text());assert len(d['certificates'])==384

def sign(p):return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2

def legal(triple,par):
 s=set()
 for p in permutations(range(3)):
  if sign(p)!=par:continue
  for a in product((0,1),repeat=3):
   if sum(a)%2:continue
   s.add(''.join(triple[p[i]][(q+a[i])%2] for i in range(3) for q in range(2)))
 return s
checked=0
for row in d['certificates']:
 triple=tuple(row['triple']);par=row['known_permutation_parity'];q0=row['first_facelet'];color=row['adversarial_first_color']
 all_state_words=legal(triple,par);assert len(all_state_words)==12
 observed={w for w in all_state_words if w[q0]==color};assert len(observed)==row['surviving_states']
 seen=[]
 for pair in row['six_second_query_collision_pairs']:
  q1=pair['second_facelet'];x,y=pair['collision'];assert x!=y
  assert x in observed and y in observed
  assert x[q1]==y[q1]==pair['second_color']
  seen.append(q1);checked+=1
 assert sorted(seen)==list(range(6))
assert checked==2304
result={'result':'R14_P83_INDEPENDENT_384_ROOT_2304_PAIR_WITNESS_REPLAY_PASS','root_adversary_records':384,'verified_second_query_collision_pairs':checked,'all_correspond_to_exact_known_parity_legal_oriented_assignments':True,'not_a_full_20_frame_root_lower_bound':True}
Path(__file__).with_name('R14_P83_INDEPENDENT_384_ADVERSARY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result)

#!/usr/bin/env python3
"""CUBE-REV 0.28: independent physical 48-sticker short-support audit.

Does not use the historical 54-facelet implementation.
Only verifies cited witness words and cube rotation orbits, not HTM optimality.
"""
from itertools import product, permutations, combinations

N = {'U':(0,1,0),'R':(1,0,0),'F':(0,0,1),
     'D':(0,-1,0),'L':(-1,0,0),'B':(0,0,-1)}
T = {'U':(1,1,-1),'R':(0,1,-1),'F':(2,1,-1),
     'D':(1,-1,1),'L':(0,-1,1),'B':(2,-1,1)}
WORDS = {
 'face_diagonal_corners_12': "U2 R' B D2 B' R U2 R' B D2 B' R",
 'body_diagonal_corners_12': "U' B2 U L' F2 L U' B2 U L' F2 L",
 'adjacent_corners_14': "R' D R F D F' U' F D' F' R' D' R U",
 'adjacent_edges_13': "L F R' F' L' U2 R U R U' R2 U2 R",
}
def rotate(v,axis,k):
 x,y,z=v
 for _ in range(k%4):
  if axis==0: y,z=-z,y
  elif axis==1: x,z=z,-x
  else: x,y=-y,x
 return (x,y,z)

def initial():
 return [(p,n,face) for p in product((-1,0,1),repeat=3)
         if sum(x!=0 for x in p) in (2,3)
         for face,n in N.items() if sum(a*b for a,b in zip(p,n))==1]

def play(word):
 stickers=initial()
 assert len(stickers)==48
 for move in word.split():
  axis,layer,sgn=T[move[0]]
  power=2 if move.endswith('2') else 3 if move.endswith("'") else 1
  k=power*sgn
  stickers=[(rotate(p,axis,k),rotate(n,axis,k),c) if p[axis]==layer
            else (p,n,c) for p,n,c in stickers]
 return stickers

def factors(stickers):
 # Pair each current physical sticker with the SAME original sticker.
 # Identify each original cubie from its initial sticker position.
 pieces={}
 for (origin,_,_), (p,n,color) in zip(initial(),stickers):
  tag=tuple(sorted(face for face,v in N.items()
                   if sum(a*b for a,b in zip(origin,v))==1))
  if tag not in pieces: pieces[tag]=(p,[])
  assert pieces[tag][0]==p
  pieces[tag][1].append((color,n))
 return {tag:(pos,tuple(sorted(a))) for tag,(pos,a) in pieces.items()}

def proper24():
 def sign(perm):return (-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
 rot=[]
 for perm in permutations(range(3)):
  for signs in product((-1,1),repeat=3):
   if sign(perm)*signs[0]*signs[1]*signs[2]==1:
    rot.append(lambda p,perm=perm,signs=signs:
               tuple(signs[i]*p[perm[i]] for i in range(3)))
 assert len(rot)==24
 return rot

def test():
 baseline=factors(initial())
 assert len(baseline)==20
 corners={tag:pos for tag,(pos,_) in baseline.items() if len(tag)==3}
 edges={tag:pos for tag,(pos,_) in baseline.items() if len(tag)==2}
 assert len(corners)==8 and len(edges)==12
 corner_orbits={}
 for name,word in WORDS.items():
  actual=factors(play(word))
  changed={tag for tag in baseline if baseline[tag]!=actual[tag]}
  assert len(changed)==2 and len(word.split())==int(name.split('_')[-1])
  cc='corners' in name
  assert all(len(tag)==(3 if cc else 2) for tag in changed),(name,changed)
  points=[(corners if cc else edges)[tag] for tag in changed]
  orbit={frozenset(R(p) for p in points) for R in proper24()}
  if cc:
   distance=sum(a!=b for a,b in zip(*points))
   assert len(orbit)=={1:12,2:12,3:4}[distance]
   corner_orbits[name]=orbit
   print(name,'HTM',len(word.split()),'distance',distance,'orbit',len(orbit))
  else:
   assert len(orbit)==24
   print(name,'HTM',len(word.split()),'orbit',len(orbit))
 assert len(corner_orbits['face_diagonal_corners_12']|
            corner_orbits['body_diagonal_corners_12'])==16
 all_corners=set().union(*corner_orbits.values())
 assert all_corners=={frozenset(pair) for pair in combinations(corners.values(),2)}
 assert len(all_corners)==28
 print('PASS four original-cubie physical supports and 12+4+12 corner orbits')
 print('NOTE: this verifies full cubie factors, NOT immediate sensor bit/trit outputs')
if __name__=='__main__': test()

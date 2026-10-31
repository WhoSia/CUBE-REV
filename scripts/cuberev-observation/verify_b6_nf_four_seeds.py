#!/usr/bin/env python3
"""Four constructive N-F seed certificates; replay using the archived 54-facelet cube.

python verify_b6_nf_four_seeds.py /path/to/CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip

All four pairs are two radius-6 states with exactly the two DL endpoint
corners and one near / one far ORIGINAL tagged edge changing. The 48
full cube symmetries are checked for support coverage, with mirrored
generator primes inverted as conjugation requires.
"""
import itertools,sys,zipfile
assert len(sys.argv)==2
with zipfile.ZipFile(sys.argv[1]) as z:
 ctx={"__name__":"archived_cube"};exec(z.read("independent_b4.py"),ctx)
F=ctx["F"]; N=ctx["N"]; E=ctx["E"]
pairs=[
("U L2 B' U B L2","U F' D F' D' F2"),
("U F L' F L F2","U D2 B R' B' D2"),
("U L2 F U' F' L2","U B D' B D B2"),
("R' L2 B' U B' U'","R' F' D F L2 B2")]
def play(word):
 s=ctx["START"]
 for w in word.split():s=ctx["turn"](s,ctx["A"].index(w))
 return s
def diff(a,b):
 e1,e2=ctx["ev"](a),ctx["ev"](b); c1,c2=ctx["cv"](a),ctx["cv"](b)
 return ({E[i] for i in range(12) if e1[i]!=e2[i]},
 {ctx["corner_xyz"][i] for i in range(8)
  if c1[4*i:4*i+4]!=c2[4*i:4*i+4]})
def endpoints(e):
 p=tuple(N[e[0]][i]+N[e[1]][i] for i in range(3));k=p.index(0)
 return frozenset(tuple(t if i==k else p[i] for i in range(3))
                  for t in (-1,1))
h=endpoints("DL");anti=frozenset(tuple(-x for x in p) for p in h)
star=next(e for e in E if endpoints(e)==anti)
near={e for e in E if e!="DL" and endpoints(e)&h}
far={e for e in E if e!=star and endpoints(e)&anti}
assert len(near)==len(far)==4
all_supports=set()
types=set()
for x,y in pairs:
 assert len(x.split())==len(y.split())==6
 a,b=play(x),play(y)
 assert a!=b
 edges,corners=diff(a,b)
 assert corners==h and len(edges&near)==len(edges&far)==1,(x,y,edges,corners)
 n=next(iter(edges&near));f=next(iter(edges&far))
 def attributes(e,cs):
  endpoint=next(v for v in endpoints(e) if v in cs)
  axis=next(i for i in range(3) if
            len({v[i] for v in endpoints(e)})==2)
  return endpoint[2],axis
 z1,a1=attributes(n,h);z2,a2=attributes(f,anti)
 types.add((z1*z2,a1==a2))
 for perm in itertools.permutations(range(3)):
  for signs in itertools.product((-1,1),repeat=3):
   det=(-1)**sum(perm[i]>perm[j] for i in range(3)
                 for j in range(i+1,3))*signs[0]*signs[1]*signs[2]
   rot=lambda v:tuple(signs[i]*v[perm[i]] for i in range(3))
   if frozenset(rot(v) for v in h)!=h:continue
   mapping={f:next(g for g in F if N[g]==rot(vector))
            for f,vector in N.items()}
   def moved(word):
    out=[]
    for token in word.split():
     suffix=token[1:]
     if det==-1 and suffix!="2":
      suffix="" if suffix=="'" else "'"
     out.append(mapping[token[0]]+suffix)
    return " ".join(out)
   u,v=moved(x),moved(y)
   es,cs=diff(play(u),play(v))
   assert cs==h and es=={next(g for g in E if set(g)==
                {mapping[t[0]],mapping[t[1]]}) for t in edges}
   all_supports.add(frozenset(es))
assert len(types)==4,types
assert all_supports=={frozenset((a,b)) for a in near for b in far}
print("PASS four six-HTM physical seed witness pairs, all four mirror types")
print("PASS signed cube symmetry transport + physical replay")
print("PASS exactly sixteen distinct N-F support pairs at fixed DL corners")
print("NOTE: an existence theorem, not a lower-bound or B6 base sufficiency proof")

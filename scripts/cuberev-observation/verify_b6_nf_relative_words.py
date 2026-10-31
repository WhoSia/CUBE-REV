#!/usr/bin/env python3
"""CUBE-REV: shared-prefix cancellation certificate for four N-F seeds.

Algebraic only. For word pairs x=p*a, y=p*b, the word x^{-1}y
freely reduces to a^{-1}b. Output is an HTM upper bound, never an
optimality or a full cubie-support statement.
"""
PAIRS=[
 ("A","U L2 B' U B L2","U F' D F' D' F2"),
 ("B","U F L' F L F2","U D2 B R' B' D2"),
 ("C","U L2 F U' F' L2","U B D' B D B2"),
 ("D","R' L2 B' U B' U'","R' F' D F L2 B2"),
]
def inv(token):
    if token.endswith("2"):return token
    return token[:-1] if token.endswith("'") else token+"'"
def inverse(word):return [inv(x) for x in reversed(word)]
def reduced(word):
    out=[]
    for t in word:
        if out and out[-1][0]==t[0]:
            def power(v):return 2 if v.endswith('2') else 3 if v.endswith("'") else 1
            k=(power(out.pop())+power(t))%4
            if k:out.append(t[0]+{1:'',2:'2',3:"'"}[k])
        else:out.append(t)
    return out

for name,x,y in PAIRS:
    xs,ys=x.split(),y.split()
    assert len(xs)==len(ys)==6
    assert xs[0]==ys[0]
    target=inverse(xs[1:])+ys[1:]
    assert reduced(inverse(xs)+ys)==reduced(target)
    assert len(target)==10
    print(name,"prefix",xs[0],"relative", " ".join(target))
print("PASS four common-prefix 10-HTM upper-bound certificates")
print("LIMIT free-word proof; no claim 10 is the shortest HTM length")

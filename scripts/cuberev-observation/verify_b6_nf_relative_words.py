#!/usr/bin/env python3
"""CUBE-REV: FORMAL chronological-prefix cancellation for four N-F seeds.

WARNING: this is a free-word statement in the chronological token order,
NOT an original-cubie stabilizer certificate. Physical turns act on the
original tagged pieces by LEFT composition. If p is the first executed turn,
the relevant original-tag relative g is conjugated by p, so the 10-token
auxiliary word below need NOT fix the same original cubies or prove a B5
collision. See B6_RADIUS_DOUBLING_STABILIZER.md and test_b6_word_order.py.
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
    assert xs[0]==ys[0]  # first executed action, not final action
    assert xs[-1]!=ys[-1]
    target=inverse(xs[1:])+ys[1:]
    assert reduced(inverse(xs)+ys)==reduced(target)
    assert len(target)==10
    print(name,"prefix",xs[0],"relative", " ".join(target))
print("PASS four 10-token formal auxiliary words after chronological prefix cancellation")
print("LIMIT these auxiliary words are NOT 10-HTM original-tag stabilizer witnesses")

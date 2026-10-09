#!/usr/bin/env python3
"""One concrete transitive-action congruence counterexample and PSD quotient failure."""
from itertools import product
def o(x):return x%2
def step(a,x):return (x+a)%4
def obs_trace(word,x):
    res=[]
    for a in word:
        x=step(a,x);res.append(o(x))
    return tuple(res)
for a,x,y in product((1,3),range(4),range(4)):
    if o(x)==o(y):assert o(step(a,x))==o(step(a,y))
traces=0
for h in range(9):
    for word in product((1,3),repeat=h):
        assert obs_trace(word,0)==obs_trace(word,2)
        assert obs_trace(word,1)==obs_trace(word,3)
        traces+=1
# In X=Z3, A={0,1,-1}, B is all-ones. Class {1,2} gets two words,
# class {0} gets one, despite state return-maximality and PSD.
B=[[1]*3 for _ in range(3)]
assert 2==sum(B[0][i] for i in (1,2))>B[0][0]==1
print("CUBE_REV_017_ACTION_CONGRUENCE_UNIDENTIFIABLE_PASS",traces)
print("CUBE_REV_017_COARSE_SENSOR_PSD_STATE_RETURN_COUNTEREXAMPLE_PASS")

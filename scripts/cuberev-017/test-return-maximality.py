#!/usr/bin/env python3
"""0.17 exact arithmetic regression of the general return-maximality theorem.
Mathematical proof is the PSD Gram / CS inequality in RETURN_MAXIMALITY_THEOREM.md.
This stdlib test is not a Lean formalization or substitute for that proof.
"""
def power(B,t):
    n=len(B)
    q=[[int(i==j) for j in range(n)] for i in range(n)]
    for _ in range(t):
        q=[[sum(q[i][k]*B[k][j] for k in range(n))
            for j in range(n)] for i in range(n)]
    return q
def swap(n=2):
    return [[int(j==1-i) for j in range(n)] for i in range(n)]
def cycle(n,loops=0):
    B=[[loops*int(i==j) for j in range(n)] for i in range(n)]
    for i in range(n):
        B[i][(i+1)%n]+=1
        B[i][(i-1)%n]+=1
    return B
def check(B, t, should_hold):
    Q=power(B,t)
    diag={Q[i][i] for i in range(len(B))}
    assert len(diag)==1
    return_max=all(Q[i][j]<=Q[i][i] for i in range(len(B))
                   for j in range(len(B)))
    assert return_max == should_hold, (len(B),t,return_max,should_hold)
    return Q[0][0]
# One swap (symmetric vertex-transitive but NOT PSD) falsifies odd claim.
for t in range(13):
    r=check(swap(),t,t%2==0)
    assert r==int(t%2==0)
# Symmetric inverse-closed cycle graph, negative eigenvalues: even times hold.
for n in (3,4,5,6,7):
    B=cycle(n,0)
    for t in (0,2,4,6,8,10,12):
        check(B,t,True)
# The lazy cycle B=3I+two opposite generators is PSD:
# spectrum 3+2cos(2pi k/n) >=1; holds at all odd/even horizons.
for n in (3,4,5,6,7):
    B=cycle(n,3)
    for t in range(13):
        check(B,t,True)
print("CUBE_REV_017_RETURN_MAXIMAL_EVEN_PSD_AND_ODD_COUNTEREXAMPLE_PASS")
print("test_families: swap n2, symmetric cycles n3-7, PSD lazy cycles n3-7; horizons0..12")

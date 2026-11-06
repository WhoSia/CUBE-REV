#!/usr/bin/env python3
"""R14-P5.5: source-independent finite checks of a two-sector parity-coupled
cyclic-cubie family orbit theorem; unlike P54 imports no Rubik geometry.
"""
from collections import Counter, deque
import json

def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def permutation(n,r,swaps=(),orient=()):
    arr=list(range(n));t=[0]*n
    for i,j in swaps:arr[i],arr[j]=arr[j],arr[i]
    for i,v in orient:t[i]=(t[i]+v)%r
    return tuple(r*arr[i]+(j+t[i])%r for i in range(n) for j in range(r)),parity(arr),sum(t)%r

def audit(n,m,r,s,k,l):
    assert n-k>=2 and m-l>=2 and r>=2 and s>=2
    size_a=n*r;size_b=m*s
    q={(a,b) for a in range(size_a) for b in range(size_b)}
    H=[]
    E=((),())
    def add(a_swaps=(),b_swaps=(),a_twist=(),b_twist=()):
        aa,pa,oa=permutation(n,r,a_swaps,a_twist)
        bb,pb,ob=permutation(m,s,b_swaps,b_twist)
        assert pa==pb and oa==0 and ob==0
        assert all(aa[x]==x for x in range(0,k*r,r))
        assert all(bb[x]==x for x in range(0,l*s,s))
        H.append((aa,bb))
    for j in range(k+1,n):add(a_swaps=((k,j),),b_swaps=((l,l+1),))
    for j in range(l+1,m):add(a_swaps=((k,k+1),),b_swaps=((l,j),))
    for j in range(k+1,n):add(a_twist=((k,1),(j,r-1)))
    for j in range(l+1,m):add(b_twist=((l,1),(j,s-1)))
    rest=set(q);orbits=[]
    while rest:
        v=min(rest);seen={v};todo=deque([v])
        while todo:
            x,y=todo.popleft()
            for a,b in H:
                z=(a[x],b[y])
                if z not in seen:seen.add(z);todo.append(z)
        assert seen<=rest;rest-=seen;orbits.append(len(seen))
    exceptional=int(n-k==2 and m-l==2)
    wanted=(r*k+1)*(s*l+1)+exceptional
    assert len(orbits)==wanted,(n,m,r,s,k,l,len(orbits),wanted)
    assert sum(orbits)==size_a*size_b
    if exceptional:
        hist=Counter(orbits)
        # Intact x intact breaks into TWO exactly 2rs-sized orbits.
        assert hist[2*r*s]==2,(n,m,r,s,k,l,hist)
    return len(orbits),len(H)

def main():
    cases=((4,4,2,3),(5,4,3,4),(3,3,2,2),(5,5,4,2),(2,2,2,3))
    records=[]
    for n,m,r,s in cases:
        for k in range(n-1):
            for l in range(m-1):
                count,generators=audit(n,m,r,s,k,l)
                records.append((n,m,r,s,k,l,count,generators))
    assert len(records)==9+12+4+16+1
    examples=[dict(n=n,m=m,r=r,s=s,k=k,l=l,orbits=o) for n,m,r,s,k,l,o,h in records if n-k==2 and m-l==2]
    assert len(examples)==5
    print(json.dumps({
        'result':'R14_P55_PARITY_COUPLED_TWO_SECTOR_FAMILY_ORBITS_PASS',
        'family':'(C_r wreath S_n) x (C_s wreath S_m) restricted by even orientation sums and matched permutation parity',
        'exact_orbit_rule':'(r*k+1)*(s*l+1) + 1_{n-k=2 AND m-l=2}',
        'conditions':'r,s>=2; n-k>=2; m-l>=2; one fixed first facelet per visited cubie',
        'parameter_families':list(cases),
        'all_exhaustive_slot_orbit_censuses_pass':True,
        'tested_parameter_prefix_profiles':len(records),
        'boundary_examples':examples,
        'not_claimed':'novelty priority; adaptive minimax 20 frame solution; physical HTM cost'
    },indent=2,sort_keys=True))
if __name__=='__main__':main()

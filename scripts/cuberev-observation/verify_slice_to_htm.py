#!/usr/bin/env python3
"""Normalize three x-middle-slice edge-flip sequences to pure 18-generator HTM.

Tests physical equality of all 48 movable sticker positions and orientations.
Requires sibling verify_short_support_phase.py; no historical cube solver.
"""
from verify_short_support_phase import N,T,initial,rotate,play,factors

MIXED=[
 "U' F R' U F' MR' F U' R F' U MR",
 "F U' R F' U MR' U' F R' U F' MR",
 "MR' U F' L U' F MR F' U L' F U'",
]
NORMAL={n:face for face,n in N.items()}

def normalize(seq):
    frame=0
    out=[]
    for m in seq:
        if m.startswith('MR'):
            assert m in ('MR',"MR'")
            k=1 if m.endswith("'") else -1
            out.extend(('R',"L'") if k==1 else ("R'",'L'))
            frame+=k
        else:
            f=NORMAL[rotate(N[m[0]],0,-frame)]
            out.append(f+m[1:])
    assert frame%4==0
    return ' '.join(out)

def physical_mixed(word):
    stickers=initial()
    for m in word.split():
        if m.startswith('MR'):
            k=1 if m.endswith("'") else -1
            stickers=[(rotate(p,0,k),rotate(n,0,k),c) if p[0]==0
                      else (p,n,c) for p,n,c in stickers]
        else:
            ax,layer,sgn=T[m[0]]
            power=2 if m.endswith('2') else 3 if m.endswith("'") else 1
            k=sgn*power
            stickers=[(rotate(p,ax,k),rotate(n,ax,k),c) if p[ax]==layer
                      else (p,n,c) for p,n,c in stickers]
    return stickers

base=factors(initial())
for mixed in MIXED:
    pure=normalize(mixed.split())
    assert len(pure.split())==14
    assert physical_mixed(mixed)==play(pure)
    after=factors(play(pure))
    changed={tag for tag in base if base[tag]!=after[tag]}
    assert len(changed)==2 and {''.join(t) for t in changed}=={'BU','FU'}
    print('PASS verified 14 HTM outer-only:',pure)
print('PASS 3 independent physical slice-to-HTM conversions')

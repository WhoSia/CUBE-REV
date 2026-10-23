#!/usr/bin/env python3
"""Self-contained 54-sticker geometry -> 18 legal HTM oriented-edge transitions."""
from __future__ import annotations
import json
from pathlib import Path

NORMAL = {"U":(0,1,0),"R":(1,0,0),"F":(0,0,1),
          "D":(0,-1,0),"L":(-1,0,0),"B":(0,0,-1)}
EDGES = (("U","R"),("U","F"),("U","L"),("U","B"),
         ("D","R"),("D","F"),("D","L"),("D","B"),
         ("F","R"),("F","L"),("B","L"),("B","R"))
ACTIONS = tuple(f + suffix for f in "URFDLB" for suffix in ("", "'", "2"))

def turn(v: tuple[int,int,int], axis: int, count: int) -> tuple[int,int,int]:
    x,y,z=v
    for _ in range(count % 4):
        if axis == 0: y,z=-z,y
        elif axis == 1: x,z=z,-x
        else: x,y=-y,x
    return x,y,z

def edge_transitions() -> list[list[int]]:
    stickers=[]
    for face,norm in NORMAL.items():
        for a in (-1,0,1):
            for b in (-1,0,1):
                point=(norm[0],a,b) if norm[0] else ((a,norm[1],b) if norm[1] else (a,b,norm[2]))
                stickers.append((point,norm,face))
    assert len(stickers)==54
    rows=[]
    for label in ACTIONS:
        norm=NORMAL[label[0]]
        axis=next(j for j,k in enumerate(norm) if k)
        layer=norm[axis]
        quarter=-layer*(2 if label.endswith("2") else (3 if label.endswith("'") else 1))
        rot=[(turn(p,axis,quarter),turn(n,axis,quarter),face)
             if p[axis]==layer else (p,n,face) for p,n,face in stickers]
        lookup={(p,n):face for p,n,face in rot}
        original_to_new=[]
        eo=[]
        for a,b in EDGES:
            na,nb=NORMAL[a],NORMAL[b]
            pos=tuple(na[i]+nb[i] for i in range(3))
            first,second=lookup[(pos,na)],lookup[(pos,nb)]
            try:
                idx=EDGES.index((first,second)); flip=0
            except ValueError:
                idx=EDGES.index((second,first)); flip=1
            original_to_new.append(idx);eo.append(flip)
        row=[]
        for source in range(12):
            destination=original_to_new.index(source)
            for bit in range(2):
                row.append(2*destination+(bit ^ eo[destination]))
        assert sorted(row)==list(range(24)),label
        rows.append(row)
    return rows

if __name__ == "__main__":
    print(json.dumps({"actions":ACTIONS,"edge_transitions":edge_transitions()},separators=(",",":")))

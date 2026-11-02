#!/usr/bin/env python3
"""A shared FIRST executed move is not cancellable for original-tag support.

The short relative expression for a common chronological prefix is conjugated
by that move. Toy S4 verifies the resulting tag stabilizer may differ.
This is NOT a physical 3x3 replay of the four historical B6 N-F witnesses.
"""
from pathlib import Path
import ast

def mul(a,b): return tuple(a[i] for i in b)
def inv(a): return tuple(a.index(i) for i in range(len(a)))

def main():
    p=(1,2,3,0)
    a=(1,0,2,3)
    b=(2,1,0,3)
    x,y=mul(a,p),mul(b,p)     # first execute p, then a or b
    stabilizing_relative=mul(inv(x),y)
    naive_shortening=mul(inv(a),b)
    assert stabilizing_relative==mul(inv(p),mul(naive_shortening,p))
    assert x[2]==y[2] and stabilizing_relative[2]==2
    assert naive_shortening[2]!=2

    pairs=[
      ("U L2 B' U B L2","U F' D F' D' F2"),
      ("U F L' F L F2","U D2 B R' B' D2"),
      ("U L2 F U' F' L2","U B D' B D B2"),
      ("R' L2 B' U B' U'","R' F' D F L2 B2"),
    ]
    for u,v in pairs:
        xs,ys=u.split(),v.split()
        assert len(xs)==len(ys)==6
        assert xs[0]==ys[0]     # common FIRST executed turn
        assert xs[-1]!=ys[-1]   # no common LAST executed turn
    source=Path(__file__).with_name("verify_b6_negative_witnesses.py")
    tree=ast.parse(source.read_text(encoding="utf-8"))
    archived=None
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(
            isinstance(target,ast.Name) and target.id=="W" for target in node.targets):
            archived=ast.literal_eval(node.value)
            break
    assert archived is not None and len(archived)==19
    for x,y in archived.values():
        xs,ys=x.split(),y.split()
        assert len(xs)==len(ys)==6
        assert xs[0]==ys[0], ("not a shared first action",x,y)
        assert xs[-1]!=ys[-1], ("B5 cancellation risk",x,y)
    print("PASS: all 19 archived new B6 witness pairs share first but not last action")
    print("PASS: shared executed prefix is conjugated in the original-tag relative")
    print("PASS: four B6 N-F seed pairs have shared first, distinct last moves")
    print("LIMIT: no 3x3 physical facelet replay in this isolated test")
if __name__=="__main__": main()

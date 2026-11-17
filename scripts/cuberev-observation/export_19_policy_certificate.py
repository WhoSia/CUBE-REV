#!/usr/bin/env python3
"""Export a search-derived, self-contained decision-tree witness for 19 frames.

Search requires the repository's EdgeGame. The verifier does NOT import this file
or that engine. Run beside pinned constructive scripts from Q's reproduction folder.
"""
from audit_r14_p840_constructive_19_frame import EdgeGame
from check_edge_parity_depth import representative_prefixes, COLORS
import hashlib
import json
from pathlib import Path


def export_one(prefix):
    g = EdgeGame(prefix)
    nodes = []
    count = 0

    def descend(belief, budget):
        nonlocal count
        ix = len(nodes)
        nodes.append(None)
        count += 1
        if all((belief & sign).bit_count() <= 1 for sign in g.signs):
            nodes[ix] = ["leaf"]
            return ix
        action = g.action(belief, budget, budget)
        assert action is not None
        if action == -2:
            nodes[ix] = ["repeat", descend(belief, budget - 1)]
        else:
            assert action >= 0
            nexts = {}
            for color in sorted(g.cells[action]):
                child = belief & g.cells[action][color]
                if child:
                    nexts[color] = descend(child, budget - 1)
            assert len(nexts) > 1, (prefix, action, budget)
            nodes[ix] = ["read", action, nexts]
        return ix

    root = descend(g.full, 8)
    assert root == 0
    g.action.cache_clear()
    return {"prefix":prefix,"nodes":nodes}


def main():
    reps = [''.join(c * n for c, n in zip(COLORS, counts)) for counts in sorted(representative_prefixes())]
    proof = {"schema":"cuberev-0.29-upper-policy-v1",
             "model":"first slot of eleven edges, then eight adaptive second/unread reads; corner sign released only after last edge color",
             "first_slots":11,"remaining_budget":8,"sign_release":"terminal",
             "representatives":[export_one(p) for p in reps]}
    file = Path(__file__).with_name("upper-policy-certificate.json")
    blob = (json.dumps(proof,sort_keys=True,separators=(',',':'))+'\n').encode()
    file.write_bytes(blob)
    print(json.dumps({"certificate":str(file),"sha256":hashlib.sha256(blob).hexdigest(),"bytes":len(blob),"representatives":len(reps),"nodes":sum(len(row['nodes']) for row in proof['representatives'])},indent=2))

if __name__=='__main__':main()

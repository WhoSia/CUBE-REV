#!/usr/bin/env python3
"""Independent finite action audit for CornerTurnGenerators.lean.

Checks the 12×8 cubie permutation/offset table, all 288 sticker source
positions, and the full action on each of 24 oriented corner identities per
position. It does NOT substitute for a successful Lean compilation or
induction over every length of face-turn path.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(ROOT.parents[1] / 'reproduction'))
from audit_r029_w_corner_geometric_decoder import geometry, CORNERS
from audit_r029_w_transport_all_prefixes import permutation_parity


def check():
    moves = geometry()
    assert len(moves) == 12
    source = (ROOT/'CornerTurnGenerators.lean').read_bytes()
    assert b'corner_turn_cyclic' in source
    assert b'corner_turn_zero_twist_offset' in source
    assert b'edge_corner_turn_sign_agree' in source
    generators = []
    oriented_checked = 0
    sticker_checked = 0
    for ti, perm in enumerate(moves):
        p, d = [], []
        for i in range(8):
            srcs = [perm[24+3*i+j]-24 for j in range(3)]
            assert all(0 <= v < 24 for v in srcs)
            srcpiece, offset = divmod(srcs[0], 3)
            assert srcs == [3*srcpiece+(offset+j)%3 for j in range(3)]
            p.append(srcpiece)
            d.append(offset)
            sticker_checked += 3
            for piece in range(8):
                for twist in range(3):
                    colors = CORNERS[piece][twist:]+CORNERS[piece][:twist]
                    moved = ''.join(colors[(offset+j)%3] for j in range(3))
                    newtwist = (twist+offset)%3
                    expected = CORNERS[piece][newtwist:]+CORNERS[piece][:newtwist]
                    assert moved == expected
                    oriented_checked += 1
        assert sorted(p) == list(range(8))
        assert sum(d)%3 == 0
        ep = [perm[2*i]//2 for i in range(12)]
        assert sorted(ep) == list(range(12))
        assert permutation_parity(ep) == permutation_parity(p)
        generators.append({'turn':ti, 'corner_source_pieces':p,
                           'corner_twist_offsets':d, 'edge_source_pieces':ep})
    rng = Random(0x02920261121)
    composed_checked = 0
    for _ in range(4000):
        state = [(i, 0) for i in range(8)]
        path = [rng.randrange(12) for j in range(rng.randrange(1,81))]
        for t in path:
            g = generators[t]
            state = [(state[g['corner_source_pieces'][i]][0],
                      (state[g['corner_source_pieces'][i]][1] + g['corner_twist_offsets'][i]) % 3)
                     for i in range(8)]
            assert sorted(piece for piece, _ in state) == list(range(8))
            assert sum(twist for _, twist in state) % 3 == 0
            composed_checked += 1
    return {'status':'PASS','source_sha256':hashlib.sha256(source).hexdigest(),
            'face_turns':12,'single_turn_sticker_checks':sticker_checked,
            'oriented_corner_action_checks':oriented_checked,
            'composed_turn_steps':composed_checked,
            'corner_generator_table':generators,
            'scope':'Independent finite geometric audit; Lean source still requires kernel compilation'}


if __name__=='__main__':
    print(json.dumps(check(),ensure_ascii=False,indent=2))

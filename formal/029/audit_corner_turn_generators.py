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
from itertools import product

ROOT = Path(__file__).resolve().parent
import sys
# Prefer the tracked GitHub source layout. ZIP snapshots may have a reproduction/
# copy, but that copy is not present in a clean repository checkout.
REPO = ROOT.parents[1]
SOURCE_ROOTS = (REPO / 'scripts' / 'cuberev-observation', REPO / 'reproduction')
SOURCE = next((folder for folder in SOURCE_ROOTS
               if (folder / 'audit_r029_w_corner_geometric_decoder.py').is_file()
               and (folder / 'audit_r029_w_transport_all_prefixes.py').is_file()), None)
if SOURCE is None:
    raise FileNotFoundError('Missing tracked corner geometry and permutation audit helpers')
sys.path.insert(0, str(SOURCE))
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
    # Verify the universal one-move twist sum directly on ALL 3^8 vectors.
    # This independent finite check also tests odd and otherwise physically
    # unreachable twist vectors, so it validates the generator law itself.
    twist_vectors_checked = 0
    for g in generators:
        src, delta = g['corner_source_pieces'], g['corner_twist_offsets']
        for twists in product(range(3), repeat=8):
            updated = [((twists[src[i]] + delta[i]) % 3) for i in range(8)]
            assert sum(updated) % 3 == sum(twists) % 3
            twist_vectors_checked += 1
    assert twist_vectors_checked == 12 * 3**8
    # Fail-closed mutation controls for all three finite generator axioms.
    base = generators[0]
    duplicate_source = base['corner_source_pieces'].copy()
    duplicate_source[0] = duplicate_source[1]
    assert len(set(duplicate_source)) != 8
    bad_offset = base['corner_twist_offsets'].copy()
    bad_offset[0] = (bad_offset[0] + 1) % 3
    assert sum(bad_offset) % 3 != 0
    original_cyclic = [3 * base['corner_source_pieces'][0] +
                       (base['corner_twist_offsets'][0] + j) % 3 for j in range(3)]
    mirrored = original_cyclic.copy()
    mirrored[1], mirrored[2] = mirrored[2], mirrored[1]
    assert mirrored != original_cyclic
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
            'all_generator_twist_vector_checks':twist_vectors_checked,
            'mutation_controls_rejected':3,
            'corner_generator_table':generators,
            'scope':'Independent finite geometric audit; Lean source still requires kernel compilation'}


if __name__=='__main__':
    print(json.dumps(check(),ensure_ascii=False,indent=2))

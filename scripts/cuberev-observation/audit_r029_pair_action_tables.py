#!/usr/bin/env python3
"""Independent check of the Lean `pair_actions_match` native evaluation.

Rebuilds the 48-sticker quarter turns from explicit rotation matrices (not the
cross-product formula of FaceTurns.lean and its Python transcription), requires
them to equal that transcription, then replays every pairSwap/pairFlip word of
PhysicalEdgeWords.lean on all 48 slots against adjSlot/flipSlot of
EdgeOperations.lean. A corrupted table entry must be rejected.
"""
import ast
import re
from pathlib import Path

from audit_r029_w_corner_geometric_decoder import CORNERS, EDGES, geometry

ROOT = Path(__file__).resolve().parents[2]
NORMAL = {'U': (0, 1, 0), 'R': (1, 0, 0), 'F': (0, 0, 1), 'D': (0, -1, 0), 'L': (-1, 0, 0), 'B': (0, 0, -1)}
PLUS90 = {  # +90 degrees about +x, +y, +z
    0: ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    1: ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
    2: ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
}
AXIS = {'U': 1, 'D': 1, 'R': 0, 'L': 0, 'F': 2, 'B': 2}


def apply(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def matrix_turns():
    slots = []
    for name in EDGES + CORNERS:
        normals = [NORMAL[c] for c in name]
        place = tuple(sum(n[i] for n in normals) for i in range(3))
        slots += [(place, n) for n in normals]
    index = {s: i for i, s in enumerate(slots)}
    turns = []
    for t in range(12):
        face = 'URFDLB'[t // 2]
        axis = AXIS[face]
        side = sum(NORMAL[face])  # +1 or -1: which layer, and the sign of the face normal
        m = PLUS90[axis]
        if (-1 if t % 2 == 0 else 1) * side < 0:  # Lean convention: even turn = -1 about the face normal
            m = tuple(zip(*m))
        turns.append([index[(apply(m, p), apply(m, n)) if p[axis] == side else (p, n)] for p, n in slots])
    return turns


def table(source, name):
    body = source.split(f'def {name} : Array (List Turn) := #[', 1)[1].split('\n]\n', 1)[0]
    return ast.literal_eval('[' + body + ']')


def follow(turns, word, slot):
    for t in word:
        slot = turns[t][slot]
    return slot


def adj(i, s):
    return (2 * ((i + 1) if s // 2 == i else i if s // 2 == i + 1 else s // 2) + s % 2) if s < 24 else s


def flip(i, s):
    return 2 * i + (1 - s % 2) if s < 24 and s // 2 == i else s


def check(turns, swaps, flips):
    assert len(swaps) == 121 and len(flips) == 144
    for i in range(11):
        for j in range(11):
            word = swaps[11 * i + j]
            assert all(follow(turns, word, s) == adj(j, adj(i, s)) for s in range(48)), ('swap', i, j)
    for i in range(12):
        for j in range(12):
            word = flips[12 * i + j]
            assert all(follow(turns, word, s) == flip(j, flip(i, s)) for s in range(48)), ('flip', i, j)


def main():
    turns = matrix_turns()
    assert turns == geometry(), 'matrix model differs from the transcribed Lean geometry'
    source = (ROOT / 'formal/029/PhysicalEdgeWords.lean').read_text()
    swaps, flips = table(source, 'pairSwapTable'), table(source, 'pairFlipTable')
    check(turns, swaps, flips)
    print('PASS matrix geometry equals transcription; 121 swap and 144 flip words act correctly on all 48 slots')
    bad = [list(w) for w in swaps]
    bad[1] = bad[1][:-1]
    try:
        check(turns, bad, flips)
    except AssertionError:
        print('PASS corrupted swap word rejected')
    else:
        raise SystemExit('FAIL corrupted swap word accepted')


if __name__ == '__main__':
    main()

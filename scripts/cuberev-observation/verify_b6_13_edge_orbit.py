#!/usr/bin/env python3
"""Certify a 13-HTM upper witness for 48 B6-positive F-h* sensor layouts.

Run from scripts/cuberev-observation:
  python verify_b6_13_edge_orbit.py HISTORICAL_B1_B5_ARCHIVE.zip

Uses archived independent 54-facelet physical replay and existing
verify_b6_geometric_rule.py. The >=13 lower bound is inherited from the
separately certified B6-positive full-state census, NOT proved here.
"""
import hashlib
import sys
import zipfile
from itertools import combinations
from pathlib import Path
from verify_b6_geometric_rule import EDGE_NAMES, ENDS, valid_pairs

SHA256 = "002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94"
WITNESSES = (
    "L F R' F' L' U2 R U R U' R2 U2 R",
    "U F U F2 D' L' U' L U D F2 U2 F'",
    "F R' F' L' U2 R U R U' R2 U2 R L",
)


def main(archive):
    raw = Path(archive).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA256, "wrong historical source archive"
    with zipfile.ZipFile(archive) as z:
        context = {"__name__": "verified_archived_cube", "__file__": "independent_b4.py"}
        exec(compile(z.read("independent_b4.py"), "independent_b4.py", "exec"), context)
    assert tuple(context["E"]) == tuple(EDGE_NAMES)
    F, E, A = context["F"], context["E"], context["A"]
    start, turn, ev, cv = (context[k] for k in ("START", "turn", "ev", "cv"))
    rotations = context["rotation_maps"]()
    assert len(rotations) == 24

    def replay(word):
        s = start
        for tok in word.split():
            assert tok in A
            s = turn(s, A.index(tok))
        return s

    def changed_tags(state):
        change_e = frozenset(E[i] for i, (x, y) in enumerate(zip(ev(start), ev(state))) if x != y)
        changed_c = frozenset(i for i in range(8) if cv(start)[4*i:4*i+4] != cv(state)[4*i:4*i+4])
        return change_e, changed_c

    base_states = [replay(w) for w in WITNESSES]
    assert len(set(base_states)) == 1 and base_states[0] != start
    for w in WITNESSES:
        assert len(w.split()) == 13
        assert changed_tags(replay(w)) == (frozenset(("UR", "UF")), frozenset())

    support_to_word = {}
    for _, edge_map, _, face_map in rotations:
        word = " ".join(F[face_map[F.index(t[0])]] + t[1:] for t in WITNESSES[0].split())
        state = replay(word)
        observed = changed_tags(state)
        expected = frozenset((E[edge_map[E.index("UR")]], E[edge_map[E.index("UF")]]))
        assert observed == (expected, frozenset()), (word, observed, expected)
        assert len(word.split()) == 13
        support_to_word[expected] = word
    assert len(support_to_word) == 24
    assert all(any(ENDS[a] & ENDS[b] for a, b in combinations(pair, 2))
               for pair in support_to_word)

    # Exact midpoint realization: with chronological turns g=t13...t1,
    # take x=inverse(t8..t13) (six actions), y=t1..t7 (seven actions).
    # Then x^-1*y=g as physical LEFT actions on ORIGINAL cubie tags.
    def inv_turn(token):
        return token if token.endswith("2") else (
            token[:-1] if token.endswith("'") else token+"'")
    for pair, word in support_to_word.items():
        tokens = word.split()
        left = " ".join(inv_turn(t) for t in reversed(tokens[7:]))
        right = " ".join(tokens[:7])
        assert len(left.split()) == 6 and len(right.split()) == 7
        sx, sy = replay(left), replay(right)
        assert sx != sy
        changed_e = frozenset(E[i] for i, (x, y) in enumerate(zip(ev(sx),ev(sy))) if x != y)
        changed_c = frozenset(i for i in range(8) if cv(sx)[4*i:4*i+4] != cv(sy)[4*i:4*i+4])
        assert (changed_e, changed_c) == (pair, frozenset())
    print("PASS: all 24 rotated words give exact B7 6+7 physical collision pairs")

    eligible = {(h, pair) for h in E for pair in valid_pairs(h)}
    assert len(eligible) == 156
    positive_48 = set()
    for h in E:
        neg = frozenset(tuple(-v for v in p) for p in ENDS[h])
        hstar = next(x for x in E if ENDS[x] == neg)
        far = {x for x in E if x != hstar and (ENDS[x] & ENDS[hstar])}
        assert len(far) == 4
        for f in far:
            pair = frozenset((hstar, f))
            assert (h, pair) in eligible
            word = support_to_word[pair]
            assert changed_tags(replay(word)) == (pair, frozenset())
            positive_48.add((h, pair))
    assert len(positive_48) == 48

    rest = set(positive_48)
    orbits = []
    while rest:
        h, pair = next(iter(rest))
        orbit = {(E[em[E.index(h)]], frozenset(E[em[E.index(e)]] for e in pair))
                 for _, em, _, _ in rotations}
        assert orbit <= rest
        rest -= orbit
        orbits.append(orbit)
    assert sorted(map(len, orbits)) == [24, 24]
    print("PASS: three 13-HTM words give the same two-edge-flip state")
    print("PASS: all 24 proper rotations physically replayed, exact original-tag support")
    print("PASS: each of 48 F-h* B6-positive layouts has an HTM <=13 stabilizer witness")
    print("PASS: two proper-rotation orbits of size 24")
    print("PASS: all 48 F-h* B6 layouts explicitly fail B7 via 6+7 pairs")
    print("BOUNDARY: length >=13 depends on prior B6-positive census")
    return orbits


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_b6_13_edge_orbit.py HISTORICAL_ARCHIVE.zip")
    main(sys.argv[1])

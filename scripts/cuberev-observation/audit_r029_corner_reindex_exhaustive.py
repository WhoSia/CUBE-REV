#!/usr/bin/env python3
"""Exhaustively checks the finite 8-corner generator reindex sign identity.

The theorem quantifies over permutation arrays. This file exhausts its
8! finite corner domain for every 12 turn generators; it is not Lean kernel
verification.  Edge 12! domain is NOT exhausted (separate seeded tests).
"""
from itertools import permutations
try:
    from audit_r029_cross_turn_parity import CORNER, EDGE, parity
except ModuleNotFoundError:
    from check_turn_parity import CORNER, EDGE, parity

checked = 0
for p in permutations(range(8)):
    old = parity(p)
    for src,_ in CORNER:
        new = parity(tuple(p[i] for i in src))
        assert new == (old + parity(src)) % 2
        checked += 1
assert checked == 12 * 40320
# Critical negative control: repeated labels destroy the reindex parity law.
repeated = (0, 0, 1)
swap = (1, 0, 2)
assert parity(tuple(repeated[i] for i in swap)) == 0
assert (parity(repeated) + parity(swap)) % 2 == 1
print(f'PASS: exhaustive 8! corner permutations × 12 turn source orders = {checked:,} identities')
print('PASS: repeated-label counterexample refutes unqualified reindex law')
print('CAVEAT: independent finite oracle, not a Lean proof of the code')

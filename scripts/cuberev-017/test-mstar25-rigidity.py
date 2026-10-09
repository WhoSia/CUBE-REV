#!/usr/bin/env python3
"""CUBE-REV 0.17: exact k=25 heavy-singleton rigidity prerequisite.

The theorem is conditional on the frozen physical 60-positive-base dual:
sum weights 476, 10 distinct weight-20 singleton bases, maximum mass 20
for every legal four-turn word, and that the c>=16 nonheavy projections
are precisely the public 50x116 table. This script checks the latter
14-cover UNSAT independently, NOT the physical action-semantic bridge.
No result here decides whether the FULL 1192-base M* equals 25.
"""
import json
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / 'docs/0.16/P10_50_BY_116.json'
d = json.loads(DATA.read_text())
weights = tuple(map(int, d['weights']))
cols = tuple(map(int, d['coverage_masks']))
assert len(weights) == 50 and len(cols) == 116
assert sum(weights) == 276 and len(set(cols)) == 116
TARGET = (1 << 50) - 1
@lru_cache(maxsize=None)
def mass(bits):
    total = 0
    while bits:
        bit = bits & -bits
        total += weights[bit.bit_length() - 1]
        bits ^= bit
    return total

assert {mass(c) for c in cols} == {16, 20}
assert max(map(mass, cols)) == 20
options = tuple(tuple(c for c in cols if c >> i & 1) for i in range(50))
memo = set()
visits = branches = prunes = 0

def feasible(covered, used):
    global visits, branches, prunes
    if covered == TARGET:
        return True
    remain = TARGET & ~covered
    slots = 14 - used
    if slots == 0 or mass(remain) > 20 * slots:
        prunes += 1
        return False
    state = (covered, used)
    if state in memo:
        return False
    memo.add(state)
    visits += 1
    need = mass(remain) - 20 * (slots - 1)
    candidates = None
    for i in range(50):
        if remain >> i & 1:
            viable = [c for c in options[i] if mass(c & remain) >= need]
            if candidates is None or len(viable) < len(candidates):
                candidates = viable
                if not viable:
                    break
    if not candidates:
        prunes += 1
        return False
    for col in sorted(candidates, key=lambda c: mass(c & remain), reverse=True):
        branches += 1
        if feasible(covered | col, used + 1):
            return True
    return False

assert not feasible(0, 0), "FROZEN 50x116 14-COVER BECAME SAT"
assert (visits, branches, prunes) == (165, 220, 52), (
    visits, branches, prunes
)
# If 14 candidate words cover weight 276, a single mass<=12 word
# makes the remaining maximum 13*20+12=272, a contradiction.
assert 13*20 + 12 < 276 <= 14*20
# Hence a hypothetical 25-word full cover has one c=20 word
# for each of the 10 weight-20 singleton bases; a second singleton
# or any c=0 word would leave at most 14 words for the other 50.
# The checked 14-word UNSAT excludes both cases. There are 15
# non-singleton, positive-mass words, with 15*20-276=24 defect units.
assert 25 - 10 == 15
assert 15*20 - 276 == 24
assert 24 // 4 == 6
assert 15 - 6 == 9  # at least nine other words have mass20
print("CUBE_REV_017_MSTAR25_SINGLETON_AND_POSITIVE_MASS_RIGIDITY_PASS")
print(f"public_50x116_14_unsat=YES states={visits} branches={branches} prunes={prunes}")
print("conditional_k25=10_HEAVY_SINGLETON_PLUS_15_NONHEAVY_POSITIVE; AT_LEAST_19_MASS20_TOTAL; MSTAR_UNRESOLVED")

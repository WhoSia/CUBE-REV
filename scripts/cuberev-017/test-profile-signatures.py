#!/usr/bin/env python3
"""0.17: classify every heavy20 five-word solution by word-type signature.

This is an independent indexed 3+2 FINITE classification from the original
public P10 50x116 table. It avoids 80 choose 5 enumeration but is not the
missing nonenumerative Rubik-group classification theorem.
"""
from collections import Counter
from itertools import combinations
from json import loads
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = loads((ROOT / 'docs/0.16/P10_50_BY_116.json').read_text())
CERT = loads((ROOT / 'docs/0.16/P12_CORE_CERTIFICATE.json').read_text())
COLUMNS = []
for n in P['coverage_masks']:
    orig = int(n)
    h = sum(1 << i for i, index in enumerate(CERT['heavy20'])
            if orig >> index & 1)
    l = sum(1 << i for i, index in enumerate(CERT['light8'])
            if orig >> index & 1)
    if h or l:
        COLUMNS.append((h, l, f'{h.bit_count()}H{l.bit_count()}L'))
assert len(COLUMNS) == 80
PAIRS = []
INVERTED = [0] * 20
for a, b in combinations(range(80), 2):
    h = COLUMNS[a][0] | COLUMNS[b][0]
    l = COLUMNS[a][1] | COLUMNS[b][1]
    pos = len(PAIRS)
    PAIRS.append((a, b, h, l))
    for bit in range(20):
        if h >> bit & 1:
            INVERTED[bit] |= 1 << pos
assert len(PAIRS) == 3160
FULL = (1 << 20) - 1
ALL_PAIRS = (1 << 3160) - 1
COUNTS = Counter()
TYPES = Counter()
TRIPLES = 0
for a, b, c in combinations(range(80), 3):
    TRIPLES += 1
    mh = FULL & ~(COLUMNS[a][0] | COLUMNS[b][0] | COLUMNS[c][0])
    ml = COLUMNS[a][1] | COLUMNS[b][1] | COLUMNS[c][1]
    bits = ALL_PAIRS
    while mh:
        low = mh & -mh
        bits &= INVERTED[low.bit_length()-1]
        mh ^= low
        if not bits:
            break
    while bits:
        low = bits & -bits
        bits ^= low
        pos = low.bit_length()-1
        d, e, ph, pl = PAIRS[pos]
        if d <= c:
            continue
        assert ((COLUMNS[a][0] | COLUMNS[b][0] | COLUMNS[c][0] | ph) == FULL)
        mask = ml | pl
        typ = '|'.join(sorted(COLUMNS[i][2] for i in (a, b, c, d, e)))
        COUNTS[mask] += 1
        TYPES[typ] += 1
assert TRIPLES == 82160
expected = {int(k): int(v) for k,v in
            CERT['light_profiles_17_with_multiplicity'].items()}
assert dict(COUNTS) == expected
assert dict(TYPES) == {
    '4H2L|4H2L|5H0L|5H0L|5H0L': 2628,
    '4H0L|4H2L|4H2L|5H0L|5H0L': 180,
    '3H4L|4H2L|5H0L|5H0L|5H0L': 200
}
# The 200 six-light realizations necessarily use the third signature,
# while the other 2,808 realizations use exactly four light positions.
assert sum(v for k,v in COUNTS.items() if k.bit_count()==6)==200
assert sum(v for k,v in COUNTS.items() if k.bit_count()==4)==2808
assert len(COUNTS)==17 and sum(COUNTS.values())==3008
print("CUBE_REV_017_17_LIGHT_PROFILES_THREE_SIGNATURE_TYPES_PASS")
print(f"TRIPLES={TRIPLES} PAIRS={len(PAIRS)} COMPLETIONS=3008 TYPES=3")
for k,v in sorted(TYPES.items()):
    print(f"TYPE {k} COUNT={v}")
print("NONENUMERATIVE_COMPLETENESS_OPEN")

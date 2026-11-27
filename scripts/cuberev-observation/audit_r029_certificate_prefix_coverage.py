#!/usr/bin/env python3
"""Differential replay of Lean `coverageCheck` against the frozen JSON.

Independently recomputes, for all 24576 raw first-eleven rows, the gauge-
minimal histogram under the 48 legal color maps (strict lexicographic order
on the URFDLB histogram, as `lexLess`/`counts`) and its collation-sorted
expansion, then checks the certificate `prefix` strings: every raw row's
normalized prefix is a certificate prefix, and the certificate has exactly
the 52 distinct representative prefixes. Reads the same bytes that the
SHA-256-checked Lean `include_str` evaluates (decoded from the blob).
Caveat: replays the specification, not the compiled Lean code path.
"""
import base64, gzip, hashlib, json, pathlib
from itertools import permutations, product

root = pathlib.Path(__file__).resolve().parents[2] / 'formal' / '029'
blob = root / 'certificate_blobs' / 'upper-policy-certificate.json.gz.b64'
raw = gzip.decompress(base64.b64decode(blob.read_text()))
# same bytes that Lean include_str reads (POLICY_SHA in formal/029/check_data.py)
assert hashlib.sha256(raw).hexdigest() == '80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227'
cert = json.loads(raw)
prefixes = [r['prefix'] for r in cert['representatives']]
assert len(prefixes) == 52 and len(set(prefixes)) == 52, 'certificate prefixes'

EDGES = ['DL','BL','FL','UL','DB','DF','UB','UF','DR','BR','FR','UR']
COLORS, COLL = 'BDFLRU', 'URFDLB'
OPP = dict(B='F', F='B', D='U', U='D', L='R', R='L')

def hist(word):
    return tuple(word.count(c) for c in COLL)

def lex_less(a, b):
    return a < b  # equal-length tuples: Python tuple order is lexLess

sym = []
for images in permutations(COLORS):
    m = dict(zip(COLORS, images))
    if all(m[OPP[c]] == OPP[m[c]] for c in COLORS):
        sym.append(m)
assert len(sym) == 48

def normalized_prefix(word):
    best = None
    for m in sym:
        h = hist([m[c] for c in word])
        if best is None or lex_less(h, best):
            best = h
    return ''.join(c * n for c, n in zip(COLL, best))

seen, rows = set(), 0
for omitted in range(12):
    keep = [i for i in range(12) if i != omitted]
    for bits in product([0, 1], repeat=11):
        word = [EDGES[i][b] for i, b in zip(keep, bits)]
        seen.add(normalized_prefix(word))
        rows += 1
assert rows == 24576
assert seen <= set(prefixes), sorted(seen - set(prefixes))[:3]
assert set(prefixes) <= seen, 'certificate has a prefix no raw row normalizes to'
print(f'PASS {rows} raw rows normalize into {len(seen)} prefixes')
print('PASS certificate prefix set equals the normalized prefix set (52 = 52)')

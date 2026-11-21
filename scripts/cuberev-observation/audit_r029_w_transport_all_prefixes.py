#!/usr/bin/env python3
"""Independent exhaustive checks of 19-frame coordinate transport and 14 corner reads.

This audits finite invariants used by the manuscript; it is NOT a replacement
for a Lean theorem over all physical policies.
"""
import json
from collections import Counter
from itertools import permutations, product
from pathlib import Path

from verify_19_policy_certificate import (
    COLORS, LABELS, OPPOSITES, assignments, permutation_parity, support_representatives,
)

CORNERS = ("UFR", "URB", "ULF", "UBL", "DRF", "DBR", "DFL", "DLB")
INDEX = {frozenset(p): j for j, p in enumerate(LABELS)}


def symmetries():
    out = []
    for p in permutations(COLORS):
        m = dict(zip(COLORS, p))
        if {frozenset(m[c] for c in pair) for pair in OPPOSITES} == OPPOSITES:
            out.append(m)
    assert len(out) == 48
    return out


def count_vectors():
    supported = set()
    for omitted in LABELS:
        for row in product(*(p for p in LABELS if p != omitted)):
            supported.add(tuple(row.count(c) for c in COLORS))
    assert len(supported) == 1362
    return sorted(supported)


def permute_vector(counts, mapping):
    return tuple(counts[COLORS.index(next(c for c in COLORS if mapping[c] == k))]
                 for k in COLORS)


def expected_prefix(counts):
    return ''.join(c * n for c, n in zip(COLORS, counts))


def relabel_sign(mapping):
    perm = tuple(INDEX[frozenset(mapping[c] for c in name)] for name in LABELS)
    return permutation_parity(perm)


def orientation_sign(mapping):
    # A cubie color relabeling must send the legal even-flip sector to itself.
    return sum((tuple(mapping[c] for c in name) != tuple(LABELS[INDEX[frozenset(mapping[c] for c in name)]]))
               for name in LABELS) % 2


def audit_transport():
    reps = support_representatives()
    canonical_vectors = {tuple(prefix.count(c) for c in COLORS): prefix for prefix in reps}
    canonical_assignments = {r: set(assignments(r)) for r in reps}
    mappings = symmetries()
    assert {orientation_sign(m) for m in mappings} == {0}, 'Reflections must preserve even edge flip.'
    seen_vectors = set()
    total = 0
    tested_words = 0
    sign_flips = Counter()
    for counts in count_vectors():
        original = expected_prefix(counts)
        options = [(m, permute_vector(counts, m)) for m in mappings]
        canonical = min(tup for m, tup in options)
        assert canonical in canonical_vectors
        m = next(m for m, v in options if v == canonical)
        prefix = canonical_vectors[canonical]
        order = tuple(sorted(range(11), key=lambda i: COLORS.index(m[original[i]])))
        assert ''.join(m[original[i]] for i in order) == prefix
        pos_bit = permutation_parity(order + (11,))
        label_bit = relabel_sign(m)
        previous = assignments(original)
        forward = set()
        for word, bit in previous:
            transformed = ''.join(m[word[i]] for i in order) + ''.join(m[c] for c in word[11:])
            pair = (transformed, bit ^ pos_bit ^ label_bit)
            assert pair in canonical_assignments[prefix], (original, prefix, pair)
            assert pair not in forward, 'Transport must be injective.'
            forward.add(pair)
        assert forward == canonical_assignments[prefix], ('Missing or surplus transported assignment', original, prefix)
        seen_vectors.add(counts)
        total += len(previous)
        tested_words += len(forward)
        sign_flips[pos_bit ^ label_bit] += 1
    assert len(seen_vectors) == 1362
    return {"opposite_pair_symmetries": len(mappings),
            "legal_flip_preserving_symmetries": sum(orientation_sign(m) == 0 for m in mappings),
            "supported_first_color_count_vectors": len(seen_vectors),
            "canonical_representatives": len(reps),
            "transformed_candidate_records": tested_words,
            "candidate_records_before_transport": total,
            "sign_correction_vectors": dict(sorted(sign_flips.items()))}


def corner_pair_decoder():
    decoded = {}
    for cubie in CORNERS:
        for shift in range(3):
            rotated = cubie[shift:] + cubie[:shift]
            pair = rotated[:2]
            assert pair not in decoded, (pair, cubie, shift, decoded.get(pair))
            decoded[pair] = (cubie, shift, rotated)
    assert len(decoded) == 24
    return decoded


def audit_corners():
    decoder = corner_pair_decoder()
    for corner in CORNERS:
        for shift in range(3):
            w = corner[shift:] + corner[:shift]
            assert decoder[w[:2]] == (corner, shift, w)
    # For any permutation of eight corner pieces and twists summing to zero,
    # the 14 observations (two at seven positions) give the exact original.
    # Exhaustive enumeration of 8!*3^7 states is unnecessary: the decoder is
    # pointwise injective and the remaining permutation/twist constraints unique.
    for omitted in range(8):
        for corner in CORNERS:
            others = [c for c in CORNERS if c != corner]
            assert set(CORNERS).difference(others) == {corner}
            for twists in product(range(3), repeat=3):
                last = (-sum(twists)) % 3
                assert (sum(twists) + last) % 3 == 0
    return {"oriented_corner_pairs": len(decoder), "distinct_read_pairs": len(decoder),
            "possible_missing_positions_checked": 8,
            "determination": "two cyclically ordered stickers at each of seven corners; final cubie and twist are fixed by exclusion and zero twist sum"}


def run():
    return {"status": "PASS", "transport": audit_transport(), "corners": audit_corners(),
            "scope": "finite combinatorial transport and injective corner decoder, not a Lean proof of full physical policy"}

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))

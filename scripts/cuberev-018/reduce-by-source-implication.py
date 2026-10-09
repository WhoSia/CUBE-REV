#!/usr/bin/env python3
"""CUBE-REV 0.18 — exact row-support implication quotient.

On the original sticker-derived Rubik 18-HTM source-to-dictionary incidence
matrix (1192 admissible source sets x 1323 maximal genuine four-turn words),
let R[i] be the set of candidate experiments able to distinguish S_i.
If R[i] subseteq R[j], satisfying source i *forces* source j to be
satisfied, so only inclusion-minimal row supports are needed.

This is an all-k logical equivalence. No SAT solver, P6 dual assumption,
33-specific heuristic, noise model, or human-cognition claim is involved.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--physical', required=True)
p.add_argument('--output', required=True)
a = p.parse_args()
path = Path(a.physical)
raw = path.read_bytes()
data = json.loads(raw)
assert data["schema"] == "cube-rev.018.cube-physical-mstar-maximal-v1"
assert data["counts"] == {
    "literal": 104976, "partitions": 1913,
    "coverageTypes": 1477, "maximal": 1323, "bases": 1192
}
n = 1192
k = 1323
supports = [0] * n
masks = [int(c["mask"], 16) for c in data["candidates"]]
for j, mask in enumerate(masks):
    assert mask >= 0 and mask >> n == 0
    while mask:
        b = mask & -mask
        supports[b.bit_length() - 1] |= 1 << j
        mask ^= b
assert all(supports), "Uncovered original source base"
# Stable minimal supports; equal supports retain first original index.
order = sorted(range(n), key=lambda i: (supports[i].bit_count(), i))
retained = []
for i in order:
    ri = supports[i]
    if any((supports[t] & ~ri) == 0 for t in retained):
        continue
    retained.append(i)
assert len(set(supports)) == 1146
assert len(retained) == 398
assert len({supports[i] for i in retained}) == len(retained)
# Independently check every removed source condition has a retained,
# logically stronger condition: R[retained] subseteq R[removed].
witnesses = []
for i in range(n):
    eligible = [j for j in retained if (supports[j] & ~supports[i]) == 0]
    assert eligible, ("Missing implication witness", i)
    witnesses.append(eligible[0])
assert all(witnesses[j] == j or
    (supports[witnesses[j]] & ~supports[j]) == 0 for j in range(n))
assert all(any((mask >> j) & 1 for mask in masks)
           for j in retained)
# Materialize the exact implication relation as indices into the
# frozen original base order, preserving a short independent proof.
record = {
    "schema": "cube-rev.018.row-implication-all-k-v1",
    "physical_input_sha256": hashlib.sha256(raw).hexdigest(),
    "original_constraints": n,
    "original_words": k,
    "distinct_row_supports": len(set(supports)),
    "retained_constraints": len(retained),
    "removed_constraints": n - len(retained),
    "retained_row_indices": retained,
    "removed_row_implication_witnesses": witnesses,
    "retained_degree_histogram": dict(sorted(
        Counter(supports[j].bit_count() for j in retained).items())),
    "claim": ("For every selected subset of the 1323 genuine Rubik four-turn "
              "words, covering all 398 retained original bases is logically "
              "equivalent to covering all 1192 original bases. Every "
              "discarded row has a retained row with a subset of its "
              "candidate-covering support.")
}
out = Path(a.output)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(record, indent=2) + "\n")
print("CUBE_REV_018_ROW_IMPLICATION_ALL_K_EXACT_PASS",
      json.dumps({key: record[key] for key in
        ("original_constraints", "original_words", "distinct_row_supports",
         "retained_constraints", "removed_constraints")},sort_keys=True),
      flush=True)

#!/usr/bin/env python3
"""R14-P8.29: transport the explicit B7 collision through Zassenhaus's
historical six-generator presentation, checking every one of the 288
P8.28 generator conjugacies.

This is an independent *representation consistency* audit, NOT an
independent geodesic/minimality certificate and NOT a proof of b_7.
It deliberately imports two previously distinct P48 source engines.
"""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    with redirect_stdout(StringIO()):
        spec.loader.exec_module(mod)
    return mod

z = load("p827_historical", "audit_r14_p827_zassenhaus_original_48_sticker_conjugacy.py")
b = load("p824_physical", "audit_r14_p824_independent_48_sticker_b7_collision.py")
assert z.slots == b.slots, "Independent physical slot definitions disagree"
assert len(z.all_maps) == 288

N = 48
IDENT = tuple(range(N))
def comp(a, c):
    return tuple(a[c[i]] for i in range(N))
def inv(a):
    p = [0] * N
    for i, j in enumerate(a):
        p[j] = i
    return tuple(p)
def powperm(p, k):
    out = IDENT
    for _ in range(k % 4):
        out = comp(p, out)
    return out
def pullback(p, phi):
    back = inv(phi)
    return tuple(back[p[phi[i]]] for i in range(N))

word = b.w
physical = b.state(word)
assert physical != IDENT
assert len(word) == 13
prefix = b.state(word[:6])
suffix = b.state(word[6:])
x_phys = inv(suffix)
y_phys = prefix
assert comp(inv(x_phys), y_phys) == physical
kept_stickers = {i for pos in b.kept for i in b.pieces[pos]}
assert len(kept_stickers) == 38
assert all(x_phys[i] == y_phys[i] for i in kept_stickers)

for case in z.all_maps:
    source_labels = case["source_label_to_physical_sticker_slot"]
    phi = tuple(source_labels[str(label)] for label in z.labels)
    assert set(phi) == set(range(N))
    face_map = case["source_T1_to_T6_faces"]
    signs = case["turn_direction_signs"]
    face_to_source = {f: i for i, f in enumerate(face_map)}
    assert len(face_to_source) == 6

    # Re-express the physical 13-HTM word in historical source generators.
    source_steps = []
    for token in word:
        face = token[0]
        power = 2 if token.endswith("2") else 3 if token.endswith("'") else 1
        index = face_to_source[face]
        source_steps.append(powperm(z.Hist[index], power * signs[index]))

    historical_word = IDENT
    for step in source_steps:
        historical_word = comp(step, historical_word)
    assert historical_word == pullback(physical, phi), "Word transport mismatch"

    hist_prefix = IDENT
    for step in source_steps[:6]:
        hist_prefix = comp(step, hist_prefix)
    hist_suffix = IDENT
    for step in source_steps[6:]:
        hist_suffix = comp(step, hist_suffix)
    x_hist, y_hist = inv(hist_suffix), hist_prefix

    assert x_hist != y_hist
    assert comp(inv(x_hist), y_hist) == historical_word
    assert x_hist == pullback(x_phys, phi)
    assert y_hist == pullback(y_phys, phi)

    # All 38 historical labels belonging to the 16 observed original
    # physical cubies yield the identical positions in both states.
    phi_inv = inv(phi)
    observed_historical = {phi_inv[i] for i in kept_stickers}
    assert len(observed_historical) == 38
    assert all(x_hist[i] == y_hist[i] for i in observed_historical)

print(json.dumps({
    "status": "PASS",
    "scope": "representation_transport_only",
    "historical_conjugacies_checked": len(z.all_maps),
    "turn_word_htm_length": len(word),
    "two_state_prefix_and_inverse_suffix_lengths": [6, 7],
    "observed_original_cubies": len(b.kept),
    "observed_sticker_labels": len(kept_stickers),
    "b7_minimum_resolved": False,
    "b6_positive_certificate_reexecuted": False
}, sort_keys=True))

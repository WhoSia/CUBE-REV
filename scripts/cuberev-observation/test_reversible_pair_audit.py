#!/usr/bin/env python3
"""Independent bounded enumeration checking reversible_pair_audit.py."""
from itertools import permutations, product
from reversible_pair_audit import shortest_distinguishers, signature, preset_distinguishes

def brute_pair(actions, q, s, t, maxlen):
    # Enumerate all action words until the pair graph bound is reached.
    frontier = [(s, t, ())]
    for _ in range(maxlen + 1):
        new = []
        for x, y, word in frontier:
            if q[x] != q[y]:
                return word
            for i, a in enumerate(actions):
                new.append((a[x], a[y], word + (i,)))
        frontier = new
    return None

def main():
    checked = 0
    for n in (2, 3, 4):
        for action in permutations(range(n)):
            for q in product((0, 1), repeat=n):
                actions = [action]
                actual = shortest_distinguishers(actions, q)
                for (s, t), word in actual.items():
                    expected = brute_pair(actions, q, s, t, n * (n - 1) // 2 - 1)
                    assert (word is None) == (expected is None), (n, action, q, s, t)
                    if word is not None:
                        assert len(word) == len(expected)
                        assert signature(actions, q, word, s)[-1] != signature(actions, q, word, t)[-1]
                checked += 1
    a = (1, 2, 3, 0)
    assert preset_distinguishes([a], (1, 0, 0, 0), (0, 0))
    print(f"PASS: {checked} explicit reversible single-generator/output systems (n=2..4)")

if __name__ == "__main__":
    main()


# CUBE-REV 0.28 R6 / Origin Re-entry: exact physically matched histories,
# with a causal nonidentification witness. No behavioral evidence claimed.
import unittest

class R6HistoryConfoundingPhysicalCourt(unittest.TestCase):
    def test_r6_identical_physical_endpoint_and_distinct_causal_models(self):
        from b6_independent_48sticker_goals import MOVES, compose, word
        from itertools import product

        eye = bytes(range(48))
        # Both are 2 HTM long and leave every moving sticker slot identical.
        # Their physically intermediate states and input histories differ.
        assert MOVES["U"] != MOVES["R"]
        self.assertEqual(word("U U'"), eye)
        self.assertEqual(word("R R'"), eye)
        self.assertNotEqual(word("U"), word("R"))
        self.assertEqual(compose(MOVES["U'"], MOVES["U"]), eye)
        self.assertEqual(compose(MOVES["R'"], MOVES["R"]), eye)

        # H=0/1 means the prior legal action history, Y=0/1 the following
        # action choice. Both mechanisms have the exact same observed
        # joint law P(H=h,Y=y | final_cube=solved), including full history.
        #
        # Memory mechanism: H uniform, Y is computed as H.
        # Latent-policy mechanism: Z uniform, H=Z and Y=Z; H is not a
        # causal parent of Y. Z could be a goal or planner class; this is
        # NOT a claim that humans actually possess such a binary state.
        memory = {(h,y): (0.5 if h==y else 0.0)
                  for h,y in product(range(2),repeat=2)}
        latent = {(h,y): sum(0.5 if h==z and y==z else 0.0
                             for z in range(2))
                  for h,y in product(range(2),repeat=2)}
        self.assertEqual(memory,latent)
        self.assertEqual(sum(memory.values()),1.0)
        # Both fit the observational dependence exactly, but disagree
        # under history randomization (do(H=h)) with equal current cube.
        for h in (0,1):
            interventional_memory = {y: float(y==h) for y in (0,1)}
            interventional_latent = {y: 0.5 for y in (0,1)}
            self.assertNotEqual(interventional_memory,interventional_latent)
            self.assertEqual(sum(interventional_memory.values()),1.0)
            self.assertEqual(sum(interventional_latent.values()),1.0)
        print("R6_P48_MATCHED_HISTORY_CAUSAL_NONIDENTIFICATION_PASS")

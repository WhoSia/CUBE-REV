"""Replay the ten-state example in CUBE-REV 0.29."""
from collections import defaultdict
from fractions import Fraction
from functools import cache
from itertools import combinations, permutations, product
import json

LABELS = ("UR", "UF", "UL", "UB", "DR")
HISTORY = {0: "F", 1: "U", 2: "R", 4: "U"}
SLOTS = ("B2", "C2", "D1", "D2", "E1", "E2")
UNREAD = (3, 5, 6, 7, 8, 9)


def feasible_words():
    words = set()
    completions = 0
    for order in permutations(range(len(LABELS))):
        inversions = sum(a > b for a, b in combinations(order, 2))
        if inversions % 2:
            continue
        for flips in product((0, 1), repeat=len(LABELS)):
            if sum(flips) % 2:
                continue
            completions += 1
            word = "".join(LABELS[label][::-1] if flip else LABELS[label]
                           for label, flip in zip(order, flips))
            if all(word[slot] == color for slot, color in HISTORY.items()):
                words.add("".join(word[slot] for slot in UNREAD))
    assert completions == 960
    assert len(words) == 10
    return tuple(sorted(words))


def children(words, slot):
    groups = defaultdict(list)
    for word in words:
        groups[word[slot]].append(word)
    return tuple(tuple(group) for _, group in sorted(groups.items()))


def first_query(words, slot):
    groups = children(words, slot)
    if len(groups) == 1:
        return None
    costs = [optimal_cost(group) for group in groups]
    return (1 + max(depth for depth, _ in costs),
            len(words) + sum(total for _, total in costs))


@cache
def optimal_cost(words):
    if len(words) <= 1:
        return 0, 0
    costs = [cost for slot in range(len(SLOTS))
             if (cost := first_query(words, slot)) is not None]
    # Each objective can choose its own best continuation.
    return min(depth for depth, _ in costs), min(total for _, total in costs)


def main():
    words = feasible_words()
    report = {}
    for i, slot in enumerate(SLOTS):
        sizes = sorted(map(len, children(words, i)), reverse=True)
        depth, total = first_query(words, i)
        report[slot] = {
            "partition": sizes,
            "expected_remaining_after_first": str(Fraction(sum(n*n for n in sizes), len(words))),
            "optimal_worst_cost": depth,
            "optimal_mean_cost": str(Fraction(total, len(words))),
        }
    fixed = next(len(qs) for n in range(1, len(SLOTS) + 1)
                 for qs in combinations(range(len(SLOTS)), n)
                 if len({tuple(word[i] for i in qs) for word in words}) == len(words))
    assert fixed == 3
    assert [s for s in SLOTS if report[s]["optimal_worst_cost"] == 2] == ["C2"]
    assert report["C2"]["optimal_mean_cost"] == report["D1"]["optimal_mean_cost"] == "2"
    assert report["C2"]["expected_remaining_after_first"] == "18/5"
    assert report["D1"]["expected_remaining_after_first"] == "13/5"
    print(json.dumps({"fixed": fixed, "first_query": report}, indent=2))


if __name__ == "__main__":
    main()

"""Replay the ten-state example in CUBE-REV 0.29."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache
from itertools import combinations, permutations, product
import json

LABELS = ("UR", "UF", "UL", "UB", "DR")
HISTORY = {0: "F", 1: "U", 2: "R", 4: "U"}
SLOTS = ("B2", "C2", "D1", "D2", "E1", "E2")
UNREAD = (3, 5, 6, 7, 8, 9)


def feasible_words(history=HISTORY):
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
            if all(word[slot] == color for slot, color in history.items()):
                words.add("".join(word[slot] for slot in UNREAD))
    assert completions == 960
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


def target_partitions(size, group_count):
    """Enumerate each unlabeled partition once, ordered by first appearance."""
    for labels in product(range(group_count), repeat=size):
        if tuple(dict.fromkeys(labels)) == tuple(range(group_count)):
            yield labels


def target_costs(words, labels):
    """Return minimum fixed and adaptive worst-case depths for a target."""
    target = dict(zip(words, labels))
    query_sets = [qs for size in range(len(SLOTS) + 1)
                  for qs in combinations(range(len(SLOTS)), size)]

    def fixed_identifies(slots):
        signatures = {}
        for word in words:
            signature = tuple(word[slot] for slot in slots)
            if signatures.setdefault(signature, target[word]) != target[word]:
                return False
        return True

    @cache
    def adaptive(candidates):
        if len({target[word] for word in candidates}) == 1:
            return 0
        partitions = (children(candidates, slot) for slot in range(len(SLOTS)))
        return 1 + min(max(map(adaptive, partition)) for partition in partitions
                       if len(partition) > 1)

    return len(next(qs for qs in query_sets if fixed_identifies(qs))), adaptive(words)


def target_census(words):
    census = {}
    for group_count in (2, 3):
        counts = Counter(target_costs(words, labels)
                         for labels in target_partitions(len(words), group_count))
        census[str(group_count)] = {
            f"fixed_{fixed}_adaptive_{adaptive}": count
            for (fixed, adaptive), count in sorted(counts.items())
        }
    assert census["2"] == {"fixed_1_adaptive_1": 61, "fixed_2_adaptive_2": 450}
    assert census["3"] == {"fixed_1_adaptive_1": 101, "fixed_2_adaptive_2": 8400,
                           "fixed_3_adaptive_2": 829}
    binary_labels = tuple(word[2:4] in {"UL", "LU", "UR", "RU"} for word in words)
    assert target_costs(words, binary_labels) == (1, 1)
    three_group_labels = tuple(
        0 if word[0] == "U" else 1 if word in {"DRULUB", "DRLUBU", "DLUBUR"} else 2
        for word in words
    )
    assert target_costs(words, three_group_labels) == (3, 2)
    # Keep the observed addresses and change only their colors to U, F, U, U.
    second_history = {0: "U", 1: "F", 2: "U", 4: "U"}
    second_words = feasible_words(second_history)
    yes_words = {"RLRDBU", "RBLURD", "LRBURD", "LBDRUR", "BRRDLU", "BLURDR"}
    assert len(second_words) == 12 and yes_words <= set(second_words)
    second_labels = tuple(word in yes_words for word in second_words)
    fixed, adaptive = target_costs(second_words, second_labels)
    assert (fixed, adaptive) == (3, 2)
    policy = {"R": "D1", "L": "D1", "B": "E1"}
    for branch in children(second_words, SLOTS.index("B2")):
        reply = branch[0][SLOTS.index("B2")]
        for leaf in children(branch, SLOTS.index(policy[reply])):
            assert len({word in yes_words for word in leaf}) == 1
    census["binary_counterexample"] = {
        "observed_colors": "UFUU",
        "candidate_count": len(second_words),
        "yes_words": sorted(yes_words),
        "fixed": fixed,
        "adaptive": adaptive,
        "after_B2": policy,
    }
    return census


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", action="store_true",
                        help="count the costs of all two- and three-group targets")
    args = parser.parse_args()
    words = feasible_words()
    assert len(words) == 10
    if args.targets:
        print(json.dumps(target_census(words), indent=2))
        return
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

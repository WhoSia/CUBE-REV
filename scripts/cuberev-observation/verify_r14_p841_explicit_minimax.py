#!/usr/bin/env python3
"""Verify both corner-oracle roots with explicit slot strings and all queries."""
from itertools import permutations, product
from functools import cache

EDGES = ("DL", "BL", "FL", "UL", "DB", "DF", "UB", "UF", "DR", "BR", "FR", "UR")
COLORS = "URFDLB"
UNREAD = "-"

def move_to_front(items, index):
    return items[index:index+1] + items[:index] + items[index+1:]

@cache
def count_up_to_two(labels, slots, sign, flip):
    if not slots:
        return int(sign == flip == 0)
    total = 0
    for j, word in enumerate(labels):
        for reverse, letters in enumerate((word, word[::-1])):
            if slots[0] in (UNREAD, letters[0]):
                total += count_up_to_two(labels[:j] + labels[j+1:], slots[1:],
                                         sign ^ (j % 2), flip ^ reverse)
                if total >= 2:
                    return 2
    return total

def normalized(slots, sign):
    # All single-read positions are sorted ahead of all unread positions.
    key = lambda c: (c == UNREAD, c)
    inversions = sum(key(left) > key(right) for i, left in enumerate(slots) for right in slots[i+1:])
    return ''.join(sorted(slots, key=key)), sign ^ (inversions % 2)

@cache
def can_identify(labels, slots, sign, flip, budget):
    if count_up_to_two(labels, slots, sign, flip) <= 1:
        return True
    if budget == 0:
        return False
    for i, observed in enumerate(slots):
        if observed == UNREAD:
            for side in (0, 1):
                def children():
                    for answer in COLORS:
                        updated, new_sign = normalized(slots[:i] + answer + slots[i+1:], sign)
                        yield labels, updated, new_sign, flip ^ side, budget - 1
                if all(can_identify(*child) for child in children()):
                    return True
        else:
            # Move queried position and each candidate label to the front
            # before removing them, updating the residual permutation sign.
            rest = move_to_front(slots, i)[1:]
            options = ((j, side) for j, word in enumerate(labels) for side in (0, 1)
                       if word[side] == observed)
            if all(can_identify(labels[:j]+labels[j+1:], rest, sign ^ ((i+j) % 2),
                                flip ^ side, budget - 1) for j, side in options):
                return True
    return False

@cache
def literal_wins(words, budget):
    if len(words) <= 1:
        return True
    if not budget:
        return False
    for i in range(len(next(iter(words)))):
        groups = {}
        for word in words:
            groups.setdefault(word[i], set()).add(word)
        if len(groups) > 1 and all(literal_wins(frozenset(child), budget - 1)
                                   for child in groups.values()):
            return True
    return False


def literal_words(labels, slots, sign, flip):
    for order in permutations(range(len(labels))):
        inversions = sum(left > right for i, left in enumerate(order) for right in order[i+1:])
        if inversions % 2 != sign:
            continue
        for sides in product((0, 1), repeat=len(labels)):
            if sum(sides) % 2 != flip:
                continue
            words = [labels[j][::(-1 if side else 1)] for j, side in zip(order, sides)]
            if all(observed in (UNREAD, word[0]) for observed, word in zip(slots, words)):
                yield ''.join(word if observed == UNREAD else word[1]
                              for observed, word in zip(slots, words))


def verify_literal_suffixes():
    checks = 0
    examples = (
        (EDGES[:4], ("----", "B---", "BB--", "BDL-", "BBFL", "BBBB")),
        (EDGES[4:8], ("----", "D---", "FU--", "BDF-", "BDFU", "UUUU")),
        (EDGES[8:], ("----", "R---", "RR--", "FRR-", "BFRR", "RRRR")),
    )
    for labels, histories in examples:
        for slots, sign, flip in product(histories, (0, 1), (0, 1)):
            words = frozenset(literal_words(labels, slots, sign, flip))
            assert count_up_to_two(labels, slots, sign, flip) == min(2, len(words))
            for budget in range(9):
                assert can_identify(labels, slots, sign, flip, budget) == literal_wins(words, budget)
                checks += 1
    print("literal suffix comparisons", checks)


if __name__ == "__main__":
    for sign in (0, 1):
        answer = can_identify(EDGES, UNREAD * 12, sign, 0, 18)
        assert not answer
        print("sign", sign, "wins", int(answer), "games", can_identify.cache_info().currsize, flush=True)
    verify_literal_suffixes()

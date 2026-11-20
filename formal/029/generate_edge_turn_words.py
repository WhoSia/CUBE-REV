"""Generate finite face-turn witnesses; Lean validates every final action."""
from collections import deque
from itertools import permutations, product
import json
from pathlib import Path
import sys


def inverse(path):
    return tuple(t ^ 1 for t in reversed(path))


def generate(turns):
    identity = tuple(range(48))

    def follow(path):
        result = identity
        for t in path:
            result = tuple(turns[t][s] for s in result)
        return result

    # R U' R U R U R U' R' U' R2 in lookup order.
    seed = (2, 1, 2, 0, 2, 0, 2, 1, 3, 1, 2, 2)
    start = (6, 14, 22)
    assert follow(seed) == cycle_effect(start)
    routes = {start: ()}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        for t, row in enumerate(turns):
            child = tuple(row[s] for s in state)
            if child not in routes:
                routes[child] = routes[state] + (t,)
                queue.append(child)
    assert len(routes) == 12 * 11 * 10 * 8

    def cycle(path):
        transport = routes[path]
        return inverse(transport) + seed + transport

    swaps = []
    for a, b in product(range(11), repeat=2):
        if a == b:
            swaps.append(())
            continue
        support = sorted({a, a+1, b, b+1})
        goal = swap_effect(a, b)
        factors = [tuple(2*i for i in indices) for indices in permutations(support, 3)]
        effects = {f: cycle_effect(f) for f in factors}
        if goal in effects.values():
            word = cycle(next(f for f, p in effects.items() if p == goal))
        else:
            f, g = next((f, g) for f, g in product(factors, repeat=2)
                        if tuple(effects[g][v] for v in effects[f]) == goal)
            word = cycle(f) + cycle(g)
        assert follow(word) == goal
        swaps.append(word)

    flips = []
    for a, b in product(range(12), repeat=2):
        if a == b:
            flips.append(())
            continue
        c = next(i for i in range(12) if i not in (a, b))
        base = tuple(2*i for i in (a, b, c))
        goal = tuple(s ^ int(s // 2 in (a, b)) for s in identity)
        plain = cycle(base)
        for signs in product(range(2), repeat=3):
            moved = tuple(s + d for s, d in zip(base, signs))
            word = cycle(moved) + inverse(plain)
            if follow(word) == goal:
                flips.append(word)
                break
        else:
            raise AssertionError((a, b))
    return swaps, flips


def cycle_effect(triple):
    result = list(range(48))
    for a, b in zip(triple, triple[1:] + triple[:1]):
        result[a], result[a ^ 1] = b, b ^ 1
    return tuple(result)


def swap_effect(a, b):
    def swap(i, at):
        return at+1 if i == at else at if i == at+1 else i
    return tuple(2 * swap(swap(s // 2, a), b) + s % 2 for s in range(24)) + tuple(range(24, 48))


def probe_routes(turns):
    root = (0, 24)
    routes = {root: ()}
    queue = deque([root])
    while queue:
        a, b = queue.popleft()
        for t, row in enumerate(turns):
            child = row[a], row[b]
            if child not in routes:
                routes[child] = routes[a, b] + (t,)
                queue.append(child)
    assert len(routes) == 576
    return [routes[a, b] for a, b in product(range(24), range(24, 48))]


def write_probes(path, rows):
    out = ["import FaceTurns", "", "namespace CubeRev029.Physical", "",
           "-- Generated routes from raw edge slot 0 and raw corner slot 24.",
           "def jointProbeTable : Array (List Turn) := #["]
    out += ["  [" + ", ".join(map(str, row)) + "]" + ("," if i+1 < len(rows) else "")
            for i, row in enumerate(rows)]
    out += ["]", "", "end CubeRev029.Physical", ""]
    Path(path).write_text("\n".join(out))


def main(turns, path, probes=None):
    moves = json.loads(Path(turns).read_text())
    swaps, flips = generate(moves)
    out = ["import FaceTurns", "", "namespace CubeRev029.Physical", "",
           "-- Generated from geometric quarter-turn maps by generate_edge_turn_words.py.",
           "-- Every endpoint is checked in EdgeOperations.lean.", ""]
    for name, rows in (("pairSwapTable", swaps), ("pairFlipTable", flips)):
        out += [f"def {name} : Array (List Turn) := #["]
        out += ["  [" + ", ".join(map(str, row)) + "]" + ("," if i+1 < len(rows) else "")
                for i, row in enumerate(rows)]
        out += ["]", ""]
    out += ["end CubeRev029.Physical", ""]
    Path(path).write_text("\n".join(out))
    if probes is not None:
        write_probes(probes, probe_routes(moves))


if __name__ == "__main__":
    main(*sys.argv[1:])

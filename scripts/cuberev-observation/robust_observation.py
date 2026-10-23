#!/usr/bin/env python3
"""Physical edge observation / error-correction experiment family.

Use the 24-state oriented-edge transitions exported from the actual 54-sticker
geometry rather than accepting a hand-written transition table as evidence.
No network or heavyweight solver is needed for the smoke tests.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path

ACTIONS = ("U","U'","U2","R","R'","R2","F","F'","F2","D","D'","D2","L","L'","L2","B","B'","B2")

def load_moves(path: Path) -> list[list[int]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    moves = data["edge_transitions"]
    assert len(moves) == 18 and all(sorted(row) == list(range(24)) for row in moves)
    return moves

def signatures(moves: list[list[int]], word: tuple[int, ...]) -> tuple[int, ...]:
    states = [2 * j for j in range(12)]
    signs = [0] * 12
    for depth, action in enumerate(word):
        states = [moves[action][s] for s in states]
        signs = [old | ((s & 1) << depth) for old, s in zip(signs, states)]
    return tuple(signs)

def feasible_sources(signs: tuple[int, ...], min_distance: int, max_size: int = 5) -> set[int]:
    ok = set()
    for r in range(2, max_size + 1):
        for subset in itertools.combinations(range(12), r):
            if all((signs[a] ^ signs[b]).bit_count() >= min_distance
                   for a, b in itertools.combinations(subset, 2)):
                ok.add(sum(1 << j for j in subset))
    return ok

def explore(moves: list[list[int]], length: int, min_distance: int) -> dict:
    # Literal traversal: for L=7, use the separate prefix-state DAG optimizer.
    assert 1 <= length <= 5, "Literal runner is bounded at L<=5: no fake L7 exhaustive claim."
    covered: set[int] = set()
    for word in itertools.product(range(18), repeat=length):
        covered.update(feasible_sources(signatures(moves, word), min_distance))
    return {str(r): sum(m.bit_count() == r for m in covered) for r in range(2, 6)}

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--moves", type=Path, required=True, help="JSON 54-sticker-derived 18x24 oriented-edge move table")
    p.add_argument("--length", type=int, default=2)
    p.add_argument("--errors", type=int, default=1)
    args = p.parse_args()
    print(json.dumps({"length": args.length, "errors": args.errors,
                      "feasible": explore(load_moves(args.moves), args.length, 2*args.errors+1)},sort_keys=True))
if __name__ == "__main__":
    main()

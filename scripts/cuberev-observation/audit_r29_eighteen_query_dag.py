#!/usr/bin/env python3
"""Generate and independently check a losing-strategy DAG for both 18-query roots."""
import argparse
from itertools import islice
import gzip
import hashlib
import json
from pathlib import Path

LABELS = ("DL", "BL", "FL", "UL", "DB", "DF", "UB", "UF", "DR", "BR", "FR", "UR")
COLORS = "URFDLB"
ROOTS = tuple((LABELS, "-" * 12, sign, 0, 18) for sign in (0, 1))


def parity(items):
    return sum(a > b for i, a in enumerate(items) for b in items[i + 1:]) % 2


def transitions(state):
    labels, slots, sign, flip, budget = state
    for i, known in enumerate(slots):
        for side in ((0, 1) if known == "-" else (1,)):
            children = {}
            if known == "-":
                for answer in COLORS:
                    marked = slots[:i] + answer + slots[i + 1:]
                    order = sorted(range(len(slots)), key=lambda j: (marked[j] == "-", marked[j]))
                    children[answer] = (labels, ''.join(marked[j] for j in order),
                                        sign ^ parity(order), flip ^ side, budget - 1)
            else:
                for j, label in enumerate(labels):
                    for orientation, pair in enumerate((label, label[::-1])):
                        if pair[0] == known:
                            answer = pair[1]
                            assert answer not in children
                            children[answer] = (labels[:j] + labels[j + 1:], slots[:i] + slots[i + 1:],
                                                sign ^ ((i + j) % 2), flip ^ orientation, budget - 1)
            yield children


def completions(labels, slots, sign, flip):
    if not slots:
        if sign == flip == 0:
            yield ()
        return
    for j, label in enumerate(labels):
        for orientation, pair in enumerate((label, label[::-1])):
            if slots[0] in ("-", pair[0]):
                for suffix in completions(labels[:j] + labels[j + 1:], slots[1:],
                                          sign ^ (j % 2), flip ^ orientation):
                    yield (pair,) + suffix


def generate():
    from verify_r14_p841_explicit_minimax import can_identify

    rows = {}

    def record(state):
        key = encode(state)
        if key in rows:
            return
        if state[-1] == 0:
            rows[key] = list(islice(completions(*state[:-1]), 2))
            return
        answers = []
        rows[key] = answers
        for children in transitions(state):
            color = next(c for c, child in children.items() if not can_identify(*child))
            answers.append(color)
            record(children[color])

    for root in ROOTS:
        record(root)
    return rows


def encode(state):
    labels, slots, sign, flip, budget = state
    return f"{','.join(labels)}:{slots}:{sign}:{flip}:{budget}"


def legal_witness(state, pairs):
    labels, slots, sign, flip, _ = state
    index = {''.join(sorted(label)): j for j, label in enumerate(labels)}
    if len(pairs) != len(slots):
        return False
    order, orientations = [], []
    for known, pair in zip(slots, pairs):
        j = index.get(''.join(sorted(pair)))
        if j is None or known not in ("-", pair[0]):
            return False
        order.append(j)
        orientations.append(int(pair != labels[j]))
    return (len(set(order)) == len(labels)
            and parity(order) == sign and sum(orientations) % 2 == flip)


def check(rows):
    visited = set()
    leaves = 0
    arcs = 0

    def visit(state):
        nonlocal leaves, arcs
        key = encode(state)
        if key in visited:
            return
        visited.add(key)
        proof = rows[key]
        if state[-1] == 0:
            if len(proof) != 2 or proof[0] == proof[1] or not all(
                    legal_witness(state, pairs) for pairs in proof):
                raise ValueError(f"Invalid leaf: {key}")
            leaves += 1
            return
        queries = list(transitions(state))
        if len(proof) != len(queries):
            raise ValueError(f"Missing query witness: {key}")
        for children, answer in zip(queries, proof):
            if answer not in children:
                raise ValueError(f"Invalid response: {key}")
            arcs += 1
            visit(children[answer])

    for root in ROOTS:
        visit(root)
    if len(visited) != len(rows):
        raise ValueError("Certificate contains unreachable nodes")
    return {"nodes": len(visited), "leaves": leaves, "arcs": arcs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generate", "check"))
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    if args.mode == "generate":
        rows = generate()
        args.certificate.write_text(json.dumps(rows, sort_keys=True, separators=(",", ":")) + "\n",
                                    encoding="utf-8")
    data = args.certificate.read_bytes()
    if data.startswith(b"\x1f\x8b"):
        data = gzip.decompress(data)
    print(json.dumps({**check(json.loads(data)), "sha256": hashlib.sha256(data).hexdigest()}))


if __name__ == "__main__":
    main()

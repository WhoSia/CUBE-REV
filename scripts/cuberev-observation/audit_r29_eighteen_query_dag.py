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
TRACE_QUERIES = (
    (3, 1), (9, 0), (3, 0), (1, 1), (10, 1), (0, 0), (9, 1), (1, 0), (11, 0),
    (5, 1), (0, 1), (6, 0), (10, 0), (4, 1), (5, 0), (2, 1), (11, 1), (6, 1),
)


def parity(items):
    return sum(a > b for i, a in enumerate(items) for b in items[i + 1:]) % 2


def queries(slots):
    for i, known in enumerate(slots):
        for side in ((0, 1) if known == "-" else (1,)):
            yield i, side


def slot_order(marked):
    return sorted(range(len(marked)), key=lambda i: (marked[i] == "-", marked[i]))


def transitions(state):
    labels, slots, sign, flip, budget = state
    for i, side in queries(slots):
        known = slots[i]
        children = {}
        if known == "-":
            for answer in COLORS:
                marked = slots[:i] + answer + slots[i + 1:]
                order = slot_order(marked)
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


def trace(rows, root):
    """Lift one stored path back to the original addresses and two edge states."""
    state = root
    addresses = [(i, 0) for i in range(len(LABELS))]
    fixed = {}
    history = []
    for original, side in TRACE_QUERIES:
        slot = next(i for i, (p, _) in enumerate(addresses) if p == original)
        swapped = addresses[slot][1]
        query = slot, side ^ swapped
        index = list(queries(state[1])).index(query)
        answer = rows[encode(state)][index]
        new_state = next(children[answer] for i, children in enumerate(transitions(state))
                         if i == index)
        known = state[1][slot]
        if known == "-":
            marked = state[1][:slot] + answer + state[1][slot + 1:]
            addresses[slot] = original, side
            addresses = [addresses[i] for i in slot_order(marked)]
        else:
            pair = known + answer
            fixed[original] = pair[::-1] if swapped else pair
            addresses.pop(slot)
        state = new_state
        history.append((original, side, answer))

    if state[-1] != 0:
        raise ValueError("Trace did not reach a certificate leaf")
    witnesses = []
    for residual in rows[encode(state)]:
        lifted = dict(fixed)
        for (p, swapped), pair in zip(addresses, residual, strict=True):
            lifted[p] = pair[::-1] if swapped else pair
        colors = [lifted[p] for p in range(len(LABELS))]
        if (not legal_witness(root, colors)
                or any(colors[p][side] != answer for p, side, answer in history)):
            raise ValueError("Lifted assignment does not satisfy the original history")
        witnesses.append(colors)
    if len(witnesses) != 2 or witnesses[0] == witnesses[1]:
        raise ValueError("Trace did not preserve two distinct witnesses")
    return {
        "root_sign": root[2], "edge_order": LABELS,
        "history": [(LABELS[p], side, answer) for p, side, answer in history],
        "leaf": encode(state), "lifted_edges": witnesses,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generate", "check", "trace"))
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    if args.mode == "generate":
        rows = generate()
        args.certificate.write_text(json.dumps(rows, sort_keys=True, separators=(",", ":")) + "\n",
                                    encoding="utf-8")
    data = args.certificate.read_bytes()
    if data.startswith(b"\x1f\x8b"):
        data = gzip.decompress(data)
    rows = json.loads(data)
    receipt = {**check(rows), "sha256": hashlib.sha256(data).hexdigest()}
    if args.mode == "trace":
        receipt["traces"] = [trace(rows, root) for root in ROOTS]
    print(json.dumps(receipt, indent=2 if args.mode == "trace" else None))


if __name__ == "__main__":
    main()

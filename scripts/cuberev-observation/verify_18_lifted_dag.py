"""Check the original 18-read certificate by independently lifting witnesses."""
import argparse
from dataclasses import dataclass
from functools import cache
import gzip
import hashlib
import json
from pathlib import Path

COLORS = frozenset("URFDLB")
LABELS = ("DL", "BL", "FL", "UL", "DB", "DF", "UB", "UF", "DR", "BR", "FR", "UR")


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def distinct_fields(pairs):
    fields = {}
    for key, value in pairs:
        require(key not in fields, f"Duplicate JSON key: {key}")
        fields[key] = value
    return fields


@dataclass(frozen=True)
class State:
    labels: tuple
    seen: str
    sign: int
    flip: int
    budget: int

    def key(self):
        return f"{','.join(self.labels)}:{self.seen}:{self.sign}:{self.flip}:{self.budget}"


def sign_bit(order):
    """Parity from cycle lengths, with no inversion-count routine."""
    remaining = set(range(len(order)))
    bit = 0
    while remaining:
        start = remaining.pop()
        index = order[start]
        while index != start:
            remaining.remove(index)
            index = order[index]
            bit ^= 1
    return bit


def bits(labels, words):
    lookup = {word: (index, flip)
              for index, label in enumerate(labels)
              for flip, word in enumerate((label, label[::-1]))}
    require(len(words) == len(labels), "Incorrect witness length")
    order = []
    flip = 0
    for word in words:
        require(type(word) is str and word in lookup, f"Invalid oriented label {word}")
        index, twist = lookup[word]
        order.append(index)
        flip ^= twist
    require(len(set(order)) == len(labels), "Repeated label in witness")
    return sign_bit(order), flip


def legal(state, words):
    require(isinstance(words, (tuple, list)), "Witness must be an ordered array")
    require(bits(state.labels, words) == (state.sign, state.flip), "Incorrect witness parity")
    require(all(c == "-" or c == w[0] for c, w in zip(state.seen, words)),
            "Witness contradicts its record")


def addresses(record):
    return [(i, side) for i, color in enumerate(record) for side in (0, 1)
            if side == 1 or color == "-"]


def inverse_step(state, position, side, reply):
    require(type(reply) is str and reply in COLORS, f"Invalid color reply: {reply}")
    known = state.seen[position]
    if known == "-":
        record = list(state.seen)
        record[position] = reply
        order = [i for color in sorted(COLORS) for i, c in enumerate(record) if c == color]
        order.extend(i for i, c in enumerate(record) if c == "-")
        labels = state.labels
        child_record = "".join(record[i] for i in order)

        def lift(words):
            result = [""] * len(order)
            for i, word in zip(order, words, strict=True):
                result[i] = word[::-1] if i == position and side == 1 else word
            return tuple(result)
    else:
        fixed = known + reply
        label = next((label for label in state.labels if fixed in (label, label[::-1])), None)
        require(label is not None, f"No label has sides {fixed}")
        labels = tuple(word for word in state.labels if word != label)
        child_record = state.seen[:position] + state.seen[position + 1:]

        def lift(words):
            return tuple(words[:position]) + (fixed,) + tuple(words[position:])

    # Lift the identity permutation with zero flips to measure the two offsets.
    # That baseline need not have the observed colors. The offsets apply to all
    # words because the lift is a fixed permutation/slot reversal or insertion.
    sign_offset, flip_offset = bits(state.labels, lift(labels))
    child = State(labels, child_record, state.sign ^ sign_offset,
                  state.flip ^ flip_offset, state.budget - 1)
    return child, lift


def verify(rows):
    require(isinstance(rows, dict), "Expected a mapping of states")
    arcs = leaves = 0
    reached = set()

    @cache
    def visit(state):
        nonlocal arcs, leaves
        key = state.key()
        require(key in rows, f"Missing state {key}")
        reached.add(key)
        row = rows[key]
        require(type(row) is list, f"Expected an array at {key}")
        if state.budget == 0:
            require(len(row) == 2 and row[0] != row[1], f"Need two distinct witnesses at {key}")
            for witness in row:
                legal(state, witness)
            leaves += 1
            return tuple(tuple(w) for w in row)

        queries = addresses(state.seen)
        require(len(row) == len(queries) and queries, f"Incomplete query coverage at {key}")
        for (position, side), reply in zip(queries, row, strict=True):
            successor, lift = inverse_step(state, position, side, reply)
            pair = tuple(lift(w) for w in visit(successor))
            require(pair[0] != pair[1], f"Lift merged the witnesses at {key}")
            for witness in pair:
                legal(state, witness)
                require(witness[position][side] == reply, f"Lift contradicts reply at {key}")
            arcs += 1
        return pair

    roots = [State(LABELS, "-" * 12, sign, 0, 18) for sign in (0, 1)]
    for root in roots:
        visit(root)
    require(reached == rows.keys(), "Certificate contains unreachable rows")
    return {"nodes": len(reached), "arcs": arcs, "leaves": leaves,
            "lifted_witnesses_checked": 2 * arcs, "root_signs": [0, 1]}


def read(path):
    compressed = path.read_bytes()
    raw = gzip.decompress(compressed) if compressed.startswith(b"\x1f\x8b") else compressed
    return json.loads(raw, object_pairs_hook=distinct_fields), hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    rows, digest = read(args.certificate)
    print(json.dumps({**verify(rows), "sha256_uncompressed": digest}, indent=2))


if __name__ == "__main__":
    main()

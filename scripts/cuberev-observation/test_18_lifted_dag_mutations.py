"""Confirm that representative corruptions of the frozen DAG are rejected."""
import argparse
import json
from pathlib import Path

from verify_18_lifted_dag import InvalidCertificate, LABELS, read, verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    rows, _ = read(args.certificate)
    root = f"{','.join(LABELS)}:{'-' * 12}:0:0:18"
    odd_root = root.replace(":0:0:18", ":1:0:18")
    leaf = next(key for key in rows if key.endswith(":0"))
    bad_parity = list(rows[leaf][0])
    bad_parity[0] = bad_parity[0][::-1]
    mutations = [
        ("missing query reply", {**rows, root: rows[root][:-1]}),
        ("invalid reply color", {**rows, root: ["?", *rows[root][1:]]}),
        ("missing odd root", {key: row for key, row in rows.items() if key != odd_root}),
        ("duplicated terminal witness", {**rows, leaf: [rows[leaf][0]] * 2}),
        ("wrong witness flip", {**rows, leaf: [bad_parity, rows[leaf][1]]}),
        ("unreachable row", {**rows, "unreachable": []}),
    ]
    outcomes = {}
    for name, altered in mutations:
        try:
            verify(altered)
        except InvalidCertificate as error:
            outcomes[name] = str(error)
        else:
            raise RuntimeError(f"Accepted a corrupted certificate: {name}")
    print(json.dumps(outcomes, indent=2))


if __name__ == "__main__":
    main()

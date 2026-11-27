#!/usr/bin/env python3
"""Compare the quarter-turn table printed by the real Lean `turnSlot` with an
independent rotation-matrix geometry (see audit_r029_pair_action_tables.py)."""
import sys
from pathlib import Path

from audit_r029_pair_action_tables import matrix_turns


def parse(text):
    return [[int(x) for x in line.split()] for line in text.splitlines() if line.strip()]


def main():
    lean = parse(Path(sys.argv[1]).read_text())
    assert len(lean) == 12 and all(len(r) == 48 for r in lean), 'malformed Lean turn table'
    assert lean == matrix_turns(), 'Lean turnSlot differs from the independent geometry'
    print('PASS Lean turnSlot equals the independent rotation-matrix geometry for all 12 turns')
    lean[5][7], lean[5][8] = lean[5][8], lean[5][7]
    assert lean != matrix_turns()
    print('PASS a swapped table entry is detected')


if __name__ == '__main__':
    main()

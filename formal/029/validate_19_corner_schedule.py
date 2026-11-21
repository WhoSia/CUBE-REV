#!/usr/bin/env python3
"""Cross-check the actual 19-frame controller and its Lean schedule declaration.

This is a build-time consistency check, not an alternative to the Lean proof.
The two independent representations must agree exactly, including repetitions
and the final read. Rejects mutations that would leak a future color or omit a
required observation.
"""
from collections import Counter
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRIPT = next((folder for folder in (ROOT / 'scripts' / 'cuberev-observation', ROOT / 'reproduction')
               if (folder / 'audit_r029_x_end_to_end.py').is_file()), None)
if SCRIPT is None:
    raise FileNotFoundError('Missing the pinned X controller source (not a proof of soundness).')
sys.path.insert(0, str(SCRIPT))
from audit_r029_x_end_to_end import CORNER_SCHEDULE  # noqa: E402


def lean_schedule(text: str) -> tuple[int, ...]:
    match = re.search(r'def\s+cornerFrameAddresses\s*:[^=]*:=\s*\[([^]]+)\]', text, re.S)
    if match is None:
        raise ValueError('Cannot locate the Lean frame schedule declaration.')
    return tuple(int(x) for x in re.findall(r'\b\d+\b', match.group(1)))


def check_schedule(observed: tuple[int, ...]) -> None:
    if len(observed) != 19 or any(not 0 <= x < 24 for x in observed):
        raise ValueError('The schedule must have exactly 19 valid corner addresses.')
    if len(set(observed)) != 14:
        raise ValueError('There must be exactly 14 distinct corner addresses.')
    if len(set(observed[:11])) != 11:
        raise ValueError('The first eleven corner reads must be distinct.')
    if 4 in observed[:18] or observed[18] != 4:
        raise ValueError('URB[2] must be released only at frame 19.')
    if observed[13:18] != (21,) * 5:
        raise ValueError('Frames 14–18 must use the known DLB[1] padding color.')
    address_counts = Counter(observed)
    distinct_counts = Counter(x // 3 for x in address_counts)
    if distinct_counts != Counter({i: 2 for i in range(8) if i != 5}):
        raise ValueError('The seven observed corners must omit only position five.')
    if any(x % 3 == 2 for x in address_counts):
        raise ValueError('The schedule must read two cyclic stickers per corner.')


def main() -> None:
    declaration = (HERE / 'NineteenSchedule.lean').read_text()
    lean = lean_schedule(declaration)
    physical = tuple(CORNER_SCHEDULE)
    if lean != physical:
        raise ValueError(f'Lean/controller schedule mismatch: {lean} != {physical}')
    check_schedule(lean)
    for replacement in (
        lean[:18] + (3,),
        lean[:13] + (4,) + lean[14:],
        lean[:13] + (22,) + lean[14:],
    ):
        try:
            check_schedule(replacement)
        except ValueError:
            pass
        else:
            raise AssertionError('Corrupted corner schedule was accepted.')
    print('PASS 19 corner-frame addresses; 14 distinct; omitted corner 5; 3 mutations rejected')


if __name__ == '__main__':
    main()

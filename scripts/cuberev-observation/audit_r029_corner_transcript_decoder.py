"""Independent audit of the BW/BX constructive corner decoder.

Factor courts (not the Cartesian product): all 8! piece permutations at
zero twist; all 3^7 legal twist vectors at identity permutation.
"""
from itertools import permutations, product

NAMES = ("UFR", "URB", "ULF", "UBL", "DRF", "DBR", "DFL", "DLB")
COLORS = "BDFLRU"
SCHEDULE = (0, 1, 6, 7, 9, 10, 18, 19, 21, 22, 12,
            13, 3, 21, 21, 21, 21, 21, 4)
POSITIONS = (0, 1, 2, 3, 4, 6, 7)

def color(x, j):
    return COLORS.index(NAMES[x // 3][(x % 3 + j) % 3])

PAIRS = {(color(x, 0), color(x, 1)): x for x in range(24)}
assert len(PAIRS) == 24

def encode(a):
    return [color(a[s // 3], s % 3) for s in SCHEDULE]

def decode(r):
    if len(r) != 19 or any(not 0 <= c < 6 for c in r):
        return None
    if any(c != r[8] for c in r[13:18]):
        return None
    a = [None] * 8
    for i in POSITIONS:
        x = PAIRS.get((r[SCHEDULE.index(3*i)], r[SCHEDULE.index(3*i+1)]))
        if x is None:
            return None
        a[i] = x
    pieces = [a[i] // 3 for i in POSITIONS]
    if len(set(pieces)) != 7:
        return None
    p = 28 - sum(pieces)
    if not 0 <= p < 8:
        return None
    a[5] = 3*p + (-sum(a[i] % 3 for i in POSITIONS)) % 3
    return a

def main():
    count = 0
    for p in permutations(range(8)):
        a = [3*x for x in p]
        assert decode(encode(a)) == a
        count += 1
    assert count == 40320
    count = 0
    for t in product(range(3), repeat=7):
        a = [3*i+x for i,x in enumerate((*t, -sum(t)%3))]
        assert decode(encode(a)) == a
        count += 1
    assert count == 2187
    r = encode([3*i for i in range(8)])
    def changed(i, x):
        return r[:i] + [x] + r[i+1:]
    duplicate = r.copy()
    duplicate[2:4] = r[:2]
    for bad in (r[:-1], r+[0], changed(13,(r[13]+1)%6),
                changed(0,6), changed(1,r[0]), duplicate):
        assert decode(bad) is None
    a = [0,3,9,12,15,6,18,21]
    b = [0,6,9,12,15,3,18,21]
    assert encode(a)[:18] == encode(b)[:18]
    assert encode(a)[18] != encode(b)[18]
    def sign(a):
        return sum(x//3 > y//3 for i,x in enumerate(a)
                   for y in a[i+1:]) % 2
    assert sign(a) != sign(b)
    print("PASS: 40320 permutation cases, 2187 twist cases, 6 negatives, early sign collision")

if __name__ == "__main__":
    main()

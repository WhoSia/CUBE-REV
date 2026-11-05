#!/usr/bin/env python3
"""R11: exactly classify 18/19/20 single-color CORNER facelet schedules.

Uses the independent 3D-generated P48 corner PIECES/SLOTS/FACES convention.
For each omitted set, enumerate every corner label assignment and legal
three-cycle orientation consistent with observed colors of SOLVED corners;
optionally require same corner permutation parity as the solved edges.

An omitted spatial facelet still belongs to the same corner position.
Counts are across all C(24,k) spatial omission masks, not 3D RGB cameras.
The full-corner state of an arbitrary true cube has the same fiber counts
under physical group transport of queries (the proof is in the R11 note).
"""
from collections import Counter, defaultdict
from itertools import combinations
from b6_independent_48sticker_goals import CORNERS, PIECES, SLOTS, FACES, word

NORMAL_TO_COLOR={v:k for k,v in FACES.items()}
CUBIES=tuple(tuple(NORMAL_TO_COLOR[SLOTS[s][1]]
                    for s in PIECES[p]) for p in CORNERS)
assert len(CUBIES)==8 and len(set(map(frozenset,CUBIES)))==8
ALL_SLOTS=tuple((i,k) for i in range(8) for k in range(3))

def corner_fiber(omitted, corner_parity=None, max_solutions=2):
    """Count original-to-slot corner configurations matching solved colors."""
    omitted=set(omitted)
    unresolved=tuple(i for i in range(8)
                     if any((i,k) in omitted for k in range(3)))
    potential=[]
    for dest in unresolved:
        opts=[]
        for src in unresolved:
            for twist in range(3):
                # Destination sticker k receives source sticker (k+twist)
                # in this convention; it is the inverse of physically
                # composing source-to-destination twist but 0 sum is invariant.
                if all(CUBIES[src][(k+twist)%3]==CUBIES[dest][k]
                       for k in range(3) if (dest,k) not in omitted):
                    opts.append((src,twist))
        potential.append(opts)
    count=0
    def visit(depth,used,assigned,twist_sum):
        nonlocal count
        if count>=max_solutions:return
        if depth==len(unresolved):
            inversion=sum(assigned[i]>assigned[j]
                          for i in range(len(assigned))
                          for j in range(i+1,len(assigned)))%2
            if twist_sum%3==0 and (corner_parity is None or
                                   inversion==corner_parity):
                count+=1
            return
        for source,twist in potential[depth]:
            if source in used:continue
            visit(depth+1,used|{source},
                  assigned+(unresolved.index(source),),twist_sum+twist)
    visit(0,set(),(),0)
    assert count>=1
    return min(count,max_solutions)

def _profile(mask):
    counts=Counter(i for i,k in mask)
    return tuple(sorted(counts.values(),reverse=True))

def audit():
    expected={
        4:{None:(10590,36),0:(10626,0)},
        5:{None:(41784,720),0:(42504,0)},
        6:{None:(127796,6800),0:(134528,68)}
    }
    for omitted,settings in expected.items():
        counters={p:Counter() for p in settings}
        byshape=defaultdict(Counter)
        witness={}
        for mask in combinations(ALL_SLOTS,omitted):
            for parity in settings:
                n=corner_fiber(mask,parity)
                counters[parity][n]+=1
                byshape[(parity,_profile(mask))][n]+=1
                if n==2 and parity not in witness:
                    witness[parity]=mask
        for parity,(unique,ambiguous) in settings.items():
            assert (counters[parity][1],counters[parity][2])==(
                unique,ambiguous),(omitted,parity,counters[parity])
            assert unique+ambiguous==len(tuple(combinations(ALL_SLOTS,omitted))) if omitted==4 else True
            print("R11_CORNER_MASK_CENSUS",
                  "read",24-omitted,"missing",omitted,
                  "edge_parity_oracle",str(parity),
                  "unique",unique,"ambiguous",ambiguous)
            if parity in witness:
                print("R11_CORNER_AMBIGUITY_WITNESS",
                      "read",24-omitted,"edge_parity_oracle",str(parity),
                      "unread",",".join(f"{CORNERS[i]}:{CUBIES[i][k]}"
                                        for i,k in witness[parity]))
        for (parity,pattern),hist in sorted(byshape.items(),
                                            key=lambda z:(str(z[0][0]),z[0][1])):
            if hist[2]:
                print("R11_CORNER_BAD_PATTERN","read",24-omitted,
                      "edge_parity_oracle",str(parity),
                      "pattern",pattern,"ambiguous",hist[2])
    print("R11_CORNER_PARITY_COUPLING_PASS",
          "20_reads_without_edge_parity_unique=10590/10626",
          "19_reads_with_edge_parity_unique=42504/42504",
          "19_reads_without_edge_parity_unique=41784/42504",
          "18_reads_with_edge_parity_ambiguous=68/134596")
    print("R11_BOUNDARY corner-sensor observability only;",
          "global adaptive exact horizon remains 18..21")

if __name__=="__main__":
    audit()

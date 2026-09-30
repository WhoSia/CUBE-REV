# CUBE-REV Generation VI G6-CLOSE — Results

## Exact executable authority
- strict science HEAD: `8fc47583baef1cec60573411fff06188860fee36`
- GitHub Actions run: `36659952229` — SUCCESS
- artifact: `11073428675`
- artifact digest: `sha256:9a85580f8a2d9a828fb35295c9c8246cf28f1b05488dfc5cda55020e278115e2`
- same-head gates: rustfmt, workspace check/tests, G6-P1, G6-P2, G6-P6, G6-CLOSE, G5-P5-R3 and G5-P6 — all PASS

## Frozen domain
- `dG=3`
- `d1=2`
- 960 full states
- 50 phase-1 q coordinates
- phase-2 cost exact through G1 radius 6

## Shortest-entry matched bank
Two raw same-q divergent representative pairs occur, but C4 relabeling reduces them to **one independent family**.

The family contains:
- `U F B` vs `F B U2`
- C4-equivalent `U R L` vs `R L U2`

Within each pair, `dG`, `d1`, and q match. One state has shortest-entry phase-2 costs `(1,2,2,3)`; the other has four shortest endpoints certified `d2>6`.

## Slack-only matched bank
A stronger contrast occurs in **48 q coordinates**.

Each deterministic pair is matched on:
- `dG=3`
- `d1=2`
- exact q
- shortest-entry cost signature `n2:[1,2]:gt6=0`

but differs in +1-slack signature:
- `n4:[0,1,1,2]:gt6=0`
- versus `n4:[1,2,2,3]:gt6=0`.

There are **48 raw pairs**, reduced by C4 to **24 independent families**.

Example:
- `R2 L U` vs `U L U`
- q `(142,0,405)`
- same shortest profile `(1,2)`
- different value of one additional phase-1 move.

## Generation-VI synthesis
Tested ladder:

`weak projected PDB -> exact q/d1 -> shortest endpoint-cost fiber -> slack frontier -> full state`

Closure refinement:

> Exact phase coordinate plus shortest-entry continuation geometry does not determine the value of one additional unit of phase-1 lookahead.

This is an exact 3×3 planning-horizon result on the frozen domain.

## Authority ceiling
No global frequency estimate, globally minimal representation, full D4h executable census, or behavioral-equivalence claim is made.

P4-R4 viewpoint/mixed-radix remains BLOCKED.
G4-R2 provenance remains HOLD.
World contact remains CLOSED.

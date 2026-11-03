# P0.28 — Disconnected optimal-sensor swap graph (a local-search barrier)

**Date:** 2026-11-03. **Status:** intrinsic finite graph theorem PASS; B6 physical meaning is inherited from the existing 0.28 facelet-positive and facelet-negative certificates. Not a new radius-six facelet census, nor a new general theory of matroids.

## Problem

Take the *actual* 16-tag original-cubie B6-injective sensor designs, with all observations of each selected original tag recording its full cubie position and orientation. Fix the two unobserved original corner tags to be the endpoints of a cube edge h. All such designs observe the remaining six corners and 10 of the 12 original edge tags.

Each design is represented by an omitted edge **2-set** E. Exactly 13 E are B6-positive for this h according to the previous facelet-certified 0.28 four-case geometric criterion. An edge in the *sensor-swap graph* joins two designs iff one observed edge tag is exchanged for another observed edge tag and the resulting design is also B6-positive. In omission notation, E and F are adjacent iff |E symmetric_difference F|=2.

## Exact combinatorial result

For each of the 12 possible h, the original 12-vertex graph whose edges are the allowed omitted edge pairs decomposes as

    W_5 disjoint_union C_4 disjoint_union K_2 disjoint_union K_1,

where W_5 is the 5-vertex wheel (8 edges), C_4 a four-cycle (4 edges), and K_2 a single edge. The 12-vertex graph has 13 allowed edges in total.

The sensor-swap graph is the **line graph** of that allowed-omission graph. Consequently its connected components have

    |V(component)| = 8, 4, 1.

The number of links within the 8-vertex component is
C(4,2)+4*C(3,2)=18, since the wheel has degree profile
(4,3,3,3,3). The C4 contributes 4 links and K2 contributes 0.
Thus the 13-vertex sensor-swap graph has exactly **22 links**.
There are 12 such independent fixed-corner sectors, giving
156 labelled layouts and 264 within-sector one-tag-swap links
(counting links of each fixed-h graph once). The full 20-tag
single-sensor swap graph has NO cross-h edge either, because
different 2-corner omissions would require changing at least one
corner tag but also edge omission patterns could remain identical;
this latter issue is **NOT yet independently enumerated** and the
264-link total is ONLY the within-fixed-h subtotal, not necessarily
the full 156-vertex swap-graph edge count.

For the particular two valid sensor designs with h=DL,
E_A={FR,UR} and E_B={DR,UL}, the existing explicit matroid-exchange
counterexample shows one forbidden swap; the line-graph argument
now proves they lie in distinct connected components within
the fixed-h sector, so **no sequence of B6-valid single edge-tag
swaps holding the omitted corner pair fixed can connect them**.

## Controlled finite regression

- scripts/cuberev-observation/verify_b6_sensor_exchange_graph.py
  derives the 13 nodes directly from the independent intrinsic
  cube-incidence predicate; it does NOT query historical success mask IDs.
- scripts/cuberev-observation/test_b6_sensor_exchange_graph.py
  checks all 12 h, 8+4+1 component sizes, 22 links, an explicit
  disconnected pair, and reciprocal one-sensor-swap adjacency.
- Negative control: all C(12,2)=66 omission pairs are accepted.
  Their sensor-swap graph is the Johnson graph J(12,2):
  connected, degree 20, with 660 edges.
- Existing previous proof: verify_b6_geometric_bridge.py plus
  actual B6-positive 41-target MITM and rotated negative witnesses.
  The current test is **only the combinatorial layer**.

## Interpretation and caution

This is not an NP-hardness proof or a claim that local optimization is
impossible; allowing temporary worse-than-optimal designs, simultaneous
multi-sensor swaps, changed corner omissions, or different sensor costs
can connect regions. It **does** establish that a local search restricted
to this fixed pair of omitted corners and always maintaining optimal
B6 injectivity may become trapped within one of the components.

The mathematical ingredients (line graphs, wheel graphs, matroid
basis-exchange counterexamples) are classical. The contribution is a
concrete, finite, physical-cube-specific obstruction and a reproducible
combinatorial explanation rather than a new generic graph theorem.

## Prior art and paper question

Cameron (1999), Permutation Groups §4.14, cautions that permutation
group bases do not necessarily have vector-space exchange properties.
Bailey & Cameron (2011), Base Size, Metric Dimension and Other
Invariants of Groups and Graphs, emphasize repeated reinvention of
stabilizer concepts in different terminology. Therefore do not claim
new discovery of nonmatroidal permutation group bases; present this
as a quantified geometric phase obstruction in the original-radius
physical cube model.

Paper-ready question: Can we derive the entire fixed-h 13-layout
geometry and the B6 word-metric positive/negative grading from a
short, independently checked physical difference-support theorem?
The 8+4+1 exchange graph is explanatory but does **not** replace
the 41-goal HTM>=13 proof obligation.

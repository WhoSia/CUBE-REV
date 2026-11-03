# CUBE-REV 0.28 — A structural 24×3 proof of the complete B6 optimal-sensor exchange graph

**Status:** exact finite cube-incidence theorem derived from the previously certified four-case positive layout criterion, with a separate 156-node BFS and independent JavaScript face-normal implementation as controls. **Not** an independently rerun B6 physical 54-sticker, HTM-geodesic, or positive-mask certification.

## Definition and source boundary

Let h range over 12 original geometric edges of the 3x3 cube. The two omitted oriented corner tags of every B6-positive 16-tag design are the endpoints C_h of h. Let F_h be the 13 omitted-edge-tag pairs E (subsets of size 2 from the 12 original edge tags) that obey the previously verified four-case B6 geometric criterion. Each design is the 4-element omitted-tag set C_h ∪ E.

Two designs are adjacent if their 16-element OBSERVED tag sets differ by removing exactly one tag and adding exactly another one. Equivalently their omitted-tag sets have symmetric difference of size 2.

- Same h: |E Δ E'|=2.
- Different h, k: |C_h Δ C_k|=2 is necessary and sufficient for the corner contribution to be exactly one tag; this holds iff h and k share ONE endpoint corner. Since the combined omitted-tag XOR must be exactly two, the edge omission pairs must be IDENTICAL: E=E'∈F_h∩F_k.
- Different h, k with no shared endpoint: |C_h Δ C_k|=4, so NO one-tag swap is possible.

Thus all cross-h edges correspond **bijectively** to triples (h,k,E) where unordered h,k share a corner and E∈F_h∩F_k.

## Lemma 1 — the fixed-corner part

For every h the allowed-edge-pair graph on twelve physical edge tags decomposes as

    W5 ⊔ C4 ⊔ K2 ⊔ K1,

where W5 is the 5-vertex wheel with 8 edges, C4 the 4-cycle with 4 edges, K2 a single edge. In the one-observed-tag-swap graph at fixed h, each allowed pair is itself a vertex. This is the line graph of the allowed graph, so its component sizes are 8, 4 and 1. The line graph of W5 has

    binom(4,2) + 4 binom(3,2) = 18

edges, because its original wheel has degrees 4,3,3,3,3. The C4 line graph contributes 4 more, and K2 contributes none. Thus each fixed h yields 13 nodes and 22 within-h links.

This is standard line-graph algebra; the cube-dependent input is the *specific admissibility geometry*.

## Lemma 2 — exactly three cross-core links for every adjacent h,k

Two distinct original cube edges meet in exactly one corner iff they belong to a pair of the three edges incident at that cube corner. There are

    8 × binom(3,2) = 24

such UNORDERED adjacent core-edge pairs. The 24 proper cube rotations act transitively on unordered adjacent edge-pairs, and preserve the four-case admissibility criterion, so it is enough to check one representative h=DL and k=DF (their omitted corner-tag pairs share one original cube corner).

Direct geometric incidence calculation gives

    F_DL ∩ F_DF = {
      {BR,UB}, {BR,UR}, {UB,UR}
    }.

All three pairs lie within the 8-edge W5 component of both F_DL and F_DF. The 24-rotation equivariance of the geometric rule, independently verified in earlier 0.28 code, transports this statement to every adjacent h,k. The separate small Python program in this turn ALSO checks all 24 adjacent pairs directly and never assumes the 3-per-pair conclusion.

Therefore cross-h one-tag swaps number exactly

    24 × 3 = 72,

and every cross-h link joins only wheel components, never a C4 or isolated K2 sector.

## Theorem — exact full swap topology

The 12 wheel line-graph components each have eight optimal designs. The graph on 12 core edges, joining h,k iff they meet at one original cube corner, is connected (the line graph of the connected cube-edge/vertex graph). By Lemma 2, every such adjacent h,k induces at least one link between their wheel components. Hence all 12×8=96 wheel-derived designs form one connected component of size **96**.

The twelve C4 line-graph components remain mutually disconnected and disconnected from all wheel parts by Lemma 2. Each contains four designs. The twelve original K2-edge singletons have no within-h or cross-h swap neighbors and remain isolated. Thus the global 156 optimal designs split into

    96 + 12×4 + 12×1 = 156
    number of connected components = 1+12+12=25.

Total undirected links:

    12×22 + 24×3 = 264+72=336.

The degree histogram (checked by the full graph finite auditor) is

    0:12, 2:48, 4:24, 6:24, 7:48,

whose weighted degree sum 0×12+2×48+4×24+6×24+7×48=672 equals 2×336 as a second count.

QED, conditional on the original positive-layout geometric criterion.

## Independent checks, precise independence statement

- verify_b6_cross_core_bridge.py: derives 24 adjacent core-edge pairs, exact 3 shared omitted-edge pairs per pair, their membership in W5 components, and the connectivity of the underlying 12-core adjacency graph. Does **not** build the full 156-node swap graph.
- test_b6_cross_core_bridge.py: four regressions including all 24 pairs and named DL–DF bridge.
- audit_b6_full_sensor_swap_graph.py: separate 156-node graph, 336 edges, 25 components and per-core structure; tests fail-closed on incorrect counts.
- independent_js_b6_exchange_graph.mjs: independent JavaScript translation from six cube face vectors to allowed omissions and 156-node graph, cross-checking the same 25-component signature. Shares the four-case *scientific criterion*, not implementation code.
- Existing verify_b6_geometric_rule.py: validates 24 proper rotations and 13 admissible omitted-edge pairs per h.
- B6 41-target original-physical positive proof and 19 rotated original-physical negative witnesses: **inherited**, not recalculated by these combinatorial checks.

## Consequences, nonconsequences and publication assessment

Under the historical original-cubie B6 injectivity proof, the set of globally minimum 16-sensor designs is disconnected under any sequence of one-sensor exchanges that maintains both budget 16 and B6 injectivity at EVERY intermediate design, **even allowing changes of the omitted corner pair**. The design landscape is an example where ordinary matroid basis exchange and swap-connectedness fail.

This does **not** establish computational complexity lower bounds for general cube-sensor optimization; the full ground set here is only 20 tags and temporary infeasible or nonminimal designs, multiple simultaneous swaps, or altered cost functions may reconnect all sectors. Classic determining-set and resolving-set exchange failures are prior work (Boutin 2009/2010, Cameron 1999). The original contribution if any is the explicit physically constrained B6 finite model and its 24×3 incidence geometry, subject to further novelty review.

Priority for next independent research: derive a short **original 18-HTM word-metric** reason why exactly these W5/C4/K2 omission pairs admit no ≤12 nonidentity stabilizer element. Unlike the 24×3 graph topology, that missing proof cannot follow merely from abstract stabilizer order or standard line-graph identity.

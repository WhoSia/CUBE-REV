# Manuscript Appendix Draft — Histogram-Gauge Ambiguity and the Stable-Sort Sign Cocycle
**CUBE-REV 0.29, AP version; prepared as an additive appendix to the working research manuscript, not an overwrite of preserved paper T/U/V/W.**

## A. The normalization-map witness is part of a decision history

The reduction of 1,362 feasible first-eleven color histograms to 52 representatives is mathematically correct. Yet a histogram representative is not a *canonical labeled state*: forty representatives have nontrivial color-automorphism stabilizers. Therefore any transport theorem that refers only to the target representative, without retaining the map that carried the actual observed word to that representative, loses data required by inverse reconstruction.

The issue is especially consequential for the edge/corner permutation parity coupling. For any color automorphism (g), let (\alpha_g\in S_{12}) be the permutation induced on unordered edge types. As proved by a generator argument, its sign equals that of the corresponding permutation (\tau_g\in S_3) of opposite-color pairs. But the frozen policy does not act by (\alpha_g) alone. It also applies a **stable sort** of the eleven already observed first-color positions, represented by an index permutation (\beta_{g,n}), and fixes the twelfth edge slot.

The parity correction is therefore
[
\varepsilon(g,n)=\operatorname{parity}(\alpha_g)+
\operatorname{parity}(\beta_{g,n})\pmod2.
]
This is the quantity used when converting a normalized edge candidate's parity sign to the physical corner permutation parity. Computing only (\operatorname{parity}(\alpha_g)) is insufficient.

## B. Closed formula and cocycle theorem

Take colors (c_0<\dots<c_5) in the frozen lexical order `URFDLB`, and let (n_i) denote the observed count of (c_i). The sorted initial word contains (n_0) copies of (c_0), then (n_1) copies of (c_1), and so on. For any (g), the stable sort of (g)'s image reorders whole color blocks. A reversal of transformed block order between (c_i) and (c_j) causes exactly (n_i n_j) inversions; no same-color pair contributes. Consequently
[
\operatorname{parity}(\beta_{g,n})=
\sum_{0\le i<j\le5}
n_i n_j
[\operatorname{rank}(g(c_i))>\operatorname{rank}(g(c_j))]
\pmod2.
]
This reduces the correction to fifteen color-block comparisons, independent of the number of legal edge permutations. The coefficient (n_i n_j) may be replaced by the product of the parities of (n_i) and (n_j).

**Lemma A.1 (cocycle).** For any two color automorphisms (g,h\in G) and any admissible histogram (n),
[
\varepsilon(hg,n)=\varepsilon(g,n)+\varepsilon(h,g n)
\pmod2.
]
*Proof.* A stable sort by (g) followed by a stable sort by (h) has the same relative order as the stable sort by (hg), since both maps are bijections of the six colors and every sort preserves within-color ordering. The sign of the composite sorting permutation is the product of signs. The induced edge-label sign is a group character by the twelve-edge/three-pair factorization, so it also satisfies the composition law. Taking the sum of these two parity identities proves the claim. □

Thus (G) acts on a *formal signed histogram* ((n,p)) by (g(n,p)=(gn,p+\varepsilon(g,n))). The adjective *formal* is essential: the 11-color histogram omits the full ordered past transcript, the remaining second-color observations, the corner state and the geometry of physical probe routing.

## C. Exact gauge obstruction and signed orbit count

Let (G_n) be the stabilizer of (n) under (G). A normalization gauge is **parity-unsafe** if (\varepsilon(h,n)=1) for some (h\in G_n). Independent finite verification gives 24 parity-unsafe representative orbits out of 52, collectively representing 426 of the 1,362 labeled histograms. The breakdown by stabilizer order is: thirteen unsafe orbits of stabilizer size 2, eight of size 4 and three of size 8.

For a gauge-safe orbit, the two parity labels stay in separate signed orbits. For an unsafe orbit, an element of its stabilizer interchanges them. Hence the number of orbits in the formal signed histogram space is
[
2(52-24)+24=80.
]
The independent size distribution is seven signed orbits of size 12, 36 of size 24 and 37 of size 48. A character-twisted Burnside audit provides the independent fixed-point receipt
[
\sum_{g,n:\,gn=n,\varepsilon(g,n)=0}1=1920,\qquad
\sum_{g,n:\,gn=n,\varepsilon(g,n)=1}1=576,
\quad 2\cdot1920/48=80.
]

An earlier calculation using the *label-only* character action (p\mapsto p+\operatorname{parity}(\alpha_g)), without position sorting, produced 94 orbits and ten unsafe ordinary representatives. That statement remains true for its different simplified model, but **does not identify the gauge hazards of the actual frozen controller**. The corrected 80-orbit analysis is the appropriate structural sanity check for the policy's combined sign transport.

## D. Consequences for the nineteen-frame upper bound

The existing 52-root certificate need not be discarded: its executable transport keeps a selected color map and the stable-sort order, and its leaf sign is corrected by the XOR of the two signs. The rigorous upper theorem must establish that the Lean interpreter uses the **same selected map, same sort, same inverse, same terminal sign**, for all ordered feasible first-eleven transcripts.

The next proof obligation is therefore not to replace 52 by 80 trees, nor to enumerate more initial cubes. It is to prove a **signed, observation-preserving bisimulation** between each original posterior and its deterministically selected representative posterior. Such a bisimulation must preserve query addresses, all feasible response colors, candidate set membership, and the terminal corner parity. The new cocycle identity makes the sign correction compositional; without the rest of that bisimulation it cannot complete the 19-frame theorem.

A robust negative-control experiment would deliberately discard the selected normalization map after computing a histogram representative and check that a feasible first-eleven transcript in one of the 24 unsafe classes produces a misinterpreted leaf sign. A positive control would retain the map and show that both valid normalization choices yield the same recovered physical initial arrangement after their respective corrections.

**Review boundary.** Neither the 80 signed orbits nor the 24 unsafe classes is a claim of a new optimal observation bound; they are mathematical diagnostics for the **proof of correctness of a purported optimal policy**. Standard group cohomological language explains the cocycle but does not replace the physical observation semantics or the certified adaptive lower bound.

**Reproducibility:** `scripts/cuberev-observation/audit_r029_hall_burnside_graph_quotient.py` computes all 48 color maps, all 1,362 feasible histograms, 326,880 generator-composition cocycle checks, 24 unsafe representatives, 426 affected histograms, the 80 corrected signed orbits and fixed-point sums. The structural 12-edge/three-pair sign character is separately kernel-checked in `formal/029/ColorGraphCharacter.lean`. The full cocycle and representative-policy semantics still require a single composed Lean theorem.

*Editorial location:* This appendix can follow the 52-orbit proof and precede the terminal parity decoder in the final T/U lineage, because it identifies the exact transition at which a color-count canonicalization must retain its normalization witness.

# AK2 — Hall's theorem identifies all possible eleven-color edge transcripts

**CUBE-REV 0.29 · 2026-11-21 · Status:** exact combinatorial proof, independent finite audit; not yet a dedicated Lean formalization. **Proof role:** replace an orientation brute-force search by a six-vertex, twelve-edge graph incidence theorem. The initial 18-frame lower bound and 19-frame upper-policy certificate are separate results.

## Graph and observation model

Let `V={U,D,R,L,F,B}`, with forbidden opposite pairs `{U,D}`, `{R,L}`, `{F,B}`. Construct `H=K_{2,2,2}`, the complete multipartite graph on these three 2-vertex blocks. Its edges are exactly the 12 distinct unordered color pairs of physical Rubik's edge cubies. For an initial cube, one facelet of each of eleven distinct edge positions is read; one edge position remains unread. As this is only the initial edge-prefix subproblem, its corner colors and legal physical routing are not used here.

A count vector `n:V→ℕ` with `Σ_v n(v)=11` is **realizable** if there exists a choice of eleven distinct edge cubies and one endpoint color from each that realizes exactly those multiplicities. It does not record the order of the eleven physical reads; retaining their order is a later transport obligation.

**Theorem AK2 (matching characterization).** Such a count vector is realizable if and only if, for every `S⊆V`,

```text
Σ_{v∈S} n(v) ≤ |{e∈E(H) : e∩S ≠ ∅}|.
```

**Necessity.** Each of the `Σ_{v∈S} n(v)` distinct observed edge positions that return a color in `S` must be occupied by a different edge cubie incident to `S`. There are only `|E(H) incident to S|` such edge types.

**Sufficiency.** Replace each color `v` by `n(v)` *distinguishable demand tokens*, and construct a bipartite graph between the 11 demand tokens and all 12 original edge types. A token of color `v` is adjacent exactly to edge types incident to `v`. For an arbitrary token subset `T`, let `S` be the set of colors occurring in `T`. Its size satisfies `|T|≤Σ_{v∈S}n(v)≤|N(T)|`, so Hall's marriage theorem yields a matching saturating all 11 tokens. The matching selects 11 different edge cubies, with one endpoint color on each. The twelfth edge type is the omitted one. The oriented first sticker of each selected piece can be chosen so it reports the token's requested color; the last, unread edge's orientation is then chosen to make the global edge-flip sum even. No extra parity restriction on the first 11 count vectors arises. QED.

## Closed-form Hall capacity from the multipartite graph

Let `s_i=|S∩P_i|`, where `P_i` are the three opposite-color pairs and `s_i∈{0,1,2}`. The complement contains `2-s_i` vertices from pair `i`. The induced graph on this complement has

```text
(2-s_1)(2-s_2)+(2-s_1)(2-s_3)+(2-s_2)(2-s_3)
```

edges. Therefore the right-hand Hall capacity equals

```text
12 - [(2-s_1)(2-s_2)+(2-s_1)(2-s_3)+(2-s_2)(2-s_3)].
```

This turns an eleven-edge orientation search into at most 64 elementary subset inequalities on a vector of six nonnegative integers. Only `C(11+6-1,6-1)=4368` integer count vectors can even occur, before the Hall test. The first-color support set is consequently finite without generating any of the `12!·2^{11}` ordered oriented assignments.

## Executable and negative controls

The independent standard-library audit `scripts/cuberev-observation/audit_r029_hall_burnside_graph_quotient.py` verifies Hall support against a separate dynamic program that deletes each possible edge and then propagates the two endpoint-color choices of the other eleven edges. The two implementations produce the *same set* of **1,362** vectors, not just the same cardinality. Mutation controls reject a graph missing an edge and a count vector whose total is not eleven. The same script continues with Burnside and induced edge-sign calculations, separately documented.

**Strict boundary:** Realizability of a first-color count vector does **not** show that an arbitrary physical cube with that vector is reconstructible within eight later paired frames; it only supplies the correct root support for the next decision-game proof. It also does not prove that arbitrary color relabelings are legal physical whole-cube rotations: the 48-element action is a representation symmetry of the *edge* game. Corner-to-edge parity must be explicitly transported.

## Primary-source reading and terminology

- [Cameron (1999), *Permutation Groups*, §§1.3, 1.10 and 1.17](https://drive.google.com/file/d/14WWOUzTUy7PVuFcr5cnX0O2Fsfxqif/view): group actions, wreath products and permutation parity.
- [Seress (2003), *Permutation Group Algorithms*, Ch. 4](https://drive.google.com/file/d/1kUj3ajt6Fq_O8S9omgyUEHnbTAazItne/view): stabilizer chains and strong generating sets, useful for larger symmetry groups but not needed to enumerate this 48-element group.
- [Bailey & Cameron (2011), *Base Size, Metric Dimension and Other Invariants of Groups and Graphs*](https://drive.google.com/file/d/1PSS1zaeX_CD6VVuxrP1H6AfrYXscktuV/view): distinction between group bases and graph resolving sets. An eleven-color prefix is a categorical sensor histogram, not automatically either of these parameters.
- [McKay & Piperno, *Practical Graph Isomorphism, II* (arXiv 1301.1493v1 preprint)](https://drive.google.com/file/d/1iQ38YgNK14g1lCazcHUS7Y6CvNujXbuf/view): canonical labeling and stabilizer-orbit quotienting, but their graph-isomorphism algorithm is not a proof of our feedback decision-tree bound.

**Editorial:** The Hall theorem itself is classical; the research contribution, if demonstrated novel, is its use as a concise characterization of the specific cube sensor model and its integration with adaptive group-equivariant policy certification. Do not label a standard matching theorem as newly discovered.

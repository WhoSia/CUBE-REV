# Exact Adaptive Color Identification of a Rubik's Cube — AR Working Manuscript
## Signed Posterior Bisimulation and Canonical-Transport Completeness
**CUBE-REV 0.29, manuscript AR v1, 21 November 2026. Independent additive chapter; all earlier T/U/V/W, AK–AM and AP drafts remain preserved.**

**Editorial / formal evidence status:** sections 1–4 are mathematical claims with a bounded formal hypothesis interface; their Lean sources have been submitted to the read-only build but must be checked against actual logs. Sections 5–7 are explicit **open** obligations, not disguised theorems. This is a draft for scientific review, not submission-ready copy.

### Abstract (AR supplement)

A principal difficulty in certifying an optimal adaptive color-probe policy is the possibility that state-relabeling symmetries preserve the counted colors of an observation prefix without preserving the exact interpretation of the remaining permutation parity. We describe a state-and-response-preserving notion of *signed posterior bisimulation* for a Rubik's Cube observation experiment in which each frame reads one edge and one corner sticker simultaneously. The construction retains three pieces of normalization data, all selected from a previously observed prefix: a six-color automorphism, a twelve-slot edge position permutation, and a parity-correction bit. For every fixed such witness, we establish an explicit inverse state map and an exact identity between the fibers of the original and normalized observation functions. Induction then carries this equality through every finite ordered sequence of paired queries and categorical replies, and a policy-transport theorem preserves the number and causal order of reads. A group-action calculation determines that twenty-four of the fifty-two Hall-feasible histogram orbits admit gauge changes with opposite combined sign correction. The construction furnishes a sound component of a formal nineteen-frame upper bound; proving the actual prefix selector, parity coupling and certified decision-tree interpreter remains necessary to close that bound.

### 1. Problem and role of the symmetry reduction

Let (\mathcal S) be the fixed-center, legally reachable initial configurations of the ordinary (3\times3\times3) Rubik's Cube. Let (E) and (C) denote its twenty-four edge and twenty-four corner sticker positions. A paired color query at frame (k) is an ordered pair (q_k=(e_k,c_k)\in E\times C). The observer chooses (q_k) on the basis of the earlier paired queries and answers, and receives
[
     r_k=(\operatorname{col}_{s}(e_k),\operatorname{col}_{s}(c_k))
     \in\{U,D,R,L,F,B\}^2.
]
The addresses are represented in the *initial coordinate frame*; a separate fixed-probe compiler realizes them using known intervening cube rotations. Neither a historical output nor a terminal reconstruction may depend on an answer not yet observed when its own query was selected.

The existing upper-policy construction first reads one color from each of eleven distinct edge positions. The first eleven answers, as an ordered color string, are then normalized by an opposite-preserving color automorphism (g\in G), where (G\cong(C_2)^3\rtimes S_3). After color relabeling, the eleven indices are stably sorted, yielding a twelve-slot permutation (\beta) that fixes the twelfth, initially unread edge. This leads to fifty-two representatives of feasible unordered color histograms. All continuation trees are stored in those representative coordinates.

The numerical reduction from 1,362 feasible histograms to 52 is mathematically justified by Hall's marriage theorem on (K_{2,2,2}) and Burnside's lemma. However, the representative histogram alone does *not* supply an unambiguous inverse identification map: 40 of the 52 histogram orbits have nontrivial stabilizers, and 24 have stabilizers that can change the combined edge-type/position-sort sign correction. Thus a proof that merely says “run the certified representative policy, then relabel the output back” is incomplete unless it retains the actual color and position maps and proves that the remaining observation functions intertwine.

### 2. Algebraic setting and explicit signed transport

A source cubie-and-corner state consists of an ordered family (e\colon\{0,\dots,11\}\to\{0,\dots,23\}) of oriented edge types and a full corner-color array (c\colon\{0,\dots,23\}\to\{0,\dots,5\}). The *signed extension* is (S_{\pm}=S\times\mathbb Z/2\mathbb Z). We stress that the sign coordinate is a **formal tag**: the physical sensor cannot read it freely.

A representative source state uses a relabeled oriented-edge array (e'\colon\{0,\dots,11\}\to\mathbb N), retaining (c), together with a formal sign bit. Fix a color graph automorphism (g), a bijection (\beta) of edge slots, and a correction bit (\varepsilon). Define
[
  T_{g,\beta,\varepsilon}((e,c),p)=
  ((g_*(e\circ\beta),c),\;p\oplus\varepsilon).
\tag{2.1}
]
Here (g_*) denotes the established action on *oriented* edge identities, not just unordered endpoint sets. The inverse is
[
  D_{g,\beta,\varepsilon}((e',c),p')=
  ((g_*^{-1}(e')\circ\beta^{-1},c),\;p'\oplus\varepsilon).
\tag{2.2}
]
The specified inverse color table is genuine for all forty-eight allowed maps and all twenty-four oriented edge identifiers. The slot order contains both its forward and inverse functions and proofs of their two compositions being identities.

**Proposition 2.1 (signed inverse).** For any eligible (g), invertible slot order (\beta), and (\varepsilon\in\mathbb Z/2),
[
 D_{g,\beta,\varepsilon}
     (T_{g,\beta,\varepsilon}(x))=x
     \qquad \text{for all tagged original states }x.
\tag{2.3}
]
*Proof.* Apply the inverse permutation on slots and the inverse color-table action, as in the previously verified nonsigned representation inverse. The corner array is unchanged. The sign tag undergoes two XOR operations by the *same* bit, and (p\oplus\varepsilon\oplus\varepsilon=p). Each component is thus unchanged. This proof does not assume a particular cube scramble or depend on a finite enumeration of physical cube states. □

An important subtlety is that (2.3) proves **injectivity** of (T) even for arbitrarily labeled arrays that are not legal Rubik states; it is not the legality-embedding theorem.

### 3. Exact paired response equivariance

Let (\mathcal Q) be the set of paired abstract addresses, represented by an edge slot/side pair together with a corner facelet address. The physical source observation (O\colon S_{\pm}\times\mathcal Q\to\{0,\ldots,5\}^2) ignores the parity tag. Define the original-coordinate query pullback (Q_\beta(q)) by applying (\beta) to the edge slot while keeping the edge side and corner facelet fixed. Define (R_g(r_e,r_c)=(g(r_e),r_c)), which relabels the **edge answer only**.

The representation observation (O'\) returns the indicated color from the relabeled edge array and the unchanged corner color. These concrete functions satisfy the following for **every** original tagged state and every pair address:
[
 O'(T_{g,\beta,\varepsilon}(x),q)
   =R_g\bigl(O(x,Q_\beta(q))\bigr).
\tag{3.1}
]

**Proposition 3.1 (covariant paired read).** Identity (3.1) holds for all eligible color automorphisms, invertible edge-slot orders, and fixed parity correction bits.

*Proof.* The edge component follows from the oriented-edge relabeling theorem, which preserves the colors on both sides of every oriented edge type under the inverse-bounded six-color map. The corner component is unchanged by construction. The parity coordinate is not present in the response and hence cannot create extra sensor information. □

Equation (3.1) should not be confused with the statement that (g) is a physical fixed-center cube rotation: the forty-eight color graph automorphisms include transformations not implemented by rigid rotations of the actual cube. The identity is instead a *semantic covariance of the abstract edge/corner state representation* with a precisely constructed original-coordinate query map. Its validity for the actual physical sensor follows only after applying the independently proved query routing compiler.

### 4. Posterior fibers and arbitrary ordered transcripts

For a belief predicate (B\colon S_{\pm}\to\{\mathsf{false},\mathsf{true}\}), let
[
 B\restriction_{q,r}
    =\{x\in B:\ R_g(O(x,Q_\beta(q)))=r\}.
\tag{4.1}
]
Define its image under (T) by (T(B)=\{T(x):x\in B\}). Let the normalized posterior operation be (B'\restriction'_{q,r}
=\{y\in B':O'(y,q)=r\}).

**Theorem 4.1 (one-step exact fiber covariance).** If (3.1) holds, then
[
      T(B\restriction_{q,r})
          = T(B)\restriction'_{q,r}
          \qquad\text{for every }q,r,B.
\tag{4.2}
]
*Proof.* An element (T(x)) belongs to the left-hand set precisely when (x\in B) and the recoded source response at (q) equals (r). By (3.1) that second predicate is equivalent to (O'(T(x),q)=r), which is exactly membership in the right-hand set. □

This is a stronger claim than the equality of belief cardinalities or the correspondence of candidate-count histograms. It compares the *complete possible states* after the same labeled response.

For an **ordered** history (h=((q_1,r_1),\ldots,(q_m,r_m))), define the posterior recursively by (B_{\varnothing}=B) and (B_{h\mathbin\| (q,r)}=B_h\restriction_{q,r}).

**Theorem 4.2 (all-history signed posterior covariance).** For every finite sequence of paired addresses and responses,
[
       T(B_h)=[T(B)]'_h.
\tag{4.3}
]
*Proof.* Induct on the length of (h). The empty-history case is the definition of image. At a successor history, the induction hypothesis identifies the pre-query belief images, and Theorem 4.1 identifies their respective fibers under the current query and answer. Since the statement quantifies over **all** query/reply sequences, the proof applies in particular to the sequence generated by an arbitrary legal adaptive controller, without assuming that its addresses were selected nonadaptively. □

The theorem does *not* say that a single normalization (T) chosen from the initial eleven colors can correctly predict those colors: (T) is chosen *after* that prefix. Its application is the **continuation game** conditional on a realized eleven-color prefix, with (g,\beta,\varepsilon) fixed before further reads.

**Corollary 4.3 (ambiguity preservation).** If the original belief contains two distinct tagged states, its image under (T) contains two distinct tagged states.

*Proof.* Equation (2.3) implies that (T) is injective. Distinct inputs thus cannot map to the same representative state. □

### 5. Transfer of adaptive policy and exact budget

A policy is a rooted decision tree in which a nonterminal vertex chooses an address (q) and has one outgoing continuation for each categorical pair reply (r\in\{0,\ldots,5\}^2). A terminal vertex outputs a candidate initial tagged state. The proof object `Fits n tree` bounds **all** branches, including those with replies not feasible under a chosen posterior.

**Theorem 5.1 (conditional signed physical policy transport).** Fix ((g,\beta,\varepsilon)) and an admissible set (A\subseteq S_{\pm}). Suppose a representative policy (P') has `Fits k P'` and
[
     P'(O',T(x))=T(x)\qquad(x\in A),
\tag{5.1}
]
where (P'(O',y)) denotes running (P') with the representative observation function on state (y). Then there exists an original-coordinate policy (P) with `Fits k P` whose result on any (x\in A) is exactly (x) under the original simultaneous physical edge/corner color observation function.

*Proof.* At each decision-tree node with representative query (q), (P) chooses the original query (Q_\beta(q)); when its physical paired reply (r) arrives, (P) follows the representative branch indexed by (R_g(r)). This selects the physical query before seeing its reply. At a representative terminal output (y), return (D_{g,\beta,\varepsilon}(y)). This tree is the `Policy.adapt` construction; by structural induction on `Fits k`, its budget is unchanged. By (3.1) a run of the adapted tree follows exactly the same representative path as (P') run on (T(x)); by (5.1) the representative output is (T(x)), and by (2.3) the final original output is (D(T(x))=x). □

**What this establishes.** Conditional on a correctly normalized representative policy, a parity correction chosen from *past* information, and legitimate original-query routing, no extra observation is needed for inverse transport. In the present code this is the exact scope of `signed_original_policy_of_certified_representative`, not a statement that the hypotheses (5.1) have already been discharged for the fifty-two frozen trees.

### 6. Stable-sort sign cocycle and the legality constraint

The signed extension of the preceding theorems carries an arbitrary fixed correction bit. A physical cube, however, has no independently settable sign tag: legal edge and corner cubie permutations have the same sign. The frozen normalizer also performs stable sorting of the eleven observed first-color positions, which changes the permutation sign even when the color relabeling (g) itself is sign-even on edge types.

Let (\chi(g)) denote the sign of the induced permutation of the twelve edge type labels, proved equal to the sign of the three opposite-color pairs. Let (\beta_{g,n}) be the stable-sort permutation for a histogram (n) in the chosen frozen color rank order. Then
[
\varepsilon(g,n)=\chi(g)\oplus
\sum_{0\le i<j<6}n_i n_j
[\operatorname{rank}(g(c_i))>\operatorname{rank}(g(c_j))]
\pmod2.
\tag{6.1}
]
Its compositional law is
[
\varepsilon(hg,n)=\varepsilon(g,n)\oplus\varepsilon(h,gn).
\tag{6.2}
]

**Proposition 6.1 (mathematical).** Equation (6.2) holds by the composition of stable sorting and the group-character property of (\chi). The finite executable audit verifies 326,880 generator cases against the exact six-color rank convention and the full (1,362\)-histogram support.

**Formalization gate (OPEN).** The general derivation (6.1)–(6.2) is written mathematically and independently audited in Python, but no unconditional Lean lemma yet proves that a total normalization selector from each *ordered* eleven-color history computes precisely that correction bit. The current signed policy transport assumes it is supplied.

**Proposition 6.2 (computational, source-specific).** For the combined correction in (6.1), twenty-four of the fifty-two unsigned histogram representative orbits contain a parity-odd stabilizer element (426 of the 1,362 concrete histograms), and the formal signed-histogram action has eighty rather than fifty-two orbits. This does not imply the frozen fifty-two-root continuation strategy fails, since the frozen interpreter retains its specific normalization witness. It identifies a required regression class for any later Lean reimplementation.

### 7. Closing the eighteen-versus-nineteen theorem

The principal result for a publication-level treatment remains the impossibility of universal recovery from at most eighteen paired-color observations, **even if all corners are supplied to the observer in advance**. The physical lower bound relies on a finite adversarial response certificate with verified witness lifts; it must be reported with its `native_decide` trust dependency rather than called an unqualified primitive-kernel-only calculation.

The proposed upper theorem requires that every legal original state be recovered by some *unconditional* nineteen-frame adaptive policy. Four interfaces remain to connect:
1. Every actual ordered eleven-edge first-color transcript determines a valid color map, invertible position order and the correct sign correction using **only those first-eleven observations**.
2. Each representative eight-read decision tree is interpreted as a total `Policy`, with all possible answer branches checked and a genuine `Fits 8` proof, and outputs the exact representative *state* rather than merely a candidate-count receipt.
3. The nineteen-frame physical corner schedule yields the requisite original corner permutation sign **by the end of the nineteenth frame**; it never grants an unobserved parity oracle at an earlier decision node.
4. The full representative upper policy is compiled into a fixed physically feasible paired-probe route, recovering the initial (not final rotated) cube.

These are independent proof obligations. None is discharged merely by Theorems 4.1–5.1, which prove a structural transport result under explicitly enumerated hypotheses.

### 8. Reproducibility and methods bibliography

The formal sources and explicit axiom reports are `SignedRepresentativePolicy.lean`, `SignedPairedPosterior.lean`, `GraphPosteriorCovariance.lean`, `RepresentativeRoundTrip.lean` and `PairedPolicyTransport.lean`. The primary stored twenty-four-odd-stabilizer and eighty-signed-orbit audits, together with an actual legal-edge negative control for forgetting the chosen normalization map, reside in `scripts/cuberev-observation/`. The bounded cubic-geometry compiler, the finite eighteen-frame lower DAG and the fifty-two-tree nineteen-frame upper certificate remain separate.

Methods references to be harmonized for a finished paper: Cameron (1999), *Permutation Groups*; Seress (2003), *Permutation Group Algorithms*; Diestel (2017), *Graph Theory*; Schrijver (2003), *Combinatorial Optimization*; Leon (1991), *Permutation Group Algorithms Based on Partitions I*; McKay and Piperno (2013 preprint), *Practical Graph Isomorphism, II*; Jefferson et al. (2021), *Permutation Group Algorithms Based on Directed Graphs*. None of these sources is presented as already having proved the specific fixed-center paired Rubik sensor threshold. The precise missing-primary and missing-edition list is kept in a *separate, missing-only source register*.

**End of AR working chapter. The conclusion of the main one-paper manuscript must not claim the upper-bound proof is closed until the frozen representative tree semantics and the real parity-coupled output are formalized.**

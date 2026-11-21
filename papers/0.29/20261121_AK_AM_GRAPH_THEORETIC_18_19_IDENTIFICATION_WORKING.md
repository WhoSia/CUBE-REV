# Exact Adaptive Color Identification of a Rubik's Cube
## An Eighteen-Frame Obstruction, a Nineteen-Frame Certificate, and a Graph-Theoretic Policy Quotient

**CUBE-REV 0.29 · Manuscript AK–AM structural working draft · 21 November 2026**
**Status: NOT SUBMISSION-READY.** This draft records mathematical arguments and exact proof obligations while preserving the separate T/U/V/W manuscript lineage. It does **not** claim that the final universal nineteen-frame reconstruction theorem has been kernel-checked. All citation targets and editions must be verified in the eventual author's bibliographic pass.

### Abstract — provisional

We investigate exact identification of an unknown, legally reachable, fixed-center (3\times3\times3) Rubik's Cube from categorical observations. At each observation frame, a controller selects one edge sticker and one corner sticker and receives their six-valued colors simultaneously; known intervening cube turns implement the probes and are not charged to the observation budget. The goal is to recover the *initial* configuration, not merely a configuration after the turns. A certified adaptive lower-bound construction rules out universal identification within eighteen frames, even if the entire corner arrangement is disclosed in advance. An independently checked finite construction attains nineteen frames in executable models, using an eleven-frame one-sided edge prefix, at most eight adaptive follow-up reads, and a fourteen-color corner decoder. We develop a graph-theoretic explanation of the construction's symmetry reduction: the twelve edge color types are the edges of (K_{2,2,2}); Hall's theorem characterizes the feasible eleven-color prefix histograms; and Burnside's lemma reduces 1,362 feasible histograms to 52 orbits under a 48-element wreath-product action. A sign-character identity compresses the terminal parity correction to the parity of a permutation on three opposite-color pairs. The complete Lean formalization of the upper policy, notably the semantic interpretation of all representative decision trees and their sign-corrected output, remains an explicit open proof obligation.

**Keywords:** adaptive distinguishing sequences; Rubik's Cube; observational identification; permutation groups; graph automorphisms; Hall marriage theorem; Burnside orbit counting; formal verification; posterior partitions.

### 1. Introduction

It is possible to solve a Rubik's Cube without identifying its original state, and it is possible to identify a state using a sensor that reads many colors at once. Neither observation task is our problem. We study the minimum number of rounds needed by a controller that may query only two individual colors in each round: the color of one edge sticker and that of one corner sticker. The two sticker addresses must be chosen before the answers in their own round are known. All readouts refer to the unknown initial arrangement through the known intervening move history. The observations are noiseless and the centers are fixed.

The first mathematical difficulty is **lower bounding arbitrary adaptive decision trees**, not simply counting the total number of reachable cubes. Information-theoretic entropy alone is too coarse because color answers are not equiprobable, and because the query positions and the legal edge permutations/orientations are correlated. The second difficulty is **certifying an upper policy** without confusing representative color strings with physical original-coordinate observations, or confusing a color-label symmetry with a spatial cube rotation.

Our objective is the exact adaptive threshold (h_{\mathrm{adaptive}}=19), with the eighteen-frame obstruction established even after revealing all corners. The corresponding nonadaptive paired-color optimum is 21 frames. This paper separates the proof of the obstruction from the stronger correctness obligation of the upper-policy certificate. As of this draft, the lower-bound Lean sources and executable upper-policy computations exist, but a single unconditional Lean term implementing and proving the full nineteen-frame policy has not yet been constructed.

### 2. Formal observation model and legal states

Let (\mathcal S) denote legal initial states of the fixed-center cube, identified by the colors on the 48 moving stickers. Define (E) to be its 24 edge sticker addresses and (C) its 24 corner sticker addresses. For (s\in\mathcal S) and (q=(e,c)\in E\times C), the simultaneous categorical observation is
[
O(s,q)=(O_E(s,e),O_C(s,c))\in V\times V,
\quad V=\{U,D,R,L,F,B\}.
]
The decision tree's next query is a function only of previous query-and-reply pairs. Its output is the initial state (s). A budget (n) policy has no root-to-leaf path with more than (n) queries. Implementing a query with a fixed pair of physical probes and known turns requires a separate routing theorem: an abstract original-coordinate ((e,c)) is not a freely chosen color oracle.

The legality constraints include exactly one copy of each of the twelve edge types, exactly one copy of each of the eight corner types, even total edge orientation, zero total corner twist modulo three, and equal edge and corner permutation signs. Those constraints may not be dropped when transporting a representative policy back to an initial physical cube.

### 3. The eighteen-frame obstruction — proof hierarchy

**Claim L (certified lower-bound target).** For every adaptive policy of at most eighteen simultaneous edge/corner reads there exist two distinct reachable initial cubes that give the policy an indistinguishable transcript. The claim continues to hold in the more generous model in which the complete corner arrangement is announced before any query.

The proof does not follow by simply counting six-valued answers. The construction first fixes/discloses a corner arrangement, so that the corner component of each paired response is state-independent. It then provides an edge-only adversarial residual game with an ambiguity witness surviving every one-step query until budget exhaustion. A state-specific physical observation and embedding lemma transports the adversary from oriented edge words to actual legal cube states and finally to the controller that may also read the announced corners.

**Verification separation.** The adversarial strategy's abstract correctness, the finite DAG receipt, the physical edge-coordinate realization, and compilation in Lean are distinct obligations. `PhysicalEighteen.lean` and its dependencies implement the lower-bound route, and their axiom reports explicitly disclose uses of `native_decide` for finite certificate data. No statement in the present paper may turn those dependencies into an unsupported claim that every computation was reduced to primitive kernel normalization.

### 4. Initial edge-color histograms as graph matching

Define three opposite-color pairs
[
P_1=\{U,D\},\qquad P_2=\{R,L\},\qquad P_3=\{F,B\}.
]
Each unordered edge cubie consists of two nonopposite colors, so the graph of edge *types* is
[
H=K_{2,2,2},\qquad V(H)=P_1\cup P_2\cup P_3,\qquad |E(H)|=12.
]
The upper construction begins by reading one sticker of each of eleven distinct edge positions. Its first eleven replies form an ordered string (a=(a_1,\ldots,a_{11})\in V^{11}). Let (n_v=|\{i:a_i=v\}|). The unordered histogram (n\in\mathbb Z_{\ge0}^V), with total weight 11, loses the order but retains the combinatorial support constraints.

**Theorem 4.1 (Hall characterization).** There is a legal oriented edge arrangement whose first eleven one-sided color replies have histogram (n) if and only if
[
\sum_{v\in S}n_v\le
\left|\{e\in E(H):e\cap S\ne\emptyset\}\right|
\quad\text{for every }S\subseteq V(H),
\qquad \sum_{v\in V(H)}n_v=11.
]

*Proof.* If such an arrangement exists, each observation of a color (v\in S) must come from a distinct edge cubie incident with (S), proving necessity. For sufficiency, take (n_v) individually distinguishable *demand tokens* of color (v). Construct a bipartite graph on the eleven tokens and the twelve edge types, connecting a token of color (v) to the edge types incident with (v). Given any token subset (T), let (S) be the set of colors represented in (T). The assumed inequalities yield (|T|\le\sum_{v\in S}n_v\le|N(T)|). Hall's marriage theorem therefore supplies a matching saturating the eleven demand tokens. Assign the matched edge types to the first eleven positions and leave the remaining edge in the twelfth position. Choose each of the eleven edge orientations so that its observed side is the token color. Choose the last edge's (unobserved) orientation to enforce an even total edge-flip parity. Given the resulting edge permutation sign, choose a corner permutation of the same sign and twists summing to zero, obtaining a legal whole-cube initial arrangement. This also establishes sufficiency under the full cube-legality coupling. □

For computational auditing, an (S\subseteq V) contains (s_i\in\{0,1,2\}) vertices of (P_i), so the number of incident edges can be computed without enumerating any cube states:
[
12-\bigl[(2-s_1)(2-s_2)+(2-s_1)(2-s_3)+(2-s_2)(2-s_3)\bigr].
]
There are only (\binom{16}{5}=4,368) nonnegative histograms of total weight 11 and 64 subsets (S). The exact support set has size 1,362. An independent omitted-edge dynamic program produces the same *set* of 1,362 vectors and functions as a negative control against an incorrectly implemented Hall test.

**Limitation.** This theorem certifies only which initial *histograms* are physically possible, not the existence or optimality of any eight-read continuation, and not the eligibility of a dynamic policy to act on histogram counts without preserving the ordered transcript.

### 5. The fifty-two histogram orbits and the stabilizer hazard

Every automorphism of (H=K_{2,2,2}) permutes the three opposite-color pairs and may swap their two vertices independently. Consequently
[
G=\operatorname{Aut}(H)\cong(C_2)^3\rtimes S_3,\quad |G|=2^3\cdot6=48.
]
The Hall inequalities are invariant under (G). Let (X) be the 1,362 feasible histograms. By Burnside's lemma,
[
|X/G|=\frac1{48}\sum_{g\in G}|\operatorname{Fix}_X(g)|.
]
The 48 elements split into ten signed-cycle types on three 2-point blocks. Exact finite fixed-point computation gives the following class-size/fixed-point pairs, with signed cycle lengths given in parentheses:
[
\begin{array}{c|r|r}
\text{type}&\#g&\#\operatorname{Fix}_X(g)\\\hline
1^+1^+1^+&1&1362\\
1^+1^+1^-&3&252\\
1^+1^-1^-&3&46\\
1^+2^+&6&34\\
1^+2^-&6&6\\
1^-1^-1^-&1&0\\
1^-2^+&6&0\\
1^-2^-&6&0\\
3^+&8&0\\
3^-&8&0
\end{array}
]
The sum of fixed points, counted once per group element, is 2,496, so exactly
[
|X/G|=2,496/48=52.
]
The orbit-size distribution is (3\times6,10\times12,27\times24,12\times48), accounting for 1,362 vectors.

**Proposition 5.1 (normalization gauge warning).** Only twelve of the fifty-two representative histograms have trivial stabilizer. The other forty have more than one color automorphism mapping the same original histogram to the chosen representative. A representative histogram alone is therefore insufficient to reconstruct the chosen color transport or its induced parity correction.

*Proof.* By orbit–stabilizer, the nontrivial stabilizer orders are 8, 4, and 2, with 3, 10 and 27 representative orbits respectively. Their total is (3+10+27=40). Each contributes multiple automorphisms selecting the same orbit representative. □

In the frozen executable policy, a deterministic normalization selects a *particular* (g\in G), an ordering of first-color positions, and their inverses. Correctness therefore must be established with the retained gauge data. An alternative is to prove equivariance under the representative's entire stabilizer, including its effect on all adaptive query addresses and the final parity label. We do **not** assume that unproved alternative.

### 6. Edge permutation sign factors through the opposite-pair action

Let (\alpha_g\in S_{12}) denote the permutation that (g\in G) induces on the twelve unordered edge types. Let (\tau_g\in S_3) be the permutation induced on the three opposite-color pairs.

**Theorem 6.1 (sign factorization).**
[
\operatorname{sgn}(\alpha_g)=\operatorname{sgn}(\tau_g)
\qquad\text{for all }g\in G.
]

*Proof.* Since both sides are group characters into (\{\pm1\}), it suffices to verify generators. Swapping the two colors inside any one opposite-color pair exchanges the four edges incident with one swapped color with the corresponding four incident with the other color, inducing four disjoint transpositions on the twelve edge types. Both signs are +1. Swapping two opposite-color pairs, with a fixed alignment of their two internal positions, induces one transposition on the four edges joining those pairs, together with four independent transpositions exchanging their edges to the third pair. Thus the induced edge action has five transpositions, with sign -1, matching the sign of the transposition on the three pair blocks. Three internal swaps and two adjacent pair transpositions generate (G), proving the result. □

The finite formal source `ColorGraphCharacter.lean` separately evaluates all 48 color symmetries using `decide +kernel`; it also verifies that the specified five generators reach the entire group within six Cayley steps. This small finite check is *not* the same thing as an unrestricted 12! sign computation.

Let (\pi\in S_{12}) be the original edge-piece permutation (piece at a position), and let (\beta\in S_{12}) take a representative slot to the corresponding original slot, fixing the unread twelfth slot. The representative edge-piece permutation is
[
\pi_{\mathrm{rep}}=\alpha_g\circ\pi\circ\beta.
]
Therefore
[
\operatorname{parity}(\pi_{\mathrm{rep}})
=
\operatorname{parity}(\pi)+
\operatorname{parity}(\beta)+
\operatorname{parity}(\tau_g)
\pmod2.
]

If the first eleven colors are stably sorted after relabeling by (g), the parity of (\beta) is the inversion parity of the eleven observed ranks,
[
\operatorname{parity}(\beta)\equiv
\sum_{1\le i<j\le11}
[\operatorname{rank}(g(a_i))>
\operatorname{rank}(g(a_j))]\pmod2.
]
Equal colors retain their original relative order and do not contribute. The correction therefore depends only on *already observed* colors and on the chosen (g), not on future or hidden edge replies.

### 7. From the graph quotient to a causal adaptive policy

The group orbit reduction of Section 5 compresses initial histograms, but it does not by itself certify the policy trees. Let (B\subseteq\mathcal S) be the posterior belief after an actual query/reply history. For a query (q) and reply (r), define (B_{q,r}=\{s\in B:O(s,q)=r\}). A group action on states, queries, and replies is a *sound game symmetry* only if
[
g(B_{q,r})=(gB)_{gq,gr}
\]
for every feasible state, query, and reply, and if its terminal winning condition is transported with the corrected edge/corner permutation sign.

Inductively, any such equivariant correspondence preserves the minimax number of further reads: at a terminal node the success predicate is equivalent; at a nonterminal node the query-choice minimization and worst-reply maximization correspond bijectively. It follows that the *signed, colored posterior game* may be quotiented by its actual stabilizer. This is stronger than uncolored graph isomorphism and stronger than comparing candidate counts. Each action in the decision game must be selected before its corresponding reply is returned.

This posterior covariance and the twenty-first-century techniques of graph partition refinement suggest a next-generation proof kernel: certify an alternating, response-labeled bisimulation on an explicit small quotient instead of rechecking unrelated tree nodes one by one. It remains a proposed proof strategy, not a theorem supplied merely by the cited graph-isomorphism literature.

### 8. Nineteen-frame executable construction and exact remaining proof gates

The frozen strategy observes one sticker of each of eleven distinct edge positions in its first eleven paired frames and follows a continuation selected from the corresponding representative histogram, retained color map, and stable sort. The representative continuations take at most eight further paired frames. The actual corner schedule reveals two cyclically ordered colors at each of seven corner positions, leaving corner position five unread. Exact corner color reconstruction uses identification of the seven observed oriented pieces, the remaining unused piece, and the corner twist-sum constraint. The last required corner color is not obtained until the nineteenth frame.

The frozen upper-policy certificate contains 52 representative roots, 144,736 candidate assignments, and 141,097 policy nodes in the existing receipt. Every leaf has at most one edge assignment in each parity class. At a terminal leaf with two opposite-sign edge candidates, the physical corner permutation sign selects the admissible edge candidate after the correction from Theorem 6.1 and the stable-sort inversion parity.

**Open Lean obligations as of this draft:**
1. Construct a total, deterministic normalization on every ordered feasible eleven-color prefix, retaining the actual chosen (g), (\beta), and inverse maps.
2. Formalize the parity composition formula for general twelve-piece permutations (or reduce it by justified generator transport), and prove it agrees with the frozen implementation's `sign^correction` convention.
3. Reify the 52 frozen representative decision trees as Lean `Policy` values and prove that all feasible response branches and terminal candidates are correct under `NineteenReadData.check` semantics.
4. Prove that the corner-sign information used to choose a terminal candidate is available at the correct frame, with no same-frame look-ahead.
5. Combine the actual initial eleven reads, the eight-read continuation, the all-reachable 14-color corner decoder and the known-turn physical probe compiler into an unconditional policy with `Fits 19` and exact recovery of *every* reachable initial cube.

The resulting implication from 18-frame impossibility to an optimal 19-frame physical policy is valid only once all five obligations are discharged. Existing Python audits establish strong computational evidence for these parts; the present document must not preempt the formal verdict.

### 9. Relation to prior literature and novelty cautions

Theorem 4.1 applies the classical marriage theorem, which is explained in Diestel (2017), *Graph Theory*, §2.1, and Schrijver (2003), *Combinatorial Optimization*, §22.1. Section 5 uses standard group actions, wreath products and Burnside's lemma (Cameron 1999, *Permutation Groups*, §1). The explicit stabilizer caution is aligned with the orbit-based canonical labeling of McKay and Piperno (*Practical Graph Isomorphism, II*, cited from the actual owned arXiv preprint), Leon (1991) partition backtracking, and Jefferson et al. (2021) directed-graph permutation group methods. Seress (2003), *Permutation Group Algorithms*, supplies scalable stabilizer-chain algorithms; enumerating all 48 elements of this small group is cheaper than implementing a generic Schreier–Sims engine.

Sokolovskii (1971), Vasilevskii (1973), Lee and Yannakakis (1994), and Hierons and collaborators address related distinguishing or diagnostic experiments in finite-state machines; the relevant alphabets, reset rules and tasks differ and cannot be silently identified with our fixed-center physical cube sensor. Bailey and Cameron (2011) distinguish group bases from graph metric dimension; our paired color sensor with feedback is neither ordinary graph distance nor a permanent original-cubie tag. Kociemba's two-phase solving algorithm and Korf's pattern database methods optimize *solving cost*, a different problem. All earlier works should be credited without claiming that matching theory, Burnside counting or permutation characters were invented in CUBE-REV.

The potential contribution of this paper is the exact **task-specific observation bound** and a transparent certified policy, together with mathematical reduction of its finite computational witnesses. Strong novelty claims must be checked against both modern puzzle sensing and finite-machine adaptive experiment design before submission.

### 10. Reproducibility and uncertainty ledger

- Executable independent Hall–Burnside audit: `scripts/cuberev-observation/audit_r029_hall_burnside_graph_quotient.py`, including a second deleted-edge dynamic program and mutation controls.
- Formal small symmetry character: `formal/029/ColorGraphCharacter.lean`, kernel evaluated by `decide +kernel`; `#print axioms` reports standard Lean logical axioms, not `native_decide`.
- Existing 18-frame lower bound: `formal/029/PhysicalEighteen.lean`, separate finite residual DAG certificate `EIGHTEEN_QUERY_DAG.json`, native-decision trust disclosure.
- Existing frozen 19 upper decision-tree certificate: `formal/029/upper-policy-certificate.json`, checkable with `NineteenReadData.lean` and the standalone Python checker; whole-policy Lean semantics not yet closed.
- Original working manuscripts and historic 0.28 and 0.29 drafts are retained. This manuscript version is an **independent working structural appendix/draft**, not a replacement or submission candidate.

### Bibliography — source-identity placeholders pending final author verification

Bailey, R. F., and Cameron, P. J. (2011). Base size, metric dimension and other invariants of groups and graphs. *Bulletin of the London Mathematical Society* 43, 209–242. DOI: 10.1112/blms/bdq096.

Cameron, P. J. (1999). *Permutation Groups*. Cambridge University Press.

Chekuri, C. (2022). *Combinatorial Optimization*, lecture notes (CS 586/IE 519).

Diestel, R. (2017). *Graph Theory*, 5th edition. Springer.

Hopcroft, J. (1971). *An n log n Algorithm for Minimizing States in a Finite Automaton*. Stanford Technical Report STAN-CS-71-190.

Jefferson, C., Pfeiffer, M., Wilson, W. A., and Waldecker, R. (2021). Permutation group algorithms based on directed graphs. *Journal of Algebra* 585, 723–758.

Leon, J. S. (1991). Permutation group algorithms based on partitions, I: Theory and algorithms. *Journal of Symbolic Computation* 12, 533–583.

McKay, B. D., and Piperno, A. (2013 arXiv v1 preprint; verify subsequent journal edition). *Practical Graph Isomorphism, II*, arXiv:1301.1493.

Schrijver, A. (2003). *Combinatorial Optimization: Polyhedra and Efficiency*. Springer.

Seress, Á. (2003). *Permutation Group Algorithms*. Cambridge University Press.

Sims, C. C. (1971). Computation with permutation groups. *Proceedings of SYMSAC 1971*, 23–28.

**Citation-custody note:** These references were checked against actually accessible Drive documents during the research session, but edition-specific publisher metadata and exact manuscript version alignment remain part of editorial closure. No copyrighted text is reproduced beyond minimal titles and standard notation.

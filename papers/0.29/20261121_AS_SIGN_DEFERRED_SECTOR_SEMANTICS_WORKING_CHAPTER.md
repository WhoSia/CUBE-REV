# Exact Adaptive Identification of a Fixed-Center Rubik’s Cube
## AS — A Sign-Deferred Semantic Interpreter for Frozen Finite Sectors
**Working manuscript AS1 (21 November 2026), additive to AR versions; not submission-ready.**

### 12. From a counted leaf to a reproducible decoded initial state

The previously validated certificate for an eight-read adaptive continuation has a simple compressed leaf semantics. It partitions the candidate oriented edge arrangements so that each leaf contains either one candidate or precisely two candidates of *opposite* permutation parity. Hence a leaf is not necessarily a singleton in the ordinary state-space sense. It becomes a uniquely decodable original edge arrangement **only when the legal corner permutation sign has been determined from physical corner observations**.

We formalize this distinction with two maps. Let (S) be the finite set of oriented twelve-edge candidate words compatible with a normalized first-eleven-color prefix, let (\sigma:S\to\{0,1\}) be the edge cubie permutation sign, and let (B\subseteq S) be the exact posterior sector at some certificate node. Define the property
[
 \operatorname{SignUnique}(B)
 \iff \forall x,y\in B,\ \sigma(x)=\sigma(y)\Rightarrow x=y.
\tag{12.1}
]
This property is weaker than ordinary singleton identification but stronger than an unstructured candidate-count receipt. Its key utility is that the first matching candidate of the requested sign is the actual candidate for all elements of (B).

**Lemma 12.1 (unique signed selection).** Define (d_B(p)\) by scanning the finite candidate list (B) for its first candidate whose sign equals (p\); if none exists, let (d_B(p)=\bot). Under (12.1),
[
 \forall x\in B,\quad d_B(\sigma(x))=x.
\tag{12.2}
]
Furthermore, if (d_B(p)=x\), then (x\in B\) and (\sigma(x)=p).

*Proof.* Proceed by induction on the finite candidate list. At a nonempty head (h), if its sign equals the target sign, (12.1) forces (h=x). Otherwise the target candidate lies in the tail, and the induction hypothesis applies because sign uniqueness passes to sublists. The reverse membership statement follows from the same structural recursion: the selector can only return an element it examines, and only after its sign agrees with (p). □

This precise lemma, formalized as `first_candidate_is_correct_of_sign_unique` and `first_candidate_witness_belongs`, makes the frozen leaf condition useful for the eventual universal reconstruction theorem without pretending the terminal parity is independently observable.

### 13. Complete finite response fibers rather than node-count reachability

A certificate node is not described adequately by its index alone: it is reached with a particular posterior (B), which can depend on the entire ordered sequence of previous observations. For a sticker address (q) and categorical reply (r), define
[
 B_{q,r} = \{x\in B:O(x,q)=r\}.
\tag{13.1}
]
The finite filter implementation is `finiteReplyFiber observe belief q r`, and its membership theorem states the exact equality in (13.1). No histogram aggregation or implicit permutation of the candidate order occurs at this step.

The frozen instruction language is a typed graph with three kinds of nodes. A *read* node specifies a sensor address and one destination for every possible reply. A *repeat* node consumes a real frame and follows a single destination, discarding its response. A *leaf* terminates the edge continuation. A missing array index, illegal address, malformed node or out-of-budget read cannot be treated as a successfully identified cube.

For a graph (G), remaining read budget (k), node (v), and candidate list (B), define a recursively compiled policy (P_{G,k,v,B}\) whose terminal output is **a function**
[
 D_{G,k,v,B}: \{0,1\}\to S\cup\{\bot\}.
\tag{13.2}
]
At a leaf, (13.2) is simply (d_B\) from Lemma 12.1. At a read node with address (q\), the actual reply (r) selects a recursive controller (P_{G,k-1,w(r),B_{q,r}}\). At a repeat node, the policy makes an actual observation (one more frame) but continues with the same posterior (B\), so no additional information is granted for free. Missing or malformed paths produce (ot) rather than a candidate. Each recursive call strictly decreases (k); the entire policy is therefore well-founded even for malicious cyclic instruction arrays.

**Lemma 13.1 (unconditional budget safety).** For every typed graph (G), state observation channel (O), candidate list (B), root node (v) and budget (k), the compiled policy has a derivation of `Fits k` covering *all* categorical reply branches. No validity premise is needed, because invalid branches fail closed.

This is a separate theorem from correctness. A controller that returns (ot) immediately may trivially meet any observation budget; the point of Lemma 13.1 is to rule out hidden extra reads, not to show useful identification.

### 14. A sound semantic validity specification

Define (\mathrm{Valid}(G,k,v,B)\) recursively by the following conditions:
- at a leaf, (operatorname{SignUnique}(B)) holds;
- at a read node (q), every *feasible* reply (r), i.e. (B_{q,r}\ne\varnothing), has a destination (w(r)\) for which (\mathrm{Valid}(G,k-1,w(r),B_{q,r})\) holds;
- at a repeat node, (\mathrm{Valid}(G,k-1,w,B)\) holds for its sole destination, without consulting the unused reply;
- no nonterminal node is valid at zero remaining budget and no missing node is valid.

The Lean predicate `SemanticallyValidSector` expresses precisely this recursive semantic specification, using an explicit existence witness in the belief to avoid any ambiguity between impossible and feasible replies. The policy `compileSectorDecoder` carries a full `Fits` proof at construction.

**Theorem 14.1 (signed sector soundness).** For every finite typed certificate graph (G\), every initial sector (B\), each state (s\in B\), and any budget (k\), if (\mathrm{Valid}(G,k,v,B)\), then running its compiled policy on the actual categorical observations of (s\) yields a terminal decoder (D\) satisfying
[
     D(\sigma(s))=s.
\tag{14.1}
]
*Proof.* Induct on (k). In a leaf case, apply Lemma 12.1. In a read case, let (r=O(s,q)\), so (s\in B_{q,r}\). The validity premise supplies the certified child for that *actual* reply, and the induction hypothesis gives (14.1) for its smaller budget. In a repeat case, the read consumes one frame but does not change (B), so the induction hypothesis applies to the unique child. Missing nodes, malformed instructions and exhausted budgets are excluded by the corresponding validity constructor. □

The proof treats an adversarially selected response as an actual value of the fixed unknown initial state. It does not introduce a free corner-parity oracle: the policy returns (D) and **does not evaluate (D) at an unknown parity bit while deciding any of the eight continuation queries**. The real physical theorem must later apply this decoder to the sign actually obtained by the end of the nineteenth corner read.

### 15. Exact vocabulary reification of the frozen JSON certificate

The original finite artifact stores each node as one of three arrays: `["leaf"]`, `["repeat", next]`, or `["read", address, {color: next, ...}]`. The source-level parser `parseFrozenSectorNodes` converts these arrays to typed instructions `FrozenInstruction Nat Nat Unit`. It requires a query address in `0..12`, accepts only the six actual face-color labels, and verifies present child destinations are natural numbers. Missing colors map to a distinguished invalid node index equal to the array length. Because the verification protocol checks only *feasible* replies, the typed interpreter is total on arbitrary replies while rejecting incomplete paths if encountered.

A `repeat` instruction becomes a valid color query whose answer is deliberately ignored. This is safe only when charged as one physical frame, as in the parser; it may not silently skip the corner read at that frame. A `leaf` instruction is assigned no guessed initial state: the sound sector compiler derives the terminal decoder from the posterior list and signed uniqueness invariant.

The elementary proof `parsed_sector_has_bounded_policy` connects a successfully parsed typed array to the same generic `Fits k` construction. **This is not yet the theorem that the pinned 52-root input satisfies the full semantic specification**; a generic parser can represent syntactically correct but semantically false decision trees.

### 16. Current proof obligations, reviewer challenges and evidence

The frozen 52-root checker has already independently inspected 144,736 candidate records, 141,097 decision nodes, 3,188 singleton leaves and 70,774 opposite-sign two-candidate leaves. Those figures are valuable finite evidence but must be bridged by a correctness theorem showing that the pinned `NineteenReadData.verifyNode` acceptance condition implies the proposed `SemanticallyValidSector` predicate for every actual graph root and exact sector state list. Such a theorem should expose one local simulation lemma for each instruction constructor, rather than treating the full certificate as an unexplained axiom.

The strongest skeptical test is to ask where, in the type of the full physical policy, the terminal sign becomes available. The correct solution is to bundle a continuation policy returning the sign-indexed function (D\), then use the physically decoded corner sign from the actual nineteen paired corner facelet replies as the argument to (D). The seventeen or more unconstrained intermediate observation outputs do not secretly include that bit; the corner identification theorem must explicitly derive it at the permitted final time.

Further open gates are the selected color-map/slot-sort sign cocycle for each *ordered* eleven-color prefix, an exact refinement of the actual JSON certificate to the typed graph, and the fixed original-pose probing compiler. The mathematically correct conclusion of this section is **soundness of the generic typed sign-deferred interpreter conditional on explicit finite sector validity**, not an unconditional full 19-frame identification theorem.

### Source-critical methodological context

The ingested **original** 1980 IEEE FOCS paper by Furst, Hopcroft and Luks develops stabilizer-chain coset tables and a short straight-line-program DAG for group computations. Its DAG is a *calculation* graph, not automatically an adaptive query-response controller with causal correctness. Knuth's **1991 Combinatorica** original studies strong-generator transversal invariants and the sensitivity of implementation complexity to relabeling; it does not certify that representative relabeling preserves a Rubik sensor trace. Babai's **1981 Annals** original frames fixing sets and distinguishing numbers in a different general permutation-group setting, and Tillquist–Frongillo–Lladser's **2021 arXiv v1** survey concerns shortest-path *metric* observations rather than our categorical paired-sticker feedback. The full source editions and SHA-256 receipts are available in the [AS0 original-byte custody ledger](../../docs/0.29/20261121_AS0_00_INTAKE_FOUR_PRIMARY_SOURCE_CUSTODY.md).

**Research director's assessment:** the gain is not a faster brute-force loop but the replacement of per-node proof obligations with a single parametric correctness theorem and a total semantic interpreter. The next necessary step is a verified mapping from the *existing immutable bytes* of each of the 52 trees to this theorem's premises. The project must avoid declaring publication-level closure until this and the actual corner-sign timing are formally established.

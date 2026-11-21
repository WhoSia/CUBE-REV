# Exact Adaptive Identification of a Fixed-Center Rubik's Cube by Paired Facelet-Color Queries

**CUBE-REV 0.29 — AT working manuscript (21 November 2026)**  
**Scientific status:** partial formal lower/upper closure, **not** a submission claim that the global nineteen-query upper bound has been proved in Lean. The central finite soundness theorem is parametric and the instantiated 52-root theorem remains an explicit pending obligation.

## Abstract

We examine identification of a legal (3\times3\times3) cube from repeated *paired observations* of one edge facelet and one corner facelet, under known face-turn repositioning and a fixed physical observation frame. The observation cost is the number of paired sensing frames, rather than the number of moves needed to implement a frame. We distinguish a fixed nonadaptive schedule from an adaptive strategy in which the next observed edge facelet can depend only on previously observed colors. For the former, a separate result establishes the optimum 21 frames in the corresponding restricted model. For the latter, a formally checked eighteen-frame impossibility argument survives even if the full initial corner state is given to the decoder. A concrete nineteen-frame construction has been discovered and its finite edge-policy certificate independently replayed: eleven initial edge observations, a family of eight-read continuation trees for 52 symmetry representatives, and a nineteen-frame corner schedule recovering the corner permutation sign.

The proof difficulty is not the size of the finite search alone, but a semantic one: a certificate leaf that contains two candidate edge words of opposite sign is a valid identification leaf only if the sign is eventually extracted from *actual* corner observations, and the sign must not be used to choose preceding queries. We present a typed, budgeted semantics for the frozen read/repeat/leaf instruction language, a finite candidate-sector verification predicate, a terminating Boolean proof checker and a general soundness theorem relating acceptance to exact signed identification. We also prove that padding an early leaf with genuine reads preserves its decoder while forcing exactly eight continuation frames, so the final corner sign becomes physically available at the correct time. The remaining upper-proof obligations are an instantiated verification of all 52 immutable roots, correct normalization of all ordered eleven-color prefixes, and final compilation to fixed physical probes. We therefore present the nineteen-frame upper as a **reproducibly certified computational construction** whose **universal Lean instantiation is still open**, rather than as an unconditional formally closed theorem.

## 1. Model and the question of optimality

Let \(\mathcal C\) denote the set of physically reachable, fixed-center configurations, with the standard corner-twist, edge-flip and common permutation-sign constraints. An observation address \(a=(a_e,a_c)\) denotes an original-pose edge-facelet index and an original-pose corner-facelet index. The observation channel is

\[
  O : \mathcal C\times\mathcal A \longrightarrow \{0,1,2,3,4,5\}^2,qquad
  O(s,a)=(\operatorname{color}_e(s,a_e),\operatorname{color}_c(s,a_c)).
\tag{1}
\]

The coordinates refer to the unknown **initial** cube, not just to the currently rotated cube. A sequence of known face turns can route an original-position address to the fixed physical sensors; the routing computation itself must preserve the relation (1) after a sequence of measurements. This distinction prevents inadvertently treating a physical face turn as a free relabeling of unknown data.

A strategy with budget \(n\) is a rooted, response-labeled tree whose internal nodes each issue one actual paired sensor read and whose next address depends only on the observed response history. The terminal decoder is required to output the exact initial state. A fixed schedule is the special case in which the same sequence of addresses is used regardless of responses. We distinguish these two optimization problems throughout: no fixed-schedule result alone implies an adaptive lower bound, and a state-space information count alone does not imply an optimal physical policy.

## 2. Known lower-bound and computational upper-bound evidence

The current machine-readable lower-bound construction establishes **nonidentifiability after at most eighteen adaptive paired reads**, even when the complete initial corner state is revealed, under its precisely stated legal-edge and physical probing assumptions. The lower proof depends on a separately disclosed finite `native_decide` computation in Lean, so it should be described as *kernel-checked theorem assembly with a trusted native-evaluation boundary*, not as a foundationally axiom-free closed form result.

On the other hand, the upper policy begins with eleven fixed first-side reads of distinct edge slots. The corresponding eleven corner reads follow a fixed schedule. A first-eleven-color transcript has one of 1,362 attainable six-color multiplicity vectors. The 48 color transformations preserving the six-center opposite-pair graph induce 52 distinct representative multiplicity vectors. Each representative sector is equipped with one frozen eight-read edge continuation tree. The pinned policy-checker receipt is:

| Quantity | Exact value |
|---|---:|
| Center-color opposite-pair symmetries | 48 |
| Attainable eleven-color multiplicity vectors | 1,362 |
| Canonical representative vectors / trees | 52 |
| Full oriented-edge candidate records across all representatives | 144,736 |
| Total frozen decision graph nodes | 141,097 |
| One-candidate terminal leaves | 3,188 |
| Two-candidate terminal leaves with opposite signs | 70,774 |

These are **finite certificate data**, not a standalone proof that a user-facing physical observer can identify any legal initial state. The distinction is essential in a proof-carrying interpretation: a global certificate must show all relevant legal states and all feasible response paths are represented *and* that the runtime decoder uses only information available at that time.

## 3. The exact signed leaf principle

For a finite candidate sector \(B\subseteq S\), write \(\epsilon(s)\in\{0,1\}\) for the permutation parity of the complete twelve-edge cubie word. A terminal leaf is *sign-distinguishing* when

\[
  \operatorname{SignUnique}(B)
  \quad\Longleftrightarrow\quad
  \forall x,y\in B,\quad \epsilon(x)=\epsilon(y)\Rightarrow x=y.
\tag{2}
\]

This condition allows at most two candidates, and if two remain they must have opposite sign. Define the terminal function \(D_B(p)\) as the first member of \(B\) with sign \(p\), or `none` if there is no such member. By structural induction on the list of candidates,

\[
 \operatorname{SignUnique}(B)\ \wedge\ s\in B
 \quad\Longrightarrow\quad D_B(\epsilon(s))=s.
\tag{3}
\]

Conversely, if \(D_B(p)=s\), then \(s\in B\) and \(\epsilon(s)=p\). The two directions matter: the first proves correct reconstruction when the physical sign becomes available; the second prevents a malformed leaf decoder from inventing a candidate not present in the observation posterior.

The Lean names are `first_candidate_is_correct_of_sign_unique` and `first_candidate_witness_belongs` in `SignedSectorLeaf.lean`. They are general theorems for arbitrary finite state types and are not limited to a single favorable tree.

## 4. Exact reply fibers and the semantics of an adaptive certificate

Let \(O_e(s,q)\) be the observed edge-facelet color when the sector controller queries address \(q\). For a finite belief list \(B\) and reply \(r\), the exact posterior is

\[
 B_{q,r}=\{s\in B\colon O_e(s,q)=r\}.
\tag{4}
\]

An instruction is one of \(\mathrm{finish}\), \(\mathrm{choose}(q,f)\), or \(\mathrm{padding}(q,j)\). The latter denotes a *physical read* of \(q\) with an ignored reply, not a free edge or corner observation. A typed graph can be malformed (missing node, too-deep path, omitted feasible reply); such cases must fail closed. Define \(\mathrm{Valid}(G,k,j,B)\) recursively by: a leaf is valid if (2) holds; a choose instruction is valid if every *feasible* child satisfies the invariant for the filtered list (4) at budget \(k-1\); a padding instruction continues at \(k-1\) with unchanged belief; and missing or out-of-budget nonterminal nodes are invalid.

The compiled policy \(P_{G,k,j,B}\) has type

\[
     P_{G,k,j,B}:\quad
     \operatorname{Policy}(Q,R,\{0,1\}\to\operatorname{Option}(S)).
\tag{5}
\]

**The terminal output is a function of an as-yet-unknown bit.** It is not the bit itself. This is a deliberate causal separation: while query choices may depend on edge replies, they cannot depend on the corner parity inferred only after the final corner measurement.

**Theorem 4.1 (sound sector interpretation).** For any typed graph, finite belief list, observation function, sign function and remaining budget, if \(\mathrm{Valid}(G,k,j,B)\), then the compiled policy meets its full reply-branch budget, and for every \(s\in B\),

\[
   \big(P_{G,k,j,B}.\operatorname{run}(O_e,s)\big)(\epsilon(s))=s.
\tag{6}
\]

The proof is induction on budget, using (3) for the leaf, (4) and the actual reply for a choose node, and a strictly decreasing budget for padding. No assumption on the distribution of unknown states or on a randomized scrambling process is required.

## 5. From a semantic universal quantifier to a finite executable check

A mathematical validity predicate quantifies over all possible replies that can be generated by a surviving candidate, not necessarily every member of the syntactic response type. The crucial reduction is

\[
  \big[\forall r,\ B_{q,r}\ne\emptyset
      \Rightarrow \mathrm{Valid}(G',k-1,j(r),B_{q,r})\big]
  \iff
  \big[\forall s\in B,\ 
      \mathrm{Valid}(G',k-1,j(O_e(s,q)),B_{q,O_e(s,q)})\big].
\tag{7}
\]

The forward direction chooses the witness state itself to establish that its reply is feasible. The reverse direction chooses the state witnessing a feasible reply and substitutes that equality. This equivalence is formalized in Lean as `statewise_sector_valid_iff_semantic`, with the consequential terminal correctness theorem `statewise_checked_sector_recovers_each_candidate`.

Now define a *transparent Boolean checker* rather than assuming a validity predicate. Let \(A_f(B)\) be a Boolean left-to-right universal quantifier over the entries of a finite list. It returns true if the predicate holds on every listed entry, with the empty list returning true. Let \(U(B)\) inspect **every pair of listed candidates** and return true exactly when their signs differ or the candidate identities are equal:

\[
 U(B)=\bigwedge_{a\in B}\bigwedge_{b\in B}
       \big[(\epsilon(a)\ne\epsilon(b))\lor(a=b)\big].
\tag{8}
\]

Define \(V(G,k,j,B)\) by a terminating recursion on \(k\): use (8) at a leaf; compute the Boolean conjunction of recursively verified *actual* response fibers at a choose node; and check the unchanged belief at a padding node. Missing nodes and reads at zero remaining budget return false. The recursion is well-founded even for an adversarial cyclic graph because *budget strictly decreases on each executed instruction*.

**Theorem 5.1 (proof reflection).** For arbitrary typed graph \(G\), observation \(O_e\), sign \(\epsilon\), finite belief list \(B\), budget \(k\), and root \(j\),

\[
   V(G,k,j,B)=\operatorname{true}
   \quad\Longrightarrow\quad
   \operatorname{StatewiseSectorValid}(G,O_e,\epsilon,k,j,B).
\tag{9}
\]

The proof is completely generic: an auxiliary induction proves that a true finite conjunction passes to each of its listed entries; this gives sign uniqueness at the leaves and the required checked child for each actually surviving state. The hypothesis about all feasible replies in (7) follows without search-specific axioms.

Combining Theorem 5.1 with (6) yields a **checkable certificate theorem**, schematically

\[
 \begin{split}
  &V(G,8,0,B)=\mathrm{true},\ s\in B
  \\
  &\qquad\Longrightarrow\quad
    \big(P_{G,8,0,B}.\operatorname{run}(O_e,s)\big)(\epsilon(s))=s.
 \end{split}
\tag{10}
\]

In the repository, `ReflectedSectorChecker.lean` implements the predicate and its proof. This theorem establishes *soundness when accepted*, not necessarily completeness of the Boolean checker on every valid graph. Nor does it by itself compute the value of (9) for the actual 52 fixed representatives; those are separate finite instances.

### Efficient finite instances and the next unproved bridge

A literal implementation of (9) may recompute a child sector for every state that produces an identical reply. This is semantically correct but computationally redundant. A production checker should enumerate the distinct feasible reply colors once, filter the surviving candidate list by each color, and reuse the result by memoization on the tuple \((j,B,k)\). Correctness of that optimization follows from (7) provided the set of distinct reply values is itself computed exactly. The candidate-sector generator and JSON graph parser must be connected to this new checker with the very same data bytes accepted by `NineteenReadData.check`. **The counts in the existing upper receipt do not independently establish the new premise \(V=\mathrm{true}\).**

## 6. The terminal corner sign and exact physical time

Seven corners can be identified from two cyclically ordered stickers per position. The eighth corner cubie is determined by exclusion and its orientation by the legal zero-twist sum. The fixed nineteen-frame corner address schedule samples fourteen *distinct* corner positions, with additional repeats as necessary to maintain one corner read per paired frame. Its final distinguishing corner sticker is delivered only at **frame 19**.

An edge continuation tree may reach a sign-distinguishing leaf before consuming all eight of its permitted follow-up reads. If the controller simply terminated at that point, the corresponding simultaneous corner reads would also cease prematurely. This would be especially dangerous when a claimed decoder is later applied to a corner parity bit that has not actually been observed.

The transformation \(\operatorname{padToExact}(P,8)\) instead pads an early edge terminal with **actual** observations of a fixed legal fallback edge-facelet address while ignoring their responses. It proves:

\[
 \begin{aligned}
 \operatorname{Fits}(8,P)&\Longrightarrow
    \operatorname{Fits}(8,\operatorname{padToExact}(P,8)),\\
 \operatorname{run}(\operatorname{padToExact}(P,8),s)
     &=\operatorname{run}(P,s),\\
 \big|\operatorname{transcript}(\operatorname{padToExact}(P,8),s)\big|&=8.
 \end{aligned}
\tag{11}
\]

All three underlying Lean theorems have **no axiom dependencies**, as independently confirmed in the pinned build log. Combining the checkable finite validity condition with this padding yields an exactly-eight-read continuation whose terminal decoder is still (5). The physical observer can therefore collect the remaining eight actual corner replies before evaluating that decoder at the derived parity.

The full cube-specific physical theorem must additionally prove that the corner observation trace really determines the common legal edge/corner permutation sign in the original coordinate convention, including the sign correction induced by stable sorting and opposite-pair color relabeling. Neither the generic theorem nor a parser result may simply posit a free Boolean terminal oracle.

## 7. The source of signed normalization and the necessary cocycle

A first-eleven prefix appears in arbitrary order with arbitrary legitimate six-color labels. Color graph symmetries \(\sigma\) and a stable ordering \(\beta\) of the eleven observed edge slots reduce these observations to one of 52 representative multiplicity patterns. A representative word is decoded in a transformed coordinate system; the original edge permutation sign is not simply the sign of the transformed candidate word. The correct relation is, in \(\mathbb Z_2\),

\[
 \epsilon_{\rm rep}
     =\epsilon_{\rm original}
      \oplus\operatorname{sgn}(\beta)
      \oplus\operatorname{sgn}(\alpha_{\sigma}),
\tag{12}
\]

where \(\alpha_{\sigma}\) is the induced permutation of twelve edge cubie types. Both corrections must be derived from the **already observed** prefix and the chosen gauge witness, not from any unobserved sticker. Retaining the normalizer witness is essential for sound inversion. An error here can leave all finite representative trees individually valid while producing an incorrect original state after de-normalization.

A representative-gauge theorem, sign correction and round-trip state mapping exist in the formal package. The unresolved task is to produce the *fully composed physical adaptive policy* that chooses each actual next read based solely on the available history and uses the observed terminal corner sign at the correct time.

## 8. Related work, original-edition discipline and novelty

**Permutation-group computation.** Furst, Hopcroft and Luks (1980, original IEEE FOCS pp.36–41) construct polynomial-time stabilizer/coset routines and straight-line programs for group elements. Their computation DAG is not automatically the response-labeled observation policy DAG we certify. Knuth (1991, original *Combinatorica* 11:33–43) gives an explicit strong-generator/transversal data structure and demonstrates how simple relabeling can substantially alter computational behavior. The latter insight motivates recording the exact prefix normalization and not treating all symmetric traversals as operationally identical.

**Distinguishing sets and canonical labeling.** Babai (1980, *SIAM J. Comput.* 9(1):212–216), acquired in its actual five printed original pages during the AT intake, canonically labels strongly regular graphs using adjacency neighborhood traces on distinguishing vertex sets and gives a probabilistic small distinguishing-set bound. Babai (1981, *Annals of Mathematics* 113:553–568), independently acquired in an earlier source sweep, relates pointwise fixing sets and distinguishing subsets of coherent configurations to permutation-group order estimates. Neither prior work addresses the physical paired-color cube channel, legal corner parity coupling, or an adaptive nineteen-frame policy.

**Graph metric dimension.** Tillquist, Frongillo and Lladser (2023, *SIAM Review* 65(4):919–962, DOI 10.1137/21M1409512), now held in the **exact 44-page journal edition** in addition to the separate 2021 29-page preprint, define distinguishing observations by vectors of graph shortest-path distances to landmarks. Their work is relevant to classifying observation models, complexity and nonadaptive resolving sets, but does not supply a sticker-color adaptive query bound for a Rubik's cube.

**Concurrent proof methodology.** Brookes (2004) models interference and state ownership in concurrent separation logic via traces; Jones's Oxford PRG-25 monograph develops interference-aware program reasoning; Baldwin and Clark's (2000) *Design Rules* analyzes modular interfaces and design evolution. We use these as source-conscious methodological analogies for **trace semantics and modular proof obligations**, not as theorems implying cube reconstruction.

**Scope of original sources.** The exact original Harary–Melter (1976), Slater (1975) and Hennie (1964) papers remain an explicitly maintained three-item acquisition queue. The newly archived Azema–Couvissier–Richard (1972) IFAC fault-detection article is a *different* scientific work from Hennie's 1964 original. No absent primary article is silently substituted by a secondary survey.

## 9. Proof dependency map and reproducibility

The proof dependency graph is intentionally short at the point of reflection:

\[
\boxed{\mathrm{checkFiniteSector}=\mathrm{true}}
\Longrightarrow
\mathrm{StatewiseSectorValid}
\Longleftrightarrow
\mathrm{SemanticallyValidSector}
\Longrightarrow
\boxed{\text{correct sign-indexed decoder}}.
\tag{13}
\]

The separate exact-length padding theorem changes only the physical observation count, not the decoder. Parsing the frozen JSON schema is a third edge: its typed result must be shown extensionally equal to the exact finite policy used in (13). That edge has not yet been closed for all 52 roots, and retaining it as a **named obligation** is part of reproducible publication ethics.

The immutable upper-policy certificate has SHA-256 `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227` as required by the independent Python replay. The Lean source is built with pinned Lean 4.34.1 under the read-only `.github/workflows/cuberev029-lean.yml` workflow. Individual theorem axiom reports distinguish standard Lean `propext`/`Quot.sound` from `native_decide` data receipts. A successful compile of the generic proof-reflection theorem is **not** the same as a proof that the 52 concrete Boolean checker values are all true.

## 10. Explicit theorem status

**Established in Lean (subject to individual CI status):** signed unique-leaf selection; typed finite posterior update; soundness of semantic sector compilation; equivalence between all-feasible-reply validity and statewise validity; exactly eight physical continuation reads without altered terminal output; and the general Boolean-to-statewise implication once the current new module passes its pinned build.

**Established as frozen computations but not all yet reflected into the new Lean theorem:** the 52 policy JSON roots, their 144,736 candidate records, 141,097 total nodes, singleton/opposite-sign terminal counts, 48 color automorphisms, 1,362 prefix histograms and physical randomized replay.

**Open:** a computable, efficient *distinct-reply* finite checker together with its proof of equivalence; verified acceptance of each of the pinned 52 roots at the actual finite candidate sectors; complete sign-correct stable-sort normalization for every **ordered** eleven-reply transcript; and a single original-pose physical `Fits 19` policy assembled with the real final corner transcript.

Consequently, the manuscript should presently report **a rigorous eighteen-frame lower result with its declared native certificate, and a strongly replayed nineteen-frame upper construction with a newly formalized generic semantic bridge**. The decisive proof-completion event will be the unconditional statewise certificate theorem for every real representative and the final physically causal paired-frame compiler.

## Primary works actually inspected

1. László Babai (1980). *On the Complexity of Canonical Labeling of Strongly Regular Graphs*. *SIAM Journal on Computing* **9**(1), 212–216. [Exact original PDF held](https://drive.google.com/file/d/1nexKWPDCFEphguQ4t1GD3AmUEmitH_6I/view).
2. László Babai (1981). *On the Order of Uniprimitive Permutation Groups*. *Annals of Mathematics* **113**(3), 553–568. [Original PDF held](https://drive.google.com/file/d/1PdBg2ByUtXQQ61k47DHHxPUQ4J0C1j4r/view).
3. Merrick Furst, John Hopcroft and Eugene Luks (1980). *Polynomial-Time Algorithms for Permutation Groups*. IEEE FOCS 21, 36–41. [Original printed six-page conference PDF](https://drive.google.com/file/d/1AhZmbHGT_8RnIZ3D4OoSTdZK7aZLYvkF/view).
4. Donald E. Knuth (1991). *Efficient Representation of Perm Groups*. *Combinatorica* **11**(1), 33–43. [Original eleven-page journal PDF](https://drive.google.com/file/d/1mIhQ-9tchQp-quRSkFyFF5AY0m1HTdaZ/view).
5. Richard C. Tillquist, Rafael M. Frongillo and Manuel E. Lladser (2023). *Getting the Lay of the Land in Discrete Space: A Survey of Metric Dimension and Its Applications*. *SIAM Review* **65**(4), 919–962. [Original 44-page journal PDF](https://drive.google.com/file/d/1l4OPfnvgy7reraPJyOCRXupE9Rr0sjws/view).

**Source governance:** [AS four-source original custody](../../docs/0.29/20261121_AS0_00_INTAKE_FOUR_PRIMARY_SOURCE_CUSTODY.md), [AT six-source original custody](../../docs/0.29/20261121_AT0_00_INTAKE_SIX_SOURCE_CUSTODY.md), [three genuinely missing primary works](../../docs/0.29/20261121_AR0_MISSING_ONLY_DIRECT_DOWNLOAD_REGISTER.md). This chapter is an independently maintainable working paper; later improvements should preserve the difference between checked theorems, computational evidence and future obligations.

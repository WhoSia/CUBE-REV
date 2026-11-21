# Exact Adaptive Identification of a Fixed-Center Rubik’s Cube
## AU — Causal Refinement of the Nineteen-Frame Candidate Decoder: Immutable Fifty-Two-Root Reflection, Tagged Queries, and Parity Release
**Working manuscript AU1 — 21 November 2026. Research-only, not a publication-ready theorem of unconditional physical optimality.**

### Abstract

A previously constructed finite certificate describes fifty-two representative eight-read adaptive continuations after eleven first-color observations of the Rubik's Cube's twelve edge positions. The main proof problem is not the numerical size of that certificate but its operational meaning: a reply-labeled graph must be interpreted as a *causal* sequence of physically charged observations, and its terminal two-element posterior may be resolved by corner permutation sign only after that sign has been determined from nineteen actual corner sticker observations. We establish an explicit layered refinement approach. The immutable 52-root data are parsed as typed finite policies, their reachable branches are checked against the exact surviving oriented-edge candidates, and generic Lean soundness theorems turn true finite checks into signed terminal reconstruction. We then distinguish first-side queries from continuation-side queries by tagged addresses and compose an eleven-read prefix with a padded eight-read continuation, enforcing nineteen charged observations without anticipation. The completed reflection theorem is conditional only on the actual checker acceptance, now verified for the immutable 52 roots with `native_decide`. The new tagged composition bridges source-certificate semantics to a nineteen-step **abstract oriented-edge** experiment for selected representative prefixes; it does not yet provide the missing color-symmetry normalization for all 1,362 ordered original prefix classes or the fixed-probe physical face-turn policy. We give precise hypotheses, verification limits, source-provenance distinctions, and an explicit negative case showing why early edge-sector termination must not be conflated with release of the final corner sign.

### 1. The model and its causal constraint

Let `Word` encode an oriented assignment of all twelve edge cubies to twelve original positions. An oriented cubie word `w[j]` is a natural number whose half-index identifies the cubie and whose low bit identifies its orientation. The edge-color channel is determined from the fixed twelve-cubie catalogue. A paired frame interrogates one edge facelet and one corner facelet after a legal face-turn route, both chosen before the paired colors become known. Consequently a controller at frame `t` can depend on the responses of frames `1,...,t−1` but **not** on frame `t` or on the later terminal corner sign. The fixed-center convention names the six colors unambiguously; an algorithmic change of color labels is a proof-level representation transformation, not a physical whole-cube motion.

The first eleven edge observations are the first facelets at original positions `0,2,...,20`. The remaining unknown edge positions include the second facelets of those eleven and both facelets of the last unread edge. The frozen certificate describes each continuation query by a number in `0,...,12`: entries `0,...,10` address the second side of a previously observed edge, while entries `11,12` address the two sides of the last edge. **This query-address vocabulary must not be reused for the first eleven reads**, since the same integer would otherwise address a different physical sticker. A tagged query channel resolves this ambiguity.

We use two distinct Boolean notions. The selector's **sign** is the parity of the cubie permutation of the initial oriented edge word; by the physical legality condition it equals the parity of the original corner permutation in the *same* coordinate gauge. It is not the orientation-parity bit, and it must be transported under any color type relabeling or edge-slot sorting permutation. The corner sign is released only when the actual scheduled corner observations have been read, notably the last fresh corner color at frame nineteen.

### 2. A proof-reflected finite semantics of frozen graphs

Let `G` be a finite typed array of instructions. Its nodes are `finish`, `choose q child`, or `padding q child`. Let `B` be the current list of candidate states and `O(s,q)` the actual response channel. The exact posterior fiber is
[
B_{q,r}:=\{s\in B\mid O(s,q)=r\}.
\tag{2.1}
]
At a `choose` node, the controller observes one actual color `r`, then descends to the response-named child with `B_{q,r}`. At a padding node, it consumes a frame, discards the observation, and retains `B`. A malformed node or an impossible out-of-bounds child fails closed. A terminal node is acceptable if no two **different** elements of `B` share an edge cubie permutation sign:
[
operatorname{SignUnique}(B):=\forall s,t\in B,quad
operatorname{sign}(s)=operatorname{sign}(t)\Longrightarrow s=t.
\tag{2.2}
]
It does **not** require `|B|=1`; a pair of opposite-sign candidates is permitted, precisely because the terminal corner sign later disambiguates them. A two-candidate same-sign leaf is rejected.

Define `StatewiseSectorValid(G,O,sign,k,v,B)` by decreasing the remaining observation budget `k`. At each internal node it checks, for every actual surviving candidate `s∈B`, the child and posterior chosen by the actual response `O(s,q)`. This is equivalent to quantifying over all *feasible response values* because each feasible value has an `s` witness and every surviving `s` produces a feasible response. The equivalence is proved generically in Lean's `statewise_sector_valid_iff_semantic`, without relying on an enumeration of cube states.

The executable checker `checkDistinctSector` optimizes the statewise condition by calculating the list of distinct responses produced at `q`, not by scanning the belief again for each of its potentially thousands of candidates. Its crucial generic invariant is:
[
s\in B\Longrightarrow O(s,q)\in
  \operatorname{eraseDups}(\operatorname{map}(O(-,q),B)).
\tag{2.3}
]
For every typed graph, every finite belief and any remaining budget, the Lean theorem `checkDistinctSector_sound` derives `StatewiseSectorValid` from the checker returning `true`. It uses an explicit lawful equality assumption on the response alphabet to justify deduplication and thus cannot discard a physically realizable response by fiat.

**Theorem 2.1 (generic sound signed continuation).** Suppose `checkDistinctSector(G,O,sign,8,root,B)=true`. For every `s∈B`, there exists a compiled controller using exactly eight actual continuation readings and returning a terminal function `D_s : Bool → Option Word` such that `D_s(sign(s))=some(s)`. The controller does not receive `sign(s)` as an observation; it receives only the ordinary categorical sensor replies while running.

*Proof.* Checker reflection gives statewise semantic validity, which is equivalent to feasible-response validity. Induction on the read budget gives signed terminal reconstruction. Early terminal nodes are padded with actual ignored reads, preserving the output and making the transcript length exactly eight; all three padding equations are kernel-proved without additional axioms. □

The computational soundness theorem is **parametric** and does not assume that a JSON document with a plausible schema is correct. A separately verified receipt must establish its premise for the actual immutable source.

### 3. The entire original 52-root source is now connected to the theorem

The certificate file `upper-policy-certificate.json` is restored only after exact SHA-256 verification of the committed compressed data and the decompressed source. Its known original JSON digest is
`80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`.
The `NineteenReadData.check` parser validates the original certificate structure, first-eleven color histograms, 48 color automorphisms, 1,362 supported counts, 52 count-vector representatives and all reachable response-labeled branches. Its receipt is:
[
(\#\mathrm{roots},\#\mathrm{countVectors},
  \#\mathrm{candidateRecords},\#\mathrm{nodes},
  \#\mathrm{singletonLeaves},\#\mathrm{oppositeSignPairs})
=(52,1362,144736,141097,3188,70774).
\tag{3.1}
]

The newer `FiftyTwoRootReceipt.lean` adds a stronger machine check. For each actual JSON root it parses the original prefix and candidate words, reifies the original `read/repeat/leaf` instructions as a typed graph, and evaluates `checkDistinctSector` over the real color response function, not over fabricated example candidates. The Boolean `certifiedFrozenRoots(source)` is true only if the old whole-certificate structural receipt equals (3.1), there are exactly 52 roots, and every root passes the deduplicated semantic verifier.

**Theorem 3.1 (frozen representative soundness).** For every entry of the parsed immutable 52-root source, there exist an exact typed finite graph `G` and the exact candidate set `B` parsed from that entry such that (i) the parser returns `(G,B)`; (ii) the eight-read signed continuation policy is bounded; and (iii) for every `s∈B`, its output decoder, when supplied the *true original representative-gauge sign*, returns `some s`.

*Proof.* `fifty_two_frozen_roots_semantically_accepted` verifies the entire immutable source via `native_decide`. The kernel-checked `certified_source_each_root_has_exact_semantics` extracts the appropriate finite graph, belief, and semantic premise from each member of the 52-root array. `certified_source_each_root_recovers` and `every_actual_frozen_root_recovers` instantiate Theorem 2.1. The source-specific computational equality retains its explicit `native_decide` trust dependence; the generic soundness implication does not. □

**Verification evidence:** pinned read-only GitHub Actions [#44908053135](https://github.com/WhoSia/CUBE-REV/actions/runs/44908053135) completed **successfully** on 21 November 2026. It compiled the 58 source modules, replayed both frozen certificates and printed the exact theorem axioms. The success of this computation establishes the 52-root premise, **not** physical optimality.

### 4. Eleven plus eight with disjoint address tags

A potential correctness error is to use a single `Nat` address space for the eleven first-side observations and for the normalized continuation. The two domains have overlapping integer representations but different sticker interpretations. Define:
[
Q_{\mathrm{tagged}}=\{\mathrm{first},\mathrm{continuation}\}
\times\mathbb N
\quad\text{and}\quad
O_{\mathrm{tagged}}(w,(b,i))=
\begin{cases}
 \mathrm{sticker}(w_i,\mathrm{first}) & b=\mathrm{first},\\
 O_{\mathrm{sector}}(w,i) & b=\mathrm{continuation}.
\end{cases}
\tag{4.1}
]
The first eleven fixed queries are `(first,0),...,(first,10)`. Their response list is exactly the eleven original first-side color codes, in index order. Every continuation query `q∈0..12` is lifted as `(continuation,q)`, with its color response unchanged. Neither function is allowed to consult the corner permutation or future sensor replies.

Define `matchingFrozenRoot(roots,answers)` to select only an actual root whose stored first-color prefix exactly equals the ordered response vector. An absent or malformed root returns the failure value `none`; such a branch never generates an invented successful reconstruction. The controller `elevenThenFrozen` is constructed by `Policy.withPrefix` and the tagged continuation lift, so the following general result follows from the budget and run equations.

**Theorem 4.1 (tagged nineteen-read skeleton).** Every root array—including a malformed one—defines a causal tagged policy whose read budget is at most nineteen: eleven first-side observations followed by a continuation of at most eight reads. Applying `padToExact` to the entire policy preserves every output while enforcing an observation transcript of length **exactly nineteen**, even on failed or unmatched prefixes.

*Proof sketch.* For each response vector, the root continuation either fails immediately or uses `exactEightSectorPolicy`, which has `Fits 8`. The address adapter preserves `Fits 8`. `Policy.withPrefix_fits` gives `Fits (8+11)`. The universal `padToExact_fits`, `padToExact_run`, and `padToExact_transcript_length` yield the claimed total budget, output equality and exact nineteen-element transcript. □

**Theorem 4.2 (matching representative reconstruction).** Consider an actual immutable root `e` selected by the observed eleven first-side colors. Suppose the original oriented edge word `w` belongs to the exact candidate list parsed for that root, and the source receipt has passed. Running the tagged nineteen-read controller on `w` produces a terminal sign-indexed decoder, whose value on the actual edge permutation sign is `some w`.

*Proof sketch.* `Policy.withPrefix_run` proves the continuation sees the already observed ordered prefix. `Policy.adapt_run` proves that the tagged continuation observes exactly the untagged sector feedback. The root-selection equality chooses `e`; its parsed candidate list contains `w`; Theorem 3.1 supplies the eight-read reconstruction. Overall padding preserves that result and does not move a sign test into any earlier branch. □

Theorem 4.2 is explicitly **representative-gauge** and **conditional on a selected matching root**. It does not assert that every one of 1,362 raw count vectors is itself one of the 52 representative prefixes, nor that an unknown original cube can be relabeled without a known sign correction. That is the separate orbit-transport obligation described below.

### 5. Why the newly ingested refinement literature matters—and where the analogy ends

Abadi and Lamport's *The Existence of Refinement Mappings*, 14 August 1988 DEC Systems Research Center manuscript, studies when behaviors of a lower-level state-machine specification implement the externally visible behavior of a higher-level specification. Their Theorem 2 (in this manuscript's numbered text, §7) states a completeness result under **machine closure**, **finite invisible nondeterminism** for the upper specification and **internal continuity**, after introducing suitable history and prophecy auxiliary variables. These qualifications are essential: a proof of implementation cannot be inferred just from matching a finite output-count receipt.

The closest analogy in our study is the local simulation between the certificate interpreter and the actual observation policy. Its *history* is the ordered transcript of queried addresses and returned categorical colors. That transcript determines the exact surviving belief, the orbit representative and—eventually—the sign correction. A proof-level *prophecy* variable in the sense of Abadi–Lamport may help establish existence of a simulation relation in general state-machine theory. **It is not a permissible extra sensor or a license to choose the next Rubik query using future colors.** Our upper policy deliberately refuses any such prophecy: the signed decoder remains a function of a Boolean supplied only after the last physically scheduled corner observation.

Lamport's 13 June 2024 *My Writings* (item [92]) identifies the publication history of the refinement paper: an abbreviated 1988 LICS version, SRC Report 29 and the final 1991 *Theoretical Computer Science* **82(2):253–284** version. The 1988 file held here is the earlier SRC manuscript, **not** a byte-identical copy of the 1991 journal typesetting. Lamport notes in his personal retrospective that the theorem required hypotheses beyond an early intuitive expectation and that structured proof review helped catch errors in earlier derivations. That retrospective is useful for identifying the exact source edition and for guarding against overstating the scope of the theorem; it is an **author recollection**, not a mathematical premise in our Lean development.

This contrast sharpens a methodological result: a certified finite decision graph is an *implementation artifact*, while a correct physical identification controller is a *behavioral specification*. The typed-graph-to-tagged-edge relation is a compositional refinement argument. Both local invariants and allowed environmental observations must be proved; the fact that a DAG has fewer than nineteen levels cannot by itself establish physical feasibility.

### 6. Remaining proof obligations and adversarial review

A full nineteen-paired-frame theorem must eliminate four substantial, currently open hypotheses.

**All ordered original prefixes, rather than just 52 representatives.** There are 1,362 supported first-color count vectors before color-opposite-pair automorphism reduction. Each actual eleven-reply sequence, including the order of reads, must determine a canonical 48-element color symmetry witness and a stable permutation of the eleven observed edge positions. These witnesses must be functions of *past replies only*. Color renaming and slot sorting change the representative permutation sign by explicit parity characters; the required correction must be derived and proved correct for each legal word, not guessed.

**Corner data and parity availability.** The corner schedule uses fourteen distinct corner sticker addresses, observing two cyclically consecutive stickers at each of seven corner positions. The eighth corner cubie and its orientation follow from the missing cubie and the legal total twist constraint, but only after the last new sticker has arrived at frame nineteen. The terminal decoder must be applied to the corresponding legally coupled edge sign in the same original coordinate gauge, transformed by the known normalization cocycle. Merely padding the edge policy ensures elapsed frame count; it does **not** itself prove that the corner responses have been obtained or decoded.

**Physical paired routing.** Equation (4.1) is an *abstract edge-sticker observation channel*. Its query names must still be mapped into legal move sequences that bring an original desired edge facelet and the scheduled corner facelet simultaneously to the fixed physical probes. Earlier face-turn routing tables check the local geometric endpoint condition, but the final controller needs a single causal composition theorem that retains the original cube's coordinates through every previous move.

**A single universal reconstruction theorem.** Once the color-sign transport, corner coupling and routing are discharged, the general `Policy.withPrefix` and `Policy.adapt` lemmas should yield a single physical `Fits 19` reconstruction for every legal initial cube. Until then, the appropriate published claim is: the lower-bound impossibility of eighteen reads has an existing verified proof under the stated trust boundary, the 52-root signed continuation has newly verified exact finite semantics, and a tagged nineteen-step abstract representative-policy compiler is being formalized. Calling the entire physical 19-frame bound "Lean closed" would be premature.

### 7. Reproducibility and authorial-source custody

All new source files are committed to [WhoSia/CUBE-REV, `research/current`](https://github.com/WhoSia/CUBE-REV/tree/research/current). The finite certificate's original raw JSON is restored and hashed independently in the pinned workflow; the Lean `native_decide` root acceptance deliberately reports its trust dependence. The gate requires every typed Lean module to be a Lake default target and checks absence of `sorry`, `admit` and newly declared `axiom` in the audited bridge files.

The two newly observed reference files were already classified in Research OS `11_SOURCES` at reinspection: [Abadi–Lamport 1988 SRC manuscript](https://drive.google.com/file/d/1Ga68Hd3iDQA2d3j1QZmwz8onIfOK95DH/view) and [Lamport 2024 annotated bibliography and scientific autobiography](https://drive.google.com/file/d/1ELMZMILhEDFO4xRbb8JSuTZsDKKZNn2y/view). Their roles are different: the former contains a specific formal completeness theorem, the latter identifies editions and offers a first-person historical recollection. Neither should be misrepresented as having proven a Rubik cube probe bound.

The exact 2023 SIAM Review edition of Tillquist–Frongillo–Lladser is also [owned in `10_PAPERS`](https://drive.google.com/file/d/1l4OPfnvgy7reraPJyOCRXupE9Rr0sjws/view); it identifies vertices by **shortest-path distance vectors** on graphs. The categorical paired-color feedback used here is a different experiment, so metric-dimension bounds are background comparison rather than direct lower or upper certificates. The remaining missing-only bibliography currently contains **three** original papers: Harary–Melter (1976), Slater (1975) and Hennie (1964).

**The near-term next theorem is** `universal_norm_and_sign_from_ordered_prefix`, combined with an exact physical nineteen-frame paired query compiler. These are not trivial bookkeeping tasks: a wrong choice of color symmetry or slot sorting can change permutation parity and therefore make a two-element leaf return the wrong legal cube. The negative control must explicitly demonstrate that an untransported sign would fail even if the 52-root tree structure and all leaf counts remain correct.

---

### Source references

1. M. Abadi and L. Lamport, *The Existence of Refinement Mappings*, DEC Systems Research Center, 14 August 1988 manuscript, §5 and Theorem 2 in §7. [Owned primary PDF](https://drive.google.com/file/d/1Ga68Hd3iDQA2d3j1QZmwz8onIfOK95DH/view). **Version: 1988 SRC, not 1991 journal.**
2. L. Lamport, *My Writings*, 13 June 2024, item [92], author-annotated bibliography and scientific autobiography. [Owned source](https://drive.google.com/file/d/1ELMZMILhEDFO4xRbb8JSuTZsDKKZNn2y/view).
3. M. Abadi and L. Lamport, *The Existence of Refinement Mappings*, *Theoretical Computer Science* 82(2) (May 1991), 253–284. **Bibliographically identified via Lamport [92]; exact journal-byte acquisition not asserted.**
4. D. E. Knuth, *Efficient Representation of Perm Groups*, *Combinatorica* 11(1) (1991), 33–43. [Owned journal edition](https://drive.google.com/file/d/1mIhQ-9tchQp-quRSkFyFF5AY0m1HTdaZ/view).
5. M. Furst, J. Hopcroft and E. Luks, *Polynomial-Time Algorithms for Permutation Groups*, 21st IEEE Symposium on Foundations of Computer Science (1980), 36–41. [Owned conference edition](https://drive.google.com/file/d/1AhZmbHGT_8RnIZ3D4OoSTdZK7aZLYvkF/view).
6. R. C. Tillquist, R. M. Frongillo and M. E. Lladser, *Getting the Lay of the Land in Discrete Space: A Survey of Metric Dimension and Its Applications*, *SIAM Review* 65(4) (2023), 919–962, DOI 10.1137/21M1409512. [Owned original 2023 journal PDF](https://drive.google.com/file/d/1l4OPfnvgy7reraPJyOCRXupE9Rr0sjws/view).


### Appendix A. A nineteen-slot *paired* observation clock without a hidden corner oracle

The tagged construction of §4 has a useful further refinement. It originally runs against an abstract oriented-edge word and, taken in isolation, returns no corner readings. We can pair each edge read with one explicitly scheduled corner address without changing any edge policy decision. This is not the full face-turn implementation of a physical cube, but it formalizes the *information-timing* contract of a paired observation policy.

Let the state be \((w,c)\), where \(w\) is a complete oriented edge word and \(c:\{0,\ldots,23\}\rightarrow\{0,\ldots,5\}\) is an arbitrary table of corner sticker colors. The paired query address is \(((b,i),j)\), consisting of a tagged edge address and an actual original corner address. Its response is
\[
 O_{\mathrm{pair}}((w,c),((b,i),j))
   = (O_{\mathrm{tagged}}(w,(b,i)),c(j)).
\tag{A.1}
\]
Write \(C=[0,1,6,7,9,10,18,19,21,22,12,13,3,21,21,21,21,21,4]\) for the *nineteen-element corner address schedule* used by the original X certificate. Every entry in this list is a real charged corner facelet observation; five repetitions at address 21 are allowed, but must not be omitted.

The controller transformation \(\operatorname{withCornerClock}(C,P)\) recursively replaces the next edge query \(q\) by paired query \((q,C_t)\) at the next clock index \(t\), branches solely on the **first component** of the actual paired response, and advances to \(C_{t+1}\). The corner color is observed but is not used to decide the next edge query. This is a deliberately strong noninterference property: changing the entire corner table \(c\) while keeping \(w\) fixed must leave the edge policy output unchanged.

**Proposition A.1 (paired noninterference).** For every tagged edge-feedback policy \(P\), every list of corner addresses \(C\), every oriented edge word \(w\), and every corner table \(c\),
\[
 \mathrm{run}(\operatorname{withCornerClock}(C,P),
   O_{\mathrm{pair}},(w,c))
 = \mathrm{run}(P,O_{\mathrm{tagged}},w).
\tag{A.2}
\]
Moreover, if \(P\) has \(\mathrm{Fits}(n)\), the paired controller also has \(\mathrm{Fits}(n)\).

*Proof.* Structural induction over the policy. At a terminal, both sides immediately return the same output. At each read, both policies select the identical tagged edge query; the paired query additionally includes the next predetermined corner address. Because the continuation receives only the first component of the reply, both recursive subpolicies see the same edge reply. The induction hypothesis therefore equates their outputs on every response branch. Budget preservation follows from induction on the \(\mathrm{Fits}\) derivation, charging one paired observation for every original edge observation. □

**Proposition A.2 (exact corner-address history).** If the fixed schedule has the same length as the executed edge transcript, then the corner addresses appearing in the executed paired transcript, *in their actual occurrence order*, are exactly the schedule. In particular, applying the clock to the padded nineteen-read tagged policy gives all nineteen corner addresses in \(C\); the nineteenth address is 4, and that address does not occur among the first eighteen slots.

*Proof.* Structural induction over the edge policy and case analysis on the schedule list. At a terminal, the edge transcript is empty, and equality of lengths forces the schedule to be empty as well. At a read, equality of the lengths of the complete transcripts implies that the schedule has a head and a tail of exactly the length of the child's transcript. The paired read contributes the schedule head, and the induction hypothesis supplies the tail. Apply the already checked length-19 theorem of the padded tagged policy and the independent finite `NineteenSchedule` facts `actual_corner_frame_budget` and `final_corner_color_not_early` to obtain the last assertion. □

Both propositions are formalized in [`PairedCornerClock.lean`](https://github.com/WhoSia/CUBE-REV/blob/research/current/formal/029/PairedCornerClock.lean) as generic theorems over every edge policy and every possible corner table. They avoid the tempting but invalid practice of permitting the edge query controller to inspect the corner permutation sign at an earlier point in the trace.

**Remaining refinement step.** The fixed paired address list in (A.1) is still an abstract original-coordinate read. A fully physical controller must use the previously proved move-routing compiler to transport each addressed original edge and corner sticker to the two permanent probes, including restoration of its historical pose. The final original-coloring state also must reconstruct *all* twenty-four corner stickers from their fourteen newly observed colors under physical legal-cube constraints and establish the parity identification in the same gauge as the selected oriented-edge candidate. Propositions A.1–A.2 prove the causal corner schedule and no-lookahead properties; they do not discharge these geometric and legal-state obligations.

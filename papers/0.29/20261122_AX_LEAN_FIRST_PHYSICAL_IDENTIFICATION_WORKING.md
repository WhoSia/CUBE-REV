# AX Working Manuscript — From a Certified 18/19 Observation Gap to a Lean-First Physical Identification Theorem

**CUBE-REV 0.29 | research draft | 2026-11-22 | theorem-to-paper alignment.** This working chapter is a publication-writing artifact, not an accepted result or an unconditional upper-bound proof. Keep prior T–AU manuscripts intact; the final paper may synthesize rather than stack every historical appendix.

## Provisional abstract (claim calibrated)

We study identification of an initially unknown but physically reachable fixed-center Rubik's Cube using charged paired observations: each frame returns the color of one selected edge sticker and one selected corner sticker, with legal face turns allowed between frames. A certificate-backed lower-bound analysis excludes identification in eighteen frames even when the entire initial corner state is supplied. A separate computation constructs adaptive continuations of eight edge observations after eleven fixed one-sided edge observations. Fifty-two representative first-color sectors arise from the action of the forty-eight automorphisms of the edge-color graph on the 1,362 realizable eleven-color histograms. An immutable finite certificate verifies the representative continuation trees under a terminal signed-decoder condition; it is not, by itself, a total physical policy proof. We formalize in Lean the simultaneous edge/corner observation model, generic adaptive-policy transport, the fixed-probe physical routing compiler, paired corner-color schedule, symmetry-induced edge relabeling, and deterministic normalization of eleven distinct observation positions even when their colors repeat. We identify the remaining integration obligations required to turn the computational nineteen-frame construction into an unconditional kernel-checked theorem: selection and retention of the normalization gauge for every ordered initial transcript, signed posterior equivalence of every representative tree, terminal sign recovery from *actual* corner replies, and the resulting single total abstract paired-policy theorem.

*Abstract status:* the eighteen-frame obstruction is certificate-backed; the nineteen-frame physical upper conclusion is explicitly open until these obligations are discharged.

## 1. Problem specification and a precise theorem target

Let `Coloring` denote an initial sticker coloring and `Reachable` the property of being attainable from the fixed-center solved cube by legal face turns. A charged observation frame consists of a pair of initial-pose sticker addresses `q = (q_e, q_c)` and a simultaneous response `abstractPairRead s q`; the controller must select both addresses before it receives either color. Free face turns may modify the pose between charged frames, but cannot supply free color readings. A policy may adapt the next address pair to the **past** response sequence only.

The target is a *single* decision policy `P` satisfying `Fits 19 P` and

```lean
∀ s : Coloring, Reachable s →
  P.run abstractPairRead s = s
```

The existing `Physical.physical_nineteen_of_abstract` converts exactly such an abstract policy to a fixed physical edge/corner probe with legal turn routing, preserving the charged frame budget. This is a conditional compiler theorem, not the missing total policy. We must distinguish a policy correct on a chosen representative sector from one correct on every reachable initial coloring.

## 2. What the evidence establishes, and by which mechanism

| Component | Precise established result | Trust mechanism | What it does not establish |
| --- | --- | --- | --- |
| Eighteen-frame lower obstruction | Certificate-backed adversary excludes every 18-read adaptive strategy under the stated information advantage | Independently checked finite certificate plus Lean receipt; disclose `native_decide` dependence | A lower bound for a different sensor, turn-cost, or model |
| Histogram support | Eleven first-side observations realize exactly 1,362 six-color multiplicity vectors satisfying Hall-type constraints | Graph matching proof, independent omitted-edge DP and 64-cut checks | The number of *ordered histories* or decision trees |
| Color quotient | The 48-element `Aut(K_{2,2,2})` action yields 52 unsigned histogram orbits | Burnside calculations, finite Lean symmetry lemmas | A 48-element physical cube rotation group |
| Sign correction | Stable position sorting and induced edge-type relabeling both contribute to the parity correction; the corrected abstract signed histogram quotient has 80 orbits | Independent cocycle audit and concrete lost-gauge negative control; partial Lean sign lemmas | A fully proved cube-specific normalization cocycle on all legal states |
| Fifty-two continuation policies | For each frozen representative root, a signed eight-read continuation has been checked against the enumerated compatible edge assignments | Pinned original JSON, independent checker, Lean `native_decide` semantic receipt | Validity of a silently selected representative or a free parity oracle |
| Corner clock | Nineteen genuine simultaneous corner readings satisfy the prescribed schedule, and equal corner transcripts identify legal initial corner colorings | Compiled Lean observation/legality theorems | Permission to use frame-19 corner replies before choosing the frame-19 edge query |
| Physical compiler | Every correct abstract paired policy transports to a fixed-probe legal-turn policy at identical observation cost | Generic Lean theorem `physical_nineteen_of_abstract` | Existence of the required correct total abstract policy |

The trust granularity is a scientific contribution: the certificate's finite acceptance theorem is allowed to have an explicit native-computation dependency, whereas the general response-equivariance and physical-compiler lemmas must be reported by their actual printed axiom list. A passing CI step is not proof of a theorem outside that step's precise statement.

## 3. Why the first eleven observations require a permutation *witness*

The first eleven colors may repeat. Consequently, one cannot calculate the sign of the position rearrangement from a purported permutation of colors; colors are not unique tokens. Instead represent the (i)-th observed color by the distinct observation-slot label (i \in \{0,\ldots,10\}). For observed colors (c_i), order slots lexicographically by ((c_i,i)). Equal colors are therefore stable under sorting, and the resulting ordered slot list is a permutation of the eleven **distinct** input indices.

In `formal/029/EdgeSorting.lean`, the deterministic `elevenStableSlotOrder` constructs this position order, while `eleven_stable_slot_order_perm` and `eleven_stable_slot_order_certified` connect it to a bounded sequence of adjacent position swaps. The underlying lemmas `eleven_slot_reordering_has_parity_witness` and `eleven_slot_colors_follow_position_witness` show that the same swap trace, when applied to the **possibly repeated** color replies, produces the color sequence selected by the position order. The number of adjacent swaps modulo two equals the inversion parity of the unique slot order. The decomposition-independent and relabeling-covariant parity lemmas do not require enumerating eleven-factorial possible orders.

The edge-piece relabeling contributed by a color automorphism (g) has a separate sign character `induced_edge_sign_is_three_pair_sign`; in the mathematical model the combined correction is the mod-two sum of the position-sort sign and this induced piece sign. **Pending:** a Lean proof that the actual source-level `route_info` choice of color gauge and stable sorting realizes that correction for every legal *ordered* initial transcript. The verified position witness alone does not solve the full cocycle.

## 4. Normalizing without an information leak

The controller has exactly eleven initial edge colors and their coincident eleven corner colors when it chooses a representative continuation. A valid normalized policy must therefore implement the following causal order:

1. Collect the eleven paired replies in their true order.
2. Determine the feasible histogram and select **one deterministic** opposite-pair-preserving color map; retain the map, inverse map and actual stable position order.
3. Select the matching frozen eight-read representative decision tree. Translate each representative edge query back to its original position and sticker side *before* reading the reply. Keep the real scheduled corner address coupled to the same charged frame.
4. Continue for eight actual frames even if the edge tree reaches an early singleton; any padding reads remain charged so the corner schedule completes.
5. Only after the final paired response, use the truly observed corner-color transcript and the retained normalization gauge to determine the legal terminal sign and decode the original cubies. Never use this terminal sign to choose an earlier query.

The 24 representative histogram orbits admitting opposite correction signs under stabilizer changes demonstrate why step 2 must retain a concrete normalization witness. The signed count 80 (not the preliminary label-only count 94) is a diagnostic of this issue, not a number of independent physical sensor strategies.

## 5. Proof obligations as a manuscript-to-Lean contract

**Gate A — total prefix normalizer.** Prove that `elevenStableSlotOrder` is lexicographically sorted on the actual eleven replies, with deterministic tie handling; prove that a total selector maps each feasible ordered first-color transcript to one of the 52 pinned representative sectors with the precise color map and position order stored. Invalid histories must fail closed; reachable ones must not.

**Gate B — semantic posterior transport.** Given the retained gauge, prove a bijection between each source state's posterior fiber after any observed continuation and the correctly signed representative posterior fiber. Query and response adapters must commute at every actual paired address, not merely preserve the number of candidates.

**Gate C — certificate reflection.** Connect each parsed frozen continuation tree to a statewise-valid Lean decision-policy graph on every feasible branch; make the exact dependence on the pinned executable certificate and any `native_decide` axioms visible. A generic parser theorem with a conditional `StatewiseSectorValid` hypothesis does not discharge this gate.

**Gate D — corner-timed sign and identification.** Show that the final sign supplied to the representative decoder is determined by the nineteen actual corner responses plus legal initial-state constraints and the retained gauge. Show full original-state recovery, not merely one edge candidate per externally provided sign.

**Gate E — total physical theorem.** Assemble Gates A–D into one `Fits 19` total abstract paired policy, then instantiate `physical_nineteen_of_abstract`. Only this completes the unconditional upper claim.

## 6. Architecture of the final paper

**Main text** should contain the sensor model, lower-bound theorem and its finite witness, graph matching support, precise 52-orbit reduction, the 19-observation controller including its causal sign-timing argument, and the exact final physical theorem if and when proved.

**Methods and reproducibility** should expose the pinned Lean version and module build, the frozen certificate digests, the independent Python verifier as a *cross-language auditor*, the precise theorem-dependency outputs, and the conditions under which the 18/19 claims differ.

**Appendix A: formal semantics.** Reachable cubie states, paired queries, legal turn routing, budget-preserving compiler.

**Appendix B: combinatorial reduction.** Hall inequalities, `K_{2,2,2}` automorphisms, Burnside counting and the distinction between 52 unsigned sectors and 80 corrected signed histogram orbits.

**Appendix C: canonicalization and causal control.** Unique position IDs, stable-sort witness, color gauge cocycle, signed posterior bisimulation, terminal corner-sign timing.

**Appendix D: certificate and independent audit.** Exact 52-root statewise verification, mutation tests, SHA custody, Lean `#print axioms` reports, and publication-grade limitations.

This layout deliberately avoids a chronological list of 0.29 substeps. It makes proof statements and the scientific result—not the project's internal commit sequence—the organizational units.

## 7. Limitations and reviewer questions

The group of color-graph automorphisms is not interchangeable with the subgroup of physical cube rotations; only the proved observation-equivariant actions may be transported. The source's legal edge configurations must be compatible with a legal corner permutation, and the permutation sign may not be treated as a freely observable bit. Stopping a continuation early does not eliminate the remaining charged corner frames. A finite checker accepting fifty-two representatives does not settle all ordered original observation histories until the normalization and response-branch transport is proved. The computational obstruction applies to the exact model stated and should not be sold as an empirical model of human cube-solving expertise.

**Current acceptance verdict:** suitable as a Lean-first draft of the paper's theorem map and conditional upper-bound narrative. Not ready to title an unconditional nineteen-frame formal identification theorem. The next claimed contribution must report its exact kernel-compiled statement and full run commit before upgrading this text.

## AX formal integration update — real charged eleven-frame transcript

The follow-up Lean library `PrefixColorGauge.lean` (added as a mandatory 0.29 build target) instantiates the generic distinct-position stable-sort witness on **the actual edge component of** `abstractPairRead initial` at the eleven scheduled paired addresses. This is stronger than positing an arbitrary eleven-color input as an oracle, because the observation input is now definitionally tied to the frame addresses of the physical compilation model.

In the same module, `observed_first_eleven_corner_clock_exact` identifies the companion corner component of those *same charged frames* with the first eleven entries of `cornerFrameAddresses`. Consequently, sorting edge-slot IDs does not create additional corner observations and cannot reorder when corner colors become available. The time-of-arrival of the final distinguishing corner reply remains a separate gate.

The library establishes the correspondence between actual original-coordinate paired responses, the deterministic eleven-position normalizer and the exact corner-clock prefix. It does not establish the total 48-gauge selector, the 52-root statewise normalized-policy transport or the unconditional physical nineteen-frame upper theorem. Its precise statement and dependencies must be attached to the first successful **post-AX** pinned Lean CI rather than an earlier passing run.

## AY result: canonical order as a mathematical object (formal proof pending full-run seal)

The first-eleven normalizer should not be described merely as a stable sorting *procedure*. It constructs a canonical permutation `σ(c)` of eleven distinct slot IDs from a response vector `c`, and two independent properties must be established:

1. **Well-defined and permutation-preserving:** each original slot occurs exactly once, independently of repeated colors. This is `eleven_stable_slot_order_perm`.
2. **Order-correct:** any two slot IDs `i`, `j` appearing in the output in that order satisfy the lexicographic relation `(cᵢ, i) ≤_lex (cⱼ, j)`. The new `eleven_stable_slot_order_sorted` is explicitly a `List.Pairwise` claim for every observation function `colorAt : Nat → Nat`, using a transitive, total boolean comparator `elevenSlotLexLE`; it invokes the Lean core `List.pairwise_mergeSort` theorem. This is stronger than a fixed 52-sector numerical test, but it does not imply any posterior or physical-policy correctness.

The comparator is `elevenSlotLexLE c i j := decide (c i < c j ∨ (c i = c j ∧ i ≤ j))`. A separate source theorem `eleven_slot_lex_matches_prior_comparator` proves equality with the earlier branch-based comparator, avoiding an unreviewed change of canonicalization semantics. The new theorem is in [`formal/029/EdgeSorting.lean`](../../formal/029/EdgeSorting.lean), introduced in [AY source commit](https://github.com/WhoSia/CUBE-REV/commit/c57c29518c6f29816633c1d95a7faa5472ec80bc). It must not be reported as *verified by CI* until the exact-commit Lean run completes successfully.

### Why this belongs in the main text, not only a machine appendix

The 52-sector compression acts on *histograms*, while the adaptive controller receives an *ordered* eleven-color word. Passing from that word to a representative requires an order-sensitive, evidence-preserving map. Otherwise, two histories with the same histogram may be identified while carrying different permutation-parity corrections. We should therefore present the slot-ID canonicalization lemma before the signed policy transport theorem in the mathematics section. The proof implementation belongs in the Lean appendix, but the proposition and its role in maintaining the observation model should appear in the main text.

The precise scientific dependency is:

```text
ordered 11 real paired responses
    │ (first half of each charged pair)
    ▼
unique slot IDs + deterministic lex comparator
    │  [Pairwise order, permutation, swap-trace parity]
    ▼
color automorphism gauge choice — NOT YET TOTALIZED
    │  [signed gauge cocycle: proof still open]
    ▼
52 frozen representatives + statewise eight-read transport — OPEN
    │  [terminal sign from actual corner transcript: OPEN]
    ▼
one total abstract Fits 19 paired-policy — OPEN
    │  [physical compiler: conditionally proved]
    ▼
fixed-probe physical 19-frame identification — OPEN
```

**Referee-proof claim boundary:** the proposition is *not* that every arbitrary color string is physically feasible. It is that the normalization function and its sortedness proof are total on all strings, a stronger purely algorithmic statement. Feasibility and coverage of the 52 stored decision sectors are separate, cube-specific obligations.

## AZ: a proof-carrying transcript-selected color gauge

The next mechanical obligation is not to enumerate another search tree. It is to turn the color-automorphism choice, previously implicit in Python's histogram canonicalizer, into a *typed value whose legitimacy is checked by Lean* and whose input consists solely of the actual first eleven paired replies.

In [`PrefixColorGauge.lean`](../../formal/029/PrefixColorGauge.lean), `prefixGaugeHistogram` computes the six-color multiplicities of a candidate relabeling. `choosePrefixGauge` folds over the 48 verified opposite-pair-preserving automorphisms, compares their candidate histogram score under the same `Nineteen.lexLess` relation used in the frozen-root quotient, and carries each candidate as the subtype `{sigma : List Nat // sigma ∈ Nineteen.symmetries}`. The identity table is the proven valid fallback. This ensures that every selected table belongs to the actual allowed family, even for arbitrary or non-reachable input replies. The selector is *causal*: its input is an already received `List FrameColor`; the generic `Policy.withPrefix` only calls a continuation after all eleven paired frames have returned.

The theorems `chosen_prefix_color_map_legal`, `chosen_prefix_gauge_edge_equivariant`, and `chosen_prefix_gauge_even_flip_offset` specialize earlier kernel-checked finite symmetry results to the *particular* table chosen from the transcript. Thus the future representative query adapter may receive a legal response relabeling without treating it as an unverified user-provided parameter.

**Remaining precise obligations:** this fold computes a deterministic best candidate under its executable comparator, but no new Lean theorem here yet states the global least-histogram property or proves all feasible histograms map into the **exact** 52 frozen representative certificate keys. It likewise does not yet prove that the selected symmetry and eleven-slot position order jointly reproduce the signed `route_info` correction for every ordered prefix; the selected symmetry must remain available to the representative-to-original output decoder. Finally the corner-derived terminal sign is not available as an extra reply bit.

A future main-text theorem statement can be organized as:

> *Prefix normal form, under proved coverage:* For each reachable first-eleven paired transcript, the deterministic slot-order witness and a selected valid color-table witness produce a frozen-root representative sector with a computable correction bit. A statewise transcript-preserving continuation compiled from the frozen root identifies every original legal cube using exactly eight additional paired reads.

The italicized **coverage, correction, and statewise** clauses are still proof obligations, not results being asserted now. The source-change evidence for the legal-gauge bridge is [AZ implementation](https://github.com/WhoSia/CUBE-REV/commit/2df3741c0e2da141ffb166f94c9b5229f669bd6d) and [namespace qualification fix](https://github.com/WhoSia/CUBE-REV/commit/b8b7bef79f854b7b094670cc4a286f8b9e69c178). Cite the corresponding completed CI rather than these commits alone when describing the theorems as compiled.

## AZ selected-gauge inversion theorem: evidence, scope and integration gate

The representative decoder previously accepted a *chosen* legal color symmetry and an invertible permutation of twelve edge slots as parameters. The exact selected gauge is now computed from eleven already received paired replies and carries a proof that it belongs to the approved 48-element family. The following new source statements specialize the earlier general inversion results to **that exact selected gauge**:

- `chosen_prefix_gauge_inverse_is_legal`: the table inverse lies in the same opposite-pair-preserving family.
- `chosen_prefix_gauge_restores_oriented_edge`: applying the selected color map and then its inverse restores every oriented edge identity, including the sticker side, without assuming a particular scramble.
- `chosen_gauge_original_state_round_trip`: after coupling the selected map with any verified `EdgeSlotOrder` bijection on twelve positions, encode→decode returns precisely the initial paired cubie-and-corner state.

The proof uses the actual previous kernel statements `inverse_color_table_is_symmetry`, `inverse_color_table_restores_oriented_edge` and `representative_pair_state_round_trip`. It is not a restatement of certificate output counts or a newly assumed parity oracle. Source: [AZ inverse implementation](https://github.com/WhoSia/CUBE-REV/commit/238f653be9653e658b4664b2674a9b78eff4f1b5).

**Important remaining dependency:** the `EdgeSlotOrder` hypothesis is a full 12-slot permutation, whereas the preceding observed stable sort covers eleven slots. Constructing the last-slot-fixed extension, proving its inverse, and proving agreement with the Python `route_info` choice for *all* feasible ordered histories must precede a total 52-root policy transport. Having a round-trip theorem for a **supplied** 12-slot bijection does not supply the bijection. Moreover, a bijective decoder cannot establish that the certificate's representative policy produces the correct normalized output or that the true terminal sign is derivable by the 19th paired corner reply.

The manuscript should place this result under **correctness of coordinate adapters**, before the final policy theorem. The exact Lean workflow SHA and complete outcome, rather than an earlier passing run, are mandatory before claiming compilation acceptance.

## AZ route_info-order correction: the vital distinction between raw and normalized color ranks

**Identified mismatch and repair.** The old `prefixTranscriptStableOrder` is a mathematically correct canonicalization of eleven *original-code* colors. It is **not** the position permutation used by the published certificate's Python `route_info`, which sorts the *gauge-transformed* replies in the frozen `URFDLB` collation order. The Lean internal color codes are ordered `BDFLRU`. Even an entirely valid `List.Pairwise` proof for the old comparator would not justify substituting its parity into the certificate's signed terminal decoder.

The revised formal interface therefore distinguishes three objects:

1. `chosenPrefixColorMap transcript`: one 48-family color automorphism selected deterministically from the received eleven paired responses, using the Python-compatible first-minimum tie rule;
2. `frozenPrefixStableOrder transcript`: the stable permutation of eleven unique position IDs under the ranks `Nineteen.collation.idxOf ((chosen map)[observed color]!)`, which is the **transformed URFDLB** ordering used in `route_info`;
3. `frozenPrefixSignCorrection transcript`: the sum modulo two of the *actual transformed eleven-position order's* inversion parity and the selected color automorphism's induced twelve-edge-label parity.

Lean proves the new position order is a permutation and lexicographically sorted under the transformed comparator and admits a parity-correct adjacent-swap witness. A concrete tied-gauge adversarial transcript `[U,U,R,R,R,R,L,L,L,B,B]` is expected to give the selected table `[3,5,4,2,0,1]` (indexed by internal color code) and corrected position order `[6,7,8,0,1,9,10,2,3,4,5]`. The executable expectation is captured by `frozen_tie_probe_has_transformed_stable_order`; the earlier tie-map theorem remains a separate check.

The theorem `frozen_prefix_sign_correction_three_pair` identifies the correction using either the induced permutation on all twelve edge types or the induced permutation on three opposite-color blocks, via the earlier `induced_edge_sign_is_three_pair_sign` character identity. The correction depends on **past observed colors and chosen gauge only**, not a free corner-parity oracle.

**Status and limitations:** Source changes [bec6079](https://github.com/WhoSia/CUBE-REV/commit/bec60795ccdada01b22d0f50adaf67f46521e225) and [ae7b05f](https://github.com/WhoSia/CUBE-REV/commit/ae7b05f5d1ea2a48b57add62f50cfa747fee93be) must pass their exact-commit Lean CI before formal acceptance. The list-based output still requires a verified extension to the complete twelve-edge `EdgeSlotOrder` and a proof that the actual 52 frozen branches are transported without loss for every feasible ordered transcript. We are repairing the normalization *definition* rather than announcing the entire 19-frame upper-bound proof.

## BA — Twelve-slot trace parity and a constructive inverse coordinate adapter

The crucial difference between the eleven colors acquired in the fixed prefix and the twelve *positions* of the physical edge array is no longer relegated to an informal “append the unread edge” remark. The [Lean position-sort library](../../formal/029/EdgeSorting.lean) now introduces `eleven_slot_trace_full_twelve_parity` for an arbitrary observation-color function. It asserts the existence of an in-bounds adjacent-transposition trace that takes the full twelve-slot identity order to the actual sorted eleven-position order **followed by the unchanged twelfth slot**, and establishes that the trace-length parity agrees with the full twelve-position inversion parity and the original eleven-position parity. The theorem is a universal swap/position statement: it does not assume that the input color history is physically realizable, nor that the unread edge color has been observed.

The existing `frozenPrefixStableOrder` computes the eleven-slot order on **gauge-transformed** colors ranked by the frozen `URFDLB` collation, rather than directly on their internal `BDFLRU` codes. The additional `frozen_prefix_sign_correction_full_twelve_trace` is intended to strengthen the parity bridge by stating, for each actual received prefix transcript, that the frozen combined correction is exactly

\[
\epsilon(\mathrm{prefix}) =
\Big(\lvert T\rvert + \operatorname{sgn}(\sigma_{\mathrm{pairs}})\Big)\bmod 2,
\]

where `T` is a bounded trace of **real permutations of the twelve positions**, with the twelfth unobserved position fixed, and `σ_pairs` is the induced permutation of the three opposite-color pairs. Neither term is an uncharged observation.

A separate addition to [RepresentativeRoundTrip.lean](../../formal/029/RepresentativeRoundTrip.lean), `slotOrderFromAdjacentTrace`, composes actual bijective adjacent transpositions on `Fin 12` and takes its inverse from the resulting `Equiv`, thereby **constructing** the explicit `EdgeSlotOrder` fields and inverse proofs instead of accepting a pair of unverified functions. This is a concrete architectural advance toward replacing an abstract supplied order. However, a further compatibility theorem is still needed to prove that this `Fin 12` coordinate permutation is pointwise equal to the output-index pullback of the list-sorting trace, as well as the exact frozen `route_info` slot adapter. Constructing a bijection is not by itself proof of *which* bijection the frozen policy uses.

**Proof acceptance and disclosure.** The new BA statements must be accepted only after the exact-source Lean CI run (including `#print axioms`) succeeds. The generic theorems are separate from the intentionally disclosed `native_decide` dependence in one concrete merge-sort tie fixture, and neither resolves the statewise reflection of all 52 frozen trees or the terminal corner sign.

### BA reviewer-facing theorem hierarchy

| Paper component | Lean interface | Remaining integration assumption |
| --- | --- | --- |
| Collision-safe canonicalization | `eleven_stable_slot_order_perm`, `eleven_stable_slot_order_sorted` | None about physical feasibility; applies to all color words |
| Position sign on twelve slots | `eleven_slot_trace_full_twelve_parity` | Requires a verified full permutation-to-position-index correspondence before policy application |
| Chosen frozen color gauge and sign character | `chosen_prefix_color_map_legal`, `chosen_prefix_gauge_sign_character` | Exact first-minimum tie rule and sector coverage, audited independently |
| Signed correction | `frozen_prefix_sign_correction_full_twelve_trace` | Full original-state signed posterior bisimulation |
| Inverse-capable position adapter | `slotOrderFromAdjacentTrace` | Show the adapter implements *this* stable trace and frozen source query translations |
| Policy transport | `chosen_gauge_paired_transport_run` | Every 52-sector tree valid on all reachable posterior states, terminal sign obtained from observed corner clock |

An eventual headline theorem must combine these with one `Fits 19` abstract policy before applying the already established physical-route compiler. These BA results narrow and clarify the handoff but are **not** an unconditional nineteen-frame identification theorem.

## BB — Pointwise semantics of the twelve-slot coordinate adapter

A finite bijection of twelve slot indices is insufficient evidence for a correct adaptive probe translator: the policy must select the original slot containing the *representative slot's actual edge*. We therefore require an equality of two operations, not merely two abstract bijections. For every list `xs` of length twelve, every trace `T` in which each swap index is strictly below eleven, and each `j : Fin 12`, the required formula is

\[
\big(\operatorname{adjTrace}(T,xs)\big)[j]?
 =
 xs\big[\operatorname{slotOrderFromAdjacentTrace}(T).\mathrm{forward}(j)\big]?.
\]

The question mark denotes the Lean optional list lookup. Crucially, the statement **does not require the elements of `xs` to be distinct**. The original measured color string repeats, whereas its *position IDs* are unique. The proof may use the independently kernel-proved `get_adjacent` lemma for a single adjacent swap and induction over the bounded trace, with the index composition arranged in output-to-input order.

The new [source commit](https://github.com/WhoSia/CUBE-REV/commit/e2b094c6f6bff781e791367519b6037eaa833d78) introduces two propositions in `RepresentativeRoundTrip.lean`: `adjacent_twelve_index_matches_list` identifies the concrete `Fin 12` index transposition with the list-level `adjIndex`, and `slot_order_trace_getElem?` states the universal pointwise transport formula above. These are **pending Lean CI acceptance** until the exact revision compiles and its `#print axioms` receipts are inspected.

If accepted, the result closes the *index-semantics* gap exposed in BA: `EdgeSlotOrder` is not simply invertible; its forward direction is precisely the lookup pullback of the actual list rearrangement. With `eleven_slot_trace_fixes_unread_twelfth` and `eleven_slot_trace_full_twelve_parity`, the reader can then audit both the positional meaning and the sign of the same trace.

**Remaining requirements even after pointwise acceptance:** connect the trace witness to the selected frozen source `route_info` ordering in a deterministic executable selector (rather than only an existential path), show full signed posterior commutation across all actual charged query/response branches, prove the fifty-two frozen root policies statewise on every reachable history, and infer the terminal sign from the actual nineteen corner responses. This section does not declare a total physical nineteen-frame theorem.

### BB verified acceptance — full twelve-slot adapter

The two separate Lean verification gates have now **completed successfully**. [Run #44933058857, attempt 2](https://github.com/WhoSia/CUBE-REV/actions/runs/44933058857) verified the generic, element-type-polymorphic pointwise pullback `slot_order_trace_getElem?` (source [e2b094c](https://github.com/WhoSia/CUBE-REV/commit/e2b094c6f6bff781e791367519b6037eaa833d78)). [Run #44933735143](https://github.com/WhoSia/CUBE-REV/actions/runs/44933735143) verified the next compiled source [b505afc](https://github.com/WhoSia/CUBE-REV/commit/b505afcfb2b0e715a03a030c2bfb8944527f75f1), which joins this pointwise equivalence to the actual response-dependent frozen normalization and the exact full twelve-position sign correction as `frozen_prefix_has_semantic_twelve_slot_adapter`. This second theorem returns a bounded `path` and a genuine `EdgeSlotOrder` with `order = slotOrderFromAdjacentTrace path`, verifies the list-index correspondence for **all** `Fin 12` output positions, and reports the inherited color-pair parity correction.

The printed axioms for both `slot_order_trace_getElem?` and `frozen_prefix_has_semantic_twelve_slot_adapter` are exactly `[propext, Classical.choice, Quot.sound]`; neither includes `sorryAx` nor an added native computation dependency. This acceptance is **about these specific theorems**, not a proof that the frozen policy is a total state-identifying 19-frame controller. A concrete *executable* trace selector, an explicit statewise link from this chosen adapter to all frozen eight-read tree branches, and terminal corner-derived sign correctness remain the next principal proof targets.

## BC — The unread twelfth edge is fixed in both coordinate directions

The first eleven edge-color observations do not measure the twelfth original edge slot. It is therefore not enough to prove that the sorting trace `T` rearranges eleven labels correctly and that its extension on twelve labels has even or odd parity as expected. The eventual query decoder must preserve the **unread twelfth address itself** under the forward original-to-representative pullback and under the inverse decoder.

Let `O(T)` denote the concrete, invertible twelve-slot adapter `slotOrderFromAdjacentTrace T`. Whenever every adjacent-swap index in `T` is strictly less than ten, the precise additional claims are

\[
O(T).\mathrm{forward}(11)=11,\qquad
O(T).\mathrm{backward}(11)=11.
\]

This is a statement about the *position maps*, not the colors at those positions. It holds independently of reachability and of any repeated stickers; it cannot make the unknown twelfth edge observable. The intended Lean theorems `adjacent_twelve_index_fixes_unread`, `slot_order_bounded_trace_fixes_unread`, and `slot_order_bounded_trace_inverse_fixes_unread` live in [`RepresentativeRoundTrip.lean`](../../formal/029/RepresentativeRoundTrip.lean). In particular, the inverse claim should be obtained via the verified `right_inv` property at position eleven, not by assuming a new permutation symmetry.

The initial BC implementation surfaced a faulty direction of equality rewriting in the inverse proof. [Source correction](https://github.com/WhoSia/CUBE-REV/commit/e9ee320f9c7841cb566dbe83f155a4af9779a278) changes only the proof, using `right_inv` of the constructed adapter. The theorem acceptance label must follow an exact post-correction Lean run, not the earlier failing CI. Treat every new theorem as **unverified until its corresponding CI succeeds**, and keep the 19-frame upper theorem open independently.

### BC follow-up: computational witness versus existential witness

BB already gives a proof-carrying existential trace for each actual frozen prefix transcript. This provides formal existence, a bounded-path condition and precise pointwise query semantics, but it **does not yet supply a computable, deterministic trace-producing program**. A deployable continuation cannot execute an arbitrary noncomputable witness extracted from a proposition in Lean. The next constructive milestone is an executable sorter that records the concrete adjacent swaps as data, with a proof that (i) each recorded swap is bounded, (ii) replay produces the selected stable permutation, and (iii) the resulting `EdgeSlotOrder` gives the same adapter and parity. The signed 52-sector posterior and terminal corner-time obligations remain subsequent gates.

## Source and version anchors

- [CUBE-REV 0.29 formal package](../../formal/029/README.md).
- [Physical abstract-to-real compiler](../../formal/029/PhysicalPolicyCompiler.lean).
- [Unique eleven-slot stable normalization](../../formal/029/EdgeSorting.lean).
- [Certified corner clock](../../formal/029/PairedCornerClock.lean).
- [Fifty-two-root certificate reflection](../../formal/029/FiftyTwoRootReceipt.lean).
- [Signed sector decoding](../../formal/029/SignedTerminalIdentification.lean).
- [AX exact-byte retirement custody ledger](../../docs/0.29/20261122_AX_LEAN_FIRST_RETIREMENT_LEDGER.md).
- [Latest full Lean verification before AX](https://github.com/WhoSia/CUBE-REV/actions/runs/44925506967).

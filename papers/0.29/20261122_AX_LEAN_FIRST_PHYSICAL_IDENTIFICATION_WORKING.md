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

## Source and version anchors

- [CUBE-REV 0.29 formal package](../../formal/029/README.md).
- [Physical abstract-to-real compiler](../../formal/029/PhysicalPolicyCompiler.lean).
- [Unique eleven-slot stable normalization](../../formal/029/EdgeSorting.lean).
- [Certified corner clock](../../formal/029/PairedCornerClock.lean).
- [Fifty-two-root certificate reflection](../../formal/029/FiftyTwoRootReceipt.lean).
- [Signed sector decoding](../../formal/029/SignedTerminalIdentification.lean).
- [AX exact-byte retirement custody ledger](../../docs/0.29/20261122_AX_LEAN_FIRST_RETIREMENT_LEDGER.md).
- [Latest full Lean verification before AX](https://github.com/WhoSia/CUBE-REV/actions/runs/44925506967).

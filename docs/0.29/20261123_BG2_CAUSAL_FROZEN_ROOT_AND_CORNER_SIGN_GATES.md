# CUBE-REV 43 / BG2 — Concrete Causal Handoff Between Frozen Roots and Paired Physical Answers

Date: 2026-11-23. Parent evidence: `52d26dd`, plus BG LIRA ledger. **Status: proof-obligation refinement only; no Lean build or new global identification theorem.**

## Verified-by-source interface map

| Stage | Existing exact symbol | Proven/computed scope | Missing bridge |
| --- | --- | --- | --- |
| 52-root receipt | `FiftyTwoRootReceipt.every_actual_frozen_root_recovers` | A parsed representative entry in the immutable source has a correct eight-read signed decoder on its parsed belief | Every physically reachable original eleven-response history selects a matching entry **after** the selected gauge and slot-order normalization |
| Actual root matcher | `TaggedNineteenRootPolicy.matchingFrozenRoot` | `find?` matches the **literal ordered eleven answer list** against each JSON entry's `rootFirstColors` | It does not call `chosenPrefixColorMap`, `verifiedFrozenPrefixTrace?`, or any signed original-to-representative encoder |
| Fallback behavior | `TaggedNineteenRootPolicy.continuationFromFrozenRoots` | No match or parser error yields `.stop (fun _ => none)` | `Fits 8` remains true even when every such fallback fails to identify the cube |
| Conditional recovery | `TaggedNineteenRootPolicy.exact_nineteen_tagged_recovers_matching_actual_root` | Given `selected`, `entryParsed`, and `candidate`, produces `some word` for the correct supplied sign | Discharge `selected` and `candidate` from actual original state and past responses, not assumptions |
| Paired clock | `PairedCornerClock.withCornerClock_run` | Edge policy ignores returned corner color for its branching; all scheduled paired reads remain charged | Interpret the final returned corner colors to *compute* the terminal sign |
| Corner agreement | `PairedCornerClock.same_paired_corner_colors_force_all_legal_corners` | Equal nineteen actual corner replies imply equal legal original corner colorings | Supply a constructive corner-state decoder and proof that its derived permutation parity equals the edge sign after combined correction |
| Adaptive signed transcript | `SignedPolicyTranscript.transported_signed_policy_transcript_exact` | For an explicitly chosen symmetry, order, and correction, true replies agree with the transported representative tree at every branch | Establish that these parameters are determined by the *first eleven already acquired replies*, and agree exactly with the frozen `route_info` representation |

## A. Concrete root mismatch gate

`matchingFrozenRoot roots answers` is an exact `find?` over `rootFirstColors` equal to `some answers`. The abstract 52-orbit count is about normalization orbits, **not** 52 literal first-eleven sequences. Therefore this selector alone cannot be offered as a global total continuation for all original legal cube states.

The minimum proposed integration interface should explicitly construct:
```text
original ordered prefix h
  -> chosen URFDLB color gauge g(h)
  -> verified original-slot stable normalization o(h)
  -> normalized ordered representative prefix r(h)
  -> actual matchingFrozenRoot roots r(h) = some entry
  -> parseRepresentativeRoot entry = ok (graph, belief)
  -> encode(g(h), o(h), originalState) in belief
```
Each arrow needs its own proof, exact input type, and failure gate. Source documents reporting 52 histogram orbits do not certify the implication for every *ordered* original history. A counterexample in the matcher fallback path is an immediate failure, even if the resulting policy still satisfies the cost bound.

## B. Sign is not a sensor

The signed leaf computes `Bool → Option Word`; the Bool is an **output decoder parameter**, not a field returned by `taggedPairedObserve`. Source `docs/0.29/20261121_AR12_SIGNED_SINGLETON_AND_NO_PARITY_ORACLE.md` proves the essential negative control: an independent unobserved sign bit cannot be inferred from any paired sticker policy.

The nineteen-frame proof therefore needs a total function on the **actual completed paired transcript** (or a fully reconstructed original corner coloring derived from it), not on the hidden state:
```text
actual paired answers at frames 1..19
  -> reconstruct original corner coloring (on Reachable states)
  -> compute physical corner permutation sign
  -> apply exact frozen position+gauge sign correction
  -> supply resulting sign to edge terminal decoder
  -> invert representative encoding to the original edge state
```
The applicable correction is **both** position-sort parity and induced color-edge relabeling parity, per `papers/0.29/20261121_AP_SIGN_COCYCLE_REVIEWER_APPENDIX.md`. The simplified label-only action was previously shown to count 94 signed orbits versus 80 under the combined action; treating the two as interchangeable would change the theorem's mathematical model.

## C. Explicit Lean-facing obligations (do not assert these as theorems)

**BG2-A (normalization totality on reachable prefixes):**
For any reachable state, processing its first eleven real paired replies yields a selected legal gauge, certified bounded order, and normalized prefix that matches a parseable frozen root.

**BG2-B (initial posterior alignment):**
For every state producing that prefix, the signed representative encoding belongs to the selected root's exactly parsed belief. Stronger bidirectional equality is desirable, as membership alone may hide too-small or inconsistent beliefs.

**BG2-C (all-history equivariance):**
For every feasible continuation branch, the original physical pair responses map through the chosen *past-fixed* gauge and slot-order to exactly the representative response consumed by the certified eight-read tree.

**BG2-D (corner information release at frame 19):**
The observable terminal sign function depends only on completed paired observations, equals the physically required sign on every reachable state, and uses no future answer or hidden sign state. It must not become available on an early-stop path before the remaining reads are charged.

**BG2-E (original identification):**
The signed decoder output and completed corner reconstruction recover the precise original reachable coloring, not merely a representative edge word or an equivalence class.

**BG2-F (budget and routing):**
Concatenate eleven charged first paired observations with exactly eight charged continuation observations; then instantiate the existing abstract-to-physical compiler without adding a free sensor or free observation.

## D. LIRA/JEV mini-decision for next isolated work

| ID | Decision | E | C | G | L | Verdict |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| BG2-01 | Treat current literal root matcher as a total original-state selector | .890 evidence *against* adoption | .080 support for adoption | .050 | .950 urgency of replacing assumption | REJECT as currently phrased |
| BG2-02 | Prove explicit normalized-history-to-root membership interface | .455 | .300 | .180 | .853 | P0 / HOLD until theorem |
| BG2-03 | Construct a causal terminal sign from completed corner transcript | .505 | .350 | .240 | .870 | P0 / HOLD until theorem |
| BG2-04 | Declare unconditional physical `Fits 19` from existing conditional results | .900 evidence that prerequisites are missing | .050 support for declaration | .050 | .120 recommendation to publish claim | REJECT |

**Interpretation:** BG2-01's E measures the strength of the *counterargument* (the code explicitly has a fallback), while its C measures support for the proposed adoption. E must not be conflated with C or reported as supporting the invalid claim. BG2-04 similarly distinguishes the strength of blocker evidence from support for publication.

**Independent review needed:** a second researcher should assess the judgment inputs and assess whether any existing theorem already closes BG2-A through BG2-E. If so, change this ledger and provide the exact theorem, revision, and full CI receipt.

## E. Collaboration and commit hygiene

Claude owns `EdgeSorting.lean`; GPT-6 edits only these independent documents and future non-overlapping causal integration modules. The only active research branch is `research/current`. No force push, no bot authors or committers, no migration of `main`, and no source deletion without archival byte verification.

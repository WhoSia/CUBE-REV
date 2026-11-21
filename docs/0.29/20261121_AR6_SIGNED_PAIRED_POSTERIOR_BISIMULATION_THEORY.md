# CUBE-REV 0.29 AR6 — Signed paired-color posterior bisimulation: theorem ledger and open cube instantiations

**2026-11-21 · research/current · mathematical proof unit.**

## Result and quantifiers

For the continuation of a physically legal 3×3×3 cube identification procedure after its first eleven one-sided edge observations, the normalization witness consists of: a color graph automorphism (g) from the 48-element (K_{2,2,2}) automorphism group, a *proved-invertible* 12-slot edge position order (eta) that fixes the 12th slot, and a parity-correction bit (epsilon) computed from previously received colors. The witness must be chosen before any of the remaining paired-color replies become available.

Write the original source state as a full oriented 12-edge arrangement and 24 corner facelet colors, **plus a formal parity tag** (p). The representative mapping sends
[
  ((e,c),p)longmapsto ((g(e\circ\beta),c),\ p\oplus\epsilon).
]
This is a mathematical *tagged-state extension*. The parity tag is not an extra physically observable field: one actual frame returns precisely one edge and one corner color. Its eventual identification with the corner permutation parity is a separate physical-legality theorem.

The structural theorem completed in source form in `SignedRepresentativePolicy.lean` and `SignedPairedPosterior.lean` asserts **conditionally on the fixed witness**:

1. **Exact round trip:** decoder applied to the encoded signed state equals the same original tagged state. It needs a genuine inverse slot order, an inverse color table and the same correction bit on both sides.
2. **Response covariance:** the representative's paired reply equals the real physical paired reply after relabeling only the edge color, at the original-coordinate query pulled back by (eta). The bit is not a readout.
3. **One-step posterior equality:** the image of an original posterior fiber under the signed encoder equals the representative posterior fiber at the same transformed address/reply.
4. **Arbitrary finite ordered histories:** for every `history : List (PairedAddress12 × PairedReply12)`, the entire remaining posterior set after that exact causal query-and-reply transcript commutes with signed transport. This is not just matching belief cardinalities, histograms, or policy DAG node counts.
5. **No ambiguity collapse:** encoding is injective, so distinct signed original states in a belief cannot merge into one representative state. This is essential when testing the last parity bit.
6. **Exact policy-budget transport:** any policy of at most (k) paired reads that is certified to recover the signed representative state on every normalized admissible original state can be transported to a physical-address policy of at most (k) reads that recovers the tagged original state.

The all-history theorem is a list induction after the exact one-step fiber identity. The policy transport relies on `Policy.adapt`, `Policy.adapt_fits` and `transport_certified_policy`; its query address is fixed before the current response is available. It is therefore a theorem about feedback decision trees, **not** a post-hoc relabeling of a final cube permutation.

## Why the order of logical quantifiers is decisive

The formal statements quantify over all original tagged states, all admissible original belief predicates, all paired original-coordinate query/reply histories, and all fixed normalization triples ((g,eta,epsilon)) satisfying the explicit color and inverse hypotheses. **They do not assert that an arbitrary normalization triple works as the correct *physical* parity correction**: (epsilon) is supplied as a parameter.

For the 19-frame upper-bound target the quantifier order must be:

- first receive the eleven past edge-color answers, with their actual ordered original sticker indices;
- choose (g,eta,epsilon) **deterministically from that observed history alone**;
- prove the chosen color map is valid, the sorting map invertible and the parity correction equals the true composition sign;
- only then run the remaining at most eight paired queries using the fixed witness.

Permitting (epsilon) to depend on the *terminal* physical corner sign, or choosing (g) after seeing the continuation response, would be an invalid clairvoyant policy.

## Signed parity is not an independent physical oracle

For an actual legal cube the edge and corner permutation signs coincide. The formal tag (p) must be constrained by a proved proposition such as
[
   p=\operatorname{parity}(\text{original edge cubie permutation})
     =\operatorname{parity}(\text{physical corner cubie permutation}).
]
Until the corner read schedule is sufficient, an unconstrained tag would create two entirely indistinguishable formal states; no sensor could identify it by itself. Therefore the tagged-state round trip and exact fiber equalities **do not** prove that the physical model exposes a free terminal sign oracle. The nineteen-frame corner decoder must be composed at precisely its actual final frame.

In particular the earlier 24/52 *gauge-unsafe* histogram orbits require the *combined* stable-sort cocycle (epsilon), not merely the 12-edge type sign character (chi). This is a regression requirement for the eventual policy interpreter.

## Formal evidence, trust and proof-debt table

| File | Theorem unit | Mathematical scope | Still open for the paper |
| --- | --- | --- | --- |
| `ColorGraphCharacter.lean` | `induced_edge_sign_is_three_pair_sign` | Exact 48-element color action; kernel reduction | General theorem for arbitrary 12-edge permutation composition |
| `RepresentativeRoundTrip.lean` | `representative_pair_state_round_trip` | Explicit invertible slot order and exact 24-value edge/corner inverse | Link deterministic sorting function from actual observed prefix to `EdgeSlotOrder` |
| `SignedRepresentativePolicy.lean` | `signed_representative_round_trip`; `signed_original_policy_of_certified_representative` | Fixed ((g,eta,epsilon)) correct output and same budget, **conditional on representative policy** | Supply (epsilon) from observed prefix; certify every representative decision tree |
| `GraphPosteriorCovariance.lean` | `transported_posterior_covariance` | General posterior image/pullback algebra | Explicit physical signed instantiation |
| `SignedPairedPosterior.lean` | `signed_paired_posterior_one_step`, `signed_paired_posterior_all_histories` | Exact all-history paired reply fibers for fixed witness | Instantiate the changing first-eleven prefix selector and correct terminal candidate semantics |
| `NineteenReadData.lean` | `check` and frozen receipt | 52 trees, 144,736 edge candidates, 141,097 nodes checked with computational certificate | Reify tree in Lean's `Policy` and prove sound `run` for every feasible reply |
| `PhysicalPolicyCompilerFast.lean` | `physical_nineteen_of_abstract_bounded` | Formal implication from abstract 19-recovery policy to physical fixed-sensor policy | Construct the unconditional abstract 19-recovery policy |

The new AR modules have no `sorry`, `admit` or declared nonstandard `axiom`; their **actual compiler and `#print axioms` output**, however, must be inspected from the pinned read-only CI before labeling them kernel checked. Static no-placeholder checks alone are insufficient.

## Referee-attack scenarios

- Replace the selected (epsilon) with the label-only (chi(g)): fails on the 24 gauge-unsafe classes because the stable-sort (eta) parity also matters.
- Replace the original ordered history by its color histogram: the base 52 histogram orbits still exist but no longer establish exact route correspondence or leaf semantics.
- Forget the inverse slot map (eta^{-1}): the encoder/decoder cease to be a general 12-position inverse, independently of matching color counts.
- Append a terminal readout of corner sign as an extra free observation: violates the paired original sensor model unless the fixed nineteen-corner schedule has actually observed enough stickers at that frame.
- Omit the `∀ history` quantifier: a single preselected sensor schedule may look correct while an adaptive response branch breaks.
- Conflate 18-frame impossibility with 19-frame construction: a lower-bound DAG says nothing about the completeness of an upper-bound policy interpreter.

## Next constructive obligation

Build an *actual* normalization witness generator from each of the 1,362 reachable first-color histograms and an ordered eleven-color word, retaining its selected color map and stable sorting permutation. Prove `eps = parity(edge label relabeling) XOR parity(stable sort)` for all such histories, combine that with the physical corner permutation parity theorem, and interpret **all** 52 frozen representative continuation trees as honest `Policy` values. Only then can `Fits 19` and physical recovery be concluded.

**Related scholarship:** Cameron (1999) and Seress (2003) for group actions and stabilizers, McKay–Piperno (2013 preprint) for refinement/canonical labeling, and Leon (1991), Jefferson et al. (2021) for general partition-based permutation search; their methods are not asserted to prove the present physical paired-color Rubik theorem.

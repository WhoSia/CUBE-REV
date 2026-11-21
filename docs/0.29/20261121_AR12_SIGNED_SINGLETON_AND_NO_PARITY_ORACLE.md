# CUBE-REV 0.29 AR12 — Terminal singleton preservation and impossibility of a free parity oracle

**21 November 2026 · Formal research note.**
**Status:** Lean source `SignedTerminalIdentification.lean` and pinned read-only CI verification to be distinguished from the still-open unconditional physical nineteen-frame policy.

## 1. Observation as a function, not an information grant

The original paired Rubik sensor receives exactly the color of one edge sticker and one corner sticker per frame. Its response contains **no independently accessible bit** reporting the edge permutation sign or the corner permutation sign. An implementation may *derive* a sign from previously read enough corner stickers, but a sign coordinate attached to a mathematical state is not itself an extra observation.

To make the boundary explicit, consider the signed extension
```
SignedOriginalState := CubieAndCornerState × Bool
signedRealPairRead ((cube, sign), query) := realPairRead cube query
```
for any edge/corner coloring `cube`. This extension temporarily treats the tag as a free bit, without imposing physical cube legality.

### Theorem 1 — a free parity bit is not observable

For **every** signed-output adaptive decision tree `P` and any fixed cubie/corner coloring `c`,
```
P.run signedRealPairRead (c, false)
  = P.run signedRealPairRead (c, true).
```
*Proof.* At any query address, the two states yield the same paired response, since `signedRealPairRead` ignores the tag. Induction on the decision tree therefore follows the same branch at every step and returns the same output; the result is `Policy.run_fixed_reply_equiv`. □

Consequently no single such policy can be correct on **both** `(c,false)` and `(c,true)` because the two outputs would need to be distinct. This contradiction holds independently of the observation budget: increasing the number of frames cannot recover an *independent, unobservable* parity tag.

**Implication for the nineteen-frame upper bound:** at a two-candidate terminal representative leaf, choosing a candidate by “the physical corner parity bit” is legal **only** after proving that this parity is determined by the corner colors actually observed in the first nineteen frames, using the legal-cube structural constraint. Granting it as an input to the policy would be equivalent to silently adding a new sensor. This simple universal impossibility theorem is an effective negative control on formal policy definitions.

## 2. Correct terminal success is an exactly-one posterior

For a posterior belief predicate `B : S → Prop`, define
```
beliefExactlyOne B :=
  ∃ x, B x ∧ ∀ y, B y → y = x.
```
The leading existential prevents the empty posterior from passing as a successfully identified state. In particular, “at most one candidate per permutation sign” and “exactly one candidate total after incorporating legal corner sign” are **different** predicates.

For a signed normalized state map `T : S → R` with an explicit decoder `D : R → S` satisfying `D(T(x))=x`, an elementary proof yields
```
beliefExactlyOne B ↔ beliefExactlyOne (transportedBelief T B).
```
*Proof (forward).* Given unique `x` in `B`, every member of the image `T(B)` is `T(y)` for some `y∈B`; uniqueness gives `y=x`.

*Proof (reverse).* If `T(B)` has a unique element `T(x)` and `y∈B`, then `T(y)=T(x)`. Apply `D` and `D∘T=id` to obtain `y=x`. Existence is inherited from the explicit image witness. □

Unlike an equality of candidate cardinalities computed by a finite search, this proof is parametrically valid for **any** state sets and beliefs with a concrete left-inverse transport.

## 3. Terminal singleton equivalence after any ordered paired history

AR1–AR2 prove that, for any eligible fixed color automorphism `g`, any invertible chosen edge slot order `β`, any **past-determined** parity correction `ε`, and any prior belief `B`,
```
  T(B | h) = T(B) | h
```
where the source observation on the left is recoded by the actual query pullback and the reply color map, and the representative observation on the right is the original categorical paired query on normalized states. Both sides retain full **ordered** query-and-answer records `h`, not just eleven-color histograms.

Combining the equality with the general exactly-one image theorem yields
```
beliefExactlyOne (B | h)
  ↔ beliefExactlyOne (T(B) | h).
```
No oracle is supplied by this equivalence. If an abstract representative leaf contains two physically different candidates of opposite permutation signs, it is **not** uniquely identified until the physical corner schedule actually constrains that sign. The formal singleton theorem therefore does not assert that the frozen 52 policy roots have singleton leaves; it states the **condition under which** terminal singleton verification transports back to physical coordinates.

## 4. Referee red-team cases

1. **Trivial incorrect success:** implement “at most one per sign” and accept an empty posterior. Our `beliefExactlyOne` rejects it by requiring a witness.
2. **Free parity oracle:** append an unconstrained Bool to the representation and let the policy branch on it. Theorem 1 proves no paired sticker policy can recover that free tag for both values; the construction would be a different query model.
3. **Wrong stabilizer gauge:** forget the color map selected after the first eleven observed colors. Earlier AR predecessors isolated 24 histogram classes where this can change the combined color-label/stable-sort parity.
4. **Wrong physical corner availability:** apply the terminal parity correction before the actual nineteenth corner observation. This uses information unavailable at the time of query selection and violates the legal adaptive policy model.
5. **Wrong quantifier:** verify one predetermined schedule and infer every feedback continuation. The all-history transport theorem quantifies over every possible ordered list, although it still assumes a fixed prior normalization witness.

## 5. Honest formal boundary and research priority

The new `formal/029/SignedTerminalIdentification.lean` contains four theorems:
- `exactly_one_iff_transported_belief`;
- `signed_terminal_singleton_iff_after_any_history`;
- `unconstrained_parity_tag_is_unobservable`;
- `cannot_recover_an_independent_parity_oracle`.

Formal proof verification is a separate executable gate: the source is registered in Lake and the read-only GitHub workflow and checked for no `sorry`/unapproved `axiom` plus `#print axioms`. Do not write “Lean verified” until the actual remote job reports SUCCESS.

**Next substantive work:** constrain the sign tag by actual legally reachable cube geometry (edge permutation parity equals corner permutation parity), reify all 52 eight-read trees with exact feasible reply support and terminal outputs, and prove the nineteen-corner scheduled transcript determines the required original sign **by the nineteenth observation**. Only then apply the abstract-to-physical compiler to obtain an unconditional `Fits 19` policy. The original eighteen-read impossibility theorem and its `native_decide` finite trust boundary remain separate.

**Mathematical sources:** the tagged-state argument is an elementary indistinguishability lemma; Cameron (1999) and Seress (2003) explain the underlying permutation-group sign convention, and the existing project geometry and corner identification lemmas supply the physical coordinate semantics. No novelty claim is made about the abstract indistinguishability principle.

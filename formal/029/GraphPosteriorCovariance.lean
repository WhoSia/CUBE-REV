import AdaptiveLowerBound

namespace CubeRev029

/-- A posterior belief transported as an image, not just a collection of
candidate counts. Preserving this predicate is required for a sound
symmetry quotient of an adaptive query/reply game. -/
def transportedBelief (encode : S → T) (belief : S → Prop) : T → Prop :=
  fun t => ∃ s, belief s ∧ encode s = t

/-- For an equivariant observation channel and an injective relabeling of
answers, posterior refinement commutes with transport. This is the exact
alternating, reply-labelled fiber identity needed by the quotient; it is
stronger than matching posterior cardinalities. -/
theorem transported_posterior_covariance
    {S T Q₁ Q₂ R₁ R₂ : Type}
    (encode : S → T)
    (queryForward : Q₁ → Q₂)
    (replyForward : R₁ → R₂)
    (replyInjective : Function.Injective replyForward)
    (sourceObserve : S → Q₁ → R₁)
    (targetObserve : T → Q₂ → R₂)
    (equivariant : ∀ s q,
      targetObserve (encode s) (queryForward q) =
        replyForward (sourceObserve s q))
    (belief : S → Prop) (q : Q₁) (r : R₁) :
    transportedBelief encode (posterior sourceObserve belief q r) =
      posterior targetObserve (transportedBelief encode belief)
        (queryForward q) (replyForward r) := by
  funext t
  apply propext
  constructor
  · rintro ⟨s, ⟨hb, hs⟩, ht⟩
    refine ⟨⟨s, hb, ht⟩, ?_⟩
    rw [← ht, equivariant s q, hs]
  · rintro ⟨⟨s, hb, ht⟩, hr⟩
    refine ⟨s, ⟨hb, ?_⟩, ht⟩
    apply replyInjective
    calc
      replyForward (sourceObserve s q) =
          targetObserve (encode s) (queryForward q) :=
        (equivariant s q).symm
      _ = targetObserve t (queryForward q) := by rw [ht]
      _ = replyForward r := hr

/-- State-injective transport carries a two-state collision witness to a
two-state collision witness: it does not collapse distinct initial cubes. -/
theorem transported_belief_preserves_ambiguity
    {S T : Type} (encode : S → T)
    (injective : Function.Injective encode)
    (belief : S → Prop) (ambiguous : Ambiguous belief) :
    Ambiguous (transportedBelief encode belief) := by
  obtain ⟨s, t, hs, ht, different⟩ := ambiguous
  exact ⟨encode s, encode t, ⟨s, hs, rfl⟩,
    ⟨t, ht, rfl⟩, fun eq => different (injective eq)⟩

/-- An adversary lower-bound certificate transports through a state
embedding and response-injective observation equivalence, provided every
target query is the translation of a source query.  Neither player may
choose the current reply before the current query.

This relates the user's strongest 18-frame impossibility theorem to
graph/game symmetry. It does NOT create the original certified adversary
nor assert the corresponding hypotheses for the whole physical cube. -/
theorem adversary_transport_across_equivariant_game
    {S T Q₁ Q₂ R₁ R₂ : Type}
    (encode : S → T) (encodeInjective : Function.Injective encode)
    (queryForward : Q₁ → Q₂) (queryBackward : Q₂ → Q₁)
    (everyTargetQuery : ∀ q, queryForward (queryBackward q) = q)
    (replyForward : R₁ → R₂)
    (replyInjective : Function.Injective replyForward)
    (sourceObserve : S → Q₁ → R₁)
    (targetObserve : T → Q₂ → R₂)
    (equivariant : ∀ s q,
      targetObserve (encode s) (queryForward q) =
        replyForward (sourceObserve s q))
    (n : Nat) (belief : S → Prop)
    (hard : Adversary sourceObserve n belief) :
    Adversary targetObserve n (transportedBelief encode belief) := by
  induction n generalizing belief with
  | zero =>
      exact transported_belief_preserves_ambiguity
        encode encodeInjective belief hard
  | succ n ih =>
      intro q₂
      obtain ⟨reply, child⟩ := hard (queryBackward q₂)
      refine ⟨replyForward reply, ?_⟩
      have fiber := transported_posterior_covariance
        encode queryForward replyForward replyInjective
        sourceObserve targetObserve equivariant
        belief (queryBackward q₂) reply
      rw [everyTargetQuery q₂] at fiber
      rw [← fiber]
      exact ih (posterior sourceObserve belief (queryBackward q₂) reply) child

#print axioms transported_posterior_covariance
#print axioms transported_belief_preserves_ambiguity
#print axioms adversary_transport_across_equivariant_game

end CubeRev029

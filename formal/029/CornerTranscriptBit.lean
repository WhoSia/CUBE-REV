import NineteenCornerTranscript

namespace CubeRev029.Physical

/-- A mathematical factorization of a corner-dependent Boolean through
the actual nineteen charged corner replies. This uses classical choice
on the reachable-state fiber, so it is NOT an executable decoder. -/
noncomputable def cornerTranscriptBit (bit : Coloring → Bool)
    (replies : List Nat) : Bool :=
  if h : ∃ s : Coloring,
      Reachable s ∧ scheduledCornerColors s = replies then
    bit (Classical.choose h)
  else false

/-- Any Boolean that is determined by the full original corner coloring
is also determined on reachable cubes by their nineteen actual corner
responses. The *only* physical premise used is the already established
reachable-corner observation uniqueness theorem.

This is a factorization/existence result, not a callable runtime parity
selector: cornerTranscriptBit uses Classical.choice and will not by
itself generate a computable 19-frame observation policy. -/
theorem corner_transcript_bit_correct
    (bit : Coloring → Bool)
    (cornerExtensional : ∀ s t : Coloring,
      (∀ i : Fin 8, ∀ j : Fin 3,
        s (cornerRawSlot i j) = t (cornerRawSlot i j)) →
      bit s = bit t)
    (s : Coloring) (legal : Reachable s) :
    cornerTranscriptBit bit (scheduledCornerColors s) = bit s := by
  have witness : ∃ t : Coloring,
      Reachable t ∧
      scheduledCornerColors t = scheduledCornerColors s :=
    ⟨s, legal, rfl⟩
  unfold cornerTranscriptBit
  rw [dif_pos witness]
  have hchosen := Classical.choose_spec witness
  exact cornerExtensional (Classical.choose witness) s
    (same_nineteen_corner_answers_force_all_corner_colors
      (Classical.choose witness) s hchosen.1 legal hchosen.2)

/-- Two legal cubes producing identical nineteen corner readouts have
the same value under any corner-extensional Bool. This is a *necessary
consistency test* for a proposed terminal sign, separate from defining
an implementable decoder that consumes physical replies. -/
theorem corner_transcript_bit_fiber_constant
    (bit : Coloring → Bool)
    (cornerExtensional : ∀ s t : Coloring,
      (∀ i : Fin 8, ∀ j : Fin 3,
        s (cornerRawSlot i j) = t (cornerRawSlot i j)) →
      bit s = bit t)
    (s t : Coloring)
    (hs : Reachable s) (ht : Reachable t)
    (same : scheduledCornerColors s = scheduledCornerColors t) :
    bit s = bit t :=
  cornerExtensional s t
    (same_nineteen_corner_answers_force_all_corner_colors
      s t hs ht same)

#print axioms corner_transcript_bit_correct
#print axioms corner_transcript_bit_fiber_constant

end CubeRev029.Physical

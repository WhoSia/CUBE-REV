import FrozenNormalizationParityTransport
import PhysicalFrozenSignIntegration

namespace CubeRev029.Nineteen

open CubeRev029.Eighteen
open CubeRev029.Physical

set_option autoImplicit false

/-!
The mathematical handoff to the 52 frozen certified roots no longer has
separate edge/corner parity coupling or signed-normalization parity
hypotheses. Both are discharged by physical turn geometry, the generic
adjacent-swap parity proof and the actual first-eleven gauge correction.

The remaining hypothesis is that the exact normalized physical candidate
belongs to the chosen immutable frozen root's posterior, along with
all-history root selection and actual executable reply decoding.
-/

/-- Every real physical turn history and every first-eleven charged prefix
produce at least one exact normalized complete edge word, whose actual
signed frozen decoder input equals the physical corner-derived sign. -/
theorem physical_turns_have_sign_correct_normalized_word
    (turns : List Turn) (firstElevenReplies : List FrameColor) :
    ∃ path : List Nat,
      (∀ i ∈ path, i < 10) ∧
      adjTrace path (List.range 12) =
        frozenPrefixStableOrder firstElevenReplies ++ [11] ∧
      edgeWordSign
        (adjTrace path (relabelEdgeWord
          (chosenPrefixColorMap firstElevenReplies)
          (originalPhysicalEdgeWord turns))) =
        (observedTerminalCorrectedParity
          firstElevenReplies (coordinatesAlong turns) == 1) := by
  have complete :
      (wordLabels (originalPhysicalEdgeWord turns)).Perm (List.range 12) := by
    exact edge_coordinates_along_piece_perm turns
  obtain ⟨path, bounds, routed, transportedParity⟩ :=
    frozen_prefix_normalized_word_has_exact_parity
      firstElevenReplies (originalPhysicalEdgeWord turns) complete
  refine ⟨path, bounds, routed, ?_⟩
  exact physical_turns_normalized_sign_from_corner_observations
    turns firstElevenReplies
    (adjTrace path (relabelEdgeWord
      (chosenPrefixColorMap firstElevenReplies)
      (originalPhysicalEdgeWord turns)))
    transportedParity

/-- Apply the ACTUAL immutable fifty-two-root certified eight-read decoder
to a fully normalized real physical edge candidate. There is now NO
arbitrary sign equality hypothesis, NO parity oracle, and NO unproved
reindexing axiom. Instead the exact candidate-in-belief hypothesis remains
visible: eliminating it needs universal root selection and signed posterior
transport, not another repetition of the parity argument. -/
theorem physical_frozen_root_recovers_if_normalized_candidate_in_belief
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (entry : Lean.Json) (member : entry ∈ roots.toList)
    (graph : Array (FrozenInstruction Nat Nat Unit))
    (belief : List Word)
    (entryParsed : parseRepresentativeRoot entry = .ok (graph, belief))
    (turns : List Turn)
    (firstElevenReplies : List FrameColor) :
    ∃ path : List Nat,
      (∀ i ∈ path, i < 10) ∧
      adjTrace path (List.range 12) =
        frozenPrefixStableOrder firstElevenReplies ++ [11] ∧
      (let normalized := adjTrace path (relabelEdgeWord
        (chosenPrefixColorMap firstElevenReplies)
        (originalPhysicalEdgeWord turns))
       normalized ∈ belief →
         ((exactEightSectorPolicy 0 graph observation edgeWordSign 0 belief).run
             observation normalized)
             (observedTerminalCorrectedParity firstElevenReplies
               (coordinatesAlong turns) == 1) = some normalized) := by
  have complete :
      (wordLabels (originalPhysicalEdgeWord turns)).Perm (List.range 12) := by
    exact edge_coordinates_along_piece_perm turns
  obtain ⟨path, bounds, routed, transportedParity⟩ :=
    frozen_prefix_normalized_word_has_exact_parity
      firstElevenReplies (originalPhysicalEdgeWord turns) complete
  refine ⟨path, bounds, routed, ?_⟩
  dsimp
  intro candidate
  exact physical_turns_frozen_root_recovers_if_normalization_correct
    roots parsed entry member graph belief entryParsed
    turns
    (adjTrace path (relabelEdgeWord
      (chosenPrefixColorMap firstElevenReplies)
      (originalPhysicalEdgeWord turns)))
    candidate firstElevenReplies transportedParity

#print axioms physical_turns_have_sign_correct_normalized_word
#print axioms physical_frozen_root_recovers_if_normalized_candidate_in_belief

end CubeRev029.Nineteen

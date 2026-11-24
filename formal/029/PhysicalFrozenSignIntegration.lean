import ParityReindexBridge
import FrozenTerminalSignBridge

namespace CubeRev029.Nineteen

open CubeRev029.Eighteen
open CubeRev029.Physical

set_option autoImplicit false

/-!
The real turn-word physical edge/corner parity coupling discharges the
`legalCoupling` hypothesis of BM's normalized-edge-sign theorem. The
remaining `transportedParity` equation is explicitly scoped to the actual
normalization of that very same original edge word. The 52-root selection,
posterior belief membership, and computable terminal corner readout are
additional obligations for an unconditional Fits 19 policy.
-/

/-- Real legal face turns, with their lookup-order orientation, discharge
the physical edge/corner parity hypothesis. Only the actual selected
frozen normalization sign transport remains an external premise. -/
theorem physical_turns_normalized_sign_from_corner_observations
    (turns : List Turn)
    (firstElevenReplies : List FrameColor)
    (normalizedWord : Word)
    (transportedParity :
      parity (normalizedWord.map (· / 2)) =
        (parity ((originalPhysicalEdgeWord turns).map (· / 2)) +
          frozenPrefixSignCorrection firstElevenReplies) % 2) :
    edgeWordSign normalizedWord =
      (observedTerminalCorrectedParity
        firstElevenReplies (coordinatesAlong turns) == 1) := by
  exact normalized_edge_sign_matches_observed_corner_sign
    firstElevenReplies (originalPhysicalEdgeWord turns)
    normalizedWord (coordinatesAlong turns)
    (original_physical_edge_word_sign_agrees_corner turns)
    transportedParity

/-- The certified frozen JSON continuation can now consume the terminal
sign from a reachable turn-word state once an EXACT normalized word and
entry membership have been established. The physical coupling premise
has disappeared; normalization transport and root membership still have
to be proved for each feasible actual prefix. -/
theorem physical_turns_frozen_root_recovers_if_normalization_correct
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (entry : Lean.Json) (member : entry ∈ roots.toList)
    (graph : Array (FrozenInstruction Nat Nat Unit))
    (belief : List Word)
    (entryParsed : parseRepresentativeRoot entry = .ok (graph, belief))
    (turns : List Turn)
    (normalizedWord : Word)
    (candidate : normalizedWord ∈ belief)
    (firstElevenReplies : List FrameColor)
    (transportedParity :
      parity (normalizedWord.map (· / 2)) =
        (parity ((originalPhysicalEdgeWord turns).map (· / 2)) +
          frozenPrefixSignCorrection firstElevenReplies) % 2) :
    ((exactEightSectorPolicy 0 graph observation edgeWordSign 0 belief).run
        observation normalizedWord)
        (observedTerminalCorrectedParity firstElevenReplies
          (coordinatesAlong turns) == 1) = some normalizedWord := by
  exact frozen_root_recovers_with_observed_corner_sign
    roots parsed entry member graph belief entryParsed
    (originalPhysicalEdgeWord turns) normalizedWord candidate
    firstElevenReplies (coordinatesAlong turns)
    (original_physical_edge_word_sign_agrees_corner turns)
    transportedParity

#print axioms physical_turns_normalized_sign_from_corner_observations
#print axioms physical_turns_frozen_root_recovers_if_normalization_correct

end CubeRev029.Nineteen

import PrefixColorGauge
import CornerSignedCorrection

namespace CubeRev029.Physical

/-- The terminal signed-sector parity is formed from the oriented corner
permutation AND the precise, already defined frozen prefix correction.
The correction is derived from past paired replies, not a free sign sensor. -/
def observedTerminalCorrectedParity
    (firstElevenReplies : List FrameColor)
    (corners : CornerCoordinates) : Nat :=
  correctedCornerParity corners
    (frozenPrefixSignCorrection firstElevenReplies)

/-- Make the historical frozen route_info convention explicit at the
terminal interface. This proof uses the *actual* frozen prefix function
rather than a label-only correction or a fresh independently chosen gauge. -/
theorem observed_terminal_parity_uses_three_pair_character
    (replies : List FrameColor) (corners : CornerCoordinates) :
    observedTerminalCorrectedParity replies corners =
      (cornerPermutationParity corners +
        (Eighteen.parity (frozenPrefixStableOrder replies) +
          Eighteen.parity (Nineteen.inducedThreePairPermutation
            (chosenPrefixColorMap replies))) % 2) % 2 := by
  unfold observedTerminalCorrectedParity correctedCornerParity
  rw [frozen_prefix_sign_correction_three_pair]

/-- When both possible initial physical states have the same eleven
genuinely received paired prefix replies and the same nineteen actual
corner replies, their terminal corrected parity agrees. The result
makes NO assumption that the terminal sign can be observed earlier. -/
theorem observed_terminal_corrected_parity_fiber_constant
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (samePrefix :
      firstElevenPairedAddresses.map (abstractPairRead s) =
      firstElevenPairedAddresses.map (abstractPairRead t))
    (sameCorners : scheduledCornerColors s = scheduledCornerColors t) :
    observedTerminalCorrectedParity
        (firstElevenPairedAddresses.map (abstractPairRead s)) a =
      observedTerminalCorrectedParity
        (firstElevenPairedAddresses.map (abstractPairRead t)) b := by
  rw [samePrefix]
  exact corrected_corner_parity_from_past_and_nineteen_replies
    s t hs ht a b ha hb sameCorners
    (frozenPrefixSignCorrection
      (firstElevenPairedAddresses.map (abstractPairRead t)))

/-- A fixed historical eleven-reply vector can be used to compute the
correction for all states consistent with that observed prefix, without
inspecting their unknown original coloring to select a gauge. -/
theorem observed_terminal_corrected_parity_given_history
    (replies : List FrameColor)
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (sameCorners : scheduledCornerColors s = scheduledCornerColors t) :
    observedTerminalCorrectedParity replies a =
      observedTerminalCorrectedParity replies b := by
  exact corrected_corner_parity_from_past_and_nineteen_replies
    s t hs ht a b ha hb sameCorners
    (frozenPrefixSignCorrection replies)

/-- Neither the chosen color-gauge sign nor the stable-sort correction
reads the first-eleven corner colors. Equality of the eleven EDGE
answers alone fixes the complete actual frozen prefix correction. -/
theorem frozen_prefix_sign_correction_ignores_corner_replies
    (first second : List FrameColor)
    (sameEdges : first.map Prod.fst = second.map Prod.fst) :
    frozenPrefixSignCorrection first =
      frozenPrefixSignCorrection second := by
  have gauge := chosen_prefix_gauge_ignores_corner_replies
    first second sameEdges
  have rank : frozenPrefixColorRank first =
      frozenPrefixColorRank second := by
    funext i
    simp only [frozenPrefixColorRank, gauge, sameEdges]
  have order : frozenPrefixStableOrder first =
      frozenPrefixStableOrder second := by
    simp only [frozenPrefixStableOrder, rank]
  unfold frozenPrefixSignCorrection
  rw [order, gauge]

/-- This full-state terminal parity factors through two *independently
paid* information channels: the eleven first edge colors determine the
past-selected gauge/position correction, while the nineteen scheduled
corner colors determine the physical corner permutation parity. Thus
equality of eleven EDGE replies suffices; the first-eleven corner replies
need not be separately assumed equal beyond the nineteen-corner record. -/
theorem observed_terminal_parity_from_edge_and_corner_histories
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (sameEdgePrefix :
      (firstElevenPairedAddresses.map (abstractPairRead s)).map Prod.fst =
      (firstElevenPairedAddresses.map (abstractPairRead t)).map Prod.fst)
    (sameCorners : scheduledCornerColors s = scheduledCornerColors t) :
    observedTerminalCorrectedParity
        (firstElevenPairedAddresses.map (abstractPairRead s)) a =
      observedTerminalCorrectedParity
        (firstElevenPairedAddresses.map (abstractPairRead t)) b := by
  unfold observedTerminalCorrectedParity
  exact corrected_corner_parity_respects_equal_prefix_corrections
    s t hs ht a b ha hb sameCorners
    (frozenPrefixSignCorrection
      (firstElevenPairedAddresses.map (abstractPairRead s)))
    (frozenPrefixSignCorrection
      (firstElevenPairedAddresses.map (abstractPairRead t)))
    (frozen_prefix_sign_correction_ignores_corner_replies
      _ _ sameEdgePrefix)

#print axioms frozen_prefix_sign_correction_ignores_corner_replies
#print axioms observed_terminal_parity_from_edge_and_corner_histories

#print axioms observed_terminal_parity_uses_three_pair_character
#print axioms observed_terminal_corrected_parity_fiber_constant
#print axioms observed_terminal_corrected_parity_given_history

end CubeRev029.Physical

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
        (parity (frozenPrefixStableOrder replies) +
          parity (Nineteen.inducedThreePairPermutation
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

#print axioms observed_terminal_parity_uses_three_pair_character
#print axioms observed_terminal_corrected_parity_fiber_constant
#print axioms observed_terminal_corrected_parity_given_history

end CubeRev029.Physical

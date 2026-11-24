import ParityReindexBridge
import PrefixColorGauge
import SymmetryWordTransport

namespace CubeRev029.Nineteen

open CubeRev029.Eighteen
open CubeRev029.Physical

set_option autoImplicit false
set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-!
Full algebraic signed transport for a complete edge word, using the
ACTUAL 48-color gauge and canonical 11-slot sorted prefix. This is
separate from total frozen JSON-root membership and physical routing.
-/

/-- The actual 48 legal color symmetries permute the twelve edge labels.
Stronger than eraseDups.length = 12: each full labeling is an honest
permutation of the original 0..11 edge IDs. -/
theorem all_color_symmetries_permute_edge_labels :
    ∀ sigma ∈ symmetries,
      (inducedTwelveEdgePermutation sigma).Perm (List.range 12) := by
  decide +kernel

/-- The parity of relabeling a complete edge permutation is its original
parity plus the sign character of the chosen 48-color automorphism. No
fixed permutation of labels, orientation vector or particular scramble
is assumed. -/
theorem relabeled_complete_word_parity
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (word : Word)
    (complete : (wordLabels word).Perm (List.range 12)) :
    parity (wordLabels (relabelEdgeWord sigma word)) =
      (parity (wordLabels word) +
        parity (inducedTwelveEdgePermutation sigma)) % 2 := by
  have hperm := all_color_symmetries_permute_edge_labels sigma hsigma
  have distinct : ((List.range 12).map (relabeledEdgeType sigma)).Nodup :=
    hperm.symm.nodup List.nodup_range
  have even : parity ((List.range 12).map (fun i => i)) = 0 := by
    decide +kernel
  have h := parity_reindex_of_even_reference complete.symm
    (relabeledEdgeType sigma) (fun i => i)
    distinct (by decide +kernel) even
  have shifted :
      parity ((wordLabels word).map (relabeledEdgeType sigma)) =
      (parity (inducedTwelveEdgePermutation sigma) +
        parity (wordLabels word)) % 2 := by
    simpa [inducedTwelveEdgePermutation] using h
  rw [relabelEdgeWord_labels, shifted]
  omega

/-- Relabel the edge names, then perform a legal sequence of adjacent
position swaps: the parity shift is the sum of the group sign character
and the swap-count parity. This is valid for EVERY complete edge word. -/
theorem relabeled_and_sorted_word_parity
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (word : Word)
    (complete : (wordLabels word).Perm (List.range 12))
    (path : List Nat)
    (bounds : ∀ i ∈ path, i + 1 < word.length) :
    parity (wordLabels (adjTrace path (relabelEdgeWord sigma word))) =
      (parity (wordLabels word) +
        parity (inducedTwelveEdgePermutation sigma) + path.length) % 2 := by
  have permRelabeled :
      (wordLabels (relabelEdgeWord sigma word)).Perm (List.range 12) := by
    rw [relabelEdgeWord_labels]
    exact (complete.map (relabeledEdgeType sigma)).trans
      (all_color_symmetries_permute_edge_labels sigma hsigma)
  have distinct := permRelabeled.symm.nodup List.nodup_range
  have boundsR : ∀ i ∈ path,
      i + 1 < (wordLabels (relabelEdgeWord sigma word)).length := by
    intro i member
    simpa [wordLabels, relabelEdgeWord] using bounds i member
  have htrace := adjTrace_parity path
    (wordLabels (relabelEdgeWord sigma word)) distinct boundsR
  calc
    parity (wordLabels (adjTrace path (relabelEdgeWord sigma word))) =
        parity (adjTrace path (wordLabels (relabelEdgeWord sigma word))) := by
          exact congrArg parity
            (by simpa only [wordLabels] using
              (adjTrace_map (fun id : Nat => id / 2) path
                (relabelEdgeWord sigma word)))
    _ = (parity (wordLabels (relabelEdgeWord sigma word)) +
        path.length) % 2 := htrace
    _ = (parity (wordLabels word) +
        parity (inducedTwelveEdgePermutation sigma) + path.length) % 2 := by
          rw [relabeled_complete_word_parity sigma hsigma word complete]
          omega

/-- The REAL prefix-selected color gauge and stable-order trace give a
signed normalized word for any original complete physical edge word.
Existence of a sign-correct normalized word is NOT a proof that a frozen
representative root is selected or its candidate belief contains it. -/
theorem frozen_prefix_normalized_word_has_exact_parity
    (firstElevenReplies : List FrameColor)
    (word : Word)
    (complete : (wordLabels word).Perm (List.range 12)) :
    ∃ (path : List Nat),
      (∀ i ∈ path, i < 10) ∧
      adjTrace path (List.range 12) =
        frozenPrefixStableOrder firstElevenReplies ++ [11] ∧
      parity (wordLabels
        (adjTrace path
          (relabelEdgeWord (chosenPrefixColorMap firstElevenReplies) word))) =
        (parity (wordLabels word) +
          frozenPrefixSignCorrection firstElevenReplies) % 2 := by
  obtain ⟨path, routed, bounds, correction⟩ :=
    frozen_prefix_sign_correction_full_twelve_trace firstElevenReplies
  have wordLen : word.length = 12 := by
    have hl := complete.length_eq
    simpa [wordLabels] using hl
  have legalBounds : ∀ i ∈ path, i + 1 < word.length := by
    intro i hi
    have h := bounds i hi
    omega
  have transport := relabeled_and_sorted_word_parity
    (chosenPrefixColorMap firstElevenReplies)
    (chosen_prefix_color_map_legal firstElevenReplies)
    word complete path legalBounds
  have signCharacter := chosen_prefix_gauge_sign_character firstElevenReplies
  refine ⟨path, bounds, routed, ?_⟩
  rw [transport, signCharacter]
  omega

#print axioms all_color_symmetries_permute_edge_labels
#print axioms relabeled_complete_word_parity
#print axioms relabeled_and_sorted_word_parity
#print axioms frozen_prefix_normalized_word_has_exact_parity

end CubeRev029.Nineteen

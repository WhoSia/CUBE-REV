import PhysicalCertifiedSignHandoff

namespace CubeRev029.Nineteen

open CubeRev029.Eighteen
open CubeRev029.Physical

set_option autoImplicit false
set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-!
# Production bubble trace: deterministic signed physical normalization

The previous BN development constructed an existential adjacent-swap path.
This module instead uses the EXACT executable path returned by the already
Lean-compiled bubbleCandidatePath11. No different sorter is substituted.
This still does not establish universal frozen-root membership or a 19-frame
executable corner decoder. The new source needs pinned Lean compilation.
-/

/-- The production eleven-pass bubble trace sorts exactly the observed eleven
positions, fixes the unread twelfth position and has the parity of the sorted
prefix. Importantly, the path is the executable path, NOT an existentially
chosen adjacent-swap certificate. -/
theorem executable_bubble_trace_fixes_unread_and_sign
    (replies : List FrameColor) :
    adjTrace
        (bubbleCandidatePath11 (frozenPrefixColorRank replies))
        (List.range 12) =
      frozenPrefixStableOrder replies ++ [11] ∧
    (∀ i ∈ bubbleCandidatePath11 (frozenPrefixColorRank replies),
      i < 10) ∧
    (bubbleCandidatePath11 (frozenPrefixColorRank replies)).length % 2 =
      parity (frozenPrefixStableOrder replies) := by
  let rank := frozenPrefixColorRank replies
  let path := bubbleCandidatePath11 rank
  obtain ⟨sorted, bounded⟩ := bubble_candidate_normalizes rank
  have bounded11 : ∀ i ∈ path,
      i + 1 < (List.range 11).length := by
    intro i hi
    have bound := bounded i hi
    simp only [List.length_range]
    omega
  have twelveRange : (List.range 11) ++ [11] = List.range 12 := by
    decide +kernel
  have full : adjTrace path (List.range 12) =
      frozenPrefixStableOrder replies ++ [11] := by
    rw [← twelveRange, adjTrace_append_unread path (List.range 11) 11 bounded11]
    exact congrArg (fun xs => xs ++ [11]) sorted
  have bounded12 : ∀ i ∈ path,
      i + 1 < (List.range 12).length := by
    intro i hi
    have h := bounded i hi
    simp only [List.length_range]
    omega
  have sign := adjTrace_parity path (List.range 12)
    List.nodup_range bounded12
  rw [full] at sign
  have even : parity (List.range 12) = 0 := by decide +kernel
  rw [even] at sign
  obtain ⟨_, _, _, sameParity, _⟩ :=
    eleven_slot_trace_full_twelve_parity rank
  have signLength : path.length % 2 =
      parity (frozenPrefixStableOrder replies) := by
    have sameParity' :
      parity (frozenPrefixStableOrder replies ++ [11]) =
        parity (frozenPrefixStableOrder replies) := by
      simpa [frozenPrefixStableOrder] using sameParity
    rw [sameParity'] at sign
    omega
  exact ⟨full, bounded, signLength⟩

/-- For EVERY complete original edge word, the ACTUAL production bubble
path after the selected 48-color relabeling changes its inversion parity by
exactly the historical frozen route_info correction. No path existential is
left in the theorem statement. -/
theorem executable_bubble_normalized_word_parity
    (replies : List FrameColor)
    (word : Word)
    (complete : (wordLabels word).Perm (List.range 12)) :
    parity (wordLabels
      (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
        (relabelEdgeWord (chosenPrefixColorMap replies) word))) =
      (parity (wordLabels word) +
        frozenPrefixSignCorrection replies) % 2 := by
  let path := bubbleCandidatePath11 (frozenPrefixColorRank replies)
  have wordLength : word.length = 12 := by
    have count := complete.length_eq
    simpa [wordLabels] using count
  obtain ⟨_, bounded, pathParity⟩ :=
    executable_bubble_trace_fixes_unread_and_sign replies
  have validBounds : ∀ i ∈ path, i + 1 < word.length := by
    intro i hi
    have hi' := bounded i hi
    omega
  have transported := relabeled_and_sorted_word_parity
    (chosenPrefixColorMap replies)
    (chosen_prefix_color_map_legal replies)
    word complete path validBounds
  have gauge := chosen_prefix_gauge_sign_character replies
  have correction := frozen_prefix_sign_correction_three_pair replies
  have hpath : path.length =
      (bubbleCandidatePath11 (frozenPrefixColorRank replies)).length := rfl
  rw [transported, gauge, correction]
  omega

/-- Apply the production path to an ACTUAL physical turn-word state:
its normalized representative sign is the observed-corner sign with the
past-determined prefix correction, without an external parity premise. -/
theorem executable_physical_normalized_sign_correct
    (turns : List Turn) (replies : List FrameColor) :
    edgeWordSign
      (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
        (relabelEdgeWord (chosenPrefixColorMap replies)
          (originalPhysicalEdgeWord turns))) =
      (observedTerminalCorrectedParity replies
        (coordinatesAlong turns) == 1) := by
  have complete :
      (wordLabels (originalPhysicalEdgeWord turns)).Perm (List.range 12) :=
    edge_coordinates_along_piece_perm turns
  exact physical_turns_normalized_sign_from_corner_observations
    turns replies _
    (executable_bubble_normalized_word_parity replies
      (originalPhysicalEdgeWord turns) complete)

/-- Certified eight-read frozen root recovery is now connected to the
ACTUAL executable prefix bubble trace, rather than a merely existential
normalizer. The exact normalized candidate's membership in the chosen
frozen root remains an EXPLICIT unproved assumption. -/
theorem frozen_root_recovers_executable_physical_bubble_candidate
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (entry : Lean.Json) (member : entry ∈ roots.toList)
    (graph : Array (FrozenInstruction Nat Nat Unit))
    (belief : List Word)
    (entryParsed : parseRepresentativeRoot entry = .ok (graph, belief))
    (turns : List Turn) (replies : List FrameColor)
    (candidate :
      adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
        (relabelEdgeWord (chosenPrefixColorMap replies)
          (originalPhysicalEdgeWord turns)) ∈ belief) :
    ((exactEightSectorPolicy 0 graph observation edgeWordSign 0 belief).run
        observation
        (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
          (relabelEdgeWord (chosenPrefixColorMap replies)
            (originalPhysicalEdgeWord turns))))
        (observedTerminalCorrectedParity replies
          (coordinatesAlong turns) == 1) =
      some (adjTrace (bubbleCandidatePath11
          (frozenPrefixColorRank replies))
        (relabelEdgeWord (chosenPrefixColorMap replies)
          (originalPhysicalEdgeWord turns))) := by
  have complete :
      (wordLabels (originalPhysicalEdgeWord turns)).Perm (List.range 12) :=
    edge_coordinates_along_piece_perm turns
  exact physical_turns_frozen_root_recovers_if_normalization_correct
    roots parsed entry member graph belief entryParsed turns
    (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
      (relabelEdgeWord (chosenPrefixColorMap replies)
        (originalPhysicalEdgeWord turns)))
    candidate replies
    (executable_bubble_normalized_word_parity replies
      (originalPhysicalEdgeWord turns) complete)

#print axioms executable_bubble_trace_fixes_unread_and_sign
#print axioms executable_bubble_normalized_word_parity
#print axioms executable_physical_normalized_sign_correct
#print axioms frozen_root_recovers_executable_physical_bubble_candidate

/-- The actually charged first eleven edge colors agree with the
original physical edge word. No corner decoder, flip parity or
certificate assumption is needed for this observation bridge. -/
theorem physical_first_eleven_replies_match_word (turns : List Turn) :
    (firstElevenPairedAddresses.map
      (abstractPairRead (paint turns solved))).map Prod.fst =
      ((originalPhysicalEdgeWord turns).take 11).map
        (fun e => sticker e false) := by
  have h := edge_coordinates_along_agree turns
  change
    [paint turns solved (edgeSlot 0 false),
     paint turns solved (edgeSlot 1 false),
     paint turns solved (edgeSlot 2 false),
     paint turns solved (edgeSlot 3 false),
     paint turns solved (edgeSlot 4 false),
     paint turns solved (edgeSlot 5 false),
     paint turns solved (edgeSlot 6 false),
     paint turns solved (edgeSlot 7 false),
     paint turns solved (edgeSlot 8 false),
     paint turns solved (edgeSlot 9 false),
     paint turns solved (edgeSlot 10 false)] =
    [sticker (edgeCoordinatesAlong turns 0) false,
     sticker (edgeCoordinatesAlong turns 1) false,
     sticker (edgeCoordinatesAlong turns 2) false,
     sticker (edgeCoordinatesAlong turns 3) false,
     sticker (edgeCoordinatesAlong turns 4) false,
     sticker (edgeCoordinatesAlong turns 5) false,
     sticker (edgeCoordinatesAlong turns 6) false,
     sticker (edgeCoordinatesAlong turns 7) false,
     sticker (edgeCoordinatesAlong turns 8) false,
     sticker (edgeCoordinatesAlong turns 9) false,
     sticker (edgeCoordinatesAlong turns 10) false]
  rw [h 0 false, h 1 false, h 2 false, h 3 false, h 4 false,
      h 5 false, h 6 false, h 7 false, h 8 false, h 9 false, h 10 false]

#print axioms physical_first_eleven_replies_match_word

end CubeRev029.Nineteen

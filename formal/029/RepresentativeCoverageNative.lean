import NormalizedRootMembership

namespace CubeRev029.Nineteen

open Eighteen CubeRev029.Physical

/-- The ONLY new `native_decide` of BS-3. Trust boundary: the compiled
evaluation of `coverageCheck` on the same SHA-256-pinned certificate bytes
as `fifty_two_frozen_roots_semantically_accepted`. It enumerates all 24576
raw rows and requires an exact certificate prefix for each. -/
theorem representative_prefixes_covered_source :
    coverageCheck (include_str "upper-policy-certificate.json") = true := by
  native_decide

/-- BS-3 + BS-4 with the coverage premise discharged. Remaining explicit
premises: `hflip` (even edge-flip parity) and `hfst` (observed first
colors are the word's first-eleven first-stickers). -/
theorem normalized_word_recovered_certified
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (word : Word) (complete : (wordLabels word).Perm (List.range 12))
    (hflip : flipBit word = 0)
    (replies : List FrameColor) (hlen : replies.length = 11)
    (hfst : replies.map Prod.fst = (word.take 11).map (fun e => sticker e false)) :
    ∃ entry ∈ roots.toList,
      ∃ (graph : Array (FrozenInstruction Nat Nat Unit)) (belief : List Word),
        parseRepresentativeRoot entry = .ok (graph, belief) ∧
        adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
            (relabelEdgeWord (chosenPrefixColorMap replies) word) ∈ belief :=
  let ⟨entry, h, graph, belief, hp, hm, _⟩ :=
    normalized_word_recovered_by_certified_root roots parsed
      representative_prefixes_covered_source word complete hflip replies hlen hfst
  ⟨entry, h, graph, belief, hp, hm⟩

theorem physical_normalized_recovered_certified
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (turns : List Turn) (replies : List FrameColor)
    (hflip : flipBit (originalPhysicalEdgeWord turns) = 0)
    (hlen : replies.length = 11)
    (hfst : replies.map Prod.fst =
      ((originalPhysicalEdgeWord turns).take 11).map (fun e => sticker e false)) :
    ∃ entry ∈ roots.toList,
      ∃ (graph : Array (FrozenInstruction Nat Nat Unit)) (belief : List Word),
        parseRepresentativeRoot entry = .ok (graph, belief) ∧
        ((exactEightSectorPolicy 0 graph observation edgeWordSign 0 belief).run
          observation
          (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
            (relabelEdgeWord (chosenPrefixColorMap replies)
              (originalPhysicalEdgeWord turns))))
          (observedTerminalCorrectedParity replies (coordinatesAlong turns) == 1) =
          some (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
            (relabelEdgeWord (chosenPrefixColorMap replies)
              (originalPhysicalEdgeWord turns))) :=
  physical_normalized_word_recovered_by_certified_root roots parsed
    representative_prefixes_covered_source turns replies hflip hlen hfst

#print axioms representative_prefixes_covered_source
#print axioms normalized_word_recovered_certified
#print axioms physical_normalized_recovered_certified

end CubeRev029.Nineteen

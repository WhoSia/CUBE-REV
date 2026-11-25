import RepresentativeRootInclusion

namespace CubeRev029.Nineteen

open Eighteen CubeRev029.Physical

set_option autoImplicit false
set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-!
# BS-4: executable normalization lands in the certified root's sector

Reuses `sector_complete`, BS-1 (`first_eleven_row_perm`), BS-3 and the
production `bubbleCandidatePath11`. Explicit (unproved here) premises:
`hfst` (the observed first colors are the original word's first-eleven
first-stickers) and `hflip` (even edge-flip parity of the physical word).
-/

theorem getBang_map {α β : Type} [Inhabited α] [Inhabited β] (f : α → β)
    (l : List α) (i : Nat) (h : i < l.length) :
    (l.map f)[i]! = f l[i]! := by
  have h' : i < (l.map f).length := by simpa using h
  first
    | simp [h]
    | (rw [getElem!_pos (l.map f) i h', getElem!_pos l i h]; simp)

theorem sticker_mem_collation : ∀ e < 24, sticker e false ∈ collation := by
  decide +kernel

theorem normalized_word_first_colors (word : Word)
    (complete : (wordLabels word).Perm (List.range 12))
    (replies : List FrameColor)
    (hfst : replies.map Prod.fst = (word.take 11).map (fun e => sticker e false)) :
    ((adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
        (relabelEdgeWord (chosenPrefixColorMap replies) word)).take 11).map
      (fun e => sticker e false) = normalizedPrefix replies := by
  have hsigma := chosen_prefix_color_map_legal replies
  have wlen : word.length = 12 := by simpa [wordLabels] using complete.length_eq
  have w24 : ∀ e ∈ word, e < 24 := by
    intro e he
    have hm : e / 2 ∈ List.range 12 :=
      complete.subset (by unfold wordLabels; exact List.mem_map.2 ⟨e, he, rfl⟩)
    have := List.mem_range.1 hm
    omega
  obtain ⟨hfull, _, _⟩ := executable_bubble_trace_fixes_unread_and_sign replies
  have hstab : (frozenPrefixStableOrder replies).length = 11 := by
    have := (frozen_prefix_stable_order_perm replies).length_eq
    simpa using this.symm
  have w'len : (relabelEdgeWord (chosenPrefixColorMap replies) word).length = 12 := by
    simp [relabelEdgeWord, wlen]
  have w'eq : (List.range 12).map
      (fun i => (relabelEdgeWord (chosenPrefixColorMap replies) word)[i]!) =
      relabelEdgeWord (chosenPrefixColorMap replies) word := by
    have := range_map_getBang (relabelEdgeWord (chosenPrefixColorMap replies) word)
    rwa [w'len] at this
  have nw : adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
      (relabelEdgeWord (chosenPrefixColorMap replies) word) =
      (frozenPrefixStableOrder replies ++ [11]).map
        (fun i => (relabelEdgeWord (chosenPrefixColorMap replies) word)[i]!) := by
    rw [← hfull, adjTrace_map, w'eq]
  rw [nw, List.map_append, List.take_left' (by simp [hstab])]
  unfold normalizedPrefix
  rw [List.map_map]
  apply List.map_congr_left
  intro i hi
  have hi11 : i < 11 :=
    List.mem_range.1 ((frozen_prefix_stable_order_perm replies).symm.subset hi)
  have hiw : i < word.length := by omega
  have hmapped : (relabelEdgeWord (chosenPrefixColorMap replies) word)[i]! =
      relabelEdgeValue (chosenPrefixColorMap replies) word[i]! :=
    getBang_map _ word i hiw
  have hmem : word[i]! ∈ word := by
    first
      | (rw [getElem!_pos word i hiw]; exact List.getElem_mem hiw)
      | simp [hiw]
  show sticker ((relabelEdgeWord (chosenPrefixColorMap replies) word)[i]!) false = _
  rw [hmapped, symmetry_relabelEdgeValue_responses _ hsigma _ (w24 _ hmem) false, hfst]
  congr 1
  have htake : i < (word.take 11).length := by simp; omega
  rw [getBang_map _ (word.take 11) i htake]
  have : (word.take 11)[i]! = word[i]! := by
    first
      | (rw [getElem!_pos (word.take 11) i htake, getElem!_pos word i hiw]; simp)
      | simp [htake, hiw]
  rw [this]

theorem normalized_word_in_prefix_sector (word : Word)
    (complete : (wordLabels word).Perm (List.range 12))
    (hflip : flipBit word = 0)
    (replies : List FrameColor) (hlen : replies.length = 11)
    (hfst : replies.map Prod.fst = (word.take 11).map (fun e => sticker e false)) :
    adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
        (relabelEdgeWord (chosenPrefixColorMap replies) word) ∈
      sector (List.range 12) 0 (normalizedPrefix replies) := by
  have hsigma := chosen_prefix_color_map_legal replies
  have permR : (wordLabels (relabelEdgeWord (chosenPrefixColorMap replies) word)).Perm
      (List.range 12) := by
    rw [relabelEdgeWord_labels]
    exact (complete.map (relabeledEdgeType (chosenPrefixColorMap replies))).trans
      (all_color_symmetries_permute_edge_labels _ hsigma)
  have hperm := adjTrace_perm (bubbleCandidatePath11 (frozenPrefixColorRank replies))
    (relabelEdgeWord (chosenPrefixColorMap replies) word)
  have hlabels : (wordLabels (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
      (relabelEdgeWord (chosenPrefixColorMap replies) word))).Perm (List.range 12) :=
    (hperm.map (· / 2)).trans permR
  have hnormLen : (normalizedPrefix replies).length = 11 := by
    have := (frozen_prefix_stable_order_perm replies).length_eq
    simp [normalizedPrefix]
    simpa using this.symm
  have wlen : word.length = 12 := by simpa [wordLabels] using complete.length_eq
  have nwlen : (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
      (relabelEdgeWord (chosenPrefixColorMap replies) word)).length = 12 := by
    rw [hperm.length_eq]; simp [relabelEdgeWord, wlen]
  refine sector_complete (normalizedPrefix replies) (List.range 12) 0 _ hlabels
    (fun id h => List.mem_range.1 h) (by omega) ?_ ?_
  · rw [flipBit_reorder _ _ hperm]
    rw [symmetry_preserves_flipBit_for_all_complete_words _ hsigma word complete]
    exact hflip
  · rw [hnormLen]
    exact normalized_word_first_colors word complete replies hfst

/-- Parsing a certificate entry whose prefix literal decodes to `P` yields
exactly the root belief `sector (range 12) 0 P`. -/
theorem parse_root_belief (entry : Lean.Json)
    (graph : Array (FrozenInstruction Nat Nat Unit)) (belief : List Word)
    (P : List Nat)
    (hp : parseRepresentativeRoot entry = .ok (graph, belief))
    (hr : rootFirstColors entry = some P) :
    belief = sector (List.range 12) 0 P := by
  unfold rootFirstColors at hr
  unfold parseRepresentativeRoot at hp
  cases hv : entry.getObjVal? "prefix" with
  | error e => simp [hv] at hr
  | ok pj =>
    cases hs : pj.getStr? with
    | error e => simp [hv, hs] at hr
    | ok str =>
      simp [hv, hs] at hr
      cases hn : entry.getObjVal? "nodes" with
      | error e => simp [hv, hs, hn, bind, Except.bind] at hp
      | ok nj =>
        cases ha : nj.getArr? with
        | error e => simp [hv, hs, hn, ha, bind, Except.bind] at hp
        | ok nodes =>
          cases hg : parseFrozenSectorNodes nodes with
          | error e => simp [hv, hs, hn, ha, hg, bind, Except.bind] at hp
          | ok g =>
            simp [hv, hs, hn, ha, hg, bind, Except.bind, pure, Except.pure, ← hr] at hp
            first
              | exact hp.2.symm
              | exact hp.symm
              | (obtain ⟨_, _, h⟩ := hp; exact h.symm)

/-- BS-3 + BS-4: for ANY complete word with even flip parity, any reply
vector of the right length whose first colors are the word's first-eleven
first-stickers, the ACTUAL production normalized word lies in the belief of
a certificate root, and that root recovers it. Unconditional modulo the
explicit premises `hfst`, `hflip` and the one new `native_decide`. -/
theorem normalized_word_recovered_by_certified_root
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
            (relabelEdgeWord (chosenPrefixColorMap replies) word) ∈ belief ∧
        ((exactEightSectorPolicy 0 graph observation edgeWordSign 0 belief).run
          observation
          (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
            (relabelEdgeWord (chosenPrefixColorMap replies) word)))
          (edgeWordSign (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
            (relabelEdgeWord (chosenPrefixColorMap replies) word))) =
          some (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
            (relabelEdgeWord (chosenPrefixColorMap replies) word)) := by
  obtain ⟨ws, x, hw⟩ : ∃ ws x, word = ws ++ [x] := by
    rcases List.eq_nil_or_concat word with h | ⟨L, b, h⟩
    · subst h; simp [wordLabels] at complete
    · exact ⟨L, b, h⟩
  have wlen : word.length = 12 := by simpa [wordLabels] using complete.length_eq
  have wslen : ws.length = 11 := by subst hw; simp at wlen; omega
  have htake : word.take 11 = ws := by
    subst hw; exact List.take_left' wslen
  rw [htake] at hfst
  obtain ⟨o, ho, row, hrow, hp⟩ := first_eleven_row_perm ws x (hw ▸ complete)
  have hcol : ∀ c ∈ replies.map Prod.fst, c ∈ collation := by
    intro c hc
    rw [hfst] at hc
    obtain ⟨e, he, rfl⟩ := List.mem_map.1 hc
    have hm : e / 2 ∈ List.range 12 :=
      complete.subset (by
        unfold wordLabels
        exact List.mem_map.2 ⟨e, by rw [hw]; exact List.mem_append_left _ he, rfl⟩)
    have := List.mem_range.1 hm
    exact sticker_mem_collation e (by omega)
  obtain ⟨entry, hentry, hroot⟩ := normalized_prefix_has_certified_root roots parsed
    replies hlen hcol row (List.mem_flatMap.2 ⟨o, ho, hrow⟩) (by rw [hfst]; exact hp)
  obtain ⟨graph, belief, hparse, hrec⟩ :=
    every_actual_frozen_root_recovers roots parsed entry hentry
  have hbelief := parse_root_belief entry graph belief _ hparse hroot
  have hsector := normalized_word_in_prefix_sector word complete hflip replies hlen
    (by rw [hfst, htake])
  rw [← hbelief] at hsector
  exact ⟨entry, hentry, graph, belief, hparse, hsector, hrec _ hsector⟩

/-- Physical instantiation: the premise `hfst` ties the observed replies to
the actual turn-word's first eleven stickers; `hflip` is the (still
separately owed) edge-flip parity of a reachable state. -/
theorem physical_normalized_word_recovered_by_certified_root
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
              (originalPhysicalEdgeWord turns))) := by
  have complete : (wordLabels (originalPhysicalEdgeWord turns)).Perm (List.range 12) :=
    edge_coordinates_along_piece_perm turns
  obtain ⟨entry, hentry, graph, belief, hparse, _, hrun⟩ :=
    normalized_word_recovered_by_certified_root roots parsed
      (originalPhysicalEdgeWord turns) complete hflip replies hlen hfst
  have sign := executable_physical_normalized_sign_correct turns replies
  rw [sign] at hrun
  exact ⟨entry, hentry, graph, belief, hparse, hrun⟩

#print axioms normalized_word_first_colors
#print axioms normalized_word_in_prefix_sector
#print axioms parse_root_belief
#print axioms normalized_word_recovered_by_certified_root
#print axioms physical_normalized_word_recovered_by_certified_root

end CubeRev029.Nineteen

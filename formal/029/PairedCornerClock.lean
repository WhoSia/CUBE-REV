import TaggedNineteenRootPolicy
import RepresentativeCoverageNative
import NineteenSchedule
import NineteenCornerTranscript

namespace CubeRev029.Nineteen

open Eighteen
open CubeRev029.Physical

/-- An explicitly paired abstract observation channel. The edge word and
corner sticker table are arbitrary fixed ORIGINAL states; the policy
never has access to the corner table except through the returned pair. -/
abbrev TaggedPairedState := Word × (Fin 24 → Nat)

def taggedPairedObserve (state : TaggedPairedState)
    (query : TaggedEdgeAddress × Fin 24) : Nat × Nat :=
  (taggedEdgeObserve state.1 query.1, state.2 query.2)

/-- Attach a fixed corner clock to any edge feedback policy. Every time
the edge controller makes a query, charge one genuinely paired read at
the next corner address. The corner color is discarded as far as the
edge decision tree is concerned, so its future answers cannot affect
the next edge query. -/
def withCornerClock {O : Type}
    (cornerSchedule : List (Fin 24)) :
    Policy TaggedEdgeAddress Nat O →
    Policy (TaggedEdgeAddress × Fin 24) (Nat × Nat) O
  | .stop output => .stop output
  | .read edgeAddress next =>
      .read (edgeAddress, cornerSchedule.headD 0) (fun response =>
        withCornerClock cornerSchedule.tail (next response.1))

/-- Pairing a fixed corner-address schedule cannot introduce free reads
or more expensive feedback branches. -/
theorem withCornerClock_fits {O : Type}
    (cornerSchedule : List (Fin 24))
    {n : Nat} {tree : Policy TaggedEdgeAddress Nat O}
    (bounded : Fits n tree) :
    Fits n (withCornerClock cornerSchedule tree) := by
  induction bounded generalizing cornerSchedule with
  | stop n output =>
      exact Fits.stop n output
  | read n query next branches ih =>
      exact Fits.read n (query, cornerSchedule.headD 0) _
        (fun response => ih response.1 cornerSchedule.tail)

/-- The extra corner sensor cannot alter the edge continuation output,
for ANY corner-color assignment and ANY original edge word. In
particular, no hidden corner sign can enter the next edge decision. -/
theorem withCornerClock_run {O : Type}
    (cornerSchedule : List (Fin 24))
    (tree : Policy TaggedEdgeAddress Nat O)
    (state : TaggedPairedState) :
    (withCornerClock cornerSchedule tree).run taggedPairedObserve state =
      tree.run taggedEdgeObserve state.1 := by
  induction tree generalizing cornerSchedule with
  | stop output => rfl
  | read edgeAddress next ih =>
      change
        (withCornerClock cornerSchedule.tail
          (next (taggedEdgeObserve state.1 edgeAddress))).run
          taggedPairedObserve state =
        (next (taggedEdgeObserve state.1 edgeAddress)).run
          taggedEdgeObserve state.1
      exact ih (taggedEdgeObserve state.1 edgeAddress)
        cornerSchedule.tail

/-- Extract the corner address of each actual paired query. The
recording includes every padding step; it does NOT suppress a repeated
corner reading merely because the edge output has stopped changing. -/
def observedCornerAddresses {O : Type}
    (cornerSchedule : List (Fin 24))
    (tree : Policy TaggedEdgeAddress Nat O)
    (state : TaggedPairedState) : List (Fin 24) :=
  ((withCornerClock cornerSchedule tree).transcript
    taggedPairedObserve state).map (fun answered => answered.1.2)

/-- If the schedule has exactly as many slots as the executed edge
transcript, the paired controller reads every scheduled corner address
in order. This makes it impossible to promote the terminal corner sign
before its last scheduled address has actually been observed. -/
theorem observed_corner_addresses_eq_schedule {O : Type}
    (tree : Policy TaggedEdgeAddress Nat O)
    (state : TaggedPairedState) :
    ∀ cornerSchedule : List (Fin 24),
      cornerSchedule.length =
          (tree.transcript taggedEdgeObserve state.1).length →
      observedCornerAddresses cornerSchedule tree state = cornerSchedule := by
  induction tree with
  | stop output =>
      intro cornerSchedule count
      cases cornerSchedule with
      | nil =>
          rfl
      | cons head tail =>
          simp [Policy.transcript] at count
  | read edgeAddress next ih =>
      intro cornerSchedule count
      cases cornerSchedule with
      | nil =>
          simp [Policy.transcript] at count
      | cons first remaining =>
          have countRest :
              remaining.length =
                ((next (taggedEdgeObserve state.1 edgeAddress)).transcript
                    taggedEdgeObserve state.1).length := by
            simpa [Policy.transcript] using count
          have recursive :=
            ih (taggedEdgeObserve state.1 edgeAddress)
              remaining countRest
          simpa [observedCornerAddresses, withCornerClock,
            Policy.transcript, taggedPairedObserve] using
            congrArg (List.cons first) recursive

/-- A complete nineteen-frame paired *abstract* policy. This theorem
does not assert that every legal cube's first eleven colors have been
transported to the 52 original representative roots; nor that the
tagged edge addresses have been physically routed by face turns. -/
def exactNineteenPairedRoots (roots : Array Lean.Json) :
    Policy (TaggedEdgeAddress × Fin 24) (Nat × Nat)
      (Bool → Option Word) :=
  withCornerClock cornerFrameAddresses (exactNineteenTagged roots)

theorem exact_nineteen_paired_roots_fits (roots : Array Lean.Json) :
    Fits 19 (exactNineteenPairedRoots roots) := by
  exact withCornerClock_fits cornerFrameAddresses
    (exact_nineteen_tagged_fits roots)

theorem exact_nineteen_paired_roots_corner_addresses
    (roots : Array Lean.Json) (state : TaggedPairedState) :
    observedCornerAddresses cornerFrameAddresses
      (exactNineteenTagged roots) state = cornerFrameAddresses := by
  apply observed_corner_addresses_eq_schedule
  rw [actual_corner_frame_budget,
    exact_nineteen_tagged_transcript_length]

theorem exact_nineteen_paired_roots_run
    (roots : Array Lean.Json) (state : TaggedPairedState) :
    (exactNineteenPairedRoots roots).run taggedPairedObserve state =
      (exactNineteenTagged roots).run taggedEdgeObserve state.1 := by
  exact withCornerClock_run cornerFrameAddresses
    (exactNineteenTagged roots) state

/-- The final fresh corner sticker is still the NINETEENTH original
corner read. Earlier repetitions cannot advance the sign-release
position. -/
theorem final_corner_sticker_is_nineteenth_paired_read
    (roots : Array Lean.Json) (state : TaggedPairedState) :
    (observedCornerAddresses cornerFrameAddresses
      (exactNineteenTagged roots) state)[18]! = (4 : Fin 24) := by
  rw [exact_nineteen_paired_roots_corner_addresses]
  exact final_corner_color_not_early.2

/-- Full certified-root integration on the genuine paired address/channel:
for every original candidate of the SELECTED frozen representative,
nineteen simultaneous edge/corner replies return the correct signed
edge candidate. The chosen sign is evaluated only on the final
returned decoder, not while selecting any edge read.
This theorem remains about original-coordinate tagged pairs, not
yet the physical face-turn route or all 1,362 noncanonical prefixes. -/
theorem exact_nineteen_paired_recovers_matching_actual_root
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (entry : Lean.Json) (member : entry ∈ roots.toList)
    (word : Word) (corner : Fin 24 → Nat)
    (selected : matchingFrozenRoot roots
      (firstElevenTagged.map (taggedEdgeObserve word)) = some entry)
    (graph : Array (FrozenInstruction Nat Nat Unit))
    (belief : List Word)
    (entryParsed : parseRepresentativeRoot entry = .ok (graph, belief))
    (candidate : word ∈ belief) :
    ((exactNineteenPairedRoots roots).run taggedPairedObserve
        (word, corner)) (edgeWordSign word) = some word := by
  rw [exact_nineteen_paired_roots_run]
  exact exact_nineteen_tagged_recovers_matching_actual_root
    roots parsed entry member word selected graph belief entryParsed candidate

/-- Extract the actual CORNER COLOR, not merely the corner address,
from each physically charged abstract paired observation. -/
def observedCornerColors {O : Type}
    (cornerSchedule : List (Fin 24))
    (tree : Policy TaggedEdgeAddress Nat O)
    (state : TaggedPairedState) : List Nat :=
  ((withCornerClock cornerSchedule tree).transcript
    taggedPairedObserve state).map (fun answered => answered.2.2)

/-- Every returned corner color is exactly the color of its scheduled
original-coordinate corner sticker, when the charged schedule has
the same number of entries as the executed edge transcript. -/
theorem observed_corner_colors_eq_schedule {O : Type}
    (tree : Policy TaggedEdgeAddress Nat O)
    (state : TaggedPairedState) :
    ∀ cornerSchedule : List (Fin 24),
      cornerSchedule.length =
          (tree.transcript taggedEdgeObserve state.1).length →
      observedCornerColors cornerSchedule tree state =
        cornerSchedule.map state.2 := by
  induction tree with
  | stop output =>
      intro cornerSchedule count
      cases cornerSchedule with
      | nil => rfl
      | cons head tail => simp [Policy.transcript] at count
  | read edgeAddress next ih =>
      intro cornerSchedule count
      cases cornerSchedule with
      | nil => simp [Policy.transcript] at count
      | cons first remaining =>
          have countRest :
              remaining.length =
                ((next (taggedEdgeObserve state.1 edgeAddress)).transcript
                  taggedEdgeObserve state.1).length := by
            simpa [Policy.transcript] using count
          have recursive :=
            ih (taggedEdgeObserve state.1 edgeAddress)
              remaining countRest
          simpa [observedCornerColors, withCornerClock,
            Policy.transcript, taggedPairedObserve] using
            congrArg (List.cons (state.2 first)) recursive

theorem exact_nineteen_paired_roots_corner_colors
    (roots : Array Lean.Json) (state : TaggedPairedState) :
    observedCornerColors cornerFrameAddresses
      (exactNineteenTagged roots) state =
        cornerFrameAddresses.map state.2 := by
  apply observed_corner_colors_eq_schedule
  rw [actual_corner_frame_budget,
    exact_nineteen_tagged_transcript_length]

/-- Direct bridge to the previously proved REAL scheduled-corner
transcript of a 48-facelet coloring. We do not guess the corner colors:
the paired controller has actually received them in frame order. -/
theorem exact_nineteen_paired_corner_colors_match_colorings
    (roots : Array Lean.Json) (word : Word)
    (original : Coloring) :
    observedCornerColors cornerFrameAddresses
      (exactNineteenTagged roots)
      (word, fun addr => original (cornerSlot addr)) =
        scheduledCornerColors original := by
  simpa [scheduledCornerColors] using
    (exact_nineteen_paired_roots_corner_colors roots
      (word, fun addr => original (cornerSlot addr)))

/-- Two legal original cubes with identical executed nineteen paired
corner-color records must agree on ALL 24 original corner stickers.
Their edge words may differ. This is exactly the necessary conditional
identifiability consequence of the fixed physical corner schedule;
the final edge proof and actual move-route compiler remain separate. -/
theorem same_paired_corner_colors_force_all_legal_corners
    (roots : Array Lean.Json)
    (word₁ word₂ : Word)
    (original₁ original₂ : Coloring)
    (legal₁ : Reachable original₁)
    (legal₂ : Reachable original₂)
    (same :
      observedCornerColors cornerFrameAddresses
          (exactNineteenTagged roots)
          (word₁, fun addr => original₁ (cornerSlot addr)) =
        observedCornerColors cornerFrameAddresses
          (exactNineteenTagged roots)
          (word₂, fun addr => original₂ (cornerSlot addr))) :
    ∀ i : Fin 8, ∀ j : Fin 3,
      original₁ (cornerRawSlot i j) =
        original₂ (cornerRawSlot i j) := by
  have leftEq :=
    exact_nineteen_paired_corner_colors_match_colorings
      roots word₁ original₁
  have rightEq :=
    exact_nineteen_paired_corner_colors_match_colorings
      roots word₂ original₂
  have sameScheduled :
      scheduledCornerColors original₁ =
        scheduledCornerColors original₂ :=
    leftEq.symm.trans (same.trans rightEq)
  exact same_nineteen_corner_answers_force_all_corner_colors
    original₁ original₂ legal₁ legal₂ sameScheduled

#print axioms withCornerClock_fits
#print axioms withCornerClock_run
#print axioms observed_corner_addresses_eq_schedule
#print axioms exact_nineteen_paired_roots_fits
#print axioms exact_nineteen_paired_roots_corner_addresses
#print axioms exact_nineteen_paired_roots_run
#print axioms final_corner_sticker_is_nineteenth_paired_read
#print axioms exact_nineteen_paired_recovers_matching_actual_root
#print axioms observed_corner_colors_eq_schedule
#print axioms exact_nineteen_paired_roots_corner_colors
#print axioms exact_nineteen_paired_corner_colors_match_colorings
#print axioms same_paired_corner_colors_force_all_legal_corners

/-- Keep the edge policy's terminal output AND the charged corner replies.
The next edge branch depends only on the edge reply. The accumulated
corner record is returned at the leaf, never supplied to that branch. -/
def withRecordedCornerClock {Q O : Type}
    (schedule : List (Fin 24)) (rev : List Nat) :
    Policy Q Nat O → Policy (Q × Fin 24) FrameColor (O × List Nat)
  | .stop output => .stop (output, rev.reverse)
  | .read address next =>
      .read (address, schedule.headD 0) (fun reply =>
        withRecordedCornerClock schedule.tail (reply.2 :: rev) (next reply.1))

theorem withRecordedCornerClock_fits {Q O : Type}
    (schedule : List (Fin 24)) (rev : List Nat)
    {n : Nat} {tree : Policy Q Nat O} (fit : Fits n tree) :
    Fits n (withRecordedCornerClock schedule rev tree) := by
  induction fit generalizing schedule rev with
  | stop n output => exact .stop n _
  | read n address next branches ih =>
      exact .read n (address, schedule.headD 0) _
        (fun reply => ih reply.1 schedule.tail (reply.2 :: rev))

/-- On a path with exactly the scheduled length, the returned decoder
and corner record are the actual edge run and the actual charged colors.
The state appears only in this semantic theorem, not in the controller. -/
theorem withRecordedCornerClock_run {S Q O : Type}
    (edge : S → Q → Nat) (corner : S → Fin 24 → Nat)
    (s : S) (tree : Policy Q Nat O)
    (schedule : List (Fin 24)) (rev : List Nat)
    (count : schedule.length = (tree.transcript edge s).length) :
    (withRecordedCornerClock schedule rev tree).run
        (fun state q => (edge state q.1, corner state q.2)) s =
      (tree.run edge s, rev.reverse ++ schedule.map (corner s)) := by
  induction tree generalizing schedule rev with
  | stop output =>
      cases schedule with
      | nil => simp [withRecordedCornerClock, Policy.run]
      | cons head tail => simp [Policy.transcript] at count
  | read address next ih =>
      cases schedule with
      | nil => simp [Policy.transcript] at count
      | cons first rest =>
          have hrest : rest.length =
              ((next (edge s address)).transcript edge s).length := by
            simpa [Policy.transcript] using count
          change (withRecordedCornerClock rest (corner s first :: rev)
            (next (edge s address))).run
              (fun state q => (edge state q.1, corner state q.2)) s =
            ((next (edge s address)).run edge s,
              rev.reverse ++ (first :: rest).map (corner s))
          rw [ih (edge s address) rest (corner s first :: rev) hrest]
          simp [List.reverse_cons, List.append_assoc]

#print axioms withRecordedCornerClock_fits
#print axioms withRecordedCornerClock_run

/-- The root found by the executable selector, not an arbitrary existential
witness, recovers the normalized complete word. -/
theorem selected_normalized_continuation_recovers
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (word : Word) (complete : (wordLabels word).Perm (List.range 12))
    (hflip : flipBit word = 0)
    (replies : List FrameColor) (hlen : replies.length = 11)
    (hfst : replies.map Prod.fst = (word.take 11).map (fun e => sticker e false)) :
    let normalized := adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank replies))
      (relabelEdgeWord (chosenPrefixColorMap replies) word)
    ((continuationFromFrozenRoots roots (normalizedPrefix replies)).run
      observation normalized) (edgeWordSign normalized) = some normalized := by
  dsimp only
  obtain ⟨ws, x, hw⟩ : ∃ ws x, word = ws ++ [x] := by
    rcases List.eq_nil_or_concat word with h | ⟨L, b, h⟩
    · subst h; simp [wordLabels] at complete
    · exact ⟨L, b, by rw [h, List.concat_eq_append]⟩
  have wlen : word.length = 12 := by simpa [wordLabels] using complete.length_eq
  have wslen : ws.length = 11 := by subst hw; simp at wlen; omega
  have htake : word.take 11 = ws := by
    subst hw; exact List.take_left' wslen
  obtain ⟨o, ho, row, hrow, hp⟩ := first_eleven_row_perm ws x (hw ▸ complete)
  have hcol : ∀ c ∈ replies.map Prod.fst, c ∈ collation := by
    intro c hc
    rw [hfst, htake] at hc
    obtain ⟨e, he, rfl⟩ := List.mem_map.1 hc
    have hm : e / 2 ∈ List.range 12 :=
      complete.subset (by
        unfold wordLabels
        exact List.mem_map.2 ⟨e, by rw [hw]; exact List.mem_append_left _ he, rfl⟩)
    have := List.mem_range.1 hm
    exact sticker_mem_collation e (by omega)
  have covered := normalized_prefix_has_certified_root roots parsed
    representative_prefixes_covered_source replies hlen hcol row
    (List.mem_flatMap.2 ⟨o, ho, hrow⟩) (by rw [hfst, htake]; exact hp)
  obtain ⟨entry, hentry, hselected, hroot⟩ :=
    matching_frozen_root_total roots (normalizedPrefix replies) covered
  obtain ⟨graph, belief, hparse, hrec⟩ :=
    every_actual_frozen_root_recovers roots parsed entry hentry
  have hbelief := parse_root_belief entry graph belief _ hparse hroot
  have hsector := normalized_word_in_prefix_sector word complete hflip replies hlen hfst
  rw [← hbelief] at hsector
  simp only [continuationFromFrozenRoots, hselected, hparse]
  exact hrec _ hsector

#print axioms selected_normalized_continuation_recovers

/-- The production continuation receives only the real eleven replies.
It transports the sector queries and records the eight remaining corner
colors, with real padding on every branch (including malformed histories). -/
def physicalRecordedContinuation (roots : Array Lean.Json) (pre : List FrameColor) :
    Policy (Fin 24 × Fin 24) FrameColor
      (List FrameColor × ((Bool → Option Word) × List Nat)) :=
  (withRecordedCornerClock (cornerFrameAddresses.drop 11)
    (pre.map Prod.snd).reverse
    ((continuationFromFrozenRoots roots (normalizedPrefix pre)).padToExact 0 8)).adapt
      (fun q => (physicalSectorAddress pre q.1, q.2))
      (fun _ r => ((chosenPrefixColorMap pre)[r.1]!, r.2))
      (fun result => (pre, result))

theorem physical_recorded_continuation_fits
    (roots : Array Lean.Json) (pre : List FrameColor) :
    Fits 8 (physicalRecordedContinuation roots pre) := by
  unfold physicalRecordedContinuation
  apply Policy.adapt_fits
  apply withRecordedCornerClock_fits
  exact Policy.padToExact_fits 0
    (continuation_from_frozen_roots_fits roots (normalizedPrefix pre))

/-- One actual paired-address controller, not a family selected by an
unobserved state. Its leaf retains the gauge input and charged corner
record for the terminal inverse decoder. -/
def physicalNineteenRecorded (roots : Array Lean.Json) :
    Policy (Fin 24 × Fin 24) FrameColor
      (List FrameColor × ((Bool → Option Word) × List Nat)) :=
  Policy.withPrefix firstElevenPairedAddresses []
    (physicalRecordedContinuation roots)

theorem physical_nineteen_recorded_fits (roots : Array Lean.Json) :
    Fits 19 (physicalNineteenRecorded roots) := by
  have h := Policy.withPrefix_fits firstElevenPairedAddresses []
    (physicalRecordedContinuation roots) (physical_recorded_continuation_fits roots)
  simpa [physicalNineteenRecorded, first_eleven_address_count] using h

#print axioms physical_recorded_continuation_fits
#print axioms physical_nineteen_recorded_fits

/-- The real transported run returns the same terminal decoder as the
normalized sector and the exact charged corner record. No sign is
evaluated and no inverse is applied until after this run. -/
theorem physical_recorded_continuation_run
    (roots : Array Lean.Json) (pre : List FrameColor) (turns : List Turn) :
    let norm := adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank pre))
      (relabelEdgeWord (chosenPrefixColorMap pre) (originalPhysicalEdgeWord turns))
    (physicalRecordedContinuation roots pre).run abstractPairRead (paint turns solved) =
      (pre, ( (continuationFromFrozenRoots roots (normalizedPrefix pre)).run observation norm,
        pre.map Prod.snd ++ (cornerFrameAddresses.drop 11).map
          (fun addr => paint turns solved (cornerSlot addr)))) := by
  dsimp only
  let tree := continuationFromFrozenRoots roots (normalizedPrefix pre)
  let edge : Coloring → Nat → Nat := fun s q =>
    (chosenPrefixColorMap pre)[s (edgeNumber (physicalSectorAddress pre q))]!
  let corner : Coloring → Fin 24 → Nat := fun s c => s (cornerSlot c)
  let s := paint turns solved
  let norm := adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank pre))
    (relabelEdgeWord (chosenPrefixColorMap pre) (originalPhysicalEdgeWord turns))
  have fit : Fits 8 tree := continuation_from_frozen_roots_fits roots _
  have count : (cornerFrameAddresses.drop 11).length =
      ((tree.padToExact 0 8).transcript edge s).length := by
    rw [Policy.padToExact_transcript_length 0 edge s fit]
    decide +kernel
  have clock := withRecordedCornerClock_run edge corner s
    (tree.padToExact 0 8) (cornerFrameAddresses.drop 11)
    (pre.map Prod.snd).reverse count
  have same : tree.run edge s = tree.run observation norm := by
    apply Policy.run_fixed_reply_equiv
    intro q
    exact (physical_normalized_sector_observation turns pre q).symm
  have pad := Policy.padToExact_run 0 edge s fit
  unfold physicalRecordedContinuation
  rw [Policy.adapt_run]
  change (pre, (withRecordedCornerClock (cornerFrameAddresses.drop 11)
    (pre.map Prod.snd).reverse (tree.padToExact 0 8)).run
      (fun state q => (edge state q.1, corner state q.2)) s) = _
  rw [clock, pad, same, List.reverse_reverse]

#print axioms physical_recorded_continuation_run

/-- Undo the actual observed-prefix gauge and position permutation.
Only the returned representative word and the charged prefix are inputs. -/
def restoredEdgeCoordinates (pre : List FrameColor) (word : Word) : EdgeCoordinates :=
  fun i => relabelEdgeValue (inverseColorTable (chosenPrefixColorMap pre))
    word[((bubbleCandidateSlotOrder (frozenPrefixColorRank pre)).backward i).val]!

theorem restored_edge_coordinates_correct (pre : List FrameColor) (turns : List Turn) :
    restoredEdgeCoordinates pre
      (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank pre))
        (relabelEdgeWord (chosenPrefixColorMap pre) (originalPhysicalEdgeWord turns))) =
      edgeCoordinatesAlong turns := by
  funext i
  let order := bubbleCandidateSlotOrder (frozenPrefixColorRank pre)
  let sigma := chosenPrefixColorMap pre
  have hcan : ∀ k : Fin 12, canonicalEdgeSources[k.val]? = some k := by
    decide +kernel
  have hall : ∀ k : Fin 12, k ∈ canonicalEdgeSources := by
    decide +kernel
  have hmem : edgeCoordinatesAlong turns i / 2 ∈ canonicalEdgeSources.map Fin.val := by
    apply (edge_coordinates_along_piece_perm turns).subset
    exact List.mem_map.mpr ⟨i, hall i, rfl⟩
  obtain ⟨k, _, hk⟩ := List.mem_map.mp hmem
  have hlt : edgeCoordinatesAlong turns i / 2 < 12 := by
    rw [← hk]
    exact k.isLt
  have hword : edgeCoordinatesAlong turns i < 24 := by omega
  have hlen : (relabelEdgeWord sigma (originalPhysicalEdgeWord turns)).length = 12 := by
    simp [relabelEdgeWord, originalPhysicalEdgeWord, canonicalEdgeSources]
  have hget :
      (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank pre))
        (relabelEdgeWord sigma (originalPhysicalEdgeWord turns)))[(order.backward i).val]? =
        some (relabelEdgeValue sigma (edgeCoordinatesAlong turns i)) := by
    rw [bubble_candidate_slot_order_matches_actual_replay
      (frozenPrefixColorRank pre) _ hlen (order.backward i)]
    change (relabelEdgeWord sigma (originalPhysicalEdgeWord turns))
      [(order.forward (order.backward i)).val]? = _
    rw [order.left_inv, relabelEdgeWord, List.getElem?_map,
      originalPhysicalEdgeWord, List.getElem?_map, hcan i]
    rfl
  change relabelEdgeValue (inverseColorTable sigma)
    (adjTrace (bubbleCandidatePath11 (frozenPrefixColorRank pre))
      (relabelEdgeWord sigma (originalPhysicalEdgeWord turns)))[(order.backward i).val]! = _
  rw [List.getElem!_of_getElem? hget]
  exact inverse_color_table_restores_oriented_edge sigma
    (chosen_prefix_color_map_legal pre) ⟨edgeCoordinatesAlong turns i, hword⟩

#print axioms restored_edge_coordinates_correct

/-- Rebuild all 48 original moving stickers from the two recovered
coordinate arrays. No physical state or move-history witness is an input. -/
def rebuildColoring (edges : EdgeCoordinates) (corners : CornerCoordinates) : Coloring :=
  fun slot =>
    if slot.val < 24 then
      sticker (edges ⟨slot.val / 2 % 12, Nat.mod_lt _ (by decide)⟩)
        (slot.val % 2 == 1)
    else
      orientedCornerColor
        (corners ⟨(slot.val - 24) / 3 % 8, Nat.mod_lt _ (by decide)⟩)
        ⟨(slot.val - 24) % 3, Nat.mod_lt _ (by decide)⟩

theorem rebuild_coloring_correct (edges : EdgeCoordinates)
    (corners : CornerCoordinates) (s : Coloring)
    (he : EdgesAgree edges s) (hc : CornersAgree corners s) :
    rebuildColoring edges corners = s := by
  have cover : ∀ slot : Slot,
      (∃ i : Fin 12, ∃ b : Bool, slot = edgeSlot i b) ∨
      (∃ i : Fin 8, ∃ j : Fin 3, slot = cornerRawSlot i j) := by
    decide +kernel
  have edgeIndex : ∀ i : Fin 12, ∀ b : Bool,
      (edgeSlot i b).val < 24 ∧
      (⟨(edgeSlot i b).val / 2 % 12, Nat.mod_lt _ (by decide)⟩ : Fin 12) = i ∧
      ((edgeSlot i b).val % 2 == 1) = b := by
    decide +kernel
  have cornerIndex : ∀ i : Fin 8, ∀ j : Fin 3,
      ¬ (cornerRawSlot i j).val < 24 ∧
      (⟨((cornerRawSlot i j).val - 24) / 3 % 8, Nat.mod_lt _ (by decide)⟩ : Fin 8) = i ∧
      (⟨((cornerRawSlot i j).val - 24) % 3, Nat.mod_lt _ (by decide)⟩ : Fin 3) = j := by
    decide +kernel
  funext slot
  rcases cover slot with ⟨i, b, rfl⟩ | ⟨i, j, rfl⟩
  · obtain ⟨h, hi, hb⟩ := edgeIndex i b
    simp only [rebuildColoring, if_pos h, hi, hb]
    exact (he i b).symm
  · obtain ⟨h, hi, hj⟩ := cornerIndex i j
    simp only [rebuildColoring, if_neg h, hi, hj]
    exact (hc i j).symm

#print axioms rebuild_coloring_correct

end CubeRev029.Nineteen

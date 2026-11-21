import TaggedNineteenRootPolicy
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

end CubeRev029.Nineteen

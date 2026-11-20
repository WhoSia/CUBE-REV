import EdgeOperations
import RootCoordinates

namespace CubeRev029.Physical

open Eighteen

/-- A bounded even trace can be applied in pairs, because each pair is
provided with a face-turn realization that preserves the solved corners. -/
theorem even_trace_reachable (act : Nat → Word → Word) (width : Nat)
    (lengths : ∀ i w, (act i w).length = w.length)
    (pairs : ∀ w, w.length = 12 → Reachable (encodeEdges w) → ∀ i j : Fin width,
      Reachable (encodeEdges (act j.val (act i.val w))))
    (path : List Nat) (w : Word) (len : w.length = 12)
    (reached : Reachable (encodeEdges w))
    (bounds : ∀ i ∈ path, i < width) (even : path.length % 2 = 0) :
    Reachable (encodeEdges (path.foldl (fun state i => act i state) w)) := by
  match path with
  | [] => exact reached
  | [_] => simp at even
  | i :: j :: rest =>
      have bi : i < width := bounds i (by simp)
      have bj : j < width := bounds j (by simp)
      have shorter : rest.length % 2 = 0 := by simp only [List.length_cons] at even; omega
      exact even_trace_reachable act width lengths pairs rest (act j (act i w))
        (by rw [lengths, lengths, len]) (pairs w len reached ⟨i, bi⟩ ⟨j, bj⟩)
        (fun x mem => bounds x (by simp [mem])) shorter
termination_by path.length

theorem adjTrace_foldl (path : List Nat) (w : Word) :
    adjTrace path w = path.foldl (fun state i => adjacent i state) w := by
  induction path generalizing w with
  | nil => rfl
  | cons _ _ ih => exact ih _

theorem flipTrace_foldl (path : List Nat) (w : Word) :
    flipTrace path w = path.foldl (fun state i => flipAt i state) w := by
  induction path generalizing w with
  | nil => rfl
  | cons _ _ ih => exact ih _

/-- Construct every admissible even-sector edge assignment using geometric
face quarter-turns from solved, with every corner sticker restored. -/
theorem solved_corners_even_sector_reachable {w : Word} (legal : Completes (root 0) w) :
    Reachable (encodeEdges w) := by
  obtain ⟨order, ordered, bounded, even⟩ := root_even_swap_path legal
  let initial : Word := (List.range 12).map (2*·)
  have base : Reachable (encodeEdges initial) := by rw [encode_identity]; exact solved_reachable
  have labelsReach := even_trace_reachable adjacent 11 adjacent_length reachable_adjacent_pair
    order initial (by simp [initial]) base bounded even
  rw [← adjTrace_foldl, ← adjTrace_map, ordered, ← unflipped_is_label_embedding] at labelsReach
  obtain ⟨flips, ends, bounds, even⟩ := root_even_flip_path legal
  have result := even_trace_reachable flipAt 12 flipAt_length reachable_flip_pair flips
    (unflipped w) (by simp [unflipped, root_length legal]) labelsReach
    (by intro i mem; simpa [root_length legal] using bounds i mem) even
  rwa [← flipTrace_foldl, ends] at result

#print axioms solved_corners_even_sector_reachable

end CubeRev029.Physical

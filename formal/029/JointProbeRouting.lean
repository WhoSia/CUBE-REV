import PhysicalObservation
import ProbeRouteWords

namespace CubeRev029.Physical

def edgeNumber (a : Fin 24) : Slot := ⟨a.val, by have := a.isLt; omega⟩
def jointPath (edge corner : Fin 24) : List Turn :=
  jointProbeTable[24 * edge.val + corner.val]!

theorem joint_routes_checked : jointProbeTable.size = 576 ∧
    ∀ e c : Fin 24, follow (jointPath e c) (edgeNumber 0) = edgeNumber e ∧
                     follow (jointPath e c) (cornerSlot 0) = cornerSlot c := by
  native_decide

def inversePath (path : List Turn) : List Turn :=
  (path.map inverseTurn).reverse

theorem follow_append (a b : List Turn) (s : Slot) :
    follow (a ++ b) s = follow b (follow a s) := by
  simp [follow, List.foldl_append]

theorem follow_undo (path : List Turn) (s : Slot) :
    follow (inversePath path) (follow path s) = s := by
  induction path generalizing s with
  | nil => rfl
  | cons head tail ih =>
      simp only [inversePath, List.map_cons, List.reverse_cons]
      change follow (inversePath tail ++ [inverseTurn head]) (follow tail (turnSlot head s)) = s
      rw [follow_append, ih]
      exact turn_inverse head s

/-- A single known turn word simultaneously brings any desired initial edge
and corner sticker to any two fixed sector-appropriate probes. -/
theorem joint_any_probes (pe pc te tc : Fin 24) :
    ∃ moves : List Turn, follow moves (edgeNumber pe) = edgeNumber te ∧
      follow moves (cornerSlot pc) = cornerSlot tc := by
  let undo := inversePath (jointPath pe pc)
  have base := joint_routes_checked.2 pe pc
  have goal := joint_routes_checked.2 te tc
  have reachEdge : follow undo (edgeNumber pe) = edgeNumber 0 := by
    rw [← base.1]
    exact follow_undo _ _
  have reachCorner : follow undo (cornerSlot pc) = cornerSlot 0 := by
    rw [← base.2]
    exact follow_undo _ _
  refine ⟨undo ++ jointPath te tc, ?_, ?_⟩
  · calc
      follow (undo ++ jointPath te tc) (edgeNumber pe) =
          follow (jointPath te tc) (follow undo (edgeNumber pe)) := follow_append _ _ _
      _ = follow (jointPath te tc) (edgeNumber 0) := congrArg (follow _) reachEdge
      _ = edgeNumber te := goal.1
  · calc
      follow (undo ++ jointPath te tc) (cornerSlot pc) =
          follow (jointPath te tc) (follow undo (cornerSlot pc)) := follow_append _ _ _
      _ = follow (jointPath te tc) (cornerSlot 0) := congrArg (follow _) reachCorner
      _ = cornerSlot tc := goal.2

theorem inverseTurn_twice : ∀ t : Turn, inverseTurn (inverseTurn t) = t := by
  decide +kernel

theorem follow_undo_forward (path : List Turn) (s : Slot) :
    follow path (follow (inversePath path) s) = s := by
  induction path generalizing s with
  | nil => rfl
  | cons head tail ih =>
      simp only [inversePath, List.map_cons, List.reverse_cons]
      change follow tail (turnSlot head (follow (inversePath tail ++ [inverseTurn head]) s)) = s
      rw [follow_append]
      have cancel (q : Slot) : turnSlot head (turnSlot (inverseTurn head) q) = q := by
        have h := turn_inverse (inverseTurn head) q
        rwa [inverseTurn_twice] at h
      change follow tail
        (turnSlot head (turnSlot (inverseTurn head) (follow (inversePath tail) s))) = s
      rw [cancel, ih]

/-- The controller can pull the desired two initial colors to the probes
after any previously executed pose. Neither prior pose nor requested
addresses depend on the two replies of the current frame. -/
theorem joint_frame_after_pose (pe pc te tc : Fin 24) (prior : List Turn) :
    ∃ step : List Turn, ∀ orig : Coloring,
      (paint step (paint prior orig) (edgeNumber pe),
       paint step (paint prior orig) (cornerSlot pc)) =
      (orig (edgeNumber te), orig (cornerSlot tc)) := by
  obtain ⟨setup, he, hc⟩ := joint_any_probes pe pc te tc
  refine ⟨setup ++ inversePath prior, fun orig => ?_⟩
  have e : follow prior (follow (setup ++ inversePath prior) (edgeNumber pe)) = edgeNumber te := by
    rw [follow_append, he, follow_undo_forward]
  have c : follow prior (follow (setup ++ inversePath prior) (cornerSlot pc)) = cornerSlot tc := by
    rw [follow_append, hc, follow_undo_forward]
  exact Prod.ext (congrArg orig e) (congrArg orig c)

/-- The algebraic lookup convention is exactly chronological execution of
the same quarter-turn actions in reverse storage order. -/
theorem paint_chronological (moves : List Turn) (state : Coloring) :
    paint moves state = moves.reverse.foldl (fun c t => turnColoring t c) state := by
  induction moves with
  | nil => rfl
  | cons a tail ih => simp [paint_cons, List.reverse_cons, List.foldl_append, ← ih]

#print axioms joint_any_probes
#print axioms joint_frame_after_pose

end CubeRev029.Physical

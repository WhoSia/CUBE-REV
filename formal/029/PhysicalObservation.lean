import SolvedCornerReachable

namespace CubeRev029.Physical

open Eighteen

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem turn_preserves_sector :
    ∀ t : Turn, ∀ s : Slot, (turnSlot t s).val < 24 ↔ s.val < 24 := by decide +kernel

theorem follow_preserves_sector (path : List Turn) (s : Slot) :
    (follow path s).val < 24 ↔ s.val < 24 := by
  induction path generalizing s with
  | nil => rfl
  | cons t rest ih => exact (ih (turnSlot t s)).trans (turn_preserves_sector t s)

def cornerSlot (c : Fin 24) : Slot :=
  ⟨24 + c.val, by have := c.isLt; omega⟩

abbrev FrameColor := Nat × Nat
abbrev EdgeProbe := Fin 12 × Bool

def probes (e : EdgeProbe) (c : Fin 24) (state : Coloring) : FrameColor :=
  (state (edgeSlot e.1 e.2), state (cornerSlot c))

def queryEdge (e : EdgeProbe) (path : List Turn) : Address :=
  let slot := follow path (edgeSlot e.1 e.2)
  (slot.val / 2, slot.val % 2 == 1)

def supplyCorner (c : Fin 24) (path : List Turn) (edge : Nat) : FrameColor :=
  (edge, solved (follow path (cornerSlot c)))

/-- With solved initial corners, the edge sector is the only unknown
source of color in a frame, independent of the turn path. -/
theorem observe_encoded (e : EdgeProbe) (c : Fin 24) (w : Word) (path : List Turn) :
    probes e c (paint path (encodeEdges w)) =
      supplyCorner c path (observeWord w (queryEdge e path)) := by
  have inEdge := (follow_preserves_sector path (edgeSlot e.1 e.2)).mpr (edgeSlot_inside e.1 e.2)
  have inCorner : ¬ (follow path (cornerSlot c)).val < 24 :=
    fun small => by
      have bad := (follow_preserves_sector path (cornerSlot c)).mp small
      change 24+c.val < 24 at bad
      omega
  change (encodeEdges w (follow path (edgeSlot e.1 e.2)),
    encodeEdges w (follow path (cornerSlot c))) = _
  simp [encodeEdges, inEdge, inCorner, supplyCorner, queryEdge]

def runFrames (e : EdgeProbe) (c : Fin 24) (state : Coloring) :
    Policy (List Turn) FrameColor O → O
  | .stop output => output
  | .read path next =>
      let moved := paint path state
      runFrames e c moved (next (probes e c moved))

def frameTranscript (e : EdgeProbe) (c : Fin 24) (state : Coloring) :
    Policy (List Turn) FrameColor O → List (List Turn × FrameColor)
  | .stop _ => []
  | .read path next =>
      let moved := paint path state
      let reply := probes e c moved
      (path, reply) :: frameTranscript e c moved (next reply)

def accumulate (prior : List Turn) : Policy (List Turn) FrameColor O → Policy (List Turn) FrameColor O
  | .stop output => .stop output
  | .read path next =>
      .read (path ++ prior) (fun r => accumulate (path ++ prior) (next r))

theorem accumulate_fits (prior : List Turn) {tree : Policy (List Turn) FrameColor O}
    (h : Fits n tree) : Fits n (accumulate prior tree) := by
  induction h generalizing prior with
  | stop n output => exact .stop n output
  | read n path next fit ih => exact .read n (path ++ prior) _ (fun r => ih r (path ++ prior))

theorem accumulated_run (e : EdgeProbe) (c : Fin 24) (state : Coloring)
    (tree : Policy (List Turn) FrameColor O) (prior : List Turn) :
    (accumulate prior tree).run (fun x path => probes e c (paint path x)) state =
      runFrames e c (paint prior state) tree := by
  induction tree generalizing prior with
  | stop _ => rfl
  | read path next ih =>
      simp only [accumulate, Policy.run, runFrames, ← paint_append]
      exact ih _ _

theorem frame_logging (e : EdgeProbe) (c : Fin 24) (state : Coloring)
    (tree : Policy (List Turn) FrameColor O) (past : List (List Turn × FrameColor)) :
    runFrames e c state (tree.logged past) = past.reverse ++ frameTranscript e c state tree := by
  induction tree generalizing past state with
  | stop _ => simp [runFrames, Policy.logged, frameTranscript]
  | read path next ih =>
      simp only [runFrames, Policy.logged, frameTranscript]
      rw [ih]
      simp [List.reverse_cons, List.append_assoc]

/-- Observation adapters need agree only on the state being replayed. -/
theorem run_congr_state (tree : Policy Q R O) (a : A) (b : B)
    (f : A → Q → R) (g : B → Q → R) (agree : ∀ q, f a q = g b q) :
    tree.run f a = tree.run g b := by
  induction tree with
  | stop _ => rfl
  | read q next ih =>
      simp only [Policy.run, agree q]
      exact ih _

theorem encode_distinct {w w' : Word} (p : Completes (root 0) w) (q : Completes (root 0) w')
    (distinct : w ≠ w') : encodeEdges w ≠ encodeEdges w' := by
  intro equal
  apply distinct (root_facelets_separate p q _)
  rintro ⟨i, side⟩
  have same := congrFun equal (edgeSlot i side)
  simpa [faceletColor, encode_on_edge] using same

end CubeRev029.Physical

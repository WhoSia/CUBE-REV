import Init

/-!
CUBE-REV 0.17: Action-congruent deterministic observation partitions.

This is SOURCE, not a completed Lean kernel certificate until lake build has
a successful independently inspected runner receipt. Congruence itself is
classical automata theory; human cognition, full-cube perception and adaptive
optimality for the 0.16 24-state physical sensor are NOT proved here.
-/

namespace CubeRev017

universe u v w

/-- Reports after each action, with no gratuitous time-zero observation. -/
def observedTrace {S : Type u} {A : Type v} {Y : Type w}
  (step : A → S → S) (obs : S → Y) : List A → S → List Y
  | [], _ => []
  | a :: rest, s =>
      obs (step a s) :: observedTrace step obs rest (step a s)

/-- If every action respects the observation equivalence relation, any
two initially observationally identical states have equal report traces
after EVERY common finite word. -/
theorem observation_congruence_blocks_trace_separation
  {S : Type u} {A : Type v} {Y : Type w}
  (step : A → S → S) (obs : S → Y)
  (h : ∀ a x y, obs x = obs y → obs (step a x) = obs (step a y)) :
  ∀ (word : List A) (x y : S), obs x = obs y →
    observedTrace step obs word x = observedTrace step obs word y := by
  intro word
  induction word with
  | nil =>
      intro x y _
      rfl
  | cons a rest ih =>
      intro x y hxy
      have hnext : obs (step a x) = obs (step a y) := h a x y hxy
      simp only [observedTrace]
      rw [hnext, ih (step a x) (step a y) hnext]

/-- Z/4Z acted on by its translations is transitive; the parity sensor
respects all translations and thus cannot distinguish 0 from 2. -/
def parity4 (x : Fin 4) : Nat := x.val % 2
def translate4 (a x : Fin 4) : Fin 4 := x + a

theorem four_cycle_parity_action_congruence :
  ∀ (a x y : Fin 4),
    parity4 x = parity4 y →
      parity4 (translate4 a x) = parity4 (translate4 a y) := by
  decide

end CubeRev017

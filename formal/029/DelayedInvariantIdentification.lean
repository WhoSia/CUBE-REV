import AdaptiveLowerBound

/-! CUBE-REV 0.30: abstract delayed side information.
Reuse the verified 0.29 policy semantics. This model releases a label only
at a leaf; it does NOT assume that a physical auxiliary sensor can supply
that label for free. The 0.29 physical theorem is a separate result. -/
namespace CubeRev030
open CubeRev029

variable {S Q R K : Type}

/-- Only states with the same delayed label need to be separated by the
charged queries. Empty beliefs and empty fibers are allowed. -/
def FiberSeparated (label : S → K) (belief : S → Prop) : Prop :=
  ∀ s t, belief s → belief t → label s = label t → s = t

def SameLabelCollision (label : S → K) (belief : S → Prop) : Prop :=
  ∃ s t, belief s ∧ belief t ∧ label s = label t ∧ s ≠ t

theorem fiber_separated_iff_decoder (label : S → K) (belief : S → Prop) :
    FiberSeparated label belief ↔
      ∃ decode : K → Option S, ∀ s, belief s → decode (label s) = some s := by
  classical
  constructor
  · intro sep
    let decode : K → Option S := fun k =>
      if h : ∃ s, belief s ∧ label s = k then some (Classical.choose h) else none
    refine ⟨decode, ?_⟩
    intro s hs
    have h : ∃ t, belief t ∧ label t = label s := ⟨s, hs, rfl⟩
    simp only [decode, dif_pos h]
    exact congrArg some (sep _ _ (Classical.choose_spec h).1 hs
      (Classical.choose_spec h).2)
  · rintro ⟨decode, correct⟩ s t hs ht heq
    have a := correct s hs
    have b := correct t ht
    rw [heq, b] at a
    exact (Option.some.inj a).symm

theorem not_fiber_separated_iff_collision (label : S → K) (belief : S → Prop) :
    ¬ FiberSeparated label belief ↔ SameLabelCollision label belief := by
  classical
  constructor
  · intro h
    apply Classical.byContradiction
    intro hc
    apply h
    intro s t hs ht heq
    apply Classical.byContradiction
    intro hne
    exact hc ⟨s, t, hs, ht, heq, hne⟩
  · rintro ⟨s, t, hs, ht, heq, hne⟩ sep
    exact hne (sep s t hs ht heq)

/-- Exact bounded Bellman predicate. A stop is allowed at every depth.
A query must be successful for every reply, including impossible replies. -/
def DelayedWins (observe : S → Q → R) (label : S → K) :
    Nat → (S → Prop) → Prop
  | 0, belief => FiberSeparated label belief
  | n+1, belief => FiberSeparated label belief ∨
      ∃ q, ∀ r, DelayedWins observe label n (posterior observe belief q r)

/-- Exact dual. The explicit collision conjunct makes the recurrence
correct even if the query type is empty, and under early stopping. -/
def DelayedLoses (observe : S → Q → R) (label : S → K) :
    Nat → (S → Prop) → Prop
  | 0, belief => SameLabelCollision label belief
  | n+1, belief => SameLabelCollision label belief ∧
      ∀ q, ∃ r, DelayedLoses observe label n (posterior observe belief q r)

/-- A single deterministic charged policy is chosen before the label.
Only its terminal decoder receives the label. Classical choice constructs
a policy from a winning predicate; no executable finite solver is claimed. -/
theorem delayed_wins_iff_policy (observe : S → Q → R) (label : S → K)
    (n : Nat) (belief : S → Prop) :
    DelayedWins observe label n belief ↔
      ∃ tree : Policy Q R (K → Option S),
        Fits n tree ∧ ∀ s, belief s → (tree.run observe s) (label s) = some s := by
  classical
  induction n generalizing belief with
  | zero =>
      change FiberSeparated label belief ↔ _
      constructor
      · intro sep
        obtain ⟨decode, correct⟩ := (fiber_separated_iff_decoder label belief).mp sep
        exact ⟨.stop decode, .stop 0 decode, correct⟩
      · rintro ⟨tree, fit, correct⟩
        cases fit with
        | stop _ decode =>
          exact (fiber_separated_iff_decoder label belief).mpr ⟨decode, correct⟩
  | succ n ih =>
      change (FiberSeparated label belief ∨
        ∃ q, ∀ r, DelayedWins observe label n (posterior observe belief q r)) ↔ _
      constructor
      · rintro (sep | ⟨q, win⟩)
        · obtain ⟨decode, correct⟩ := (fiber_separated_iff_decoder label belief).mp sep
          exact ⟨.stop decode, .stop (n+1) decode, correct⟩
        · have existsTree : ∀ r : R, ∃ tree : Policy Q R (K → Option S),
              Fits n tree ∧ ∀ s, posterior observe belief q r s →
                (tree.run observe s) (label s) = some s :=
            fun r => (ih (posterior observe belief q r)).mp (win r)
          let next : R → Policy Q R (K → Option S) := fun r =>
            Classical.choose (existsTree r)
          refine ⟨.read q next, .read n q next (fun r => (Classical.choose_spec (existsTree r)).1), ?_⟩
          intro s hs
          change ((next (observe s q)).run observe s) (label s) = some s
          exact (Classical.choose_spec (existsTree (observe s q))).2 s ⟨hs,rfl⟩
      · rintro ⟨tree, fit, correct⟩
        cases fit with
        | stop _ decode =>
            exact .inl ((fiber_separated_iff_decoder label belief).mpr ⟨decode, correct⟩)
        | read _ q next branches =>
            refine .inr ⟨q, fun r => (ih (posterior observe belief q r)).mpr
              ⟨next r, branches r, ?_⟩⟩
            intro s hs
            simpa only [Policy.run, hs.2] using correct s hs.1

theorem delayed_loses_iff_not_wins (observe : S → Q → R) (label : S → K)
    (n : Nat) (belief : S → Prop) :
    DelayedLoses observe label n belief ↔ ¬ DelayedWins observe label n belief := by
  classical
  induction n generalizing belief with
  | zero => exact (not_fiber_separated_iff_collision label belief).symm
  | succ n ih =>
      change (SameLabelCollision label belief ∧ ∀ q, ∃ r,
        DelayedLoses observe label n (posterior observe belief q r)) ↔
        ¬ (FiberSeparated label belief ∨ ∃ q, ∀ r,
          DelayedWins observe label n (posterior observe belief q r))
      constructor
      · rintro ⟨collision, reply⟩ (sep | ⟨q, wins⟩)
        · exact (not_fiber_separated_iff_collision label belief).mpr collision sep
        · obtain ⟨r, loses⟩ := reply q
          exact (ih (posterior observe belief q r)).mp loses (wins r)
      · intro h
        refine ⟨(not_fiber_separated_iff_collision label belief).mp
          (fun sep => h (.inl sep)), ?_⟩
        intro q
        apply Classical.byContradiction
        intro noReply
        apply h
        refine .inr ⟨q, ?_⟩
        intro r
        apply Classical.byContradiction
        intro loses
        exact noReply ⟨r, (ih (posterior observe belief q r)).mpr loses⟩

/-- A lower-bound recurrence is both sound and complete for this abstract
terminal-label model, without a nonempty-query assumption. -/
theorem delayed_loses_iff_no_policy (observe : S → Q → R) (label : S → K)
    (n : Nat) (belief : S → Prop) :
    DelayedLoses observe label n belief ↔
      ¬ ∃ tree : Policy Q R (K → Option S),
        Fits n tree ∧ ∀ s, belief s → (tree.run observe s) (label s) = some s := by
  rw [delayed_loses_iff_not_wins, delayed_wins_iff_policy]

#print axioms fiber_separated_iff_decoder
#print axioms delayed_wins_iff_policy
#print axioms delayed_loses_iff_not_wins
#print axioms delayed_loses_iff_no_policy

end CubeRev030

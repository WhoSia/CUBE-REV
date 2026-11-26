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

/-- Execute a second policy after the first has terminated, without
changing the hidden state or exposing a terminal label to either query. -/
def appendPolicy {A B : Type} (next : A → Policy Q R B) :
    Policy Q R A → Policy Q R B
  | .stop output => next output
  | .read q k => .read q (fun r => appendPolicy next (k r))

theorem appendPolicy_run {A B : Type} (next : A → Policy Q R B)
    (observe : S → Q → R) (s : S) (tree : Policy Q R A) :
    (appendPolicy next tree).run observe s =
      (next (tree.run observe s)).run observe s := by
  induction tree with
  | stop output => rfl
  | read q k ih => exact ih (observe s q)

private theorem fits_add_left {A : Type} {m : Nat} {tree : Policy Q R A}
    (fit : Fits m tree) (n : Nat) : Fits (n + m) tree := by
  induction n with
  | zero => simpa using fit
  | succ n ih => simpa only [Nat.succ_add] using ih.succ

theorem appendPolicy_fits {A B : Type} (next : A → Policy Q R B)
    {n m : Nat} {tree : Policy Q R A} (fit : Fits n tree)
    (nextFit : ∀ a, Fits m (next a)) :
    Fits (n + m) (appendPolicy next tree) := by
  induction fit with
  | stop n output => exact fits_add_left (nextFit output) n
  | read n q k branches ih =>
      simpa only [appendPolicy, Nat.succ_add] using
        (Fits.read (n+m) q (fun r => appendPolicy next (k r)) ih)

/-- Run every early-label policy on the actual replies. Keep its output
but do not choose a branch by the undisclosed label. The eventual label
selects only which completed result is returned. -/
def collectFiberPolicies [DecidableEq K]
    (trees : K → Policy Q R (Option S)) :
    List K → Policy Q R (K → Option S)
  | [] => .stop (fun _ => none)
  | k :: ks => appendPolicy
      (fun result => (collectFiberPolicies trees ks).adapt id
        (fun _ r => r)
        (fun rest key => if key = k then result else rest key))
      (trees k)

theorem collect_fiber_policies_fits [DecidableEq K]
    (trees : K → Policy Q R (Option S)) (ks : List K) (d : Nat)
    (fit : ∀ k, Fits d (trees k)) :
    Fits (ks.length * d) (collectFiberPolicies trees ks) := by
  induction ks with
  | nil => exact .stop 0 _
  | cons k ks ih =>
      have h : Fits (d + ks.length * d)
          (appendPolicy (fun result =>
            (collectFiberPolicies trees ks).adapt id (fun _ r => r)
              (fun rest key => if key = k then result else rest key))
            (trees k)) := by
        apply appendPolicy_fits _ (fit k)
        intro result
        exact Policy.adapt_fits id (fun _ r => r)
          (fun rest key => if key = k then result else rest key) ih
      simpa only [collectFiberPolicies, List.length_cons, Nat.succ_mul,
        Nat.add_comm] using h

theorem collect_fiber_policies_run [DecidableEq K]
    (trees : K → Policy Q R (Option S)) (ks : List K)
    (observe : S → Q → R) (s : S) (key : K) (member : key ∈ ks) :
    ((collectFiberPolicies trees ks).run observe s) key =
      (trees key).run observe s := by
  induction ks with
  | nil => simp at member
  | cons k ks ih =>
      simp only [collectFiberPolicies, appendPolicy_run, Policy.adapt_run]
      change (if key = k then (trees k).run observe s
        else ((collectFiberPolicies trees ks).run observe s) key) = _
      rcases List.mem_cons.mp member with equal | inside
      · subst key
        simp
      · by_cases equal : key = k
        · subst key
          simp
        · rw [if_neg equal]
          exact ih inside

/-- Finite timing-overhead upper bound. Early label knowledge may select
one tree of depth d for each fiber. With delayed label knowledge a single
controller can instead execute all those trees in at most |ks|*d queries.
The bound is conditional on every tree fitting d even on impossible
replies, and on the label list covering the belief. -/
theorem delayed_policy_of_early_family [DecidableEq K]
    (observe : S → Q → R) (label : S → K) (belief : S → Prop)
    (ks : List K) (d : Nat) (trees : K → Policy Q R (Option S))
    (covers : ∀ s, belief s → label s ∈ ks)
    (fit : ∀ k, Fits d (trees k))
    (correct : ∀ k s, belief s → label s = k →
      (trees k).run observe s = some s) :
    DelayedWins observe label (ks.length * d) belief := by
  apply (delayed_wins_iff_policy observe label _ belief).mpr
  refine ⟨collectFiberPolicies trees ks, collect_fiber_policies_fits trees ks d fit, ?_⟩
  intro s hs
  rw [collect_fiber_policies_run trees ks observe s (label s) (covers s hs)]
  exact correct (label s) s hs rfl

/-- In the other direction, knowing the label before querying can never
make the required worst-case budget larger. -/
theorem early_family_of_delayed
    (observe : S → Q → R) (label : S → K) (belief : S → Prop) (d : Nat)
    (win : DelayedWins observe label d belief) :
    ∀ k, ∃ tree : Policy Q R (Option S),
      Fits d tree ∧ ∀ s, belief s → label s = k →
        tree.run observe s = some s := by
  obtain ⟨tree, fit, correct⟩ := (delayed_wins_iff_policy observe label d belief).mp win
  intro k
  refine ⟨tree.adapt id (fun _ r => r) (fun decode => decode k),
    Policy.adapt_fits id (fun _ r => r) (fun decode => decode k) fit, ?_⟩
  intro s hs equal
  rw [Policy.adapt_run]
  change (tree.run observe s) k = some s
  rw [← equal]
  exact correct s hs

#print axioms appendPolicy_fits
#print axioms collect_fiber_policies_run
#print axioms delayed_policy_of_early_family
#print axioms early_family_of_delayed

end CubeRev030

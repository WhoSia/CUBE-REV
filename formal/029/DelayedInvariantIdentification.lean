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
  | nil => simpa only [List.length_nil, Nat.zero_mul, collectFiberPolicies] using
      (Fits.stop 0 (fun _ : K => (none : Option S)) :
        Fits 0 (Policy.stop (fun _ : K => (none : Option S)) : Policy Q R (K → Option S)))
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


/-- Query sequence on the hypothetical constant-reply branch. The branch
need not be realized by every state. -/
def constantTrace (r : R) : Policy Q R O → List Q
  | .stop _ => []
  | .read q next => q :: constantTrace r (next r)

theorem constantTrace_length_le (r : R) {n : Nat}
    {tree : Policy Q R O} (fit : Fits n tree) :
    (constantTrace r tree).length ≤ n := by
  induction fit with
  | stop n output => exact Nat.zero_le n
  | read n q next branches ih =>
      exact Nat.succ_le_succ (ih r)

theorem constantTrace_run_eq (observe : S → Q → R) (r : R)
    (s : S) (tree : Policy Q R O)
    (agrees : ∀ q, q ∈ constantTrace r tree → observe s q = r) :
    tree.run observe s = tree.run (fun _ _ => r) s := by
  induction tree with
  | stop output => rfl
  | read q next ih =>
      have hq : observe s q = r := agrees q (by simp [constantTrace])
      simp only [Policy.run, hq]
      apply ih r
      intro a ha
      exact agrees a (by simp [constantTrace, ha])

/-- On a constant-reply branch, a correct delayed decoder must separate
every same-label pair by at least one of the queries on that branch.
This is a hitting-set certificate, not a bound on arbitrary branches. -/
theorem constantTrace_separates (observe : S → Q → R) (label : S → K)
    (belief : S → Prop) (r : R) (tree : Policy Q R (K → Option S))
    (correct : ∀ s, belief s → (tree.run observe s) (label s) = some s)
    (s t : S) (hs : belief s) (ht : belief t) (hk : label s = label t)
    (hne : s ≠ t) (base : ∀ q, observe s q = r) :
    ∃ q, q ∈ constantTrace r tree ∧ observe t q ≠ r := by
  classical
  apply Classical.byContradiction
  intro absent
  have agree : ∀ q, q ∈ constantTrace r tree → observe t q = r := by
    intro q hq
    apply Classical.byContradiction
    intro h
    exact absent ⟨q, hq, h⟩
  have sameConst (p : Policy Q R (K → Option S)) :
      p.run (fun _ _ => r) s = p.run (fun _ _ => r) t := by
    induction p with
    | stop output => rfl
    | read q next ih => exact ih r
  have a := correct s hs
  have b := correct t ht
  rw [constantTrace_run_eq observe r s tree (fun q _ => base q),
      sameConst tree, ← constantTrace_run_eq observe r t tree agree, hk, b] at a
  exact hne (Option.some.inj a).symm

#print axioms constantTrace_length_le
#print axioms constantTrace_run_eq
#print axioms constantTrace_separates


/-- The actual query path on a reference state, allowing nonconstant replies. -/
def referenceTrace (observe : S → Q → R) (s : S) : Policy Q R O → List Q
  | .stop _ => []
  | .read q next => q :: referenceTrace observe s (next (observe s q))

theorem referenceTrace_length_le (observe : S → Q → R) (s : S)
    {n : Nat} {tree : Policy Q R O} (fit : Fits n tree) :
    (referenceTrace observe s tree).length ≤ n := by
  induction fit with
  | stop n output => exact Nat.zero_le n
  | read n q next branches ih => exact Nat.succ_le_succ (ih (observe s q))

theorem referenceTrace_run_eq (observe : S → Q → R) (s t : S)
    (tree : Policy Q R O)
    (agrees : ∀ q, q ∈ referenceTrace observe s tree → observe s q = observe t q) :
    tree.run observe s = tree.run observe t := by
  induction tree with
  | stop output => rfl
  | read q next ih =>
      have hq : observe s q = observe t q := agrees q (by simp [referenceTrace])
      simp only [Policy.run]
      rw [← hq]
      apply ih (observe s q)
      intro a ha
      exact agrees a (by simp [referenceTrace, ha])

/-- Every realized path is a local certificate against all competing
states with the same terminal label. No assumption of constant replies. -/
theorem referenceTrace_separates (observe : S → Q → R) (label : S → K)
    (belief : S → Prop) (tree : Policy Q R (K → Option S))
    (correct : ∀ s, belief s → (tree.run observe s) (label s) = some s)
    (s t : S) (hs : belief s) (ht : belief t) (hk : label s = label t)
    (hne : s ≠ t) :
    ∃ q, q ∈ referenceTrace observe s tree ∧ observe s q ≠ observe t q := by
  classical
  apply Classical.byContradiction
  intro absent
  have agrees : ∀ q, q ∈ referenceTrace observe s tree → observe s q = observe t q := by
    intro q hq
    apply Classical.byContradiction
    intro h
    exact absent ⟨q, hq, h⟩
  have a := correct s hs
  have b := correct t ht
  rw [referenceTrace_run_eq observe s t tree agrees, hk, b] at a
  exact hne (Option.some.inj a).symm

/-- A winning budget supplies a bounded local separating list for each state.
The converse need not hold: the list may depend on the unknown state. -/
theorem delayed_wins_local_certificate (observe : S → Q → R) (label : S → K)
    (belief : S → Prop) (n : Nat) (win : DelayedWins observe label n belief)
    (s : S) (hs : belief s) :
    ∃ qs : List Q, qs.length ≤ n ∧
      ∀ t, belief t → label s = label t → s ≠ t →
        ∃ q, q ∈ qs ∧ observe s q ≠ observe t q := by
  obtain ⟨tree, fit, correct⟩ := (delayed_wins_iff_policy observe label n belief).mp win
  exact ⟨referenceTrace observe s tree, referenceTrace_length_le observe s fit,
    fun t ht hk hne => referenceTrace_separates observe label belief tree correct s t hs ht hk hne⟩

#print axioms referenceTrace_length_le
#print axioms referenceTrace_run_eq
#print axioms referenceTrace_separates
#print axioms delayed_wins_local_certificate


/-- If each query has an exclusive same-label witness against the constant
reply branch, that one branch must contain every query. The reference
state may differ between witnesses; no global reference state is needed. -/
theorem constantTrace_covers_exclusive_witnesses
    (observe : S → Q → R) (label : S → K) (belief : S → Prop)
    (r : R) (tree : Policy Q R (K → Option S))
    (correct : ∀ s, belief s → (tree.run observe s) (label s) = some s)
    (witness : ∀ q : Q, ∃ s t : S, belief s ∧ belief t ∧
      label s = label t ∧ s ≠ t ∧ (∀ a, observe s a = r) ∧
      (∀ a, observe t a ≠ r → a = q)) :
    ∀ q : Q, q ∈ constantTrace r tree := by
  intro q
  obtain ⟨s, t, hs, ht, hk, hne, base, exclusive⟩ := witness q
  obtain ⟨a, ha, diff⟩ :=
    constantTrace_separates observe label belief r tree correct s t hs ht hk hne base
  have eq : a = q := exclusive a diff
  simpa only [eq] using ha

/-- The all-constant branch reduces the lower bound to a covering-list
cardinality statement. This separates the adversary argument from the
finite-domain representation and applies also to heterogeneous fibers. -/
theorem delayed_budget_of_exclusive_witnesses
    (observe : S → Q → R) (label : S → K) (belief : S → Prop)
    (r : R) (n m : Nat) (win : DelayedWins observe label n belief)
    (witness : ∀ q : Q, ∃ s t : S, belief s ∧ belief t ∧
      label s = label t ∧ s ≠ t ∧ (∀ a, observe s a = r) ∧
      (∀ a, observe t a ≠ r → a = q))
    (coverBound : ∀ qs : List Q, (∀ q : Q, q ∈ qs) → m ≤ qs.length) :
    m ≤ n := by
  obtain ⟨tree, fit, correct⟩ := (delayed_wins_iff_policy observe label n belief).mp win
  exact Nat.le_trans
    (coverBound (constantTrace r tree)
      (constantTrace_covers_exclusive_witnesses observe label belief r tree correct witness))
    (constantTrace_length_le r fit)

#print axioms constantTrace_covers_exclusive_witnesses
#print axioms delayed_budget_of_exclusive_witnesses


/-- Cardinality of a distinct list is at most the length of any list that
covers it. Erasing one occurrence prevents duplicated reads from
artificially strengthening the lower bound. -/
private theorem nodup_cover_length [BEq Q] [LawfulBEq Q]
    (xs ys : List Q) (nd : xs.Nodup)
    (cover : ∀ q, q ∈ xs → q ∈ ys) : xs.length ≤ ys.length := by
  induction xs generalizing ys with
  | nil => exact Nat.zero_le _
  | cons a xs ih =>
      have h := List.nodup_cons.mp nd
      have ha : a ∈ ys := cover a (by simp)
      have sub : ∀ q, q ∈ xs → q ∈ ys.erase a := by
        intro q hq
        have ne : q ≠ a := by
          intro e
          apply h.1
          simpa only [← e] using hq
        exact (List.mem_erase_of_ne ne).mpr (cover q (by simp [hq]))
      have bound := ih (ys.erase a) h.2 sub
      have len := List.length_erase_of_mem ha
      simp only [List.length_cons]
      omega

theorem fin_query_cover_length (m : Nat) (qs : List (Fin m))
    (covers : ∀ q : Fin m, q ∈ qs) : m ≤ qs.length := by
  have nd : (List.finRange m).Nodup := by
    apply List.nodup_iff_eq_of_getElem_eq.mpr
    intro i j hi hj h
    simpa using congrArg Fin.val h
  have h := nodup_cover_length (List.finRange m) qs nd (fun q _ => covers q)
  simpa only [List.length_finRange] using h

/-- Fin-indexed specialization: the witness condition alone forces one
paid read for every query in the finite domain. -/
theorem delayed_fin_budget_of_exclusive_witnesses
    (m n : Nat) (observe : S → Fin m → R) (label : S → K)
    (belief : S → Prop) (r : R)
    (win : DelayedWins observe label n belief)
    (witness : ∀ q : Fin m, ∃ s t : S, belief s ∧ belief t ∧
      label s = label t ∧ s ≠ t ∧ (∀ a, observe s a = r) ∧
      (∀ a, observe t a ≠ r → a = q)) :
    m ≤ n := by
  exact delayed_budget_of_exclusive_witnesses observe label belief r n m win
    witness (fin_query_cover_length m)

#print axioms fin_query_cover_length
#print axioms delayed_fin_budget_of_exclusive_witnesses

end CubeRev030

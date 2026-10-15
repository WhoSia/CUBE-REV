import PrefixRefutationCalculus

/-!
CUBE-REV 0.25 P0-R6I — weighted prefix cutsets and certified
variable-depth language-cylinder composition.

This is an abstract TCS proof. It carries BOTH the physical state S
and the canonical DFA context Q, and it never equates unrelated action
words. Quantitative weights count canonical recursive CALLS, not
distinct physical Rubik group states or measured runtime.
-/
namespace CubeRev025

universe u v w

/-- A leaf discharges a full remaining-budget search obligation.
A split discharges this exact node and covers ALL allowed children.
The variable-depth tree is prefix-free by construction: a leaf
cannot simultaneously have descendants in the cutset. -/
inductive WeightedCutRefutation
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop) (target : S → Prop) :
    Nat → S → Q → Prop
  | discharge (k : Nat) (s : S) (q : Q)
      (certificate : PrefixRefutation move advance allowed target k s q) :
      WeightedCutRefutation move advance allowed target k s q
  | split (k : Nat) (s : S) (q : Q)
      (missing : ¬ target s)
      (children : ∀ a, allowed q a →
        WeightedCutRefutation move advance allowed target k
          (move s a) (advance q a)) :
      WeightedCutRefutation move advance allowed target (k+1) s q

/-- Finite variable-depth cutsets compose into an exact full-source
refutation, not just a set of independent success messages. -/
theorem weighted_cutset_compose
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop) (target : S → Prop) :
    ∀ (k : Nat) (s : S) (q : Q),
      WeightedCutRefutation move advance allowed target k s q →
      PrefixRefutation move advance allowed target k s q := by
  intro k
  induction k with
  | zero =>
      intro s q h
      cases h with
      | discharge _ _ _ certificate => exact certificate
  | succ k ih =>
      intro s q h
      cases h with
      | discharge _ _ _ certificate => exact certificate
      | split _ _ _ missing children =>
          exact .branch k s q missing
            (fun a ha => ih (move s a) (advance q a) (children a ha))

/-- The composed variable-depth proof tree excludes EVERY canonical
ordered physical action word of remaining length at most k. -/
theorem weighted_cutset_sound
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop) (target : S → Prop)
    (k : Nat) (s : S) (q : Q)
    (proof : WeightedCutRefutation move advance allowed target k s q) :
    ∀ word : List A, word.length ≤ k →
      legalSuffix allowed advance q word →
      ¬ target (runWord move s word) :=
  prefix_refutation_sound move advance allowed target
    k s q (weighted_cutset_compose move advance allowed target k s q proof)

/-- Weighted number of iterative-deepening recursive calls below a
canonical prefix with k remaining depth. It counts the current prefix
(k+1) times, and every child subtree under all legal next actions.
The alphabet is FINITE. The implementer must match its exact original
physical/canonical HTM grammar. -/
def weightedPrefixCalls
    {Q : Type v} {A : Type w} [DecidableEq A]
    (legalNext : Q → Finset A) (nextQ : Q → A → Q) :
    Nat → Q → Nat
  | 0, _ => 1
  | k+1, q =>
      (k+2) +
      ∑ a ∈ legalNext q,
        weightedPrefixCalls legalNext nextQ k (nextQ q a)

/-- Fundamental conservation identity for splitting one cylinder into
its exact legal children. The parent itself remains an internal node. -/
theorem exact_weighted_cylinder_split
    {Q : Type v} {A : Type w} [DecidableEq A]
    (legalNext : Q → Finset A) (nextQ : Q → A → Q)
    (k : Nat) (q : Q) :
    weightedPrefixCalls legalNext nextQ (k+1) q =
      (k+2) + ∑ a ∈ legalNext q,
        weightedPrefixCalls legalNext nextQ k (nextQ q a) := by
  rfl

/-- Every node with zero remaining depth weighs exactly one call. -/
theorem terminal_cylinder_weight_one
    {Q : Type v} {A : Type w} [DecidableEq A]
    (legalNext : Q → Finset A) (nextQ : Q → A → Q)
    (q : Q) :
    weightedPrefixCalls legalNext nextQ 0 q = 1 := by
  rfl

end CubeRev025

import ProjectionWordLanguage

/-!
CUBE-REV 0.25 P0-R6H — A graded prefix-refutation calculus.

The physical state S and the canonical-action grammar context Q are
separate and BOTH must be carried through every source prefix.
A proof is a finite tree of (a) exact current-state absence and
(b) proofs for EVERY grammar-admissible next generator.
The tree is sound AND complete for the bounded word-exclusion statement,
without assuming commuting moves or independent corner/edge words.

The file is a generic mathematical calculus. It does NOT provide
physical original B10 computation, checked 54-sticker move tables,
or a compact 18-shard Rubik's certificate by itself.
-/
namespace CubeRev025

universe u v w

/-- Valid action suffixes in a deterministic grammar state q. -/
def legalSuffix {Q : Type v} {A : Type w}
    (allowed : Q → A → Prop) (advance : Q → A → Q) :
    Q → List A → Prop
  | _, [] => True
  | q, a :: rest =>
      allowed q a ∧ legalSuffix allowed advance (advance q a) rest

/-- A depth-bounded physically meaningful absence certificate carries
the automaton context. At a positive depth it MUST cover every allowed
first action; it cannot prove absence by inspecting selected actions. -/
inductive PrefixRefutation
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop) (target : S → Prop) :
    Nat → S → Q → Prop
  | leaf (s : S) (q : Q) (missing : ¬ target s) :
      PrefixRefutation move advance allowed target 0 s q
  | branch (k : Nat) (s : S) (q : Q)
      (missing : ¬ target s)
      (children : ∀ a, allowed q a →
        PrefixRefutation move advance allowed target k
          (move s a) (advance q a)) :
      PrefixRefutation move advance allowed target (k+1) s q

/-- Soundness: a completed proof tree forbids ALL legal ordered suffixes
through depth k, not only the words explicitly sampled by a solver. -/
theorem prefix_refutation_sound
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop) (target : S → Prop) :
    ∀ (k : Nat) (s : S) (q : Q),
      PrefixRefutation move advance allowed target k s q →
      ∀ word : List A, word.length ≤ k →
        legalSuffix allowed advance q word →
        ¬ target (runWord move s word) := by
  intro k
  induction k with
  | zero =>
      intro s q cert word hLen _
      cases cert with
      | leaf _ _ missing =>
          cases word with
          | nil => simpa [runWord] using missing
          | cons a rest => simp at hLen
  | succ k ih =>
      intro s q cert word hLen hLegal
      cases cert with
      | branch _ _ _ missing children =>
          cases word with
          | nil => simpa [runWord] using missing
          | cons a rest =>
              have hNext : rest.length ≤ k := by
                simpa using hLen
              exact ih (move s a) (advance q a) (children a hLegal.1)
                rest hNext hLegal.2

/-- Completeness: every valid bounded semantic refutation can be unfolded
into this prefix proof calculus, retaining the same legal-action grammar. -/
theorem prefix_refutation_complete
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop) (target : S → Prop) :
    ∀ (k : Nat) (s : S) (q : Q),
      (∀ word : List A, word.length ≤ k →
        legalSuffix allowed advance q word →
        ¬ target (runWord move s word)) →
      PrefixRefutation move advance allowed target k s q := by
  intro k
  induction k with
  | zero =>
      intro s q h
      exact .leaf s q (by
        simpa [runWord] using
          (h [] (by simp) (by simp [legalSuffix])))
  | succ k ih =>
      intro s q h
      refine .branch k s q ?_ ?_
      · simpa [runWord] using
          (h [] (by simp) (by simp [legalSuffix]))
      · intro a hAllowed
        apply ih
        intro rest hLen hLegal
        have hAllowedWord :
            legalSuffix allowed advance q (a :: rest) :=
          ⟨hAllowed, hLegal⟩
        have hLong : (a :: rest).length ≤ k + 1 := by
          simpa using (Nat.succ_le_succ hLen)
        simpa only [runWord] using
          (h (a :: rest) hLong hAllowedWord)

/-- Exact iff between a finite ordered-word absence property and existence
of a complete, grammar-respecting inductive prefix-refutation witness. -/
theorem prefix_refutation_iff_bounded_absence
    {S : Type u} {Q : Type v} {A : Type w}
    (move : S → A → S)
    (advance : Q → A → Q)
    (allowed : Q → A → Prop) (target : S → Prop)
    (k : Nat) (s : S) (q : Q) :
    PrefixRefutation move advance allowed target k s q ↔
      ∀ word : List A, word.length ≤ k →
        legalSuffix allowed advance q word →
        ¬ target (runWord move s word) := by
  constructor
  · exact prefix_refutation_sound move advance allowed target k s q
  · exact prefix_refutation_complete move advance allowed target k s q

end CubeRev025

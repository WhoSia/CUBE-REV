import Lean

/-!
CUBE-REV 0.25 P0-R6E — TCS ordered-word projected language theorem.
Full original physical B6/B7/B8/B9 source search is a separate proof obligation.
An identical ordered physical WORD must satisfy both projected conditions.
-/
namespace CubeRev025

universe u v w z

/-- Apply one identical sequence of generators in its physical word order. -/
def runWord {S : Type u} {A : Type z}
    (step : S → A → S) (s : S) : List A → S
  | [] => s
  | a :: tail => runWord step (step s a) tail

/-- Exact one-step quotient morphisms extend to every ordered action word. -/
theorem runWord_projection
    {S : Type u} {P : Type v} {A : Type z}
    (step : S → A → S) (projectStep : P → A → P)
    (project : S → P)
    (commutes : ∀ s a, project (step s a) =
                           projectStep (project s) a) :
    ∀ (s : S) (word : List A),
      project (runWord step s word) =
      runWord projectStep (project s) word := by
  intro s word
  induction word generalizing s with
  | nil => rfl
  | cons a tail ih =>
      change project (runWord step (step s a) tail) =
        runWord projectStep (projectStep (project s) a) tail
      rw [ih (step s a), commutes s a]

/-- A real goal-reaching word belongs to BOTH projected accepted languages
under that exact same word, not two separately quantified words. -/
theorem physical_goal_word_in_common_projection_language
    {S : Type u} {C : Type v} {E : Type w} {A : Type z}
    (step : S → A → S)
    (cornerStep : C → A → C) (edgeStep : E → A → E)
    (corner : S → C) (edge : S → E)
    (goal : S → Prop)
    (cornerGoal : C → Prop) (edgeGoal : E → Prop)
    (cornerCommutes : ∀ s a,
      corner (step s a) = cornerStep (corner s) a)
    (edgeCommutes : ∀ s a,
      edge (step s a) = edgeStep (edge s) a)
    (cornerNecessary : ∀ x, goal x → cornerGoal (corner x))
    (edgeNecessary : ∀ x, goal x → edgeGoal (edge x))
    (source : S) (word : List A)
    (physicalWitness : goal (runWord step source word)) :
    cornerGoal (runWord cornerStep (corner source) word) ∧
    edgeGoal (runWord edgeStep (edge source) word) := by
  constructor
  · have hc := cornerNecessary (runWord step source word) physicalWitness
    have heq := runWord_projection step cornerStep corner
      cornerCommutes source word
    rw [← heq]
    exact hc
  · have he := edgeNecessary (runWord step source word) physicalWitness
    have heq := runWord_projection step edgeStep edge
      edgeCommutes source word
    rw [← heq]
    exact he

/-- A normal-form DFA can define legalWord. If the language accepted by
both projective goal automata is EMPTY, no allowed real physical solution
word can exist. The original physical cube/action connection is external. -/
theorem empty_common_projection_language_excludes_real_solution
    {S : Type u} {C : Type v} {E : Type w} {A : Type z}
    (step : S → A → S)
    (cornerStep : C → A → C) (edgeStep : E → A → E)
    (corner : S → C) (edge : S → E)
    (goal : S → Prop)
    (cornerGoal : C → Prop) (edgeGoal : E → Prop)
    (legalWord : List A → Prop)
    (cornerCommutes : ∀ s a,
      corner (step s a) = cornerStep (corner s) a)
    (edgeCommutes : ∀ s a,
      edge (step s a) = edgeStep (edge s) a)
    (cornerNecessary : ∀ x, goal x → cornerGoal (corner x))
    (edgeNecessary : ∀ x, goal x → edgeGoal (edge x))
    (source : S)
    (emptyJointLanguage : ∀ word, legalWord word →
      ¬ (cornerGoal (runWord cornerStep (corner source) word) ∧
         edgeGoal (runWord edgeStep (edge source) word))) :
    ∀ word, legalWord word → ¬ goal (runWord step source word) := by
  intro word hLegal hPhysical
  have hCommon := physical_goal_word_in_common_projection_language
    step cornerStep edgeStep corner edge goal
    cornerGoal edgeGoal cornerCommutes edgeCommutes
    cornerNecessary edgeNecessary source word hPhysical
  exact emptyJointLanguage word hLegal hCommon


/-- A Myhill–Nerode-style residual equivalence of acceptance under all
future COMMON ordered action words. If replacing one state by another
would change any accepted continuation, caching by their coarser
features would be unsafe. -/
def residualEquivalent {S : Type u} {A : Type z}
    (step : S → A → S) (accept : S → Prop) (x y : S) : Prop :=
  ∀ word : List A,
    accept (runWord step x word) ↔
    accept (runWord step y word)

/-- The common-word residual relation is a right congruence: taking
the SAME new first action preserves equivalence of all future suffixes. -/
theorem residual_equivalence_right_congruence
    {S : Type u} {A : Type z}
    (step : S → A → S) (accept : S → Prop)
    (x y : S) (h : residualEquivalent step accept x y) (a : A) :
    residualEquivalent step accept (step x a) (step y a) := by
  intro word
  simpa only [runWord] using (h (a :: word))

/-- Sound proof-cache reuse: a state with an empty accepted suffix
language may be replaced by any state with an exactly equal residual
language, without introducing a false absence certificate. -/
theorem residual_equivalence_preserves_empty_language
    {S : Type u} {A : Type z}
    (step : S → A → S) (accept : S → Prop)
    (x y : S) (h : residualEquivalent step accept x y)
    (nothingFromX : ∀ word : List A,
      ¬ accept (runWord step x word)) :
    ∀ word : List A, ¬ accept (runWord step y word) := by
  intro word hAccepted
  exact nothingFromX word ((h word).mpr hAccepted)

end CubeRev025

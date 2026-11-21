import SectorStatewiseValidity

namespace CubeRev029

/-- Exact length completion. A branch that stops before its allotted budget
is padded with REAL paired reads. Such padding is mandatory in CUBE-REV 0.29
because the last necessary corner sticker arrives only at frame 19.

For a well-budgeted input, the zero-budget clause only encounters a stop.
For an invalid input the source controller is returned as-is; theorems
below apply only under a Fits proof. -/
def Policy.padToExact {Q R O : Type} (fallback : Q) :
    (n : Nat) → Policy Q R O → Policy Q R O
  | 0, tree => tree
  | n+1, .stop result =>
      .read fallback (fun _ => padToExact fallback n (.stop result))
  | n+1, .read q next =>
      .read q (fun reply => padToExact fallback n (next reply))

/-- Completing early stops does not exceed the original allotted budget,
even on arbitrary response branches. -/
theorem Policy.padToExact_fits {Q R O : Type}
    (fallback : Q) {n : Nat} {tree : Policy Q R O}
    (bounded : Fits n tree) :
    Fits n (tree.padToExact fallback n) := by
  induction bounded with
  | stop n output =>
      induction n with
      | zero =>
          exact Fits.stop 0 output
      | succ k ih =>
          exact Fits.read k fallback _ (fun _ => ih)
  | read n query next branches ih =>
      exact Fits.read n query _ ih

/-- The extra physical observations are ignored by the output decoder.
In particular, padding cannot change the initial cubie reconstructed by
an already-terminated sign-deferred representative policy. -/
theorem Policy.padToExact_run {S Q R O : Type}
    (fallback : Q) (observe : S → Q → R) (state : S)
    {n : Nat} {tree : Policy Q R O}
    (bounded : Fits n tree) :
    (tree.padToExact fallback n).run observe state =
      tree.run observe state := by
  induction bounded with
  | stop n output =>
      induction n with
      | zero => rfl
      | succ k ih =>
          simpa only [Policy.padToExact, Policy.run] using ih
  | read n query next branches ih =>
      simpa only [Policy.padToExact, Policy.run] using
        ih (observe state query)

/-- An originally at-most-n-read controller, once padded, observes exactly
n paired frames on EVERY state. The final corner color is then available
when the terminal parity correction is evaluated. -/
theorem Policy.padToExact_transcript_length {S Q R O : Type}
    (fallback : Q) (observe : S → Q → R) (state : S)
    {n : Nat} {tree : Policy Q R O}
    (bounded : Fits n tree) :
    ((tree.padToExact fallback n).transcript observe state).length = n := by
  induction bounded with
  | stop n output =>
      induction n with
      | zero => rfl
      | succ k ih =>
          simpa only [Policy.padToExact, Policy.transcript,
            List.length_cons] using congrArg Nat.succ ih
  | read n query next branches ih =>
      simpa only [Policy.padToExact, Policy.transcript,
        List.length_cons] using
        congrArg Nat.succ (ih (observe state query))

#print axioms Policy.padToExact_fits
#print axioms Policy.padToExact_run
#print axioms Policy.padToExact_transcript_length

end CubeRev029

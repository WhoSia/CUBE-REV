/-!
CUBE-REV 0.16 internal P11 — finite rational LP certificate and a general
arithmetic obstruction. This file is SOURCE ONLY until a Lean 4.34.1
compiler/kernel execution is actually observed and checked.

The 24 embedded bitmasks are taken from the P10 50x116 mathematical table;
the physical 18-HTM cubie-action -> table semantic bridge is NOT proved here.
The all-7004-quartets >=8 overlap premise remains an external finite check.
-/
import Lean

namespace CubeRev016

/-- P10's 28-element component, indexed within the original 50 targets. -/
def p11BTargets : List Nat :=
  [3,4,5,6,8,9,10,11,12,13,14,15,18,23,24,29,30,31,32,34,
   40,41,42,44,46,47,48,49]

/-- An exact rational primal cover, represented as (mask,numerator)/75. -/
def p11FractionalMasks : List (Nat × Nat) :=
  [(7936,7),(14360,6),(15616,24),(15872,34),(8389472,7),
   (16783456,4),(4294968600,10),(4303356008,32),
   (4303356016,32),(17179869976,27),(19881312256,16),
   (7696598220800,11),(23089761271808,6),
   (24189272883200,11),(25292525535232,42),
   (492599999725568,16),(774056186273792,11),
   (774056194654208,4),(774064239017984,1),
   (914793691398144,16),(985182819581952,16),
   (1055531179720704,11),(1076421883592704,11),
   (1078620906848256,5)]

def p11CoverNumerator (i : Nat) : Nat :=
  p11FractionalMasks.foldl
    (fun total p => total + (if Nat.testBit p.1 i then p.2 else 0)) 0

/-- Every one of the 28 target masks receives EXACT total mass 75/75. -/
theorem p11_fractional_primal_all28 :
    p11BTargets.map p11CoverNumerator = List.replicate 28 75 := by
  decide

/-- The chosen candidate coefficients total exactly 360/75 = 24/5. -/
theorem p11_fractional_primal_total :
    (p11FractionalMasks.map Prod.snd).sum = 360 := by
  decide

/-- Hand-arithmetic implication of a separate combinatorial overlap bound.
The global 8-overlap premise itself has NOT been Lean-kernel formalized. -/
theorem p11_five_cover_obstructed_by_eight_overlap
    (fifth intersection : Nat)
    (hfifth : fifth ≤ 20) (hoverlap : 8 ≤ intersection) :
    80 + (fifth - intersection) < 96 := by
  omega

/-- The finite integer success threshold exceeds the fractional optimum. -/
theorem p11_integrality_gap_arithmetic :
    (6 : Nat) * 4 = 5 * (24 / 5) := by
  decide

end CubeRev016

import ExactBudgetPadding

namespace CubeRev029.Nineteen

/-- Always execute exactly eight actual continuation probes, including
unscored padding if the edge policy reaches a leaf early. The policy still
returns a sign-indexed decoder, NOT a prematurely available corner sign. -/
def exactEightSectorPolicy {S Q R : Type} [DecidableEq R]
    (fallback : Q)
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool)
    (root : Nat) (belief : List S) :
    Policy Q R (Bool → Option S) :=
  (compileSectorDecoder graph observe sign 8 root belief).val.padToExact
    fallback 8

theorem exact_eight_sector_fits {S Q R : Type} [DecidableEq R]
    (fallback : Q)
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool)
    (root : Nat) (belief : List S) :
    Fits 8 (exactEightSectorPolicy fallback graph observe sign root belief) := by
  exact Policy.padToExact_fits fallback
    (compileSectorDecoder graph observe sign 8 root belief).property

/-- The corner schedule receives exactly eight physical frame slots,
rather than merely a promise of eight-or-fewer edge probes. -/
theorem exact_eight_sector_trace_length {S Q R : Type} [DecidableEq R]
    (fallback : Q)
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool)
    (root : Nat) (belief : List S) (state : S) :
    ((exactEightSectorPolicy fallback graph observe sign root belief)
      .transcript observe state).length = 8 := by
  exact Policy.padToExact_transcript_length fallback observe state
    (compileSectorDecoder graph observe sign 8 root belief).property

/-- Combining the finite-state validity condition and exact padding:
after **precisely eight** genuine continuation observations, the edge
decoder is correct on every original candidate when its real terminal
sign is supplied. The sign is not queried by the adaptive controller. -/
theorem exact_eight_sector_recovers_given_terminal_sign
    {S Q R : Type} [DecidableEq R]
    (fallback : Q)
    (graph : Array (FrozenInstruction Q R Unit))
    (observe : S → Q → R) (sign : S → Bool)
    (root : Nat) (belief : List S)
    (verified : StatewiseSectorValid graph observe sign 8 root belief)
    (state : S) (member : state ∈ belief) :
    ((exactEightSectorPolicy fallback graph observe sign root belief).run
        observe state) (sign state) = some state := by
  have original :=
    statewise_checked_sector_recovers_each_candidate
      graph observe sign 8 root belief verified state member
  change
    (((compileSectorDecoder graph observe sign 8 root belief).val.padToExact
      fallback 8).run observe state) (sign state) = some state
  rw [Policy.padToExact_run fallback observe state
    (compileSectorDecoder graph observe sign 8 root belief).property]
  exact original

#print axioms exact_eight_sector_fits
#print axioms exact_eight_sector_trace_length
#print axioms exact_eight_sector_recovers_given_terminal_sign

end CubeRev029.Nineteen

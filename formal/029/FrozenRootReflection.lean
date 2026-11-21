import DistinctReplyChecker

namespace CubeRev029.Nineteen

open Eighteen

/-- Convert the original integer edge-cubie permutation parity to the
Boolean sign used by the sign-indexed terminal decoder. This is the
same sign convention as NineteenReadData.check's `parity (w.map (/2))`
and is not an independently guessed corner parity bit. -/
def edgeWordSign (word : Word) : Bool :=
  parity (word.map (· / 2)) == 1

/-- Parse one original JSON representative record using the existing
frozen certificate data path and the checked total typed parser.
Every initial candidate comes from NineteenReadData.sector, not from
a freshly invented or filtered candidate universe. -/
def parseRepresentativeRoot (entry : Lean.Json) :
    Except String
      (Array (FrozenInstruction Nat Nat Unit) × List Word) := do
  let first ← (← entry.getObjVal? "prefix").getStr?
  let nodes ← (← entry.getObjVal? "nodes").getArr?
  let graph ← parseFrozenSectorNodes nodes
  let firstCodes := first.toList.map colorCode
  unless firstCodes.length == 11 do
    throw "Representative prefix length is not eleven."
  pure (graph, sector (List.range 12) 0 firstCodes)

/-- This exact root Boolean is structurally justified by
checkDistinctSector_sound: if it is true, every surviving candidate is
reconstructed from its true signed leaf. There are NO hardcoded leaf
counts in this accept predicate. -/
def checkedRepresentativeRoot (entry : Lean.Json) : Bool :=
  match parseRepresentativeRoot entry with
  | .ok (graph, belief) =>
      checkDistinctSector graph observation edgeWordSign 8 0 belief
  | .error _ => false

/-- Fetch the actual representative array from the same original
unmodified JSON certificate used by the frozen 19-read receipt. -/
def parsedRepresentativeArray (source : String) :
    Except String (Array Lean.Json) := do
  let document ← Lean.Json.parse source
  (← document.getObjVal? "representatives").getArr?

/-- A stronger, executable exact-source gate combining:
(1) NineteenReadData.check's original 52-representative/1362-count
    and DAG structural receipt;
(2) exactly 52 raw representative entries;
(3) a TRUE typed, candidate-exhaustive, deduplicated-reply semantic
    checker for each and every actual entry in the same JSON bytes.

This gate returns FALSE on any error or malformed root. -/
def certifiedFrozenRoots (source : String) : Bool :=
  match check source, parsedRepresentativeArray source with
  | .ok original, .ok roots =>
      (original == (⟨52, 1362, 144736, 141097, 3188, 70774⟩ : Receipt)) &&
        ((roots.size == 52) &&
          allFinite checkedRepresentativeRoot roots.toList)
  | _, _ => false

/-- Fully generic soundness of the JSON-to-typed-root finite reflection.
If the *same source* passes the original frozen receipt and our new
recomputed verifier, each member of the parsed root list has an EXACT
candidate list, a typed instruction array and a sound StatewiseSectorValid
witness. This is NOT merely a proof that the number of leaves is right. -/
theorem certified_source_each_root_has_exact_semantics
    (source : String) (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray source = .ok roots)
    (accepted : certifiedFrozenRoots source = true)
    (entry : Lean.Json) (member : entry ∈ roots.toList) :
    ∃ (graph : Array (FrozenInstruction Nat Nat Unit))
      (belief : List Word),
      parseRepresentativeRoot entry = .ok (graph, belief) ∧
      StatewiseSectorValid graph observation edgeWordSign 8 0 belief := by
  cases receiptCheck : check source with
  | error message =>
      simp [certifiedFrozenRoots, receiptCheck] at accepted
  | ok receipt =>
      have combined :
          ((receipt == (⟨52, 1362, 144736, 141097, 3188, 70774⟩ :
              Receipt)) &&
            ((roots.size == 52) &&
              allFinite checkedRepresentativeRoot roots.toList)) = true := by
        simpa [certifiedFrozenRoots, receiptCheck, parsed] using accepted
      simp only [Bool.and_eq_true] at combined
      have everyRoot : allFinite checkedRepresentativeRoot
          roots.toList = true := combined.2.2
      have acceptedEntry : checkedRepresentativeRoot entry = true :=
        allFinite_true_implies_every_member
          checkedRepresentativeRoot roots.toList everyRoot entry member
      cases parsedEntry : parseRepresentativeRoot entry with
      | error explanation =>
          simp [checkedRepresentativeRoot, parsedEntry] at acceptedEntry
      | ok payload =>
          rcases payload with ⟨graph, belief⟩
          have checked :
              checkDistinctSector graph observation edgeWordSign
                8 0 belief = true := by
            simpa [checkedRepresentativeRoot, parsedEntry] using
              acceptedEntry
          exact ⟨graph, belief, rfl,
            checkDistinctSector_sound graph observation edgeWordSign
              8 0 belief checked⟩

/-- For every *actual* original root of an accepted source, the
constructed continuation can now be instantiated at each original
candidate. The external sign must still be physically derived from the
final legal-corner observations; this lemma does not supply it. -/
theorem certified_source_each_root_recovers
    (source : String) (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray source = .ok roots)
    (accepted : certifiedFrozenRoots source = true)
    (entry : Lean.Json) (member : entry ∈ roots.toList) :
    ∃ (graph : Array (FrozenInstruction Nat Nat Unit))
      (belief : List Word),
      parseRepresentativeRoot entry = .ok (graph, belief) ∧
      (∀ word, word ∈ belief →
        ((exactEightSectorPolicy 0 graph observation edgeWordSign
          0 belief).run observation word) (edgeWordSign word) =
          some word) := by
  obtain ⟨graph, belief, matched, valid⟩ :=
    certified_source_each_root_has_exact_semantics
      source roots parsed accepted entry member
  exact ⟨graph, belief, matched, fun word inBelief =>
    exact_eight_sector_recovers_given_terminal_sign
      0 graph observation edgeWordSign 0 belief
      valid word inBelief⟩

#print axioms certified_source_each_root_has_exact_semantics
#print axioms certified_source_each_root_recovers

end CubeRev029.Nineteen

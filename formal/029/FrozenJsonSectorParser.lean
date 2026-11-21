import SectorSemanticCompiler
import NineteenReadData

namespace CubeRev029.Nineteen

open Eighteen

/-- A certificate's query address is a sector index in [0,12]:
0..10 are the second sticker of one of the eleven already first-read edges;
11 and 12 address the two stickers of the last unread edge. The real
corner address is supplied separately by the fixed nineteen-frame schedule.

An invalid response or index is routed to a nonexistent node, so the
semantic interpreter fails closed instead of inventing a successful leaf. -/
def parseFrozenSectorNode (invalidIndex : Nat) (node : Lean.Json) :
    Except String (FrozenInstruction Nat Nat Unit) := do
  let row ← node.getArr?
  match row.toList with
  | [tag] =>
      unless (← tag.getStr?) == "leaf" do
        throw "Invalid singleton node tag."
      pure (.finish ())
  | [tag, destination] =>
      unless (← tag.getStr?) == "repeat" do
        throw "Invalid padding node tag."
      let child ← destination.getNat?
      -- 0 is a real allowed edge-color query. Its response is discarded
      -- by the repeat node, but the frame is still counted.
      pure (.padding 0 child)
  | [tag, address, branches] =>
      unless (← tag.getStr?) == "read" do
        throw "Invalid read node tag."
      let q ← address.getNat?
      unless q < 13 do throw "Out-of-range sector address."
      let alternatives ← branches.getObj?
      let validKeys := (List.range 6).map
        (fun c => String.singleton colors[c]!)
      unless alternatives.toList.all
          (fun entry => validKeys.contains entry.1) do
        throw "Unexpected color response label."
      let mut destinations : Array Nat := #[]
      for c in List.range 6 do
        match alternatives.get? (String.singleton colors[c]!) with
        | some value =>
            destinations := destinations.push (← value.getNat?)
        | none =>
            -- Missing impossible replies never provide a free oracle;
            -- if physically encountered, they reach an invalid node.
            destinations := destinations.push invalidIndex
      pure (.choose q (fun answer =>
        (destinations[answer]?).getD invalidIndex))
  | _ => throw "Malformed frozen sector instruction."

/-- Parse a complete frozen JSON node table with an unambiguous invalid
destination equal to the array length. This is an actual interpreter of
the read/repeat/leaf vocabulary in the pinned 52 representative trees;
further candidate-sector correctness is a separate semantic proof gate. -/
def parseFrozenSectorNodes (nodes : Array Lean.Json) :
    Except String (Array (FrozenInstruction Nat Nat Unit)) := do
  let mut result : Array (FrozenInstruction Nat Nat Unit) := #[]
  for node in nodes do
    result := result.push (← parseFrozenSectorNode nodes.size node)
  pure result

theorem exact_frozen_leaf_parse (invalidIndex : Nat) :
    parseFrozenSectorNode invalidIndex
      (Lean.Json.arr #[Lean.Json.str "leaf"]) =
        .ok (.finish ()) := by
  rfl

theorem malformed_singleton_is_rejected (invalidIndex : Nat) :
    parseFrozenSectorNode invalidIndex
      (Lean.Json.arr #[Lean.Json.str "made-up-leaf"]) =
        .error "Invalid singleton node tag." := by
  rfl

/-- Once exact JSON parsing succeeds, its fully typed graph can be compiled
at any budget into a policy bounded on every possible reply branch, even
ones that do not occur for a physically legal edge state. This is the
generic budget half of the parser/semantic connection, not its correctness
on the 52 actual frozen sectors. -/
theorem parsed_sector_has_bounded_policy
    (raw : Array Lean.Json)
    (nodes : Array (FrozenInstruction Nat Nat Unit))
    (parsed : parseFrozenSectorNodes raw = .ok nodes)
    (sign : Word → Bool) (budget : Nat) (belief : List Word) :
    Fits budget
      (compileSectorDecoder nodes
        (fun (word : Word) (q : Nat) => observation word q)
        sign budget 0 belief).val := by
  exact compiled_sector_fits_all_replies nodes
    (fun (word : Word) (q : Nat) => observation word q)
    sign budget 0 belief

#print axioms exact_frozen_leaf_parse
#print axioms malformed_singleton_is_rejected
#print axioms parsed_sector_has_bounded_policy

end CubeRev029.Nineteen

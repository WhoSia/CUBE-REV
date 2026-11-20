import EighteenReadData

namespace CubeRev029.Nineteen

open Eighteen

def collation : List Nat := "URFDLB".toList.map colorCode

def opposite (c : Nat) : Nat := [2, 5, 0, 4, 3, 1][c]!

def permutationsOf (unused : List Nat) : Nat → List (List Nat)
  | 0 => [[]]
  | n+1 => unused.flatMap (fun c => (permutationsOf (unused.erase c) n).map (c :: ·))

def symmetries : List (List Nat) :=
  (permutationsOf (List.range 6) 6).filter fun σ =>
    (List.range 6).all fun c => σ[opposite c]! == opposite σ[c]!

def counts (xs : List Nat) : List Nat :=
  collation.map fun c => (xs.filter (· == c)).length

def lexLess : List Nat → List Nat → Bool
  | x :: xs, y :: ys => x < y || (x == y && lexLess xs ys)
  | [], _ :: _ => true
  | _, _ => false

def rawWords : List Nat → List (List Nat)
  | [] => [[]]
  | id :: ids =>
      let tails := rawWords ids
      tails.map (sticker (2*id) false :: ·) ++ tails.map (sticker (2*id) true :: ·)

def representativeVectors : Nat × Std.HashSet (List Nat) :=
  Id.run do
    let labels := List.range 12
    let mut vectors : Std.HashSet (List Nat) := {}
    for omitted in labels do
      for row in rawWords (labels.erase omitted) do
        vectors := vectors.insert (counts row)
    let mut representatives : Std.HashSet (List Nat) := {}
    for key in vectors.toList do
      let word := (collation.zip key).flatMap fun (c, n) => List.replicate n c
      let best := symmetries.foldl (fun best σ =>
        let candidate := counts (word.map (σ[·]!))
        if lexLess candidate best then candidate else best) key
      representatives := representatives.insert best
    return (vectors.size, representatives)

def sector (unread : List Nat) (flip : Nat) : List Nat → List Word
  | [] =>
      match unread with
      | [id] => [[2*id + flip]]
      | _ => []
  | c :: cs =>
      unread.flatMap fun id =>
        let first := sticker (2*id) false
        let second := sticker (2*id) true
        if first == c then
          (sector (unread.erase id) flip cs).map (2*id :: ·)
        else if second == c then
          (sector (unread.erase id) (1-flip) cs).map ((2*id+1) :: ·)
        else []

def observation (w : Word) (q : Nat) : Nat :=
  if q < 11 then sticker w[q]! true else sticker w[11]! (q == 12)

structure TreeReceipt where
  visited : Std.HashSet Nat := {}
  singleton : Nat := 0
  pair : Nat := 0

def verifyNode (tree : Array Lean.Json) (idx : Nat) (assignments : List (Word × Nat))
    (receipt : TreeReceipt) (budget : Nat) : Except String TreeReceipt := do
  let some node := tree[idx]? | throw "Missing tree node."
  let row ← node.getArr?
  if receipt.visited.contains idx then throw "Reused or cyclic tree node."
  if assignments.isEmpty then throw "Empty node."
  let receipt := { receipt with visited := receipt.visited.insert idx }
  match budget, row.toList with
  | _, [tag] =>
      unless (← tag.getStr?) == "leaf" do throw "Invalid leaf."
      match assignments with
      | [_] => pure { receipt with singleton := receipt.singleton + 1 }
      | [a,b] =>
          unless a.2 != b.2 do throw "Two candidates of the same sign."
          pure { receipt with pair := receipt.pair + 1 }
      | _ => throw "Unresolved leaf."
  | n+1, [tag, dest] =>
      unless (← tag.getStr?) == "repeat" do throw "Invalid two-field node."
      verifyNode tree (← dest.getNat?) assignments receipt n
  | n+1, [tag, address, branches] =>
      unless (← tag.getStr?) == "read" do throw "Invalid three-field node."
      let q ← address.getNat?
      unless q < 13 do throw "Invalid query address."
      let alternatives ← branches.getObj?
      let mut total := 0
      let mut acc := receipt
      for c in List.range 6 do
        let group := assignments.filter fun a => observation a.1 q == c
        unless group.isEmpty do
          let some dest := alternatives.get? (String.singleton colors[c]!) | throw "Missing reply branch."
          acc ← verifyNode tree (← dest.getNat?) group acc n
          total := total + 1
      unless total == alternatives.toList.length do throw "Infeasible reply branch."
      pure acc
  | _, _ => throw "Budget exhausted or malformed node."

structure Receipt where
  representatives : Nat
  rawVectors : Nat
  candidates : Nat
  nodes : Nat
  singleton : Nat
  pair : Nat
  deriving BEq, Repr

def check (source : String) : Except String Receipt := do
  let input ← Lean.Json.parse source
  unless (← (← input.getObjVal? "schema").getStr?) == "cuberev-0.29-upper-policy-v1" &&
      (← (← input.getObjVal? "remaining_budget").getNat?) == 8 &&
      (← (← input.getObjVal? "first_slots").getNat?) == 11 &&
      (← (← input.getObjVal? "sign_release").getStr?) == "terminal" do
    throw "Incorrect certificate parameters."
  let cert ← (← input.getObjVal? "representatives").getArr?
  let (raw, expected) := representativeVectors
  unless symmetries.length == 48 && raw == 1362 && expected.size == 52 do
    throw "Unexpected symmetry or raw-prefix count."
  let mut seen : Std.HashSet (List Nat) := {}
  let mut tally : Receipt := ⟨cert.size, raw, 0, 0, 0, 0⟩
  for entry in cert do
    let text ← (← entry.getObjVal? "prefix").getStr?
    let firstColors := text.toList.map colorCode
    let key := counts firstColors
    let sorted := (collation.zip key).flatMap fun (c, n) => List.replicate n c
    unless firstColors.length == 11 && firstColors == sorted && expected.contains key && !seen.contains key do
      throw ("Invalid or repeated representative: " ++ text)
    seen := seen.insert key
    let words := (sector (List.range 12) 0 firstColors).map (fun w => (w, parity (w.map (· / 2))))
    let nodes ← (← entry.getObjVal? "nodes").getArr?
    let result ← verifyNode nodes 0 words {} 8
    unless result.visited.size == nodes.size &&
        result.singleton + 2 * result.pair == words.length do throw "Missing node or incomplete assignments."
    tally := { tally with candidates := tally.candidates + words.length,
                          nodes := tally.nodes + nodes.size,
                          singleton := tally.singleton + result.singleton,
                          pair := tally.pair + result.pair }
  unless seen.size == expected.size do throw "Missing representative."
  pure tally

end CubeRev029.Nineteen

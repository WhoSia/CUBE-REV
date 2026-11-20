import Lean
import Std

namespace CubeRev029.Eighteen

def colors : List Char := "BDFLRU".toList
def labelNames : List String := ["DL", "BL", "FL", "UL", "DB", "DF", "UB", "UF", "DR", "BR", "FR", "UR"]
def blank : Nat := 6

structure Position where
  labels : List Nat
  record : List Nat
  sign : Nat
  flip : Nat
  budget : Nat
  deriving BEq, Hashable, Repr

abbrev Word := List Nat
abbrev Pair := Word × Word
abbrev Certificate := Std.HashMap Position Lean.Json

def colorCode (c : Char) : Nat := colors.idxOf c
def readColor (s : String) : Option Nat :=
  match s.toList with
  | [c] => if colorCode c < blank then some (colorCode c) else none
  | _ => none

def sticker (word : Nat) (side : Bool) : Nat :=
  let label := labelNames[word / 2]!
  colorCode (label.toList[(word % 2 + side.toNat) % 2]!)

def queryAddresses (record : List Nat) : List (Nat × Bool) :=
  (List.range record.length).flatMap fun i =>
    if record[i]! == blank then [(i, false), (i, true)] else [(i, true)]

def parsePosition (key : String) : Except String Position := do
  let [labels, record, sign, flip, budget] := key.splitOn ":" | throw ("Malformed key: " ++ key)
  let labels := if labels.isEmpty then [] else (labels.splitOn ",").map labelNames.idxOf
  unless record.toList.all (fun c => c == '-' || colorCode c < blank) do
    throw ("Invalid recorded color: " ++ key)
  let record := record.toList.map colorCode
  let some sign := sign.toNat? | throw ("Invalid sign: " ++ key)
  let some flip := flip.toNat? | throw ("Invalid flip: " ++ key)
  let some budget := budget.toNat? | throw ("Invalid budget: " ++ key)
  unless labels.length == record.length && labels.all (· < labelNames.length) &&
      labels.eraseDups.length == labels.length && sign < 2 && flip < 2 && budget ≤ 18 do
    throw ("Invalid state: " ++ key)
  pure ⟨labels, record, sign, flip, budget⟩

def parseOriented (s : String) : Except String Nat := do
  for id in List.range labelNames.length do
    let label := labelNames[id]!
    if s == label then return 2 * id
    if s == String.ofList label.toList.reverse then return 2 * id + 1
  throw ("Invalid oriented label: " ++ s)

def parseWord (j : Lean.Json) : Except String Word := do
  (← j.getArr?).toList.mapM fun token => do parseOriented (← token.getStr?)

def inversions : List Nat → Nat
  | [] => 0
  | x :: xs => xs.countP (· < x) + inversions xs

def parity (xs : List Nat) : Nat := inversions xs % 2

theorem inversions_insert (before after : List Nat) (rank : Nat) :
    inversions (before ++ [rank] ++ after) =
      inversions (before ++ after) +
      before.countP (rank < ·) + after.countP (· < rank) := by
  induction before with
  | nil => simp [inversions, Nat.add_comm]
  | cons x xs ih =>
      simp only [List.cons_append, inversions, List.countP_append, List.countP_cons,
        List.countP_nil]
      rw [ih]
      omega

theorem inversions_map_order (f : Nat → Nat) (order : ∀ a b, f a < f b ↔ a < b)
    (xs : List Nat) : inversions (xs.map f) = inversions xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      have comparisons : (fun y => decide (f y < f x)) = (fun y => decide (y < x)) := by
        funext y
        simp only [order]
      simp only [List.map_cons, inversions, ih, List.countP_map, Function.comp_def]
      rw [comparisons]

theorem count_below_above (xs : List Nat) (rank : Nat) (noRank : rank ∉ xs) :
    xs.countP (· < rank) + xs.countP (rank < ·) = xs.length := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      have noHead : rank ≠ x := fun eq => noRank (by simp [eq])
      have noTail : rank ∉ xs := fun found => noRank (List.mem_cons_of_mem x found)
      have count := ih noTail
      simp only [List.countP_cons, List.length_cons]
      by_cases h : x < rank
      · have h' : ¬ rank < x := by omega
        simp [h, h']
        omega
      · have h' : rank < x := by omega
        simp [h, h']
        omega

/-- If the other ranks include exactly `rank` values smaller than the
inserted rank, the sign change is the sum of the position and rank modulo 2. -/
theorem parity_insert_rank (before after : List Nat) (rank : Nat)
    (noRank : rank ∉ before)
    (smaller : (before ++ after).countP (· < rank) = rank) :
    parity (before ++ [rank] ++ after) =
      (parity (before ++ after) + before.length + rank) % 2 := by
  have across := count_below_above before rank noRank
  rw [List.countP_append] at smaller
  unfold parity
  rw [inversions_insert]
  omega

def labelSign (labels : List Nat) (w : Word) : Nat :=
  parity (w.map fun id => labels.idxOf (id / 2))

def reverseWord (id : Nat) : Nat := 2 * (id / 2) + (1 - id % 2)

theorem reverseWord_label (id : Nat) : reverseWord id / 2 = id / 2 := by
  unfold reverseWord
  omega

theorem reverseWord_bit (id : Nat) : reverseWord id % 2 = 1 - id % 2 := by
  unfold reverseWord
  omega

def flipBit (w : Word) : Nat := (w.map (· % 2)).sum % 2

theorem flipBit_append (a b : Word) : flipBit (a ++ b) = (flipBit a + flipBit b) % 2 := by
  simp only [flipBit, List.map_append, List.sum_append]
  exact Nat.add_mod _ _ _

theorem flipBit_reorder (a b : Word) (order : a.Perm b) : flipBit a = flipBit b := by
  induction order with
  | nil => rfl
  | cons id _ ih =>
      simp only [flipBit, List.map_cons, List.sum_cons] at ih ⊢
      omega
  | swap x y tail =>
      simp only [flipBit, List.map_cons, List.sum_cons]
      omega
  | trans _ _ first second => exact first.trans second

theorem flipBit_reinsert (before after : Word) (id : Nat) :
    flipBit (before ++ [id] ++ after) = (flipBit (before ++ after) + id % 2) % 2 := by
  have even := flipBit_append before after
  simp only [flipBit, List.map_append, List.map_cons, List.map_nil, List.sum_append,
    List.sum_cons, List.sum_nil, Nat.add_zero] at even ⊢
  omega

theorem flipBit_reverse_one (w : Word) (i id : Nat) (h : w[i]? = some id) :
    flipBit (w.set i (reverseWord id)) = (flipBit w + 1) % 2 := by
  induction w generalizing i with
  | nil => simp at h
  | cons hd tl ih =>
      cases i with
      | zero =>
          simp only [List.getElem?_cons_zero, Option.some.injEq] at h
          subst hd
          simp only [List.set_cons_zero, flipBit, List.map_cons, List.sum_cons, reverseWord_bit]
          omega
      | succ i =>
          simp only [List.getElem?_cons_succ] at h
          have changed := ih i h
          simp only [List.set_cons_succ, flipBit, List.map_cons, List.sum_cons] at changed ⊢
          omega

def legal (p : Position) (w : Word) : Bool :=
  w.length == p.labels.length &&
    w.all (fun id => p.labels.contains (id / 2)) &&
    (w.map (· / 2)).eraseDups.length == p.labels.length &&
    labelSign p.labels w == p.sign && flipBit w == p.flip &&
    (p.record.zip w).all (fun (color, id) => color == blank || sticker id false == color)

def root (sign : Nat) : Position :=
  ⟨List.range labelNames.length, List.replicate labelNames.length blank, sign, 0, 18⟩

def invert (p : Position) (i : Nat) (side : Bool) (reply : Nat) :
    Except String (Position × (Word → Word)) := do
  let seen := p.record[i]!
  if seen == blank then
    let updated := p.record.set i reply
    let order := (List.range 7).flatMap fun c => (List.range updated.length).filter (updated[·]! == c)
    let childRecord := order.map (updated[·]!)
    let lift := fun w : Word => (List.range order.length).map fun parent =>
      let id := w[order.idxOf parent]!
      if parent == i && side then reverseWord id else id
    let image := lift (p.labels.map (2 * ·))
    return (⟨p.labels, childRecord, (p.sign + labelSign p.labels image) % 2,
             (p.flip + flipBit image) % 2, p.budget - 1⟩, lift)
  else
    let words := p.labels.flatMap fun id => [2 * id, 2 * id + 1]
    let some fixed := words.find? (fun id => sticker id false == seen && sticker id true == reply)
      | throw "No legal label has the recorded pair."
    let smallerLabels := p.labels.erase (fixed / 2)
    let lift := fun w : Word => w.take i ++ [fixed] ++ w.drop i
    let image := lift (smallerLabels.map (2 * ·))
    return (⟨smallerLabels, p.record.eraseIdx i, (p.sign + labelSign p.labels image) % 2,
             (p.flip + flipBit image) % 2, p.budget - 1⟩, lift)

def wordPair (p : Position) (rows : List Lean.Json) : Except String Pair := do
  let [x, y] := rows | throw "Expected two leaf words."
  let a ← parseWord x
  let b ← parseWord y
  unless a != b && legal p a && legal p b do throw "Malformed or identical leaf witnesses."
  return (a, b)

structure Receipt where
  nodes : Nat
  arcs : Nat
  leaves : Nat
  lifted : Nat
  deriving BEq, Repr

def check (source : String) : Except String Receipt := do
  let obj ← (← Lean.Json.parse source).getObj?
  let mut positions := #[]
  let mut supplied : Certificate := {}
  for (key, row) in obj.toList do
    let p ← parsePosition key
    if supplied.contains p then throw "Repeated canonical key."
    supplied := supplied.insert p row
    positions := positions.push p
  let mut completed : Std.HashMap Position Pair := {}
  let mut arcs := 0
  let mut leaves := 0
  let mut childPositions : Std.HashSet Position := {}
  for budget in List.range 19 do
    for p in positions do
      if p.budget == budget then
        let row ← supplied[p]!.getArr?
        if budget == 0 then
          completed := completed.insert p (← wordPair p row.toList)
          leaves := leaves + 1
        else
          let queries := queryAddresses p.record
          unless row.size == queries.length && row.size > 0 do throw "Incomplete query list."
          let mut sample : Option Pair := none
          for ((i, side), answer) in queries.zip row.toList do
            let some c := readColor (← answer.getStr?) | throw "Invalid reply."
            let (child, lift) ← invert p i side c
            let some pair := completed[child]? | throw ("Missing verified child: " ++ reprStr child)
            let left := lift pair.1
            let right := lift pair.2
            unless left != right && legal p left && legal p right &&
                sticker left[i]! side == c && sticker right[i]! side == c do
              throw ("Lift fails at " ++ reprStr p)
            if sample.isNone then sample := some (left, right)
            arcs := arcs + 1
            childPositions := childPositions.insert child
          let some pair := sample | throw "Missing parent witnesses."
          completed := completed.insert p pair
  unless completed.contains (root 0) && completed.contains (root 1) do
    throw "Missing a parity root."
  -- Every non-root supplied row is somebody's child. Since child budgets
  -- decrease by one, this also excludes disconnected components.
  for p in positions do
    unless p == root 0 || p == root 1 || childPositions.contains p do
      throw "Unreachable record."
  return ⟨completed.size, arcs, leaves, 2 * arcs⟩

end CubeRev029.Eighteen

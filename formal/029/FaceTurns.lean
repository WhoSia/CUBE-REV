import EighteenReadData

namespace CubeRev029.Physical

open Eighteen

abbrev Slot := Fin 48
abbrev Turn := Fin 12
abbrev Vec := Int × Int × Int
abbrev Geometry := Vec × Vec

def normal : Char → Vec
  | 'U' => (0,1,0)
  | 'R' => (1,0,0)
  | 'F' => (0,0,1)
  | 'D' => (0,-1,0)
  | 'L' => (-1,0,0)
  | 'B' => (0,0,-1)
  | _ => (0,0,0)

def add (a b : Vec) : Vec :=
  (a.1+b.1, a.2.1+b.2.1, a.2.2+b.2.2)

def scale (m : Int) (a : Vec) : Vec :=
  (m*a.1, m*a.2.1, m*a.2.2)

def dot (a b : Vec) : Int :=
  a.1*b.1 + a.2.1*b.2.1 + a.2.2*b.2.2

def cross (a b : Vec) : Vec :=
  (a.2.1*b.2.2-a.2.2*b.2.1, a.2.2*b.1-a.1*b.2.2, a.1*b.2.1-a.2.1*b.1)

def rotate (axis : Vec) (direction : Int) (v : Vec) : Vec :=
  add (scale direction (cross axis v)) (scale (dot v axis) axis)

def cornerNames : List String := ["UFR", "URB", "ULF", "UBL", "DRF", "DBR", "DFL", "DLB"]

def names : List String := labelNames ++ cornerNames

def slots : List Geometry :=
  names.flatMap fun piece =>
    let ds := piece.toList.map normal
    let p := ds.foldl add (0,0,0)
    ds.map (p, ·)

def face (t : Turn) : Char := "URFDLB".toList[t.val / 2]!

def quarterGeometry (t : Turn) (s : Geometry) : Geometry :=
  let axis := normal (face t)
  let direction := if t.val % 2 == 0 then -1 else 1
  if dot s.1 axis == 1 then (rotate axis direction s.1, rotate axis direction s.2)
  else s

def slotOf (s : Geometry) : Option Slot :=
  let k := slots.idxOf s
  if inside : k < 48 then some ⟨k, inside⟩ else none

def turnSlot (t : Turn) (s : Slot) : Slot :=
  (slotOf (quarterGeometry t slots[s.val]!)).getD s

def inverseTurn (t : Turn) : Turn :=
  if h : t.val % 2 = 0 then ⟨t.val + 1, by have := t.isLt; omega⟩
  else ⟨t.val - 1, by have := t.isLt; omega⟩

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem geometry_is_closed :
    slots.length = 48 ∧ slots.Nodup ∧
      ∀ t : Turn, ∀ s : Slot, (slotOf (quarterGeometry t slots[s.val]!)).isSome = true := by
  decide +kernel

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem turn_inverse : ∀ (t : Turn) (s : Slot), turnSlot (inverseTurn t) (turnSlot t s) = s := by
  decide +kernel

abbrev Coloring := Slot → Nat

def solved : Coloring :=
  fun s => colorCode (names.flatMap String.toList)[s.val]!

def turnColoring (t : Turn) (c : Coloring) : Coloring :=
  fun s => c (turnSlot t s)

def follow (turns : List Turn) (s : Slot) : Slot :=
  turns.foldl (fun x t => turnSlot t x) s

/-- The moves are stored in lookup order. Each lookup pulls a sticker
from a face quarter-turn, so the physical execution order is reversed. -/
def paint (turns : List Turn) (c : Coloring) : Coloring :=
  fun s => c (follow turns s)

def Reachable (c : Coloring) : Prop :=
  ∃ turns : List Turn, c = paint turns solved

theorem paint_append (a b : List Turn) (c : Coloring) :
    paint (a ++ b) c = paint a (paint b c) := by
  funext s
  simp [paint, follow, List.foldl_append]

theorem paint_cons (t : Turn) (ts : List Turn) (c : Coloring) :
    paint (t::ts) c = turnColoring t (paint ts c) := rfl

theorem paint_reachable (c : Coloring) (h : Reachable c) (turns : List Turn) :
    Reachable (paint turns c) := by
  obtain ⟨w, rfl⟩ := h
  exact ⟨turns ++ w, (paint_append _ _ _).symm⟩

theorem solved_reachable : Reachable solved := ⟨[], rfl⟩

#print axioms geometry_is_closed
#print axioms turn_inverse

end CubeRev029.Physical

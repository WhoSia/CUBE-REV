import ResidualLift

namespace CubeRev029.Eighteen

instance decideAgrees : (cs : List Nat) → (w : Word) → Decidable (Agrees cs w)
  | [], [] => isTrue .nil
  | [], _ :: _ => isFalse (by intro h; cases h)
  | _ :: _, [] => isFalse (by intro h; cases h)
  | c :: cs, id :: w =>
      letI := decideAgrees cs w
      decidable_of_iff ((c = blank ∨ sticker id false = c) ∧ Agrees cs w)
        ⟨fun h => .cons h.1 h.2, fun h => by cases h; constructor <;> assumption⟩

instance decideCompletes (p : Position) (w : Word) : Decidable (Completes p w) :=
  decidable_of_iff ((wordLabels w).Perm p.labels ∧ parity (wordLabels w) = p.sign ∧
      flipBit w = p.flip ∧ Agrees p.record w)
    ⟨fun ⟨l, s, f, r⟩ => ⟨l, s, f, r⟩, fun h => ⟨h.labels, h.sign, h.flip, h.record⟩⟩

instance decideSecond (p child : Position) (i fixed : Nat) : Decidable (SecondStep p child i fixed) :=
  decidable_of_iff (i ≤ child.record.length ∧ fixed / 2 ∈ p.labels ∧ p.labels.Nodup ∧
      child.labels = p.labels.erase (fixed / 2) ∧
      child.record.insertIdx i (sticker fixed false) = p.record ∧
      (child.sign + i + child.labels.countP (· < fixed / 2)) % 2 = p.sign ∧
      (child.flip + fixed % 2) % 2 = p.flip)
    ⟨fun ⟨b, m, nd, l, r, s, f⟩ => ⟨b, m, nd, l, r, s, f⟩,
     fun h => ⟨h.bound, h.labelPresent, h.distinctLabels, h.labels, h.record, h.sign, h.flip⟩⟩

instance decideFirst (p child : Position) (i j : Nat) (side : Bool) (color : Nat) :
    Decidable (FirstStep p child i j side color) :=
  decidable_of_iff (j < child.record.length ∧ i ≤ (child.record.eraseIdx j).length ∧
      child.record[j]? = some color ∧ color ≠ blank ∧
      (child.record.eraseIdx j).insertIdx i blank = p.record ∧ child.labels = p.labels ∧
      child.labels.Nodup ∧ (child.sign + i + j) % 2 = p.sign ∧
      (child.flip + side.toNat) % 2 = p.flip)
    ⟨fun ⟨j', i', c, n, r, l, d, s, f⟩ => ⟨j', i', c, n, r, l, d, s, f⟩,
     fun h => ⟨h.childSlot, h.parentSlot, h.color, h.nonblank, h.record, h.labels, h.distinctLabels,
       h.sign, h.flip⟩⟩

end CubeRev029.Eighteen

import CornerPairDecoder

namespace CubeRev029.Physical

/-- The *actual* nineteen corner-probe addresses of the frozen X controller.
An entry is a corner-sticker index 0..23 in the initial reference pose.
Re-reading address 21 in frames 14--18 is legal padding: its color is already
known, and it cannot influence the simultaneous edge address of that frame. -/
def cornerFrameAddresses : List (Fin 24) :=
  [0, 1, 6, 7, 9, 10, 18, 19, 21, 22, 12,
   13, 3, 21, 21, 21, 21, 21, 4]

/-- Fourteen genuinely distinct ordered corner-sticker addresses in the order
of their first occurrence, corresponding to seven pairs. -/
def cornerFirstOccurrences : List (Fin 24) :=
  [0, 1, 6, 7, 9, 10, 18, 19, 21, 22, 12, 13, 3, 4]

theorem actual_corner_frame_budget : cornerFrameAddresses.length = 19 := by decide

theorem actual_corner_first_eleven_distinct :
    (cornerFrameAddresses.take 11).Nodup := by decide

theorem actual_corner_first_occurences :
    cornerFrameAddresses.eraseDups = cornerFirstOccurrences := by decide

theorem actual_corner_fourteen_distinct :
    cornerFirstOccurrences.Nodup ∧ cornerFirstOccurrences.length = 14 := by decide

/-- The crucial last new corner sticker is URB[2], zero-based sticker 4.
It has not been seen in any of the preceding eighteen replies. -/
theorem final_corner_color_not_early :
    (4 : Fin 24) ∉ cornerFrameAddresses.take 18 ∧
    cornerFrameAddresses[18]! = (4 : Fin 24) := by decide

theorem five_padding_corner_reads :
    (cornerFrameAddresses.drop 13).take 5 = List.replicate 5 (21 : Fin 24) := by decide

/-- The actual schedule, not an idealized seven-position scan, leaves corner
position five unread. Each other corner contributes exactly two distinct cyclic
sticker slots. This is the premise of corner_fourteen_unique_missing_five. -/
theorem actual_corner_schedule_coverage :
    (∀ i : Fin 8, i ≠ 5 →
       ((cornerFirstOccurrences.filter fun slot => slot.val / 3 == i.val)).length = 2) ∧
    ((cornerFirstOccurrences.filter fun slot => slot.val / 3 == 5)).length = 0 := by
  decide

#print axioms actual_corner_frame_budget
#print axioms actual_corner_first_occurences
#print axioms final_corner_color_not_early
#print axioms actual_corner_schedule_coverage

end CubeRev029.Physical

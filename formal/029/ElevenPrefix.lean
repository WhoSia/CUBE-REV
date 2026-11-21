import NineteenCornerTranscript
import ObservationTransport

namespace CubeRev029

/-- Ask a fixed list of paired addresses, recording responses in order, and
then continue with an adaptive policy chosen from those responses.
All queries in the fixed prefix are chosen before any of their answers;
the continuation is only selected after the prefix is complete. -/
def Policy.withPrefix {Q R O : Type}
    (queries : List Q) (reversed : List R)
    (continuation : List R → Policy Q R O) : Policy Q R O :=
  match queries with
  | [] => continuation reversed.reverse
  | query :: remaining =>
      .read query (fun response =>
        Policy.withPrefix remaining (response :: reversed) continuation)

/-- Prefixing an arbitrary adaptive continuation uses exactly the length of
the fixed list in addition to its existing worst-case observation budget. -/
theorem Policy.withPrefix_fits {Q R O : Type}
    (queries : List Q) (reversed : List R)
    (continuation : List R → Policy Q R O)
    {n : Nat}
    (continuationsFit : ∀ replies, Fits n (continuation replies)) :
    Fits (n + queries.length)
      (Policy.withPrefix queries reversed continuation) := by
  induction queries generalizing reversed with
  | nil =>
      simpa [Policy.withPrefix] using continuationsFit reversed.reverse
  | cons query remaining ih =>
      have branches : ∀ r, Fits (n + remaining.length)
          (Policy.withPrefix remaining (r :: reversed) continuation) :=
        fun r => ih (r :: reversed)
      have combined : Fits ((n + remaining.length) + 1)
          (Policy.withPrefix (query :: remaining) reversed continuation) := by
        change Fits ((n + remaining.length) + 1)
          (Policy.read query (fun r =>
            Policy.withPrefix remaining (r :: reversed) continuation))
        exact Fits.read (n + remaining.length) query _ branches
      simpa only [List.length_cons, Nat.succ_eq_add_one, Nat.add_assoc]
        using combined

/-- The continuation sees exactly the ordered prefix transcript, not a
permutation or a look-ahead at any later observation. -/
theorem Policy.withPrefix_run {S Q R O : Type}
    (observe : S → Q → R) (state : S)
    (queries : List Q) (reversed : List R)
    (continuation : List R → Policy Q R O) :
    (Policy.withPrefix queries reversed continuation).run observe state =
      (continuation (reversed.reverse ++ queries.map (observe state))).run
        observe state := by
  induction queries generalizing reversed with
  | nil => simp [Policy.withPrefix]
  | cons query remaining ih =>
      change
        (Policy.withPrefix remaining
          (observe state query :: reversed) continuation).run observe state =
        (continuation
          (reversed.reverse ++
            (observe state query :: remaining.map (observe state)))).run
          observe state
      simpa [List.reverse_cons, List.append_assoc]
        using (ih (observe state query :: reversed))

end CubeRev029

namespace CubeRev029.Physical

/-- The first eleven paired original-coordinate addresses used by the frozen
nineteen-frame physical policy. The edge coordinates are the first facelet
of each of eleven distinct edge positions. -/
def firstElevenPairedAddresses : List (Fin 24 × Fin 24) :=
  [(0, 0), (2, 1), (4, 6), (6, 7), (8, 9), (10, 10),
   (12, 18), (14, 19), (16, 21), (18, 22), (20, 12)]

theorem first_eleven_address_count :
    firstElevenPairedAddresses.length = 11 := by decide

theorem first_eleven_matches_frozen_corner_schedule :
    firstElevenPairedAddresses.map Prod.snd =
      cornerFrameAddresses.take 11 := by decide

theorem first_eleven_edge_addresses :
    firstElevenPairedAddresses.map Prod.fst =
      ([0,2,4,6,8,10,12,14,16,18,20] : List (Fin 24)) := by decide

/-- If every allowed first-eleven reply vector has a verified eight-read
continuation, the composed policy fits exactly the nineteen-frame budget.
This is *conditional*: existence and correctness of the 52 representative
continuations are separate cube-specific proof obligations. -/
theorem nineteen_budget_of_eight_read_continuations
    (next : List FrameColor →
      Policy (Fin 24 × Fin 24) FrameColor Coloring)
    (bounded : ∀ replies, Fits 8 (next replies)) :
    Fits 19 (Policy.withPrefix firstElevenPairedAddresses [] next) := by
  have fit := Policy.withPrefix_fits
    firstElevenPairedAddresses [] next bounded
  simpa [first_eleven_address_count] using fit

#print axioms first_eleven_address_count
#print axioms first_eleven_matches_frozen_corner_schedule
#print axioms first_eleven_edge_addresses
#print axioms nineteen_budget_of_eight_read_continuations

end CubeRev029.Physical

#print axioms CubeRev029.Policy.withPrefix_fits
#print axioms CubeRev029.Policy.withPrefix_run

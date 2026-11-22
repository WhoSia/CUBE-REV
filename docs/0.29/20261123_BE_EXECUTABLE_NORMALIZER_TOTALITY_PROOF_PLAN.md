# CUBE-REV 43 / 0.29-BE — Totality of the executable eleven-slot normalizer

Date: 2026-11-23. Status: **research proof plan, not a Lean-accepted theorem**. Parent state: BD at `41f71f3758e9daa1acd6241df7a51c534fe41674`. Active branch: `research/current`.

## Precise open goal

BD already proves soundness **if** `verifiedBubbleTrace? colorAt = some path`. BE should prove the checker never rejects, for arbitrary `colorAt : Nat → Nat` (a stronger statement than physical feasibility):

```lean
theorem bubble_candidate_sorted_total (colorAt : Nat → Nat) :
    bubbleCandidateSorted colorAt = true := by
  -- OPEN: derive the invariant below; do not replace with a finite transcript check.
  sorry

theorem verified_bubble_trace_total (colorAt : Nat → Nat) :
    verifiedBubbleTrace? colorAt =
      some (bubbleCandidatePath11 colorAt) := by
  simp [verifiedBubbleTrace?, bubble_candidate_sorted_total]
```

**These snippets are specifications only; neither is committed to a compiled `.lean` file.** In particular, the `sorry` is an explicit proof placeholder in this *document*, not an accepted result.

## Actual implementation inspected

`elevenBubbleSchedule` is the concatenation of eleven identical passes with adjacent positions 0,…,9 (110 scheduled comparisons). `bubbleCandidateTrace11` stores the swap indices as `Fin 10`, replays the current permutation, and swaps positions `i` and `i+1` when `elevenSlotLexLE colorAt right left` is true. Each element is a distinct original slot index; the comparator orders the pair `(colorAt index, index)` lexicographically, so two *different* slot IDs cannot compare equal even when their colors match. Thus the swapped condition is a genuine strict inversion for distinct elements. This distinctness proviso is essential: on arbitrary lists with duplicate IDs, a non-strict swap could exchange equal elements, invalidating a strictly decreasing inversion-count proof, though not necessarily sortedness.

## Preferred invariant — one maximal element per left-to-right pass

For an arbitrary 11-element list `xs` of **distinct slot IDs**, a left-to-right pass of adjacent compare/exchange preserves the list multiset and puts its greatest element at the final position. More strongly, after `k` full passes (0 ≤ k ≤ 10):

1. the last `k` positions contain the `k` greatest IDs under the fixed color/index comparator, in nondecreasing order;
2. no comparison within the next pass can dislodge those already fixed suffix elements: when the sweep reaches their boundary, the left side is ≤ the fixed right side;
3. the remaining prefix consists exactly of the complementary multiset.

At k = 10, the remaining single element precedes the sorted ten-element suffix and the entire eleven-list is pairwise sorted. The eleventh pass is redundant, but harmless. The existing 11×10 schedule therefore has sufficient coverage. A proof should be given for the *actual replay-based fold* rather than merely a mathematically similar sorter.

## Lean decomposition / proof obligations

**BE1 — comparator laws.** Reuse `eleven_slot_lex_antisymm` and `eleven_slot_lex_refl`; prove totality, transitivity, and that comparing distinct slot IDs in both directions cannot both give true. Keep tie-breaking by original index. No assumption that observed colors are distinct.

**BE2 — one comparator step.** Introduce a pure list-level compare/exchange at boundary `i`, then show its resulting list equals `adjacent i xs` precisely when the existing fold emits `i`. Establish length preservation and permutation as existing helpers permit. Verify the orientation of the output-to-input position map.

**BE3 — one pass.** Prove via induction on boundary index that the maximum of the visited prefix appears at the sweep frontier. This is stronger and less fragile than proving final sortedness directly. Protect list accesses with `length = 11` and `i < 10`, not unchecked `get! ` reasoning alone.

**BE4 — fixed suffix.** Induct over pass count; prove suffix stability and sortedness, including the extra redundant eleventh pass. Explicitly bridge the fold over the schedule to `adjTrace (bubbleCandidatePath11 colorAt) (List.range 11)`.

**BE5 — close executable totality.** Derive `List.Pairwise (fun i j => elevenSlotLexLE colorAt i j = true) ...`, hence `bubbleCandidateSorted colorAt = true`, then `verifiedBubbleTrace?` always returns `some`, and finally reuse BD's `verified_bubble_trace_sound`. Keep `#print axioms` receipts and run the pinned complete Lean gate before marking accepted.

## Independent counterexample gate

Check the invariants on worst-case reverse-ordered colors, all-equal colors (where *original index* is the tie-breaker), and alternating color ranks. These are debugging witnesses only, never substitutes for BE3–BE5. Verify that `Fin 10` excludes slot 11 throughout and that signed parity remains the frozen combined position-plus-gauge correction.

## Separate global-physical barrier

Closing BE5 would prove **normalizer totality**, not full nineteen-frame physical identification. The latter still needs statewise validity of every feasible branch in all 52 frozen signed sectors, plus terminal corner sign derived solely from actual corner observations by frame 19. Neither a sorted output nor a finite Python replay establishes those semantic obligations.

## Evidence discipline

No extra Python auditor; no archive deletion without an exact-byte Drive receipt and manifest SHA comparison; no `github-actions[bot]` writes. Maintain `research/current` and preserve `main`. Classify each claim as proposed, Lean-compiled, or full-pipeline verified; update the paper/README only after the corresponding stronger gate.

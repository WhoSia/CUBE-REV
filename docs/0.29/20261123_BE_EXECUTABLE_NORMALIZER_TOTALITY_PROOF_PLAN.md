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

## BE source implementation receipts — pending Lean CI

The research branch now contains two separate human-attributed source commits:

- `ea9d2735cb40db8a07a9f56d711e6207ddd9c830`: proposed closed finite-schedule certificates `eleven_bubble_schedule_length` and `eleven_bubble_schedule_boundary_multiplicity`. These pin 110 comparisons and eleven visits to each of the ten boundaries.
- `478dd1c1d745651bb83c06fc716c05b6ff4fcaa4`: proposed `eleven_slot_lex_reverse_is_strict`, deriving strictness of an executed comparison from antisymmetry and distinct original slot IDs.

**Acceptance gate:** GitHub reported both commit author and committer as `WhoSia`, not an Actions bot. At inspection, the GitHub commit status endpoint exposed no CI statuses on these commits. Therefore these new Lean declarations are **source-authored, not independently compile-accepted**. They do not imply the unproved one-pass suffix invariant, `bubbleCandidateSorted = true`, or physical `Fits 19`. A pinned clean Lean build and axiom prints are still necessary.

## BF — Concrete recorder/direct-execution refinement (source authored)

A new proof layer replaces informal claims that the candidate is 'like bubble sort' with equations about the **actual recorded path**:

- `bubbleOrderStep`: direct compare/exchange on the currently ordered slot IDs.
- `bubblePathStep`: the original recorder transition, factored into a named function without changing the recorded semantics.
- `bubble_path_step_replay`: exact one-step list equality between replay and direct execution.
- `bubble_fold_replay`: arbitrary-schedule induction, explicitly parameterized by the preceding path.
- `bubble_candidate_trace_is_fold` and `bubble_candidate_replay_eq_direct_fold`: specialize to the original executable `bubbleCandidateTrace11`; the bridge is *not* about a toy implementation.
- `bubble_order_step_perm`, `bubble_order_step_length` and `bubble_direct_fold_perm`: multiset and length preservation for every step and every schedule. These results are independent of whether the order is sorted.

Source commits on `research/current`:
- `cfaae0a7b37113dd06db0b05122c2ec261400f10`
- `d7928aa49fce6c9618b497599afe52386366fc42`
- `8b2d9a238d5bea00bb182cc5378d1c2bd8b7a1a0`

**Status: awaiting Lean compilation.** These commits are source-level proof proposals; their axioms and successful checking must not be reported without an exact pinned CI receipt. `bubbleCandidateSorted = true` remains open.

### Precise remaining inductive step

On the direct fold, prove the invariant after processing boundaries `0, …, j-1` within a single pass:

1. The current entry at position `j` is a maximum (under `elevenSlotLexLE`) of the first `j+1` pre-pass entries.
2. The processed entries to its left form a permutation of the other visited entries.
3. When the step compares entries at `j` and `j+1`, totality places their maximum at `j+1`; the retained slot identities remain distinct by the already available permutation lemma.

At the end of a pass the maximum occupies index 10. For the next pass, prove a stronger boundary claim: a sorted fixed suffix is not modified by comparisons that reach it, because the largest remaining prefix item cannot exceed the first fixed suffix item. Iterating this makes the fixed sorted suffix grow by one per pass. Ten passes suffice for eleven positions, and the extra eleventh is idempotent on a sorted list. Crucially, prove this on the **actual schedule** using the recorded/direct fold bridge; no standalone alternative sorter can silently replace the candidate.

Use only finite, concrete `getElem?` index safety lemmas for sublists of length 11. Retain the color-rank/index total order, not an order on colors alone. All statements hold for arbitrary `colorAt : Nat → Nat`, so histogram enumeration is unnecessary.

## Independent counterexample gate

Check the invariants on worst-case reverse-ordered colors, all-equal colors (where *original index* is the tie-breaker), and alternating color ranks. These are debugging witnesses only, never substitutes for BE3–BE5. Verify that `Fin 10` excludes slot 11 throughout and that signed parity remains the frozen combined position-plus-gauge correction.

## Separate global-physical barrier

Closing BE5 would prove **normalizer totality**, not full nineteen-frame physical identification. The latter still needs statewise validity of every feasible branch in all 52 frozen signed sectors, plus terminal corner sign derived solely from actual corner observations by frame 19. Neither a sorted output nor a finite Python replay establishes those semantic obligations.

## Evidence discipline

No extra Python auditor; no archive deletion without an exact-byte Drive receipt and manifest SHA comparison; no `github-actions[bot]` writes. Maintain `research/current` and preserve `main`. Classify each claim as proposed, Lean-compiled, or full-pipeline verified; update the paper/README only after the corresponding stronger gate.

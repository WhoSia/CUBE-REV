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

## BG result — universal normalizer totality (Lean-compiled in pinned CI)

**Scope.** For *every* `colorAt : Nat → Nat` (repeated colors included; ties broken by original slot index) the executable eleven-pass schedule accepts its own check: `bubbleCandidateSorted colorAt = true`. This is algorithmic totality of the deterministic normalizer plus unconditional refinement to the frozen stable order. It is **not** statewise validity of the 52 signed sectors, terminal corner sign, or the physical Fits 19 theorem; those remain open.

**Theorems** (`formal/029/EdgeSorting.lean`): `bubble_range_fold_eq_carry` (index sweep = structural carry pass, the loop-to-recursion bridge), `bubble_carry_max`, `bubble_carry_of_pairwise`, `bubble_carry_append_suffix`, `bubble_iter_invariant` (sorted dominating suffix grows by one per pass), `bubble_iter_sorted`, `bubble_candidate_direct_fold_sorted`, then `bubble_candidate_sorted_total`, `verified_bubble_trace_total` (`verifiedBubbleTrace? colorAt = some (bubbleCandidatePath11 colorAt)`) and `bubble_candidate_normalizes`. The proof is generic in an abstract comparator (`BubbleOrder`: refl/trans/total/antisymm) instantiated at `elevenSlotLexLE colorAt`; no finite enumeration of `colorAt` and no standalone replacement sorter: the bridge is the existing `bubble_candidate_replay_eq_direct_fold`.

**Evidence.**
- `d18f0d2c241503ac3c78d9a5e5feb7f6be2d9cce`: first BG push. CI run `45181505429` failed in `lake build` EdgeSorting for exactly three reasons, all Mathlib-only tactics in a Mathlib-free package: `split_ifs` in the BF declarations `bubble_path_step_replay` and `bubble_order_step_perm` (so those BF declarations had **not** compiled at `52d26dd`), and `tauto` in the new BG code.
- `66016acb976a2006dd6e484cbe84731de73b5b78`: those three tactics replaced with core `split` / `simp_all` / explicit `Or` injections. CI run `45181851995`: `Build completed successfully (123 jobs)`, no `sorryAx`. Axioms printed in that log: `bubble_path_step_replay`, `bubble_fold_replay`, `bubble_order_step_perm`, `bubble_direct_fold_perm` depend on `[propext]`; `bubble_candidate_sorted_total`, `verified_bubble_trace_total`, `bubble_candidate_normalizes` and `bubble_candidate_direct_fold_sorted` on `[propext, Classical.choice, Quot.sound]`. The `Inspect new theorem dependencies` step of that run was cancelled by a newer push (workflow concurrency), so the full pipeline did not complete for that SHA.
- `5be06871086b9732136d41dd047e46b6b7d6f7fb` (later HEAD containing the above): EdgeSorting builds and prints the same axioms, but run `45182751089` fails in the unrelated BH module `CornerTranscriptBit.lean` (`failed to synthesize Decidable (∃ s, Reachable s ∧ scheduledCornerColors s = replies)`, plus a `sorry`). Full-pipeline success is therefore **not** established at any SHA yet.

**Claim level.** Lean-compiled in pinned CI for the EdgeSorting library with audited standard axioms (propext, Classical.choice, Quot.sound); not yet full-pipeline verified. Not run locally: the authoring sandbox cannot reach the Lean release host.

**Remaining.** (1) Obtain a green full pipeline on a SHA containing BG (blocked on BH `CornerTranscriptBit`). (2) `if_pos`/`if_neg` deprecation warnings in the new code (non-fatal). (3) Next mathematical question: statewise validity of every feasible branch in the 52 frozen signed sectors, and terminal corner sign from actual corner observations by frame 19.

## BJ–BL review: compile repair and claim audit (Claude, independent review)

**First full-pipeline success containing BG and BJ–BL: `566b6abd9240df891acd1df9988d2b230a0cf5c0`**, CI run `45190959094`: `Build completed successfully (133 jobs)`, all later steps green. Axioms printed for every BJ–BL theorem and for `bubble_candidate_sorted_total`: `[propext, Classical.choice, Quot.sound]`, no `sorryAx`. Level A for the *statements below*, not for the physical Fits 19 theorem.

What the CI logs actually showed (the BL note "no compile log secured" understates this; logs are readable via the jobs API):
- `ab4c32d` (run `45189039619`): `CornerPermutationSign.lean:51` failed (`rw` before unfolding `cornerPermutationOdd`). Lake therefore never built `CornerSignedCorrection` or `ObservedTerminalParity`: BK and BL had not been compiled at all. Fixed in `fda1e9b`.
- `fda1e9b` (run `45190759362`): `ObservedTerminalParity.lean:22-23` used an unqualified `parity`. With `autoImplicit` on, Lean silently turned it into a fresh implicit variable and elaborated the statement of `observed_terminal_parity_uses_three_pair_character` with `sorry`. Fixed in `566b6ab` (`Eighteen.parity`). This is a hazard for every future module: a misspelled or out-of-scope name becomes a variable, not an error, so a theorem can *look* proved while stating the wrong thing. Recommend `set_option autoImplicit false` in new files.

What BL does and does not establish:
- Established: for reachable `s, t` with corner coordinates `a, b`, equal first-eleven EDGE replies and equal nineteen corner replies imply equal `correctedCornerParity ... (frozenPrefixSignCorrection ...)`. This is an information-flow/factorization statement about a *defined* quantity.
- Not established: that this quantity equals the sign the frozen decoder consumes, `edgeWordSign` of the representative word. No theorem connects the two, so the sign convention (orientation of the correction, pose and `paint` order conventions) is untested. The BL interface is decorative until that identity is proved or at least checked on concrete reachable states.
- The per-turn fact `edge_corner_turn_sign_agree` (CornerTurnGenerators) already exists; what is missing is an edge-coordinate analogue of `CornerCoordinates` / `coordinatesAlong` / `CornersAgree` for reachable colorings, an induction giving `parity(edge pieces) = parity(corner pieces)` along every turn word, and the link from the sorted/gauged representative word to the physical edge permutation.

Attribution note: the BH–BL commits by the other agent carry author and committer name `OOZ OON" Kim` (email maps to the WhoSia account, no bot, no trailer), not the name `WhoSia` required by the protocol. Published history is not rewritten; later commits should set `user.name=WhoSia`.

# CUBE-REV 43 / BI — Nineteen-Reply Corner Coordinate Identifiability

Date: 2026-11-23. Track: GPT-6 independent causal corner-sign formalization, with Claude controlling `EdgeSorting.lean`.

## Source and claim scope

New module `formal/029/CornerSignUniqueness.lean` provides source-level statements:

1. `same_nineteen_replies_force_corner_coordinates`: If two physically reachable `Coloring`s have equal nineteen actual scheduled corner replies, and two `CornerCoordinates` records agree with those colorings, then the coordinate records are equal. Proof uses `same_nineteen_corner_answers_force_all_corner_colors`, `cornerCyclicPair_colors`, and `cornerCyclicPair_injective`.
2. `same_nineteen_replies_force_corner_statistic`: Every user-provided function on those complete coordinates is then equal on two reachable states sharing the nineteen responses. The theorem **does not define** a particular physical edge sign.
3. `same_nineteen_replies_force_corner_piece_order`: The ordered piece lists are identical, a stronger property than merely having equal piece multisets.

This is a necessary bridge to a corner-derived permutation parity, not a constructor of a computable terminal decoder. The separate `CornerTranscriptBit.lean` factorization is **noncomputable** and must never be described as a deployable readout.

## CI and source provenance

- Module source commit: `72fe519c92a393ee49d029cf830a6a8e3b7a07da`.
- Lake target registration: `d61c5a85cec8d8c69201ee82e2e774e57c4b85d0`.
- Read-only Lean workflow inspection addition: `e07064a59a5b965b30178701a313440c7cc2dec0`.
- Prior BH source fix: `bf11e21c169a347f3d1b5e2d4bdd37f20c69759c`.
- **No passing pinned Lean run of the new BI source is yet inspected**. The newly added theorems are source-authored only until actual success and `#print axioms` audit.

Claude supplied independent evidence that the BG `EdgeSorting` universal normalization totality compiles on pinned Lean 4.34.1 in the earlier build stage of run `45181851995`; the overall run was cancelled before end-to-end verification. Claude's historical reference to BH's missing `Decidable` instance predates the targeted source fix above. Both claims must retain their exact revision boundaries.

## BI decision ledger, LIRA / JEV

E=0.30 directness+0.20 independence+0.20 reproducibility+0.20 falsification power+0.10 scope match. E/C/G/L remain distinct and are NOT calibrated probabilities.

| Candidate | E | C | G | L | Gate |
| --- | ---: | ---: | ---: | ---: | --- |
| Corner-coordinate uniqueness using actual nineteen reads | .680 | .740 | .550 | .880 | HOLD, Lean BI build uninspected |
| Corner-piece permutation sign derived from complete corner coordinates | .620 | .580 | .430 | .925 | OPEN, explicit sign operator/physical conservation bridge |
| Required frozen decoder sign computable from full paired transcript and past-selected cocycle | .480 | .340 | .230 | .950 | OPEN, must prove actual causal readout |
| Universal normalized root selection and original belief membership | .455 | .300 | .180 | .940 | OPEN, no unsupported direct-root fallback allowed |
| Global unconditional physical `Fits 19` | .300 | .080 | .040 | .930 | HOLD until all non-compensatory gates satisfied |

The priority differences among the last three are within score uncertainty: treat them as a tied P0 research cluster. High L is a development priority, never proof acceptance.

## Next executable research obligations

A. Construct an explicit `Fin 8` permutation from `cornerPieceList` for reachable states, with a total parity function whose value is invariant under the identical-coordinate theorem above.

B. Show how the physically legal relation between corner and edge permutation signs, coupled to the frozen correction `position parity XOR gauge parity`, defines the terminal bit **from observations already received**, not hidden-state access.

C. Give a computable candidate recovery from the fourteen distinct observed corner colors plus the two conservation constraints; prove it returns the correct original coordinates for all reachable cubes and only after the nineteenth charged frame.

D. Prove all-history normalization/sector selection on original ordered first-eleven replies, and membership of the transformed original state in the selected parsed belief. Do not interpret `matchingFrozenRoot = none` as a successful path.

E. Only then compose a single complete policy and use the already-established physical observation compiler.

All commits must be human `WhoSia` author and committer. No bot commits, new branch explosion, force push, or automatic `main` migration.

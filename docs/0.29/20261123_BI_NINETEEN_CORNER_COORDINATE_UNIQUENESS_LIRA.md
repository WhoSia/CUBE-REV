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

## BJ concrete parity implementation — source acceptance pending

The independent file `formal/029/CornerPermutationSign.lean` (commit `021589c717a17f3687d47445c0205884ca713b99`) now **defines** the required intermediate algebraic quantity, rather than leaving “corner permutation sign” as an unspecified statistic:

```lean
def cornerPermutationParity (a : CornerCoordinates) : Nat :=
  CubeRev029.Eighteen.parity ((cornerPieceList a).map Fin.val)

def cornerPermutationOdd (a : CornerCoordinates) : Bool :=
  cornerPermutationParity a == 1
```

It proposes three unconditional mathematical implications under their **explicit physical reachability and coordinate-agreement premises**:

- `corner_permutation_parity_witness_independent`: two coordinate witnesses of the same reachable original coloring produce equal parity.
- `corner_permutation_parity_from_nineteen_replies`: equal actual 19-read corner observations of reachable states imply equality of this concrete corner permutation parity.
- `corner_permutation_odd_from_nineteen_replies`: the same for a Boolean oddness indicator.

The proof directly invokes BI's **ordered-coordinate** uniqueness, not just an equality of unordered corner piece multisets, and uses the existing inversion-count parity from `EighteenReadData.lean`. The result must **not** be conflated with the signed frozen leaf's required `edgeWordSign`, which depends on edge/corner legal parity coupling and the selected position+gauge cocycle. In addition, unique identifiability does not itself implement an effective decoder from nineteen replies.

Build registration `57ba52e81ade39921bb8b481d0a3c272fc8385f0`; read-only pinned CI registration `25fdb4a9151718c26d7a80eea2e2f42bf9fc0447`.

**Strict verification gate:** all new BJ declarations remain source proposals until their exact CI run succeeds, the printed `#print axioms` output is reviewed, and current BF/BG/BH/BI modules build together. No new full-pipeline-success claim is made.

### LIRA BJ update (analyst judgments, not calibrated probabilities)

| Objective | E | C | G | L | Next falsifying check |
| --- | ---: | ---: | ---: | ---: | --- |
| Concrete corner parity formula and observational fiber invariance | .700 | .710 | .630 | .920 | Exact BJ Lean compilation and same-fiber proof |
| Observable, executable parity decoding from 19 paid replies | .420 | .260 | .200 | .950 | Construct total certified decoder, no Classical.choice |
| Correct frozen-sector sign after position/gauge correction | .460 | .310 | .230 | .970 | Produce end-to-end legal-state parity-coupling theorem |
| All-original-histories root selection and belief membership | .455 | .300 | .180 | .955 | Actual normalized selector totality proof |
| Full physical `Fits 19` | .300 | .080 | .040 | .940 | Formal end-to-end policy and successful pinned CI |

The numerical differences between the last three L scores are below plausible methodological uncertainty; treat them as a tied P0. Scores do not override compiler or causal-observation proof gates.

## BK: Past-dependent correction retained rather than imagined as a corner observation

A separate `formal/029/CornerSignedCorrection.lean` now introduces `correctedCornerParity a prefixCorrection := (cornerPermutationParity a + prefixCorrection) % 2` and the two explicit-hypothesis equalities `corrected_corner_parity_from_past_and_nineteen_replies` and `corrected_corner_parity_respects_equal_prefix_corrections`. Neither theorem treats the past-dependent correction as a free sensor; the first holds for **the same correction** and the second requires equality of corrections derived elsewhere from equal actual prefixes.

**Source commits:** `f8f4f01c1526eecfe5a08f2d2c015e61da01fafd` (module), `f1f2f8d07554ca3b12a839a8ff9dd4e38de2cab2` (Lake), `30ae11c96774c17e9dab837f758f28ecceb38a78` (read-only CI). **Compilation remains unverified** until the new exact-HEAD workflow run is inspected.

For the future specialization, the production helper `PrefixColorGauge.frozenPrefixSignCorrection` already defines the genuine combined position-sort and color-gauge parity. The BK module deliberately accepts a `Nat` correction rather than claiming the actual first-eleven `FrameColor` prefix was carried into the frozen terminal decoder. The missing composition theorem must instantiate `prefixCorrection := frozenPrefixSignCorrection actualFirstElevenPairedReplies`, prove the equality needed by the root's signed decoder, and show only past responses are consulted. Also prove physical edge/corner permutation parity coupling for all reachable original cubes.

**LIRA noncompensatory gate:** even an accepted BK equality cannot upgrade the global signed-sector transport or `Fits 19`. Current assessment for the **fully integrated required leaf sign** remains C=.31, G=.23, L=.97 (analyst judgment; not a posterior probability). The immediate work order is inspect CI, fix errors, then prove the actual prefix-to-BK specialization with a typed runnable transcript decoder.

## BL: Exact production-prefix cocycle meets nineteen-frame corner parity

**New source:** `formal/029/ObservedTerminalParity.lean`, committed in `9a2b2c3c0084eb4594942247e1493b77b373a62e`, registered with Lake at `5b35d5f7a04e2e3bde2e5bf94edb9299387f63c6` and with read-only CI at `ef12b03cf9b5449fdabfa55f9589517e7a0c0d33`. A further source change `ab4c32d4118958ff9468bd81e0ba00ec58612c0c` strengthens the interface to be independent of the first-eleven corner replies.

BL defines `observedTerminalCorrectedParity firstElevenReplies corners`, which is **exactly** `correctedCornerParity corners (frozenPrefixSignCorrection firstElevenReplies)`, using the production `PrefixColorGauge.frozenPrefixSignCorrection` rather than an independently chosen representative or guessed color-gauge rule.

BL declares four mathematical implications:

1. `observed_terminal_parity_uses_three_pair_character`: the corrected parity uses the existing proved three-opposite-pair symmetry character, not the earlier label-only parity approximation.
2. `observed_terminal_corrected_parity_fiber_constant`: equality of complete first-eleven paired replies plus equality of nineteen actual corner observations suffices for equality of the corrected parity.
3. `frozen_prefix_sign_correction_ignores_corner_replies`: the actual frozen prefix correction is a function only of the **first-eleven edge colors**, using the already established gauge independence and a congruence of stable-sort orders.
4. `observed_terminal_parity_from_edge_and_corner_histories`: a strictly stronger causal statement: equality of *just* eleven first edge colors **and** nineteen real corner colors suffices to equalize the corrected terminal parity on corresponding reachable corner coordinates.

This resolves a structural *information-flow independence* obligation: the terminal correction has a known deterministic dependency on past paid edge colors and completed corner colors. It **does not** prove that the frozen decoder's `edgeWordSign` equals this corrected quantity, because the actual legal-state edge/corner parity coupling and all-state representative transport have not been composed. The corner coordinate agreement premises remain explicit, although existing `reachable_has_permutation_corners` supplies witnesses for reachable states.

**Compilation status:** the BL Lean declarations are *submitted for pinned CI*, not yet accepted or axiom-audited on this exact revision. Inspect the exact log before promoting the claim. A previously compiled BG normalizer does not automatically certify these new modules.

### BL LIRA reassessment (judgment values, not empirical probabilities)

| Proposition / action | E | C | G | L | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| Exact actual-prefix cocycle integration as a source theorem | .680 | .740 | .580 | .860 | HOLD for pinned Lean build |
| Edge-only prefix / corner-only completion dependency | .710 | .770 | .630 | .900 | HOLD for pinned Lean build |
| Equality with frozen leaf's required sign for all legal states | .460 | .330 | .240 | .970 | P0, not established |
| Normalized 52-sector root totality / belief membership | .455 | .300 | .180 | .950 | P0, not established |
| Single physical `Fits 19` | .300 | .080 | .040 | .940 | HOLD: hard proof gates |

**Uncertainty rule:** L differences within 0.05 are treated as a tie; no numeric score overrides absent compilation, decoder implementability, or exact all-state premises.

### Potential falsifiers and acceptance tests

- Test normalized histories with equal edge responses and different corner replies; the BL correction must remain identical. Otherwise the prefix gauge illicitly uses corner data.
- Test two legal states with matching 19 corner replies but different first-eleven edge replies; their **raw physical corner parity** must be equal, but their *corrected* parity may differ. Do not erase the past-gauge distinction.
- Test repeated edge colors and tied color-gauge histograms: `frozenPrefixSignCorrection` must retain the exact strict-improvement fold and URFDLB color collation.
- Test an early frozen-tree leaf: sign can be used only after the final corner observation; padding must still constitute actual charged reads.
- Confirm no theorem assumes that a merely matched 52-root JSON entry contains every physical-state normalized representative.

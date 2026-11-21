# CUBE-REV 0.29 — Adaptive lower bound and pinned data checks

The main contribution is the impossibility of identifying a fixed-center Rubik's Cube in at most eighteen paired observations. The physical Lean theorem gives a collision even when both starting cubes have the same solved corners. The nineteen-frame construction has a checked finite policy and a separately verified physical routing lemma.

| Component | Verified scope |
| --- | --- |
| `AdaptiveLowerBound.lean` | Finite-budget decision policies, transcript collision against a ranked residual certificate, preservation of budget under known responses and address pullback, and specialization to disclosed corners. |
| `EighteenReadData.lean` | Boolean legality checks, child reconstruction and witness lift over all 43,870 arcs, and the proofs for the flip bit and rank-insertion inversion parity. |
| `NineteenReadData.lean` | Reconstruct the first-color orbit support, enumerate feasible representative edge assignments, check every reply in the frozen trees and each terminal sign class. |
| `*DataReceipt.lean` | Prove equality to the expected finite receipts using Lean's native computation. Each prints its generated native-evaluation trust dependency. |

The finite graph now constructs the semantic certificate directly. The two local lift lemmas prove admissibility and observation preservation for **every** admissible child word, including the observed response and injectivity. The parser reconstructs the graph from the original input, and the validator checks the local theorem premises at every address. The actual roots now instantiate the generic policy theorem.

| Component | Verified scope |
| --- | --- |
| `ResidualWord.lean`, `ResidualLift.lean` | Universal insertion, reordering, color, parity and orientation laws for both kinds of read. |
| `SemanticGraph.lean`, `SemanticInput.lean` | Turn the finite validated graph into a semantic adversarial certificate. Return a known color directly, and use a universal lift for every fresh query. |
| `RootCoordinates.lean` | At either root, the assignments have twelve valid oriented edges. The 24 real edge addresses separate distinct assignments. |
| `EighteenCertified.lean` | For either corner parity and every policy with budget 18, distinct 24-facelet edge assignments produce the same paired transcript when the corner colors are a known function. |

| Component | Verified scope |
| --- | --- |
| `FaceTurns.lean`, `EdgeSorting.lean` | Geometric quarter-turn permutations on the 48 non-center stickers and factorization of every even edge permutation into an even number of adjacent swaps. |
| `EdgeOperations.lean`, `EdgeFlips.lean`, `SolvedCornerReachable.lean` | Endpoint checks for 121 ordered pairs of adjacent swaps and 144 ordered pairs of flips. These yield legal turn words for every even-sector edge assignment with all corner stickers fixed. |
| `PhysicalObservation.lean`, `PhysicalEighteen.lean` | Adaptive composition of relative turns and a physical collision for any fixed edge and corner probe pair under every policy with budget at most 18. |
| `JointProbeRouting.lean` | All 576 paired target addresses have legal routing words from a base probe pair. Composition and inverses extend the result to arbitrary fixed probes and prior poses. |
| `NineteenSector.lean` | Every compatible oriented assignment is in the candidate list used at the start of the continuation. The proof applies to any first-color list with exactly one unread edge and to either flip bit. |

The physical lower bound uses native evaluation for the pinned graph and the endpoint table. The universal transition, policy, and realization lemmas are proved in Lean. The 19-frame result still needs a universal proof linking the checked representative policy and the corner decoder to one geometric observation policy. The 21-frame non-adaptive optimum is outside these Lean theorems.

## Run

Use the pinned Lean 4.34.1 toolchain and Python 3.

```sh
lake build
python3 check_data.py ../../data/0.29/EIGHTEEN_QUERY_DAG.json.gz /path/to/upper-policy-certificate.json
```

Use the upper-policy JSON from the [S editable bundle](https://drive.google.com/file/d/1g5NCo2vqcjaiHGaSUEiL_OZoy3naY4SV/view). These are the checked input digests:

- Eighteen raw JSON: `dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce`.
- Nineteen JSON: `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`.

`check_data.py` verifies the input bytes, prepares ignored local copies for `include_str`, and builds the physical lower bound against the pinned data. It verifies malformed-data controls separately, including two corruptions of an arc that preserve the stored node witnesses.

## Y — clean-build certificates and exact nineteen-frame corner schedule

A **clean GitHub checkout** does not already have the two JSON inputs used by
`include_str` in `EighteenCertified.lean` and `NineteenDataReceipt.lean`.
Do not run `lake build` against an absent or an arbitrary substituted JSON.
The authoritative compressed blobs and strict restorer are now committed:

```sh
python3 restore_pinned_data.py
python3 validate_19_corner_schedule.py
lake build
```

`restore_pinned_data.py` checks the pinned SHA-256 of both the deterministic
compressed bytes and their original JSON, and fails rather than overwriting
a conflicting existing proof input. It needs only the Python standard library.
`NineteenSchedule.lean` states that the physical 19-frame X schedule reads
**14 distinct cyclic corner stickers** on seven positions, leaving position 5
unread, with the final new color arriving on frame 19. The new
`corner_fourteen_unique_missing_five` conditional uniqueness theorem matches
that precise schedule, unlike the earlier convenient omitted-position-7 case.
The cross-language script rejects schedule drift and three corruptions.

**Trust boundary:** these input and preflight checks were actually run in a
clean Python environment. The *new* Lean sources require a successful pinned
4.34.1 `lake build` and full axiom inspection before they can be called
kernel-verified. The universal upper-bound policy has not yet been constructed
as one verified Lean theorem; see `../../docs/0.29/20261121_Y_LEAN_PROOF_GATES.md`
for the remaining obligations.

## Z — physical corner-coordinate extraction and the remaining conservation theorem

Z adds two source-level Lean modules that connect the **same geometric `turnSlot`**
used in the physical eighteen-frame lower bound to the nineteen-frame corner
decoder, without introducing an unverified cubie move table:

- `CornerTurnGenerators.lean` defines the corner-source permutation and cyclic
  twist offset for each of the twelve quarter turns and states five finite
  properties (source range, injectivity, cyclic triples, zero total twist
  offset, equal edge/corner parity increments).
- `ReachableCornerCoordinates.lean` defines `CornersAgree`, a coordinate action
  on all oriented cubies, and a structural turn-word induction yielding
  `reachable_has_oriented_corners`: each geometrically reachable 48-sticker
  state admits oriented corner coordinates reproducing every physical corner
  sticker color.

The following is executable **without Lean**, using only the pinned Python
standard library and the existing geometric helper source:

```sh
python3 formal/029/restore_pinned_data.py
python3 formal/029/validate_19_corner_schedule.py
python3 formal/029/audit_corner_turn_generators.py
python3 formal/029/audit_reachable_corner_bridge.py
python3 formal/029/audit_lake_manifest.py
```

The independent audit checked every `12 × 3^8 = 78,732` generator/twist-vector
combination, 2,304 local oriented corner actions, and 2,225,232 physical
corner-sticker comparisons over reproducible legal turn histories, including
negative controls. The full package contains 29 required Lake default targets,
**including the physical eighteen-frame lower-bound theorem** and both input
receipt modules, and 35 checked internal imports.

**Crucial open theorem:** the produced corner coordinates for every reachable
state must have distinct piece labels and total twist zero (and satisfy the
proper permutation sign relation). For each generator, the finite facts already
express a source permutation `σ` and offsets `δ` with total `δ ≡ 0 (mod 3)`.
The missing Lean argument must prove that these properties preserve the piece
permutation and twist sum under arbitrary composition, then discharge the
`LegalCornerCoordinates` premise of `corner_fourteen_unique_missing_five`.
Only after that can the frozen 52-sector trees and arbitrary-order first-color
transport be assembled into one universal nineteen-read policy theorem.

**Compilation status:** the Z execution environment lacked `lean` and `lake`.
The new source files, their `decide +kernel` proof scripts, and printed axiom
commands are **not** proof of a successful kernel compilation. Obtain a real
Lean 4.34.1 build log and axiom report before changing the paper's formal
verification claim. The complete clean-room Z archive and its digest are
preserved in [Drive](https://drive.google.com/file/d/1c5yPtOxSB4zpYnXQObqkiFQq2Tgkq7Pj/view);
see [the Z formal closure ledger](../../docs/0.29/20261121_Z_CORNER_BRIDGE_AND_FORMAL_GATES.md).

## 2026-11-21 AA–AB — corner conservation and scheduled-transcript bridge

The historical Z section above records its *then-open* proof obligations. They
must not be mistaken for the current status. The following later source modules
are now in the mandatory Lake target list:

- `CornerConservation.lean` proves piece-label sum and twist-sum preservation
  for each basic geometric turn and, by induction, for arbitrary turn words.
- `ReachableCornerIdentification.lean` proves the actual missing-position-5
  **fourteen-color** uniqueness result for two `Reachable` cube states.
- `CornerPermutation.lean` proves that reachable corners contain each of the
  eight source cubie identities exactly once; this is stronger than the
  numerical piece-label sum invariant.
- `NineteenCornerTranscript.lean` proves a new *conditional bridge*: if two
  reachable initial cubes give the same colors at the **actual nineteen
  scheduled corner addresses**, then all their 24 corner sticker colors agree.
  It accounts for the five repeated reads and final frame-19 new color.

The last implication is a genuine proof obligation in the nineteen-frame
upper-bound program, but it **does not by itself** exhibit or certify the
19-frame adaptive edge policy. A complete upper-bound theorem still needs:

1. a verified, executable Lean decision policy or a sound semantic
   certificate interpreter for all 52 frozen representative trees;
2. a *universal* reindexing/renaming theorem transporting each arbitrary
   eleven-edge prefix to the appropriate representative, preserving
   feasibility, orientation and permutation sign;
3. a proof that each frame chooses both original-coordinate addresses
   **before observing that frame's pair of colors**, and that the combined
   terminal edge sign and actual nineteen-corner transcript determine the
   unique initial legal coloring;
4. an unconditional `Fits 19` witness and proof of
   `∀ s, Reachable s → tree.run (abstractPairRead s) = s`, which can then be
   passed to `physical_nineteen_of_abstract_bounded`.

**Verification boundary:** a Lean source file and a static manifest check
are not a successful kernel compile. The AB module has been committed and
registered in the pinned Lake/CI builds, but no new successful AB job and
axiom inspection are established in this note. Even a successful build of
all current modules does not prove the as-yet-unconstructed *universal
nineteen-frame policy theorem*. Keep this distinction explicit in papers.

The historic eighteen-frame physical lower theorem remains the first
contribution. Keep the T-version claim order, the U-version physical lower
proof, and the independently corrected W-version worked example separate
until the complete upper-bound composition is checked.

## 2026-11-21 AC–AE — pinned successful compilation and exact remaining bridge

The older Z and AB notes above describe their historical verification state.
Current evidence supersedes their *pending build* status:

- **AB correction:** `NineteenCornerTranscript.lean` initially failed
  in a purely syntactic/numeric normalization of `24 + (3*i+1)` versus
  `(24+3*i)+1`. Commit `52d14805786782d1a4941066d1449b52c1def55b`
  added `Nat.add_assoc`. The ensuing module and its kernel axiom printouts
  passed in the pinned CI.
- **AC:** `ObservationTransport.lean` proves a generic adaptive policy
  transport under response equivariance, representative correctness and
  round-trip inversion, preserving the worst-case query budget. Both its
  main theorem and fixed-reply congruence theorem report **no axioms**.
  No cube-specific universal 52-representative witness is supplied by this
  theorem.
- **AD:** `ElevenPrefix.lean` records the actual first eleven simultaneous
  original-coordinate edge/corner addresses, proves ordered-history
  semantics for a continuation chosen after the prefix, and proves
  `11 + 8 = 19` at the `Fits` predicate level for an eight-frame
  continuation valid on every possible reply vector.
- **AE:** `NineteenSymmetry.lean` defines the map induced by all 48
  opposite-color-preserving center relabelings on twelve edge types
  and 24 oriented edge identities. Three **kernel-computed** finite theorems
  establish in-range bijection on the twelve types, even total flip offset
  and equivariance of both sticker-color responses. All three
  have `#print axioms` dependencies limited to standard Lean axioms
  `propext`, `Classical.choice`, `Quot.sound`; none contains
  `sorryAx` or `native_decide.ax`.

**Complete pinned CI run:** [#44888672661](https://github.com/WhoSia/CUBE-REV/actions/runs/44888672661),
**SUCCESS**, including 4 preflight audits, Lake compilation, the pinned
certificate replay with mutation controls, and individual Lean/axiom checks.
Build steps are read-only: no GitHub Actions bot commits or authorship.

The **still-open main result** is an unconditional `Fits 19` policy whose
behavior on *every* reachable cube equals the initial state. The 52 frozen
representatives need complete formal policy reification, every ordered
eleven-color prefix needs a proven invertible canonical transport, parity
correction needs to be connected to the terminal corner observations, and
the entire construction must be combined with
`physical_nineteen_of_abstract_bounded`. None of the AC–AE lemmas alone
supplies these missing cube-specific witnesses.

**Important trust distinction:** the earlier eighteen-read lower-bound
certificate uses `native_decide` and displays corresponding native-decision
axiom dependencies. The new transport theorem is axiom-free; the AE finite
symmetry results use only kernel computation with standard logical axioms.
Do not collapse these into a single unsupported phrase such as
"fully kernel verified."

## 2026-11-21 AK–AQ: graph quotient, sign cocycle and corrected exact CI

- **Hall matching support:** the 12 edge cubie types form `K_{2,2,2}`. Four structurally proved irredundant Hall-cut families characterize feasible eleven-color histograms. The standalone independent 64-cut/omitted-edge DP comparisons agree on all 4,368 nonnegative six-color histograms summing to eleven, accepting 1,362.
- **Group quotient:** `Aut(K_{2,2,2}) ≅ (C₂)^3 ⋊ S₃` has 48 elements and ten signed-cycle types, with Burnside fixed-point sum 2,496 and 52 unsigned histogram orbits. This explains the frozen certificate's 52 representative histograms but does not formally prove every policy branch.
- **Formal `ColorGraphCharacter.lean`:** `induced_edge_sign_is_three_pair_sign` validates the induced 12-edge permutation sign using the three opposite-color pairs (finite 48-element `decide +kernel`); five color generators reach the full group by Cayley distance six. Its printed axioms are only `propext`, `Classical.choice`, `Quot.sound` where needed.
- **Formal `GraphPosteriorCovariance.lean`:** exact state-set/potential-reply posterior fiber transport, ambiguity witness transport, and lower adversary transport. This is a general theorem **conditional** on explicit state embedding, query surjectivity and reply injectivity, not an instantiated proof for every physical Rubik sensor position. Printed axioms are `propext` and `Quot.sound` at most; the ambiguity witness theorem reports no axioms.
- **AJ fix:** the source's `Fin 12 ≃ Fin 12` notation was unavailable in the pinned core package, and `Equiv` itself was not imported. Replaced both with an *explicit invertible* `EdgeSlotOrder` record with forward/backward functions and mutual inverse proofs. `representative_pair_state_round_trip` and `correct_original_policy_of_certified_representative` now compile. Their trust dependencies are only the standard Lean logical axioms; the second theorem still assumes the correctness of a representative policy.
- **Full parity correction:** the frozen `route_info` uses both `sign(label relabeling)` and `sign(stable first-eleven sort)`. Its group-action cocycle is checked on **326,880** histogram/group/generator compositions. There are **24** representative orbits with an odd total correction in their stabilizer (426 labeled histograms). The corresponding *formal signed-histogram* quotient has **80** orbits; the preliminary 94 orbits from a label-only action belong to a different simplified model and must not be substituted into the physical controller proof. A legal edge-array witness confirms that using the wrong normalization gauge changes the recovered sign.
- **Full verified workflow:** [#44898175828](https://github.com/WhoSia/CUBE-REV/actions/runs/44898175828) **SUCCESS**. It runs static package gates, independent Hall/Burnside/cocycle receipts and negative controls, compiles all mandatory Lean targets, replays both frozen data certificates and mutation controls, and separately prints theorem axioms. Workflow is read-only; no GitHub Actions bot commit.

**Unclosed full upper theorem:** canonicalize *every ordered* eleven-color reply using a retained map and slot-order witness; prove stable-sort sign correction in generic Lean permutation algebra; reify 52 representative eight-read decision trees including all feasible replies and terminal corner parity; and instantiate `physical_nineteen_of_abstract_bounded` with an unconditional `Fits 19` policy recovering every reachable initial cube.

**Custody:** the source-current [GitHub proof-debt and referee review](../../docs/0.29/20261121_AQ4_ADVERSARIAL_REFEREE_ACCEPTANCE_MATRIX.md), [Drive-owned mathematical books / missing-edition ledger](../../docs/0.29/20261121_AM1_DRIVE_SOURCES_MISSING_EDITION_LEDGER.md), and [Notion CUBE-REV 42](https://app.notion.com/p/41fef561cf92819abc3cf36da389d5e9) preserve the exact distinction between current proofs, executable certificates and still-open claims.

## 2026-11-21 AS: all candidate-sector semantics, finite quantifier reduction and exact 8-read parity release

**Pinned proof gate:** [GitHub Actions #44903796513 — FULL SUCCESS](https://github.com/WhoSia/CUBE-REV/actions/runs/44903796513), containing all **54 mandatory Lean libraries**. The report replays the independent lower/upper data checkers and prints each new theorem's actual axiom dependencies. It does **not** establish an unconditional nineteen-frame upper policy.

New package modules and exactly verified scope:

| New theorem source | Strongest proved implication | `#print axioms` and boundary |
| --- | --- | --- |
| `SignedSectorLeaf.lean` | AtMostOnePerSign for a finite sector ⇒ the correct-sign decoder returns exactly each candidate and never invents one | `propext`; sign itself is an external **terminal** argument |
| `SectorSemanticCompiler.lean` | Correct reply-fiber filtering, fail-closed typed graph with `Fits budget`; `SemanticallyValidSector` ⇒ each feasible original candidate is recovered by the returned sign-indexed decoder | Main theorem `propext, Quot.sound`; actual 52 roots not yet instantiated |
| `FrozenJsonSectorParser.lean` | `leaf/read/repeat` JSON grammar converts to typed instructions; malformed nodes rejected, missing replies map to an invalid node, valid typed graph always has bounded policy | Standard `propext, Classical.choice, Quot.sound`; parser correctness does not imply graph's semantic success |
| `SectorStatewiseValidity.lean` | **For every finite belief and all budgets**, `SemanticallyValidSector ↔ StatewiseSectorValid`, replacing all-reply quantifiers by the replies that surviving candidate states can actually generate | `propext, Quot.sound`; no `native_decide.ax` |
| `ExactBudgetPadding.lean` | Completing early leaf termination to exactly `n` real reads preserves original output, satisfies `Fits n` and produces **exactly n query/reply pairs** on every state | All three theorems **depend on no axioms** |
| `ExactEightSector.lean` | **Exactly eight actual edge-continuation read frames**, total `Fits 8`, and sign-indexed decoder recovering each candidate **if** its finite statewise proof condition holds | `propext` for budget/length; `propext, Quot.sound` for terminal recovery |

The `ExactBudgetPadding` construction specifically repairs a serious source-of-unsoundness risk: an adaptive edge policy that can stop early must **not** cut short the simultaneous corner measurements. The fourteenth distinct corner color may not be available until the nineteenth frame; padding each early stop by **actual** reads, ignoring only the irrelevant extra edge responses, leaves exactly eight physical continuation slots for the fixed corner schedule. A full physical end-to-end proof must still transport those corner colors and derive their sign at exactly the permitted time, not use a free parity bit while selecting queries.

### Exact remaining proof gate (do not blur)

The frozen `NineteenDataReceipt.lean` validates a large JSON checker result with `native_decide`. In contrast, the above **generic** Lean theorems have explicit premises `StatewiseSectorValid` / `SemanticallyValidSector`. The missing formal bridge is to **verify that premise for each and every actual pinned representative sector** using a mathematically sound executable checker and its proof of reflection `check = true → StatewiseSectorValid`. This can use the finite statewise quantifier reduction and the exact `NineteenReadData.sector` candidate generator; it should not recalculate all cube permutations from scratch.

Then the only upper-specific obligations left are the actual deterministic normalization of every **ordered** first-eleven-color reply vector, the correct stable-sort **combined** color/position parity correction, the legal edge/corner sign coupling from **actually read** scheduled corners and the original-pose paired physical routing compiler. Until these are proved and assembled, the project must not call the full 19-frame attainable bound *unconditionally Lean-closed*.

### Primary-literature and custody receipts

Four correctly edited original-edition PDFs (Knuth 1991 Combinatorica, Babai 1981 Annals, Furst–Hopcroft–Luks 1980 IEEE FOCS, Tillquist et al. 2021 arXiv preprint) were ingested from Drive `00_INTAKE` into `10_PAPERS` after independent raw SHA-256 and page/edition verification; the folder was empty at post-move audit. [Original-byte custody](../../docs/0.29/20261121_AS0_00_INTAKE_FOUR_PRIMARY_SOURCE_CUSTODY.md). The **current missing-only count is five exact papers/editions**, not the prior eight; [current missing-only register](../../docs/0.29/20261121_AR0_MISSING_ONLY_DIRECT_DOWNLOAD_REGISTER.md).

[AS24 exact causal timing and finite quantifier theorem](../../docs/0.29/20261121_AS24_STATEWISE_CHECK_AND_EXACT_PARITY_TIMING.md) · [AS English working-manuscript chapter](../../papers/0.29/20261121_AS_SIGN_DEFERRED_SECTOR_SEMANTICS_WORKING_CHAPTER.md) · [Notion CUBE-REV 44](https://app.notion.com/p/41fef561cf928180b2b2f4c66703f971).

## 2026-11-21 AV: audited post-AU proof boundary and physical compiler handoff

The AU tagged and corner-clock theorems are compiled intermediates, not an unconditional physical nineteen-frame policy. The verified full-success Lean run is [#44910953723](https://github.com/WhoSia/CUBE-REV/actions/runs/44910953723); it is specifically tied to commit `ea6a6805d7faa2e12598bc7fbd461a491fc52ad5`, not to later manifest-only or CI-policy commits. The [P7 allowlist correction](https://github.com/WhoSia/CUBE-REV/commit/d9a6f6d853d43123732c04ac749e718b8477bb48) reconciled 142 genuinely tracked 0.29 files, deleting none; [audit #44911970086](https://github.com/WhoSia/CUBE-REV/actions/runs/44911970086) passed. CI is read-only and must not create commits authored or committed by `github-actions[bot]`.

The target abstract theorem is a **single total** `Policy (Fin 24 × Fin 24) FrameColor Coloring` with `Fits 19` and `∀ s, Reachable s → tree.run abstractPairRead s = s`. These are precisely the hypotheses of `Physical.physical_nineteen_of_abstract` in `PhysicalPolicyCompiler.lean`; its conclusion produces a fixed-probe legal-turn policy with `Fits 19` and `runFrames ... = s`. Therefore physical routing is already proved *conditionally*, rather than a reason to rewrite a turn planner.

The remaining upper-bound integration must supply, without lookahead or an oracle:

1. A deterministic total selection of the appropriate frozen representative from every feasible **ordered** eleven-color prefix, retaining the chosen 48-symmetry gauge and eleven-slot stable-sort witness. Prove the combined edge permutation-sign cocycle, including the odd-gauge counterexample regression; never substitute the preliminary 94 label-only orbits for the 80 full signed-histogram orbits.
2. A statewise interpretation of every frozen eight-read decision graph that returns the actual original edge coloring, using the true terminal parity *in the retained gauge*. The `native_decide` dependency of the 52-root receipt must remain disclosed separately from the generic logical theorems.
3. A paired observation adapter from the abstract original-coordinate edge query to the real `Fin 24 × Fin 24` pair at each charged frame, without substituting extra corner observations for free. Use the actually returned 19 corner colors and the established legal-corner identification theorem, then establish output equality for every `Reachable` original coloring.

### BB — Exact meaning of the twelve-slot coordinate mapping

The adjacent-swap `EdgeSlotOrder` constructor has a second correctness question beyond `left_inv` and `right_inv`: does its chosen `forward` function actually pull a representative-position lookup back to the correct original slot? [`RepresentativeRoundTrip.lean`](RepresentativeRoundTrip.lean) now contains the proposed generic `adjacent_twelve_index_matches_list` and `slot_order_trace_getElem?` theorems. The latter relates the **actual adjacent-swapped list at any of twelve indices** to the original list at the slot returned by `EdgeSlotOrder.forward`, using `List.getElem?` so the assertion is valid for arbitrary element types and repeated colors. These BB additions require their own clean exact-commit Lean CI acceptance; do not conflate with the already successful BA CI [#44931854349](https://github.com/WhoSia/CUBE-REV/actions/runs/44931854349).

**Consequence if accepted:** each bounded eleven-slot normalization trace can be used as a semantically justified 12-position adapter for the generic policy transport, not just as an invertible permutation with correct parity. **Not yet proved:** a total executable trace selection reproducing the frozen Python tie-handling rule pointwise on all ordered prefixes, the terminal sign decoder from true corner replies, and unconditional 19-frame correctness.

**BB exact-CI acceptance:** The full Lean package and theorem dependency checks passed in [#44933058857](https://github.com/WhoSia/CUBE-REV/actions/runs/44933058857) and [#44933735143](https://github.com/WhoSia/CUBE-REV/actions/runs/44933735143). The new `slot_order_trace_getElem?` and `frozen_prefix_has_semantic_twelve_slot_adapter` proofs show the exact pointwise twelve-slot index pullback and its coupling to the frozen signed correction. The explicit axiom lists are `[propext, Classical.choice, Quot.sound]` for both, with no `sorryAx`. This closes the generic coordinate-adapter semantics, **not** the 52-sector global policy correctness or physical 19-frame upper theorem.

**Claim barrier:** no theorem with all three properties above has yet been cited as kernel-compiled. A successful source-level check, static manifest audit, finite replay or conditional compiler theorem cannot be reported as the completed unconditional physical nineteen-frame upper bound. A future completed theorem must be tested on a pinned clean Lean 4.34.1 run with explicit `#print axioms` and immutable certificate digests.

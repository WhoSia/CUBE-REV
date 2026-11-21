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

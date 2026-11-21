# CUBE-REV 0.29 Z — physical corner bridge and formal theorem gates

**Date:** 2026-11-21. **Paper priority:** physical impossibility of 18 paired frames first; 19-frame policy attaining the bound second. This file is a proof engineering receipt, **not** a claim that the full nineteen-frame optimum is Lean certified.

## Delivered in Z

1. `formal/029/CornerTurnGenerators.lean`: extracts a face-turn corner-source index and twist from the **same `turnSlot` function** as the original 48-sticker geometry. Its five proposed kernel checks state: source corner bounds; injectivity on eight corners; preservation of the cyclic order of three corner stickers; zero total twist offset modulo 3; and equality of edge/corner permutation-sign increments for each of 12 basic quarter turns. No hand-entered generator table appears in the Lean definition.
2. `formal/029/ReachableCornerCoordinates.lean`: defines an `Fin 8 → Fin 24` oriented-corner action on an arbitrary corner arrangement, factors every physical 48-sticker face turn through the source-index/twist rule, proves an elementary cyclic color-lookup identity, and provides a structural induction for **existence of eight oriented corner coordinates matching all 24 actual corner-sticker colors of every `Reachable` coloring**. This theorem does *not* yet establish the legal piece permutation and twist conservation properties for all paths.
3. `formal/029/audit_corner_turn_generators.py`: independent geometry audit: all 12 basic turns, 288 sticker-source identities, 2,304 oriented-corner response identities, **78,732** input twist-vector cases (12 × 3⁸), 163,365 steps of deterministic legal compositions, and three malformed-generator negative controls. PASS.
4. `formal/029/audit_reachable_corner_bridge.py`: 2,304 local turn/corner tests plus 1,500 deterministic legal scrambles with **2,225,232** corner-sticker comparisons between geometric paint and cubie-coordinate action. PASS.
5. `formal/029/audit_lake_manifest.py`: 29 explicitly registered Lean library/default targets, 35 local import edges, no missing import or cycle, primary eighteen-frame theorem and both data receipts compulsory, read-only CI permissions. PASS.
6. `lakefile.toml` and `.github/workflows/cuberev029-lean.yml`: both new modules are compulsory Lake targets, each new Python audit runs before compiling, and main `PhysicalEighteen` and both certificate receipt modules are also built by default. Actions is read-only, with no bot commits.

## Mathematical conservation law to complete in Lean

For each basic turn `t`, define `σₜ(i)` as the source corner piece at destination position `i`, and `δₜ(i)` as the cyclic shift of its first source sticker. The finite generator lemmas establish

- `σₜ` is a permutation of the eight indices;
- the three source-sticker indices are `3σₜ(i) + ((j + δₜ(i)) mod 3)`, for `j=0,1,2`;
- `Σᵢ δₜ(i) ≡ 0 (mod 3)`;
- the edge and corner source permutations have equal signs.

For a corner array `aᵢ=(pieceᵢ,twistᵢ)`, the induced action is

`(t⋅a)ᵢ = (piece_{σₜ(i)}, (twist_{σₜ(i)}+δₜ(i)) mod 3)`.

Because `σₜ` is a permutation, `Σᵢ piece_{σₜ(i)} = Σᵢ pieceᵢ`. Moreover,

`Σᵢ (twist_{σₜ(i)}+δₜ(i)) ≡ Σᵢ twistᵢ (mod 3)`.

These equalities are **valid for every input coordinate array**, not just the 78,732 audit cases. The crucial next Lean theorem must express these reindexing/sum facts and induct over arbitrary `List Turn` paths. Only then may `reachable_has_oriented_corners` be strengthened to `∃ a, LegalCornerCoordinates a ∧ CornersAgree a s` with the correct edge/corner permutation parity, and only then can the actual missing-position-5 fourteen-color uniqueness theorem be invoked for all reachable cubes.

## Boundaries and risks

- The existing `PhysicalEighteen.physical_eighteen_impossible` lower theorem belongs to the historically compiled U revision and is unchanged here.
- The new Z Lean files contain theorem statements and tactic proofs, but **this execution container has no `lean` or `lake`, and no successful remote CI log was accessible in this session**. A source-level proof, static dependency pass, and independent exhaustive Python test **must not** be described as kernel-verified. Run the pinned Lean 4.34.1 build and inspect its actual output and `#print axioms`, then fix every compile error before declaring a completed formal component.
- The frozen 19-frame certificate has SHA-256 `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`. The 18-frame DAG has SHA-256 `dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce`. Both remain immutable.
- The V physical worked trace contained an impossible corner color pair and remains archived as a negative example; use the separately verified W correction.
- First-eleven-color transport for *arbitrary observed order* and reification of the frozen 52-tree continuation into a single Lean `Policy` remain open, separate from the corner legality bridge.
- The preset 21-frame optimum is a distinct theorem and has not been Lean formalized.

## Reproduction from a clean checkout

```sh
python3 formal/029/restore_pinned_data.py
python3 formal/029/validate_19_corner_schedule.py
python3 formal/029/audit_corner_turn_generators.py
python3 formal/029/audit_reachable_corner_bridge.py
python3 formal/029/audit_lake_manifest.py
cd formal/029
lake build
lake env lean CornerTurnGenerators.lean
lake env lean ReachableCornerCoordinates.lean
lake env lean PhysicalEighteen.lean
```

Run the Python audits with standard assertion-enabled execution (`python3`, never `python3 -O`). The `lake` commands require Lean 4.34.1 and cannot be claimed successful in the current environment.

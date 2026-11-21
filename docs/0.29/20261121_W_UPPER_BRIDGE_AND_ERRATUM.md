# CUBE-REV 0.29 W — Upper-bound transport and physical replay audit

Date: 2026-11-21 (Asia/Seoul). This is an **audit and formalization ledger**, not a publication-ready W manuscript. P–V remain frozen.

## Priority of the results

The paper's primary finding is the **impossibility of universal reconstruction in 18 paired frames**, even when the corners are fully disclosed. The 19-frame construction is the matching optimality witness. The previously compiled Lean theorem `PhysicalEighteen.physical_eighteen_impossible` gives the physical lower bound with reachable states. The corresponding one-piece formalization of the physical **19-frame upper bound remains open**.

## Newly reproduced finite evidence (Python, independently of EdgeGame)

The runner `check_r029_w_upper_bridge.py --certificate reproduction/upper-policy-certificate.json` reads the **unchanged** 19-frame policy JSON (SHA-256 `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`) and checks the following:

| Condition | Validated result | Method |
| --- | --- | --- |
| Representative policy | 52 roots; 141,097 policy nodes; 144,736 representative assignments | Independent tree checker |
| Symmetry transport of first-color records | 1,362 feasible count vectors, 52 canonical representatives | Direct enumeration |
| Full candidate set transport | 3,215,616 oriented edge assignments; image equals each representative's complete compatible set | Explicit bijection of address positions, sticker colors, orientation and permutation parity |
| Color-relabel flips | All 48 opposite-pair-preserving relabelings keep even total edge flip even | Finite enumeration over 12 edge labels per symmetry |
| Parity correction | In 726 count vectors the sign is unchanged; in 636 it is reversed | `sgn(transformed) = sgn(original) XOR sgn(position sort) XOR sgn(label relabeling)` |
| Corner decoder | 24 distinct ordered two-color pairs for the 8 possible corner labels and 3 orientations | Enumerate 8×3 pairs, identify eighth corner by exclusion and twist-sum law |
| Physical corner regression | 12 face-turn generator states and 3,000 reproducible random turn words | Independent 48-sticker geometry |
| Simultaneous probe routing | All 576 base target pairs, plus 4,000 random probe/prior-pose combinations | Independent route table and geometric turn permutations |
| Physical turn invariants | For all 12 face-turn generators: total edge flip offset 0 mod 2, corner twist offset 0 mod 3, equal edge/corner permutation signs | Explicit generator action tables; composition gives invariants for arbitrary words |
| Negative controls | Wrong parity correction, loss of second corner color, corrupted turn route are each rejected | Three mutation tests |

The transport test uses **sorted first-color records** because arbitrary permutations of the initial 11 positions are handled by an explicit permutation. The transport formula has an inverse and preserves each query/color relation. The number 3,215,616 counts one representative ordered record per feasible color-count vector; it is not the cardinality of all physical initial states.

## A newly detected problem in V's worked example

**The raw V witness is internally inconsistent.** Its `corner_permutation` states that position `URB` holds the cubie `URB`, but the trace reports `URB[1] = U` and `URB[2] = L`. Such a cubie cannot show the pair `(U,L)`. In fact, that ordered pair uniquely identifies the oriented `ULF` cubie in the canonical right-handed corner order. The reported `DRF[2] = L` likewise contradicts V's originally claimed `DBR` cubie at that position. The old worked-example script checked neither physical corner consistency nor the turn-string endpoints. Accordingly **do not cite V's original example as a physically valid replay**.

Preserve V's original witness byte-for-byte (SHA-256 `5c2232b642b609c5eaf829e59265e7f566facb032ee67b113ccddabf51fa76e4`). The new **corrected illustrative witness** (`worked-physical-replay-corrected.json`, SHA-256 `e908e0d51f1b939b292b8f393f8443019dcff814baf235ccb23ef5036cc91aa6`) keeps the eight edge addresses/responses and original query routes, but replaces its incompatible corner permutation with a **different legal corner state**:

- Corner labels by position `UFR, URB, ULF, UBL, DRF, DBR, DFL, DLB`: `UFR, ULF, UBL, DBR, DFL, DLB, URB, DRF`.
- Corner twists: `(0,0,0,0,1,0,0,2)`; twist sum 0 mod 3.
- Corner permutation sign even, matching the reconstructed original edge permutation.
- Fourteen corner readings use two cyclic slots at seven corner positions: `UFR[1–2], ULF[1–2], UBL[1–2], DFL[1–2], DLB[1–2], DRF[1–2], URB[1–2]`. The eleventh read is `DRF[1]`, frame 12 is `DRF[2]`, frame 13 is `URB[1]`, and frame 19 is `URB[2]`. The known `DLB[1]` is repeated in frames 14–18.
- The audited last eight frame routes reproduce **all 16 intended sticker addresses and all eight edge replies**. The corner color observations are consistent with the corrected state. The original remains a negative test.

The corrected state is an **illustrative replacement**, not a claim that the raw V random sample was the same physical cube. A future W manuscript must replace the example data and explicitly acknowledge the erratum in the version history. Figure 2 and any caption derived from V must be rechecked before republication.

## Generator-to-word legality proof

For each face quarter-turn `t`, the independently derived 48-sticker permutation has the following cubie action on positions `p`:

- edges: `e'_p = e_{σ_t(p)}` and `f'_p = f_{σ_t(p)} + a_t(p) (mod 2)`;
- corners: `c'_p = c_{τ_t(p)}` and `k'_p = k_{τ_t(p)} + b_t(p) (mod 3)`.

The finite certificate checks that `sum_p a_t(p) = 0 (mod 2)`, `sum_p b_t(p) = 0 (mod 3)`, and `sgn(σ_t) = sgn(τ_t)` for each of the 12 generators. Summing after a position permutation leaves a sum unchanged; signs multiply under composition. Induction on the length of a turn word therefore gives conservation of edge flip parity, corner twist sum and equality of the permutation signs. These are mathematical consequences of generator checks, but **the new invariants have not yet been added as compiling Lean theorems**.

## Remaining Lean obligations (do not hide these in the submission)

1. **Universal transport:** prove that the 48 color renamings preserve the legal flip sector and induce bijections between compatible edge assignments for each first-color record, with exact parity correction and query/response commutation. The Python audit above is a finite test and explanatory witness, not yet a Lean lemma.
2. **Universal corner decoder:** prove two cyclic ordered reads at each of seven positions recover the seven oriented cubies, then the eighth from the unused label and the legal twist-sum invariant. Align this with the physical `Coloring` and `Reachable` definitions.
3. **Certificate-to-policy composition:** turn `NineteenReadData.check` and the `sector_complete` theorem into a single Lean `Policy` that selects every frame's two addresses **before** both replies and returns the exact initial 48-sticker state in ≤19 frames, for every reachable initial state. The existing joint route theorem handles the physical addresses.
4. **Independent kernel/trust review:** the historical finite graph and policy receipts use `native_decide`. Re-run the pinned Lean 4.34.1 build, inspect `#print axioms` for the final theorem, verify every included data hash, and classify the trusted native evaluator explicitly.
5. **Preset 21 theorem:** formalize separately; it is not a prerequisite for the principal 18-frame impossibility result, but it is needed if the final headline asserts *both* exact preset and adaptive optima as completely Lean-verified.

## Reproduce

Extract the V reproduction assets and the W scripts into the same `reproduction/` folder, retain `formal/029/ProbeRouteWords.lean` beside it, and run:

```bash
python3 check_r029_w_upper_bridge.py --certificate upper-policy-certificate.json --output W-upper-bridge-receipt.json
python3 audit_r029_w_worked_route.py
```

The second command **must reject** the original V replay and accept the corrected illustrative replay. A successful computational receipt does not license a claim that the remaining universal Lean theorem has been proved.

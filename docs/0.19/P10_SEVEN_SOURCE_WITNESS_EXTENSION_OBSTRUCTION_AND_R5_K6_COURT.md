# CUBE-REV 0.19 — P10: Seven Physical Five-Source Words, Extension Obstruction and the Certified Six-Word Court

## The physical problem and current proof grades

The original fixed source family R has 1,192 admitted subsets of twelve initially flip-zero physical UR-edge starting positions; R5 is its 480-element **five-source-only** subfamily. Experiments are actual five-HTM-word cube actions observed by an intrinsic orientation bit after each move. The integer objective M*_R5(5) counts the number of fixed **complete word experiments**, not the number of turns or a human solving strategy.

**Currently proved by independent finite local physical checks:**
- P9: no set of **five** actual physical L5 word experiments covers all original R5. Hence M*_R5(5)>=6. A new dedicated external GitHub CI receipt for P9 is not yet confirmed.
- P10: the following **seven** real five-turn word experiments cover all 480 original R5 sources:
  1. `F' B' U F B`
  2. `F' B D F B`
  3. `F B' L F B`
  4. `F B' D F B`
  5. `F B' R F B`
  6. `F B U F B`
  7. `F B' U2 L2 F`

Therefore the **mathematically supported integer interval** is

```
6 <= M*_R5(5) <= 7.
6 <= M*(5) <= 8  (original full 1192-source family).
```

A separate SciPy/HiGHS *numerical mixed-integer optimization* solved the five-only 480x2023 incidence with **optimal integer objective 7** in approximately 20 seconds, producing an actual seven-word witness. **This numerical k6-infeasibility determination is NOT an independently checked UNSAT/DRUP certificate, and it has not been promoted to an exact theorem.**

## The seven-word R5 cover is not singly extendible to a full eight-word cover

An independent source-locked Python script replays all seven words against all twelve original physical starting slots, exactly reconstructs their observation-history partitions, and checks injectivity for each of the original 1,192 source masks.

It finds **1,120 of 1,192 covered**:
- all **480 five-element** requirements covered;
- **64 four-element** requirements not covered;
- **8 three-element** requirements not covered.

Fix those exact 72 uncovered source masks. Enumerate the **14,938 distinct physically realizable five-word-length output partitions** and for each count the subset of these 72 requirements it identifies. The **maximum is 36**, so no single additional real five-action experiment can distinguish the entire missing family. The physical replay script asserts both the full 14,938-partition census and the bound 36.

**Exact conclusion for this particular seven-word dictionary:** at least **two** additional words are required to extend it to all original 1,192 sources. This is NOT a theorem that any seven-word R5 cover has this property, and does not contradict the already validated **eight-word complete-original-family** cover. It is a witness to context-dependent cover interactions: constructing a good dictionary for the five-source subfamily does not automatically minimize extension cost for lower-cardinality source requirements.

## Exact all-k physical reduction and safe 16-fold symmetry

For the identical 480-source R5 source family, all 18^5=1,889,568 actual legal physical words project onto 14,938 observation partitions and **3,344 distinct R5 source-coverage types**. Inclusion-maximal physical R5 coverage types number **2,023**, with all-k domination preserving the existence of a k<=6 cover.

Directly enumerate the 16 source-incidence automorphisms induced by signed coordinate maps (x,y,z)->(±x,±y,±z) or (±y,±x,±z), including orientation-reversing *combinatorial relabelings*, not executable Rubik actions. For each map, explicitly verify:
1. the full original 480 five-source family is permuted bijectively;
2. every physically realized maximal R5 coverage mask maps to another mask in the same 2,023-element family.

These 2,023 masks decompose into **137 column orbits**. Any nonempty source-covering dictionary can be globally relabeled so that one of its selected columns becomes an orbit representative. This gives a **sound OR clause over 137 representative Boolean variables** to break symmetry while **retaining all 2,023 actual physical Boolean decision variables**. Collapsing each orbit to a single Boolean variable is NOT equivalent and must not be done.

A new standalone source-locked test `scripts/cuberev-019/prove-L5-five-source-k6-SAT.py` does exactly that with an optional `--prepare-only` finite-check mode. **Local preparation without any SAT solver: PASS** (3,344 -> 2,023; 16 symmetries; 137 orbits; independent actual seven-word upper). The proof-producing mode writes a deterministic CNF, attempts k<=6 Glucose4 SAT/UNSAT and requires a separate **pinned drat-trim verification against that exact CNF** before accepting any UNSAT statement. A numerical status of TIME_LIMIT/UNKNOWN is not upgraded.

The corresponding read-only GitHub Actions `.github/workflows/cuberev-019-r5-k6-exact-court.yml` was committed. **Its execution/verified DRUP outcome has not yet been independently read** and k6 remains open.

## A negative method test: conditioning does not defeat the fractional gap

For each of the 137 orbit representatives as the first selected R5 experiment, solve the residual ordinary fractional covering LP for the remaining requirements using all 2,023 physically realizable R5 columns. All 137 numerical residual LP optima are <=5. Thus the bare first-experiment conditional LP finds no proof that a 6-word cover is impossible. This is a **numerical diagnostic**, not a solver-free rational theorem. More involved integer cuts, collision-hypergraph constraints, proof logging or higher-order symmetry-aware branching are necessary.

The unconditional R5-only exact fractional LP optimum remains **185/39**, with independent source-locked rational primal and dual certificates in P8. The full-original-family fractional LP remains **16/3**, while actual dictionary cardinalities are integers.

## Sources, code, durable artifacts and next step

- Actual source and observation-checking code: `scripts/cuberev-019/verify-L5-seven-five-source-and-extension.py`.
- SAT/DRUP proof court and independent preparatory reduction: `scripts/cuberev-019/prove-L5-five-source-k6-SAT.py`.
- New CI: `.github/workflows/cuberev-019-r5-k6-exact-court.yml`. Proof must be externally checked and source-linked to become authoritative.
- P9 exact lower k5: `docs/0.19/P9_EXACT_FIVE_SOURCE_K5_UNSAT_AND_FULL_K6_RANK_GATE.md`.
- P8 original-source-invariant LP certificates: `docs/0.19/P8_ORDER_INVARIANT_FRACTIONAL_COST_AND_K6_DUAL_PAIR_COURT.md`.
- Immutable original physical authority SHA256: `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`.
- P10 source+evidence ZIP, 11 SHA-256-verified component files, archive SHA256 `0000675be24b698b3edde657cf4faa56eedc2b85330551bc169dc2483520c525`: https://drive.google.com/file/d/1aMmSupK8HJgOUoNNffOrMxtmKmNkVDUH/view .
- Notion 0.19 active research authority: https://app.notion.com/p/3f4ef561cf92813d9edfff4911db39d2 .

**Next proof gate:** Resolve R5-only k<=6 SAT vs certified UNSAT first. If UNSAT independent proof is verified, the lower bound becomes **M*(5)>=7** immediately. But full M*(5) would still be 7 or 8 until a full original 1192-source seven-word witness or externally checked full k7 UNSAT proof is found. Do not infer this from the failure of the specific seven-word R5 witness to extend with one additional word.

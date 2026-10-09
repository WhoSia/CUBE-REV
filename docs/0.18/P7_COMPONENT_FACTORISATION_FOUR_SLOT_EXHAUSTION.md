# CUBE-REV 0.18 — Factorized Rubik Set Cover, Exhaustive Four-Slot Minimum and the Remaining Five-Slot Proof

**Single ACTIVE official version:** CUBE-REV 0.18. This is an internal P7 certificate report, not a new formal version. Our subject remains the actual 3×3×3 Rubik's Cube: 18 legitimate HTM face turns, the tracked UR-edge's 24 position/flip states, four post-move orientation-bit observations, and 1,192 original legal source subsets.

## Exact all-cardinality reduction to 2 connected components

The physical incidence has 1,192 original source rows and 1,323 inclusion-maximal four-turn experiment columns (computed from all 18^4 = 104,976 literal legal HTM action words). A complete **row-support subsumption proof** retains 398 irredundant source conditions, with a stored stronger-row witness for each of the 1,192 original sources. A complete **projected column-dominance proof** reduces 1,323 original physical word representatives to 168, with a dominating original word for each of the 1,323 candidates. BOTH transformations are valid **for any dictionary size k**, not merely the historical 24-word near-dual family.

The 398×168 bipartite incidence graph has exactly two connected components:

| Component | Original Cube source size | Coverage rows | Real HTM word candidates | Numerical HiGHS optimum |
|---|---:|---:|---:|---:|
| A | five initial source slots | 334 | 80 | 27 |
| B | four initial source slots | 64 | 88 | 7 |

No retained physical word covers constraints in both components. Consequently the equality `M* = M*_A + M*_B` is combinatorially exact. The two verified physical upper witnesses split into 27 plus 7 selected four-move words. **But the independent proof of A's lower bound 27 is not yet finished.**

## New independent executable proof: component B has minimum 7

The local independent verifier derives the two all-k quotients anew from the frozen original real-Cube physical instance (SHA-256 `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`). On the 64×88 four-slot component, it uses Python 3 **standard library alone**, not HiGHS or the SAT solver.

To disprove any ≤6-word dictionary, it recursively chooses an uncovered source requirement and branches over **every** permissible cube word that covers it. It memoizes identical (uncovered-source-mask, remaining-word-budget) states. Its only pruning uses optimistic *overestimates* of achievable extra coverage: the sum of the largest remaining single-word uncovered hit counts, and for any chosen next word, the assumed theoretical best remaining hit count multiplied by remaining slots. Overestimates cannot prune a valid cover. Thus the search is exhaustive, sound, and terminates with no solution.

Observed local full search:

- Original legal Cube source size: 1,192; physical candidates: 1,323.
- Independent row and column quotient: **398 × 168**, component **64 × 88**.
- Search at cardinality ≤6: **33,846 memo states, 45,010 branches, 14,147 capacity prunes, no cover** (about 0.8 seconds).
- Positive control: the already HTM-replayed CP-SAT physical 34-word dictionary contains **seven** actual representative words in the four-slot component, and their union covers all **64** retained original source requirements.

Therefore `M*_B = 7` has an independent, tiny, fully re-executable **finite exhaustion argument**. This is distinct from a DRUP certificate; the proof checker is the explicit auditable algorithm. A second optional [read-only stdlib GitHub Actions court](../../.github/workflows/cuberev-018-four-slot-stdlib.yml) is submitted. Its queued execution is **not** yet a new CI PASS.

The [full independent standalone verifier](../../scripts/cuberev-018/prove-four-slot-minimum-seven-stdlib.py) was separately mirrored in an archival reproduction bundle:

- Clean-extraction ZIP maintained in personal CUBE-REV Library (73,186 bytes; SHA-256 `3e8f4231ce255c99229f02315c608a5f53ca6a26d5b930056bc3a101ae1ec564`)
- Saved to personal Library `/CUBE-REV/0.18/CUBE_REV_018_DOUBLE_QUOTIENT_AND_FOUR_SLOT_EXHAUSTIVE_CERT_20261010.zip`. The ZIP contains a pinned source physical instance, original row certificate, true Cube 34-word witness, standard-library independent rechecker, numerical HiGHS control logs, receipt and SHA manifest. Verified a fresh extraction and successful replay.

## Component A (334×80): remaining genuinely difficult certificate

Locally **two** different independent integer-program formulations confirm the numerical minimum 27 for this five-slot component. SciPy 1.17/HiGHS returns `Optimal / objective 27 / integer lower bound 27 / MIP gap 0`. A direct feasibility court with at most 26 selected physical columns returns `INFEASIBLE` (approximately 14 seconds in one run). These are **soundly scoped numerical solver receipts**, NOT an independent proof-carrying UNSAT trace.

The previously written [component SAT and DRUP runner](../../scripts/cuberev-018/prove-physical-component-minima.py), attached to [read-only GitHub Actions](../../.github/workflows/cuberev-018-component-unsat.yml), attempts **at most 26 words** on the exact original 334×80 component; it also explicitly processes the easier 64×88 k6 component FIRST to preserve its portable DRUP receipt if the harder SAT phase hits a budget.

A valid external `drat-trim s VERIFIED` proof of component A's 26-word UNSAT, combined with our independent component B 7 proof and already fresh real HTM 34 upper, would establish **exact M* = 34** in the declared physical observation model. Until then our **fully independent proof-checked global interval remains 30≤M*≤34**.

## Failures and interpretation guards

- A numerical solver saying `Optimal` is NOT a byte-indexed independently checked UNSAT proof.
- A restriction to the 162 full-mass candidates or the union of two 34-word dictionaries is NOT the original global 33-word decision problem unless justified by the all-k double-quotient theorem.
- The old P6 34-word menu FAILED conventional real HTM replay from the D/D' face direction mismatch. The separately created CP-SAT 34-word dictionary PASSED actual sticker-based HTM replay [#37948949764](https://github.com/WhoSia/CUBE-REV/actions/runs/37948949764).
- The result is about fixed dictionaries of four-action UR-edge *observation-history experiments* over the declared 1,192 initial-source family, not a 34-move solver for arbitrary 3×3 Rubik's Cube states.
- None of these finite numerical theorems has yet been formally translated into a complete Lean kernel physical-sticker-to-CNF proof. Literature novelty relative to existing automata distinguishing-sequence and test-suite minimization remains separately audited.

**Next decisive proof obligation:** produce a self-contained DRUP/LRAT or independently exhaustive finite search certificate of `M*_A>26`, and validate it against the original Cube incidence and all-k quotient witnesses. All work stays in formal version 0.18.

# CUBE-REV 0.19 — P11: High-rank rigidity, symmetry first-column reduction, and integer union cuts

**Research status:** This is a locally independently reexecuted *necessary-condition theorem* for the original physical five-state-only six-experiment court. It **does not** solve its SAT/UNSAT decision. The certified physical bound is still `6 <= M*_{R5}(5) <= 7`, and the full original 1192-requirement `M*(5)` remains one of `{6,7,8}`. Previously issued local R5 k5 exhaustive certificate supplies the strict `>=6` lower bound. The P10 real seven-word R5 dictionary supplies the `<=7` upper bound. CI runtime PASS has not been independently retrieved.

## Physical assumptions

Twelve initial zero-flip positions of the tracked UR edge on the real 3x3 cube; 18 outer face HTM actions; one intrinsic orientation bit after each of five moves, with the full ordered transcript retained; original exactly 480 admitted five-position source sets. Experiment cost is **one per five-move word**. The original 1192-source dataset is fixed with SHA-256 `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`.

## Theorem 1 — At least three high-rank physical words in any six-word R5 cover

Define `rank(w)` to be the number of distinct 5-bit observation histories among the twelve tracked-edge initial slots under real physical word w. A complete R5 six-word dictionary **must contain at least three words with `rank(w)>=6`.**

The complete original physical census of 14,938 distinct observation partitions induces 3,344 distinct R5 cover sets, with distinct types by output-history rank: ranks 1,2,3,4 each only the empty R5 covering type; rank5: 2,168 types; rank6: 1,144 types; rank7: 32 types. The maximum number of admitted five-source requirements covered by a rank5 word is 64; for a rank6 word it is 132; for rank7 it is either 100 (16 types) or 168 (16 types). No higher rank is physically realizable by any real five-HTM word in this model.

The already independently verified P9 5-word impossibility theorem rules out any `rank<=4` word in a hypothetical six-word cover: deleting it would leave five words obliged to cover all R5, impossible. Hence every selected word has rank at least5.

- Zero high-rank words: at most 6×64=384 requirements covered, less than480.
- Exactly one high-rank word of rank6: at most 132+5×64=452, less than480.
- Exactly one rank7 word: its source coverage has either size100 or168. Across ALL physically realizable rank5 words, its uncovered source set has maximal additional one-word gain 64 (100 case) or 48 (168 case). Thus its remaining 5 rank5 words add at most 5×64=320 <380, or 5×48=240 <312. No such cover exists.
**Duplicate-coverage edge case:** The 690,900 two-high audit enumerates pairs of **distinct** physically realizable five-source coverage masks. A six-word dictionary containing two words with identical five-source coverage masks is already impossible under P9: deleting either leaves five words with precisely the same R5 union, contradicting the proved five-word impossibility. Thus omitting equal-mask pairs is logically valid and does not restrict the theorem to different move strings.

- Exactly two high-rank words: independently enumerate ALL unordered pairs from the 1,176 physically realizable distinct rank6/rank7 R5 covering types: exactly `C(1176,2)=690,900`. For 680,500 pairs, more than `4×64=256` sources remain uncovered, making four remaining rank5 words insufficient. For all other 10,400 pairs, compute the exact best residual gain `g(U)` over ALL 2,168 physically realizable rank5 R5 cover types after the high-pair union U; for every pair `4*g(U) < |R5 \ U|`. These necessary upper bounds exclude all remaining pairs.

This proof is **source-locked finite enumeration with exact integer bitsets**, independent of numerical optimization and SAT heuristics. It is reproduced by `verify-P11-R5-rank-symmetry-cuts.py` using only the physical source, actual maps, all original partition representatives, and original dual certificate.

## Theorem 2 — Sound 69-orbit representative gate

The 3,344 physically realized R5 coverage types reduce by inclusion dominance to 2,023 inclusion-maximal types (the existence of any k-cover is preserved). Across these 2,023 columns, physically reconstructed observation ranks are 5: 975, 6: 1,016, 7: 32. The 16 previously checked signed-coordinate **incidence relabelings** preserve all original admitted R5 source masks, the complete physically maximal coverage family, and **each column's rank**. The 2,023 columns form 68 rank5 orbits, 66 rank6 orbits, and 3 rank7 orbits. Some symmetries are reflections; they are *not* physically executable face turns.

Because any solution contains at least three high-rank words, it may be globally relabeled so that at least one selected high-rank word belongs to a selected set of 69 representatives (one from each rank6/rank7 orbit). Thus the Boolean clause `OR_{j in 69 high representatives} x_j` is an exact satisfiability-preserving symmetry breaker. This is not an equivalent 69-variable integer optimization: all 2,023 physical selection decisions must remain. The stronger `sum_{high actual columns} x_j >= 3` is also a valid Boolean/cardinality condition, independently derived from Theorem 1.

## Theorem 3 — Exact source-dual pair forbidden clauses

The P8 exact rational dual for R5 has 80 positive original five-source row weights, total integer numerator 1,480 and a maximum capacity 312 per physically realizable experiment. If at most 6 words cover all R5, **any selected pair** must jointly cover weighted union mass at least `1480 - (6-2)×312 = 232`. Among `C(2023,2)=2,045,253` unordered pairs of the source-exact inclusion-maximal physical R5 covers, 747,883 fail this inequality; they supply source-validated necessary binary clauses `not x_i or not x_j`. Exactly 1,297,370 pairs are not excluded by this particular test.

The computation uses exact 80-bit source-row membership, integer weights, and independently replayed real physical observation partitions. This is a necessary condition but does **not** refute all six-word solutions.

## Proof/court engineering

- `scripts/cuberev-019/verify-L5-R5-rank-symmetry-and-pair-cuts.py`: standalone no-solver source-locked independent physical verifier; checks all theorems with explicit integer arithmetic, emits JSON receipt. Local full verifier passes.
- `scripts/cuberev-019/prove-L5-five-source-k6-SAT.py`: now runs this separate proof checker as a **hard gate** before changing the SAT instance; imposes the 69-representative first-column clause, totalizer-based `>=3` high-rank requirement and 747,883 sound binary pair exclusions, plus original 480 requirements and at-most-six cardinality.
- `.github/workflows/cuberev-019-r5-k6-exact-court.yml`: newly gated by independent P11 verification; any UNSAT emitted must still pass independent pinned DRUP verification against the *strengthened actual CNF*. No CI success receipt has yet been independently seen.

**Important:** This P11 advance does not establish `M*_{R5}(5)=7`, since that requires an independently checked **six-word UNSAT** proof or an independently checkable equivalent full finite exhaustive proof. Nor does it settle the full 1192-source k7 case. The 7-word R5 positive witness already exists, but its particular dictionary cannot be extended by one additional word to cover the full family. Do not generalize its non-extension property to all R5 dictionaries.

## Next highest-value proof obligations

1. Resolve the SAT/UNSAT of the P11-strengthened six-word physical R5 court, retaining the physical 2023-variable selection semantics; if UNSAT, independently validate DRUP and all P11 derived clauses, then upgrade `M*_{R5}(5)=7` and original `M*(5)>=7`.
2. If strong SAT still times out, split into `exactly 3 high-rank`, `exactly 4`, `exactly 5`, `exactly 6` subcourts and use residual-weight upper bounds and the 69 high-orbit cases. Additional symmetry breaking must be proven source-preserving.
3. Then attack the **full original 1,192-source** seven-word dictionary by physically replayed SAT witness or independent UNSAT, not by assuming the particular P10 seven-word R5 dictionary can extend.

## References

- P9 physical R5 five-word finite certificate and P10 7-word R5 witness, GitHub `docs/0.19/`.
- Original physical source and full partition SHA-256 audit in bundle manifest.
- GitHub research branch `research/current` and Notion active 0.19 canonical page.
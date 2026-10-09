# CUBE-REV 0.19 — P12: Exact Restricted Five-Source Dictionary Cardinality Seven

**Statement.** Fix the original 480 admitted five-element sets of 12 initial flip-zero UR-edge slots from source SHA-256 `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`. An experiment is a five-HTM word acting on the physically sticker-derived tracked-edge map, with one intrinsic orientation bit read after every action. The minimum number of **fixed nonadaptive dictionary words** such that at least one word distinguishes every admitted five-state source is **exactly seven**:

\[
M^*_{\mathcal R_5}(5)=7.
\]

This is a **locally independently rechecked, finite computer-assisted proof**. A fresh external GitHub Actions run receipt or an independent proof-assistant formalization must be checked separately. In particular this does **not** certify the entire original 1,192-source \(M^*(5)\), which is now bounded \(7\le M^*(5)\le8\).

## Positive physical upper certificate

Actual legal five-turn words, verified against all 480 original source sets by independent replay:

```
F' B' U F B
F' B D F B
F B' L F B
F B' D F B
F B' R F B
F B U F B
F B' U2 L2 F
```

## Negative physical six-word theorem — exhaustive proof partition

Prior independently audited P9 proves no five physical words cover all 480 admitted five-source constraints. Therefore a hypothetical six-word solution cannot contain any word with fewer than five distinct observation histories (it would contribute zero to all five-source requirements and could be removed).

Let \(r(w)\) be the number of distinct five-bit histories across the twelve initial states. All actual five-HTM physical observation partitions have \(r\le7\). In the original, **rank-specific** real physical source-coverage types there are 2,168 types of rank five, 1,144 rank six, and only 32 rank seven (some types across ranks may have identical masks, but remain distinct physical ranked choices). For a putative six-word cover, let \(t\in\{0,\dots,6\}\) be the number of selected rank-seven words. Duplicate identical coverage masks may always be deleted; P9 excludes any resulting cover of five or fewer words. Seven separate cases are refuted:

| Exactly t rank-seven words | Proof mechanism | Finite court size |
|---|---|---:|
| 0, at least one rank five | One nonnegative integer dual, exact cap for **all** raw rank-five/six physical masks | 1 dual |
| 0, all six rank six | Rank-six-only inclusion dominance 1,144→1,080 (rank preserved), signed incidence symmetry yields 70 first-word orbits; each fixed word leaves a weighted residual with total mass >5×per-word capacity | 70 duals |
| 1 | 3 rank-seven first-word orbits; for each, 5 remaining physical rank-five/six words are ruled out by original-source row weights | 3 duals |
| 2 | 44 orbits of all \(\binom{32}{2}=496\) real rank-seven pairs; exact source-residual dual against every original rank-five/six type | 44 duals |
| 3 | 327 orbits of all \(\binom{32}{3}=4,960\) rank-seven triples; exact residual dual against every original rank-five/six type | 327 duals |
| 4 | All \(\binom{32}{4}=35,960\) four-word rank-seven subsets; for each uncovered source requirement, all physical choices of the first of two remaining rank-five/six words are covered using 480-row candidate support intersections | complete finite enumeration |
| 5 | All \(\binom{32}{5}=201,376\) five-word rank-seven subsets; no single rank-five/six word covers the residual | complete finite enumeration |
| 6 | All \(\binom{32}{6}=906,192\) rank-seven six-word subsets; max cover 472 of 480 | complete finite enumeration |

Each integer dual is a list of explicit nonnegative integers on the *original 480 five-state source row coordinates*; the independent checker calculates candidate weighted mass by plain Python integer arithmetic across every physically realized rank-specific original coverage type, not trusting fractional LP calculations, a solver verdict, or a fragile reduced-array index. **445 integer dual case certificates** were audited. Group relabelings include some reflections, which are **incidence automorphisms rather than actual cube moves**; closure is explicitly checked before orbit reduction.

### Critical correction against unsound cross-rank dominance

For a rank-constrained proof, it is **unsound** to infer that all nonmaximal rank-five/six words are redundant merely because a physically realized rank-seven word covers a superset of their source demands. This would change the number of rank-seven words. P12 restores all 2,168 raw rank-five and 1,144 raw rank-six physically generated coverage types; only the all-rank-six branch performs a new **within-rank** dominance reduction to 1,080. The two-/three-rank-seven dual courts use the complete raw physical rank-five/six family. The four-/five-rank-seven finite courts also use all the original raw physical non-rank-seven masks.

### Reproducibility gates

1. Rebuild `physical.json` using the frozen original 0.18 physical exporter; assert SHA-256.
2. Rebuild the 18 action maps and enumerate 18⁵ physical words, unique partitions exactly 14,938.
3. Run P9's complete five-word UNSAT checker again.
4. Run the P12 arithmetic-only script on three explicit integer certificate files (445 cases, fully source-locked).
5. Run P12's independent high-rank 4/5/6 complete finite enumerator and original seven-word physical replay.
6. Only combine the three gate receipts after source hash and all exact counts agree. The combined receipt certifies `CUBE_REV_019_R5_PHYSICAL_EXACT_SEVEN_INDEPENDENT_FINITE_COURTS_PASS`.

This is a closed finite **mathematical R5 subproblem**, not evidence about human cognition, FMC, or ordinary cube-solving cost. **Next:** decide full 1,192-source k=7 SAT/UNSAT under the same physical oracle; the original eight-word witness establishes the upper bound eight.
# CUBE-REV 0.18 — Row-Implication Quotient, Exact 398-Condition Core and the k=33 Proof Gap

**Sole active version:** CUBE-REV 0.18. **Scientific target:** actual 3×3 Rubik's Cube 18 legal HTM moves, one tracked UR-edge (24 cubie position/orientation states), four post-action flip reports, 1,192 original admissible initial source-slot subsets. Generic set-cover notation is a *proof language for this cube experiment*, not a detached automata study.

## New all-k theorem: coverage-row implication

Let `\mathcal W` be the 1,323 legitimate inclusion-maximal coverage representatives for the frozen 104,976 length-four physical Rubik words. For every original source subset `S_i`, define its *candidate support*

```
R_i = { w in W : the four-bit observation-history map h_w is injective on S_i }.
```

The original set-cover constraint is `∨_{w in R_i} x_w` for every one of the 1,192 source sets. If `R_i ⊆ R_j`, then satisfying source `i` entails satisfying source `j` for **every possible dictionary size**. Therefore `j` is logically redundant. Retain exactly the **inclusion-minimal row supports** (remove duplicates). This preserves the existence/nonexistence of a universal dictionary with any given cardinality k.

A complete physical-source incidence reconstruction and deterministic, independent bitset implication audit yield:

| Frozen real Rubik observation contract | Distinct rows |
|---|---:|
| Original admissible source subsets | **1,192** |
| Distinct candidate-support rows | **1,146** |
| Inclusion-minimal, irredundant support rows | **398** |
| Redundant original constraints | **794** |
| Original inclusion-maximal four-turn experiment candidates | **1,323, UNCHANGED** |

The **398** irredundant constraints comprise **64** admissible four-slot sources and **334** five-slot sources; all original 220 three-slot source constraints are redundant. Distribution of remaining source support cardinality: 4-slot sources `37:16,38:16,46:24,66:8`; five-slot sources `4:54,5:112,6:48,7:112,8:8`. These are exact finite counts under the physical cube oracle, not yet closed-form symbolic face-group formulas.

Proof sufficiency is auditable without trusting an optimizer: [deterministic all-k implication checker](../../scripts/cuberev-018/reduce-by-source-implication.py) reconstructs every `R_i` directly from the physical 1323-column universe, saves all 398 retained original row IDs, and writes a **1,192-entry implication witness list**, one retained stronger condition for each original source. Each witness `r` is verified by checking `R_r & ~R_i = 0`. Every discarded original clause follows propositionally from a retained clause. Conversely every retained clause already existed in the original system. Thus the two CNFs are equivalent **over the original dictionary variables**, without applying a mere heuristic or an unvalidated physical symmetry.

## Independent integer optimization result: apparent k=34 optimum

On the locally restored source-checked `physical.json` from the original [CP-SAT full Rubik independent HTM replay](https://github.com/WhoSia/CUBE-REV/actions/runs/37948949764), an independent SciPy 1.17 / HiGHS integer set-cover court constructed the 398 irredundant rows and all 1,323 unchanged candidates. The solver returned:

```
LP relaxation optimum = 23.8
MIP status             = 0 (Optimization terminated successfully)
MIP objective          = 34.0
MIP dual bound         = 34.0
MIP gap                = 0.0
Elapsed                ≈ 9.88 seconds
```

**Mathematical evidence tier:** an independent optimizer declares an exact integer optimum of **34**, consistent with the separately actual-HTM-replayed physical 34-word upper witness. This is powerful supporting computation; it is **NOT YET an independently checked portable UNSAT certificate for k≤33**. The exact public theorem will not be promoted to `M*=34` in the canonical result header until the proof-producing SAT run and external DRUP checker PASS. At present the independently proof-checked established interval remains **30≤M*≤34**.

The fractional LP value 23.8 is NOT a sharp lower bound for k33: a large integrality gap persists. Integer-optimization optimal status is not itself a human-checkable logical proof of absence of 33, though the compressed exact instance should make proof generation significantly cheaper.

## New portable k33 court

[Exact-rowcore k33 solver source](../../scripts/cuberev-018/solve-rowcore-k33.py) reads the original real-cube physical instance and the implication certificate. It independently verifies all **1,192** row implications and that retained rows form an antichain. Only after this check does it generate the 398 original coverage clauses plus **unweighted at-most-33** sequential-counter cardinality constraints for ALL 1,323 physical maximal word representatives.

[Read-only GitHub Actions workflow](../../.github/workflows/cuberev-018-rowcore-k33.yml) performs:

1. Rebuild from the actual 18 legal HTM sticker-derived cube transitions (104,976 literal four-move words), check 1,913 partitions and 1,323 maximal cover masks.
2. Rebuild an exact proof certificate of all 1,192→398 row-support implications.
3. Encode the now *provably equivalent* 398-row original k33 CNF with no dual-weight/heavy/positive-word cuts.
4. If SAT: save actual selected four-turn words; independently replay on all original 1,192 physical source sets.
5. If UNSAT: save CNF and DRUP; require the separately pinned [drat-trim](https://github.com/marijnheule/drat-trim) to report `s VERIFIED` on the exact generated CNF. Only then may the previous k29 lower bound improve to k33 UNSAT → **M*≥34**.
6. If UNKNOWN/time budget exceeded: retain an auditable non-result. Never label a solver timeout an UNSAT proof.

**Evidential ceiling:** even a kernel-checked SAT proof of the matrix does not formally certify all physical sticker-cube states under Lean; semantic correspondence of the source-to-CNF generator remains its own separate proof obligation. The previous P6 D/D' direction discrepancy is retained as the cautionary counterexample.

## Research significance / publication standard

The 1,192→398 reduction is an elementary monotonicity argument applied to a nontrivial, fully enumerated **Rubik-specific physical incidence geometry**. It is **not claimed as a new universal theorem for automata**. Publishable value comes from a precise physical observation contract, reproducible structural classification of the row-support antichain, a verifiable optimality gap closure at k33, the reverse semantics bridge (including face-turn conventions), and comparison to existing preset distinguishing/homing sequence, test-design, and exact set-cover certification work. Paper drafting follows actual external proof receipt, not excitement about an optimizer's reported optimum.

**Current status:** `0.18_OPEN / CUBE_MSTAR_INTERVAL_30_34_PROOF_CHECKED / ROW_CORE_398_EQUIVALENCE_EXACT / HIGHS_OPTIMAL34_SOLVER_RECEIPT / K33_INDEPENDENT_DRUP_PENDING`.

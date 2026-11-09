# CUBE-REV 0.28 — R14-P7.2: T-tree one-step failure, a 12-state witness, and exact repair by a simpler tie-break

**Date:** 2026-11-09. **Status:** Complete finite 495-case classification based on independently verified R14-P7.1 exact AND–OR receipt, 48 color-graph automorphism orbit census, three locally recomputed exact Bellman branch proofs, and a new independent 47,520-state policy replay. **No claim that a two-step strategy is necessary.** Full physical P48 global adaptive minimum remains **18 ≤ h_adaptive ≤ 21**, unsolved.

## A. Conditional model and strategies

Choose four distinct edge types from the twelve legal edge colors, the edge set of `K_{2,2,2}` (six face colors, three opposite pairs `UD`, `RL`, `FB`). Assume the residual four-piece permutation parity and total edge flip parity have already been fixed. In the explicitly calculated even-even reference case there are `4!/2 * 2^3 = 96` oriented legal states, and eight spatial sticker-coordinate queries.

For belief `B`, let `B_(q,c)` be each nonempty color-response child; set

```
M(B,q) = max_c |B_(q,c)|,
K(B,q) = |{c : B_(q,c) != empty}|,
S(B,q) = sum_c |B_(q,c)|^2.
```

Three online deterministic strategies under test:

1. **Original one-step**: choose lexicographic minimum `(M,S,q)`.
2. **Two-step P7.1**: choose lexicographic minimum `(max_c min_{q'} max_d |B_(q,c,q',d)|, M,S,q)`.
3. **Simpler one-step P7.2**: choose lexicographic minimum `(M,K,S,q)`, **preferring fewer distinct color outcomes** when the worst immediate candidate cell is tied.

A fourth falsification control `(M,-K,S,q)` chooses *more* outcomes under the same first criterion.

**Crucial:** These algorithms apply to *actual observed colors* through exact deterministic partitions of all 96 legal assignments; there is no uniform input distribution assumption or probability claim. Neither parity-oracle residual model nor its decision tree is the original two-probe 12E/8C physical task.

## B. A finite exact graph characterization of the old one-step regret

Let `H_L` be the unordered four-edge subgraph of `K_{2,2,2}` induced by source label set `L` and let `deg(H_L)` list the degrees of its nonisolated color vertices, in decreasing order. The independently verified prior 495-row exact-AND–OR receipt and an independent 48-element graph automorphism audit establish the **finite, fully quantified statement**

```
D_original_one_step(L) > D_exact(L)
           iff deg(H_L) = (3,2,1,1,1).
```

Thus the failures are precisely the **four-edge T trees**: a three-edge star with a fourth edge attached to one leaf and ending at a previously absent color vertex. All remaining four-edge graphs have zero original-one-step regret. The 495 label sets split into 18 orbits under the full 48 automorphisms of the *color graph*. Three and only three whole orbits have one-read regret, of cardinalities `24`, `48`, `48`. Note that the 48 **abstract face-color graph automorphisms** classify edge-type subsets; they are **not** all physical Rubik spatial move symmetries (especially not automatic physical corner chirality automorphisms).

The graph characterization has an independent combinatorial count, without relying on the 495-row labels. Pick the unique degree-3 center (6 possibilities), three of its four neighbors (4 possibilities), and a pendant edge from one of the three selected neighbors to a **new** color vertex. Every 3-of-4 neighbor choice has precisely five such pendant edges: two from each of the two neighbors in the opposite pair, one from the third neighbor. Consequently there are `6 * 4 * 5 = 120` distinct T graphs, and the unique degree-3 center prevents double counting.

The finite classification and the count both pass an independent checker that directly constructs **every one of the 120** T-shaped four-edge subsets, comparing those sets to the receipt's 120 one-step failures. This proves the *defined policy's* finite criterion; it is not a theorem about every possible tie-break or greedy variant.

## C. Local 12-state branch witness explains WHY

In each of three T-tree orbit representatives, exhaustive exact 96-state Bellman search shows the root observation is **not** necessarily the point of failure: every initial slot is optimal. Instead a reachable two-query history produces a **12-state belief**. In representative `L = {BL,BR,DB,DF}`, the history reads spatial sticker slot 0 as `B` and slot 2 as `B`.

The original one-step policy first minimizes maximum child size and then sum-of-squares, and at this 12-state belief it chooses slot 4:

```
slot 4 : nonempty child populations [3,4,3,1,1]
         M=4, S=36, remaining exact action depth=3
```

The competing query slot 1 instead yields:

```
slot 1 : nonempty child populations [4,4,4]
         M=4, S=48, remaining exact action depth=2.
```

The 4-state color-`D` child of the bad `slot 4` query consists of these **four explicit legal even-parity/even-flip words** (facelets in spatial order):

```
BLBRDBDF
BLBDDFRB
BRBLDFDB
BDBRDFLB
```

Of the eight available next individual facelet queries, **none** assigns four pairwise distinct colors to these four words. Therefore that branch **cannot be resolved in one read**. In contrast, *each* of the three 4-state children of the competing `slot 1` query can be fully separated by a single subsequent facelet query. The structural reason is the possible *future partition geometry*, not the immediate maximum candidate population or the sum of squared cell sizes.

The three representatives have the same local failure pattern (two observations, twelve candidates, `M=4` tie, original `S=36` preference, but exact `3` remaining against exact `2` for the alternative). Their original actual 96-state Bellman values and literal four-word lower certificates are regenerated by an independent small solver in `audit_r14_p72_t_tree_theorem.py`. The independent checker separately reconstructs actual legal states and full outcome buckets to validate all three witnesses, without importing the producer.

## D. **Falsification of the claim that two-step lookahead is necessary**

The additional one-step tie-break `(M,K,S,q)` uses **no two-step tree search**. A fresh all-495 computation shows:

| Policy | Worst depths 3 / 4 / 5 | Exact regrets over 495 |
|---|---|---|
| Exact full AND–OR minimum | 72 / 369 / 54 | N/A |
| Original `(M,S,q)` | 72 / 249 / 174 | `0:375`, `1:120` |
| Two-step P7.1 | 72 / 369 / 54 | `0:495` |
| **New one-step `(M,K,S,q)`** | **72 / 369 / 54** | **`0:495`** |
| Reversed one-step `(M,-K,S,q)` | 72 / 249 / 174 | `0:375`, `1:120` |

**This is a scientifically consequential correction.** The two-step result remains correct, but a simpler one-step tie-break also realizes the full 495-case optimum. It would be false to claim that two-step anticipation is required for these four-edge residuals. The proposed general explanation is not that 'fewer outcomes is universally better', but that the T-tree's ambiguous 4-state residual is avoidable when, at equal worst-child population, the policy favors the coarser-looking **three equal four-state cells that are individually one-probe separable**.

An **independent direct-frozenset, per-hidden-state policy replayer** (not using the original bitmask producer) reconstructs all 495 legal four-label state spaces, recomputes the new one-step rule, and identifies each of all **495×96=47,520** target states, within exact AND–OR depth, zero mismatches. This establishes algorithmic equivalence for the specified finite set, **not** for arbitrary beliefs or all possible tie-break rules.

The same new one-step tie-break was further stress-tested on **two named known hard** five- and six-edge residual sets, yielding worst depths **7 and 9**, respectively, with all 960 and 11,520 initial states decoded. The preexisting exact minima 7 and 9 are imported from prior R14 restricted-court proofs. A result on those **two examples** does not establish the rule for every set of 5 or 6 edge types.

## E. Reproducibility and proof dependencies

- Dependency: verified P7.1 495-row `R14_P7_ALL_495_LOOKAHEAD_RESULTS.json`, containing separately computed exact AND–OR minimax, one-step, and two-step depths. The 495-case graph classification does **not** recompute all these minima from scratch; the existing independent checker `verify_r14_p7_lookahead.py` supplies that proof gate.
- `audit_r14_p72_t_tree_theorem.py`: 48 automorphisms, 18 orbits, exact T iff failure, 120 count, three 12-state local exact Bellman witnesses.
- `verify_r14_p72_t_tree_theorem.py`: independent graph construction, 120-label enumeration, literal reproduction of all 3 local 12-state branches.
- `audit_r14_p72_alternate_tiebreak_all_495.py`: direct bitset 495-case alternative one-step policies.
- `verify_r14_p72_alternate_tiebreak.py`: independent direct frozenset 47,520 individual starting-state replay of the new one-step policy.
- `audit_r14_p72_five_six_fewest_branch_stress.py`: two deliberately limited 5-/6-edge stress cases.
- Raw complete JSON proofs: `R14_P72_T_TREE_EXACT_REGRET_RECEIPT.json`, `R14_P72_ALL_495_TIEBREAK_RESULTS.json`, `R14_P72_5_6_FEWEST_BRANCH_STRESS.json`.

## F. Actual next research gate

**Seek counterexamples for other residual sizes and full mixed-prefix beliefs before suggesting general optimality.** The finite graph criterion depends on exactly four available distinct type labels, known parity, and a particular strategy. Even an always-optimal four-edge one-step tie-break does not imply an optimal 20-frame two-color physical Rubik policy. The separate edge and corner posterior parity factors and online choice of partial versus complete cubie measurements remain the central unsolved step. A genuine theorem of broader interest would explain when an immediate minimax cardinality tie-break using branch-count structure must preserve future optimal depth, or exhibit its exact failure conditions in the next harder family.

**No submission or originality priority claim.** The underlying group-action, decision-tree and certificate-complexity vocabulary is classical. The current result is a domain-specific exact computational structural characterization with an explicit falsification/erratum and a checkable tiny witness.

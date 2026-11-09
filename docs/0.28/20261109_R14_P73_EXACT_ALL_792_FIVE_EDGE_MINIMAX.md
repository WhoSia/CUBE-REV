# CUBE-REV 0.28 — R14-P7.3: Complete exact adaptive minimax of all 792 parity-conditioned five-edge residuals

**Date:** 2026-11-09. **Status:** Exhaustive direct full AND–OR lower bound on all 792 distinct actual Rubik five-edge source-type sets; full dynamic policy decoding on all 792×960=760,320 starting assignments; independent exact reanalysis under a different state representation on every one of 24 source-color graph symmetry orbit representatives. **Conditional edge-only theorem, NOT full P48 20-frame identification.**

## 1. Precisely defined domain

Let

```
TYPES = {UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR}
```

be the twelve distinct original edge cubie types. For each five-type subset `L ⊂ TYPES`, choose five labeled spatial edge positions and condition on a known permutation parity and total edge-flip parity. The explicit court uses parity-even/permutation-even orientation-even; the other three fixed-bit choices are isomorphic by signed spatial position coordinate changes. This is an **oracle-conditioned residual edge-only problem** arising naturally after prior full measurements, not an independent policy for the coupled corner/edge game.

A state is a bijection of five source edge types to five spatial slots, with one flip bit at each slot, subject to parity constraints. Each of the ten available queries reads exactly one physical six-color facelet value from one of these five spatial edge positions. The parity-even/flip-even state set has

\[
|X_L|=\frac{5!}{2}2^{5-1}=\boxed{960}.
\]

There are exactly

\[
\binom{12}{5}=\boxed{792}
\]

different five-type sets `L`, all explicitly evaluated in the primary producer.

## 2. Strategy and exact Bellman criterion

For a nonempty belief `B` and available read slot `q`, let `B_(q,c)` denote the nonempty candidates left after reading color `c`. Put

```
M(B,q) = max_c |B_(q,c)|
K(B,q) = number of nonempty color branches
S(B,q) = sum_c |B_(q,c)|^2.
```

The new R14-P7.2 **one-step** rule is

```
πfew(B) = argmin_q ( M(B,q), K(B,q), S(B,q), q )
```

with exact deterministic tie breaks. Its full worst-case decision-tree depth `Dfew(L)` is calculated through recursive partitioning, **not** from its local tuple score. Independently the R14-P7.1 two-step-max-leaf rule `π2` is run on each of the same 792 complete finite games.

The *true exact* minimax `D*(L)` is certified by the complete AND–OR feasibility recursion

\[
\operatorname{Win}(B,k)=\big(|B|=1\big)\;\lor\;
\bigvee_{q\in Q}\bigwedge_{c:B_{q,c}\ne\varnothing}
\operatorname{Win}(B_{q,c},k-1),
\]

with `Win(B,0)=false` for nonsingleton beliefs. For every one of the 792 sets the new producer does BOTH:

1. Construct the entire deterministic `πfew` policy and show it identifies every state within `Dfew(L)` queries.
2. Compute exact `Win(X_L,Dfew(L)-1)=false` by direct exhaustive AND–OR recursion over the actual 960 complete states.

A fully materialized source-state decoder walks all leaves **for each of 960 hidden starting states in each of all 792 games**, independently checking that the surviving belief is the **correct singleton**, for a total of **760,320** complete state replays.

Thus the policy supplies an upper bound and the AND–OR impossibility calculation supplies the matching lower bound; `D*=Dfew` on every one of the 792 sets. No assumption that a greedy policy *should* be optimal was used to infer a lower bound.

## 3. Complete finite classification

| Exact worst-case observations | Number of five-type sets | New simple one-step policy | Two-step max-leaf policy |
|---|---:|---:|---:|
| **5** | **12** | 5 | 5 |
| **6** | **672** | 6 | 6 |
| **7** | **108** | 7 | 7 |
| **Total** | **792** | **exact on all 792** | **exact on all 792** |

Consequently, in this exact finite model,

\[
\boxed{\forall L\in\binom{TYPES}{5},\quad D^*(L)=D_{\pi_{few}}(L)=D_{\pi_2}(L)}.
\]

This extends the all-495 known-parity four-edge result to the full five-edge family and upgrades P7.1's prior **two hard sample** results to a complete **792-case** classification. The worse five-type sets require seven residual edge facelet observations even with an oracle giving parity beforehand. This is a **restricted residual theorem**; it is not a full-cube 21-frame lower bound or 20-frame upper policy.

## 4. Independent representation / orbit verification

A fresh *independent verifier* reconstructs five-edge legal states by lists and `frozenset` belief partitions, without importing the bitmask producer. It enumerates **all 48 face-color graph automorphisms** preserving the opposite pairs `UD,RL,FB`, and partitions the 792 source five-type sets into **24 automorphism orbits**, with orbit-size histogram:

- 12 orbits of size 24;
- 10 orbits of size 48;
- 2 orbits of size 12.

For **all 24 actual representative label sets** it independently performs the full exact negative `Win(X_L,D-1)=false`, constructs the simple one-step `πfew` policy and directly replays **960 hidden target states per representative**, 24×960=**23,040** target replays. The orbit-wise depth histogram expands to exactly `5:12, 6:672, 7:108`. The independent verifier does not use the producer's bitmasks, its local choice helper, nor its Bellman memoization; it **does** read the previous 792-row receipt to know the proposed `D` to falsify.

The 48 graph automorphisms are a statement about the edge-only **source color graph**, not about all realizable 48-facelet **full physical** transformations with corner chirality. Within the edge-only known-parity conditional model, permutations of source color names preserve the color-partition decision game up to relabeling; a changed parity convention can be compensated by a spatial coordinate exchange. The full 792-case producer directly verifies every label set and therefore does not require accepting an unverified physical full-cube symmetry extension.

## 5. Scientific importance and negative controls

1. The P7.2 statement that the `(M,K,S,q)` one-step rule is optimal on all 495 four-edge games is extended to all **792 five-edge** games.
2. The more complex two-step lookahead remains optimal on all 792; however it is **not necessary**: the simpler one-step tie-break attains the same exact depth.
3. The 120 previous four-edge `(M,S,q)` failures are genuinely **policy-specific** and precisely the T-tree subgraphs. They do **not** imply inherent extra difficulty for those input sets.
4. All 792 five-edge scenarios use **known** permutation and flip parities, so the result does not resolve arbitrary partially observed edge beliefs, the simultaneous corner response, or the unknown-parity full physical cube.
5. It remains **OPEN** whether the `(M,K,S,q)` one-step rule is exact for every six-edge type set, for arbitrary partial observation histories, or for the original coupled two-probe Rubik state identification problem.
6. Generic decision-tree theory, symmetry groups, and greedy tie-break principles are prior mathematics. The novelty priority of this case-specific exhaustive finite theorem requires an explicit literature search, not a presumption of originality.

## 6. Reproducible sources, output, and promotion gates

- `search_r14_p73_five_edge_counterexample.py`: deterministic entire 792-set exploratory upper-policy comparison, one-step `πfew` versus two-step `π2`; all outcomes equal.
- `R14_P73_ANYTIME_FIVE_EDGE_SEARCH.json`: entire 792-row exploratory upper-policy census.
- `audit_r14_p73_all_792_five_edge_exact.py`: primary full 792-group exact AND–OR lower-proof AND complete 760,320 hidden-state policy replay.
- `R14_P73_ALL_792_EXACT_MINIMAX_RECEIPT.json`: full machine-readable proof receipt with exact budgets, state counts, policy results and checker memoization sizes.
- `verify_r14_p73_24_orbit_independent_exact.py`: independent all-24-orbit full exact Bellman negative test with 23,040 direct frozenset decoder replays.
- `R14_P73_INDEPENDENT_24_ORBIT_RECEIPT.json`: independent verification receipt.

**Scientific next step:** Before overgeneralizing to six-edge sets, actively seek a counterexample in all `C(12,6)=924` source edge type sets and compare against exact lower bounds for representatives. Most importantly, connect any residual oracle-only strategy to actual full P48 **mixed** partial-color beliefs with matched corner/edge permutation parity and real, not abstract, source facelet orientation. The global interval **18≤h_adaptive≤21 remains unresolved**.

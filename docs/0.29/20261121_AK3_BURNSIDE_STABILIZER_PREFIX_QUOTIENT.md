# AK3 — Burnside's lemma and the ten signed-cycle classes of the cube edge-color graph

**CUBE-REV 0.29 · 2026-11-21.** A structural replacement for repeated full-state enumeration. AK2 proved that the support set `X` of eleven observed first-color *count vectors* is the Hall-feasible set of the edge graph `K_{2,2,2}`. This document proves that its color relabeling automorphism group has ten conjugacy types and that the exact 52-representative count follows from a small fixed-point table.

## Automorphism group and action

The six color vertices split into the three opposite-color pairs `P_1={U,D}, P_2={R,L}, P_3={F,B}`. Every color-graph automorphism is uniquely described by (a) a permutation of these three pairs and (b) an independent swap/no-swap within each of the three source pairs. Hence

```text
G = Aut(K_{2,2,2}) ≅ (C₂)^3 ⋊ S₃,      |G| = 2³·3! = 48.
```

The action on count vectors is `(g·n)(v)=n(g^{-1}v)`. The Hall inequality is invariant under this action because a graph automorphism bijects the sets of edges incident to `S` and `gS`. Thus `g·X=X`, which justifies taking a quotient. Notice that the action is a bookkeeping symmetry of the initial edge-color observation problem; it does not assert that all 48 maps are physical rotations of the fixed-center cube.

## Signed cycle type

A group element acts on the **three opposite-color pairs** as a permutation `τ∈S₃`. For each cycle of `τ`, take its length and the XOR (0/1) of the internal pair swaps around that cycle. The multiset of these signed lengths is invariant under conjugation in the wreath product. There are ten types for three pairs (the bipartitions of three).

The independently reproduced Hall/Burnside audit produced:

| Signed pair-cycle type: (length, swap XOR) | Elements in class | Fixed Hall-feasible count vectors per element | Contribution to Burnside sum |
|---|---:|---:|---:|
| (1+,1+,1+) | 1 | 1,362 | 1,362 |
| (1+,1+,1−) | 3 | 252 | 756 |
| (1+,1−,1−) | 3 | 46 | 138 |
| (1+,2+) | 6 | 34 | 204 |
| (1+,2−) | 6 | 6 | 36 |
| (1−,1−,1−) | 1 | 0 | 0 |
| (1−,2+) | 6 | 0 | 0 |
| (1−,2−) | 6 | 0 | 0 |
| (3+) | 8 | 0 | 0 |
| (3−) | 8 | 0 | 0 |
| **Total** | **48** | — | **2,496** |

Here `+` indicates even swap parity in that pair cycle and `−` odd parity. The fixed-point numbers are the exact outputs of the Hall-feasible inequality test, with each type checked against **every element of its own conjugacy class**; a separate omitted-edge orientation DP verifies the same support set. The finite numerical entries are computer-verified, not all separately derived as closed-form symbolic identities.

By Burnside's orbit-counting lemma,

```text
#(X/G) = (1/48) Σ_{g∈G} |Fix_X(g)| = 2496/48 = 52.
```

This explains the 52 representative *histograms* from a 10-row conjugacy-class computation rather than a hidden enumeration over all 12-piece permutations or the decision trees' 144,736 candidate assignments.

## Stabilizer audit and tie-breaking hazard

Let `G_n={g∈G:g·n=n}`. The orbit-stabilizer theorem `|G·n|=48/|G_n|` produces:

| Stabilizer order | Orbit size | Number of representative orbits | Contributing count vectors |
|---:|---:|---:|---:|
| 8 | 6 | 3 | 18 |
| 4 | 12 | 10 | 120 |
| 2 | 24 | 27 | 648 |
| 1 | 48 | 12 | 576 |
| **Total** | — | **52** | **1,362** |

An essential mathematical caveat arises: **40 of the 52 representatives have nontrivial stabilizers** (52−12). Therefore a canonical representative histogram generally admits more than one color normalization `g`. It is not sound to discard the selected `g` after choosing the representative and then treat its policy as if equivariance followed automatically.

A safe implementation must either:
1. choose a deterministic explicit normalization (for instance the first admissible `g` in one frozen enumerated order), retain its inverse and the resulting parity character, then prove every chosen branch; or
2. prove the representative policy is equivariant under the full stabilizer of its histogram, including address selection, response relabeling and terminal parity.

The first route aligns with the existing frozen Python `route_info`; the second might simplify the certificate DAG after a separate graph-bisimulation proof. In neither route may a symmetry map be chosen by inspecting future, unobserved colors.

## Methodological and novelty boundary

McKay–Piperno's *Practical Graph Isomorphism, II* treats stabilizer-orbit pruning and canonical labeling for graph isomorphism, and Cameron's *Permutation Groups* supplies group actions and wreath products. These standard techniques motivate this derivation but do not independently certify the Rubik 18/19-frame adaptive identification problem. The new graph representation is a proposed structural explanation of the *existing* 52-policy quotient, not a claim to originality of Burnside's lemma.

**Executable:** `scripts/cuberev-observation/audit_r029_hall_burnside_graph_quotient.py` (stdlib only). The output includes the exact ten-class table, orbit sizes, stabilizers, a second dynamic-programming support check, and negative controls. These are independent evidence, not a Lean kernel proof of the full 19-frame policy.

# CUBE-REV 0.28 R8 — Uniform Local Edge-Color Certificate Complexity Versus Adaptive Identification

**Date:** 2026-11-05. **Scientific status:** exact finite-combinatorial census, structural group-equivariance argument, independent P48 Python regression, and a separate universal adaptive Hall lower bound from R7. Source CI must be checked independently before marking remote PASS.

## 1. The important problem is still the full adaptive Rubik identification problem

The original CUBE-REV question concerns what an embodied observer can recover from a reversible physical world using observation, action, memory and representation. We must not replace that hard question with an easier one simply because it admits a finite paper. The true target stays the exact adaptive six-color horizon in the physical full legal Rubik group, currently `18 <= h_adaptive <= 21`, while the nonadaptive horizon is exactly 21. This R8 result uncovers a **structural difference between state-specific evidence and executable identification policies**, not an adaptive 17-frame solution.

## 2. Precise model and theorem

Take the standard 3x3 fixed-center legal Rubik group. Each of the 12 unique edge cubies has two original colored stickers, making 24 physical edge-facelet slots. A physical single-facelet query reveals one of six fixed face colors. We grant the decoder, for free, the **complete actual corner state** `kappa` (including corner positions and orientations). Its edge observations may query arbitrary initial spatial edge slots; there is no action-cost restriction for this certificate problem.

For a legal full state `g`, define its *local edge certificate number*

```
C_edge(g | kappa)
 = min{|S| : S is a subset of the 24 initial edge-facelet slots
              and any legal h with corners(h)=kappa
              and colors_h(s)=colors_g(s) for every s in S
              necessarily has h=g}.
```

The set `S` **may depend on the true state g**. This is a nondeterministic/instance-specific identification certificate, not a procedure a sensor can select without knowing g.

**R8 theorem (exact uniform local certificate threshold).**

```
For every legal Rubik full state g with its complete corners granted:
     C_edge(g | corners(g)) = 17.

For every such g exactly 14,664 different 17-slot query sets S
uniquely certify g among the 12! * 2^10 corner-compatible edge states.
```

The word *uniform* here means the numerical local certificate complexity and its count are constant for every legal state, **NOT** that one universal set of 17 slots works for all states. The latter is false because nonadaptive full-group identification requires 21 frames even with full corners.

## 3. Canonical solved-state finite classification

Fix the completely solved true state and its complete corners. Consider every mask `M` of edge facelets that are **not** read. For any edge position with both stickers read, its original edge cubie type and flip are uniquely determined because all twelve possible edge-color pairs are distinct. Therefore all alternative edge hypotheses must rearrange only the remaining labels among edge positions that have at least one unread sticker.

Enumerate a bijection between remaining edge labels and incomplete edge positions. For each candidate assignment, require:
- every actually read sticker color matches the solved state's sticker color;
- the edge permutation is **even** (fixed solved corners have even permutation parity);
- the total edge flip parity is even.

A fully unread edge position admits both flip orientations; if there are `u>=1` such positions and all read colors match, exactly `2^(u-1)` assignments of their flips obey the global even-flip condition. Otherwise the flips of partially read positions are forced by their observed sticker colors, and their sum must already be even. Count valid possibilities up to two; `1` means a valid certificate, `2+` means nonuniqueness.

The finite exhaustive census is:

| Unread edge facelets | Read facelets | Masks tested | Exactly unique | Nonunique |
| ---: | ---: | ---: | ---: | ---: |
| 4 | 20 | 10,626 | 9,426 | 1,200 |
| 5 | 19 | 42,504 | 26,400 | 16,104 |
| 6 | 18 | 134,596 | 36,184 | 98,412 |
| 7 | 17 | 346,104 | **14,664** | 331,440 |
| 8 | 16 | **735,471** | **0** | 735,471 |

Every mask has the solved state as at least one candidate. The complete 735,471-mask test establishes that **no 16-read set uniquely certifies solved**, and by monotonicity no shorter read set can. The positive 17-read count establishes the matching upper bound.

One explicit 17-read certificate for solved is the complement of these seven missing colored sticker slots:

```
UR:U UR:R UF:U UL:U UB:U DR:R DF:D
```

where `UR:U` denotes the U-color facelet at the original UR spatial edge position in the solved coordinate system. No seven-element set listed here is a global adaptive policy; these are the *omitted* slots of one state-specific certificate. The C++ output pins one such exact mask deterministically.

## 4. Proof that the result holds for every legal cube state

Let `g` and `h` be legal original-sticker-to-spatial-slot permutations having the **same complete corners**. Define the legal relative transformation

```
k = g^{-1} o h.
```

It has all corners solved (h and g coincide on every corner sticker), hence a legal even edge permutation and even edge flip parity. If `T` is any set of initial edge-facelet slots, then the edge color observed in state `h` at the transported slot `g(s)` equals the edge color observed in state `k` at slot `s`:

```
color_h(g(s)) = color_k(s)
```

because `k^{-1}=h^{-1} o g`; sticker colors are intrinsic to original sticker identities. Conversely `h=g o k` gives all corner-compatible h by ranging over the legal relative edge subgroup.

Thus the mapping `T -> g(T)` is a bijection between certificate masks for solved and certificate masks for `g`, preserving mask cardinality and the exact number of consistent alternatives. All legal cube states inherit the solved state's minimum **17** and its **14,664** valid 17-slot certificate masks. This is an exact proof by group equivariance, assuming standard legal-cube edge parity/flip characterization.

## 5. Why this does NOT settle the original adaptive problem

The R7 all-adaptive Hall-capacity theorem proves that even with full corners and unrealistically free access to any edge facelet position,

```
h_adaptive >= 18.
```

R8 establishes a strictly smaller state-specific certificate size:

```
max_g C_edge(g | corners(g)) = 17 < 18 <= h_adaptive.
```

There is no contradiction: a certificate can be selected **after knowing which g is true**, while a correct deterministic observation tree must choose its next query from only previous colors and work for **every** possible g.

The difference between certificate complexity and deterministic/adaptive decision tree complexity is an established area of theoretical computer science, not invented by CUBE-REV. Direct prior comparisons include Buhrman & de Wolf (2002), *Complexity Measures and Decision Tree Complexity: A Survey*, DOI `10.1016/S0304-3975(01)00144-X`, and Grossman, Komargodski & Naor (ITCS 2020), *Instance Complexity and Unlabeled Certificates in the Decision Tree Model*, DOI `10.4230/LIPIcs.ITCS.2020.56`. This work's potential novelty is the exact **Rubik physical six-color/permutation/flip constrained instance**, not the general concept.

Also distinguish physical **edge-only queries with a free full corner oracle** from the actual combined edge+corner probe policy. The constructed 17-slot certificate is NOT a full-cube 17-frame identification algorithm.

## 6. Audits and next hard mathematical directions

- [Exact C++ full omission-mask census](../../scripts/cuberev-observation/audit_r8_edge_state_certificates.cpp) exhaustively checks all masks with 4–8 omitted facelets, exact edge color identity, permutation parity and flip parity. It performs early stopping at two candidates to distinguish unique from ambiguous.
- [Independent Python P48 geometry cross-check](../../scripts/cuberev-observation/test_r8_edge_state_certificates.py) obtains edge stickers from the 3D-generated P48 physical model rather than hardcoded C++ piece names, reproduces the all-four and all-five omitted-mask results, and validates the explicit 17-slot witness.
- Read-only [physical observation CI](../../.github/workflows/cuberev-observation-generalization.yml) compiles C++, checks expected 735471 zero-singleton result, and auto-discovers the Python P48 unittest. Check the complete remote CI result before promoting to independent CI PASS.

The next non-avoidance question is **whether the 17-certificate to >=18-adaptive gap can be closed by a universal identifying decision tree of depth 18,19 or20**, while respecting the true two simultaneous color probes and no free resets. The lower-bound route needs to retain more than Hall-consistent pair types: edge permutations, flips and actual joint action geometry may remove still-more transcript branches.

Finally, the human reconstruction programme is not solved by any of these certificate counts. Actual 0.21 P4 records had zero comparable cross-source exact state/view/stage/previous-action pairs at the strict endpoint. A human history mechanism must be tested with independently supported matched behavior and explicit latent-goal/reconstructor controls; mathematical Rubik certificates do not measure cognition.

**Custody boundary:** GitHub source and semantic note, human author/committer only; P7 active allowlist updated; Notion is scientific semantic head and Drive holds irreplaceable sources. Source bytes, math induction, observed behavior and publication novelty are distinct authority claims.

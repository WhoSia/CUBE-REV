# CUBE-REV 0.28 R14-P5.2/P5.3 — Stronger Full-Cube Root Quotient and Exact Two-Frame Posterior Census

**Date:** 2026-11-06. **Status:** P48 48-facelet physical legality and observation-covariance theorem + exact parity-matching count table, LOCAL PASS. Exact full adaptive horizon still OPEN, 18<=h<=21.

## Critical correction to R14-P5.1

P5.1 classified 36 ordered first-probe color responses into three orbits under **whole rigid cube rotations**: same (6), opposite (6), adjacent (24). This is true, but **not the full observational automorphism group**. Treating those three as irreducible subproblems is unnecessarily weak.

The stronger P5.3 legal **source-cubie color-label** transformations show all **36 first responses belong to a SINGLE zero-error Bellman orbit**. The older three classes must remain labelled "orbits under the subgroup of 24 rigid spatial rotations", not the maximal root response quotient. No first-frame color pair can have a different optimal remaining observation depth from another in the unbounded known-turn model.

## The decisive two-sided symmetry

For physical hidden cube sticker permutation x (original->spatial), spatial slot query q, and solved-sticker color c0,

    O_q(x) = (c0(x^{-1}(q_edge)), c0(x^{-1}(q_corner))).

P5.1's left action x->g*x, q->g(q), normalizes all 576 root query locations to one. P5.3 adds **right source-label actions** x->x*h^{-1} with q unchanged.

Let r be a proper rigid rotation of the 3D cube and phi_r its permutation of the six face colors. Define h_E(r) as the 48-sticker permutation acting exactly as r on the 24 **original edge** stickers and fixing all original corner stickers; define h_C(r) similarly, acting on only original corner stickers.

The source-derived P48 legality invariants reveal that:
- all **24** proper rigid rotations restricted to corners yield legal h_C(r) with corner permutation even and zero total corner twist;
- exactly **12** of the 24 restrictions to edges are legal h_E(r), with even edge permutation and even total edge flip;
- the twelve legal edge rotations act **transitively** on all six face colors (two transformations sending U to each target face);
- the 24 legal corner rotations also act transitively on all six face colors (four sending U to each target face).

Thus the 12x24=288 independent products h_E*h_C are legal cube group states, and for any root output (a,b) and any desired (a',b') some such h sends the former to the latter. For any legal x and any spatial query q, direct sticker inversion yields

    O_q(x*h^{-1}) = (phi_edge(O_q(x).edge), phi_corner(O_q(x).corner)).

This is an exact bijection of **the full hidden-state space** preserving every future paired query, with an independent fixed color permutation for each sensor. Any adaptive zero-error policy is transported simply by interpreting each future observed edge and corner color through the inverse of these two known relabelings. It therefore preserves the complete Bellman recursion and terminal singleton predicate.

**Exact global equation:**

    h_adaptive = 1 + D(B_(q0,(U,U))),

where q0 is any fixed paired spatial facelet query, and B_(q0,(U,U)) is the posterior when both returned colors are U. The right side is **not evaluated**; the equation removes root choice and outcome duplication, not the 18–21 open bound.

The legal source-label group action is different from physical rotations of the whole cube during a probe. Right multiplication by a legal cubie permutation transforms the *candidate hidden initial state*, not the robot's current pose or probe location.

## Full physical two-frame exact branch counts (R14-P5.2)

For the fixed root query q0 and first responses representative of P5.1's classes, (U,U), (U,D), and (U,R), P5.2 independently converts actual 3D P48 original facelet source colors into the oriented cubie words used by the exact matching/parity dynamic program.

The pointwise stabilizer of q0 yields **12** orbit representatives of the possible second paired queries (P5.1, exact). This gives 3x12=36 explicitly computed first-response/second-action families. For each one, every one of 36 potential second-color outcomes is enumerated by exact parity-matching counts, and their totals are verified to equal the actual first-posterior size

    N1=|G|/36=1,201,444,535,402,496,000.

In all three first-response classes the 12 second-query outcome *cell-size profiles* coincide, consistent with stronger P5.3 source-color symmetry. The smallest largest posterior after the second query is

    N2_max=41,608,468,758,528,000,

achieved at one second-query orbit representative: read **another edge position** and **another corner position** (local slot-index representative [3,4], counting 0-based). That representative produces 36 nonempty second-color branches. This is an optimum for **one-step maximum surviving cardinality** among the 12 second-query orbits, not a verified optimum for the remaining full adaptive minimax depth. Do not claim it solves the 20-frame problem.

The 36-row exact P48 branch table is available as a preserved JSON receipt and can be used as an exact root-level branch-and-bound oracle.

## Evidence

P5.3 original Drive source:
https://drive.google.com/file/d/1rTpbmoUgDdpAvo8lK2dwMHnn3BBT_skT/view

P5.3 JSON independent local execution:
https://drive.google.com/file/d/1dfu1UHjxrgBOVxgCLmh3Mr8_9oZ35Ys3/view

Its independent physical test checks 601 actual legal P48 18-HTM word-prefix states, verifies 288 distinct legal right-relabeling transformations, and performs 31,104 explicit query-output covariance checks. The compact GitHub active checker may differ in source bytes but uses the same mathematical generators, legality tests, and expected result; raw Drive source is the original complete test.

P5.2 exact full-P48 posterior Python:
https://drive.google.com/file/d/1f-xjtvWE_vndNS0UA1bO1RRe_M9Wq4Nr/view

P5.2 full 36-row posterior table:
https://drive.google.com/file/d/1rRLg7-hXjLUm9iEEaWVL9AiFrhbTMsIV/view

GitHub:
- `scripts/cuberev-observation/audit_r14_p51_p48_group_lift.py`
- `scripts/cuberev-observation/audit_r14_p52_two_frame_p48_posteriors.py`
- `scripts/cuberev-observation/audit_r14_p53_source_label_automorphisms.py`

All components must be checked by read-only CI. Drive source/receipt hashes are a separate custody gate.

## Scientific priority

The group law and cubie legality are existing mathematics (e.g. the Fundamental Theorem of Cubology). The novelty candidate is a *specific, certified exact observation-automorphism quotient for the two-probe full legal cube model*, most valuable if it supports a new adaptive horizon theorem. Do not claim that the group invariants or general Bellman covariance principle are newly invented. Original h_adaptive remains 18..21 OPEN.

**Next decisive work:** After quotienting root query and root response to one canonical history, use the exact P48 partial-color matching oracle to traverse mixed early prefixes with state-set canonicalization; test whether any 20-frame policy can be constructed, or prove a universal adversarial obstruction without restricting to completely read cubie prefixes. Independently finish Paper A's radius-six manuscript and provenance gates instead of endlessly fragmenting the research into small numerical notes.

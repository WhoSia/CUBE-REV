# CUBE-REV 0.28 — R14-P8.1: A parity-correlation activation gate in mixed partial color observations

**Date:** 2026-11-09. **Evidence:** combinatorial involution proof; full twelve-edge/eight-corner matching DP; small exhaustive coupled decision-tree test; explicitly dependent P48 geometric regression. **Not** an optimal twenty-frame Rubik policy, new fixed-horizon theorem, or originality/priority claim.

## 1. Full physical question and the exact posterior algebra

For a legal 3×3×3 cube, define the spatial observation transcript \(H=(H_E,H_C)\), consisting of the literal observed colors at edge and corner facelet positions. Let \(E_p(H_E)\) count *oriented* assignments of all twelve original edge cubies compatible with edge observations, with even total edge flip, and permutation sign \(p\in\{0,1\}\). Let \(C_p(H_C)\) analogously count corner assignments with total corner twist zero modulo three, and permutation sign \(p\).

The *only cross-sector legality condition* is equality of permutation parity. Therefore

\[
N(H)=E_0C_0+E_1C_1
=\frac{E_\Sigma C_\Sigma+\Delta_E\Delta_C}{2},
\]

where \(E_\Sigma=E_0+E_1\), \(\Delta_E=E_0-E_1\), and analogously for corners. This is an exact rank-one interaction correction, not an approximation or an independence assumption.

## 2. Sign-reversing unseen-cubie involution (general lemma)

**Lemma.** If two different spatial edge positions are entirely absent from \(H_E\), then \(E_0(H_E)=E_1(H_E)\). The same statement holds for corners and \(C_0=C_1\).

**Proof.** Choose distinct unobserved positions \(a,b\). For every compatible assignment, exchange the full cubie identities at positions \(a,b\), **carrying their orientations with them**. All observed facelets lie outside \(\{a,b\}\), so they are unchanged. The multiset of orientations and its total modulo two (edges) or modulo three (corners) remain unchanged. Transposing two values in the position-to-source permutation changes its sign. The map is an involution with no fixed assignment, giving a bijection between the even- and odd-permutation completions. QED.

**Corollary (support gate).** Whenever either sector has two completely unread positions, one sector's parity imbalance vanishes and thus

\[
\boxed{N(H)=E_\Sigma(H_E)C_\Sigma(H_C)/2.}
\]

For a *nonzero parity interaction term* \(\Delta_E\Delta_C\), it is therefore necessary that the observation history has visited **at least 11 distinct spatial edge positions and at least seven distinct spatial corner positions**. These are **counts of touched cubie positions, not complete cubies, individual sticker reads, time steps, or sufficient conditions for the term to be nonzero**. No claim is made that a 20-frame policy must or must not visit them.

An additional exact interpretation: when at least one sector has two completely untouched cubie positions, the joint number of color-compatible legal full-cube states is half the unrestricted product \(E_\Sigma C_\Sigma\), and for **fixed predetermined spatial query sets** the probability of the two sector color-events under the uniform legal-group prior factorizes into edge-only and corner-only marginal event probabilities. In a fully adaptive experiment the selected query locations may themselves depend on colors returned by the other sensor, so cross-sector transcript independence must not be inferred. This **does not** say the hidden edge and corner assignments are independent; their permutation signs are always coupled. Likewise, factorized transcript probabilities do not eliminate possible information value from future adaptive paired queries.

## 3. Exact DP full-cube sanity checks

The new source enumerates matching completions by a used-source-label mask, running permutation parity, and orientation residue. For the solved-orientation reference readings, the exact full-prefix rows are:

| Fully observed spatial edge cubies | Fully observed spatial corner cubies | \((E_0,E_1)\) | \((C_0,C_1)\) | Legal joint completions |
|---:|---:|---:|---:|---:|
| 0 | 0 | (490,497,638,400; 490,497,638,400) | (44,089,920; 44,089,920) | 43,252,003,274,489,856,000 |
| 9 | 5 | (12; 12) | (27; 27) | 648 |
| 10 | 6 | (2; 2) | (3; 3) | 12 |
| 11 | 6 | (1; 0) | (3; 3) | 3 |
| 10 | 7 | (2; 2) | (1; 0) | 2 |
| 11 | 7 | (1; 0) | (1; 0) | 1 |

The program checks 48 additional arbitrary mixed, partially observed sector histories with at least two untouched cubies and verifies \(E_0=E_1\) or \(C_0=C_1\) exactly; it directly demonstrates 72 valid sign-flipping involution images per sector on different mixed prefixes. These checks are illustrative; the preceding involution proof is the general justification.

## 4. Explicit oracle-removal test in the last 2E+2C suffix

After observing all facelets on ten edge positions and six corner positions, a solved-reference full cube leaves exactly **twelve** jointly legal states, divided evenly into **six** even/even and **six** odd/odd states. The remaining original edge source labels are `(BL,BR)` and the remaining corner labels are `(DBL,DRB)` in the independent abstract cyclic convention. There are four possible spatial edge facelet queries and six possible spatial corner facelet queries, thus **24** independently selectable paired queries.

A fresh literal-state `frozenset` Bellman recursion yields **exact worst-case paired-query depth two** if parity has NOT been given. It computes the complete policy and decodes all twelve target states. Giving the true common parity for free splits the prior into two six-state beliefs, each with **exact worst-case depth one** for the same paired observation alphabet. This is a concrete strict value-of-parity-oracle counterexample to reusing the oracle-conditioned P7 residual depths directly, rather than a claim about the 20-frame full puzzle.

## 5. Physical P48 consistency, limitations, and next gate

`verify_r14_p8_p48_geometry.py` reuses the earlier independent-from-project 3D physical P48 cubie/facelet geometry engine `CUBEREV_028_R14_P51_P48_GROUP_LIFT.py` and its orientation-aware matching counter `CUBEREV_028_R14_P52_TWO_FRAME_P48_POSTERIORS.py`. On **30** scrambled 18-HTM-derived physical prefixes and three depths, a newly implemented matching DP agrees exactly with the archived DP. Its two-sector rank-one parity equation and unseen-position balancing conditions pass for all tested physical observations. Because it imports P5.1/P5.2, it is explicitly **not** a second independent physical coordinate derivation. The primary count DP uses a conventional abstract cyclic corner-word ordering, and complete full P48 validity still relies on the archived geometry proof.

**Scientifically useful result:** An exact, checkable structural **activation criterion** for the parity interaction term; a concrete small coupled decision-tree gap demonstrating that parity cannot be silently given by an oracle; a production-ready integer matching-count primitive with no full-cube state enumeration. The algebra/involution are elementary and may be known; no novelty priority is claimed.

**Next substantive experiment:** Form belief representations with two parity strata and full edge/corner local partial color constraints; compare a true parity-coupled joint lookahead with an incorrect oracle-conditioned policy on reachable mixed prefixes. Preserve the complete vector `(E0,E1,C0,C1)` and successor color partitions; neither scalar candidate count nor the vanishing interaction term alone is a sound Bellman quotient. The original **18 <= h_adaptive <= 21** remains unresolved.

## 6. Reproduction

Run from a checkout where the P5.1/P5.2 archived source modules can be loaded in the declared Python module path:

```bash
python audit_r14_p8_parity_activation.py
python verify_r14_p8_joint_suffix.py
python verify_r14_p8_p48_geometry.py
```

JSON receipts: `R14_P8_DELAYED_PARITY_ACTIVATION_RECEIPT.json`, `R14_P8_2E2C_COUPLED_SUFFIX_RECEIPT.json`, `R14_P8_P48_GEOMETRY_REGRESSION_RECEIPT.json`. The physical regression loads the repository-local P5.1/P5.2 named modules when present and falls back to the archival `/mnt/data` filenames for an offline reconstruction. This is an explicit dependency, not an independent P48 audit. All actual CI pass and repository custody assertions require independent remote confirmation.

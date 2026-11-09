# CUBE-REV 0.28 — R14-P8.2: Exact physical P48 mixed-prefix successor-color partitions

**2026-11-09 · Empirical finite certificate and parity-aware matching identity · NOT a global adaptive 20-frame solution.**

## Research question

Given an actual 3D-derived physical 48-moving-sticker geometry and a literal partial color history `H=(HE,HC)`, can we generate the *exact full 36-color successor partition* for every one of 24 edge × 24 corner spatial facelet query pairs without full legal-cube state enumeration, and independently verify a genuinely coupled hard suffix?

## Full conditional model and proof of branch conservation

For edge/corner orientation-preserving label-matching DP counts `(E0(HE),E1(HE))` and `(C0(HC),C1(HC))`, let

\[
J(H)=E_0(H_E)C_0(H_C)+E_1(H_E)C_1(H_C).
\]

For `q=(qe,qc)` and colors `y=(a,b)` compute the exact child

\[
J_{q,y}=E_0(H_E\cup\{(q_e,a)\})C_0(H_C\cup\{(q_c,b)\})+E_1(H_E\cup\{(q_e,a)\})C_1(H_C\cup\{(q_c,b)\}).
\]

These are **integers** including the matched permutation parity restriction and both orientation sums. Each state has exactly one color at each specified facelet, hence the disjoint union identity

\[
\sum_{a,b\in\{U,D,R,L,F,B\}}J_{q,(a,b)}=J(H)
\]

holds for every query, including queries repeating old slots. Crucially, this identity is verified on all 576 query pairs in each audited prefix, not merely assumed.

Sector counts can be cached separately: 24 edge slots × six colors and 24 corner slots × six colors are enough for **each** prefix to build all 576×36 joint counts by parity-wise products. This avoids 20,736 separately executed full matching DPs and does not erase sign-resolved information.

## Exact five-prefix finite census

| Literal physical color history | `J(H)` | Best possible one-step largest child | Best `q` in canonical local P5.1 numbering | Actions with any nonzero parity-correlation child |
|---|---:|---:|---|---:|
| No observations | 43,252,003,274,489,856,000 | 1,201,444,535,402,496,000 | (0,0) | 0 |
| One facelet on each of two different edge and corner positions | 29,255,954,595,840,000 | 1,213,580,338,790,400 | (4,6) | 0 |
| All stickers at first 10 edge positions and first 6 corner positions | 12 | 2 | (20,18) | 24 |
| All stickers at first 11 edge positions and first 7 corner positions | 1 | 1 | (0,0) | 576 |
| Just one facelet each at first 11 edge and 7 corner positions | 1,327,104 | 82,944 | (1,1) | 0 |

The query objective in the table is **only** minimum immediate largest child population. The test code breaks ties by fewest nonempty color outcomes, then sum squared child sizes, then local slot index; no exact future Bellman-depth optimality is inferred.

There are five prefixes × 576 queries = **2,880 exact branch-conservation tests**. Every query processes all 36 possible ordered color responses (some are incompatible). The latest partial prefix has already touched 11 edge and 7 corner cubie *positions*, satisfying P8.1's **necessary** support condition for nonzero `DeltaE*DeltaC`. Nevertheless the parity-correction term vanishes for all children of all 576 next queries in this particular prefix. **The support threshold is not sufficient** for a nonzero correction. In contrast, the 12-state fully read 10E/6C suffix has 24 actions whose child posterior parity correction is nonzero; both sectors can become sign-unbalanced from one new paired observation.

The fully read 11E/7C prefix is already singleton and included only as a count/covariance regression, not as an identification challenge.

## Independent literal 12-state verification

A different source file regenerates the integer lattice 48-sticker P5.1 coordinate ordering from scratch, reconstructs the twelve orientation-compatible **parity-matched** suffix assignments after ten fully observed edges and six fully observed corners, and groups all 12 actual literal-color state pairs by observation at every one of the **576** possible spatial paired facelet queries. It independently checks all 576 sorted child-count partitions against a SHA-256 digest emitted by the DP producer:

`1be8220e424192013fe87cdac4cc6079384ee51c5015bae161014d55ca45dd77`

Therefore this suffix check does **not** share the dynamic-programming implementation or import the producer's original physical geometry module. Its derivation nonetheless follows the same documented lattice ordering specification; it does not separately audit every legal 18-HTM move or routing word.

## What is established, and what is not

**Established:** exact parity-coupled one-step child cardinalities at every 24×24 P48 query for five specified, color-consistent histories; conservation for every query; independent literal 12-state check of every query partition; a concrete demonstration that touching the 11E/7C support boundary does not by itself activate parity imbalance.

**Not established:** that the tuple `(E0,E1,C0,C1)` is a sufficient belief-state canonicalization; that one-step cardinality greed produces a global optimal decision tree; that the abstract 48 source-color automorphisms extend to full physical corner chirality; any unrestricted full-cube depth-20 strategy or all-policy depth-21 lower proof. The original `18<=h_adaptive<=21` remains OPEN.

## Reproduce

From the same repository folder containing the P8.1 matching DP and P5.1 geometry module:

```bash
python audit_r14_p82_mixed_p48_successor_partition.py
python verify_r14_p82_12state_independent_suffix.py
```

The producer loads `audit_r14_p51_p48_group_lift.py` from its repository-local folder, with an explicitly declared `/mnt/data/CUBEREV_028_R14_P51_P48_GROUP_LIFT.py` fallback for archived local reproduction. The verifier does not import P5.1, P8.1 or the producer's DP; the only shared artifact is the producer's digest in the receipt.

Receipts: `R14_P82_MIXED_P48_SUCCESSOR_PARTITIONS_RECEIPT.json` and `R14_P82_INDEPENDENT_12STATE_RECEIPT.json`. Promote only with clean-checkout CI checks, SHA-256 verification of stored raw sources, and read-only CI permissions. GitHub Actions authorship remains prohibited for repository commits.

**Next R14-P8.3 gate:** choose two actually reachable mixed histories with identical scalar `J(H)` (and, if possible, identical four parity counts) but different sorted collections of 576 color-partition fingerprints; test whether physical query-group transport relates them before calling them nonisomorphic. Then implement a sound history-plus-action canonical Bellman interface instead of treating child-size histograms as full decision-tree states.

# CUBE-REV 0.28 — Exact single-erasure robustness of B6 original-cubie sensors

**Date:** 2026-11-04. **Status:** combinatorial classification conditional on the earlier, *original-physical* B6=16 and exactly 156 positive 16-tag layout certificate. This is **not** a new independent HTM proof of the archived positive-family criterion.

## Observational distinction

Let T be the twenty original 3×3 cubie tags: eight *oriented corner tags* and twelve *oriented edge tags*, measured by the physical object's position and orientation. Let B6 denote the eighteen-HTM word ball of radius six. For S⊆T let S be B6-valid iff the full-position-and-orientation observation map on B6 is injective.

A B6-valid set S is **one-erasure robust** if S\\{t} remains B6-valid **for every t∈S**. Write b6^(1) for the smallest robust |S|, and N19^(1) for the number of robust 19-tag sets.

## Theorem (single physical-cubie erasure)

Conditional on the prior physical certificate that every B6-valid sixteen-tag set omits exactly two **adjacent** original corners and exactly two original edges and that the complete sixteen-tag positive family is the geometrically specified 156 layouts,

**b6^(1)=19 and N19^(1)=12.**

The twelve robust 19-tag layouts are **exactly those omitting a single edge tag**, hence observe *all eight corners and eleven of the twelve edges*. No 18-tag layout is one-erasure robust, and no 19-tag layout omitting a corner is robust.

### Proof of lower bound and complete 19-tag shape restriction

Validity is monotone under **adding** sensors. Because b6=16, every valid 16-tag subset is among the 156 bases. A 17-tag set is valid iff its three missing tags can be extended to an allowed four-tag missing layout; similarly an 18-tag set is valid iff its two missing tags have such an extension.

Suppose an 18-tag candidate has two omitted corners. Deleting any other observed corner yields three omitted corners, impossible to extend to a positive four-tag missing layout (which always omits exactly two corners). If it instead omits two edges, deleting any other observed edge yields three omitted edges, likewise impossible. If the two absent tags comprise a corner c and edge e, deleting the *opposite cube corner* of c gives a 17-tag set missing two **nonadjacent** corner tags, which cannot extend to an allowed four-tag layout (every positive omitted corner pair must be adjacent). Hence **no 18-tag set is one-erasure robust**, without any complete 190-candidate search. Any one-erasure robust 17-tag or smaller design could be augmented to an 18-tag robust set (erasure robustness is upward monotone), so none exist.

For a 19-tag layout missing a corner c, erasing the opposite original corner again leaves a nonadjacent omitted pair and fails. Thus any robust 19-tag layout must miss an original **edge tag** only.

### Constructive upper bound and exact count

Choose one originally omitted edge e. To prove that observing the other 19 cubies is erasure-robust, it suffices to examine losing either (a) one other original edge f, or (b) one corner c. In each case we need a positive 16-tag sub-layout of the remaining 18 tags: equivalently the two omitted tags {e,f} or {e,c} must be included in some certified four-tag omitted set.

Two finite incidence coverage checks over the archived 12×13=156 geometric layouts yield:

- Every unordered pair of two original edge tags is included in at least one positive four-tag omission: **66/66**.
- Every ordered corner–edge pair (one of each) is included in at least one positive four-tag omission: **8×12=96/96**.

Therefore **all twelve** 19-tag sets omitting one edge are one-erasure robust. The previous shape argument excludes the eight 19-tag sets omitting one corner. QED.

The counts 66/66 and 96/96 are rechecked *directly*, without assuming them in the program, by the Python script below. The script also enumerates every set with 16–20 observed tags and yields number of one-erasure-robust layouts at each cardinality: 16:0, 17:0, 18:0, 19:12, 20:1.

## Reproducibility

- `scripts/cuberev-observation/audit_b6_one_erasure_robustness.py`: enumerates 156 positive omitted-tag sets by using `verify_b6_geometric_rule.py`; evaluates all one-tag erasures against existence of a certified 16-tag core, computes the 66/66 and 96/96 incidence coverage, and asserts all size counts.
- `scripts/cuberev-observation/test_b6_one_erasure_robustness.py`: five tests of all 12 edge omissions, all eight corner omissions, all 190 18-sensor sets, exact 16-tag family, and threshold.
- Existing independently authored geometric code checks 24 spatial rotations, 13 admissible omitted-edge pairs/core, and 156-node graph. The source of the four-case **physical** B6 validity is still the existing 41-goal HTM/MITM archived certificates; the present audit does not separately rederive HTM shortest distances.

## Literature and novelty

Hernando, Mora, Slater and Wood, *Fault-Tolerant Metric Dimension of Graphs* (2008) (available in Research OS 00 as HMSW-FaultTolerant.pdf, Drive 1qjgI5Jllteoog_RedYttju-zX7p6nDe4) introduces single-loss fault-tolerant **graph-distance** resolving sets. Their abstract and §1 define the single-loss rule, but their observed outputs are graph distances rather than the full location and orientation of original moving physical cubies. The one-erasure set-cover equivalence is elementary and should **not** be claimed as a new general mathematical principle. Boutin (preprint arXiv 0808.1427v1, Drive 1uQpaotOWnqEi6oTShp4WSHoy6B0B1IgD) already establishes exchange-property failures in graph determining and resolving sets, and explicitly distinguishes minimal (inclusion-minimal) versus minimum (minimum cardinality) designs. Our physical original-cubie exact instance is the only possible cube-specific contribution, subject to proof-independence and deeper novelty auditing.

## Next research gate

Reduce the finite coverage checks 66/66 and 96/96 to short geometric orbit lemmas, *then* move to independent 54-facelet and original 18-HTM distance certification of the inherited B6 positive family. Do not confuse this result with noisy/stochastic sensing, distance-landmark robustness or adaptive observation.

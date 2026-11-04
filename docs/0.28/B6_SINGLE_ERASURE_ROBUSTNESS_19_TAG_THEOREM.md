# CUBE-REV 0.28 — One-erasure B6 original-cubie sensors: rigorous 18–19 bound

**2026-11-04 CORRECTED audit.** The earlier draft of this note incorrectly asserted b6^(1)=19 by assuming every B6-valid 17/18/19-tag design necessarily contains a B6-valid sixteen-tag subset. **That implication is false for general monotone sensor predicates**. This file preserves the correction prominently rather than hiding the earlier error. No new physical HTM distance claims are made.

## Definition and existing input

Twenty original physical cubie tags (eight corners, twelve edges) each report that *specific original object's* full position and orientation. A tag set S is B6-valid if it separates all legal 18-HTM radius-six cube states. It is **one-erasure robust** if for every selected tag t∈S, the set S\\{t} is B6-valid. Let b6^(1) be minimum cardinality of such a set.

Inherited archived physical B6 classification: b6=16 and **all** B6-positive 16-tag sets are exactly 156 layouts. Each of these omits two *adjacent* corners and two edges subject to the four-case geometric rule. This physical positive-family classification still needs fully separately implemented original HTM verification.

## Theorem — rigorously proved bounds and construction

**18 ≤ b6^(1) ≤ 19**, with at least **12 independently enumerated, certifiably robust 19-tag layouts**: all eight corners and all but any one edge.

### Why 17 is impossible — a valid exact deduction

Suppose a 17-tag one-erasure robust set S exists. Then erasing *any* of its 17 selected tags leaves a B6-valid **16-tag** set, necessarily one of the 156 existing bases. So for any erased original corner tag, the 4 total missing tags must contain two corners and two edges; the same must hold on erasing any observed original edge tag. But S contains both corner tags (at least five) and edge tags (at least nine). These two erasures demand contradictory missing-tag type counts. Therefore no 17-tag set is robust. By upward monotonicity of erasure robustness no smaller set can work.

### Constructive 19-tag sufficient certificate

Let e be any one original edge tag, and observe the other 19 tags. Erasing one additional edge f leaves two missing edges, which can be extended to a **positive 16-tag** missing four-tag layout for each unordered edge pair: coverage **66/66**. Erasing any original corner c leaves missing tags {e,c}, and each such pair extends to a positive four-tag layout: coverage **96/96**. By monotonicity, all 18-tag erasure residues are B6-valid. Thus each of the 12 choices of omitted original edge produces an authentic one-erasure robust 19-tag design. This is proved conditionally on the archived B6 positive-family correctness and needs no assumption about larger minimal bases.

### What the finite 156-layout core audit does NOT prove

An 18-tag set could be B6-valid even if it has **no valid 16-tag subset**. To decide robustness of an 18-tag set, one needs to determine actual B6 validity of each of its 17-tag one-erasure residues, not merely whether each residue contains an archived positive 16-tag layout. The full 156-layout core certificate does NOT settle this. The finite auditor finds **zero** 18-tag sets for which *all erasure residues contain certified 16-tag bases*. That is a **failure of this sufficient certificate**, not proof of 18-tag impossibility. Likewise, it does not exclude additional 19-tag robust designs omitting one corner.

Therefore **b6^(1)∈{18,19} remains open**. The paper must never claim the exact 19 threshold or exact count 12 of *all* robust 19-tag designs.

## Reproducible audit and provenance

- `scripts/cuberev-observation/audit_b6_one_erasure_robustness.py` — exactly 156 historically certified positive 16-tag omitted families; reports sufficient 16-core certificates at 16..20 observed tags, 66/66 edge–edge and 96/96 corner–edge extension counts, avoids invalid converse.
- `scripts/cuberev-observation/test_b6_one_erasure_robustness.py` — five semantic-boundary tests. The 18-tag negative test concerns **existence of sufficient core certificates only**, NOT actual B6 invalidity.
- Hernando–Mora–Slater–Wood (2008), *Fault-Tolerant Metric Dimension of Graphs*, is in Research OS Drive 00 at `1qjgI5Jllteoog_RedYttju-zX7p6nDe4`. Their distance-landmark failure model is distinct from an original oriented cubie sensor.
- Boutin, *Determining Sets, Resolving Sets, and the Exchange Property*, arXiv 0808.1427v1, Drive `1uQpaotOWnqEi6oTShp4WSHoy6B0B1IgD`, already studies exchange failures. The generic idea is not new.

## Next physical decision gate

Classify **all** 17-tag B6-valid designs with actual original 18-HTM stabilizer distance tests. Every 18-tag one-erasure robust design would need every 17-tag deletion B6-valid. A full 17-tag certificate is the decisive missing input, independent of whether those 17-tag designs contain a positive 16-tag core.

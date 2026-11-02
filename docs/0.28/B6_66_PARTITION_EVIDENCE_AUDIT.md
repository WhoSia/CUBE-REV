# B6 fixed-corner omitted-edge pairs: exact evidence accounting

## Scope and provenance

For one original edge h, omit its two endpoint corner sensors and exactly
two original edge sensors. There are C(12,2)=66 possible edge omissions.
The five relative edge classes are h (1), near N (4), parallel P (2),
far F (4), and antipodal h* (1).

This note compresses already existing physical results, rather than claiming
new B6 states or introducing a new invariant.

**Authoritative older executable dependencies:**
- scripts/cuberev-observation/verify_b6_mixed_support_filtration.py:
  physical facelet replay for 15 B5 invalid-support orbits and 19 novel B6
  witness orbits, producing 360 prior and 420 new 4-cubie support masks.
- scripts/cuberev-observation/verify_b6_obstruction_filtration.py:
  grade table across 12 h choices, recording B5 invalid / new B6 witness /
  B6 positive by prior full-state census.
- scripts/cuberev-observation/verify_b6_nf_four_seeds.py:
  four actual length-six word-pair seeds transported under cube symmetries.
- scripts/cuberev-observation/verify_b6_nf_cover_duality.py:
  independent 8-edge cover combinatorics for the K4,4 block.

## The category-level accounting (fixed h)

| Omitted edge classes | B5 failure | New B6 failure | B6 success |
|---|---:|---:|---:|
| h-N | 4 | 0 | 0 |
| h-P | 2 | 0 | 0 |
| h-F | 4 | 0 | 0 |
| h-h* | 0 | 1 | 0 |
| N-N | 0 | 2 | 4 |
| N-P | 4 | 4 | 0 |
| N-F | 0 | 16 | 0 |
| N-h* | 4 | 0 | 0 |
| P-P | 0 | 0 | 1 |
| P-F | 0 | 8 | 0 |
| P-h* | 0 | 2 | 0 |
| F-F | 0 | 2 | 4 |
| F-h* | 0 | 0 | 4 |
| **Total** | **18** | **35** | **13** |

The local K4,4 statement accounts for **all 16 N-F** new witness failures,
but these 16 were already counted in the 35 B6-new failures. The other
19 B6-new failures are classified by the table. Consequently the previous
description '50 candidates still need investigation' is a status local to
the isolated K4,4 theorem: the pre-existing combined certificate already
grades all 50 as 18 prior B5 failures, 19 other B6 failures, 13 positives.
There are **no 37 unclassified omissions** in the existing audit.

The only successful relative category types at fixed h are:
N-N (4), P-P (1), F-F (4), F-h* (4), totaling 13. Across 12 choices of h
this yields 156 labelled layouts, **provided** each labelled two-corner
omission corresponds to a unique original layout, as in the historical
classification. The 13 positives depend on the prior B6 full-state census:
physical obstruction witnesses alone cannot prove sufficiency.

## What remains mathematically interesting

The existing exact grading is a finite five-category combinatorial result,
not a new general complexity theorem. A valuable next proof would derive
the split inside the six N-N and F-F candidate pairs (two invalid and four
valid in each) **from geometric incidence**, without reading the historical
graded masks as an oracle. Verify any such geometric rule against raw
physical replay and the existing full-state positive census.

A second possible step is a short derivation of the specific 19 non-N-F
B6 failure supports from fewer independent facelet witnesses. Do NOT
rerun an 8-million-state cube census when the objective is to extract a
human-sized structural proof.

## Reproduce the light audit

python scripts/cuberev-observation/audit_b6_66_partition.py

The code checks category cardinalities, all 66 placements, the
18+16+19+13 partition, and the four survivor-type counts. It is a
consistency audit only, not a physical proof replay or a new 13-pattern
sufficiency certificate.

# CUBE-REV observation generalization — algorithm lineage and reusable components

## Why code reuse, not another solver from scratch

- **Physical transition:** reuse the repository's existing CUBE-REV 0.15
  `scripts/cuberev-015/ur-fiber-tomography.mjs` (`urMoveAutomaton`)
  as the historical comparison target; the new small Python 54-sticker
  projection gives an independently executable reference for this subproblem.
  Do not silently substitute a Kociemba full-cube solver: solving the cube
  and maximizing observation-code distances are different objectives.
- **SAT/set cover:** reuse the modeling and proof discipline of
  `scripts/cuberev-018/solve-mstar-unrestricted.py`.
  A physical word is one Boolean selection variable; each eligible source
  set gives a coverage clause, and a cardinality constraint decides k.
  PySAT Glucose4 + CardEnc.seqcounter are existing solver facilities; SAT
  models must be rechecked by actual physical replay.
- **Greedy selection:** standard maximum-uncovered-set greedy heuristic is
  used to obtain a feasible *upper bound* quickly; it does not establish a
  global optimum.
- **Public code reference:** `python-sat` (https://github.com/pysathq/pysat)
  supplies the SAT engine. Its code is installed via package dependency and
  not copied into this repository. Verify the license and installed revision
  before vendoring or redistribution.
- **Potential later reuse, not yet imported:** Google OR-Tools CP-SAT
  (https://github.com/google/or-tools) for larger covering instances and
  GitHub cubejs (https://github.com/ldez/cubejs) or published Kociemba
  implementations only if a full-cube goal-policy benchmark becomes relevant.
  No claim that these external implementations have been integrated.

## What is already computed

With the original 54-sticker-derived 18-move transitions and one-bit-error
distance threshold three, the committed 27-word, length-seven witness
dictionary covers **all 220 3-element and all 495 4-element initial-source
subsets**. This is a constructive certificate that
`M*_robust(7; all size 3+4 subsets, one bit error) <= 27`.
It is independently checked in
`scripts/cuberev-observation/verify_l7_27_cover.py`.

A reproducible, explicitly heuristic search uses 13,000 randomly sampled
7-move words with seed 25, plus the original four seed witnesses; among
these, 1,587 have nonempty size-3..5 coverage. This finite *candidate*
screen includes all 220 triples and 495 quadruples and 223 of 792
quintuples. Greedy selection produces the 27-word certificate. These
candidate counts are **not** exhaustive L7 counts.

A separate, much smaller experiment uses only the *four seed words* and
targets their union of 186 covered source sets. Each seed has a private
source set not covered by the other three (private counts 61, 5, 5, 102).
Therefore **four is exactly necessary and sufficient within that
four-word candidate pool for those 186 targets**. This scoped lower bound
does not apply to all possible physical L7 experiments.

## Unresolved mathematical target

The true globally optimal dictionary size for all size-3 and size-4
source subsets remains OPEN: a constructive 27 upper bound is not a
lower-bound certificate. Future work: maximize columns by physical
enumeration or symmetry reductions; exact set cover on the complete
candidate-column family; certified SAT UNSAT/DRUP or independently
checkable combinatorial lower bounds. A solver's mere numerical
'infeasible' status is not a proof.

## Provenance/custody

No third-party cube solver source code has been pasted or vendored. The
methodology was adapted from CUBE-REV's existing modules and documented
external solvers. Human WhoSia commits only; `GitHub-Actions[bot]` must not
commit code. Read-only Actions can run the tests and upload reproducible
JSON/SHA artifacts.

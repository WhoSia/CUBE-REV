# Observation generalization — development track

Active branch: `research/observation-generalization` (forked from `research/current`).
The repository-wide scientific release remains **CUBE-REV 0.27**; none of
these smoke tests upgrades a theorem or settles the L=7 frontier.

## Scope

This module inherits the historical CUBE-REV 0.18 physical 12-UR-edge
single-bit-after-turn observation experiment and studies robust source
identification and later finite-memory belief policies. Source positions are
indexed 0..11; physical tracked-edge states are oriented position indexes
0..23. An experiment is a legal word over 18 HTM moves.

- `physical_edges.py`: generates all 18 oriented-edge permutations **from
  54 sticker coordinates and sticker-normal rotations**, not an imported
  hand-coded 24-state oracle.
- `robust_observation.py`: computes observed binary signatures and source
  subsets whose pairwise Hamming distance is at least `2t+1`.
- `test_observation.py`: invariants, inverse moves, synthetic error
  correction, and historical length-2 zero-error baseline.

Run from repository root, Python 3.11+:

```sh
python -m unittest discover -s scripts/cuberev-observation -p 'test_*.py' -v
python scripts/cuberev-observation/physical_edges.py > /tmp/edge_transitions.json
python scripts/cuberev-observation/robust_observation.py --moves /tmp/edge_transitions.json --length 2 --errors 0
```

## CI / custodial policy

The scoped workflow `.github/workflows/cuberev-observation-generalization.yml`
uses `permissions: contents: read`, checkout with
`persist-credentials: false`, no push or commit, and optionally uploads
smoke receipts as Actions artifacts. **GitHub-Actions[bot] must never author
or commit source.** The source commits are authored and committed by WhoSia.

A pushed workflow file is **not** evidence of a passing workflow run.
Do not label the job PASS until its real GitHub Actions job, output and
artifacts have been inspected.

## Known boundaries

The Python explorer deliberately caps literal enumeration at L<=5; it
is a correctness/reference implementation, **not** an L=7 solver.
The separate optimized L=7 observation prefix-DAG search and the
READ/SILENT memory-cost controller remain development targets.

The existing study's L5/L6 1-bit repairability receipts and L6
three excluded 4-element sources are preserved as historical
results, not re-proved by the newly added smoke tests.

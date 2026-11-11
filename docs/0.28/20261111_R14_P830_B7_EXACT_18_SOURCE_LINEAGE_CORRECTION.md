# CUBE-REV 0.28 R14-P8.30 — Revalidated Exact B7 Full-Tag Horizon and Source-Lineage Correction

Date: 2026-11-11. Branch: `research/current`. **Status: independently executed physical code, GitHub Actions PASS; proof is a finite constructive certificate plus elementary legal-group argument, not a full B7 BFS.**

## 1. Correction to 38th-chat research status

The most recent R14/P8.24 notes treated `b7` as unknown and concentrated on the 24-member orbit of one explicit 13-HTM witness. However the repository's *older* `verify_b7_support_completion.py`, `verify_b7_base_orbits.py` and `verify_b7_distance_profile.py` already contain a stronger claim, namely 94 complete two-original-cubie support obstructions in B7 and `b7=18`.

This is an **internal provenance inconsistency**, not license to assert a new discovery. R14-P8.30 resolves it through a fresh, independently written physical 48-sticker verifier with no imports of the older B7 or historical P48 checkers. Do not describe the theorem as first discovered in P8.30; describe it as **revalidated and restored to the active scientific verdict**.

## 2. Exact observation model

`G` is the legal fixed-center 3×3×3 cube group, HTM distance is measured in the symmetric 18-move generating set, `B_r` is the radius-r metric ball around solved, and each *persistent original-cubie-tag sensor* reads the complete position and orientation of one fixed original corner/edge cubie. These sensors are **not** the spatial six-color facelet probes of Paper B.

`b_r` minimizes the number of permanent tagged cubies whose joint observations are injective on `B_r`.

## 3. Certified lower bound: all two-corner and two-edge supports occur within B7 differences

For all `{c1,c2} subset C` (`C(8,2)=28`) there exist distinct `x,y in B7` whose original tagged cubies differ only in those two corners. Analogously, every `{e1,e2} subset E` (`C(12,2)=66`) is exactly the difference support of a two-state B7 collision.

**Executable finite witness construction:** Eight explicitly listed face-turn words of length 12, 13 or 14, with original-cubie two-tag differences. For each word `w=p s`, evaluate *both* pairs `(s^{-1},p)` and `(p^{-1},s)` for every cut where both halves have length at most seven. Then conjugate both states by each of the 24 proper cubic rotations. Independently check all 18 face turns remain face turns under each rotation. This yields 720 actual state-pair/rotation checks. It is important to include BOTH split orders: using just `(s^{-1},p)` produces only 42 distinct edge-pair supports; the reverse order is necessary to cover all 66. Every generated state is in B7 by an explicit at-most-seven-move word, regardless of whether that word is geodesic.

The new source `scripts/cuberev-observation/audit_r14_p830_independent_b7_pair_support_complete.py` constructs 48 moving stickers from coordinate positions/normals; it uses no historical P48 module and no older B7 verifier import. Exact Python assertions yield all 28/28 corner and 66/66 edge pairs. Assertions for 720 checks and 24 rotations prevent silent partial coverage.

Thus any sensor set omitting at least two corners OR at least two edges fails injectivity on `B7`.

## 4. Upper bound and exact classification

Any sensor set that omits at most one original corner and one original edge identifies every legal full cube state: remaining original positions/permutations are fixed by bijectivity and the remaining corner twist and edge flip by sum-zero orientation constraints. In particular all 8×12=96 configurations observing 7 corners plus 11 edges work globally.

Every set with fewer than 18 sensors omits at least two corners or at least two edges, hence one of the complete B7 pair collisions. Therefore:

```
b7 = 18
number of optimal 18-original-cubie-tag sensor sets = 8 * 12 = 96
b_r = 18 for every r >= 7
```

The final equality uses monotonicity of B_r and the global 18-tag upper bound. The previously certified `b5=b6=16` then shows a strict jump from 16 at radius 6 to 18 at radius 7. No statement about `b1..b4` is introduced.

The earlier plan of determining eight B6 optimal layout first-failure radii is now **partially superseded**: all 156 previously classified 16-tag B6-optimal layouts necessarily fail at B7, so their first failure radius is 7 (conditional on their independently certified B6 positivity). There is no need to seek a distinct radius 8/9/10 failure among those 156.

## 5. Executed proof and CI evidence

- [P8.30 independent physical source](https://github.com/WhoSia/CUBE-REV/blob/research/current/scripts/cuberev-observation/audit_r14_p830_independent_b7_pair_support_complete.py)
- [P8.30 read-only CI workflow](https://github.com/WhoSia/CUBE-REV/blob/research/current/.github/workflows/cuberev-r14-p830-b7-exact-full-tag-minimum.yml)
- [P8.30 successful GitHub Actions execution](https://github.com/WhoSia/CUBE-REV/actions/runs/42973939189) — all job steps success, JSON receipt artifact uploaded.
- [P7 active-set reconciliation successful CI](https://github.com/WhoSia/CUBE-REV/actions/runs/42974107967).

**Boundary:** This is not a full enumeration of all B7 states, a proof that the eight seed words have optimal lengths, a solution to 19-frame color-probe observation, or a new universal theory of base sets. The finite 48-sticker enumerator and word verification are executable witnesses, rather than Lean-kernel-checked mathematics. The original B6 156-layout classification is inherited, not fully rerun here.

## 6. Research direction updated

1. Stop listing the global `b7` minimum as unknown. Carry exact `b7=18`, and clearly distinguish the original-tag model from adaptive six-color spatial probes.
2. Recover independent sources and certify the full 156-layout B6 positivity lineage, including the original 41 18-HTM distance classes and historical archive hash. That is the dependency for asserting that all 156 layouts have exact first failure radius 7.
3. Lean formalize a **finite pair-support witness interface** and the general combinatorial implication `complete corner/edge pair supports => 18-tag lower bound`, without claiming Lean has rechecked the physical words until they are encoded.
4. Continue Paper B unrestricted `h_adaptive in [18,20]`; its 19-frame exact decision problem is separate and still open.
5. Update the 0.28 Notion canonical verdict and manuscript lineage; preserve a correction note rather than silently erasing older uncertainty.

**Authorship policy:** commits via WhoSia only; GitHub Actions is read-only and is not an authorized contributor.

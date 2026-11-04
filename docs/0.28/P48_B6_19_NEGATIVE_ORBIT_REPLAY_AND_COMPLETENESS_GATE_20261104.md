# CUBE-REV 0.28 — P48 physical B6 negative witnesses: 19 proper-rotation orbits and 420 failure supports

**2026-11-04. Status: independent physical replay of inherited short word pairs; NOT a new B6-negative exhaustive enumeration.** The new full-physical positive MITM for 41 stabilizer distance classes already passed on run [41763106125](https://github.com/WhoSia/CUBE-REV/actions/runs/41763106125). The purpose here is to reduce the independent-model gap on the **negative** side of the exact 156-layout claim.

## Source-graded statement

Nineteen earlier two-sided HTM witness pairs are explicitly listed in `verify_b6_negative_witnesses.py`. Each word has at most six face turns and is a historical candidate source. The new `verify_b6_negative_19_pairs_p48.py` **does not import the previous 54-facelet engine, its B6 output masks, its B5 archive, or an existing positive-layout list**. It builds full original-cubie position/orientation signatures by applying each historical *word* to independently generated 48 moving stickers, compares both complete original-tag states, physically replays all 48 signed spatial transports of each word pair, and takes proper-24 orbits of their four-tag supports. Improper symmetries are checked but not mixed into the 19 proper-orbit count; doing so could merge two proper orbits and lose the original 19-seed coverage contract.

**Observed local computation:** nineteen physically replayed proper spatial orbits are pairwise disjoint and cover exactly **420** distinct supports, each of the form two adjacent original corner tags plus two original edge tags. There are **35** distinct failure supports for each of the twelve possible omitted adjacent-corner edges. Every one of the 420 edge-pair omissions is rejected by the independently P48-generated geometric 13-per-core positive rule; zero overlap.

These results independently authenticate the physical *content* of the 19 historical B6-negative seeds in a second physical transition implementation. They are not a proof that 420 is the total number of B6-negative four-tag supports: the B5-proven 360 failures, excluded corner-pattern types and other support sizes are separate obligations. A seed-source-custody note must not be mistaken for new independent discovery of those words.

## Mathematical conjunction with positive evidence

For a fixed core edge `h`, 66 unordered absent edge pairs partition under the prior complete negative obstruction families as

- 18 physically excluded already at radius five, in the historical B5 negative witness archive;
- 35 now independently physically replayed in P48 from 19 historical length-six word-pair seeds, per core;
- 13 not excluded, and **independently proved positive** by the new 41-class P48 exact MITM (the geometric candidate family).

Thus, subject to the remaining original B5 and corner-pattern completeness steps, the fixed-core classification has the familiar accounting

```
12 × (18 B5 + 35 B6-new + 13 B6-positive) = 792 candidates
12 × 13 = 156 independently positive layouts
12 × 35 = 420 newly P48 replayed B6-negative collision supports
```

The B5 part is *not* independently reauthenticated by this script, so the formula is a sourced **conjunction**, not a new single-engine closure of the complete negative theorem.

## Fail-closed regressions

- `python scripts/cuberev-observation/verify_b6_negative_19_pairs_p48.py` checks every full-sticker word-pair endpoint, 48 spatial transports, 19 disjoint proper-24 orbits, 420 unique supports, 35 per core and no overlap with 156 candidates.
- `python -m unittest discover -s scripts/cuberev-observation -p 'test_b6_negative_19_pairs_p48.py' -v` tests actual positive physical witnesses, rejects identity pairs, and detects a physically altered word.
- Read-only `cuberev-028-independent-p48-mitm.yml` now runs these tests before full 41-class distance work. **A new workflow run must be observed before claiming CI PASS for this new commit.**
- CI `contents: read`, no automated GitHub writeback, no `github-actions[bot]` author or committer.

## Next stronger independence gates

1. Replace the 15 historical B5-negative four-tag witness-orbit dependencies with explicit original words independently replayed in P48; certify all **360** corresponding support masks, ideally from the earlier B5 archive raw bytes with SHA-256.
2. Check completeness of nonadjacent-corner omissions and other candidate shape exclusions from real short physical supports, not just the finite geometric rule.
3. Recombine the 360 and 420 physically authenticated negative supports with the 41-class P48 positive exact distance proof, then conduct a separate audit of all `binom(20,16)=4845` sensor choices. Only then claim that *exactly* 156 B6-optimal sensor layouts have been reconstructed with a fully independent physical negative certificate.
4. Revisit novelty with older cube-specific state reconstruction and minimum-observation work. General group-action bases, fault-tolerant metric dimension and matroid exchange counterexamples are established prior art.

**Publication status:** GO for a proof-bearing finite physical/discrete mathematics case-study manuscript; HOLD external submission and full negative-source independence language.

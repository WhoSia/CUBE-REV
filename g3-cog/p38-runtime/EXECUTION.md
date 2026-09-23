# G3-P38-R1 terminal audit

Verdict: P38_R1_AUDIT_HOLD. Observation/action/combined transport gates HOLD; world-contact HOLD; no successor opened. Audit completion is not scientific certification.

Authority: https://www.notion.so/3e4ef561cf928191a3acc3cf76d263e7

Commands from repository root:

```text
node --max-old-space-size=2048 g3-cog/p38-runtime/audit.mjs
node g3-cog/p38-runtime/verify.mjs
```

## Observation

All 155,040 states and bank terminal hashes reproduced. Exhaustive 16-target comparison count: 2,480,624. The inherited internal-sticker-ID encoding reproduces 16,993 supports, minimum 10, four size-10 supports. However the canonical adapter serializes colors rather than sticker IDs. Color-valued coordinates give 2,318,194 supports and minimum 6. A concrete pair with serialized states and hashes is retained in canonical-observation-counterexample.json. This is an audit discrepancy, not authorization to replace frozen D or revise earlier results silently.

Frozen D still has 218,368-context coverage and 16 collateral pairs under either encoding. Its frozen pair has precisely D as its difference support under both encodings. All ten deletions separate this pair. The inherited-ID leave-one-out coverage is zero throughout; color leave-one-out coverage is not zero throughout. Thus pair irreducibility does not resolve the encoding discrepancy. The supplied pair is preserved, but its prospective ordering is not independently certified.

All four inherited size-10 candidates were evaluated. Each covers all contexts; collateral-pair counts are 48, 48, 64 and 16. Frozen D uniquely minimizes collateral pairs among these four. All four belong to one verified rotation orbit. The full 24-element orientation group passed 288 move conjugacy checks and 576 closure checks. D orbit size 12, stabilizer 2; only four orbit elements are on the inherited size-10 frontier. Ranking statistics are not invariant across the orbit because the finite bank is not rotation-closed.

The prior frontier file records 3,684 of 16,993 supports; its dominance filter tests size and equal targetBits without the required subset condition. This audit reconstructs support histograms and every size-10 candidate, but does not substitute a repaired P37 frontier.

## Action

Recovered all 62 tables from the inherited antichains. All 180 Hasse edges, six A neighbors, and 11 inclusion-minimal informative selectors are materialized. Monotonicity, table-recovery and selector gamma-covariance failure counts are zero. A is inclusion-minimal and cardinality-minimal (three faces). Full selector orbit count is 22; informative and minimal families are not closed under gamma, so their intersections must not be presented as autonomous group actions.

The literal mapping g(start), g(target), gamma(history) has 1,024 unmatched directional contexts (512 each), all localized to transformed targets outside the 16 certified origins. There is no in-bank 512-to-512 bijection. This does not invalidate the separate selector-covariance test.

The frozen P34-001164/A/r2 six-move route returns to the exact target; its gamma route also returns. A separate unpruned actual-color-state 3+3 join test checks both representation antichains. However the first divergent context under the prescribed origin-hash ordering is P34-001644/A/r2, not the frozen witness. The frozen witness is preserved as valid but not certified first.

P37's search reuses solved-origin keys (6,724), not explicit target-indexed reverse caches. Its source does not include the required unpruned-mask regression. This audit does not infer incorrect action counts from those implementation differences, but it does not retroactively certify their full-domain equivalence either. Witness-specific controls are explicitly narrower.

## Factorization and gates

Under the stated independent-instrument premises the product theorem follows componentwise: O changes only the observation component and A only the action component. A differing component is already a pure-axis difference; there is no new joint-only difference for that product outcome definition. This is conditional, not a proof for arbitrary coupled outcomes.

Actual source paths are independent, but observation-coordinate semantics and exact-target reuse need reconciliation before runtime certification. Prior joint status is a literal status assignment, not a joint runtime ledger. Neither structural joint-null promotion nor external-domain validation is claimed. Observation, action, and combined transport remain separately HOLD.

## Custody

Only files in g3-cog/p38-runtime are newly created. All inherited bank and P37 inputs are verified before and after execution and unchanged. sha256-manifest.json records core audit outputs; custody-sha256.json additionally seals source, this narrative, and independent verification. No successor or world-contact action was initiated.

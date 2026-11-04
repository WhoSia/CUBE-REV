# CUBE-REV 0.18 — M-star exact-34 supersession court and original proof-byte custody (2026-11-04)

**Authoritative scientific verdict for the frozen 0.18 observation-dictionary instance: EXACT M* = 34 = 27 + 7, externally checked finite proof; NOT a claim about arbitrary Rubik shortest solution length.** This dated court supersedes older 0.18 and 2026-11-03 review sentences reporting only 30 <= M* <= 34 and "exact unresolved." Preserve those earlier sentences as timestamped history, not current facts.

## The exact instance and logical dependency

- A fixed tracked original UR edge, 18-HTM legal physical Rubik face turns, experiment words of four turns, post-action tracked-edge flip readings, and the original family of **1,192** legal initial-source subsets.
- Original physical incidence includes **1,323** inclusion-maximal experiment columns. Full cardinality-preserving implication/column-reduction checks reduce the optimization to **398 × 168**, then two disconnected components **334 × 80** (five-slot) and **64 × 88** (four-slot).
- The five-slot unsatisfiability of <=26 choices and four-slot unsatisfiability of <=6 choices imply **at least 27 + 7 = 34**; a separate actually replayed physical 34-experiment dictionary establishes the upper bound. The exact decomposition depends on the independently audited physical-to-reduced-column correspondence, not solely on UNSAT of arbitrary auxiliary CNFs.
- Historic false P6 34-word catalog **stays REJECTED**: a different fresh 34-word physical upper witness is valid. No evidence laundering by coincident cardinality.

## Confirmed original GitHub provenance

- [Exact two-component proof run 37958523951](https://github.com/WhoSia/CUBE-REV/actions/runs/37958523951) — completed SUCCESS 2026-10-09. Original job log printed `CUBE_COMPONENT_UNSAT_INDEPENDENT_DRUP_PASS cube_5slot_k26`, `CUBE_COMPONENT_UNSAT_INDEPENDENT_DRUP_PASS cube_4slot_k6`, and `CUBE_REV_018_EXACT_PHYSICAL_MSTAR34_PROOF_CHECKED_PASS`. Both standalone drat-trim checks printed `s VERIFIED`.
- [Fresh 34 physical upper replay run 37948949764](https://github.com/WhoSia/CUBE-REV/actions/runs/37948949764) — SUCCESS, distinct from the invalid P6 catalog.
- [Earlier unrestricted k29 proof run 37945846343](https://github.com/WhoSia/CUBE-REV/actions/runs/37945846343) — SUCCESS, historically established M* >=30 before exact-34 closure.

## Raw bytes placed in Drive 10_CANONICAL_PROOF_COURTS (2026-11-04)

| Proof artifact | GitHub artifact ID | Preserved Drive raw ZIP | Bytes | SHA-256 of complete ZIP |
|---|---:|---|---:|---|
| Two-component exact-34 CNF, DRUP, check logs and receipts | 11632491824 | [Drive](https://drive.google.com/file/d/19ry8e4HgyJ_C3uVbZrsGHl9D2Z4ZzHrJ/view) | 14,728,286 | `4f947c36c32185f02c59d3ed9b5d1fe6a71c1a20904e9f38f798d3e86d8228fb` |
| Physical 34-experiment upper witness | 11626372084 | [Drive](https://drive.google.com/file/d/1mRv8X6gAt2jo3pCRlDktcAvQAfdAWLoI/view) | 67,509 | `fa2c85a51914ce27cec647f15a550f909ffda65f2c2ac801419898f9f06187e9` |
| Earlier unrestricted original k29 UNSAT | 11623466425 | [Drive](https://drive.google.com/file/d/1oYYiMqoS9KuVGeGlHGy4VP6YeZwcaM4e/view) | 42,151,779 | `b39f31425509f31562396dacb9b9d8e7fc3e7e78556305f74c0bb1d68c80ec26` |

All three original GitHub artifacts were scheduled to expire **2026-11-08**. Each raw ZIP was uploaded to Drive as a new file, re-fetched via the authenticated Drive raw download, and its complete bytes compared via SHA-256. New Drive IDs were read back. Do not mistake a GitHub artifact's reported compressed size for the original uncompressed DRUP proof size.

## This-session local independently recompiled check (additional evidence)

On 2026-11-04, downloaded the exact component ZIP back from Drive; extracted the archived `drat-trim/drat-trim.c`; compiled a NEW verifier via `cc -std=gnu99 -O2 drat-trim.c -o drat-trim-check`; confirmed all four CNF/DRUP file SHA-256 values against their respective stored component receipt JSONs; then ran:

```bash
./drat-trim-check proofs/cube_5slot_k26.cnf proofs/cube_5slot_k26.drup
./drat-trim-check proofs/cube_4slot_k6.cnf proofs/cube_4slot_k6.drup
```

Both returned **`s VERIFIED`**. SHA-256 values of component raw files:
- five-slot CNF `960cc8334c428b703b326a318f2d82e0e7a3fb38cd01ca802e28ec33f9c370d7`
- five-slot DRUP `348535175d067741ac0c6ecdbaa873d6e713b69519c4cc50b6febac9449097a1`
- four-slot CNF `c6473f4fc852c4af451e6542f065b5196e03fdd3993a99b7845cbdbe97f486f6`
- four-slot DRUP `0ed5f7b95a08d7f31f0eee6465bd6cf4dee0cefa4f60ce14a2b8c2c7a3717e44`

**Precision:** This local audit rechecks external SAT proof correctness and stored-provenance byte hashes. It is not a fresh independent implementation of the 1,192-source physical-incidence map, a Lean kernel reconstruction, or a peer-reviewed novelty adjudication. The top-level ZIP receipt correctly lists **Lean kernel verification of all physical sticker transitions and academic novelty** as STILL UNPROVED. Prior `accepted_math_claim:false` fields in the generated component receipt are historical pre-check status; the final component receipts have `independent_proof_checked:true` and the final theorem receipt is independently present.

## Prevent recurrence

1. Mark old `30 <= M* <= 34` reports as **superseded 2026-10-09**, never silently delete them; use exact run, artifact hash and theorem object identity in any subsequent "latest" court.
2. A paper draft may cite the exact frozen-instance finite theorem but must not present it as a new non-enumerative general principle or a human cognition finding.
3. Preserve original three artifacts in Drive, SHA-verified, alongside the older branches and Chat Archive record. Notion keeps the current scientific verdict; Drive keeps raw bytes; GitHub contains lightweight reproducibility and provenance text, not big ZIP content.
4. Journal originality and external review remain OPEN. Do not promote an archive audit or numerical integer to a new publication merely for project momentum.

**Repo discipline:** research/current only; WhoSia original author and committer; GitHub Actions read-only, no github-actions[bot] source commits.

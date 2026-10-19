# CUBE-REV 0.27 P11b — A Self-Checkable Physical Corner-Distance Certificate

**2026-10-19; subtheorem certified, full WCA exact-18 theorem still OPEN.**

## Proof object
A fixed binary file of exactly **40,320 bytes**, `physical_corner_40320.dist.bin`, proposed as the shortest HTM distances of the **8! physical corner-permutation projection** from solved. Its SHA-256 is `b5c35a30b9782f689bdb786c5314653eb64f409232210ba23407b65f942829b8`. The generating Python BFS is completely separate from the **independent C++ validator** `p11_verify_corner_certificate.cpp`, which reads the 40,320-byte proof data and the authentic original P11 `packed_physical.hpp` 54-site 18-turn permutation table. It does not execute the generator BFS and does not import RubikOptimal or trust its saved pruning table.

## Exact finite theorem verified
For all 40320 physically labeled 8-corner permutations, independently map all 18 physical facelet actions to the corresponding 8-corner actions using the original real sticker permutation; require the permutation coordinate map ranks every state exactly once; require the identity is the **only** state whose proposed distance is zero; require every directed generator edge to change the proposed distance by at most 1; require every nonzero state to have an outgoing distance-decreasing neighbor. The actual completed C++ verification covered all 40320 states and **725760 physical generator transitions** and printed:
```
P11_CORNER_PROOF_OBJECT_SELF_CONTAINED_NATIVE_CHECK_PASS states=40320 edges=725760 histogram=1,18,243,2646,12516,17624,7080,192
```
**Proof:** Along any path to identity with length L, triangle inequalities give proposed D(x)<=L. Conversely for x!=identity a strictly descending neighbor exists and every descending path terminates after exactly D(x) physical moves at the unique D=0 state, which is identity. Thus the true projected HTM distance to solved equals D(x) at every one of the 40320 states. Since every full physical cube move induces the corresponding projected corner-permutation move, this exact table supplies a sound lower bound on full Rubik's Cube distance. This does **not** alone prove the fixed original WCA source has no 17HTM solution.

## Deliberate checker breakage and repair (do not hide failure)
During RAVEL negative controls, **the initial C++ checker wrongly accepted an all-zero distance table**! Merely demanding D(identity)=0, edge Lipschitz and descent from every *positive*-labeled vertex permits false extra D=0 states. Corrected C++ checker explicitly forbids D(x)=0 at any x!=identity. Recompiled and ACTUALLY reran tests. Genuine binary proof object PASS and **all four modified proof objects REJECTED**:
1. Identity distance changed from zero — REJECT.
2. An unrelated corner distance overwritten by 250 — REJECT.
3. Truncated 40319-byte file — REJECT.
4. Entire 40320-byte table set to zero — REJECT.

This correction is part of the scientific record and an instructive negative-control necessity, not an invented retrospective result.

## Actual full source and raw bytes
Complete minimal reproducibility archive has nine members: independently authored C++ verifier, authentic original P11 `packed_physical.hpp`, raw 40320-byte certificate, independent Python authoring/audit source, physical geometry source, actual PASS stdout, four-mutation rejection stdout, the detailed proof note and per-member SHA256 manifest.

- Package **22,948 bytes**, SHA-256 `fd4a9618d5f2e60ac02955c4cbb0c5c66c3c9fb35e4886fbca6d47a95645fef8`.
- Uploaded to the existing original Google Drive `10_CANONICAL_PROOF_COURTS` as file ID `1LTrBOgUSrGsDdSPhbSvG3sEuP9Cug-tc`: https://drive.google.com/file/d/1LTrBOgUSrGsDdSPhbSvG3sEuP9Cug-tc/view .
- Actually re-downloaded the raw 22,948 bytes from Drive; complete byte-for-byte equality with original local ZIP verified, original SHA-256 matches and 9/9 ZIP CRC passes. **P11B Drive T2 BYTE-VERIFIED**.

## Research level and further obligations
This is the first small true **independently checkable proof-carrier certificate** in 0.27; distinction from previous solver-generated self-report is essential. The previously established hosted independent physical corner BFS offline GitHub [#39196611437](https://github.com/WhoSia/CUBE-REV/actions/runs/39196611437) also PASS. A larger read-only independent RubikOptimal replay **with its nontrivial equal-axis extra pruning removed** remains running at [#39196884761](https://github.com/WhoSia/CUBE-REV/actions/runs/39196884761); no no-17 certification is asserted until that real job finishes. Even success would leave the enormous three-axis phase1x24 modulo3 projected PDB and quotient correctness as separate independent proof obligations. Original externally solver-backed d=18 and lower17 remain distinct and honest.

**Next high-value paper step:** make one-sided admissible potential certificates for the three large projection tables, rather than accumulate additional 18HTM solutions or only hash the executables.

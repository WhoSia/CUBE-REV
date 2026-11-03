# B6 exact minimum 16 — independent positive certificate + rechecked B5 negative certificate

**Date:** 2026-11-03. **Status:** PASS, subject to the exact 3x3 original oriented-cubie sensor model and previously sealed physical 54-facelet archive. This is a finite certified result, NOT an asymptotic NP-hardness theorem.

## Definition

For the 18-HTM symmetric cube group G, B_r is the word ball around solved with radius r. For S a subset of 20 ORIGINAL cubie tags, observe each tag's full position AND orientation. Define

    b_r = min {|S|: all x,y in B_r having equal observations on S implies x=y}.

Since B_5 is a subset of B_6, any sensor set identifying B_6 also identifies B_5, so b_6 >= b_5. This monotonicity is a one-line theorem, independent of any new B6 lower-bound search.

## Lower bound b_6 >= 16 (B5 proof independently re-executed)

Primary source archive:
CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip
SHA256 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94

The original b5_final_summary.json records b5_exact_minimum 16, 169 physical witness pairs, 316 rotated support masks and zero unrefuted 15-tag candidates. To avoid trusting its summary alone, extracted the entire archive and executed original proof scripts against its 54-facelet engine on 2026-11-03:

- python geometry_reduction.py -> GEOMETRIC_OBSTRUCTION_IDENTIFICATION_PASS 84 12; GEOMETRY_RECONSTRUCTS_EXACT_102_PASS 102.
- python equivariance_corners.py -> GENERATOR_EQUIVARIANCE_FOR_ALL_54_FACELETS 23328 PASS.
- python b5_nine_pair_verifier.py -> NINE-PHYSICAL-PAIR EXACT B5 15-LOWER-CERTIFICATE PASS; 9 physical orbit supports; 136 support constraints; 4,624 candidate 15-tag designs refuted out of 4,624.
- python b5_verify_coverage.py -> B5 EXACT LOWER-CERTIFICATE COVERAGE VERIFIED; 128 historical plus 41 additional physical witness pairs =169; 316 rotated supports; 4,624 candidate 15-tag designs; zero unrefuted; independent physical 54-facelet replay of all 169 pairs PASS.
- python b5_sixteen_small_certificate.py -> 15 original physical witness pairs generate 360 rotated invalid 16-tag placements; separate B5 positive classification relies on its historic full census.

The B4 geometric candidate reduction plus these actual replay checks supply the known B5 no-15-sensors lower bound b5>=16. By ball monotonicity, b6>=16. We do not need to separately enumerate hypothetical 15-sensor failures at radius six.

## Upper bound b_6 <= 16 (new independent B6-positive algorithm)

Existing original-cube geometric four-case rule produces 156 size-16 sensor sets, grouped in eight proper cube-rotation orbits. Each has 11 nonidentity legal full-cube states in its pointwise stabilizer. Using full 48 spatial cube automorphisms plus inversion gives 41 HTM-distance target classes. This physical goal generation was re-executed and matched the SHA256 seal of the 41 canonical physical states:

    c3dbf41177e16d8d0cb0cd76b433304e14f9cdac4a14f205d6231dc9dd8abc1e

The new C++ exact MITM program (scripts/cuberev-observation/verify_b6_41_mitm.cpp) enumerates the complete full-state six-ball of 8,240,087 cube states (8,331,112 canonical word paths), then tests each of 41 independently generated target six-balls for intersection. Five complete batches checked 341,575,592 goal paths, with zero intersections in every class, so all 41 goal states have 18-HTM word distance >=13.

For each of the 156 size-16 layouts S, H_S contains no nonidentity element of length <=12. The group identity

    projection(B_r,S) injective <=> H_S intersection B_(2r)={identity}

therefore proves all 156 proposed layouts are injective on B6; hence b6<=16. Critically, this new positive decision procedure does not query the old B6 sensor-projection verdicts or the old 27-representative projection census, though it shares the original physical 54-facelet action source.

## Conclusion and proof-dependency ledger

    b5>=16  [independently rerun original B5 negative facelet certificates]
          |
          v
    b6>=16  [mathematical monotonicity, B5 subset of B6]
    b6<=16  [new 41-goal full-state exact MITM PASS]
          |
          v
    b6=16   [exact minimum for stated observation model]

This **independently closes b6=16 relative to the original physical transition semantics**, without reusing the old B6-positive projection census. It does NOT establish that the 156 exhibited layouts are the ONLY size-16 bases; uniqueness/completeness of the positive family requires earlier 16-layout negative obstruction coverage, or a separate independent exhaustive checker. It is also NOT a source-independent second 3x3 physical engine, and does not prove a new general complexity class, a universal Rubik sensor theorem or a non-enumerative 13-distance inequality.

## Reproduction / no bot commits

Archive must match the above SHA256; it is never committed to GitHub. For B5 replay, extract the archive to a local Python folder (original b5 scripts may have a hardcoded import path and thus require a controlled local path adjustment). For B6 MITM, run scripts/cuberev-observation/run_b6_41_mitm.sh with the exact archive and an output directory. Source, goal manifest fingerprint and five-pass result ledger: docs/0.28/evidence/B6_MITM_41_20261103.md.

Use authenticated human-account GitHub commits only. Remote GitHub Actions CI completion is separate and not asserted.

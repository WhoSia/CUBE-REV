# CUBE-REV 0.28 — Research status, independent proof and scientific-value audit
2026-11-03. Canonical semantic notebook: [CUBE-REV 0.28 Notion](https://app.notion.com/p/409ef561cf928193b3d1dc1165ad92ea). This document is executable-evidence-oriented companion material, not a new version number.

## Research question (preserve the scientific core)

For physically legal 3x3 Rubik motion, how much original-cubie position/orientation information is required to reconstruct a state when its HTM distance from solved is bounded? Which geometric arrangements of missing cubies admit state collisions, and at which radii do those collisions first occur?

This is **not** generic adaptive-vs-preset FSM protocol benchmarking. Mathematical tools are those appropriate to the original physical problem: finite permutation groups, stabilizers, incidence geometry, word metrics, and exact independent proof programs.

## Historical lineage and distinction of objectives

- Early CUBE-REV work established physically grounded tagged-edge/orientation automata and exact finite experiment certificates, with the retained physical-validity and contribution-authorship requirements. In 0.18 the separate Mstar dictionary problem concerns 1,192 source-subset hypotheses and four-step experiments. The authentic 0.18 PROGRAM_CHARTER documents a certified **30 <= Mstar <= 34**, NOT an exact value. The old 34-word physical replay failed and was replaced by a distinct independently validated 34-word certificate. These are distinct tasks and numerical values must NEVER be compared directly to b_r.
- 0.28 uses full original-cubie position AND orientation readings at a fixed selected set of cubie tags; its hypothesis set is the legal radius-r cube ball B_r. Recorded b1..b7 values 2,4,8,14,16,16,18, with B6=8,240,087 states and 156 previously reported optimal 16-tag layouts. The 156 layouts form eight 24-rotation orbits and six extended 48-spatial-symmetry orbits.
- A fixed pair of missing adjacent original corners corresponds to a cube edge h. The 12 possible unobserved original edges split geometrically into h, four near, two parallel, four far, and opposite h*. The 66 omitted-edge pairs split 18 B5-bad + 35 new B6-bad + 13 B6-positive. The four positive types are N-N (4), F-F (4), F-h* (4), P-P (1). The 16 N-F new failures form a K4,4 witness obstruction. All these were established before this 2026-11-03 run.

## Exact reduction and stabilized finite state set

Let G be the physical cube group under the symmetric 18-HTM alphabet, B_r its word ball, S the selected original oriented cubie tags, and H_S their pointwise stabilizer. Then

    Projection of B_r onto S injective  <=>  H_S intersect B_(2r) = {1}.

This follows from B_r^(-1)*B_r=B_(2r) and the full left group action on original tags. For 16 observed tags omitting two corners and two edges, |H_S|=2 parity cases x 3 twist cases x 2 flip cases = 12 legal configurations, with 11 nonidentity targets. The 8 rotation-representative layouts initially entail 88 target obligations; 74 distinct physical full states; 41 representatives under inversion and all 48 cube spatial automorphisms, each preserving HTM distance. The physical 41-goal class SHA256 is:

    c3dbf41177e16d8d0cb0cd76b433304e14f9cdac4a14f205d6231dc9dd8abc1e

This construction is straightforward finite group theory, not itself a new general group-theoretic theorem.

## New completed independent-positive proof (2026-11-03)

For each of the 41 targets g, certify distance_18HTM(1,g)>=13 using exact two-sided radius-six enumeration. Build the solved B6 ball once and query whether the radius-six ball about g intersects it.

- Original physical ZIP digest: 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94.
- Full 20 original oriented-cubie coordinates packed losslessly into 100 bits. All 20 factor action tables are generated from the original 54-facelet physical move maps, not from selected observation projections.
- Every radius-six normal-form search generates **8,331,112 paths**, containing **8,240,087 distinct fully oriented cube states**.
- Every one of the 41 target queries exhausted all 8,331,112 paths and found **zero exact states shared** with the solved B6 set.
- 5 separate normal-exit job ranges: [0,8), [8,16), [16,24), [24,32), [32,41). **41 PASS, 341,575,592 target path probes total**.
- Integer equality of both 64-bit packed state words is checked after hashing. Hash collisions cannot cause incorrect equality.
- The normal-form enumeration is complete because adjacent same-face turns collapse under HTM and opposite faces commute, allowing a canonical order without increasing word length.
- Positive detection control: a one-face-turn state belongs to the solved-radius-six ball.
- Existing 13-HTM physical upper word flips exactly UR and UF, providing an exact distance-13 result for that state by combining this independent >=13 bound with the physical <=13 witness.

**Deduction:** All 11 nontrivial stabilizer targets for each 156 geometrically proposed positive layouts have length >12; so each layout identifies all B6 states. This is a *new, independent computational proof of the old positive B6 classification*. It does not use the old 27-representative sensor projection census or its successful-mask verdict as an oracle. It does use the same primary physical Rubik move semantics and the already checked geometric candidate rule; independence is **algorithmic, not full physical-model diversity**.

**Not newly proved:** No 15-or-fewer sensor solution (the b6>=16 lower bound), or a closed-form nonenumerative 13-distance exclusion theorem for all 41 goals. Historical independent negative B6 witnesses and the older minimality proof remain separate. The goal count 41 is a certificate economy, not a new scientific invariant. Exact distance=13 is NOT established for every target, only distance>=13 for all 41 and precise upper bounds where known.

## Reproducibility and integrity

Files:
- scripts/cuberev-observation/emit_b6_41_mitm_inputs.py
- scripts/cuberev-observation/verify_b6_41_mitm.cpp
- scripts/cuberev-observation/run_b6_41_mitm.sh
- docs/0.28/evidence/B6_MITM_41_20261103.md

Run in Linux/WSL with Python 3 and g++ C++17:

    bash scripts/cuberev-observation/run_b6_41_mitm.sh PATH/EXACT_B1_B5_SENSOR_CERTIFICATES.zip /tmp/cuberev-mitm-41

The shell script regenerates both the target manifest and C++ 20-factor table from the SHA-verified primary archive, runs all 5 chunks, and checks 41 exact PASS lines. Five local executions completed in the development environment. Do not equate this with GitHub Actions passing; no remote CI PASS has been obtained or asserted here. No large archived physical ZIP or bot-authored GitHub commits were added.

## External literature and novelty audit

Garey–Johnson (1979) Theorem 3.9 and appendix SP6 already establish NP-complete all-pairs minimum test selection; the original final-printing erratum changes the cardinality-2 restricted complexity statement. Classical group *base* theory concerns a globally trivial pointwise stabilizer, whereas b_r concerns absence of SHORT nontrivial stabilizer elements within B_(2r). The word metric changes the finite classification but does not make generic pointwise-stabilizer methods novel. See Laison, McNicholas and Seaders, Discrete Mathematics 342 (2019), 2994–2999, DOI 10.1016/j.disc.2019.06.001. Rubik word-distance exhaustions and symmetry quotients are also known technology; see Rokicki, Kociemba, Davidson and Dethridge, SIAM Journal on Discrete Mathematics, DOI 10.1137/120867366.

**Real current value:** a physically specified, completely finite and reproducible radius-restricted sensor-base classification; a human-readable 12-element stabilizer reduction; a 41-goal independently checkable positive certificate; concrete 13-turn and B7 collision witnesses; full source/assumption/provenance traceability. A paper claiming new *general complexity* or generic *group-base method* from these ingredients would overstate novelty.

## Hard review and next gate

1. Retain the independent MITM proof as an important crosscheck for the 156 positive layouts. Keep former negative proof separate and perform a stand-alone audit of b6>=16; only both together fully certify b6=16.
2. Seek a shorter geometric/word-metric explanation for why the four incidence classes, rather than other omitted-tag patterns, avoid all stabilizer elements within B12. A non-enumerative >=13 certificate or smaller checkable PDB would improve explanatory strength.
3. Validate physical semantics against a SECOND independently written cube engine for stronger model-level independence; current independent proof algorithms share the same original 54-facelet oracle.
4. Audit current literature on radius-restricted resolving/identifying sensor families before publication. Do NOT switch the project into generic FSM protocol benchmark comparisons, invent new arbitrary indices, or start unmotivated B8 bulk enumerations.
5. Research claims must be labeled SOURCE / DERIVED THEOREM / EXECUTED FINITE CERTIFICATE / OPEN NOVELTY throughout. The GitHub repository preserves executable bytes and Notion preserves the evolving argument and decisions.

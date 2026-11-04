# CUBE-REV 0.28 — Source-independent P48 B6 41-distance closure and one-erasure backup-core spectrum

**2026-11-04.** Scientific verdict: **independent 48-sticker positive B6 distance certificate PASS (41/41; local and remote CI)**. This is a computational theorem for the stated fixed-centre 3×3 oriented-original-cubie sensor model. **Submission remains on HOLD** for final coverage auditing, novelty review, and manuscript preparation.

## A. What was genuinely changed

Earlier B6 MITM used independently written search logic but generated both target states and its 20×24 factor action table from an archived 54-facelet engine. The new system derives the 48 individually labelled moving stickers from lattice positions/outer normals; directly composes 18 physical HTM moves; generates tagged-cubie stabilizer states by corner permutation/twist and edge permutation/flip subject to legality; and exports an independent 18×20×24 factor transition table from the sticker physics itself. It **does not read the archived 54-sticker engine, its 41 goal manifest, B6-positive projection flags, or B6 distance oracle**.

New code:

- [P48 physical goal and 20-factor table generator](../../scripts/cuberev-observation/b6_independent_48sticker_goals.py)
- [P48 geometry and adversarial regression tests](../../scripts/cuberev-observation/test_b6_independent_48sticker_goals.py)
- [P48 exact 41-target MITM](../../scripts/cuberev-observation/verify_b6_41_mitm_p48.cpp)
- [Read-only CI](../../.github/workflows/cuberev-028-independent-p48-mitm.yml)

Checks: 48 distinct moving stickers; 18 physical HTM moves/inverses; 864 spatial conjugation/generator tests; 324 ordered two-turn exact sticker-versus-factor composition tests; a known genuine 13-HTM two-edge flip endpoint; geometric 156 candidate designs in eight proper-rotation layout orbits; 88 nonidentity stabilizer entries -> 74 distinct full P48 states -> 41 classes under the 48 signed spatial cube symmetries and inversion. The 41 class-size histogram is (17 singletons, 19 doubles, one triple, four quadruples), matching the prior abstract class structure, without reading the prior physical goals.

## B. Exact finite decision proof

For the symmetric generating set of 18 HTM face moves and legal fixed-center cube group G, define B6(x) as the six-ball around x. Since all generators admit inverses, the midpoint identity yields

```
B6(1) ∩ B6(g) is empty    iff    d_HTM(1,g) > 12.
```

The C++ program enumerates the complete HTM ball in a normal form forbidding adjacent same-face moves and canonically ordering commuting opposite-face moves. These rewrites never increase word length. The resulting solved ball has **8,331,112 normalized word paths** and **8,240,087 distinct legal full oriented-cubie states**. A pair of packed 64-bit values stores all 20 factor IDs (12 edges × 5 bits and eight corners × 5 bits); hash equality always checks both full packed words. A hash collision alone cannot produce a false match.

For each P48-derived representative goal, enumerate the exact six-ball and look for complete full-state equality with the solved six-ball. No intersection was found in any of 41 full searches; each completed exactly 8,331,112 goal-path probes. This implies **d_HTM(1,g)>=13 for every one of the 41 independent representatives**. It does *not* imply d=13 for every representative.

| Batch | Representatives | Goal probes | Verdict |
| --- | ---: | ---: | --- |
| 0..7 | 8 | 66,648,896 | PASS |
| 8..15 | 8 | 66,648,896 | PASS |
| 16..23 | 8 | 66,648,896 | PASS |
| 24..31 | 8 | 66,648,896 | PASS |
| 32..40 | 9 | 74,980,008 | PASS |
| **Total** | **41** | **341,575,592** | **PASS** |

**Actual remote Actions run:** [41763106125](https://github.com/WhoSia/CUBE-REV/actions/runs/41763106125), commit `8401e4220fb480104add61d8ef6d289b51a14fde`; job `independent-physical-b6` completed SUCCESS. Logs were directly checked for all five `P48_CERTIFIED` lines, the final `INDEPENDENT_P48_B6_41_ALL_PASS` marker, six passing source tests, and artifact upload. Exact artifact ID **13290449539**, archived bytes SHA-256 `f80b9f6f234df7d47b2666b1c912b978b329cd630b77275cc3b19b1e4d29dd17`, with 30-day retention.

Remote generated P48 table SHA-256: `33ab96ee24228febc89740676078d7abb0967a468b3aba338e4e6ea75eb3a021`.
Remote 41-goal text SHA-256: `363edfb2f25b267735f93895103125ba97e457c14937499955f4bf4e7bcdcba8`.
Remote canonical raw P48 goal permutation bytes SHA-256: `f73c09094a4ed327f4ab8f9295c3dd1cbdc139b312e3d52ea998591a3ff685b9`.

The local five batches also completed, with raw goal SHA matching the remote and table SHA matching the remote. The goal TEXT SHA differs between local and remote because of the header comment, NOT because of goal identities. The local self-contained execution ZIP is separately available in the conversation; the remote Actions artifact preserves generated table, goals and logs.

## C. Rigorous dependency boundary and upgraded status

For each proposed B6 16-tag layout S, the four-case geometric classification omits two adjacent original corner tags and two original edge tags. Legal pointwise stabilizer `H_S` has precisely 12 elements (`S3 × C2`; 2 matched permutation parities × 3 corner twist states × 2 edge flip states) and 11 nonidentity elements. There are 156 proposed layouts in eight proper 24-rotation layout orbits. Conjugation by spatial cube symmetry permutes HTM generators (reflections map quarter turns to their inverses), so word distance is invariant. Inversion preserves distance for symmetric generators. Thus all 1,716 nonidentity layout-element obligations reduce to the 41 P48 classes now checked. Therefore **all 156 geometric candidate layouts are positive B6 16-tag sensor bases in a second physical model**.

This upgrades the B6 positive-upper-bound physical independence substantially. It does NOT rederive the four-case rule's exclusion of all other size-16 layouts; the **156-layout completeness/negative classification** continues to inherit the previous B5/B6 physical obstruction certificates. The lower bound `b6>=16` still inherits the verified B5 15-tag impossibility proof and its source lineage. Consequently `b6=16` is supported by distinct sources, but do not call the entire minimum+all-optimal-layout theorem completely independently reconstructed without separately auditing its negative classification.

## D. New exact *backup-core multiplicity* theorem (conditional on 156-layout correctness)

Let S_e be any of the 12 minimum one-permanent-erasure-robust 19-tag designs: all eight original corners plus all edges except a single originally labelled edge e. For any observed sensor v in S_e, define

```
m_e(v)= number of B6-positive 16-tag bases T with T subset (S_e without v).
```

By exact geometric incidence of the 156 positive 16-tag layouts:

- S_e contains **26 distinct** positive 16-tag sub-bases.
- For the **11 deletable selected edge tags**, `m_e(v)` takes multiplicities **1 (4 cases), 2 (1), 3 (4), 4 (2)**.
- For the **8 deletable corner tags**, multiplicities **4 (2 cases), 6 (4), 10 (2)**.
- The total deletion/core incidences are **26 + 52 = 78**.

A direct double counting independently verifies the last equality: every one of the 26 sub-bases has precisely `19-16=3` surplus sensors within S_e, so it survives exactly three of the 19 possible one-sensor deletions, giving `3×26=78`.

All 12 choices of e yield exactly the same histograms by cube symmetry. Across the 66 possible unordered excluded-edge pairs in a sixteen-tag candidate, the numbers of compatible omitted-corner edges are: multiplicity 1 for 24 pairs, 2 for six pairs, 3 for 24 pairs, and 4 for 12 pairs. Thus **every pair** can be completed to at least one of the 156 positive geometric layouts. This provides an explicit constructive basis extension for each post-failure 18-tag design.

Independent geometry checker: [audit_b6_single_erasure_core_multiplicities.py](../../scripts/cuberev-observation/audit_b6_single_erasure_core_multiplicities.py). It passed in local execution and the GitHub P48 CI. The result is *not* an additional lower-bound proof or a new general theory of fault-tolerant bases; its paper value is a sharp physical geometry and failure redundancy description.

## E. Further paper-specific questions and hard limitations

1. Can the four-case permitted-edge-pair rule be proved with a short incidence-geometry argument based on the **specific HTM short-support obstruction classes**, without relying on a stored full B6 negative mask list?
2. Can the 25-component exchange graph and the new 1/2/3/4 versus 4/6/10 backup-core spectrum be unified by a single local cuboctahedral incidence model? Does it explain why some otherwise symmetric erasures have only one available core?
3. Is there an older exact result for *radius-bounded labelled full oriented-cubie bases* that supersedes this paper? No comprehensive priority claim has yet been established.
4. The oracle here reads persistent *originally labelled cubie full position and orientation*. It is **not** a real-human perception experiment, an unlabeled color observation, or a generic graph landmark metric dimension.
5. The P48 model and MITM have now passed a second physical-generation implementation, but a truly different third-party independent verifier or formal proof checker remains desirable before a high-confidence journal submission.

**Publication verdict:** genuinely upgraded exact finite Rubik observation paper candidate; **GO for manuscript development, HOLD submission and broad novelty claims**. Preserve all older negative-control failures, source SHAs and source-authority boundaries. CI read-only, GitHub commits authored/committed by WhoSia only.

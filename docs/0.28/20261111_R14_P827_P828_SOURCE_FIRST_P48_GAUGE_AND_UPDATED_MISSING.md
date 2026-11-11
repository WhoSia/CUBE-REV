# CUBE-REV 0.28 R14-P8.27–P8.28 — Historical P48 Isomorphism, Sixfold Gauge, Original-Source Custody

Date: 2026-11-11. Research branch: `research/current`. This is a SOURCE-FIRST and actually locally executed independent validation of the entire 48-moving-sticker face-turn representation against Hans Zassenhaus (1982), Physica 114A (1982), 629–637, DOI 10.1016/0378-4371(82)90362-4. Original PDF (central Research OS `10_PAPERS`) Drive ID `1i0gVO3XuLtBYZSknKCaMChTXJ641D59U`, SHA-256 `2be2f364e19b75db0ac67f6daca1e1448534f780daccdb256ae74e059da8adf0`.

## 1. Eight original PDFs newly added to intake: actual custody

All eight PDFs were inspected for source title/version and moved with metadata-only operations from Research OS `00_INTAKE` to central `10_PAPERS`. Their original IDs, original file sizes and destination parent were verified by Drive metadata readback. Each complete original PDF was independently fetched, locally SHA-256 hashed and recorded by original Drive ID in `data/0.28/R14_P827_20261111_EIGHT_PRIMARY_SOURCE_PDF_SHA256_DRIVE_CUSTODY.json`; a raw copy is preserved in CUBE-REV's own [P8.27 data folder](https://drive.google.com/drive/folders/1HT6QRLNlMs0wGJRInyq-ur8BcWjfjZuq). Seven of the eight are directly relevant to CUBE-REV; Ingelman-Sundberg(2002) is a separate toxicology source correctly centralized as a paper, not used to claim Rubik novelty.

New scholarly originals:

- Zassenhaus (1982), *Rubik's Cube: A Toy, a Galois Tool, Group Theory for Everybody*, `1i0gVO3XuLtBYZSknKCaMChTXJ641D59U`, original Journal PDF (original six 48-sticker four-cycles).
- Knuth, *Efficient Representation of Perm Groups*, `1Thzd-fEXGIME5BwpVxaqhuXmOgnL8rb_`, 1991 manuscript, arXiv upload 1992 `math/9201304v1`; do NOT call it a 1991 arXiv submission without provenance.
- Leon (1991), *Permutation Group Algorithms Based on Partitions, I*, `1cRJ8tyDVPYsDZb1-8zHkGudyPVmgClDA`, Journal Symbolic Computation 12:533–583.
- Jefferson, Pfeiffer, Wilson & Waldecker (2021), *Permutation Group Algorithms Based on Directed Graphs*, `1XX3n7aoQF_sGOg5QMsv8ufR5s1IFrJSA`, Journal of Algebra 585:723–758, CC BY open access.
- Angluin, Krikis, Sloan & Turán (1997), *Malicious Omissions and Errors in Answers to Membership Queries*, `1L4QsPx5ULNZmQfJ8kbyhoYQD8y0MzpSN`, Machine Learning 28:211–255.
- Ron & Rubinfeld (1995), *Learning Fallible Deterministic Finite Automata*, `1Q2d8Lg6MqC1fF4vpBGWgPAACXB53WFGE`, Machine Learning 18:149–185.
- Mereb & Vendramin (2024 first arXiv; v3 dated 2026-11-02), *Rubik's as Galois': The Inverse Galois Problem for the Rubik's Cube Group*, `175mqiTNreeuGbT4-CBfxSuhYpItbkTQL`, PREPRINT `arXiv:2411.11566v3`. Distinguish original 2024 preprint date from v3 upload date; this is about Galois realizability, NOT our observation horizon problem.
- Ingelman-Sundberg (2002), *Polymorphism of Cytochrome P450 and Xenobiotic Toxicity*, `1qtGkUo5FWhfSe-OmTn4fRLtnX4b4eXN1`, Toxicology 181–182:447–452, unrelated paper, left in general 10_PAPERS.

Incoming `Erev Roth AER 1998.pdf`, MQR historical texts, traffic/chemistry sources and suspected duplicates were left untouched by CUBE-REV because neither their domain nor provenance justifies automatic movement.

## 2. Raw Zassenhaus (1982) six full 48-sticker generators

The original journal PDF, not an external summary, prints six permutations `T1`..`T6`, each composed of exactly five disjoint 4-cycles on the 48 original moving stickers labelled positive 1..24 (corners) and negative -1..-24 (edges). All 30 literal cycles were transcribed in the new Python regression source; source notation `lO`, `ll` was checked as `10`, `11`, and `-l` as `-1`. The set of commuting opposite generators is exactly pairs indexed (T1,T6), (T2,T5), (T3,T4).

Independently generated coordinate geometry: each source sticker is `(p,n)` with cubie position p in {-1,0,1}³ having exactly two/three nonzero components, face normal n one of ±basis directions incident to p. Exactly 48 coordinates arise. Each physical face quarter turn rotates cubie position and sticker normal by the corresponding 90° rotation, without importing the older P48 engine or historical source table into geometry generation.

## 3. Full explicit source-to-coordinate conjugacy

For historical generator T_i, coordinate face-turn R_{f(i)} and sign eps_i in {+1,-1}, seek a full bijection phi from all 48 historical sticker indices to 48 physical coordinates such that:

    for every i=1..6 and every source label s, phi(T_i(s)) = R_{f(i)}^(eps_i)(phi(s)).

Test all 6! source-generator to face assignments and 2^6 quarter-turn direction assignments, prune using exact opposite-face commuting pairs, and propagate candidate sticker index bijections from single seed stickers in each transitive 24-label component. Every candidate mapping must be bijective and satisfy all 6×48=288 exact generator/sticker equations. All 48 valid face/direction assignments are found; 24 with all positive directions, 24 with all negative directions.

**Important P8.28 refinement of P8.27:** Earlier we stored only the FIRST corner/edge sticker map for each of 48 face/direction assignments, hence 48 valid REPRESENTATIVES. Exhaustively enumerating all 24 possible target corner-sticker anchors and all 24 target edge-sticker anchors for each fixed generator choice revealed precisely **3 valid corner maps** and **2 valid edge maps**, with independent combination. Therefore each of 48 allowed face/direction assignments has **6 different full bijections**, yielding **288 exact full P48 generator conjugacies** in the enumerated generator-alignment model.

These six residual mappings are the full simultaneous centralizer of the six generators for a fixed face/direction assignment: one threefold global corner-sticker cyclic gauge combined with an independent twofold global edge-sticker flip gauge. Thus the centralizer is isomorphic to C3×C2 (also C6), not trivial. This is a *representation labelling* degree of freedom, not six extra physical cube states or extra physical cube rotations.

The full search is finite and exhaustive: once the six generator images are assigned, each 24-sticker component is generated by the six transforms from a single source anchor; the image of an anchor uniquely determines any equivariant map on that component. Enumerating all 24 possible physical anchor images on each orbit checks every possible equivariant map, and the inverse-image constraints reject non-bijective collisions. All 6 generator label assignments are considered in the face map loop. No stochastic assumption, no shortest path engine, no new Rubik diameter proof.

**Locally executed:** after the initial 48-map run, an independent exhaustive-anchor check explicitly found `(corner_maps,edge_maps)=(3,2)` for ALL 48 generator assignments, total 288. The P8.28 verifier now computes this entire enumeration and asserts sixfold gauges and 288 distinct bijections.

## 4. Raw original data deposited IN CUBE-REV Google Drive

[CUBE-REV R14-P8.27/P8.28 source and raw data folder](https://drive.google.com/drive/folders/1HT6QRLNlMs0wGJRInyq-ur8BcWjfjZuq), under CUBE-REV's `20_SECONDARY_DATA_FRONTIER`, includes:

| Physical raw Drive file | Drive ID | Exact SHA-256 |
|---|---|---|
| P8.27 original single-representative-per-generator receipt JSON | `1GCeRhS0AbV2OYqMW81u0MFgycuLEvBAz` | `2d5716b0f7e085689ee05dfcd2e1c0f810d1350daed0b7fd24155de4da11fd67` |
| P8.27 actual independent Python source v1 | `1s_DOVn5mSGJ_chYYEP6C0w5MLep4ADUa` | `5bc78c817f35f918585223cef00766f73ae9d269cc680819059fa0654def37bf` |
| P8.27 full 48 representative map dataset | `1ysxJwrDWOtUhMZGbRqqNLw-G-dTUgM2i` | `5f16d48018fb10201249acf78cd1cdcb2986eedaab7cf41df8c75a1d2aa49482` |
| P8.28 revised exhaustive verifier | `1cvGc90HTZtC6uHRvVSr0LOcgu_FNFzA9` | `0569bbf4e9ed3371bc96bb6fac16ed64a16b4dc213116f2800f21b8cad22100d` |
| P8.28 corrected full 288 counts JSON | `1nux_cpm0kPwX6UGdHgNyIDozaNZCEWFt` | `92f4458523a0c2cdc4f43f3952624a716e5ce13522730ece5811bc939fbbc6b7` |
| **P8.28 all 288 full sticker map dataset** | `1tVQdI-ulxxHVsLF5Ta8L1u4qixm7rkwj` | `901c8b72dedf187ea739e6289a76b0ec679a485f6f2e5c83551019afeb74ae6b` |
| 8 new primary PDFs complete raw SHA256/Drive ID manifest | `1DBe9bons0BBZW6xze3T3RMNJhj7vBA4S` | `02c6bd0dad719889d0a585cf9abc9f8899f372a04f7f6ea09c00e445b408f619` |

ALL seven P8.27/P8.28 source, receipt and map raw files were independently downloaded BACK from Drive after upload and compared byte-for-byte via the recorded SHA-256; all seven passed. The eight-source PDF custody manifest was also downloaded back and SHA-256 checked. This demonstrates raw-byte upload custody, not validity of external published mathematical claims. The original historical versions were NOT overwritten; v2 adds additional completeness evidence.

GitHub work (human WhoSia, research/current) preserves independent verifier `scripts/cuberev-observation/audit_r14_p827_zassenhaus_original_48_sticker_conjugacy.py` now updated for P8.28, read-only `.github/workflows/cuberev-r14-p827-historical-p48-conjugacy.yml` now expects 288; original first-48 GitHub v1 JSON retained for historical audit; corrected P8.28 JSON at `data/0.28/R14_P828_ZASSENHAUS_1982_EXACT_288_GAUGE_GROUP_RECEIPT.json`. Actual GitHub Actions run verdict has NOT been observed, do not mark remote PASS.

## 5. Relevance and novelty review

This is significantly stronger than comparing the support sizes of basic face turns. We have an explicit conjugacy between source-original P48 and independently built 3D face-turn geometry, plus exact quantified residual indexing freedom. It verifies the *physical group-action layer* of prior CUBE-REV certificates against an independently printed 1982 primary-source generator table. It does NOT reproduce the full 41-target B12 geodesic/HTM shortest-path certificate, prove all B6 minimal layouts B7-fail, or resolve Paper B unrestricted h_adaptive. The 6-label gauge warns that original cubie orientation conventions should be pinned when comparing scripts, while physically invariant injectivity/collision claims transport through a full bijective conjugacy.

Scientific follow-up: map one representative of each of the 8 proper-rotation orbits of 156 B6 optimal 16-tag layouts to physical P48, enumerate their 11 nonidentity stabilizer elements (order 12) and compute the **shortest 18-HTM length** of each (13–20), supported by fresh independent meet-in-the-middle certificates. That yields the first-failure-radius distribution across 156; do not infer b7 from one orbit. This is more meaningful than inflating the manuscript count.

## 6. Updated MISSING original literature and raw-data gates

Prior missing originals RESOLVED in this intake: Zassenhaus 1982, Knuth 1991 manuscript / 1992 arXiv upload, Leon 1991, Jefferson et al 2021, Angluin et al 1997, Ron–Rubinfeld 1995. Already owned Angluin (1987) and Rivest–Schapire (1993) (Drive titles verified), do not re-add. Blaha 1989 PhD and 1992 journal, Sims 1970/1971, Jerrum 1986, Bshouty 1995, Bshouty et al 1996, Bisht et al 2008, Rivest 1987 remain owned from preceding session.

Core ORIGINAL still not found by title/author Drive searches (not an absolute global absence statement):

1. Harary & Melter (1976), On the Metric Dimension of a Graph, Ars Combinatoria 2 191–195 (publisher contacted previously).
2. Slater (1975), Leaves of Trees, Congressus Numerantium 14 549–559 (publisher contacted previously).
3. Hennie (1964), Fault Detecting Experiments for Sequential Circuits, NASA NTRS 19650037493 catalog record only.
4. Vasilevskii (1973), Failure Diagnosis of Automata — exact Russian original versus English title metadata unresolved.
5. Hopcroft (1971), An n log n Algorithm for Minimizing States in a Finite Automaton — original conference chapter not located.
6. Sokolovskii (1971), Diagnostic Experiments with Automata — original source/translation relationship unresolved.
7. Furst, Hopcroft & Luks (1980), Polynomial-Time Algorithms for Permutation Groups, FOCS 36–41: not yet owned original PDF; full institutional technical report PDF `80-442.pdf` appears openly at Cornell eCommons https://hdl.handle.net/1813/6282 but has not been copied into Drive. Must label Cornell TECH REPORT vs FOCS original separately.

Additional source-trail candidates screened and not confirmed as exact originals in Drive: Singmaster (1981), Notes on Rubik's Magic Cube (BOOK, belongs 11_BOOKS); Bandelow (1982), Rubik's Cube and Beyond (BOOK, 11_BOOKS); Golomb (1981), Rubik's Cube and a Model of Quark Refinement (American Journal of Physics ARTICLE, 10_PAPERS); McKay & Piperno (2014), Practical Graph Isomorphism II (JSC ARTICLE, 10_PAPERS); Babai (1979–1982) original short-base bound papers (exact identity needed, HOLD). Do not confuse existing 1991 Knuth preprint with different 1990–1992 published bibliography titles.

Missing ORIGINAL RAW ledger separate from literature: 2026-10-30 historic `CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip` not located, expected SHA256 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94; raw b5_sixteen_layout_census.json/independent_b4.py chain missing; original 41 B6 positive HTM distance receipts and 872-minimal conflict certificates exist in previous records but were not independently re-run here; P8.21 P48 96-category CI receipts and P8.23/P8.24 explicit B7 code remote PASS not observed; 609376 Paper B conditional edge assignments and unrestricted adaptive 19 frame case still open; Lean 4 kernel receipt still unobserved. No false closure claims.

## 7. Reproducible next gate

1. Check actual P8.28 read-only Actions success and its generated artifact, then mark physical cross-implementation provenance VERIFIED_REMOTE; 2. Independently derive the sixfold centralizer without relying on all-candidates brute-force (orbit-stabilizer structural statement); 3. Bind Zassenhaus 48 historical labels to physical original-cubie orientation conventions, fix the C3×C2 gauge in explicit data; 4. Replay certified B7 word under BOTH original numbering conventions; 5. Scan source and thesis provenance again before updating the missing table. No global b7 minimum claim unless all 156 representative orbits are resolved.
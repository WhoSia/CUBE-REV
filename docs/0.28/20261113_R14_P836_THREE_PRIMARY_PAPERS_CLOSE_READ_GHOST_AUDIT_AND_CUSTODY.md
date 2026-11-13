# CUBE-REV 0.28 R14-P8.36 — Primary-paper intake, close reading, and ghost-bibliography audit

**Date:** 2026-11-13. **Scientific scope:** independently examined PDF bytes already supplied by the investigator in Research OS `00_INTAKE`, cross-referenced actual authoritative publisher/conference records, and moved **three new scholarly article PDFs** metadata-only into the canonical `10_PAPERS` folder (same exact Drive IDs and byte sizes). No assertion of full systematic prior-art coverage or novelty priority.

## 1. Admitted and read originals

### A. Wang, Wang, Shi & Li (2022) — monocular cube recognition (4 pp.)

- Full official title: *Research on State Recognition of Rubik's Cube Based on Monocular Vision*. Authors: Mihang Wang, Yigang Wang, Qing Shi, Shi Li. Conference: **2022 14th International Conference on Signal Processing Systems (ICSPS)**, conference dates 18–20 November 2022; added to IEEE Xplore 25 August **2023**. DOI [10.1109/ICSPS58776.2022.00141](https://doi.org/10.1109/ICSPS58776.2022.00141); IEEE document [10218571](https://ieeexplore.ieee.org/document/10218571/).
- PDF identification: authentic IEEE four-page proceedings layout, pp. 777–780; original Drive file id `1ny5tJVihORd9BxDwrYsBymKLYDmMBhXN`; 507,476 bytes; SHA-256 `a6c1a2579f07fe7e87518b513834d8b496b4660bbc18a1a11585166cd389d49a`.
- Method: a **single optical camera** obtains simultaneous HSV color-region and geometric contour information from full images, KNN separates difficult colors, parallel-line and barycenter tests identify frames suitable for recognition, and Kociemba solving plus augmented-reality overlays guide users. It is *not* a single six-symbol color reading and not an original-cubie identity-orientation sensor.
- Evidence: Section IV reports **20 repeated user-guided cube-solving demonstrations**; these are empirical demonstrations, not 20 zero-error observation probes or an exhaustive proof over `|G|≈4.3252×10^19` legal states.
- **Correction needed:** introduction claims an approximate `430 billion` Rubik state count, which is substantially incorrect for the legal 3×3×3 fixed-center group (43,252,003,274,489,856,000). The paper's mention of about `20 steps` is Kociemba *solving moves* (Sec. III.C), not the twenty *observation frames* of CUBE-REV. Never equate or transfer either number.
- Citation danger: the authors' "one sensor" refers to a **camera apparatus** that observes many pixel/color values in a frame; it does not establish our two-spatial-sticker categorical-query minimum or rule out feedback benefits in that strictly weaker channel. The PDF carries an IEEE authorized-access restriction line; keep original privately in Drive, do not publish its bytes in GitHub or redistribute.

### B. Futuhi & Sturtevant (2026) — admissible-heuristic learning (31 pp.)

- Full title: *Learning Admissible Heuristics for A*: Theory and Practice*. Authors Ehsan Futuhi and Nathan R. Sturtevant; **ICLR 2026 conference paper**. Stored source is **arXiv:2509.22626v2, ICLR-accepted front matter**, not an anonymously fabricated 2026 title; publisher abstract [ML Anthology](https://mlanthology.org/iclr/2026/futuhi2026iclr-learning/), [arXiv record](https://arxiv.org/abs/2509.22626), [OpenReview proceedings PDF](https://openreview.net/pdf/a2ec379ef8af5d8ddc561a995d9dc45580a6d816.pdf).
- PDF id `15GM1mtoAicpgEwgafy7QQt3VxVvEaDF3`; 1,132,182 bytes; SHA-256 `83cf227e681565cd309fd4d4d947897d52c861352dc43de2bb7201e89b773154`; 31 pp.
- Core: define a Cross-Entropy Admissibility (CEA) loss over distance classes to favor underestimation, analyze expected A* suboptimality/generalization and neural-network sample complexity; train cube *pattern database* heuristics based on edge/corner abstractions.
- Important precise empirical caveat: Table 2 reports **nonzero** overestimation rates for several CEA models (7-edge 2×10^-5; 8-corner 3×10^-7; 6-edge 9×10^-5; delta (6,4)-edge 3×10^-6). The paper calls them near-admissible. Finite small overestimation is not the same as a universally certified lower bound; CUBE-REV exact 41-target B6 exclusion cannot take a learned heuristic value as a proof of HTM distance >=13 without separate admissibility certification. Their PDB sizes, target distances and empirical A* performance have a different aim from static observations and posterior decision trees.
- Caution: the PDF is a *versioned preprint carrying conference-accepted markings*. Preserve version metadata and avoid claiming that its bytes are identical to the official publisher PDF without comparison.

### C. Harker, Vogel & Gedeon (2007) — map-seeking Rubik optimization (14 pp.)

- Title: *Analysis of Constrained Optimization Variants of the Map-Seeking Circuit Algorithm*. Authors S. R. Harker, C. R. Vogel, T. Gedeon. **Journal of Mathematical Imaging and Vision 29, 49–62 (2007)**, DOI [10.1007/s10851-007-0024-7](https://doi.org/10.1007/s10851-007-0024-7), published online 31 August 2007. Available genuine author [2007 manuscript](https://math.montana.edu/gedeon/documents/clanky/vog-sh-ged.pdf) differs in formatting from archived Springer journal article: do not confuse the two document manifestations.
- Drive file id `1P4XAjtmSI3O6FazqQhQKPUclqQ48P-S9`; 653,754 bytes; SHA-256 `027da82141cb5628ae3b258451c433997e1238e5caf0e409816d3827f5dba463`; 14 pp.
- Crucial prior representation: Section 2.2 represents **each original edge/corner cubie by a 24-component one-hot state**: twelve edge locations×two orientations, or eight corner locations×three twists. Thus a 24-state per-original-cubie factor encoding is prior work; CUBE-REV must claim originality only in *exact word-metric restricted sensor selection and physical witness completeness*, not the mere factor representation.
- Formal optimization: the map-seeking circuit converts composition of finite discrete transformations into multilinear correspondence maximization over relaxed coefficient layers. The authors analyze geometry of global/local constrained extrema and compare MSC, projected-gradient (PG) and SQP algorithms.
- Section 5.2: 100 random cube problems at each scramble depth L=2 through 12, assessing success frequency and CPU time. This is a **randomized solver experiment**, *not* exhaustive 20-tag sensor-layout classification or a 41-target HTM lower-distance proof. The conclusions explicitly note an unresolved generic global-convergence issue for MSC; no full Rubik solver optimality guarantee should be attributed to it.

### Intake-side fourth older PDF

`am_2016042515583550.pdf` in `00_INTAKE` is **Sathish Krishnan & Bharati Rajan (2016), *Fault-Tolerant Resolvability of Certain Crystal Structures*, Applied Mathematics 7, 599–604**, DOI `10.4236/am.2016.77055`, 6 pp, SHA-256 `36b961e1e7a57ddf9fbc099c01968a7b551255fc684129d1b7c047054d197b23`. It concerns vertex-distance metric dimension of graph models for crystals, not persistent original Rubik cubie pose observation or the color-frame adaptive horizon. We inspected its identity but **did not move it as one of the investigator-specified three new cube papers**. If processed later it belongs in 10_PAPERS as a distinct journal paper, not in CUBE-REV's three-paper intake ledger.

## 2. Custody changes actually completed (three files only)

Original location: Research OS Literature Commons `00_INTAKE — Literature Radar` (folder ID `1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16`).

Destination: Research OS `10_PAPERS — Canonical Literature Commons` (ID `1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP`).

1. [Wang et al. (2022) IEEE ICSPS PDF](https://drive.google.com/file/d/1ny5tJVihORd9BxDwrYsBymKLYDmMBhXN/view): `Wang et al. (2022) — Research on State Recognition of Rubik's Cube Based on Monocular Vision — IEEE ICSPS DOI 10.1109-ICSPS58776.2022.00141.pdf`
2. [Futuhi & Sturtevant (2026) ICLR/arXiv v2 PDF](https://drive.google.com/file/d/15GM1mtoAicpgEwgafy7QQt3VxVvEaDF3/view): `Futuhi & Sturtevant (2026) — Learning Admissible Heuristics for A* - Theory and Practice — ICLR 2026 arXiv 2509.22626v2.pdf`
3. [Harker, Vogel & Gedeon (2007) journal PDF](https://drive.google.com/file/d/1P4XAjtmSI3O6FazqQhQKPUclqQ48P-S9/view): `Harker, Vogel & Gedeon (2007) — Analysis of Constrained Optimization Variants of the Map-Seeking Circuit Algorithm.pdf`

All three were updated via **Drive metadata-only rename+parent move**, with **no uploaded replacement bytes**, and their exact IDs, PDF MIME type, bytes sizes and destination folder IDs were verified in independent post-move Google Drive metadata reads. No new Drive duplicate was created.

## 3. Seven legacy core missing papers — ghost test and exact authority links

These seven named records are all **real works**. Their *absence from 10_PAPERS* is a separate file-custody issue, not evidence that they are fabricated.

| Work | Bibliographic authoritative verification | Source access / edition caveat |
| --- | --- | --- |
| Harary & Melter (1976), *On the Metric Dimension of a Graph* | [Journal's own 1976 Ars Combinatoria 2 index](https://combinatorialpress.com/ars/vol2/), pp. 191–195; MR 0457289 | Real journal paper, publisher issue index verified. Standalone authorized original PDF not yet preserved in 10_PAPERS. |
| Slater (1975), *Leaves of Trees* | [Published secondary journal bibliography](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v31i2p13/pdf/); *Congressus Numerantium* XIV, pp. 549–559 | **Proceedings contribution**, not a standalone research journal issue. Direct original proceedings article PDF not custodied. |
| Hennie (1964), *Fault Detecting Experiments for Sequential Circuits* | [NASA NTRS record](https://ntrs.nasa.gov/citations/19650037493) plus [dblp FOCS 1964 page](https://dblp.org/db/conf/focs/focs64.html), pp. 95–110 | **Conference paper**; NASA catalogue explicitly has no article download. Do not mistake an unrelated NASA report citing it for the 1964 original. |
| Vasilevskii (1973), *Failure Diagnosis of Automata* | [Springer original metadata](https://link.springer.com/article/10.1007/BF01068590), *Cybernetics* 9, 653–665 (1973); translated from *Kibernetika* 4, pp.98–108 (Jul–Aug 1973) | Crucial correction: some tertiary metadata shows **1975**; publisher explicitly states 1973 for this DOI/version. Primary Russian and English translation are distinct manifestations; neither PDF yet verified in canonical corpus. |
| Sokolovskii (1971), *Diagnostic Experiments with Automata* | [Springer](https://link.springer.com/article/10.1007/BF01068822), *Cybernetics* 7, 988–994 (1971); translation of *Kibernetika* 6, pp.44–49 (Nov–Dec 1971) | Confirmed article; issue/pagination must distinguish Russian original and translation. |
| Hopcroft (1971), *An n log n Algorithm for Minimizing States in a Finite Automaton* | [Publisher chapter metadata](https://www.sciencedirect.com/science/article/abs/pii/B9780124177505500221), *Theory of Machines and Computations*, pp.189–196 (1971) | [Free Stanford technical-report mirror](https://ftpmirror.your.org/pub/misc/bitsavers/pdf/stanford/Stanford_CS_TR_Collection_2025-12-12/PDF/1971/CS-TR-71-190.pdf) is a different source manifestation, not publisher chapter PDF. |
| Furst, Hopcroft & Luks (1980), *Polynomial-Time Algorithms for Permutation Groups* | [FOCS 1980 proceedings list](https://www.sigmod.org/publications/dblp/db/conf/focs/focs80.html), pp.36–41, DOI [10.1109/SFCS.1980.4567802](https://doi.org/10.1109/SFCS.1980.4567802) | [Cornell Technical Report 80-442, free official repository](https://ecommons.cornell.edu/entities/publication/f360d936-ad6c-47ab-8ceb-105c662e23d0) is real, downloadable separately; **not identical** to FOCS pp.36–41 version. |

## 4. Five optional historical references — correction and non-ghost triage

1. **Singmaster (1980/1981), *Notes on Rubik's Magic Cube*** — [MacTutor original-edition account](https://mathshistory.st-andrews.ac.uk/Extras/Singmaster_books/) and [1981 Enslow fifth edition in Google Books](https://books.google.com/books?id=UGIPAQAAMAAJ). Fifth-edition **1980 privately distributed notes vs 1981 Enslow** require edition-specific labels. Real book, not article.
2. **Bandelow (1982), *Inside Rubik's Cube and Beyond*** — [WorldCat 1982 Birkhäuser Boston book](https://search.worldcat.org/title/Inside-Rubik%27s-Cube-and-Beyond/oclc/858919114). Real *monograph*, belongs to 11_BOOKS if separately acquired.
3. **Golomb (1981), *Rubik's Cube and a Model of Quark Confinement*** — **Correction of earlier erroneous journal attribution:** *American Journal of Physics* 49(11), 1030–1031; DOI [10.1119/1.12577](https://doi.org/10.1119/1.12577). Not *American Mathematical Monthly*. The paper exists.
4. **McKay & Piperno (2014), *Practical Graph Isomorphism, II*** — [Journal of Symbolic Computation 60, 94–112](https://www.sciencedirect.com/science/article/pii/S0747717113001193), DOI [10.1016/j.jsc.2013.09.003](https://doi.org/10.1016/j.jsc.2013.09.003). [ANU institutional open research record](https://openresearch-repository.anu.edu.au/items/03873592-21e5-404f-b906-eabe335f5163). Real paper.
5. **"Babai — early permutation-group base research"** — **NOT A VALID CITATION AS WRITTEN**: lacks year, definite title, publication, pages and identifier. It is a **topic placeholder**, not an identifiable missing paper and should be excluded from the count of verified specific bibliographic objects until a concrete primary record is selected. Do not ghost-label a named scholar; reject the vague item as an invalid paper claim.

## 5. Impact on integrated C0.3

The 2022 IEEE item blocks claims of novelty for "using only one cube sensing device". Its experimental 20 actions and 20 demonstrations are not our exact 20 categorical **observation frames**. Harker (2007) predates our use of 24-valued per-original-piece pose variables. Futuhi & Sturtevant (2026) show high-quality learned cube PDB heuristics but residual **nonzero** overestimation rates, which are not proof certificates of exact word-distance lower bounds. C0.3 should make these scope distinctions explicit with *full read original PDF references*, rather than carrying P8.35's previous metadata-only status.

**Publication priority is still unresolved** until broader exact-model adjacent work is found and examined. The three acquired PDFs resolve all three new P8.35 "missing original" intake flags and should be removed from the active missing list. Historical seven-core originals remain to obtain, with exact authority links above. The vague Babai line should not count as a real missing bibliographic item.

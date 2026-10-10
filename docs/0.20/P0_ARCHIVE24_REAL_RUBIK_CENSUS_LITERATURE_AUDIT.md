# CUBE-REV 0.20 — P0/P1: 24.md Historical Rubik Audit, Source-Locked Real-L5 Cut Census, and Missing Primary Literature

**Formal programme:** CUBE-REV 0.20 — Structural Laws of Physical Identifiability: Action-Transported Observation Codes, Restricted Perfect Hash Families & Proof-Carrying Covering Complexity.

**Source status:** Historical facts below originate in `24.md` (Drive file ID `1LEwsLIaHsXfpd1_T88HVO7fq29O5eqCH`, 312,548 UTF-8 bytes; archived exchange October 10, 2026 01:38–16:06 KST). Historical dialogue is a research claim log, not a self-validating proof. Independently checked facts are marked separately.

**Archive SHA-256 (verified locally):** `4b66db19314fd54bc4e026b82335b26a03c95d0be8235d1dafe403051cb33cfa`.

## 1. Exact recovery of the mathematical Rubik research sequence

1. **0.18 L4:** real UR tracked-edge 24-state transition maps, initially twelve flip-zero positions; original 1,192 admitted 3/4/5-state requirements; fixed four-turn words; 104,976 words -> 1,913 observation partitions -> 1,477 cover types -> 1,323 maximal cover types. Physics-preserving row/column reductions produce 398x168 incidence, with separate 334x80 and 64x88 integer covering components. Small component exact 7-word lower bound from standard-library search (33,846 states and 45,010 branches). Later externally accepted DRUP proof for hard component yields integer 27+7=34. Do not project the factorization to other horizons without a fresh proof.
2. **0.19 observational changes:** 18^5=1,889,568 legal fixed words -> 14,938 distinct five-observation partitions. The five-turn physical covering graph is not the same component split as L4. Retaining more bits for a fixed word refines its partition, but counting *distinct partitions across all words* is not monotone in observation access.
3. **P1 early horizon:** only F/F'/B/B' can flip the intrinsic bit in this physical convention. Actions that never flip can transport physical edge positions before an informative later action. L<4 cannot meet admitted five-source demands. F/B-only word confinement has at most three histories regardless of length.
4. **P3–P8:** physical incidence-preserving 16-element automorphism group, exact rational LP for full 1,192 `16/3`, exact rational LP for restricted 480 `185/39`, true physical column orbit versus unsound orbit-variable collapse; higher-order collision obstruction instead of pairwise clique packing.
5. **P9–P12:** rank-sensitive exact finite integer certificates establish minimal 7 words for restricted 480 five-source rows. A particular seven-word optimum covers 1,120/1,192 full rows, leaving 64 new maximal quartets and 8 implied face triples. The residual cannot be repaired with one fixed physical word (maximum residual coverage 36).
6. **P13:** original full family's L5 minimum is locally exactly 8 (seven-word impossibility split by number `t` of rank-seven words, t0–7; original physical eight-word cover). New external CI full P13 success was not verified at archive closure. Exact horizon profile `infinity,infinity,infinity,infinity,34,8,4,3,2,1,...` pertains solely to this frozen physical ontology.
7. **New 0.20 mathematical re-entry:** keep actual physical cube as primary explanatory object. Finite automata and combinatorics serve the cube, not replace the cube with detached toy results. Maintain the WhoSia-only commit author/committer rule, preserve rejected DRAT logs and old OPEN statuses as history.

## 2. New P1 real Rubik transported-cut phase census (independent local finite check)

Inputs: `SOURCE/original_physical.json` (SHA-256 `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`), original sticker-derived `SOURCE/original_move_maps.txt` (18x24), original physical partition authority `SOURCE/original_L5_partitions.tsv` (14,938 partitions). No synthetic cube moves were introduced.

**New C++ implementation:** [census-L5-transport-cuts.cpp](../../scripts/cuberev-020/census-L5-transport-cuts.cpp) (C++20; 18^5 leaf enumeration directly through 24-state physical move maps; 12 zero-flip starts; cumulative observations; 4-bit canonical set-partition encoding). **Independent checker:** [verify-L5-census-source.py](../../scripts/cuberev-020/verify-L5-census-source.py) (Python 3 standard library; verifies SHA, exact original TSV partition-set equality, q-indexed counts). Input SHA and TSV source identity must be independently checked: the C++ program itself declares an expected SHA but does not hash the original JSON.

| Informative moves q | Actual words | Max rank | >=5 rank words | Exactly rank 7 words | Unique rank-7 partitions |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 537824 | 1 | 0 | 0 | 0 |
| 1 | 768320 | 2 | 0 | 0 | 0 |
| 2 | 439040 | 4 | 0 | 0 | 0 |
| 3 | 125440 | 7 | 43584 | 128 | **16** |
| 4 | 17920 | 7 | 6912 | 512 | **16** |
| 5 | 1024 | 3 | 0 | 0 | 0 |

**Exact observed q-dichotomy:** all 32 distinct highest-rank L5 physical observation partitions decompose as a **disjoint union of 16 generated by q=3 and 16 generated by q=4**. No highest-rank partition is obtainable in both q phases. The exhaustive raw move word census matches 14,938 original partition keys exactly, not only the count (Python key-by-key symmetric difference empty). Independent local checker result: `CUBE_REV_020_L5_TRANSPORT_CUT_CENSUS_INDEPENDENT_PASS`.

**Novelty and generality:** this is an exact *fixed Rubik physical model census*, not a proof of a universal two-phase splitting law. The next mathematical target is to derive from transported F/B four-slot cuts, prefix permutation constraints and time ordering *why* two rank-7 phase families are disjoint, and check whether their 16+16 form survives other lengths or sensors. Blind extrapolation from the census is prohibited.

**Offline reproduction with the 0.19 P13 37-file ZIP extracted:**
```sh
c++ -std=c++20 -O3 -Wall -Wextra -pedantic scripts/cuberev-020/census-L5-transport-cuts.cpp -o /tmp/cuberev020-l5
/tmp/cuberev020-l5 SOURCE/original_move_maps.txt /tmp/cuberev020-partition-keys.txt > /tmp/cuberev020-L5-census.json
python scripts/cuberev-020/verify-L5-census-source.py --physical SOURCE/original_physical.json --tsv SOURCE/original_L5_partitions.tsv --census /tmp/cuberev020-L5-census.json --partition-keys /tmp/cuberev020-partition-keys.txt
```

## 3. Missing primary sources: live Drive name-index audit 2026-10-10

These are **not found as appropriately named standalone papers** in connected Drive via exact `name contains ...` provider filters; a copy buried in unidentified ZIPs, proceedings or under an uninformative filename remains possible. Verify metadata/DOI and licence before ingesting. Do not conflate bibliographic metadata with a downloaded PDF.

**P0–P2 highest priority**
- Chong Shangguan & Gennian Ge (2016 preprint/2017 journal), *Separating Hash Families: A Johnson-Type Bound and New Constructions*. arXiv `1601.04807`, DOI `10.1137/15M103827X`. Direct competing extremal separation system geometry, hypergraph bounds.
- Simon R. Blackburn (2000), *Perfect Hash Families: Probabilistic Methods and Explicit Constructions*. DOI `10.1006/jcta.1999.3050`. **Author is Blackburn, NOT D. R. Stinson.** Check legitimate full-text access.
- Bart Bogaerts, Stephan Gocht, Ciaran McCreesh & Jakob Nordström (2022), *Certified Symmetry and Dominance Breaking for Combinatorial Optimisation*. DOI `10.1609/aaai.v36i4.20283`, arXiv `2203.12275`. Required for proof-producing 16-fold incidence automorphism reductions.
- Stephan Gocht, Ciaran McCreesh & Jakob Nordström (2022), *An Auditable Constraint Programming Solver*. DOI `10.4230/LIPIcs.CP.2022.25`. Required for precise evidence-grade comparisons with VeriPB and branch proofs.

**P2 extensions, secondary priority**
- D. R. Stinson, R. Wei & L. Zhu (2000), *New Constructions for Perfect Hash Families and Related Structures Using Combinatorial Designs and Codes*. DOI `10.1002/(SICI)1520-6610(2000)8:3<189::AID-JCD4>3.0.CO;2-A`.
- Huaxiong Wang & Chaoping Xing (2001), *Explicit Constructions of Perfect Hash Families from Algebraic Curves over Finite Fields*. DOI `10.1006/jcta.2000.3068`.

**Already present in Drive; do not collect duplicates:** Procacci & Sanchis (2017) *Perfect and Separating Hash Families*; Lee & Yannakakis (1994) *Testing Finite-State Machines*; Gill (1961); Rivest & Schapire (1993); Panteleev (2015); Türker et al. (2016); McKay (1998); Saxena (2004); selected Gonthier proof papers and Szeider (2026). A readable full original paper is not guaranteed by the presence of a citation or proceedings index; verify when used.

## 4. Remaining falsifiers, governance and no-premature-claims

- Test whether q=3 vs q=4 class disjointness follows from invariant intersection patterns of transported physical cut-support families, or if it is a horizon-specific accident.
- A suffix-sound `(g,Pi)` automaton representation is exact and classical, but state-equivalent prefixes may need an even smaller bisimulation quotient. Compare such quotient only after specifying remaining horizon and test family.
- Current `research/current` GitHub P7 active-set CI still rejected extra tracked research files; preserve source data rather than delete scientific receipts or quietly whitelist arbitrary paths. Audit its manifest separately.
- Old 0.18 claims were correctly graded in their own time: `30<=M*(4)<=34` was once the honest interval before external DRUP. Do not read a stale historical entry as today's frozen optimum.
- External complete P13 GitHub Actions checker success still must be read from a completed run artifact before upgrading the local computer-assisted result.

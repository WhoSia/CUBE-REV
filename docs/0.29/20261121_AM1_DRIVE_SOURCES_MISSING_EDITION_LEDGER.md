# CUBE-REV 0.29 AM1 — Drive source-custody and missing-primary ledger
**2026-11-21 · scoped recheck against connected Google Drive and 38–40 archives · branch `research/current`**

## Scope and evidence labels
This is **not** a global negative search proving that a source does not exist anywhere in the user's Library. The operation inspected targeted Google Drive title/author search hits, readable extracted content for selected owned PDFs, CUBE-REV's older source and missing registers, and the 38/39/40 historical chat archives. `HELD-TEXT` means an owned Drive PDF with readable extracted passages inspected; `HELD-HOLD` means an owned PDF with incomplete edition/full-text validation; `EDITION-GAP` means a useful related version is owned but a specified *different original edition* was not located; `NOT-FOUND-SCOPED` means targeted searches found only secondary citations or other works.

## A. Verified relevant owned books and technical sources

| Source | Custody evidence | What is actually useful for CUBE-REV | Status |
| --- | --- | --- | --- |
| Diestel (2017), *Graph Theory*, 5th ed. | [Drive original](https://drive.google.com/file/d/1T2pB-wAv7RXLsXTVJ7I5EkllVdIKxBWd/view) | Section 2.1 matching/Hall, concrete proof of initial edge-color histogram feasibility | HELD-TEXT |
| Schrijver (2003), *Combinatorial Optimization: Polyhedra and Efficiency* | [Drive original](https://drive.google.com/file/d/1Y7TMSTkLxvmhpQEkyiPhPm9WiLJb3MaD/view) | Ch. 22.1–22.1a, matching/transversal and dual certificates | HELD-TEXT |
| Chekuri (2022), *Combinatorial Optimization* lecture notes | [Drive notes](https://drive.google.com/file/d/1_NdMZy6A0w_owAK5BtasY9c-6LPqJe5g/view) | Theorem 5.11 Hall, demand-token proof | HELD-TEXT |
| Seress (2003), *Permutation Group Algorithms* | [Drive book](https://drive.google.com/file/d/1kUj3ajt6Fq_O8S9omgyUEHnbTAazItne/view) | Ch.4 base/strong generating sets, Schreier–Sims and stabilizer chains | HELD-TEXT |
| Cameron (1999), *Permutation Groups* | [Drive book](https://drive.google.com/file/d/14WWOUzTUy7PVuFcr5cnX0O2Fsfxqif/view) | §§1.10,1.13,1.17: wreath product, stabilizer chains, sign | HELD-TEXT |
| Bailey & Cameron (2011), *Base Size, Metric Dimension and Other Invariants* | [Drive article](https://drive.google.com/file/d/1PSS1zaeX_CD6VVuxrP1H6AfrYXscktuV/view) | Definitions: group bases/graph resolving sets are not equivalent to this feedback color sensor | HELD-TEXT |
| McKay & Piperno, *Practical Graph Isomorphism, II* | [Drive arXiv v1 copy](https://drive.google.com/file/d/1iQ38YgNK14g1lCazcHUS7Y6CvNujXbuf/view) | Canonical labels, individualization/refinement, stabilizer orbit quotient; preserve preprint/version metadata | HELD-TEXT |
| Leon (1991), *Permutation Group Algorithms Based on Partitions I* | [Drive journal original](https://drive.google.com/file/d/1cRJ8tyDVPYsDZb1-8zHkGudyPVmgClDA/view) | Partition backtrack for canonicalization | HELD-TEXT |
| Jefferson et al. (2021), *Permutation Group Algorithms Based on Directed Graphs* | [Drive journal original](https://drive.google.com/file/d/1XX3n7aoQF_sGOg5QMsv8ufR5s1IFrJSA/view) | Digraph refinements and subgroup actions, not automatically a Rubik proof | HELD-TEXT |
| Sims (1971), *Computation with Permutation Groups* | [Drive conference original](https://drive.google.com/file/d/12ESPckYd--MAe0_V6-E5wsqsTXiAOd4A/view) | Base/stabilizer chain and coset representative computation | HELD-TEXT |
| Hopcroft (1971), *An n log n Algorithm for Minimizing States in a Finite Automaton*, Stanford TR | [Drive Stanford report](https://drive.google.com/file/d/12GrNUvr5mff-IP43DY13Vvev5Pi2sFbx/view) | Exact state partitions and refinement; distinct query/transition model | HELD-TEXT |

**Do not assert full-volume close reading** merely from passage searches: only targeted relevant chapters/abstracts/sections were inspected during this session. Readable text is not a raw-byte SHA custody check.

## B. Previously listed gaps now owned in Drive

| Old missing or uncertain primary | Current observed Drive file and edition verdict |
| --- | --- |
| Zassenhaus (1982), Rubik group original | [Original PDF now searchable](https://drive.google.com/file/d/1i0gVO3XuLtBYZSknKCaMChTXJ641D59U/view); remove generic missing-original flag |
| Vasilevskii (1973), *Failure Diagnosis of Automata* | [Original/translation PDF](https://drive.google.com/file/d/17l_o-qW9esqefiBl73bc3OzBa4sR6Y3N/view); source-translation bibliographic distinction remains |
| Sokolovskii (1971), *Diagnostic Experiments with Automata* | [Owned PDF](https://drive.google.com/file/d/1LGuVfwiMk7mk_lT6egC36F4iING6XBIf/view); retain Soviet/English edition hold |
| Furst–Hopcroft–Luks (1980), *Polynomial-Time Algorithms for Permutation Groups* | [Cornell institutional technical report scan](https://drive.google.com/file/d/1iKzVZUu7U1KQhc7kK5RPKkVO2RrG-a0a/view); the separate exact FOCS proceeding remains an EDITION-GAP. Drive extraction returned empty; no claim of full text read |
| Knuth (1991), *Efficient Representation of Perm Groups* | [Owned preprint/arXiv uploaded 1992](https://drive.google.com/file/d/1Thzd-fEXGIME5BwpVxaqhuXmOgnL8rb_/view); exact 1991 journal edition NOT established |
| Kunkle & Cooperman (2007), *Twenty-Six Moves Suffice for Rubik's Cube* | [Owned PDF](https://drive.google.com/file/d/1bXfHbYpbmyfuTcwlW3B8MsiozDOOYIRe/view) |
| Kunkle & Cooperman (2008), *Solving Rubik's Cube: Disk Is the New RAM* | [Owned PDF](https://drive.google.com/file/d/1BqQF5HH6c7kSBio7tLVK6L3_bLUGZDJX/view) |
| Kunkle & Cooperman (2009), *Harnessing Parallel Disks to Solve Rubik's Cube* | [Owned PDF](https://drive.google.com/file/d/1nFHnOr_ATu03w2OTKkIFup_KER8Y1VfB/view) |
| Kociemba, original two-phase algorithm primary web documentation | [Owned overview](https://drive.google.com/file/d/1b_MJzkHcHUcyd_qN1_LmhPAaCu51dunW/view), [coordinates](https://drive.google.com/file/d/12-i6WyZPz19tkQkppRqZXLHtgd_9UDJi/view) and [solvers](https://drive.google.com/file/d/1A7TpihkiS63is_c16gwdoIOG7NX79815/view); do not confuse the two-phase *solving* metric with the weak observation *identification* model |
| Angluin et al. (1997) / Ron & Rubinfeld (1995) | [Angluin et al. owned](https://drive.google.com/file/d/1L4QsPx5ULNZmQfJ8kbyhoYQD8y0MzpSN/view), [Ron–Rubinfeld owned](https://drive.google.com/file/d/1Q2d8Lg6MqC1fF4vpBGWgPAACXB53WFGE/view); separate automata/noise models |

All above status claims refer to concrete retrieved files and should not be copied into the historical 2026-11-11 missing ledger as if they had been held then. Preserve historical provenance and add a dated new ledger instead.

## C. Targeted negative search and edition holds (as of this session)

| Priority | Source | Current status | Research role and caution |
| --- | --- | --- | --- |
| High historical | Harary & Melter (1976), *On the Metric Dimension of a Graph*, *Ars Combinatoria* 2:191–195 | NOT-FOUND-SCOPED | Original graph metric-dimension provenance; Khuller–Raghavachari–Rosenfeld (1996) replacement is owned; their criticism of an older proof forbids uncritical citation |
| High historical | Slater (1975), *Leaves of Trees*, *Congressus Numerantium* 14:549–559 | NOT-FOUND-SCOPED | Early locating/resolving sets; not essential for current Hall and parity proof |
| High FSM history | Hennie (1964), *Fault Detecting Experiments for Sequential Circuits* | NOT-FOUND-SCOPED | NASA NTRS 19650037493 has catalog evidence, but no directly downloadable original PDF was located; do not cite as close-read |
| Exact edition | Furst–Hopcroft–Luks (1980) FOCS proceedings edition | EDITION-GAP | Cornell technical report owned but different artifact; original conference-specific byte provenance remains open |
| Exact edition | Knuth (1991) *Combinatorica* journal edition | EDITION-GAP | arXiv-uploaded earlier manuscript owned; verify exact changes before direct claims from published journal |
| Metadata | Sokolovskii (1971) Russian/English version relation | HELD-HOLD | PDF held; retain exact bibliographic provenance check |

**Updated missing-table integrity rule:** distinguish original missing bytes, scholarly preprint vs published edition, unreadable image scan, and merely absent title matches. Do not re-add owned texts as a missing resource. The current structural Hall–Burnside result does not depend on acquiring any missing paper, and its proof should not be delayed by a historical bibliography gap.

## D. Literature-guided method choice, not borrowed originality

1. **Current proof:** Hall's theorem on `K_{2,2,2}` identifies which first-eleven color histograms can occur. Finite 64-subset graph check is a verification of a mathematical criterion, not a 12! search.
2. **Current proof:** Burnside's lemma and signed opposite-pair cycles explain 52 histogram representatives. Canonicalization must preserve a gauge representative because 40/52 have nontrivial stabilizers.
3. **Current proof:** Wreath-group generator parity shows `sign(12-edge action)=sign(three-pair action)`. Proven universal sign law requires formalising the composition identity with the actually chosen stable sort.
4. **Next proof:** Graph bisimulation / posterior-partition refinement for the 52 continuation decision trees. The relevant equivalence is **colored, signed, query-and-reply alternating**, not simple graph isomorphism or an unlabelled node count.
5. **Next proof:** 18-frame lower bound remains an adversarial simultaneous probe game; graph matching does not replace the existing certified lower DAG. 19-frame complete Lean policy has not yet been constructed.

Researcher-reviewer objections to preempt: Is the 48-action really an edge-game automorphism? yes for the 12-type color graph, but not necessarily a global fixed-center physical cube symmetry. Is the terminal parity available before the last required corner observation? not in general. Does collapsing 1362 to 52 orbits imply 19-frame correctness? no; it only reduces the distinct root histogram classes.

## E. Reading receipts / references

[38.md](https://docs.google.com/document/d/1i1PGJXEGjkZUINXKDmO2MtIKuJI9MR6r/edit) and [39.md](https://docs.google.com/document/d/1AJLxObjP8VMi44uDvRW-aOd7mbxYUejR/edit) contain historical priority shifts, earlier missing-list amendments, and scientific cautions. [40.md](https://docs.google.com/document/d/1YvgD4yVMhb2jbj1iaT5QcQEQZWPWSOQA/edit) fixes manuscript versions and the 18→19 proof priority. The older [P8.22](../0.28/20261111_R14_P822_EXTENDED_MISSING_LITERATURE_AND_RAW_EVIDENCE.md) and later [P8.25/P8.26](../0.28/20261111_R14_P825_P826_UPDATED_MISSING_AND_SCIENTIFIC_AUDIT.md) should be read chronologically, not as two simultaneous inventory states.

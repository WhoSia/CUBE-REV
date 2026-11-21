# CUBE-REV 0.29 AS0 — 2026-11-21 Research OS 00_INTAKE primary-source ingestion receipt

**Research OS folders:** [source 00_INTAKE](https://drive.google.com/drive/folders/1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16) → [canonical 10_PAPERS](https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP).
**Source clock:** four PDFs were uploaded on 2026-11-21 at 11:52:58–11:53:34 UTC. The original Drive item IDs were preserved across rename/move; **no file content was rewritten**. Google Drive returned successful moves and a separate files.get readback found precisely the canonical 10_PAPERS parent for each. A post-move 00_INTAKE folder listing returned **zero remaining files** at that instant.

## Four exact primary bytes and source editions

| Original intake filename | Publication / truthful edition classification | Original PDF size, pages | Raw SHA-256 (source bytes) | Final canonical Drive original |
| --- | --- | --- | --- | --- |
| `Knuth-paper.pdf` | Donald E. Knuth (1991), *Efficient Representation of Perm Groups*, *Combinatorica* **11(1):33–43**, **the eleven-page journal typesetting**, not the separately owned 1992-uploaded arXiv manuscript | 639,435 B, **11** pages | `f1643ef7e41c3b481419c4c13fd8b1949a2cf01eb99c2ff40ff1b9bf8c45d167` | [Knuth journal PDF](https://drive.google.com/file/d/1mIhQ-9tchQp-quRSkFyFF5AY0m1HTdaZ/view) |
| `babai1981.pdf` | László Babai (1981), *On the Order of Uniprimitive Permutation Groups*, *Annals of Mathematics* **113(3):553–568**. **17 PDF pages** = JSTOR metadata cover + 16 printed article pages, with additional proof note in printed last page | 1,068,721 B, **17** pages | `e55a09f7fe6e8d1e9bbee4a565f55c677a739c8cd73f72378f84ba6c8804fded` | [Babai journal scan](https://drive.google.com/file/d/1PdBg2ByUtXQQ61k47DHHxPUQ4J0C1j4r/view) |
| `2104.07201v1.pdf` | Richard C. Tillquist, Rafael M. Frongillo & Manuel E. Lladser (2021), *Getting the Lay of the Land in Discrete Space: A Survey of Metric Dimension and Its Applications*, **arXiv:2104.07201v1**, manuscript dated/submitted 2021-04-01. **Not** the exact SIAM Review 2023 typesetting | 715,140 B, **29** pages | `8590ffa50c8022e820a35ea49c91784f3efaa37996eaf97624cdbb50a0457b92` | [Tillquist et al. 2021 v1](https://drive.google.com/file/d/16LLu5qEg_NkvN7B8nwXPUL3bbnhz2zuv/view) |
| `furst1980.pdf` | Merrick Furst, John Hopcroft & Eugene Luks (1980), *Polynomial-Time Algorithms for Permutation Groups*, **21st IEEE FOCS, printed pp. 36–41**. Actual six-page conference artifact, not the previously owned Cornell technical report | 572,158 B, **6** pages | `f2658d3888ef3a4f2ea814624d037726b2658830bb2a4a2188f61ed0e06d058e` | [Furst–Hopcroft–Luks IEEE FOCS original](https://drive.google.com/file/d/1AhZmbHGT_8RnIZ3D4OoSTdZK7aZLYvkF/view) |

**Raw SHA method:** the source PDF was read as raw bytes, its PDF magic `%PDF-` and byte count verified, SHA-256 computed independently in JavaScript from the Drive raw response and in container Python `hashlib.sha256` on the same source snapshot. All four 64-digit digests matched exactly; the generic SHA implementation also passed the known `abc` test vector. Pages and visible journal title/printed page numbers were verified using PyMuPDF and the rendered first/last-page contact sheet. The JSTOR cover and the 2021 arXiv manuscript date are explicitly identified instead of being silently treated as publication pages.

**Important boundary:** SHA was computed on the **pre-move raw file snapshot**, whereas Google Drive post-move verified metadata, same file ID, name and parent. No second post-move full-byte SHA was computed; since the move was metadata-only this is expected to be unchanged, but a future custody auditor can independently rehash the current Drive item for a post-move seal. The source eprint from 2021 is not asserted byte-identical to the SIAM 2023 article.

## Scientific reading: exact useful primary passages and limits

### Knuth 1991

Section 1 develops transversal-system data structures for permutation groups, while §2 gives recursively maintaining strong generators by algorithms `A_k` and `B_k` with a correctness proof. Section 4 analyzes worst-case complexity and data storage; §5 warns that even a **conjugate permutation obtained by a two-point relabeling** can significantly change the sparse tableau and membership-test workload. This last example is directly useful for our critical analysis of the 48-color normalizer: two mathematically equivalent orbit representatives can have different computational search traces. It motivates retaining an explicit normalizing witness rather than assuming every gauge produces identical traversal cost or sign convention. We do *not* claim Knuth proved the CUBE-REV 19-frame threshold.

### Babai 1981

The original Annals article introduces a pointwise **fixing set** and related distinguishing number for coherent configurations in the introductory reduction of its bound on uniprimitive group order. It proves a bound for a different general permutation-group action using hypergraph covering ideas. In CUBE-REV the 11-color histogram group orbit and the exact signed posterior are observation-model-specific; Babai's fixing set is not interchangeable with shortest-path graph metric dimension or paired sticker feedback. This original is important as a **historical and methodological constraint on novelty claims** around small bases, distinguishing sets, and group actions.

### Furst–Hopcroft–Luks 1980

The FOCS six-page paper (pp.36–41) proves polynomial-time algorithms for central tasks with finite permutation groups represented by generators, using pointwise-stabilizer chains, coset tables and **sifting/membership tests**. Theorem 1 constructs coset representatives; Theorem 2 concerns straight-line programs and a polynomial-size DAG of group calculations. This suggests exact approaches to normalize candidate-subgroup actions and cache equivalent subproblems **without** an explicit traversal of all physical cube states. However, their computational group's word/DAG construction is not the same as CUBE-REV's **response-labeled adaptive observation policy DAG**, which must satisfy a separate causal correctness proof.

### Tillquist–Frongillo–Lladser 2021 v1

The 29-page survey defines graph metric dimension via vectors of **shortest-path distances to selected landmark vertices**, discusses NP-complete optimization and heuristics, and includes applications to canonical labeling and network identification. CUBE-REV reads **categorical sticker colors** and permits **sequential response-adaptive paired probes**, so one cannot cite a metric-dimension result as if it gave a cube probe bound. It is supporting background for separating observation families, not an equality of sensor models. The later 2023 SIAM Review journal edition remains a specific edition-acquisition gap if the publication final version is needed.

## Missing-primary ledger consequence

**Newly resolved exact source gaps:** Knuth 1991 journal typesetting, Babai 1981 journal original, Furst–Hopcroft–Luks 1980 IEEE FOCS proceedings. **2021 preprint newly acquired:** Tillquist et al. 2021; **2023 SIAM Review exact journal edition still outstanding**. As a result the pre-ingestion eight-item missing-only list must become **five current exact works/editions**, without mixing already owned books or adjacent versions:
Harary–Melter 1976; Slater 1975; Hennie 1964; Babai 1980 on strongly regular graph canonical labeling; Tillquist et al. exact SIAM Review 2023 journal version.

The older 2026-11-21 AR0 eight-item register is a **historical state before this 00 intake**, and should be preserved in Git history but replaced at the current canonical missing-only link by a dated revised five-item register. Do not add the four newly acquired files to a “missing” output.

## Reproducibility and research direction

**Scientific verdict:** ingestion is valuable for **algorithmic theory and citation precision**, particularly Knuth's transversal invariant and Babai's distinguishing sets. It does **not** directly discharge the unfinished Rubik 19-frame Lean theorem. The most useful AS next step is a generic *proof-carrying semantic compiler* interpreting already frozen `["read",addr,branches]`, `["repeat",dest]`, and `["leaf"]` graph nodes, partitioning the remaining first-color sector by actual observed reply and delaying sign-based terminal choice until the end of the nineteenth corner observation. This is preferable to enumerating another set of 12! assignments or multiplying state counts.

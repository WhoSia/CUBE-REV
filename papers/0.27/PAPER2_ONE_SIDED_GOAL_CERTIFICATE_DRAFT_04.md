# A Checkable One-Sided Goal Filter for Finite-Depth Geodesic Exclusion on the Rubik's Cube

**CUBE-REV Paper 2 — Research draft 0.4 (19 October 2026), incorporating P16 negative-cost result**  
**Status:** working technical manuscript; the full 17-move exclusion for the fixed instance has **not** been independently certified. All results below are from completed experiments unless explicitly marked as proposed.  
**Metric:** half-turn metric (HTM), all face quarter-turns and half-turns having unit cost.

## Abstract

A program that returns a shortest solution provides a candidate answer, but the claim that no shorter solution exists is more difficult to check. We study this distinction for a fixed, documented Rubik's Cube scramble for which an independent optimal solver reports an 18-move solution. We develop a certificate architecture that replaces an exact goal-side distance table by a one-sided set of fingerprints. The verifier must establish only that every state reachable within a specified goal-side radius is represented in the filter. False positive fingerprints can increase search work but cannot make a non-existent path appear absent. For a distance threshold of 17, a complete exclusion reduces to the absence of intersections between a source radius-10 ball and a goal radius-7 ball. We materialized the latter as 109,043,123 distinct 64-bit fingerprints, generated from an independently checked radius-6 checkpoint of 8,240,087 full 54-sticker states. A separate verifier completed all 156,561,653 required goal-side inclusion tests. A complete 15-child source court with shared prefix `14,1,4` excluded 90,800,620 canonical source nodes, and an independent checker rejected seven corrupted traversal receipts. In parallel, an unmodified external optimal solver and a conservative version with an additional equal-axis pruning rule removed both report a valid 18-move solution; neither alone constitutes a self-contained certificate excluding all 17-move words. We also tested a hybrid search using an independently certified 40,320-state corner-permutation distance table. On a smaller complete source/goal-radius-five court, it safely reduced membership queries but increased measured runtime; the audit boundary can be smaller without yielding a faster algorithm. Our completed result is the goal-side certificate and scoped source exclusions. The instance-wide independent proof that no solution of length at most 17 exists remains unfinished.

## 1. Introduction

The upper bound in an optimal-search claim is usually short. A solver can print a word, and an independent program can apply its moves to check that the stated cube is solved. The lower bound is different: unless all shorter possibilities are excluded with sound reasoning, an 18-move solution does not establish an optimal distance of 18. This difference is particularly visible in a finite group such as the Rubik's Cube, where the rules and all physical states are discrete but the collection of candidate words grows rapidly with depth.

Optimal Rubik's Cube solving is not new. Korf's pattern-database method established exact solutions for random cube instances using admissible subgoal distances [1]; Rokicki, Kociemba, Davidson, and Dethridge gave a large-scale computational proof that the group's diameter in HTM is 20 [2]. We make no claim to have invented bidirectional search, admissible pattern databases, or computational cube proofs. The question here is narrower: what does a reader need to verify a negative conclusion for **one identified physical instance**, if the original optimizer is not treated as an oracle?

Our answer separates two responsibilities. A producer can use whatever computation is convenient to assemble an overapproximation of states close to the goal. A small verifier checks that this overapproximation includes all required goal-side states. A source-side search can then establish the absence of intersection without depending on the producer's exact distance claims or its ability to detect hash collisions. This shifts part of the trust boundary from a large performance-oriented optimizer to a compact inclusion checker and a grammar-complete source enumerator.

We present the mathematics and a complete goal-side implementation on an authentic fixed scramble. We also state precisely the large remaining source-side computation. This is a useful intermediate technical result: the compact verification architecture is real, while the intended global exclusion theorem remains open.

## 2. Problem and physical instance

Let \(G\) denote the Rubik's Cube state group with the 18 face turns \(A=\{U,U',U2,R,R',R2,F,F',F2,D,D',D2,L,L',L2,B,B',B2\}\). The metric \(d_{18}\) counts each such turn as one move. We fix the solved state \(e\) and the source state \(s\) reached by the following publicly recorded scramble:

```
R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2
```

An 18-move solution was verified on the full labeled 54-sticker representation:

```
F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2
```

A separate optimal-search program subsequently returned another 18-move solution:

```
U' D' R2 F' D2 B' R F2 B U2 L2 U F U L U' F2 B2
```

The second word was replayed in both a separate geometric facelet implementation and the original native 54-site C++ move representation. Both sequences solve the same labeled physical source. Consequently \(d_{18}(s,e)\le18\). The independent optimizer also reports completion of a depth-17 search, but that output is subject to the soundness of the optimizer's projected pruning tables and its search implementation. It is not substituted for the independent certificate developed below.

For the certificate, a cube is recorded as 54 uniquely labeled sticker positions, rather than only nine colors on each face. This representation makes full-state equality and independent geometric replays unambiguous. When fingerprints are used, we hash this fixed physical representation with a deterministic 64-bit map \(H\); the hash does not replace the underlying semantics of the cube.

## 3. The single-cutoff theorem

Write \(B_r(x)=\{y\in G:d_{18}(x,y)\le r\}\). The HTM move generators have inverses of the same cost, and the Cayley graph is undirected. A path of at most 17 moves from \(s\) to \(e\) can be split after at most ten moves so that its remaining suffix has length at most seven. Conversely, joining two such paths gives a word of length at most 17. Therefore

\[
 d_{18}(s,e)\le 17
 \quad\Longleftrightarrow\quad
 B_{10}(s)\cap B_7(e)\ne\varnothing.
\qquad \text{(1)}
\]

The advantage of (1) is that a single exclusion encompasses all shorter solutions as well. No separate exclusion at depth 16 is mathematically required in the final certificate. In particular, if the intersection in (1) is empty, the independently verified 18-move word implies \(d_{18}(s,e)=18\).

A source-side enumerator need not generate every noncanonical word. Consecutive moves on the same face can be combined or canceled, and moves on opposite faces commute. By deleting such reductions and sorting commuting adjacent opposite-face turns in a fixed order, every HTM word has a length-nonincreasing representative satisfying a finite-state canonical grammar. Its completeness follows from local group identities; any canonical pruning must preserve an endpoint and never lengthen the word. The grammar is applied to words up to depth ten, including all shorter prefixes.

## 4. One-sided goal-filter certificate

Let \(H:G\to\{0,1\}^{64}\) be a deterministic fingerprint and let \(F\) be a sorted list of 64-bit integers. The verifier will establish

\[
 \forall y\in B_7(e),\qquad H(y)\in F.
\qquad \text{(2)}
\]

No claim that every element of \(F\) corresponds to a state in \(B_7(e)\) is required. This asymmetry is useful: additional fingerprints, including collisions, may cause extra candidate matches, but cannot hide a real intersection.

**Proposition 1 (one-sided exclusion).** Suppose (i) (2) holds; (ii) a source enumerator covers every endpoint in \(B_{10}(s)\), possibly with duplicates; and (iii) for each visited source endpoint \(x\) it establishes \(H(x)\notin F\). Then \(d_{18}(s,e)>17\).

**Proof.** Suppose otherwise. By (1) there is a state \(z\in B_{10}(s)\cap B_7(e)\). By the source coverage assumption, the enumerator visits \(z\), and its negative membership test gives \(H(z)\notin F\). But (2) gives \(H(z)\in F\), a contradiction. The proof uses no collision-resistance assumption. \(\square\)

If a fingerprint match occurs, the negative certificate for that branch must remain unresolved or fall back to whole-state checking. In particular, accepting a Bloom-filter-like negative conclusion only when every query returns `absent` is sound once inclusion and source coverage are secured. Counting hash-table entries by itself is insufficient.

### 4.1 Independent inclusion checking

We construct a complete physical solved-side ball \(B_6(e)\), then exploit the identity

\[
 B_7(e)=B_6(e)\cup\bigcup_{a\in A} B_6(e)a.
\qquad \text{(3)}
\]

A verifier independently checks that the checkpoint contains the complete \(B_6(e)\) (including the solved root, correct layer expansion, no duplicate state omission, and appropriate closure of preceding layers). It then checks that the fingerprint of every checkpoint state and all 18 of its one-move neighbors is present in \(F\). These are the only goal-side inclusion requirements. The verifier can accept a true superset even if the producer used a different sorting or sharding technique.

In the implementation, 64 disk partitions hold the sorted fingerprints. File checksums help detect accidental changes to the stored inputs, but they do not establish inclusion, search completeness, or physical correctness. Those properties are established by enumerated state transitions and the verifier's explicit tests.

## 5. Completed goal-side experiment

The independent generator reconstructed the exact seven BFS layer cardinalities for \(B_6(e)\):

| Depth | Newly reached physical states |
|---:|---:|
| 0 | 1 |
| 1 | 18 |
| 2 | 243 |
| 3 | 3,240 |
| 4 | 43,239 |
| 5 | 574,908 |
| 6 | 7,618,438 |
| **Cumulative** | **8,240,087** |

The physical checkpoint contains 8,240,087 records of 54 bytes, totaling 444,964,698 bytes. A separate checker verified all unique states and 11,189,682 layer-edge obligations. B6 construction took 18.61 seconds on the reported local host; the independent B6 audit took 13.76 seconds. These are measured, machine-dependent observations, not universal performance bounds.

The producer then emitted each checkpoint state's own fingerprint and all 18 neighbor fingerprints. This gave exactly \(8,240,087\times19=156,561,653\) generated fingerprints, divided into nine resumable batches and 64 partitions. External sorting and deduplication left 109,043,123 unique 64-bit entries, occupying 872,344,984 bytes. The merge completed in 27.41 seconds with peak memory around 70 MiB for that stage.

The independently compiled inclusion checker subsequently tested every required fingerprint, in two position-verified segments covering all 8,240,087 physical B6 states. Both segments passed, for all 156,561,653 individual obligations. A deliberately removed mandatory fingerprint was rejected. A deliberately inserted extra fingerprint was accepted. The latter test matters: treating a harmless false positive as invalid would silently change the intended one-sided theorem into a stronger, unnecessary exact-set requirement.

### 5.1 Completed limited source-side courts

For the canonical four-move prefix identified by action indices `14,1,4,7`, source search to depth ten visited 6,802,324 nodes and found no fingerprint hits in the checked B7 filter. The source action indices refer to the fixed original move ordering \((U,D,R,L,F,B)\), with powers in three consecutive positions per face, as specified in the software supplement. The corresponding older depth-11-with-B6 court covered 90,800,620 canonical virtual nodes, 5,806,714 physically visited after admissible pruning, and zero whole-state goal meetings. This comparison is local to one subcourt; it does not exclude the other source prefixes and must not be reported as the global no-17 result.

We next kept all 64 B7 partitions mapped in one process and explored **all 15 legal fourth actions** following the shared prefix `14,1,4`, reusing the same complete B7 filter throughout. The source-depth-ten court contained **90,800,620 canonical nodes**, including **83,998,296 depth-ten leaves**. The traversal made zero filter hits and completed in **143.50 seconds**, with **853,648 KiB** peak resident memory. A separate Python verifier recomputed the exact grammar mass of each fourth-action region, confirmed complete and nonduplicated coverage, and rejected **seven altered receipts** (missing region, duplicated region, false hit, wrong mass, false summary, missing proof marker, extra illegal child). The verifier rehashed the physical B6 checkpoint and all **64 immutable B7 partition files** and matched their pinned digests. This independently reconfirms the negative result for the fixed three-action prefix, conditional on the audited B7 inclusion certificate. **The same prefix had already been closed by the earlier P8 source11+B6 method**; P15 is a different proof mechanism and a cost measurement, not newly closed global coverage. The other third-action prefixes remain untested by this method.

For a same-host comparator, we also freshly executed the older C8/E6-pruned source-depth-eleven versus whole-B6 engine on **the same 15 fourth-action regions**. It accounted for **1,212,049,276 canonical virtual nodes** by **89,011,588 actual visits** and **1,123,037,688 admissibly omitted descendants**, with **83** exact whole-B6 probes and zero meetings. The run required **26.28 seconds wall time, 49.40 seconds CPU, and 1,218,448 KiB peak resident memory**. The new one-sided filter run consumed **143.44 seconds CPU and 143.51 seconds wall time**. Both were run on the same host, but the older engine used **four OpenMP threads** and reconstructed its goal resources at startup, while the new engine used one thread and the previously materialized B7 files. Their wall-time ratio is therefore *not* an apples-to-apples claim about asymptotic algorithm speed. Even accounting for threading, this experiment gives no support to the hypothesis that direct one-sided B7 lookup is faster. It is easier to audit, and the cost of that simpler trust boundary is measurable.

| Same original 15 fourth-action regions | One-sided source10 + B7 | Pruned source11 + B6 |
|:--|--:|--:|
| Canonical virtual nodes | 90,800,620 | 1,212,049,276 |
| Physically traversed nodes | 90,800,620 | 89,011,588 |
| Admissibly omitted nodes | 0 | 1,123,037,688 |
| Goal membership / full-state meetings | 0 / 0 | 83 / 0 |
| Wall time, seconds | 143.51 | 26.28 |
| CPU time, seconds | 143.44 | 49.40 |
| Peak resident memory, KiB | 853,648 | 1,218,448 |
| Parallel execution threads | 1 | 4 |


### 5.2 A certified small-oracle hybrid: fewer queries but slower search

An independently checked lower bound can remove entire branches without weakening the one-sided proof. Suppose a projection $\pi$ sends every physical HTM move to one move in a smaller state graph and an independent checker has established that $h$ never exceeds true distance from the projected solved state. Consider a source-search node $x$ at depth $k$ with $r-k$ source moves still permitted and a goal filter that contains $B_t(e)$. If

$$
h(\pi(x)) > (r-k)+t,
\qquad \text{(4)}
$$

then every state reachable from $x$ within the remaining source budget lies outside $B_t(e)$. No descendant need be looked up in the goal filter. This observation depends on the actual proof of admissibility of $h$ and the physical projection, not on the file checksum, numerical size, or asserted provenance of its lookup table.

To test the cost of this extra logic, we reused the **independently certified** 40,320-entry corner-*permutation* table rather than installing the large three-axis optimal-solver heuristic. The underlying checker verifies all 40,320 states and 725,760 HTM transitions; it rejected a perturbed distance table. In a smaller complete radius-five source/goal experiment on the same original scramble, physical BFS covered 621,649 distinct source states. At source depth five, the corner condition $h>5$ ruled out 139,704 of those states (22.5%) before the goal-filter lookup. In a canonical depth-five DFS, the grammar contained 624,124 word nodes, more than the number of unique physical states because the grammar does not demand globally unique endpoints. Applying (4) throughout this tree skipped 2,352 descendant word nodes and reduced filter queries to 494,659. The zero-hit result was unchanged; an additional solved-side radius-five control confirmed that no legitimate goal state was discarded by the certified corner bound.

The runtime outcome went against the hoped-for speed improvement. On the same executable and materialized goal filter, the direct canonical traversal required 0.153 seconds while the corner-augmented traversal required 0.386 seconds. In a separate whole-BFS two-pass lookup comparison, the unpruned filter scan took 0.262 seconds and the hybrid took 0.762 seconds. Both are short, host-specific timings rather than scalable throughput estimates. Reconstructing a corner-permutation coordinate from 54 sticker labels at every node cost more than the saved membership operations. The next optimization target is therefore **incrementally maintaining the certified projected coordinate during traversal**, not stacking more distance tables into the trust boundary.

The result has two implications. Small auditable lower bounds can coexist with a one-sided goal filter, so the architecture need not impose entirely unpruned source traversal. But an admissible branch predicate is not automatically an efficient branch predicate. A method paper must show both a correct certificate and an honest account of the work required to generate and check it. The present 40,320-state hybrid is an end-to-end physical test of the pruning contract, not a completed radius-17 certificate or an improvement over the optimized cube solver.

## 6. Complementary optimal-solver evidence

An independent installation of RubikOptimal 1.1.0 solved the fixed state in 18 face turns and reported an exhaustive pruned depth-17 iteration. A conservative rereun removed a stronger, initially unaudited equal-three-axes pruning rule. This second run also returned the same 18-turn word, generating 645,445,908 nodes at depth 17 and 1,947,210,938 in total. Independently reconstructed distances for all 40,320 corner permutations and all 725,760 corresponding corner transitions matched the installed solver's small corner tables.

These observations strengthen the case that the particular state has exact HTM distance 18. They do not replace a portable no-17 certificate because the much larger three-axis quotient distance tables, their symmetry-coordinate transitions, and their use in the external program have not yet received a complete independent finite-state audit. The status of the claim is thus **solver-backed exact 18, goal-side independent certificate complete, global source-side one-sided certificate incomplete**.

## 7. Discussion

The proof architecture addresses a practical difficulty in long negative searches. Conventional optimal solvers are built to reduce work; they can contain hundreds of megabytes of compressed tables, symmetry conventions, and nontrivial pruning conditions. A verifier that duplicates the entire implementation is not independent in the sense relevant to a computational proof. The one-sided filter gives another division of labor. Constructing it may be expensive, and it can be too permissive; however, validating its inclusion property requires straightforward whole-state enumeration from a smaller ball. The source traversal can use a simple canonical grammar and fail whenever a filter hit appears, without reusing the external optimizer's large projected-distance machinery.

The approach does not necessarily dominate a strong pattern-database search in runtime. It trades pruning power for a smaller trusted mathematical interface. The full source-side depth-ten canonical tree here contains roughly 264.5 billion nodes before any additional pruning, so building the goal filter alone is not enough. The P15 batched benchmark sharpened this concern: across 15 matching prefix sectors, the strong projected-oracle method finished substantially sooner on this host despite carrying a larger and more delicate trust base. Improving source-side traversal while retaining a small, independently checkable proof contract is now the main unresolved engineering question. The P16 hybrid experiment supplies a concrete counterexample to the tempting inference that fewer goal-filter lookups must reduce runtime. A measured, incremental coordinate update is required before claiming any speed improvement from an audited auxiliary distance table. Parallel partitioning, independently checked grammar counts, and durable per-prefix receipts are necessary before a global exclusion can be declared. Large files also raise a custody problem: preserving hashes for 444 MB and 872 MB inputs does not substitute for independently retrieving those exact bytes from a durable archive.

One-sided inclusion is a general device, not specific to the Rubik's Cube. Any finite reversible planning system with complete smaller goal balls and a sound state identifier could use a similar goal-side superset to prove bounded unreachability. The underlying set-theoretic inclusion argument is elementary and should not itself be advertised as a new search theorem. Any convincing method contribution will have to demonstrate that the proposed verifier contract materially reduces the independent trust burden on a completed large instance or across several test cases, with a fair comparison to existing checked search certificates. This remains unestablished. That broader claim remains a research question, not a result of this single instance.

## 8. Conclusion

We verified a concrete goal-side certificate that includes every state within seven HTM moves of the solved Rubik's Cube. The certificate contains 109,043,123 unique fingerprints; an independent verifier checked its complete inclusion obligation by regenerating the required physical states. We also independently rechecked all 15 fourth-action courts of the previously closed three-action prefix `14,1,4`, with word-grammar and tamper controls, and verified two distinct 18-move solutions for the same original scramble. A solver with a stronger pruning rule disabled reports the same optimum, while a fully independent bounded-unreachability certificate for depth 17 remains under construction. The next decisive experiment is the closure of all canonical source-depth-ten prefixes with auditable zero-hit receipts. Until that computation is complete, the paper establishes the goal-side verification component, not the full geodesic lower bound at 18.

## References

[1] R. E. Korf, “Finding Optimal Solutions to Rubik's Cube Using Pattern Databases,” *AAAI*, pp. 700–705, 1997. https://aaai.org/Papers/AAAI/1997/AAAI97-109.pdf

[2] T. Rokicki, H. Kociemba, M. Davidson, and J. Dethridge, “The Diameter of the Rubik's Cube Group Is Twenty,” *SIAM Journal on Discrete Mathematics* 27(2), 1082–1105, 2013. https://doi.org/10.1137/120867366

[3] H. Kociemba, *RubiksCube-OptimalSolver*, public software repository, `https://github.com/hkociemba/RubiksCube-OptimalSolver` (software consulted October 2026; exact installed package wheel and audit hashes in supplementary receipts).

## Supplementary evidence and status map

- P1 external source-depth-ten versus solved-B6 Go proof: GitHub Actions #39087089460 (conditional source lower bound 17).
- P10 third-party optimal solver: GitHub Actions #39192428399 (different 18-word, physical verifier PASS).
- P11/12 conservative third-party rerun with equal-axis strengthening removed: GitHub Actions #39196884761, independent corner PDB certificate PASS.
- P13 one-sided goal filter pilot: verified B5/B5 local proof for this original source, only length <=10 exclusion.
- P14 B6 and B7 real complete inclusion checks: 8,240,087 B6 states and 156,561,653 inclusion obligations, 64 sorted B7 partitions.
- P16 **certified corner-bound hybrid pilot**: independent 40,320-state corner-permutation proof object checked before use, 725,760 transitions verified; a radius-five physical experiment excluded 139,704 goal queries at the state level, or 2,352 canonical descendant nodes in tree pruning, but ran slower than direct one-sided lookup. This is a limited performance and correctness experiment, not newly completed depth-17 source coverage.
- P15 **complete 15-child three-action-prefix source court**: 90,800,620 source10 virtual nodes, no B7 hits, 7/7 corrupted receipts rejected, and P14 B6/B7 raw SHA reverified; comparator source11+B6 was independently rerun on the same host. These logs and source are appended to the P15 supplement. This is a second certification route for an already closed three-action prefix, not additional source-prefix coverage or a full global 17-move exclusion.

**Intermediate draft, not yet a submission manuscript.** The instance-wide proof obligation is not complete, one-sided source total has not been independently closed, and this draft requires external reader review and copyediting. BRM Paper 1 and the older Humantech competition draft are distinct source and submission lineages; their frozen texts are not edited by this work.

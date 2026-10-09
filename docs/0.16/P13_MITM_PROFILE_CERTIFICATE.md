# Internal 0.16 P13 — 17 light profiles via an indexed 3+2 construction

**0.16 remains OPEN.** This is not a new formal version and not a fully nonenumerative cube-group theorem.

The earlier P12 complete finite certificate checked all C(80,5)=24,040,016 five-word subsets of 80 near-tight word candidates (the candidate restriction is valid ONLY in a hypothetical 24-word universal catalogue, not in arbitrary 25-word comparisons). Exactly 3,008 five-sets covered 20 heavy positive-dual bases, with 17 observed light-target coverage patterns.

**New independent finite derivation avoiding the full five-combination census:** for each of C(80,3)=82,160 unordered triples, let H3 be its union on the 20 heavy targets and R=H\H3 be the uncovered heavy mask. Precompute all C(80,2)=3,160 unordered pairs and, for each heavy target h, a bitset of the pairs covering h. Intersect the bitsets indexed by R; then require the pair's first word index to be greater than the triple's final word index to count each increasing five-set ONCE. This constructs exactly the potential five-covers, not any unrelated combinations.

An independent strict C++20 verifier, [p13-17-profiles-mitm.cpp](../../scripts/cuberev-016/p13-17-profiles-mitm.cpp), exhausts 82,160 triples and 3,160 pair records but only **3,008 five-set completions survive the inverted index**. It reconstructs EXACTLY the previous 17 light patterns and their full multiplicities: 85×624,90×312,95×20,102×312,105×312,119×20,125×20,153×312,165×312,170×624 and 175,187,221,235,238,245,250 ×20 each. Canonical 80×28 bitsets are derived from PUBLIC P10 and P12 JSON by [p13-emit80.py](../../scripts/cuberev-016/p13-emit80.py); no private mathematical table is required.

**Mathematical content:** the inverted-pair intersection characterizes legal completions exactly:
`(H3 union H2)=H iff H2 superset(H minus H3)`. The increasing-index condition is a unique factorization of any five-subset into its first3 and final2 elements. Thus the correctness of the 3+2 method is proved analytically and the remaining counts are a smaller finite, independently executable check.

**Truth boundary:** this is a genuinely DIFFERENT, substantially compressed computation, not a uniform hand derivation of the seven affine/ten six-light patterns from face geometry. Nor does it improve the original M* range: **25≤M*≤34**, exact optimum OPEN. For Lean, formalize the pair-intersection equivalence and the finite 80-mask input separately; then kernel-check either the full 3+2 count or a proof trace. Compiler success is not yet observed.

# CUBE-REV 0.19 — P1: The Earliest Physical Observability Horizon

## Theorem scope

Fixed **real 3×3 Rubik’s Cube**, tracked UR edge in one of 12 initial cubie slots and initial intrinsic flip=0, sticker-derived 18-HTM actions. After every move the observer obtains the single intrinsic UR-edge flip bit, retaining the entire ordered binary history. The required source family is the original 1,192 L4 physical source subsets (220 size-3, 492 size-4, 480 size-5). Each experiment is one fixed, nonadaptive length-`L` word. Dictionary objective is minimum number of such words whose induced histories are injective on every source subset for **at least one** selected dictionary word (different requirements may use different words).

**Result:**
```
L = 0,1,2,3: M*(L) = +infinity (some 5-state requirements cannot be identified)
L = 4:       M*(L) = 34        (independently checked exact physical SAT/DRUP chain from 0.18)
L = 5:       6 <= M*(L) <= 8  (local exact 70-row integer dual and 8 physically replayed words; k7 unresolved)
```
This is **not** a bound on an individual human's working memory, number of physical cube moves required to solve, or universal state identification: the source subset is assumed known and different dictionary experiments may be chosen for different source subsets.

## Transported four-point observation cuts — structural lemma

For every legal face move `a`, the physically sticker-derived 24-state tracked-edge action map decomposes as
`(p,b) -> (sigma_a(p), b XOR f_a(p))`, where `p` is the current tracked-edge slot (0..11), `b` its intrinsic flip bit, `sigma_a` is a permutation of 12 positions and `f_a(p)` is the flip increment.

The only HTM tokens with nonzero `f_a` are `F, F', B, B'`. For F/F' each support is the **four original front-face edge positions** `{1,5,8,9}`; for B/B' it is the **four back-face edge positions** `{3,7,10,11}`. For all fourteen other tokens the flip increment is identically zero.

Let `w=(a_1,...,a_L)`, let `p_{i-1}(s)` be initial slot `s` transported by the first `i-1` moves, and let `o_i(s)` be the flip bit after the first `i` moves, with `o_0(s)=0`. Define
`d_i(s)=o_i(s) XOR o_{i-1}(s)=f_{a_i}(p_{i-1}(s))`.
Therefore the ordered bit history `(o_1,...,o_L)` and the increment history `(d_1,...,d_L)` determine one another by triangular prefix XOR inversion and **induce the same partition of the twelve initial slots**.

For each flip-capable step `i`, its support in initial-state coordinates is the pullback set
`E_i={s: p_{i-1}(s) in support(f_{a_i})}` of cardinality exactly four. Every nonflip action gives an all-zero `d_i` but transports state before later pullbacks. Thus a fixed experiment's observation partition is exactly the joint membership-pattern partition induced by its physically transported four-slot cuts `E_i`.

Immediate information bound: if a word has `q` flip-capable tokens, `rank(w)=|image(h_w)|<=2^q`. Crucially, `q` alone does **not** determine this rank; the allowed transported cuts depend on the word's full physical action sequence.

## F/B-only confinement theorem, valid for arbitrary length

Under every token `F,F',F2,B,B',B2`, each of the three position sets `F={1,5,8,9}`, `B={3,7,10,11}`, and `N={0,2,4,6}` is invariant as a set, **and** the flip increment depends only on membership of the current slot in F, B or N (F quarter turns toggle all F slots; B quarter turns toggle all B slots). Starting at flip=0, any word using only F/B face moves creates **at most three different output histories** across all twelve initial slots, regardless of its length. This is a physical theorem, not a finite-enumeration coincidence.

## Exact horizon threshold for original source family

For `L<=3`, any physical word has either `q<=2` flip-capable moves, hence rank <= 4, or (only possible at `L=3`) `q=3`, in which case every move is an F/B quarter turn and rank <=3 by confinement. Thus **no 0–3 move experiment distinguishes any 5-state source subset**. Because the frozen source family has 480 5-state requirements, no finite dictionary can cover it: `M*(L)=infinity` for `L<=3`. At L4 the independently external-DRUP-checked 0.18 theorem establishes M*=34. Hence **L=4 is the first feasible observation horizon**.

Exhaustive 18-HTM physical word enumerations provide sharper, finite-horizon corroboration for maximum rank across 12 initial slots:
| L | q=0 | q=1 | q=2 | q=3 | q=4 | q=5 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 1 | — | — | — | — | — |
| 1 | 1 | 2 | — | — | — | — |
| 2 | 1 | 2 | 3 | — | — | — |
| 3 | 1 | 2 | 4 | 3 | — | — |
| 4 | 1 | 2 | 4 | 5 | 3 | — |
| 5 | 1 | 2 | 4 | 7 | 7 | 3 |

In particular L4 5-state identification **requires exactly 3** flip-capable tokens and one nonflip transport token: q<=2 gives at most four codes; q=4 gives F/B-only confinement <=3. At L5 5-state identification can only arise for q=3 or4; q<=2 lacks information codes and q=5 is F/B-only.

## Higher-order set-cover obstruction: pairwise incompatibilities are weak

Physical L5 maximal-column set: 8,807. Correct L5 all-k source implication core: 544 rows (480 size-5 + 64 size-4); projected maximal columns: 2,887. Construct the row incompatibility graph G with an edge (r,s) precisely when **no physically realizable L5 experiment** distinguishes both source sets r and s. Direct bitset intersections against all 8,807 physical L5 maxima yield exactly **2,192 edges and zero triangles** among the 544 rows. Thus the ordinary pairwise incompatibility clique packing can certify at most 2 experiments, whereas an independent positive integer-weight covering dual certifies at least 6 experiments. The 7/8 decision therefore requires genuine higher-order cover constraints and cannot be solved by pairwise incompatibility clique enumeration alone.

A numerical MILP of the 70 dual-support rows finds a feasible 6-experiment cover for that 70-row restriction (not necessarily satisfying 544 rows). A separate staged k7 numerical court found feasible <=7 covers for a growing 126-row subset, but no full 544-row witness. These are diagnostics, **not proofs of 7-infeasibility**.

## 5-turn exact proof court — authoritative status boundary

5-turn full physical history: 1,889,568 words, 14,938 unique physical partitions, 14,446 coverage types, 8,807 maximal coverage types; exact physical row/column quotient to 544×2,887. Original 0.18 M*(4)=34 proof [GitHub Actions 37958523951](https://github.com/WhoSia/CUBE-REV/actions/runs/37958523951).

L5 certified-local interval: `6 <= M*(5) <= 8` (integer linear dual 384/72, physically verified 8 words). A full physical SAT/DRUP court is now implemented as `scripts/cuberev-019/export-L5-physical.mjs`, `scripts/cuberev-019/prove-L5-k7-k6.py`, `.github/workflows/cuberev-019-l5-exact-court.yml`. It regenerates the physical instance and exact all-k quotient; checks 70-row dual; tests k7, then k6 if k7 SAT; uses Glucose4 proof traces and independent pinned drat-trim. **No new CI result or checked L5 k7 UNSAT proof is yet claimed here.** The logical status must only be promoted after independent verification receipt appears.

## Article positioning / falsifiers

1. Distinguished results: exact physical 4-step dictionary size; physically proved initial feasible horizon; transported-cut representation; striking L4→L5 structural sensitivity and 6–8 L5 interval.
2. Generic automata-theoretic distinguishing sequences and set cover are preexisting, not novel concepts.
3. Physical ontology is deliberately narrow: full 3x3 cube's single tracked edge and intrinsic flip sensor vs humans' multi-sticker visual observation, attention, memory, physical slip, unknown source sets and non-reset adaptive policies are different observational systems.
4. Speedcubing, FMC and blindfolded competition data are external reference ecologies. They are neither compulsory evidence for physical M* nor directly exchangeable optimality metrics.
5. Next decisive test: externally DRUP-check k7 if UNSAT, or physically replay a 7-word cover and attack k6.

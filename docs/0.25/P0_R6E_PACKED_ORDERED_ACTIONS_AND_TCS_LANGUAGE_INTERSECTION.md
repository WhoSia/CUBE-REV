# CUBE-REV 0.25 P0-R6E — Packed Ordered-Word Physical Search and Formal Common-Language Exclusion

## VERIFIED 2026-10-14 — actual full original B9 global lower16 proof (supersedes original prospective section)

**NEW SOURCE-SPECIFIC RESULT: 16 ≤ d18(s) ≤ 18.** Full actual fixed-center original physical 54-sticker WCA 3×3 cube, 18 HTM legal turns, exact complete-cubie CP/CO/EP/EO identity. [Actual P0-R6E original B6(goal)/B9(source) external GitHub Actions run #38520307408](https://github.com/WhoSia/CUBE-REV/actions/runs/38520307408), completed SUCCESS, full job 115708392135, Go original source audit independently passed.

Completed experiment's raw receipt:
- Real solved-side entire-cubie goal B6 size **8,240,087** states; goal projected corner6 **1,405,068**, one-step corner7 **6,807,696**, projected edge6 **7,672,278**.
- Source complete iterative normal-form B9 baseline **21,419,814,808** recursive calls; actual **120,217,012** source recursive visits + **21,299,597,796** soundly omitted recursive calls, exact integer equality, zero complete CP/CO/EP/EO intersections.
- Ordered same-generator two-move candidate checks **1,406,001,619**; all packed corner checks matched this count, edge packed checks **280,043,085**; **1,484,449,469** two-step rejected first-action subtrees across iterative bounds.
- **4,608** deterministic physically reachable cubie states × original legal 18HTM turn test cases in the packed-to-full transition regression passed before source enumeration.
- Wall **1,093.99 seconds**, max RSS **1,340,448 KiB**, user CPU **1,093.26 s**, system CPU **0.53 s**.
- Exact executable full-completion marker P0R6E_GLOBAL_LOWER 16 UPPER 18 FULL_PHYSICAL_SOURCE_COMPLETE 1 SOURCE_RADIUS 9 PROJECTION_EQUIVALENCE_4608 1.
- Independent Go auditor P0R6E_B9_GO_INDEPENDENT_CERT_PASS BASELINE 21419814808 ACTUAL_VISITS 120217012 SKIPPED_CALLS 21299597796 ORDERED_PAIRS 1406001619 WALL_SECONDS 1093.990 PEAK_RSS_KIB 1340448 VERIFIED_GLOBAL_LOWER 16 UPPER 18.
- Original physical 18-move solution is still replayed on the original 54 stickers, certifying upper18.

Soundness deduction: Every legal physical solution word of length ≤15 would split at a source prefix of length ≤9 and a solved-side suffix of length ≤6, hence would yield an actual complete-cubie meet of B9(s) and B6(e). Every canonical source prefix has been counted by the independent exact original-normal-form recurrence; no eliminated source call can meet the full solved-side ball by the proved projection same-ordered-word necessary condition and exact full-key checks where needed. Since all remaining physically possible B9 source calls were exhaustively checked with zero full-cubie meets and timeout did NOT occur, **ALL ≤15 actual 18 HTM solutions of this original source are excluded**. This is a finite proof for one official scramble, not for every cube.

**Scope limitations:** This is NOT a complete Lean proof of the full physical normal-form construction, nor a second full independent Go B9 physical search. The Go program independently audits exact canonical call accounting, genuine required original physical receipt markers, resource data and result typing. A systematic error shared by inherited C++ physical turn implementation and its own reference assertions still motivates future independent engines or proof-carrying trace verification; never overstate independence. Previously established lower15 from B8 is now a historical precursor, not the current frontier.

**Next strict geodesic frontier:** Full original B10(source) versus exact B6(goal) zero meet would exclude lengths ≤16 and prove **17≤d18(s)≤18**, but this requires completing a substantially larger source-language proof. The **unpruned iterative canonical B10 word-call count 285,921,738,920** is established by independent 18-action Go vs two-state TCS transfer; not 285B unique cubes. Before any naive expensive monolithic job, optimize proof cost and consider certified partition of canonical first-generator languages into independent prefix shards. If any true complete cubie intersection appears, reconstruct and independently replay the shorter actual solution and abandon the proposed lower17. No new lower17 is claimed at time of this update.


**Science contract:** source-specific official WCA Seoul Summer 2026 3×3 Final Group A1 original 54-facelet fixed-center cube; all original 18 legal HTM actions, all eight corner and twelve edge perm+orientation. **Previously completed, actual external Actions-certified original distance: 15≤d18(s)≤18** via [R6B full goal B6/source B8](https://github.com/WhoSia/CUBE-REV/actions/runs/38518179172). The present P0-R6E source B9 test is a **NEW UNVERIFIED attempt** to exclude 15 moves and prove lower16; never presuppose its result.

## Two genuinely different research axes

**A / physical systems-and-cost axis.** R6D's source B7 had already removed ~92.5% of R6C's physical DFS visits with effectively no wall-time gain (R6D 674,679 visits, wall 20.00s, RSS 1,341,068 KiB; R6C 9,005,784 visits, wall 20.01s, RSS 1,340,256 KiB; [external completed Actions #38518256469](https://github.com/WhoSia/CUBE-REV/actions/runs/38518256469)). The bottleneck is NOT a proof lack, but expensive repeated candidate turn-pair checks. Optimize the **cost of deciding the same scientifically sound predicate**, not the predicate itself: packed direct 8-corner transformation first, exact set membership C6, then only if corner accepted perform the packed 12-edge transformation and E6 membership. The physical full cubie transition is still required for source recursive traversal and exact full-cubie goal hit checks; only *discarded last-two-action candidate simulations* are factored. No massive new unordered_set or precomputed >10-million-state cache is introduced.

**B / pure mathematics and TCS axis.** R6A corner-one-step, R6C synchronized one-action, R6D ordered two-action exclusion are instances of a common formal statement over the free monoid A* and a normal-form regular language. Let full physical automaton M=(S,A,δ) and projected automata M_C=(C,A,δ_C), M_E=(E,A,δ_E) satisfy exact commuting morphisms π_C δ=δ_C π_C and π_E δ=δ_E π_E. For a fixed source x, let full goal T be exact B6(e), and projected accepting sets C_T=π_C(T), E_T=π_E(T). Let N_l,k ⊂ A* be the legal canonical suffix words of lengths ≤k from previous generator l (a DFA-recognizable finite language). Define accepted-word sets:

    L_C(x,k,l)={w∈N_l,k | δ_C*(π_C(x),w)∈C_T}
    L_E(x,k,l)={w∈N_l,k | δ_E*(π_E(x),w)∈E_T}
    L_T(x,k,l)={w∈N_l,k | δ*(x,w)∈T}.

**Exact inclusion:** L_T(x,k,l) ⊆ L_C(x,k,l) ∩ L_E(x,k,l). Therefore empty INTERSECTION is a sound exact full-state goal exclusion for every canonical suffix in the declared length budget. The SAME ordered word must be accepted by both projected languages: (∃w C-accepts(w)) ∧ (∃v E-accepts(v)) is too weak to imply ∃w both accept(w). In general equality is false: corners and edges passing separately is not sufficient to ensure a compatible full cubie state. A full-state exact equality check remains mandatory for surviving words.

The source normalization automaton tracks the last-generator face/order, making N_l,k regular. The product automaton with (corner quotient state, edge quotient state, canonical DFA state, remaining depth) implements the language intersection condition. Full materialization of C×E is infeasible; R6E implements an **on-demand symbolic short-word slice** and checks projection acceptance only as required. Memory-time complexity may be interpreted through cached residual right languages, approximate branch support masks, and automaton minimization; none may omit a true accepted common word. Equivalent states for exclusion at depth k require equality of legal action-word residual language, not merely equal corner heuristic distance. Left/right group action conventions and inverse-action closure must be made explicit whenever backward tables are added.

## Exact physical C++17 packed operator

[Implementation](../../scripts/cuberev-025/p0_r6e_packed_projected_two_turn_cpp/main.cpp) includes unchanged inherited original R6D physical solver as a renamed entry and uses its full true source B6, C6/C7 and E6 images. Given the existing original exactKey packed encoding:

    c = Σ cp[i] 2^(3i) + Σ co[i] 2^(24+2i)
    e = Σ ep[i] 2^(4i) + Σ eo[i] 2^(48+i),

we apply actual 18HTM generator m without materializing a whole Cube for candidate second actions:

    cp'[i]=cp[m.cp[i]], co'[i]=(co[m.cp[i]]+m.co[i]) mod 3
    ep'[i]=ep[m.ep[i]], eo'[i]=eo[m.ep[i]] XOR m.eo[i].

To make this independently falsifiable against the full original 54-facelet-derived turn table, the executable tests **256 deterministic real reachable cube states × all 18 physical actions = 4,608 exact packed corner AND edge successor-equality checks**, before any search. It also validates real original WCA 54-sticker input, known 18-move physical completion, and explicit noncommutativity U F ≠ F U in the REAL cube.

The new source branch predicate is IDENTICAL to R6D at every ordered two-move candidate: identical source normal form, exactly same C6/E6 images, same early corner envelope C7, and the same full state checking on surviving prefixes. The only change is factored evaluation. Therefore the claimed D/E decision-equivalence receipt requires exact equality of:
- full physical original B6 total 8,240,087; C6 projection 1,405,068;
- canonical cumulative source B7 120,213,368;
- actual DFS visits, eliminated canonical calls, **and number of ordered-pair candidates tested**;
- exact full-cubie intersections zero; 4,608 original physical projection successor agreement checks.

The packed implementation records all second-action checks and counts how often the expensive edge move is skipped due to corner rejection. Saving source DFS calls is NOT an expected benefit here: the algorithm is purposefully *semantically identical* to R6D. The measurable engineering benefit (or failure) is wall seconds and peak RSS. Added bookkeeping could itself alter costs. Same-runner sequential benchmarking mitigates hardware heterogeneity but needs repetition or reversed order to support stable performance conclusions.

## Independent Go receipt audit, CI and optional original B9 proof

[Go --packed audit](../../scripts/cuberev-025/p0_r6_receipt_go/main.go) validates D-vs-E exact source calls and pair count; then reports true wall seconds / RSS without selecting the winning result beforehand. [P0-R6E matched benchmark workflow](../../.github/workflows/cuberev-025-P0-R6E-packed-pair-benchmark.yml) starts with a lightweight original 54-sticker physical compile, 4,608 turn-regression checks, and small B3/B3 test, then runs completed B6(goal)/B7(source) original D/E on the same runner. Log artifacts are retained on success/HOLD/failure. CI is read-only, persists no GitHub credentials for checkout, and forbids bot-authored/committed history.

The independent harder [P0-R6E B9 original whole-cube court](../../.github/workflows/cuberev-025-P0-R6E-global-lower16-B9.yml) is separated and resource gated. It tests actual B9(source) vs exact B6(goal) with R6E full physical model. Complete canonical iterative source recursion from depths 0..9 has precisely **21,419,814,808 unpruned recursive calls** (all depth-limits combined), computed by independent recurrence N9=N8+Σ_{d=0}^9 c_d; this is NOT distinct cube states. A complete original full-cubie nonintersection, identical baseline=(actually visited+soundly skipped), completed physical source/witness regression, measured wall/RSS, and independent Go --source9 receipt would certify **16≤d18(s)≤18**. If a 15-or-fewer real-cubie intersection exists, if any resources run out, or if the evidence fails, do NOT claim lower16; preserve the previous completed external **15≤d18(s)≤18** bound. A found intersection must be reconstructed and independently 54-facelet replayed before claiming an actual shorter whole-cube solution.

## Pure TCS and Lean4 proof boundary

[Lean4 ProjectionWordLanguage.lean](../../formal/025/ProjectionWordLanguage.lean) contains:
1. action-word evaluation preserving physical action order;
2. an inductive proof that exact one-step projected homomorphisms commute with every finite ordered action word;
3. inclusion of the true full goal-reaching source-word language in the **intersection** of both projected accepted-word languages;
4. a canonical-language-parameterized theorem that an empty projected common language excludes any true physical solution in that legal suffix language.

The formal theorem is **generic and conditional** on having honest exact one-step quotient morphisms, honest necessary goal projections, and a legalWord predicate describing the desired normal-form grammar; it does NOT certify the original 54-sticker generators, the enormous finite enumeration, the canonical-word DFA's completeness for the whole 18HTM group, nor full original Rubik's geodesic distance. Those are distinct physical/finite executable witness obligations. [Fast read-only Lean workflow](../../.github/workflows/cuberev-025-P0-R6E-lean-language.yml) is an external kernel gate; until an actual Actions SUCCESS and build log are read, record Lean4 result as PENDING.

## Future genuine TCS research after this exact negative/positive engineering test

- **Myhill–Nerode residual language equivalence:** states whose canonical continuation languages are indistinguishable up to remaining depth k can share proof-carrying support masks, but must preserve last face and ordered future generators; equality of distances alone is insufficient.
- **Regular-language intersection emptiness under projection:** develop a compact automaton for allowed HTM normal forms, with corner and edge languages dynamically intersected over the same word; derive source-complete nonexistence certificates.
- **Tighter lower-bound classes:** cost-partitioned admissible heuristics give quantitative path lower bounds; joint-language emptiness gives qualitative no-continuation proof. Study their product without violating operator-cost sums or mixing differently ordered words.
- **Verification assurance:** independent Go/C++ original-cubie transitions versus Lean generic language inclusion; collect traceable move-table equivalences, source canonical coverage and explicit typed HOLD states. No unsupported transfer from generic finite examples to the physical original cube.

## Evidence and governance

At authorship time the new R6E performance test, actual B9 experiment and Lean projection-language kernel check remain **SUBMITTED/UNVERIFIED**. R6B prior global lower15, R6D prior B7 proof and previous independent Lean same-action kernel theorem are separately completed and inherited. Research code C++17 (physical), Go (independent receipt), Lean4 (abstract TCS). No Python-first claims, no bot author/committer, read-only Actions, P7 exact allowlist, no protected human 451 raw reconstructions in public source.


## 2026-10-14 mathematical branch: exact rational source normal-form grammar

An additional independent pure TCS observation eliminates the need to model the 18-letter canonical-word automaton in all 18 last-action states just to COUNT the complete search universe. The inherited physical word normalization forbids consecutive rotations of the same face and fixes one total order among commuting opposite faces. Group the six faces in their actual URFDLB index order as *low* {U,R,F} and *high* {D,L,B}. Each face has exactly three HTM generator powers. At a given old low-ending face, legal next faces comprise two low and three high (six low-labeled moves + nine high-labeled moves); at a high-ending face, the reverse opposite face is forbidden, leaving two low and two high (six low + six high-labeled moves). Therefore if (L_d,H_d) are canonical words of exactly length d ending at each class, the **exact transfer** is

    [L_(d+1)]   [6 6] [L_d]
    [H_(d+1)] = [9 6] [H_d]       with L_1=9, H_1=9.

Its characteristic polynomial is **lambda²−12lambda−18**, roots 6±3sqrt(6). If c_d=L_d+H_d counts all canonical legal source action WORDS of length d, then for every d>=1,

    c_(d+2)=12 c_(d+1)+18 c_d;  c_1=18, c_2=243.

This recurrence is exact combinatorial normal-form counting, NOT a Rubik full-state count. The growth constant is 6+3sqrt(6)≈13.348469; therefore the unpruned canonical source word tree still expands exponentially even after removing obvious same-face/opposite-face normalization redundancy. The iteratively deepened total number of complete recursive entries through source radius R is N_R=sum_(d=0)^R (R-d+1)c_d, c_0=1. In particular, N_7=120,213,368; N_8=1,604,664,504; **N_9=21,419,814,808**. These exact integer values bound the *accounting population* from which true pruning removes calls; a source search cannot be declared complete by merely comparing wall time to this population.

[Independent Go 6-face class transfer and complete 18-action DFA cross-check](../../scripts/cuberev-025/p0_r6e_normal_form_transfer_go/main.go) checks all lengths 1..10, reproduces the physical inherited normal-form baseline N7,N8,N9 and emits a typed receipt. [Lean4 CanonicalTransfer.lean](../../formal/025/CanonicalTransfer.lean) formalizes the 2x2 transfer's characteristic recurrence and first exact 18/243 layers. **The Lean theorem checks the algebraic consequence of the stated transfer; the correspondence of the transfer to the source canonical grammar is independently enumerated in Go**, not yet a theorem tying actual complete Rubik's physical normal forms to Lean's grammar. [Short independent Go Actions court](../../.github/workflows/cuberev-025-P0-R6E-canonical-grammar.yml) provides a cheap CI gate separate from the long B9 search. Existing [Lean TCS kernel Actions](../../.github/workflows/cuberev-025-P0-R6E-lean-language.yml) builds both CanonicalTransfer and ProjectionWordLanguage via the default Lean lake configuration.

**Research significance:** the transfer has effective dimension two for this face-class counting observable despite the 18-move legal alphabet. This separates the **combinatorial language-growth problem** (a rational, completely solved series) from the **physical Rubik's state coalescence and source-specific geodesic-exclusion problem** (requiring true cubie physics, noncommuting action order, goal projections, and sound subtree certificates). Future TCS work can use the exact grammar transfer to cost bound lookahead, to choose safe proof-prefix partitions, and to prove recurrence-based source-count artifacts without recomputing an enormous DFS tree.

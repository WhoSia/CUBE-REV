# CUBE-REV 0.25 P0-R6I-P6 — Certified Pareto Cutset Optimization and Physically Measured Source/Goal Cost Decomposition

**2026-10-15 scientific status.** The source-specific WCA Seoul Summer 2026 3×3 Final A1 unrestricted whole-original 18HTM distance is still **16≤d18(s)≤18** (original full source B9 vs goal B6 court #38520307408). Only the first-U and first-D source B10 cylinders were previously completed; the other **16** physical source B10 action cylinders are still OPEN. This P6 phase establishes a correct finite optimization model, independent exhaustive audit and measured physical source costs; it does NOT certify lower17 or a real 43-way full source-B10 speedup.

## 1. Exactly stated finite multiobjective optimization problem

Let R=10 and L be the exact 18-action canonical Rubik 18 HTM word grammar, carrying the actual last-action DFA state, with no consecutive same face and a fixed order for commuting opposite faces. For each of the 18 first-generator cylinders, either preserve the whole depth1 source prefix or replace it by ALL its legal depth2 child prefixes. These are precisely 2^18=262,144 individually labelled complete prefix-free policies. The original source root is tested separately.

For a canonical legal prefix p at depth m, let W_R(p) be the source iterative DFS recursive-call population (not distinct cubies) and q_p its DFA state. Exact grammatical conservation is W_R(p)=(R−m+1)+sum over legal next generators a of W_R(pa). Thus all allowed mixed-depth frontiers, after accounting for internal prefixes, sum to the original full source B10 word-call baseline **285,921,738,920**, independently checked against the original 18-letter dynamic programme.

A modelled leaf-cost c(p), in integer nanoseconds with arithmetic rational rates rounded UP once per leaf, is:

    c(p)=ceil_ns[setup + (observedFirstActionWall(first(p))−setup)*W_10(p)/W_10(first(p))].

Actual original full B10 physical measurements: U-first=711.50s and D-first=561.99s. This formula is a declared EXTRAPOLATION for deeper physical source prefixes and is NOT a measured physical cost function. Tested setup alternatives: 20.00s (original UNMEASURED assumption) and 14.49s (rounded from one real B6/B7 full goal/projection trial). Another two independent full B6/B7 runs confirm setup is variable, as documented below. The resulting multiobjective minimization score is (n, T, M): number of independent leaf jobs, total modelled runner seconds, and maximum single modelled leaf duration. Parallel P-worker actual makespan is a SEPARATE combinatorial objective, not derived uniquely from (n,T,M).

## 2. Exact certified Pareto dynamic programming and exhaustive 2^18 counterpart

[Independent Go source](../../scripts/cuberev-025/p0_r6i_pareto_dp_go/main.go) constructs the 18 legal first-generator keep/split branch alternatives and exact original DFA cylinder weights. Scores combine with (n1,T1,M1)⊕(n2,T2,M2)=(n1+n2,T1+T2,max(M1,M2)). The DP retains the minimum T at each exact (n,M) and discards componentwise dominated completed scores. Independently, a separate exhaustive loop evaluates ALL 262,144 labelled policies and computes their uncompressed Pareto frontier. Strict equality of the cost triples between these two methods is required to print SUCCESS; all model score calculations use exact arbitrary-precision rational numerator steps rounded to integer nanoseconds, without floating-point optimization comparisons.

[Actual Actions #38670899068](https://github.com/WhoSia/CUBE-REV/actions/runs/38670899068) completed SUCCESS, Go job 116213525610 printed P0R6I_EXACT_DEPTH2_PARETO_DP_262144_BRUTE_FORCE_AUDIT_PASS. Under the original 20s per-job assumption its entire Pareto front contains EXACTLY THREE solutions:

| First-generator policy | Independent leaf jobs | Internal IDDFS calls | Sum model seconds | Max leaf model seconds |
|---|---:|---:|---:|---:|
| Keep all original first-generator cylinders | 18 | 11 | 11,461.410000 | 711.500000 |
| Split all 9 low-class cylinders, keep all 9 high | 144 | 101 | 13,981.409997 | 561.990000 |
| Split all original 18 first-generator cylinders | 243 | 191 | 15,961.409993 | 71.803693 |

[Calibration Actions #38671142130](https://github.com/WhoSia/CUBE-REV/actions/runs/38671142130), Go job 116214309851, also completed SUCCESS with original assumption 20s AND measured single-run setup 14.49s. The 14.49s variant retains EXACTLY these three discrete Pareto decisions and changes their T/M to respectively (11,461.410000,711.500000), (13,287.149996,561.990000), and (14,721.659993,66.706474) seconds.

The previously chosen heuristic 43-cylinder source cutset (split first U and D only) was rigorously PARETO DOMINATED by the 18-cylinder original in this THREE-COST OBJECTIVE. At 20s it has (43 jobs, 11,961.409999 total model s, 711.50 max model s); at 14.49s, (43, 11,823.659999s, 711.50s). This is an important preserved NEGATIVE result. It DOES NOT contradict the older hypothesis that 43 jobs may have a slightly better four/eight-worker longest-processing-time simulated makespan, since parallel makespan depends on job packing and cannot be decided by only the three Pareto coordinates. Neither 43 nor another policy has been shown to minimize actual hardware makespan.

## 3. Lean 4: why dominated DP states may be safely discarded

[Formal proof source](../../formal/025/ParetoCutsetDominance.lean) introduces natural-number CutsetScore, its scoreJoin additive/additive/max composition, scoreWeakDominates componentwise preorder, reflexivity and transitivity, and the DP-safety theorem:

    scoreWeakDominates x y
      ⇒ scoreWeakDominates (scoreJoin x future) (scoreJoin y future).

That is, a common suffix of independent future leaf choices cannot make a dominated score dominate its previous better alternative under these three objectives. It is a legitimate algebraic basis for pruning Pareto DP states, NOT a proof of actual source-cubie state equivalence or a full physical cache mechanism.

First [Lean Actions #38671052106](https://github.com/WhoSia/CUBE-REV/actions/runs/38671052106) and [#38671063471](https://github.com/WhoSia/CUBE-REV/actions/runs/38671063471) compiled unsuccessfully because the lean-core-only package could not resolve generic order lemma names. Replaced these steps by Lean standard arithmetic omega tactics; [corrected Lean kernel #38671220448](https://github.com/WhoSia/CUBE-REV/actions/runs/38671220448) completed **SUCCESS, 17 build jobs**. Do not erase the failed historical experiments.

## 4. Real original physical C++17 stage measurement: what actually costs resources?

[Original physical stage profiler](../../scripts/cuberev-025/p0_r6i_physical_phase_profile_cpp/main.cpp) uses the unchanged original 54-sticker-derived physical cubie/packed 18 HTM move model. It separately measures exact physical input/known 18-turn solved-witness/4,608 packed-to-full legal move tests; the entire original B6 solved-side full CP/CO/EP/EO goal; corner projected goal construction; edge projected goal construction; and six true original source prefixes in the same process with one shared complete goal. It records measured source wall milliseconds and candidate ordered pair checks, packed edge checks and full whole-cubie goal probes for each prefix, plus process RSS milestone/peak. [Independent Go physical cost and source ledger audit](../../scripts/cuberev-025/p0_r6i_physical_phase_audit_go/main.go) rechecks all 18-action canonical suffix weights, visited+soundly skipped calls, 4,608 physical move equivalences, true complete whole-cubie goal size and actual wall/RSS receipts. It cannot produce any GLOBAL lower17 marker.

[Actual original GitHub workflow #38670899068](https://github.com/WhoSia/CUBE-REV/actions/runs/38670899068) successfully completed both physical B3/B3 preflight and real full B6(goal)/B7(source) stage jobs with Go audits. The small physical goal B3=3,502 setup measurements were: whole goal1.836ms, corner projected goal7.834ms, edge projected goal0.199ms, total9.869ms. This is a useful correctness smoke, NOT a representative cost for entire B6.

Three completed original B6/B7 physical full-goal/projection measurements are available from consecutive independently scheduled workflow runs:

| Run, job | Whole physical goal B6 (ms) | Corner projection (ms) | Edge projection (ms) | Goal+projection shared setup (ms) |
|---|---:|---:|---:|---:|
| #38670899068 / 116213646524 | 2619.459 | 9534.127 | 2332.512 | **14486.098** |
| #38671127033 / 116214377861 | 2602.322 | 8937.239 | 1568.493 | **13108.054** |
| #38671142130 / 116214417176 | 2604.689 | 8827.267 | 2279.237 | **13711.193** |

**Median shared setup: 13,711.193ms =13.711193s; observed range 13.108054–14.486098s.** Corner projected-goal construction is the largest stage (8.827–9.534s), while full original whole-cubie goal construction is consistently ~2.6s. Do not assume a universal 13.7s per job in all runner hardware/source-B10 operations from three sequential independent samples.

In the first full original B6/B7 run, process peak RSS was **1,340,720KiB**, with current RSS ~657,816KiB immediately after the whole goal, ~1,111,188KiB after corner projection and ~1,341,020KiB after edge projection. RSS high water cannot be attributed separately to one source search: the entire goal/projection court is shared in process and dominates memory. Recreating it independently in every GitHub job incurs repeated real cost; a hypothetical process-shared goal court requires separate exact physical integrity, concurrency, memory-sharing and independent evidence validation.

## 5. Physical source-state geometry falsifies a grammar-size-only physical cost hypothesis

Six source prefix samples from the SAME original source/B6 goal in the first full runner:

| Prefix | Exact source canonical word calls | Actual visits | Ordered 2-generator pair checks | Packed edge checks | Physical source wall (ms) |
|---|---:|---:|---:|---:|---:|
| U | 7,353,187 | 41,269 | 355,710 | 63,258 | 281.314 |
| D | 6,003,853 | 33,697 | 275,820 | 48,555 | 219.167 |
| U,R | 550,863 | 3,093 | 32,079 | 6,085 | 23.286 |
| U,D | 449,778 | 2,526 | 19,344 | 3,421 | 16.273 |
| D,R | 550,863 | 3,093 | 20,952 | 3,895 | 20.695 |
| D,L | 449,778 | 2,526 | 18,366 | 3,526 | 16.045 |

Every prefix has fully exact canonical visited+soundly skipped = stated source word calls and ZERO full-cubie goal matches. Crucially U,R versus D,R have identical canonical DFA context after the last R and identical remaining source radius, hence exactly identical 550,863 canonical word calls and 3,093 actual source recursion visits. But their ORIGINAL physical source configurations differ, giving **32,079 vs 20,952 ordered pair tests** and **6,085 vs 3,895 packed edge tests**. Thus the stronger claim that physical search work is a function ONLY of canonical suffix-language size or source-recursion visits has been empirically FALSIFIED at the subtest level, even though the fast physics/Go proof remains correct. Physical wall-times may vary by runner/cache; do not infer a universal constant per-pair cycle cost from just two prefixes.

Six original source B7 prefixes together required576.780ms in the first runner, versus14,486.098ms common goal preparation, showing that *at this shallow small set of source prefixes* the common goal dominates. It does NOT imply original source B10 physical first-U/D searches, already measured in hundreds of seconds, are cheap.

## 6. Proof boundary and next research questions

The EXACT optimization applies only to fully exhaustive two-level prefix policies and the explicitly quantized *proxy* costs, not the enormous space of all variable-depth R10 canonical source cuts, worker-scheduling problem or true physical source state costs. The Lean DP lemma applies to identical future choices and the three additive/max score coordinates, not general actual parallel makespan dominance. The three physical runs validate same whole original B6 target and six prefix physical no-meets, not a complete B10 source proof. All remaining sixteen first-action source-B10 regions remain unproved; global lower17 is OPEN.

Research opportunities now precisely posed: (i) exact/bounded P-machine scheduled makespan DP including worker-load vector and fixed setup; (ii) state-aware physical cost regression using actual ordered pair counts, packed edge-gate costs and source-prefix full-key lookup frequencies, rather than mere word size; (iii) shared immutable B6 court among sibling physical source partitions versus independent-run setup costs, with a real read-only hardware memory/throughput audit; (iv) a conditional antichain negative-certification mechanism formally binding actual DFA context and same-ordered-action physical corner-edge projection necessity. Never claim a lower17 certificate without full source original physical coverage.

**Governance:** human WhoSia author AND committer, no bot commits, read-only GitHub Actions, protected private 451 human FMC reconstruction cases unexposed. Languages: original physical C++17, independent finite Go + audit, formal TCS Lean4. All CI compilation failures and negative/mixed measurements retained.

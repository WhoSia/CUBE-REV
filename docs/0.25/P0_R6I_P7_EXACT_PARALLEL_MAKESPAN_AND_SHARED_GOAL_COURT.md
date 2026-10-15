# CUBE-REV 0.25 P0-R6I-P7 — Certified Parallel Scheduling and Shared Original Goal Court

**Official research title:** Certified Parallel Scheduling over Canonical Prefix Cutsets: Exact Worker-Load State Abstraction, Geometry-Conditioned Search Costs, Shared Goal-Court Economics & Proof-Preserving Optimization.

**Scientific boundary, October 15 2026:** The WCA Seoul Summer 2026 Final A1 original cube under unrestricted 18HTM retains **16≤d18(s)≤18**; completed whole source B9 / solved B6 physical court and Go receipt proved lower16. Only first-U and first-D source-B10 first action cylinders have been independently fully proven, leaving **16 OPEN**. P7 includes a mathematical scheduler and an original B6(goal)/B7(source) real full-cubie shared-vs-isolated experiment. This is NOT a global source-B10 search.

## 1. Exact P-machine makespan: mathematical problem and certificates

There are exactly nine low-class original first-action tasks and nine high-class tasks under the real 18-letter normal-form action grammar. Physical first-U B10 measured wall 711.50s and first-D 561.99s; P7 provisionally transfers these two timings to every other first-action task in the corresponding class. With integer-centisecond model costs L=71150,H=56199, define

    OPT_P(l,h)=minimum possible maximum worker load for l low and h high jobs on P identical nonpreemptive workers,
    OPT_1(l,h)=l·L+h·H,
    OPT_P(l,h)=min_(0≤i≤l,0≤j≤h) max(i·L+j·H,OPT_(P−1)(l−i,h−j)).

This is exact Bellman dynamic programming with state (P,l,h), not an LPT approximation. A separate threshold-feasibility DP tests whether all 18 jobs fit at upper bound OPT and rejects OPT−1 centisecond. The implementation also reconstructs a concrete integer worker allocation whose maximum matches OPT.

[Go source](../../scripts/cuberev-025/p0_r6i_p7_exact_parallel_dp_go/main.go), [read-only GitHub Actions #38679063747](https://github.com/WhoSia/CUBE-REV/actions/runs/38679063747), job 116239209413 COMPLETED SUCCESS:
- P=4: exact model optimum **2,959.46 seconds**.
- P=8: exact model optimum **1,685.97 seconds**.
- Both have independently verified feasible optimum and strictly infeasible smaller cap, with all nine+nine tasks covered.

For the actual canonical 43-prefix mixed-depth policy (splitting first U and D one additional canonical action, leaving the other 16 untouched), a separately computed LPT assignment gives a CONSTRUCTIVE UPPER bound and max(total/P,max-task) a universal model LOWER bound. All 43 target prefixes plus internal source canonical calls exactly sum to 285,921,738,920.

| Worker P | Each independent job setup (model) | Bound from below | Constructive LPT bound from above |
|---|---:|---:|---:|
|4|20.00s|2990.352500s|3006.117286s|
|4|14.49s|2955.915000s|2970.378033s|
|4|13.71s|2951.040000s|2965.318756s|
|8|20.00s|1495.176250s|1530.491927s|
|8|14.49s|1477.957500s|1509.951559s|
|8|13.71s|1475.520000s|1507.043848s|

Consequences under the DECLARED unsplit first-action and 43-leaf proxy prices, not real B10 physical performance:
- Four workers +20s per separate job: even perfect 43 scheduling cannot beat exact 18 scheduling (2990.35>2959.46).
- Four workers +13.71s setup: neither policy wins provably, because 2959.46 lies within 43's certified bound interval.
- Eight workers, under either studied setup, a constructed 43 schedule is faster than exact optimal 18 scheduling in the proxy model. This is not an exact 43 optimum proof.

[Lean4 ParallelWorkerLoads.lean](../../formal/025/ParallelWorkerLoads.lean) proves max load invariant under arbitrary permutations of identical worker identities, a sound symmetry quotient for future full load-vector DP. [Kernel Actions #38679093362](https://github.com/WhoSia/CUBE-REV/actions/runs/38679093362) SUCCESS with 19 build jobs. Lean does not independently encode every Go scheduling state or physical B10 goal member.

## 2. Actual original 54-sticker SAME-PROCESS goal court sharing

[Real physical C++17 source](../../scripts/cuberev-025/p0_r6i_p7_shared_goal_cpp/main.cpp) uses exactly the inherited original physical 54-sticker-derived CP/CO/EP/EO and packed 18 HTM transition kernel, WCA original source and the known verified 18-move completion, 4,608 packed vs full legal physical turns, entire solved-side B6 (8,240,087 full cubie goal states), corner C6 1,405,068 and edge E6 7,672,278. Six original normal-form source B7 prefixes are U, D, U-R, U-D, D-R, D-L.

- shared mode: build physical whole B6 and both projected goal structures ONCE and check all six source prefixes serially using the unmodified target.
- isolated mode: build and destroy an entire independent original physical B6/projection court for EACH of six prefixes, with the exact same true source-prefix DFS.
- [Independent Go verifier](../../scripts/cuberev-025/p0_r6i_p7_shared_goal_audit_go/main.go) calculates each original canonical suffix-call population separately and demands exactly identical physical visited, safely skipped, ordered pairs, packed edge and full whole-cubie query counts in both modes. It checks real wall/RSS, full physical target/projection sizes, 4608 original legal move tests and 1 versus6 constructions; any timeout or true full-cubie intersection fails.

[Original shared-court GitHub Actions #38679063747](https://github.com/WhoSia/CUBE-REV/actions/runs/38679063747) completed all four jobs SUCCESS, including B3/B3 physical smoke and TWO separate original full B6/B7 matched paired comparisons with REVERSED execution order:

| Within-run order | Shared original full process time | Isolated six whole-court process time | Shared B6 setup only | Six independent B6 setups |
|---|---:|---:|---:|---:|
|shared then isolated, job 116239307243|13.315667s|92.118322s|12.849624s|79.193270s|
|isolated then shared, job 116239307225|14.000522s|95.195759s|13.524996s|81.640617s|

External /usr/bin/time wall includes extra executable startup overhead: approx14.75/92.20s (shared first) and15.49/95.28s (isolated first). Internal source sample physical search times were 465.390/490.406ms and474.878/511.095ms, respectively. Whole-process peak RSS shared was **1,340,496/1,340,524 KiB** and isolated **1,387,784/1,387,760 KiB** for the two matched jobs. The independent physical target rebuild setup required approximately **6.16×** or **6.04×** the shared setup, as expected from one versus six constructions, while whole measured process wall dropped about85% by sharing. These results are two actual ORIGINAL physical source B7 experiments, NOT any assertion of a universal B10 wall speedup or inter-runner shared memory.

Crucially ALL SIX original source-prefix physical source search counters were identical between the two modes, for each reversed-order job, and actual whole-cubie intersections were zero. U-R and D-R both have exact 550,863 canonical calls and 3,093 visited but respectively 32,079 vs20,952 ordered pairs, reinforcing the separate P6 finding that physical original cubie state affects true expensive projection checks even when canonical grammar counts agree. The Go verifier does not independently reconstruct the original 8.24M-element goal set through a different physics implementation or cryptographically attest its full contents; the two C++ modes use the same original deterministic physical goal construction. Preserving independent per-leaf proof receipts plus an immutable target-court provenance identifier remains a future proof-engineering requirement.

## 3. Cost model: immutable goal built once per worker

The original full B10 first-U and first-D model prices already include one B6 goal construction. Under an explicitly assumed fixed setup s, a worker with l low and h high jobs can REUSE one complete goal court in its own process. The model worker cost changes to:

    C_worker = 0 if l+h=0,
    C_worker = s+l·(711.50−s)+h·(561.99−s) otherwise.

Independent mode remains C_worker=l·711.50+h·561.99. This is an explicit extrapolation of the PHYSICALLY VERIFIED B7 shared-vs-isolated structure into the original B10 first-action cost model, not measured real B10 sibling task sharing. [New exact Go worker-target sharing model](../../scripts/cuberev-025/p0_r6i_p7_schedule_shared_model_go/main.go) computes both policies under Bellman and independent feasible/strict infeasible threshold decision problems. The initial Go compilation #38679260161 failed due a typo in the high-task price property; after repair [Actions #38679314245](https://github.com/WhoSia/CUBE-REV/actions/runs/38679314245) SUCCESS and preserved the compiler-failure history.

| Worker count | Setup proxy | Optimal independent-build makespan | Optimal per-worker shared goal model makespan |
|---:|---:|---:|---:|
|4|13.71s|2959.46s|**2904.62s**|
|8|13.71s|1685.97s|**1658.55s**|
|4|14.49s|2959.46s|2901.50s|
|8|14.49s|1685.97s|1656.99s|
|4|20.00s|2959.46s|2879.46s|
|8|20.00s|1685.97s|1645.97s|

Each DP returns a genuine model assignment with exact 9 low /9 high tasks and a lower-bound certificate that the immediately smaller 0.01s makespan is infeasible. No true original shared-B10 hardware job was run for these six model optima.

Comparing unlike goal-court policies can mislead: at four workers and setup13.71s, 18 shared-goal model optimum2904.62s is better than the 43 ISOLATED lower bound2951.04s, but a 43 SAME-WORKER-shared-goal model may also be faster; it has not been optimized here. At eight workers a feasible isolated-goal 43 split model upper bound1507.04s is below even the shared-goal 18 model optimum1658.55s, but the true real physical performance may diverge from per-word cost extrapolation.

## 4. Mathematical and operational next step

Use a proof-carrying worker batch as the unit of physical search: build one immutable whole B6 goal+corner/edge projection and bind its audit identifier, then execute multiple canonical source-prefix cylinders serially within the batch. Preserve separate full-cubie zero-meet receipts for every leaf, including true original source state, canonical last-action context, exact depth, actual visited+safe skipped and full goal lookup, and independently verify that all prefixes compose into an exhaustive unambiguous source language. Per-worker RSS constraints and original whole physical target immutability matter; running jobs on different GitHub-hosted VMs cannot simply share pointer memory across machines.

Next physical step should choose only a SMALL number of original B10 depth2 prefixes, run complete bounded physical prefix searches with and without real same-process goal sharing, perform independent Go source coverage and resource audit, and then fit actual ordered-pair/edge/full-query cost coefficients to improve scheduling. Do NOT automatically start the sixteen missing expensive first-action B10 proof jobs or infer lower17 from these six shallow source B7 prefixes.

**Result authority:** Original whole cube 16≤d18(s)≤18. Only two distinct complete source-B10 first-action cylinders U/D certified. TCS word-grammar exactness, Go scheduling under declared costs, Lean max-load symmetry, original physical shared B6/B7 cost experiment all documented separately. WhoSia author+committer only; no bot code contributions; read-only Actions, no writeback; private 451 human FMC reconstructions protected.


## 7. Inspectable exact worker assignment witnesses and setup amortization

The original two-class B10 declared-cost exact worker schedules have tangible witness tuples (low jobs, high jobs) with all work covered:

- Four-worker exact optimum 2959.46s: (0,5), (1,4), (4,0), (4,0), actual per-worker model times 2809.95s, 2959.46s, 2846.00s, 2846.00s. All nine low and nine high first-generator prefixes are assigned exactly once. Independent threshold DP rules out any completion below 2959.46s at integer-centisecond resolution.
- Eight-worker exact optimum 1685.97s: (0,2), (0,3), (0,3), (1,1), (2,0), (2,0), (2,0), (2,0), with modeled times 1123.98, 1685.97, 1685.97, 1273.49 and four times1423.00 seconds. Again exact nine low plus nine high assignment and independent feasibility proof at optimal−0.01s.

A further fixed-setup exact algebraic amortization theorem in [ParallelWorkerLoads.lean](../../formal/025/ParallelWorkerLoads.lean) states that N physically independent source prefix jobs, each needing an original whole B6 target initialization of fixed hypothetical cost s, reduce total runner setup by (N−B)·s when regrouped into B nonempty SAME-PROCESS worker batches while preserving identical leaf search work. This is an identity about total work under a fixed per-build setup model, NOT a direct theorem about parallel makespan, cache reuse across GitHub machines or true physical source B10 pruning complexity. The enhanced [Lean kernel #38680108832](https://github.com/WhoSia/CUBE-REV/actions/runs/38680108832) completed SUCCESS with19 build jobs. A simple N=18,B=4,s=13.71s example saves exactly191.94 aggregate hypothetical runner seconds of setup. This complements, but cannot replace, the exact P-worker Bellman solver.

## 8. B10 sibling source calibration provenance and first engineering negative result

A deliberately small, read-only original full-cubie physical R10 probe was added: [genuine original 54-sticker C++17 U-R / D-R source-B10 sibling tester](../../scripts/cuberev-025/p0_r6i_p7_b10_sibling_cpp/main.cpp) and [independent Go suffix/source-court comparator](../../scripts/cuberev-025/p0_r6i_p7_b10_sibling_audit_go/main.go). These two depth2 cylinders lie WITHIN the already completed first-U and first-D B10 first-action proofs; they are performance calibration, NOT expansion from 2/18 full first-action covers.

The first workflow [#38679949807](https://github.com/WhoSia/CUBE-REV/actions/runs/38679949807) was officially FAILURE due to an OUTPUT RECEIPT NAMESPACE mismatch: the original C++17 physical source trial completed both shared-court R10 cylinders zero whole-cubie hits and exact per-prefix source accounting, but the workflow required P0R6I_P7_B10_MODE_COMPLETE while the cloned C++ pilot still emitted P0R6I_P7_MODE_COMPLETE. The job failed before independent rebuilt target or Go comparison and therefore MUST NOT be marked paired PASS. Its raw original physical shared log is preserved and contains two exact source-R10 prefix source word-call populations of1,310,203,083 each, source visits7,353,415 and7,353,394 and genuine whole-cubie B6 zero-meet. Physical source durations57.248 and55.183s, with shared setup15.189s, full process127.620s, peak RSS1,341,540KiB. The normal-form call populations were identical yet original geometry-dependent ordered-pair checks differed:88,754,209 (U-R) vs77,248,894 (D-R), packed edge checks17,574,309 vs15,032,971, full whole-cubie goal lookups94,759 vs69,511.

The typed label was repaired with GitHub commit c06a981102850992bb8380a1c349a26a7f0e2cb6. Read-only [resubmission #38680264075](https://github.com/WhoSia/CUBE-REV/actions/runs/38680264075) repeats full original B10 source checks shared and separately rebuilt with independent Go parity audit. Until full process, rebuilt phase and Go receipts ALL complete successfully, no independent physically paired B10 cost claim can be made. The previous physically verified B7 target-sharing comparisons and Go/Lean B10 cost models remain valid in their own scopes.


## 9. Fully completed TRUE source-B10 paired original-cube sibling calibration — exact physical and independent audit

**Historical first attempt #38679949807 FAIL must be retained:** the C++17 original source-B10 shared physical computation itself completed both U-R / D-R prefix cylinders with real B6 full goal zero intersections and exact canonical accounting, but stdout retained an older R6I-P7 receipt namespace while the workflow expected R6I-P7-B10, so CI failed before attempting isolated rebuilding and Go parity. Corrective commit c06a981102850992bb8380a1c349a26a7f0e2cb6 changed the emitted label only. No original physical move semantics or source DFA policy changed.

**Subsequent read-only actual original workflow [#38680264075](https://github.com/WhoSia/CUBE-REV/actions/runs/38680264075), job116242956310: COMPLETED SUCCESS.** Both real full original CP/CO/EP/EO physical source-B10 sibling cylinders were completely searched to radius 10, first with one shared original complete B6 and projected corner/edge court and then after rebuilding a new court for each prefix, with entirely independent Go original 18-letter suffix source-accounting and strict full physical parity.

Each original source prefix (U-R=action IDs 0,3 and D-R=IDs 9,3) has **1,310,203,083 exact source canonical iterative word calls**. They have identical canonical last-action state R and remaining source depth, but differ in true physical cubie starting state. The original physical source results in BOTH shared and isolated mode were identically:

| Original depth2 prefix | Canonical calls | Physical DFS visits | Mathematically sound omitted calls | Ordered candidate pair checks | Packed edge checks | Exact full-goal lookups | Full physical target meets |
|---|---:|---:|---:|---:|---:|---:|---:|
| U-R (0,3) |1,310,203,083|7,353,415|1,302,849,668|88,754,209|17,574,309|94,759|0|
| D-R (9,3) |1,310,203,083|7,353,394|1,302,849,689|77,248,894|15,032,971|69,511|0|

Thus the same full original B10 canonical language mass and nearly identical physical DFS visits do not imply identical original whole-cube projection pair/edge/full query cost. No heuristic projection collision is promoted to a full-cubie physical meet. Go independently checked every source call/skip equality, original full solved-side B6 8,240,087/CP projection1,405,068/EP projection7,672,278 cardinalities, 4,608 true full vs packed original move validations, one-vs-two target building scope and exact physical search counts on BOTH runs.

Actual same Actions worker resource receipts:

| Same original B10 paired worker | Shared FULL ORIGINAL B6 court built once | Separate B6 targets built twice |
|---|---:|---:|
| Whole-court setup |13,063.951ms|27,289.538ms|
| Actual full-source B10 two-prefix searches |86,636.796ms|91,397.531ms|
| Complete internal process wall |**99,701.318ms**|**122,344.709ms**|
| External /usr/bin/time wall |101.14s|122.40s|
| Peak process RSS |1,341,092KiB|1,359,176KiB|
| Built targets |1|2|

The verified complete-program saved time is 22,643.391ms = ~**18.51%** compared with independent rebuilding in this single paired source-B10 runner. Independent source/corner/edge physical visit/candidate counts agree EXACTLY across the two cost modes. Shared target setup is lower by14,225.587ms, and the remaining process-time difference also reflects runtime/cache/allocator effects; it would be unsound to attribute all22.64s exclusively to one fewer goal build.

The earlier source-B7 six-prefix matched physical experiments exhibited ~85% process-wall savings from sharing because their SOURCE searches were very short and setup dominated; the genuine B10 two-prefix experiment demonstrates why one cannot extrapolate that relative improvement to deeper original source searches. The first official FAILED workflow's U-R/D-R physical timings (57.248/55.183s for two source searches) also differed from the successful rerun (44.418/42.219s), so single worker/cache wall observations are NOT a universal constant. Correct conclusion: same-process read-only target court reuse is physically worthwhile and search semantics/proof obligations are preserved in these original source-B10 sibling tests, but precise speed improvement is hardware/time and original physical geometry dependent.

**No global proof upgrade:** the two U-R and D-R cylinders are STRICT subtrees of the already physically certified first-U and first-D original source-B10 action cylinders. They do not certify any of the sixteen still-open first-action source-B10 cylinders and do not establish original lower17. Current verified global source-specific original WCA whole-cube bound remains **16≤d18(s)≤18**.

**Resulting engineering direction:** batch multiple FIRST-ACTION or depth2 source proof obligations on a worker sharing one immutable original solved-B6 target, while emitting *separate* source prefix/DFA/remaining-depth/physical full-cubie no-meet receipts for each leaf. Then use a model with at least exact canonical source call weight + observed ordered candidate pair/packed edge/full target query counts + one-per-batch target setup and verified peak RAM; an unconstrained scalar word-count heuristic is no longer scientifically adequate. Protect target provenance, goal fingerprint, and external task/job authenticity. Only after a source-complete original B10 frontier is actually measured and independently audited may any lower17 claim be considered.

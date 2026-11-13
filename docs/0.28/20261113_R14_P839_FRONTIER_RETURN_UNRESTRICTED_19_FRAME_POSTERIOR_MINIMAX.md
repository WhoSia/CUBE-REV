# CUBE-REV R14-P8.39 — Strategic return from archival DFS to unrestricted 19-frame minimax

**Date:** 2026-11-13. **Status:** investigator-level specification / OPEN; **NO** newly verified 19-frame impossibility or 19-frame constructive policy asserted.

## Why return to the main conjecture now

R14-P8.37 recovered five previously problematic primary-classic sources and one duplicated acquisition, while P8.38 actually ran and verified the complete zero/one/two-fault static sensor census. Further minor archival-hunt iterations are now marginal compared with the core open problem: **does an unrestricted exact adaptive policy identifying the unknown legal Rubik cube state exist with at most 19 charged paired color observations?** Present fact: fixed protocol bound 21, constructive adaptive bound ≤20, adversarial lower bound ≥18; **19 remains unknown**. Different from static permanent-tag sensor costs.

## Precisely define the categorical action game

Let G be the finite fixed-center legal cube group. The hidden state g ∈ G is unknown but fixed at time zero. A public accumulated action T ∈ G sends it to current state T·g (orientation/convention must be fixed in implementation and validated against 48-sticker physical actions). At one charged observation frame, the observer reads exactly the six-way color of one designated spatial **edge** sticker and one designated spatial **corner** sticker: o(Tg) ∈ {0,…,5}², subject to physically attainable pairs. Legal public cube moves between observation frames are free **as defined in Paper B's experiment**. The decision rule may select each following public action as a function of past observation pairs. The required output is exact identification of initial g; if final physical state can be decoded instead, the public T makes these equivalent via inversion, provided full group actions remain bijective.

An exact dynamic-programming state is a posterior P ⊆ G and a public transform T. For each allowed free action a and pair output c, define fiber
F(P,T,a,c) = {g∈P : o(aTg)=c}.
Any admissible policy must preserve every feasible branch and meet maximum-frame-depth bound. The conceptual recurrence for available observation frames is

V(P,T)=0 for |P|=1;
V(P,T)=1+ min_{a∈A} max_{c: F(P,T,a,c) nonempty} V(F(P,T,a,c),aT),

where A represents the **precise permitted action closure**, not an invented arbitrary one-move restriction. A may be all legal action transformations if arbitrary free moves are truly permitted, but do not claim the group-min over all 4.3×10^19 transforms is computationally enumerated.

## Gate-controlled BFS/DFS execution plan

**BFS (broad):** Search competing complete representations of P: (1) original-sticker color constraint factorization; (2) exact group coset/orbit posterior; (3) sparse discrepancy and output-fiber dictionaries; (4) P8.6 exceptional root decomposition. Establish a model equivalence oracle for all small group toy instances and known exact P8.6 root samples before prioritizing a search scheme. Choose a canonical encoding that does not forget orientation, parity or public action T.

**DFS 1 (physical equivalence gate):** generate fixed-site query results with both independent P48 and original P8.6 physical implementations. On a bounded explicit set of small 18-move-prefix representatives, compare all output pairs and resulting posterior cardinalities, not merely chosen actions.

**DFS 2 (sound symmetry quotient):** only quotient T or P by transformations H that preserve the **permitted action set** and observation pair function up to a registered **bijective output relabeling**. For every accepted orbit reduction, verify commutation of action, transformed posterior and output fibers. If a single orientation/color counterexample exists, remove that H from the quotient.

**DFS 3 (19-frame adversary):** build admissible lower bounds on worst-case branch depth from capacity and explicit witness collisions. Do not turn a 12-initial-edge-restricted lower bound into an *unrestricted* ≥20 bound. Restrict a state family if and only if the restriction is proven closed under every policy action being excluded; otherwise a failed branch proves only that search heuristic failed, not that a 19-frame policy is impossible.

**Anytime and proof-contract conditions:** an upper bound **≤19** needs a complete executable policy covering all G initial states and all observation histories, with independent physical replay and SHA-sealed complete output-fiber receipt. A lower bound **≥20** needs an admissible universal adversary or a sound, exhaustive restricted quotient of all allowed policies. Logs and caches may accelerate experiments but are not the proof. Timeout/partial node coverage is `UNKNOWN`, never `NO_POLICY`.

## Strategic priorities

1. Close root observational equivalence and bidirectional physical action tests.
2. Execute bounded finite posterior-state experiments with exact test controls; archive counterexamples and permitted quotient symmetries.
3. Attempt 19 constructive branch refinement and only later full universal adversarial lower bound; both must survive an independent second implementation.
4. Track publisher-equivalent historical precedent from Sokolovskii/Hennie/Moore/Lee–Yannakakis; classic adaptive diagnostic ideas are *not novel* and should be credited.
5. Maintain the A-led integrated manuscript C0.3, but if the full 19-frame problem is still OPEN at a submission gate, disclose it rather than imply closure.

**Cycle principle:** archive-source DFS discovered Harary–Melter's old proof error, exact translations and potential source-claim pitfalls; fault-robustness DFS produced a new exact 1,048,576-layout finding. Next switch to the high-ambition main minimax problem, only diving into one posterior cache/symmetry bug when it directly blocks evidence.

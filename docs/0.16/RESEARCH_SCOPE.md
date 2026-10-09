# CUBE-REV 0.16 — source-backed mathematical research scope

**This is a research note inside the ONE formally titled CUBE-REV 0.16 version.** Internal P0/P1/P2/P3/P4 numbers are Notion filing divisions, not separately proposed project names. The 0.15 predecessor remains CLOSED; its two-adversarial-bit 15-vs16 exact optimum gap remains mathematically OPEN.

## Frozen mathematical model

- Physical state: tracked UR-edge cubie coordinate (current edge slot among 12, intrinsic flip among 2), total 24.
- Allowed actions: all 18 reversible outer-face HTM tokens. Observation after each chosen action: ideal one-bit intrinsic flip (equivalently complement orientation-zero bit).
- Three/four/five-action case studies: initial orientation either known flip0 and uniform over a chosen nonempty source-position subset, or explicitly both flips. No uncounted initial observation in 0.16 active feedback comparisons.
- Exact identification target: the entire original source coordinate under 0/1 error loss. For noiseless uniform beliefs, Bayes accuracy = number of nonempty terminal observation histories / initial support size.
- An adaptive policy may choose each next action based on the past reports; a fixed-word baseline commits all actions before reports, though the cost theorem generously allows its branch-dependent early STOP decisions.

## Exact finite results and evidence

1. **Counterfactual action observation:** 24 states refine into 2→6→24 observation-future congruence classes in two action-horizon increments. This is not a universally identifying two-move realized policy.
2. **Same entropy, different one-step decision value:** among all 66 equal-mass two-position known-flip0 priors, 48 have one-read adaptive exact MAP success1 and 18 only1/2.
3. **Two moves:** on all 4095 nonempty uniform source-position supports, adaptive and fixed optimal values coincide.
4. **Three moves:** exactly 2/4095 supports have adaptive value4/4 versus best fixed3/4: {1,3,5,7}, {8,9,10,11}. A hypothetical independent BSC(ε=.05) for these two priors yields adaptive .9025 versus fixed .6994375. No measured sensor noise is implied.
5. **Four moves, exact iff and sufficient-count compression:** let F={1,5,8,9}, B={3,7,10,11}, N={0,2,4,6}. On every one of 4095 supports, feedback is strictly better *if and only if* each category has **at least two original candidate slots**. Under this condition 6 adaptive histories versus 5 fixed; otherwise the optimal values tie. This is a machine-assisted exact complete finite decision over 18^4 fixed words, adaptive Bellman recursion, independently reimplemented C++/Python/Node. Minimal positive support antichain = 216 six-slot sets selecting 2 per class; total positive family = (6+4+1)^3 = **1331**. Both optimum values are constant on each of the 124 integer count triples (nF,nB,nN). The converse and invariance rely on executable finite enumeration, not a human-length standalone proof.
6. **Five moves under initial-orientation uncertainty:** each of 18^5=1,889,568 fixed words exhausted. Uniform ALL24 initial oriented coordinates (no time-zero reading) can yield 12 adaptive versus 10 fixed histories, i.e. exact-state recovery 50% versus 41⅔%; full12 known flip0 yields 8 versus 7. Thus feedback advantage is NOT monotone in horizon for each fixed prior: the two four-position h3 gap witnesses tie at h4.
7. **Cost threshold:** with h≤3, optional early stop, a read mandatory after every taken action and combined per-step tariff k=m+c≥0, exact rational frontier for each of the two four-state witnesses is J_adapt−J_fixed=max(0,1/4−k). Separate sensor and movement costs cannot be identified when each taken action always entails precisely one read.

## Claims NOT licensed

- No demonstration that humans can sense intrinsic cubie flip as an ideal bit, that the mathematical policies reflect actual cube solvers' plans, that solving the 24-state edge coordinate solves the entire 3×3, or that any cryptographic security assertion follows.
- No novel general discovery that causal controlled sensing can beat open-loop policies.
- No theorem that POMDP posterior/belief sufficiency, the Blackwell order, or adaptive-submodularity is new.
- No claim that a feedback advantage always grows with horizon or survives unknown initial orientation and costs.
- The exact 0.16 four-turn face-count summary preserves **optimal decision value** in the explicitly fixed task/horizon; it is not a recursively sufficient posterior or an optimal-policy identifier at all future horizons.

## Intellectual predecessors to compare explicitly

- Nitinawarat, Atia and Veeravalli (2013), **Controlled Sensing for Multihypothesis Testing**, *IEEE Transactions on Automatic Control* 58(10):2451–2464, DOI [10.1109/TAC.2013.2261188](https://doi.org/10.1109/TAC.2013.2261188), already discusses a causal feedback advantage over open-loop multihypothesis testing.
- Golovin and Krause (2011), **Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization**, *JAIR* 42:427–486, DOI [10.1613/JAIR.3278](https://doi.org/10.1613/JAIR.3278). Its approximation conclusions are conditional and must not be claimed for this reversible action model without verification of its assumptions.
- Smallwood and Sondik (1973), **The Optimal Control of Partially Observable Markov Processes over a Finite Horizon**, *Operations Research* 21(5), DOI [10.1287/opre.21.5.1071](https://doi.org/10.1287/opre.21.5.1071): belief sufficiency is classical.
- Blackwell (1953), **Equivalent Comparisons of Experiments**, *Annals of Mathematical Statistics* 24(2), DOI [10.1214/aoms/1177729032](https://doi.org/10.1214/aoms/1177729032): statistical experiment comparison is classical.

## What would make this a stronger paper?

A **non-enumerative necessity proof** explaining exactly why any category with fewer than two candidates prevents strict four-step feedback advantage, plus a structural derivation for the observed 124-class count-vector value invariance. The sufficiency of each-category≥2 has a constructive explanation: first use F then B to reveal the category, then conditionally choose an at-most-two-action suffix to separate a pair within each category, using the inherited 24-state two-step pair separability. The converse currently rests on a reproducible exhaustive finite court. Stronger generalization could vary the sensor's observable sticker/frame geometry or allow read-only actions; such variants must be declared as NEW observation contracts and must not be backfilled into the current theorem.

## Executable provenance

Public core and tests: `scripts/cuberev-016/active-belief-geometry.mjs`, `two-step-belief-census.mjs`, `three-read-feedback-census.mjs`, `horizon-feedback-court.mjs`, `cost-frontier.mjs`, `structural-support-court.mjs` and corresponding tests. Source-level original human reconstructions remain PRIVATE and are not part of these executables.

Full independent mathematical receipts/source code and SHA256 manifests are in the private Library directory `/CUBE-REV/0.16/`, with full pre-registrations and outcomes on the 0.16 canonical Notion page: https://app.notion.com/p/3f4ef561cf928161b4bfc5960f97ae8a

**This note is intentionally a conservative manuscript prospect, not a declaration of journal acceptance or new experimental human evidence.**

## Internal P5 — exact four-turn decision rank by geometric UPPER bounds and 36 short LOWER witnesses

**Progress inside the existing 0.16 version, not a new formal project/title.** A stronger mathematical result than the P4 4,095-mask census now explains the entire four-action optimum by a piecewise closed formula. In the frozen, *ideal one-edge intrinsic-orientation sensor* with original flip zero known, let `(f,b,n)` count initial candidate original slots in F={1,5,8,9}, B={3,7,10,11}, and N={0,2,4,6}. Define `T5={(0,2,3),(2,0,3),(1,2,2),(2,1,2),(2,2,1)}`, componentwise domination. Define `R=5` if the count triple dominates a member of T5; otherwise `R=4` if at least four positions and two nonempty categories; otherwise `R=min(f+b+n,3)`. **Exact theorem:** best four-turn fixed-word distinct history count `X4=R`; best adaptive count `A4=R+1` **iff** f≥2, b≥2, n≥2, and A4=R otherwise. There are exactly 124 nonzero category-count profiles. This is optimal **decision VALUE** sufficiency for one stipulated model/horizon, not a human mental representation, recursively sufficient posterior or cost-independent finding.

**Proof level matters:** The upper bounds `X4≤5`, `A4≤6`, the F/B-first branch capacities, the five minimal rank-5 count inequalities, and the singleton-category rank-3 obstruction are derived from the physical U/R/D/L four-cycle incidence: every other-face turn transports exactly one F slot, one B slot and two N slots, while only odd F/B turns flip the tracked orientation. The lower bounds do **not** use full 104,976 four-action words or all 4,095 support masks: a frozen 36-word legal four-turn construction catalogue separates all 220 three-position bases, all 492 admissible four-position bases and all 480 admissible five-position bases. Independent direct physical C++20, Python and Node certificate checkers confirm these 1,192 small bases. This finite construction is an explicit **machine-checked small set-cover certificate**, not a fully calculation-free human derivation of the 36 words. The earlier 124-value table is only a regression comparison, never used as a premise for this new proof.

**Additional pure math obstruction:** `r(S)=X4(S)` violates submodularity: with Q={0,2,3,4}, u=1 and v=5, the proven ranks are `r(Q)=r(Q+u)=r(Q+v)=4` but `r(Q+u+v)=5`. Thus the cube-constrained maximum-over-experiments rank is not a matroid rank. This does NOT contradict the fact that each *fixed* partition's individual hit-count rank is submodular, or any classical matroid theorem. Distinct **value** symmetry across category counts also does not imply the full action-experiment set admits S4³ permutation symmetries.

**Reproducible custody:** private math-only package `/CUBE-REV/0.16/CUBE_REV_016_P5_COMPACT_GEOMETRIC_RANK_PROOF_PRIVATE_20261009.zip`, SHA-256 `e6f15e58c65fe9ed350d72b9dbce099203434a1ef3a8fbd060e5f2c7deb04c78`, Library ID `libfile_8965475f58d88191b96c048d62965317`. Twelve files; ZIP CRC and **clean-extracted** quick checker PASS (Python/C++20/Node independent 36-word replay, ten-file SHA256 manifest). Full proof is on the 0.16 canonical Notion §21, `THEOREM.md` inside the private package, and source exports in the existing `scripts/cuberev-016/structural-support-court.mjs` plus regression test. The stronger open challenge is to replace the 36-word finite lower certificate by one uniform incidence-square construction or prove a minimum-size universal separating-word catalogue. Existing P3/P4 results are not retroactively reclassified as handwritten theorems.

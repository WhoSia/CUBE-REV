# CUBE-REV 0.19 — P0: Five-Turn Physical Observability and Access Boundaries

**Lab/version:** CUBE-REV 0.19 OPEN. This is a research memo; the four-turn proof remains the completed 0.18 theorem. **Do not state M*(5) = 8.**

## Physical oracle and parity
Reference: `scripts/cuberev-018/export-mstar-physical.mjs`, `scripts/cuberev-015/ur-fiber-tomography.mjs`, `scripts/cube/sticker-cube.mjs`.
Input original physical source SHA-256: `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`.

An independently implemented sticker-coordinate Python oracle reproduces **all 104,976 four-HTM words**, **1,913 partitions**, **1,477 coverage types**, and the canonical maximal-source coverage masks. It uses the same 18 outer face HTM actions, tracks twelve initial flip-zero UR-edge positions, and records one intrinsic orientation bit after each action.

## Length-five full-history exhaustive result
- Exhaustively enumerated **18^5 = 1,889,568** actual 5-HTM words.
- **14,938** distinct twelve-state observation partitions, **14,446** distinct source coverage types; **8,807** inclusion-maximal coverage types.
- All **1,192 original source requirements** remain the requirement family. The bipartite graph of all rows and maximal L5 experiments has **one** connected component.
- L5-specific implication reduction: **544 retained rows**, precisely 480 original five-element requirements and 64 four-element requirements. 648 others are implied on all L5 maximal columns. Dominance reduction leaves **2,887** projected maximal columns. L4's 398-row reduction is **not validly portable** without re-proof.
- Physical orientation-output histories across the 12 starts have at most **7 distinct patterns at L=5** (against the generic binary-output limit 32); full L4 enumeration attains at most **5** patterns. This bound was established by exhaustive enumerations, not a group-theoretic symbolic theorem.

## Integer-checkable exact interval, not exact optimum
`6 <= M*(5) <= 8` for unchanged source family, fixed nonadaptive five-HTM words, full five-bit history and unit dictionary-entry cost.
- **Upper 8:** eight actual five-move strings cover all 1,192 original source sets when the Python geometric oracle independently replays their observations:
  1. F' B' L F B
  2. F' B' R F B
  3. F' B' D F B
  4. F L2 B' D2 F
  5. F U2 B R2 F
  6. F' B' U F B
  7. F B L F B
  8. F B R F B
- **Lower 6:** an integer dual-weight certificate assigns 70 original source rows weights with total numerator 384, denominator 72. For every one of 14,938 exhaustive 5-move observation partitions, covered-row weighted numerator <=72. Thus dictionary size >=ceil(384/72)=6. This **does not** settle SAT/UNSAT for <=7 words.
- MIP incumbent 8 after a time-limited optimization, and multiple randomized greedy upper attempts found 8; neither is a proof of no 7-solution.
- Physical basis 0.18 is separately **exact M*(4)=34**, independently checked DRUP proof: https://github.com/WhoSia/CUBE-REV/actions/runs/37958523951 .

## Observation access ablations (same five HTM moves)
- Only final **three** observation bits accessible: 14,167 partitions; feasible for all 1,192 source sets; constructive upper **13**.
- Only final **four** bits accessible: 15,047 partitions; feasible; constructive upper **12**.
- All **five** observation bits accessible: 14,938 partitions; constructive upper **8**.
- Only final two bits accessible: no five-state source set can be distinguished by one such word (<=4 output codes), making original source-family coverage impossible.
- All 13/12/8 values are **upper bounds**, not proven optima. Distinct partition-type counts over different candidate words are not themselves monotone in observation richness. These are transcript-truncation experiments, **not a cognitive working-memory capacity measure**.

## Ontological / computational limits
M* is a minimum-size **experiment dictionary**: for every known source subset A in the frozen requirement family there exists at least one word in the dictionary whose output history is injective on A. It is **not** the number of visual observations, moves to solve, amount of human memory, a universal Rubik state identifier, or cost of an adaptive online policy when A is unknown.

The reduction from original L4 incidence's one connected component to L4 exact-quotient's two components (334x80,64x88) is **optimization-representation-dependent**, not established as a physical group-action invariant. At L5 even the maximally reduced 544x2887 incidence remains connected.

For a partition with block sizes b1,...,bk, the count of distinguishable unrestricted r-element subsets is the elementary symmetric polynomial e_r(b1,...,bk); our source-family incidence additionally filters admitted subsets. In this particular cube intrinsic edge convention only F/B *quarter turns* can toggle edge orientation (four of twelve starting positions for any such move); all other HTM face moves preserve the bit.

Scientific priority: externally reproduce the L5 computation in CI; settle k<=7 with portable SAT/UNSAT proof; characterize structural changes in observation partition geometry and row implication; only then investigate adaptive access, genuine memory constraints, and external human data. Related classical finite automata state-identification theory already covers preset vs adaptive experiments, so these general notions are not claimed as new.

**Notion research record:** https://app.notion.com/p/3f4ef561cf92813d9edfff4911db39d2
**Harvest/re-entry candidates:** https://app.notion.com/p/3f4ef561cf928151977ce781f267d650

## Further physical mechanism: flip-capable action budget is nonmonotonic

Independent full enumeration over every 4- and 5-HTM word, grouping by the count (q) of tokens among `F, F', B, B'` (the only actions that can change the intrinsic edge-orientation bit). The maximum numbers of distinct histories across the 12 initial zero-flip positions are:

| Full physical word length | q=0 | q=1 | q=2 | q=3 | q=4 | q=5 |
|---|---:|---:|---:|---:|---:|---:|
| L=4 | 1 | 2 | 4 | 5 | 3 | — |
| L=5 | 1 | 2 | 4 | 7 | 7 | 3 |

For L=4 there are precisely 768 physical words distinguishing at least 5 initial states, all with q=3. For L=5 there are 43,584 with q=3 and 6,912 with q=4, and **none** with q=5. Every other action can transport edge position without immediately changing the orientation output, thereby enabling later separating signals. Thus merely maximizing the count of actions that might change the sensor bit is *not* an information-optimal strategy. Trivial general inequality: the whole output trace is determined by q possible changes from initial bit zero, hence the number of different traces is <=2^q. The much sharper observed limits (5 and 7, and the q=L collapse) still require a separate structural proof beyond exhaustive verification.

The **8-word** L=5 cover, exact integer **lower bound 6**, and suffix-access 13/12/8 constructive bounds are preserved as **local deterministic verification** outputs, not newly GitHub-CI-certified and not a claim that M*(5)=8.

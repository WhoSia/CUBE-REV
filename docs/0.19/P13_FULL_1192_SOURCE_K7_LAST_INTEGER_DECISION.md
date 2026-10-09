# CUBE-REV 0.19 — P13: Last Full-Source Seven-or-Eight Decision, Physical Integer Gate, and Proof-Producing Exact Court

## Exact current mathematical status — 2026-10-10

For one tracked UR edge starting intrinsically flip-zero at one of twelve physical slots, exactly five legal HTM actions per nonadaptive fixed word, complete orientation-bit readout after each action, and the frozen original 1192 source subsets R:

`7 <= M*(5) <= 8`.

The lower 7 is inherited from the **original-480-five-source exact seven** locally certified via P12's 445 row-weight certificates and complete remaining physical high-rank case checks; the upper 8 is a real physical eight-word original-R cover (independently replayed). Thus full original k<=6 is disproved as a theorem. **The remaining original 1192-source <=7-word SAT/UNSAT decision is NOT established in this P13 note.** A 150-second full 544x2403 SciPy/HiGHS MIP returned TIME_LIMIT/UNKNOWN and no seven-word model. A separate 110-second guided seven-word physical candidate search reached four uncovered original five-state rows but did NOT cover all 1192; an exact two-word replacement check for that specific incumbent's 21 fixed-five subcases also found no SAT witness. These diagnostics are NOT k7 impossibility certificates.

## P13 new original-physics conditional rank rigidity: seven requires at least TWO high-observability experiments

Define rank(w) as the number of distinct cumulative five-bit orientation histories across the twelve starting edge slots; a high-rank word has rank>=6. The original physically realized **480 five-source** restricted cover types from all 14938 physical observation partitions are:
- rank5: 2168 distinct physical source-coverage types;
- rank6: 1144;
- rank7: 32.
Rank<=4 identifies no original admitted five-state source.

**Theorem:** Any dictionary of <=7 physically realizable fixed five-HTM words identifying every original R5 five-state source must contain at least **two** high-rank words. In particular this holds for any hypothetical full original-R seven-word dictionary.

**Proof (exact original-physical finite split):** P12 already excludes five or fewer R5 words, so every selected member of an original-R seven-cover has rank>=5 (else six words would cover R5). If zero high words are selected, seven rank5 words distinguish at most 7×64=448 of 480 sources. If exactly one high word is selected, exhaust all 1176 original physical high-rank five-source cover masks h. For 1144 of them, letting U be five-source rows missed by h and g=max over each physical rank5 word of the size of its coverage on U, exact bit counts give |U|>6g. Thus six rank5 words cannot fill the uncovered rows. The remaining **32** high masks each have an independent **positive integer row-weight vector supported only on U**, with integer total W and maximum physical rank5 word covered weighted demand B satisfying **W>6B**; all 2168 ORIGINAL physically realized rank5 masks were exhaustively checked by a separate standard-library-only checker. Minimal strict integer gap among the 32 cases is **2,210,288**. Therefore zero or one high-rank word is impossible. The 32 original-row-cover-mask-keyed integer certificates are at docs/0.19/P13_K7_AT_LEAST_TWO_HIGH_PHYSICAL_INTEGER_DUALS.json. Generation used exploratory fractional LP, but actual proof uses only exact integer arithmetic.

## Complete source-locked exact 544x2403 SAT instance

Standalone no-solver builder scripts/cuberev-019/prepare-L5-full-k7-physical-CNF.py:
1. Replays every one of 14,938 original physical observation partition representatives using independent 18x24 sticker-derived actual action maps, confirms 14,446 complete-original source-coverage types.
2. Computes 8,807 inclusion-maximal original source-coverage columns. Applies all-k candidate-support implication to original 1,192 rows to obtain the original exact 544-row core (480 original five-source +64 mixed four-source demands). Applies projected column dominance to obtain exactly 2,887 physical words.
3. Uses the separately verified P12 source-original R5=7 lower bound to discard rank4 candidates in a **k<=7-specific** way. Leaves **2,403** physically realizable, individually source-replayed word choices (rank5=1,355, rank6=1,016, rank7=32). The source core remains all 544 constraints: do NOT replace it with 480 five-source constraints.
4. Verifies all 16 signed-coordinate incidence automorphisms on **all original 1192 source masks and all 8807 physically realized full-original maximal word masks**, and on the reduced rank-eligible columns. They preserve rank. Rank-eligible columns have **164 orbits**: rank5 95, rank6 66, rank7 3. Since at least two selected words are high, one chosen high word may be relabeled to one of **69 high-rank orbit representatives**, giving a symmetry-safe OR clause over 69 column variables. **All 2403** actual Boolean choices remain distinct.
5. Validates the original full-source 70-weight positive integer dual (total source mass 384, per real word <=72). In a <=7-word full-source cover, any selected pair must cover at least 384-5*72=24 distinct weighted demand. Among surviving rank>=5 full-source columns, exactly **102,979** distinct candidate pairs fail the exact weighted union condition, so each gives a sound binary clause `not x_i OR not x_j`. The stronger k6 pair threshold of 96 is *not* applicable here.
6. The pure-Python local source-locked preparation, including original physical replays and full 16×8807 incidence-automorphism checks, **PASS**: 544×2403, 69 high first-column representatives, 102979 valid dual pair clauses. Output (2.4MB) source-locked JSON kernel is retained in the Drive P13 archive, not assumed to be an external CI result.

## Proof-producing final decision contract

Standalone source scripts/cuberev-019/solve-L5-full-k7-physical-SAT.py uses PySAT's Glucose4 proof logging:
- 544 mandatory original full source-core covering clauses;
- 69 physically validated high-representative symmetry-breaking OR clause;
- exact 102979 sound full-k7 dual-derived forbidden pair clauses;
- bound **at least two** rank>=6 words (supported by independent 32-certificate finite physical proof);
- bound **at most seven** physically realizable words (normal set-cover cardinality).

**SAT branch:** Replay every selected word's physical 18x24 transitions and check full 1192 original sources, at most seven real words, and a *private admitted five-source witness* for each of the seven, which follows from independent P12 seven-minimality.

**UNSAT branch:** Emit the **exact CNF and solver proof trace**. Independently check the actual emitted CNF/proof with pinned external `drat-trim`. Separately audit the soundness and physical closure of all source/column, P12 rank4, P13 rank-two high, symmetry and dual pair transformations before claiming that the original physical k7 is UNSAT. A proof of a strengthened CNF is insufficient without these lemmas; both exact scripts recheck them.

**Budget exhaustion or numerical MIP failure means UNKNOWN**, never a negative theorem. The fully source-regenerating GitHub workflow is `.github/workflows/cuberev-019-p13-full-k7-physical-proof.yml`. It first independently reruns the exact P9/P12 finite original-physics proof, then P13 rank-two integer proof, rebuilds the 544x2403 CNF, attempts actual Glucose4 and independently checks any DRUP, and only promotes:
- `M*(5)=7` if a REAL source-replayed seven-word full-original cover exists;
- `M*(5)=8` if the full <=7 CNF is externally DRUP-verified UNSAT and the already checked eight-word physical upper is again replayed;
- else retains `M*(5) in {7,8}`.

**The new CI workflow source is committed, but neither a completed P13 run receipt nor a verified full-original k7 SAT/UNSAT result is available yet. Do not describe this as closure.**

## Proof-relevant technical limitations and research direction

The verified fractional original-R cost 16/3 (P8) is lower than both discrete possibilities 7/8 and cannot distinguish them using further ordinary row-linear positive duals. The P12 restricted-source optimum 7 creates a new **extremality rigidity**: every chosen word in a seven-word full-R dictionary must carry its own private admitted five-source requirement. The full-R four-source demands, especially the irredundant 64 mixed four-state rows, introduce nontrivial extension obstruction; the specific P10 restricted seven-word witness misses 72 smaller requirements and cannot be repaired by one eighth experiment. This does NOT prove that *all* R5 seven-word dictionaries lack full-R extension.

Next exact attacks after present k7 SAT attempt are fixed high-rank-count branches t=2..7; conditional source-dual certificates after one of 69 high orbit representatives; collision-hypergraph source-extension obstructions involving private five-source rows and 64 irredundant four-source rows. Avoid promoting an early SAT heuristic failure into a universal obstruction.

## Reference links

- [P12 original five-source exact seven](P12_EXACT_PHYSICAL_FIVE_SOURCE_SEVEN_BY_RANK_CERTIFICATES.md)
- [P13 physical source-locked integer proof](P13_K7_AT_LEAST_TWO_HIGH_PHYSICAL_INTEGER_DUALS.json)
- [P13 no-solver full physical kernel builder](../../scripts/cuberev-019/prepare-L5-full-k7-physical-CNF.py)
- [P13 independent two-high-rank physical verifier](../../scripts/cuberev-019/verify-L5-full-k7-at-least-two-high.py)
- [P13 proof-producing SAT/DRUP court](../../scripts/cuberev-019/solve-L5-full-k7-physical-SAT.py)
- [P13 all-gates source-reproducing Actions](../../.github/workflows/cuberev-019-p13-full-k7-physical-proof.yml)
- [Notion active CUBE-REV 0.19](https://app.notion.com/p/3f4ef561cf92813d9edfff4911db39d2)

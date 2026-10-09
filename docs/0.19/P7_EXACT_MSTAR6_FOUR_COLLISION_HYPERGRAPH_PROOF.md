# CUBE-REV 0.19 — P7: Exact Six-Turn Minimum Dictionary via Collision-Hypergraph Finite Proof

## Theorem, scope and evidence
For the *same frozen 1,192 source requirements* of twelve original flip-zero tracked UR-edge positions, the real sticker-derived 18-HTM cube action automaton, and the **complete intrinsic edge-orientation observation after each of six fixed moves**, the smallest cardinality of a nonadaptive fixed-word experiment dictionary is **M*(6)=4**, conditional only on the independently reproducible finite enumerations and physical transition implementation in this record.

This is a **locally re-executed complete finite computer-assisted proof**, not a new peer-reviewed general theorem and not yet an externally confirmed GitHub Actions PASS receipt. As always, the minimal number of dictionary entries does *not* represent Rubik solution move count, full 3×3 cube state identification, or human memory. The separate L4 exact M*=34 has independently DRUP-checked GitHub CI receipts; the separate L5 integer value remains unknown in {6,7,8}.

## Physical model / source authority
Canonical physical instance is reconstructed using scripts/cuberev-018/export-mstar-physical.mjs and sticker-derived urMoveAutomaton(). Input source physical SHA256: `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`. State starts (slot p, flip=0), p=0,...,11. Source family R comprises 220 admitted triples, 492 mixed four-subsets and 480 admitted five-subsets. All words use the legal physical 18-HTM action alphabet, with one output bit after each action.

## Upper bound: physical four-word certificate
The following physical 6-turn words distinguish every admitted source A for at least one of the four words:
```
F B U2 L F B
F' B' U L2 F B
F B U2 D F B
F B' U2 R F B
```
Independent Python replayer `scripts/cuberev-019/verify-L6-to-L9-dictionaries.py` checks all four against all 1192 original source masks, using real sticker-derived 18×24 maps, and validates the full union cover. Therefore M*(6)<=4.

## Lower bound: no three-word physical dictionary
A complete logical and finite-verification chain has seven independent gates. A SAT solver merely timing out would NOT qualify.

**Gate 1 — enumerate all potentially relevant original physical output partitions.** Among all 18^6=34,012,224 physical 6-HTM words, let q count the F/F'/B/B' tokens, the only flip-capable actions. For q<=2, at most 2^q<=4 different output histories are possible. For q=6 (all F/B flip turns), the F/B/N position-triplet confinement invariant limits rank to at most three. Thus a word with rank>=5 must have 3<=q<=5. The independently compiled C++ physical enumerator explores exactly 4,350,976 real words with q=3,4,5 and reconstructs 53,528 distinct physical output partitions having rank>=5.

**Gate 2 — a three-word cover must contain three rank>=5 words.** Because R includes 480 admitted five-element requirements, no rank<=4 word can distinguish *any* of those 480. An independent bitset C++ program builds five-requirement coverage for all 53,528 distinct physically realized rank>=5 partitions. For every first word it intersects the available second-word coverage supports on each five-source requirement the first word misses, and concludes no pair covers the full 480 five-set family. It explicitly asserts the independent check count 1,158,155. Therefore at most two rank>=5 words cannot cover those 480; every member of a hypothetical three-word full cover must have rank>=5.

**Gate 3 — exact collision-pair refinement kernel.** Let B(w) be the 66-pair bad-collision graph, {i,j} in B(w) iff outputs are equal. If B(u) subset B(v), then every source distinguished by v is also distinguished by u, for every source family. The C++ collision-refinement kernel removes a candidate v only if a retained physical candidate u has B(u) subset B(v), and records a source-to-parent witness. It reduces 53,528 ranks>=5 observational partition types to exactly **18,813**, preserving the existence of every <=3-word cover. A separate Python auditor replays every source word with the original physical maps and checks all **53,528** individual inclusion witnesses against their actual 66-pair graphs.

**Gate 4 — all 16 geometric incidence symmetries verified.** Enumerate 16 signed coordinate reassignments of initial slot coordinates preserving the original F/B/N source admission structure: (x,y,z)->(±x,±y,±z) or (±y,±x,±z). Some are orientation-reversing and NOT legal cube actions. They are valid *incidence automorphisms* because a separate exhaustive verifier checks all original 1192 source sets and the **complete original 53,528 realized rank>=5 physical output-partition family** closed under each permutation. The 18,813 reduced kernel is also closed. Rank>=8 members number 196, partitioned into exactly **16 high-column orbits**. Hence a three-word dictionary with exactly one high-rank word can be relabeled so that its high word is one of 16 representatives.

**Gate 5 — eliminate three low-rank words by an exact integer dual.** An explicit independently stored positive integer weight vector on 172 of the original five-element source requirements has total weight **3,126,804**. Among all retained rank<=7 physical candidates, the maximum weighted contribution of any one word is **1,000,010** (computed with exact integer arithmetic, not inferred from a floating-point LP). A hypothetical three-word cover using only rank<=7 words covers weighted source mass at most 3,000,030 <3,126,804. Thus any three-word cover must have at least one rank>=8 word. The certificate is `docs/0.19/P7_L6_INTEGER_DUAL_FOR_REDUCED_LOW_RANK.json`. The preceding dominance gate is required before this bound applies.

**Gate 6 — eliminate at least two high-rank words.** For all **C(196,2)=19,110** distinct high-rank word pairs, form the exact intersection of the sets of original source requirements failed by both. The finite auditor examines every possible third physical retained word and finds none covers all residual failed requirements. Therefore no three-word cover can contain two or more high-rank words.

**Gate 7 — eliminate exactly one high-rank word.** By Gates 4–6, any hypothetical three-word solution consists of precisely one rank>=8 word and two rank<=7 words, and the high word may be fixed to one of the 16 verified orbit representatives. For every one of 16 representative choices and all 18,617 retained low-rank choices of the second word, the finite auditor checks whether **any** of the 18,617 low-rank third words satisfies every original source unmet by the first two. Exactly **16×18,617=297,872** conditional cases are exhausted; every one is rejected.

All possible three-word physical dictionaries fall into one of those cases, so **M*(6)>=4**. Combined with physical four-word upper, **M*(6)=4**.

## Local independent verification
The original local chained reproducer `P7_prove_L6_k3_end_to_end.py` completed its complete integer/physical checks in 31.242 seconds, final exact-branch receipt:
```json
{
  "result": "CUBE_REV_019_L6_K3_FINITE_UNSAT_LOCAL_PASS",
  "full_rank5_candidates": 53528,
  "collision_inclusion_kernel_candidates": 18813,
  "full_symmetry_group": 16,
  "rank8_or_9_columns": 196,
  "high_orbit_representatives": 16,
  "verified_integer_dual_total": 3126804,
  "verified_integer_dual_max_low_word": 1000010,
  "k3_at_least_two_high_pairs_checked": 19110,
  "k3_exactly_one_high_second_word_cases_checked": 297872
}
```
This is a transparent computer-assisted finite counting proof, not an external independent DRUP SAT proof. A fresh GitHub Actions workflow was written to regenerate all original physical inputs, cross-check these steps, replay the 4-word positive cover, and upload signed-by-run source hashes and logs. Do NOT claim workflow PASS until a completed-run receipt is independently observed.

## Canonical source / custody
- Main physical source: `scripts/cuberev-018/export-mstar-physical.mjs`.
- Physical six-step full relevant enumerator: `scripts/cuberev-019/export-L6-rank5-partitions.cpp`.
- Independent two-word 480-five-set impossibility: `scripts/cuberev-019/prove-L6-two-word-five-core.cpp`.
- Original-to-kernel collision dominance + per-input parent witnesses: `scripts/cuberev-019/L6_collision_refinement_kernel.cpp`.
- Full original physical/source/symmetry/dual/inclusion/k3 check: `scripts/cuberev-019/prove-L6-three-impossibility.py`.
- Four physical upper replay: `scripts/cuberev-019/verify-L6-to-L9-dictionaries.py`.
- Exact integer lower-bound 172-row dual receipt: `docs/0.19/P7_L6_INTEGER_DUAL_FOR_REDUCED_LOW_RANK.json`.
- Read-only fully chained GitHub Actions: `.github/workflows/cuberev-019-l6-exact-court.yml`.
- Google Drive exact Python proof source: https://drive.google.com/file/d/1uutAUzqUUqRxZfpgSXJLH_Tn8IMHdC1w/view (source synced into GitHub).
- CUBE-REV 0.19 canonical Notion: https://app.notion.com/p/3f4ef561cf92813d9edfff4911db39d2 .

## What remains mathematically open
The sole remaining unclassified integer in the entire frozen horizon profile is **M*(5) in {6,7,8}**. Prior L5 dual/primal establish exactly 16/3 fractional set cover optimum, with 16 exact incidence symmetries and 196 column orbits. L5's 544×2,887 irredundant cover cannot be reduced using L6's 18,813 kernel without rederiving the actual five-word physics, its own collision families and admissible-source quotient. Transfer the **proof methods** (rank-gating, collision inclusion, original-source integer weights, orbit-representative branch certification, conditional residual obstruction), not unproved numerical results.

Reference intellectual ancestry: physically restricted perfect hash families; separating systems; automata distinguishing sequences; symmetry-aware exact combinatorial optimization; certified dominance breaking. No claims that these generic notions originated with CUBE-REV.

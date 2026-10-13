# CUBE-REV 0.25 P0-R3 — An Exact Continuous Cost-Partition No-Go for Two Physical Cubie Patterns: 7,290 Half-Unit Tests, Ten Real Rubik Word-Count Certificates & Independent Original 54-Sticker Replay

**13 October 2026 · Mathematical finite theorem for the specified two-pattern, face-uniform cost-sharing class; Go original physical finite jobs SUCCESS; independent standalone Node original 54-sticker witness checker [CI SUCCESS #38356444729](https://github.com/WhoSia/CUBE-REV/actions/runs/38356444729).** This closes one narrowly but genuinely mathematically nontrivial subproblem, NOT the full original 3×3 global 17-or-fewer search. Existing source-complete whole-cube **14≤d18(s)≤18** stays unchanged.

## 1. Fixed original physical source and projection contract

Official WCA Seoul Summer 2026 3×3 Final Group A scramble 1 (original legal HTM 20-turn string):

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

The previous actual 54-sticker-verified original whole-cube 18-turn completion:

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

is an upper bound, not an optimality theorem. [Prior P1-R6 actual whole-cube 13-or-shorter exclusion](../0.24/P1_R6_SOURCE_COMPLETE_FULL18_GLOBAL_BIDIRECTIONAL_CERTIFICATE_AND_025_GATE.md) externally completed.

The original P0-R1 five exact actual physically derived oriented cubie group-action projections are **E0=[original edges 0,4,8,10], E1=[1,5,9,11], E2=[2,3,6,7]**, and **C0=[corners 0,2,4,6], C1=[1,3,5,7]**, original reference edge order UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR and corners URF,UFL,ULB,UBR,DFR,DLF,DBL,DRB. Source shortest quotient HTM distances are respectively **7,5,5,5,6**. These are NOT separate full-cube distances. The physical action is always one of original 18 HTM, and the original whole-cube source is fixed.

## 2. Generic mathematical theorem: a small pair of words bounds a continuum of face prices

Take ANY two distinct such physical projections i,j, ANY real face-price vector x=(x_U,x_R,x_F,x_D,x_L,x_B) with **0≤x_f≤1**, and charge the price x_f to projection i and 1−x_f to projection j for EVERY genuine U/U'/U2, etc face HTM action. All other projections receive cost zero; this is a globally valid, physically admissible unit HTM action partition.

Let h_i(x) be the **true weighted shortest source-to-solved marked-cubie path** in the original 18HTM action-induced projection; its distance is the infimum/minimum over all FINITE legitimate original face words solving the marked projection, with x price. Similarly h_j(1−x). Each true original full-cube solving word projects to legal solution words in both, so:

    h_i(x) + h_j(1−x) ≤ d18(s,e).

For ANY TWO explicit legal projected source-solving words u_i and u_j, let n_i(f) and n_j(f) be their respective number of original legal HTM turns on face f (ignoring turn power but NOT claiming full-cube solve). By optimizing each quotient:

    h_i(x)+h_j(1−x)
      ≤ Σ_f (n_i(f) x_f + n_j(f)(1−x_f))
      ≤ Σ_f max(n_i(f),n_j(f)).

The second inequality holds separately for each face, since each pair of nonnegative weights x_f, 1−x_f sums to 1. It is true for **ALL REAL x_f, not merely integer or half-integer prices**. Therefore a real legal projected word pair with face-count envelope ≤7 is a **finite exact universal 7 upper certificate** on that pair's maximum additive admissible PDB heuristic. Physical path replay plus six small integer count checks is enough for independent validation; no floating-point optimization is needed.

Note this is an **upper certificate on the best admissible TWO-PDB heuristic**, not a lower-bound certificate establishing the original cube distance seven. We already know the WHOLE original cube is at least 14 away from solved. This explains why the abstract optimization fails to recover full corner-edge noncommutative synchronization.

## 3. Ten real original-cube word-pair proof packets

Original literal generated move words, ALL source-attested by [Go shortest-projection physical DAG run #38355753083](https://github.com/WhoSia/CUBE-REV/actions/runs/38355753083) except the special E2 nonshortest 7-word from [Go source-directed face-quota physical run #38356018621](https://github.com/WhoSia/CUBE-REV/actions/runs/38356018621). Reproduced in compact [ten-pair JSON certificate](../../data/cuberev-025/p0_r3_continuous_face_price_ten_physical_word_pair_witness.json) and independently replayed by [Node original whole 54-sticker checker](../../scripts/cuberev-025/verify_p0_r3_continuous_face_price_original_54sticker.mjs).

| Distinct genuine physical pattern pair | Legal original source→projection-goal word in pattern A | Legal original source→projection-goal word in pattern B | Σ face-wise max |
|---|---|---|---:|
| E0 / E1 | U' B' R2 U L B2 R' | R2 B U' L2 B' | 7 |
| E0 / E2 | F B' U F R' L2 U2 | U2 F B2 U2 R F' L' | 7 |
| E0 / C0 | F B' U F R' L2 U2 | U2 F R' U2 B2 | 7 |
| E0 / C1 | U' B R2 D' B2 R U | U' B' R2 D2 R U | 7 |
| E1 / E2 | R2 B U' L2 B' | U2 B' L2 B' L' | 6 |
| E1 / C0 | D B U' D' L2 | D B2 L' D B' | 6 |
| E1 / C1 | R2 B U' L2 B' | U L2 U2 B R' U | 7 |
| E2 / C0 | U2 B' L2 B' L' | D B2 L' D B' | 7 |
| E2 / C1 | U2 B' L2 B' L' | L2 U B2 R' F' L | 7 |
| C0 / C1 | U2 F R' U2 B2 | U L2 U2 B R' U | 7 |

Each source word alone solves its specified four labeled ACTUAL corners or edges in the **original fixed 54-sticker cube**, with position and orientation both restored. It generally does NOT solve the full source cube, and is NOT an original human-authored FMC candidate or observed behavior. There are 20 WORD POSITIONS in the certificate; repeated lexical words appearing in more than one pair do not represent independently observed real-world solves.

**The special E0/E2 lesson:** E0's actual shortest projected solution length is7 and E2's is5, but restricting both certificates to separately globally shortest projected words gives minimum face-count envelope **8**, which was measured by source-complete shortest-word DAGs. It does NOT follow that the priced optimum exceeds7. A **legal but NONSHORTEST E2 projection solution of length7** shares the complete face count exactly with E0's seven-word:

    E0: F B' U F R' L2 U2
    E2: U2 F B2 U2 R F' L'
    Both counts in face order URFDLB: [2,1,2,0,1,1]

Their total priced cost is exactly seven for EVERY continuous face-price vector. Source-directed exhaustive six-face-budget DFS found the E2 projected solution after 103 source DFS calls / 69 rejected-state memo entries on one enumerated E0 shortest count vector. Thus a local 'only separately shortest words' optimization would falsely conclude the most important useful upper certificate was absent. This is a REAL CUBE source-specific program-choice phenomenon; it is not evidence that a person considered either sequence.

## 4. Exact full continuous two-pattern optimum

For each of the ten pairs, the physically replayed explicit word pair bounds ALL continuous price assignments above by seven. Therefore:

    sup_{i<j, x ∈ [0,1]^6} [ h_i(x) + h_j(1−x) ] ≤ 7.

Conversely, taking pair E0 + any other pattern, and allocating the FULL unit face cost to E0 (x_f=1 for all six faces, thus 0 for the other projection) gives EXACT E0 original source distance 7, independently checked by its actual 190,080-state unweighted physical BFS. Hence:

    max_{i<j, 0≤x_f≤1} (h_i(x)+h_j(1−x)) = **7**.

This is **an exact two-projection continuous FACE-UNIFORM operator cost-sharing theorem** for this original source and these five concrete physical marker subsets. It does NOT solve the maximum of three-, four- or five-pattern simultaneous fractional shares; allowing non-face-uniform distinct prices for individual quarter vs half turns may change the optimum; adding new coupled corner–edge projections changes the problem. It also does NOT say the source whole-cube 17-turn impossibility is proved.

The no-go is independently supported at three proof grades:
1. [P0-R2 Go original face-owner integral 5^6 proof and Lean scaled-budget kernel](P0_R2_FULL_CORNER_88M_AND_CERTIFIED_OPERATOR_COST_DUALITY.md): integer all-pattern owner optimum 7.
2. [P0-R3 Go true physical 0/½/1 exact weighted 7,290-price experiment #38355226394](https://github.com/WhoSia/CUBE-REV/actions/runs/38355226394): maximum twice-cost 14 and hence exact HTM bound7; four maximizing halfgrid assignments. Histogram in integer half-turn units: 0:24,1:57,2:243,3:339,4:869,5:1018,6:1452,7:1184,8:1096,9:603,10:273,11:98,12:27,13:3,14:4 (sum7290). This earlier grid was evidence **only on the half-integer lattice**, not this full real theorem.
3. [P0-R3B shortest face-count original DAG #38355753083](https://github.com/WhoSia/CUBE-REV/actions/runs/38355753083) and [P0-R3C additional real physical 7-move E2 quota witness #38356018621](https://github.com/WhoSia/CUBE-REV/actions/runs/38356018621): together exhibit ten small exact word pairs, each with envelope≤7, proving the bound **for all continuous real prices**.

The independent [original physical Node 54-sticker verifier](../../scripts/cuberev-025/verify_p0_r3_continuous_face_price_original_54sticker.mjs) starts each actual physical original scramble from solved original sticker coordinates, then applies each of the 20 recorded projected legal words; it checks all four named real cubie identities and twists/flips return to their ACTUAL original positions, independently recalculates each six-face count and verifies all ten envelopes ≤7. Its [separate completed read-only original whole-54-sticker CI #38356444729](https://github.com/WhoSia/CUBE-REV/actions/runs/38356444729) is SUCCESS: all twenty legal projected source words checked for the required marked physical cubies, all ten six-face envelopes verified, and the original 18-turn full-cube upper word independently replayed. The prior E0/E2 Go witness was independently checked by source physical token-map tests, and source grade remains stronger with the Node independent check.

## 5. Research meaning: a finite proof like M*(5), with honest scope

The source 0.24 P1-R6 direct real full18HTM lower14 proof still stands and this P0-R3 does not strengthen it. But in the narrower, precisely specified restricted cost-partition question, the continuous optimization problem admits a tiny **20-projected-word source physical certificate**, not a huge 7,290-sample table or a speculative continuous extrapolation. This is conceptually closer to the compact witness/counterwitness logic required in M*(4)=34 and M*(5)=8.

More important, it reveals WHY optimization by separate geodesics can be mathematically incomplete: for dual cost proofs it may be useful to select a physically legal **nonshortest** projected path because its FACE HISTOGRAM couples better with another projected path across EVERY price vector. Any exact future globally useful source-complete joint-cubie heuristic must retain noncommutative order constraints beyond any six-face count vector.

**Next P0-R4 candidate:** abandon these five tiny separately additive projections as a route to new lower15; construct an executable exact **joint corner–edge, source-dependent constrained suffix frontier**, with complete safe source-prefix coverage and independently checked proof-shard exclusion for a genuinely harder radius (e.g., 14 or 15), and make memory-versus-computation and proof size measured rather than assumed. A successful P0-R4 must either yield a new original 14-or-15-path complete exclusion, an actual shorter than18 original solving word, or a rigorous source-specific wall for the proposed coupled model. No source rights or measured human behavior invented.

## 6. Governance and proof sources

Only WhoSia-authored/committed source on active research/current, no github-actions[bot] or github-action[bot] contributor and no Actions writeback. Read-only Actions may upload ephemeral receipt artifacts but never modify Git history. [0.25 Notion canonical](https://app.notion.com/p/3f7ef561cf9281ae8e94c46e9f916fdc), [short README](../../README.md), [P7 exact active file/blobs manifest](../../g7/p7/active-set-manifest.json). Prior [full old README GitHub Markdown archive](../../archive/readme/README_RESEARCH_CURRENT_FULL_PRE_P0R2_20261012.md) and [byte-identical Drive Markdown original](https://drive.google.com/file/d/1QQ18TJ2Ary6xl4tD1iRX3ErdVx5HDHwi/view) retain all old scientific statements, success/fail and source ontology warnings, rather than overfilling the active README.

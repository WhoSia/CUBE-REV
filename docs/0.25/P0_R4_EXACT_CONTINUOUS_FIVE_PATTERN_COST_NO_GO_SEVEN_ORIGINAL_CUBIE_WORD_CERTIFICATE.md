# CUBE-REV 0.25 P0-R4 — A Sharp Five-Pattern Continuous Operator-Cost No-Go on an Actual Rubik's Cube: Shared Seven-Turn Face Envelopes, Exact Source Quotient Duality & Independent Physical Witness Replays

**13 October 2026 · Native Go complete original-cubie face-budget search external CI SUCCESS #38370213103; strict independent Node 54-sticker witness CI pending new revision.** Exact source-specific theorem about the specified face-uniform five original projected 4-cubie PDB cost-sharing family. **This does not improve the original whole-cube unrestricted 14≤d18(s)≤18 nor settle existence of any 14–17 move full-cube solution.**

## 1. Actual original full 3×3 frozen source, not an abstract graph

Official WCA Seoul Summer 2026 Final A1 genuine original legal 20 HTM source:

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

Verified actual 18 HTM complete whole-cube solution:

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

The predecessor P1-R6 completed exact source-complete original whole-cube B6(goal) ∩ sB7 empty; **d18(s)≥14**. The 18-word independently replays solved on all original 54 stickers. The five distinct genuine marked-piece patterns partition every physical cubie, with original **edge** identities E0 [0,4,8,10], E1 [1,5,9,11], E2 [2,3,6,7], and **corner** identities C0 [0,2,4,6], C1 [1,3,5,7]. The union jointly determines all original CP,CO,EP,EO only when ALL follow THE SAME legal word—individual quotient words have no obligation to be a common whole-cube solution.

## 2. Theorem — a common face envelope forces upper bound on every continuous cost allocation

Let G be the original 3×3 fixed-center cube group with the 18 genuine HTM legal face actions A. For each of the five explicitly marked original-cubie projections π_i:G→Q_i let c_i(f)≥0 be a real face-uniform cost charged for action f, f' or f2. Suppose ∑_{i=1}^5 c_i(f)≤1 for EVERY physical face f in U,R,F,D,L,B. Let h_i^{c_i}(s) be the exact minimum projected source-to-projection-solved cost over any legal finite original face-turn word. This exists and is physically admissible (the finite projected group moves are real HTM).

For each i, pick an **actual legal original face-turn word w_i** solving the marked original physical cubies i. Let n_i(f) be the number of turns on face f in that word. The shortest weighted quotient path is no more costly than this particular original projected word:

\[
\begin{aligned}
\sum_{i=1}^5 h_i^{c_i}(s)
&\le\sum_{i=1}^5\sum_f c_i(f)n_i(f)\\
&\le\sum_f\Big(\max_i n_i(f)\Big)\sum_i c_i(f)\\
&\le\sum_f \max_i n_i(f).
\end{aligned}
\]

Consequently, a single finite five-word proof packet sharing a count envelope M_f=max_i n_i(f) with ∑M_f=7 supplies a **universal exact upper certificate ≤7 over the ENTIRE CONTINUUM** of real nonnegative face-uniform five-PDB cost shares. It does not require floating-point LP computation or a guess that separately shortest *unweighted* projected words always suffice.

## 3. Original physical five-word source proof certificate, each only a projected solve

The native source-exact Go algorithm, [P0-R4 7/8 face-cap finite verifier](../../scripts/cuberev-025/p0_r4_five_pattern_face_budget_go/main.go), genuinely constructs all five original 54-sticker-derived marked-cubie transition graphs and unweighted exact PDBs; explores all legal projected words length≤7 and length≤8 with valid normal-form pruning; uses exact marked physical state equality and certified PDB distance lower-bound lookahead; finds a seven-turn common face-count envelope. The finite scan of ALL **792** six-face cap vectors of total7 and **1,287** of total8 is complete and locally replayable; it is not needed to prove global optimality of the continuous 5-PDB objective once the seven-word envelope and exact E0 PDB are available.

**Original 18HTM physical source solves of the five independently specified marked-cubie groups** (face order U,R,F,D,L,B):

| Physical pattern | Legal original 18 HTM word solving all four specified cubies | Face count vector |
|---|---|---|
| E0 | \`B' U F R D2 R2 B'\` | (1,2,1,1,0,2) |
| E1 | \`B' R2 F2 U' R2 D' B'\` | (1,2,1,1,0,2) |
| E2 | \`R2 B R' U2 F' D2 B2\` | (1,2,1,1,0,2) |
| C0 | \`F D2 B' R U2 B2\` | (1,1,1,1,0,2) |
| C1 | \`R B' U2 F2 R2 D' B2\` | (1,2,1,1,0,2) |

Therefore every one of five physically valid projected words obeys the **same seven unit face budget**:

\[
M=(1,2,1,1,0,2),\qquad \sum_f M_f=7.
\]

They are different original legal face-turn words; none is claimed to solve the entire source cube, none is attributed to a human competitor. These literal words and pattern identity indexes are sealed in the [machine-readable original physical 5-word cap7 packet](../../data/cuberev-025/p0_r4_five_real_cubie_projected_words_cap7.json), independently checked by the separate [Node original 54-sticker direct marker-identity and orientation replay](../../scripts/cuberev-025/verify_p0_r4_five_real_face_budget_original_54sticker.mjs). The historically discovered weaker [eight-turn face cap](../../data/cuberev-025/p0_r4_five_real_cubie_projected_words_cap8.json) remains available; P0-R4 supersedes its weaker result without deleting it.

The executed [source-complete Go + inherited physical Node external SUCCESS #38370213103](https://github.com/WhoSia/CUBE-REV/actions/runs/38370213103) confirms 7 exists, prints the five literal projected words, checks all five original physical tables, source literal 18 word and 792 total7 cost-cap vectors. Its initial workflow did NOT yet replay the five NEW literal words under the separately programmed standalone 54-sticker Node engine; the added Node proof packet remains **CI PENDING until an exact completed newer workflow is inspected**.

## 4. Exact lower certificate and theorem of the restricted design family

The prior original E0 physical four-edge projection PDB has an exact HTM source distance **h_E0(s)=7** on its entire **190,080-state** quotient, with complete genuine 18 HTM BFS. Choose the valid continuous five-PDB cost share:

    c_E0(U)=c_E0(R)=...=c_E0(B)=1
    c_E1(f)=c_E2(f)=c_C0(f)=c_C1(f)=0 for all f.

The actual optimized sum then equals **7** (all other quotient prices zero), proving a sharp lower bound 7 on the supremum. Together with the seven-envelope five-word universal upper certificate:

\[
\boxed{\sup_{\substack{c_i(f)\ge0\\\sum_i c_i(f)\le1}}
\sum_{i=1}^5 h_i^{c_i}(s)=7.}
\]

This is **not** simply enumerating the integer 15,625 P0-R2 owners: it rules out improvements from **every fractional real face-uniform allocation across all five simultaneously**, a stronger valid negative theorem. It also extends P0-R3's exact real-valued **two-pattern** theorem to the FULL FIVE-PATTERN family. The missing obstruction must involve information such as coupled cubie endpoints/word order or distinct prices for quarter/inverse/halfturn rather than just assigning face-uniform unit cost among separated small PDBs.

## 5. Important limits and scientific direction

- This result is SOURCE-SPECIFIC (the fixed original WCA Final A1), pattern-family-specific (the frozen three 4-edge/two 4-corner groups), and FACE-UNIFORM (f,f',f2 charged identically). It is **not** a no-go for any admissible PDB, the full 88-million corner quotient, per-generator rather than per-face costs, true synchronizing multivariate automata or source-complete full cubie frontier certificates.
- This upper certificate is an UPPER bound on the best lower-bound HEURISTIC; it does not state actual whole-cube distance≤7. The established unrestricted original-cube **14≤d18(s)≤18** remains intact.
- The next actual cube search science has to retain **cross-pattern relative action order and physical cubie coupling** rather than trying other fractions of six face costs among the same five tiny separate quotients. A physically credible next experiment is a source-specific synchronized all-cubie prefix frontier with actual admissible full-corner/edge bounds, or a genuinely coupled corner-edge quotient, with an independent original sticker solver.
- No human psychological decisions, unreported NISS frame or copyrighted human raw 451 records were involved. Do not use CI bots as Git commit contributors.

**Local/CI code and status:** Go full 7/8 cap exact finite original physical source SUCCESS in Actions run #38370213103; Node standalone original physical packet and formal generic Lean-4 five-cost theorem are separate artifacts (Lean core previously PASS P0-R2 #38354902944, but that kernel alone does not verify these five physical words). GitHub updated external P0-R4 integrated full result will be promoted to PASS only after completed readback on the literal cap7 JSON and updated Node source SHA. All new commits must have WhoSia author and committer, with GitHub Actions read-only and P7 exact allowlisting.

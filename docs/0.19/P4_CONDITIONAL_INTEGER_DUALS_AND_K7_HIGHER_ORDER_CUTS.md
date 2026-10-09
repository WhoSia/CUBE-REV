# CUBE-REV 0.19 — P4 Exact Conditional Integer Duals and Seven-Word Pair Cuts

## Definitive boundaries
The optimal length-five experiment-dictionary cardinality M*(5) is an integer, with proven physical range 6 <= M*(5) <= 8. The exactly known ordinary fractional covering LP optimum is 16/3, not fractional physical rotations or analytic continuation. No independently checked seven-word SAT/UNSAT result has been established in this report.

## Exact symmetry-conditioned k=6 reduction
The verified 16-element signed-coordinate incidence automorphism group acts on all 1,192 original requirements, 8,807 maximal physically generated columns, and exact 544x2,887 quotient. There are 196 column orbits. For any nonempty solution of size <=6, one selected word can be transformed into one of these 196 orbit representatives (transforms are incidence relabelings, NOT necessarily legal physical moves).

Fix representative c. Let U(c) be requirements not already covered by c. Find integer row weights y_r>=0 supported only on U(c), with total W and maximal single-experiment covered weight C. If W > 5*C, at least six further physical experiments would be needed, contradicting a <=6 dictionary containing c. All 2,887 physical quotient columns were checked by exact integer sums, not by relying on numerical LP objective accuracy.

There are EXACTLY 191 certificates with W > 5*C among the 196 representatives. Therefore a six-word cover, if it exists, can be globally transformed to contain a first experiment with zero-based reduced column index one of: 0, 4, 112, 1199, 1202. This is a certified six-word branch reduction, NOT a proof that the remaining five branches have solutions and NOT a restriction on seven-word dictionaries.

The certificate archive is CUBE_REV_019_P4_Exact_Conditional_Dual_Court.zip with fully separate integer verifier P4_verify_six_branch_duals.py, physical.json, L5_constraint_matrix.npz, and the 196 integer certificate vectors. Certificate JSON SHA-256 b34eaa8509ffbdf8d6eaa3c89bcbdac253dda817837c0773bade7a8d6f204279; matrix SHA-256 86d3311a91201047361c370e663aa20f186e1f9494b564f0a1b4905dfbf56144. Local independent arithmetic verification PASS. The zip is locally staged; this GitHub memo does NOT mean the full certificate bytes are in git.

A short HiGHS integer feasibility probe on remaining five k6 cases returned numerical infeasible at representatives 112,1199 and timeout/UNKNOWN at 0,4,1202. These two infeasible outcomes DO NOT have independently verified UNSAT proofs.

## Exact weighted higher-order necessary conditions, valid for k<=7
The 70-row original physical integer dual assigns total weight 384 and any single realized length-five experiment covers weight at most 72. If t selected experiments in a dictionary of size <=k jointly cover dual mass U, then necessarily U >= 384-(k-t)*72. Proof: the remaining k-t experiments contribute at most (k-t)*72 newly covered weight.

For k=6,t=1, every selected word must have dual mass >=24; 1,010 of the 2,887 physically realized quotient columns fail this test, leaving 1,877 possible selected columns.
For k=7,t=2, any selected pair must cover at least 24 distinct weighted mass. Exact intersection and union examination of reduced physically sourced coverage masks produces 247,348 pairs whose union weight is <24; each pair induces a sound Boolean clause forbidding simultaneous selection. This includes a subset of 419 low-mass columns each scoring <12, of which at most one may be selected. The independent cut count was checked locally.
These clauses were implemented in scripts/cuberev-019/prove-L5-k7-k6.py in research/current, commit 069ddc6bc7e652800689cf9c17d72f1e12eba6b7. The SAT proof checker must verify the exact strengthened CNF, and the integer-dual validity of these extra clauses must be retained as part of theorem lineage. Their existence does not itself imply k7 UNSAT.

## Lower-bound methodological barrier
A complete rational primal and integer dual prove the ordinary LP optimum exactly 16/3 (see P3). Therefore merely finding more nonnegative row weights for the same LP cannot improve the global lower bound beyond ceil(16/3)=6. Conditional weighted cuts, symmetry-breaking, integrality, branch-and-bound, or certified SAT are needed to distinguish 6,7,8.

Exploratory GF(2) incidence row rank is 317/544 (rank 50/64 for four-state rows and rank 267/480 for five-state rows). This does NOT yield parity equations for set-cover decisions automatically, since the source constraints are OR/at-least-one, not exact cover.

## Next gates
1. Resolve all five residual k6 branches with independent external proof, or physically replay an actual six-word dictionary.
2. Run strengthened k7 SAT court; if SAT, replay physical seven-word cover and descend to k6; if UNSAT, check DRUP externally and check the added weighted cuts.
3. Verify actual GitHub Actions result instead of inferring success from a committed workflow.
4. Archive full reproducibility bundle durably with SHA-256.

Research page: https://app.notion.com/p/3f4ef561cf92813d9edfff4911db39d2
P3 theory: https://github.com/WhoSia/CUBE-REV/blob/research/current/docs/0.19/P3_GEOMETRIC_SYMMETRY_EXACT_LP_GAP_AND_K7_METHOD.md

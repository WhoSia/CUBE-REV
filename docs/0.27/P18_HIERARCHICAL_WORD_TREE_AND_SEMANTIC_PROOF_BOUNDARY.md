# CUBE-REV 0.27 — P18: Word-Tree Decomposition, the Short-Ancestor Lemma, and a Fail-Closed Hierarchical Audit

**20 October 2026 — mathematical/experimental research note, not a global exact-distance theorem.**

## 1. Why a receipt merger is not yet a proof checker

P17's fourth-sector stdout says that a program found no matches with the solved radius-seven fingerprint filter. A parser can independently show that all required fourth-sector names occur once and that each printed node count equals the canonical grammar mass. It **cannot** infer that the physical solver did visit every corresponding cube state or that its reported zero hits are truthful. Even if the printed totals are self-consistent, replacing the true membership test with the constant function `false` would produce the same set of plausible-looking receipts. This is a fundamental trust separation, not merely a need for more hashes or more anti-corruption tests.

We therefore distinguish (A) word-partition coverage, (B) full physical-state goal containment, and (C) source-side membership-check semantics. A complete mathematical lower bound requires all three. P18's receipt verifier claims only (A); dedicated P14 physical checkpoint/B7 inclusion checkers establish (B) under the shared physical move model; (C) is currently supported by implemented source executables and selected independent replay, not yet by a succinct independently checked whole-search trace.

## 2. Exact HTM radius split

Let \(s\) be the frozen 20-face-turn WCA source, \(e\) the solved physical cube, \(A\) the 18 HTM generators (three rotations per face), and \(B_r(x)\) the undirected Cayley-graph ball. If \(w\) is a path of length at most 17 from \(s\) to \(e\), it splits into a prefix of length at most 10 and a remaining suffix of at most seven moves. Conversely, two such paths concatenate. Thus

\[
 d(s,e)\le17\quad\Longleftrightarrow\quad B_{10}(s)\cap B_7(e)\ne\varnothing.
\]

Let \(H\) be the fixed fingerprint computed over 54 uniquely labeled physical stickers; injectivity of \(H\) is NOT assumed. Let \(F\) be any finite set of fingerprints. If an independent complete goal verification establishes

\[
 \forall y\in B_7(e):H(y)\in F,
\]

and a complete source-word traversal establishes

\[
 \forall w\in\mathcal W_{\le10}:H(s\cdot w)\notin F,
\]

then \(d(s,e)>17\). An independently verified length-18 solving word then establishes \(d(s,e)=18\). False-positive fingerprints cannot invalidate this implication; missing goal fingerprints can.

## 3. Exact finite word partition

A **canonical** word has no adjacent moves on the same face and never places a high-index face (D,L,B) immediately before its commuting opposite low-index face (U,R,F). Opposite faces commute, and same-face adjacent rotations compose/cancel at no greater HTM length; consequently every word has an endpoint-equivalent canonical word no longer than the original.

Write \(\mathcal U(p,r)\) for the collection of canonical words beginning with prefix \(p\), with at most \(r\) remaining moves. Denote by \(L(a)\) the set of legal successor moves following last action \(a\). Then **as sets of words, not necessarily as sets of physical cube states,**

\[
 \mathcal U(p,r) = \{p\}\,\dot\cup\!\bigdotcup_{a\in L(p_{\rm last})}\mathcal U(pa,r-1),
 \quad r\ge1.
\]

The disjointness follows from the unique next move in a word, regardless of whether different words happen to reach the same physical cube. If \(M(a,r)\) is the number of nodes in a descendant tree, then

\[
 M(a,0)=1,\qquad M(a,r)=1+\sum_{b\in L(a)}M(b,r-1).
\]

A fully independent Python implementation re-derived all masses. Its exact global census for depth \(\le10\) is **264,501,924,112 canonical words**; there are 18 legal one-move prefixes, 243 legal two-move prefixes, and 3,240 legal three-move prefixes, with

\[
 264,501,924,112
 =1+18+243+\sum_{p\in\mathcal W_3}M(p_{\rm last},7).
\]

Crucially, a parent proof cannot be obtained solely by merging its child proofs: the physical state at the parent word itself also must be excluded from \(F\). This issue recurs at every parent and at the empty word. An alternative is to invoke an independently proved distance bound that covers such short words, explicitly listing that bound as a second premise.

## 4. The short-ancestor deduction from the already replayed P13 certificate

P13's independent physical verifier was actually recompiled and rerun during P18. It checked 888,079 solved-goal radius-five self/neighbor inclusion obligations and 621,649 complete physical source-radius-five states, finding no source/goal intersection. By the radius split, this proves \(d(s,e)\ge11\) under the fixed physical model.

If a canonical source word \(w\) has length \(|w|\le3\) and its endpoint belongs to \(B_7(e)\), then \(d(s,e)\le |w|+7\le10\), contradicting \(d(s,e)\ge11\). Therefore **all source prefixes of length 0, 1, 2 and 3 are ruled out by this genuinely independent smaller-radius proof**. This is an explicit *composition* of two certificates rather than a disguised single-cutoff theorem. In particular, P18 no longer needs to pretend that a missing parent membership query was executed when its parent node was already ruled out by P13.

## 5. Strong-oracle diameter barrier (a second mathematical result)

In a source radius-ten court with solved radius-seven, a lower bound \(h\) can prune the entire remaining subtree of a node at source depth \(k\) only if

\[
 h(x)>17-k.
\]

Hence a quotient with maximum distance \(D\) has **zero internal-subtree pruning power at every source depth \(k\le 17-D\)**. For corner permutations \(D=7\), no pruning can fire at all at depths \(k\le10\). For the previously investigated full-corner \(C_8\) quotient, \(D=8\): no internal node at depth \(k\le9\) can be pruned, while some depth-ten leaves may be discarded without a B7 lookup. To prune a depth-nine internal node requires \(h\ge9\), and to prune at depth eight requires \(h\ge10\). This proves a candidate-oracle screening criterion **before** spending resources on a new projection table.

The theorem assumes an *admissible* lower bound. A large but inadmissible heuristic may prune more, but cannot appear in an independently sound lower-bound proof.

## 6. Actual P18 execution and unpromoted upper-level HOLD

The original physical 54-sticker C++ state engine rebuilt the exact \(B_6(e)\) checkpoint (8,240,087 states). A separately compiled verifier checked all six BFS layers and 11,189,682 predecessor/edge obligations. Its nine checkpoint batches then emitted 156,561,653 target self-or-neighbor fingerprints; 64 disk partitions merged to **109,043,123 sorted unique fingerprints**. A distinct checker completed exactly **156,561,653** goal-inclusion membership tests in two disjoint ranges. These are real executed checks, not merely reported expected cardinalities.

The third-action prefix `1,4,0` had an interrupted attempted monolithic run: it printed only four fourth children and was correctly rejected as incomplete. We re-executed **all fifteen legal fourth children** in individual fourth-sector processes. All completed; the independent structural verifier accepted the exact union, totaling **90,800,620 canonical source-word nodes** and **83,998,296 depth-ten leaves**, with **zero reported B7 hits**. A separate original-54-physical **breadth-first word-tree replay** (not using the prior depth-first traversal) then independently visited the 6,802,324 nodes of the fourth sector `1,4,0,3`, all 6,292,728 terminal depth-ten words, and observed zero hits. This is a *bounded semantic re-execution for one sector*, not complete independent replay of the other fourteen sectors. The BFS shares the original 54-site move table and the same goal filter and therefore is not independent of the physical representation model.

The newly accepted third prefix does **not** add more nodes under the previously closed P17 third prefixes `1,4,7` and `1,4,8`. The union of these **three disjoint prefix-word subtrees** now covers exactly **272,401,860 word nodes** and **251,994,888 depth-ten leaf words**, with no reported goal hits. In their common parent `1,4` there must be **fifteen** legal third actions. Only `{0,7,8}` are complete; the remaining `{1,2,6,9,10,11,12,13,14,15,16,17}` are **twelve still-open children**. The parent subtree is 1,212,049,276 canonical word nodes including its length-two root. The new checker labels the parent **HOLD_INCOMPLETE_SECOND** and does not call it a global lower-bound proof.

For the full source radius-ten court, all **3,240** canonical length-three prefix subtrees (together with the short-ancestor obligation) must be accounted for. The currently proven structured sector receipts are very far from exhausting this collection.

## 7. An independent checker cannot authenticate a fabricated zero-hit declaration

The new hierarchical checker is written independently of the C++ enumerator. It validates expected child IDs, prefix grammar, exact descendant and leaf masses, lack of duplicate jobs, producer-reported hit counts, parent conservation, and honest incomplete-parent status. It rejected **ten deliberate structurally corrupted receipt sets** in local testing. It also deliberately aborts when Python runs with optimization (`python -O`), which would otherwise disable its assertions. This addresses an actual reliability issue in assertion-based verifier scripts.

Even a structurally perfect receipt could falsely say `B7_hits=0`. No rearrangement of its count fields can establish the truth of that claim. A **semantic certificate** must instead carry independently checked physical-state transitions and goal-membership evidence (e.g. a portable trace, an independently reproduced search, or a separately checked inductive invariant). This is the main P18 research limitation and a concrete obligation for P19. File hashes can identify the byte streams involved but cannot prove that the program producing them enumerated all physical states correctly.

## 8. Next decisive experiment

Promote only parents whose child sets are complete, whose parent-root obligation is proved (or explicitly discharged by the P13 \(d\ge11\) lemma), and whose constituent physical zero-hit predicates are *semantically* certified. Avoid further manuscript version increments until either a whole second-action parent is actually closed or a materially stronger independent semantic proof carrier has been constructed. The central paper claim should remain the conditional **proof architecture and bounded demonstrated audits**, not a falsely completed global \(d(s,e)=18\) theorem.

**Evidence status:** P18 actual source, goal and P13 logs are in the local reproducibility package. No new branch was created, and original huge B6/B7 binaries remain local scratch data (not falsely claimed to be in Drive). The P18 structural checker and mathematical proof report are separately portable. Research OS WRITING 3.0: preserve the failure of the monolithic job and the semantic-proof gap rather than burying either beneath a clean-looking receipt ledger.

## P18B continuation — all 15 fourth sectors reverified by independent BFS (20 October 2026)

An independent explicit-queue **breadth-first** physical source-word search was extended to all fifteen fourth actions of the new original fixed-WCA third prefix `1,4,0`. The first attempt had a **real implementation defect**: the queue was initialized with `last=3` for every fourth action, so different-face branches could be traversed under the wrong canonical grammar while sometimes producing identical aggregate counts. This was discovered when the fourth-action `9` run **failed closed** with a contradictory expected count. The previous affected BFS evidence was withdrawn; the queue initialization was corrected to use the actual `fourth` argument and **all fifteen jobs rerun from scratch**.

After repair, both methods produced 15/15 complete, exactly **90,800,620** canonical source-word nodes, **83,998,296** depth-ten leaf words, and **zero** B7 fingerprint matches. They are truly distinct traversal implementations (recursive DFS versus iterative breadth-first explicit queue). A third Python checker compared the fifteen per-action outputs, demanded the full legal child set, independently checked the exact per-sector word/leaf counts, and rejected **4/4** corrupted or incomplete BFS job sets. Verified marker: `P18_BFS_DFS_COMPLETE_CROSS_METHOD_SEMANTIC_REPLAY_PASS sectors=15 word_nodes=90800620 leaves=83998296 hits=0 mutants_rejected=4`.

**Trust boundary**: both C++ traversals reuse the original P11 physical 54-sticker turn map and the same separately certified B7 goal filter/fingerprint algorithm. This independently replays the **entire new one three-prefix word court** using distinct traversal semantics; it does not independently derive all Rubik group geometry and does not verify the other twelve still-open `1,4` third children. Nor do structurally valid zero-hit receipts without such physical replay constitute checkable mathematical proof. P13 independently replayed `d>=11` still discharges short ancestors through depth3. The combined closed third-prefix subtree mass remains **272,401,860**, and the global exact-18 independently checkable theorem remains **OPEN**. The failed BFS counterexample is a scientifically material observation: matching word counts cannot establish matching word identities.

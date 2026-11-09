# CUBE-REV 0.28 R14-P8.7 — A restricted exact twenty-frame lower bound

**Date: 2026-11-09.** This theorem is about a **specified first-twelve-edge-observation family**, not all adaptive paired observation policies.

Fix a first twelve-edge observation schedule that reads the first indexed facelet from each of the twelve spatial edge cubie positions. One achievable color response string is `RRRFFFLLLBBB`. With even total edge flip there are exactly 2,592 oriented, permutation-compatible edge completions. Splitting by common edge/corner permutation parity yields two sets of **1,296** states.

For either stratum \(X_p\), define \(W_p(B,k)\) as the assertion that a deterministic policy can identify all remaining edge configurations from posterior \(B\) in at most \(k\) additional individual edge facelet queries. Every informative future edge query is a previously unread mate sticker; other first stickers are already known. The complete AND–OR recurrence is

\[
W_p(B,k)=[|B|\le1]\ \lor\ \Big[k>0\ \land\ \exists q\;\forall c\;(B_{q,c}\ne\varnothing\Rightarrow W_p(B_{q,c},k-1))\Big].
\]

An independent literal-`frozenset` implementation enumerates all 1,296 states in each stratum and proves

\[
W_0(X_0,7)=W_1(X_1,7)=\mathrm{false},\qquad
W_0(X_0,8)=W_1(X_1,8)=\mathrm{true}.
\]

For every one of twelve root mate queries and both parities, the JSON receipt contains a real response color leaving a residual that cannot be distinguished by six further mate queries. The full impossibility is universal over all adaptive future edge query choices inside the prefix family; it is not just a failure of a greedy heuristic.

**Consequences:** Even with the true parity supplied for free immediately after frame twelve, the specified prefix cannot guarantee edge reconstruction by frame nineteen. Thus the constructed twenty-frame policy from P8.6 is **sharp for this initial first-facelet schedule family**. It remains logically possible that an unrestricted different schedule solves the full cube in nineteen or eighteen frames. The global currently certified interval is therefore **18–20**, not \(h=20\).

Reproduce with `python verify_r14_p87_12_first_family_lower20.py`; the script has no P8.6 or P5.1 dependencies. The input first-color string is genuinely realizable in the original physical cube: the separate P8.6 hard physical runner constructs and validates all 2,592 compatible full 48-sticker states, each with matching corner parity.

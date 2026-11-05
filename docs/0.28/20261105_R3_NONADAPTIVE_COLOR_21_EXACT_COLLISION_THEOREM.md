# CUBE-REV 0.28 R3 — Exact nonadaptive 21-frame lower bound by edge-color collisions

**Date:** 2026-11-05. **Authority:** finite constructive theorem + independent P48 geometry witness census (10,626 omitted quadruples); remote CI not yet independently checked. **Scope:** exact six-color, one edge sticker and one corner sticker per frame, known turns, fixed precommitted (nonadaptive) observation schedule. This does NOT prove a lower bound of 21 for adaptive policies.

## Theorem
Under the R2 fixed-centre legal Rubik group and facelet-color contract, the minimum number of **predetermined** observation frames for error-free identification of every legal state is exactly **21**. The earlier 21-frame legality-assisted decoder gives the upper bound. The lower bound holds even if all eight corners are additionally revealed perfectly.

## Reduction from turns to initially located facelets
For a predetermined sequence of known 18-HTM words, each fixed edge probe reads the color of a specified *initial spatial edge-facelet slot*. The inverse of each known word identifies that slot, independently of the unknown cube state. A schedule of at most 20 frames therefore exposes at most 20 distinct slots from the 24 original spatial edge facelet locations. It suffices to give a collision for every choice of exactly four omitted edge slots, since any shorter or repeated schedule can be extended to a size-20 slot selection.

There are C(24,4)=10,626 missing-slot selections. They fall into three exhaustive types, classified by counts of omitted slots per spatial edge position:
* **2+2** (66 masks): two edge positions totally unread. Keep every piece label and all corners fixed, but flip these two edges together. Edge-flip parity stays even and all observed edge colors stay fixed.
* **2+1+1** (2,640 masks): one unread whole edge position A and two positions B,C with one unread facelet each. Select three distinct original U-colored edges, arrange them among A,B,C, and perform an even 3-cycle of these labels while retaining the U sticker at the read B,C facelets. Read colors stay U. For each of the two states choose the unobserved A flip to make the global edge-flip sum even. The edge permutation parity is unchanged, so the same legal corner configuration can be used.
* **1+1+1+1** (7,920 masks): four spatial edges each have one unread facelet. Choose three such positions, install three distinct original U-colored edges with their U stickers on their read faces, and 3-cycle the three labels. Each selected read face continues to show U. The edge-flip coordinate of any U-containing edge in a fixed destination is determined by which destination facelet carries U, not by which particular U-containing edge was installed. Thus the 3-cycle leaves the edge-flip sum unchanged. Choose an unchanged fourth edge's flip initially to make this sum even; use the same unchanged corners of matching permutation parity in both states.

In all cases the two configurations are distinct valid cubie states: bijective edge and corner labels, even total edge flip, zero corner twist, and matching edge/corner permutation parity. By the standard legal Rubik group characterization they are reachable by legal turns. They have **identical full corner states** and **identical edge colors on every observed edge slot**.

Consequently every 20-frame fixed schedule has a collision, even after giving the decoder an ideal complete corner oracle. A universal fixed schedule needs at least 21 frames. The separately certified R2 P48 21-frame schedule reaches 21, so the optimum for this **nonadaptive** model equals 21.

## Independent executable audit
The accompanying `scripts/cuberev-observation/audit_20_frame_edge_collisions.py` constructs P48 states from independent 3D facelet geometry, then checks for all 10,626 masks: both states are full 48-facelet permutations; corresponding cubie orientations and permutations are physically legal; they differ; all non-omitted edge slots have identical six-color readings; and all corner sticker assignments are exactly identical.

Local executed result:

```
20_FRAME_FIXED_EDGE_COLLISION_ALL_OMISSIONS_PASS 10626/10626
EDGE_OMISSION_PATTERN 1+1+1+1 7920
EDGE_OMISSION_PATTERN 2+1+1 2640
EDGE_OMISSION_PATTERN 2+2 66
```

This is a complete enumeration of **measurement omission patterns**, not of 4.33e19 cube states. The constructive argument covers every state choice required by the proof; the verifier tests the actual P48 state representatives and color equalities. Local execution does not equal remote CI PASS.

## Strict scientific boundary
An adaptive observation policy may choose the next relative turn after reading previous colors. A collision for every **fixed 20-slot set** does not automatically imply a common 20-observation history for every adaptive policy. Therefore only `h_color^nonadaptive(G)=21` is concluded. The adaptive optimum remains `13 <= h_color^adaptive(G) <= 21`. The best known executable fixed 21-frame action cost remains <=119 HTM, **not proven optimal**. Noise, hardware and human cognition were not measured.

## Next R3 research
Formulate a decision-tree adversary for adaptive observation, determining whether a common-color collision survives state-dependent turns; separately examine whether edge-only ambiguity can be propagated along each adaptive branch. Any claim of exact adaptive 21 requires a policy-wise proof or a complete explicit certified tree, not only this fixed-mask census.

**Doctrine:** human WhoSia commits only; maintain P7 manifest and read-only CI; GitHub for small executable source, Notion for current semantics, Drive for irreplaceable T2 original bytes.
## Additional stronger theorem: adaptive observation requires at least 16 frames

Give the decoder the **complete true corner state for free** before any sensing. Fix any such corner state, including its known permutation parity. By the Rubik legality characterization, the remaining edge state can be any of

```
12! * 2^11 / 2 = 12! * 2^10 = 490,497,638,400
```

different edge permutations/orientations: one parity restriction on the edge permutation (to match the known corners) and one parity restriction on its 12 flip bits.

Even under a fully adaptive legal-turn policy, each physical frame reveals **exactly one six-valued edge color**. Given the entire known corner configuration and all earlier edge readings, the observed corner colors and chosen turns are deterministic functions of the previous history and cannot transmit an additional independent edge symbol. A depth-`t` adaptive decision tree therefore has at most `6^t` distinct edge observation histories for these states.

```
6^15 = 470,184,984,576
12! * 2^10 = 490,497,638,400
6^15 < 12! * 2^10
```

Thus **at least 16 joint edge+corner probe frames are required even with arbitrary feedback-adaptive known 18-HTM actions**. This improves the full-group color-channel adaptive bound to

```
16 <= h_color^adaptive(full G) <= 21.
```

It is not asserted that 16 or 21 is the adaptive optimum. The fixed-schedule optimum remains exactly 21. This adversarial/oracle bound does not depend on the fixed-mask collision census and is valid for any deterministic exact-output adaptive policy; a zero-error randomized policy also cannot evade it for every random seed that must be universally correct.

**Scientific authority split:** This is a direct mathematical counting argument, not an empirical hardware or human-cognition observation. The older R2 lower bound of 13 remains true but is superseded by 16 for this channel and legality model.

## R7 upgrade (2026-11-05): adaptive full-cube color lower bound 17

**Supersedes the 16-frame lower bound above, without changing the exact fixed 21-frame theorem.** For the identical full legal Rubik group, one exact six-color *edge* facelet and one exact six-color *corner* facelet per frame, actions depending on previous colors, the new bound is

```
17 <= h_color^adaptive(full G) <= 21.
```

**Theorem (decision-tree leaf-capacity obstruction).** Give the observer the ENTIRE correct initial corner state for free. For each such corner state there are exactly `N=12! * 2^10 = 490497638400` legal compatible edge states (edge permutation parity fixed and edge flip parity even). Under any known legal turn schedule and any feedback, each edge sensor read can be reinterpreted as a query of a specific facelet slot in the *unknown initial spatial configuration*. The choice of the slot may depend on all preceding colors, but for each realized history it is known. A full corner oracle makes every corner sensor outcome determined by the oracle and actions, hence corners convey no extra edge information.

Partition the 24 edge facelet slots into 12 two-facelet positions. At any point the policy can query: (i) a previously read slot (one determined result); (ii) a first facelet at an untouched edge position (at most six candidate face colors, with a **global maximum of four FIRST-read occurrences per color** because only four distinct edge cubies contain that color); or (iii) the second facelet at an already touched position (at most four results, because an edge sticker's companion cannot be equal or opposite in the physical six-color cube).

To upper bound the number of *distinct* adaptive histories, relax the policy enormously: let it access ANY initial spatial facelet slot without paying legal turns, permit all four companion colors even when globally inconsistent, and ignore all identity/orientation/parity restrictions except the already imposed corner-fixed state count. An upper bound under this more powerful oracle is also an upper bound for the actual 18-HTM policy.

Let `F(t,m,p,c)` be the **maximum number of future readout histories** in `t` more reads from a prefix that has visited `m` different edge positions, read both stickers of `p` positions, and whose FIRST-read six-color multiplicities are `c=(c_1,...,c_6)` (sorted for memoization), with `sum(c)=m`, `0<=c_i<=4`. Write `e_i` for an increment of count i. The valid universal **upper-bound recurrence** is

```
F(0,m,p,c)=1
F(t,m,p,c) = max(
    F(t-1,m,p,c),                           # repeat known facelet
    sum_{i:c_i<4} F(t-1,m+1,p,sort(c+e_i)), # new edge position, m<12
    4*F(t-1,m,p+1,c)                        # paired second facelet, p<m
)
```

with infeasible options omitted. This is an induction over **all adaptive policies**, not a count for one precommitted sensor schedule. The i-sum counts color labels separately even when their multiplicities match; sorting counts does not merge observation outcomes. Because it ignores many real edge-label consistency restrictions, the computed F is deliberately an OVERcount of what real cube histories permit.

The Python standard-library exact-integer DP in [R7 capacity certificate](../../scripts/cuberev-observation/audit_20_frame_edge_collisions.py) evaluates

```
F(15,0,0,(0,)*6) =   109230105600
F(16,0,0,(0,)*6) =   436920422400
F(17,0,0,(0,)*6) =  1747681689600
```

An independent arithmetic formula checks the 16-step result. For 12 fresh edge-position reads, the number of distinct length-12 color words with at most four of each color is

```
C12 = sum_{c_1+...+c_6=12, 0<=c_i<=4} 12! / (c_1! ... c_6!)
    = 1706720400.
F(16,0,0,(0,)*6) = 4**4 * C12 = 436920422400.
```

The equality in the second line is a certified value of the relaxed adaptive recurrence, NOT a claim that every abstract history is a legal Rubik configuration. Finally,

```
436920422400 < 490497638400 < 1747681689600,
```

so no depth-16 adaptive decision tree can have a distinct observation transcript for every corner-compatible legal edge state. Consequently **17 frames are necessary**, even granting the full corner oracle and unrealistically free access to edge facelet slots. R2 supplies the known 21-frame upper construction. The gap 17–21 remains OPEN.

**Limits and novelty:** This is a Rubik six-color/constrained-cubie mathematical improvement, not a new general theory of decision-tree counting, not a 17-frame policy, not a human-memory or motor-cost measurement, and not yet proof of scholarly priority versus prior automata/sensing literature. The structural mechanism is finite-color capacity + physical two-facelet edge pairing; the policy adaptivity is genuinely covered by the Bellman induction. Independent CI execution and full paper-level peer review remain separate gates.

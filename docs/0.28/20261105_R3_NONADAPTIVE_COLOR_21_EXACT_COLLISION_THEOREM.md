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

# R14-P8.40 — A 19-frame adaptive color policy

For the fixed-center legal 3×3 cube, with one edge sticker color and one corner sticker color per frame and known legal turns free, the worst-case adaptive budget satisfies **18 ≤ h_adaptive ≤ 19**. The fixed budget remains 21. The 19-frame policy below attains the exact minimum within the family that reads a new edge at each of the first eleven frames.

## Policy

| Frames | Edge reading | Corner reading |
| --- | --- | --- |
| 1–11 | Side zero on eleven distinct edge positions | First eleven entries of the seven-corner scan |
| 12–14 | Adaptive choice among the eleven mates and the two unread stickers | Finish the seven-corner scan |
| 15–19 | Adaptive choice using the now-known edge permutation sign | Repeat a known corner sticker |

The seven-corner scan reads two ordered stickers per corner. The 24 possible ordered pairs distinguish source corner and orientation. The remaining corner follows from the missing label and the zero twist sum. Its reconstructed sector supplies the corner permutation sign, which equals the edge sign. Frame 14's edge query is chosen before this sign is available.

## Exhaustiveness and transport

An even-flip edge state yields one of the 867 P8.6 twelve-color count vectors when side zero is read everywhere. Deleting any one available color from each vector gives precisely the possible eleven-read vectors. For sufficiency, permute the source labels with their orientations to put the deleted color at the unread position. Either resulting edge sign admits a corner completion. This gives 1,362 count vectors.

The 48 permutations of the six colors preserving the three opposite pairs act on the twelve edge labels. A color permutation induces a source-label permutation and may reverse some edge words. The P8.6 generator checks that the number of reversals is even for every map, preserving total flip parity. A position permutation then sorts the observed eleven colors and fixes the unread position. The two transformations are bijections, transport each available query and its response, and shift permutation sign by the XOR of the source and position permutation signs. Both signs remain in the belief until frame 14. This transports every concrete eleven-color history to one of 52 representative games, including histories with repeated colors.

For each representative, enumerate the possible full edge assignments by trying every first color of the unread edge and keeping all even-flip completions. At each step the solver chooses a query whose every nonempty color branch fits the remaining budget. After frame 14's response it branches additionally by permutation sign. Repeating a known reading allows the corner scan to advance even when an edge query is unnecessary. The search tests an eight-frame continuation for all 52 representatives. Full replay reconstructs all 144,736 representative edge assignments.

Each requested sticker pair lies in the 576-pair orbit under legal face turns. The executable verifies every inverse route. Undoing the previous route and applying the next route realizes the policy with two stationary probes and no extra observations. A separate 48-sticker geometry model tests 2,001 legal inputs, executes the probe transforms, and compares all 48 recovered colors to the input. The universal upper bound uses the exhaustive edge games, the transport proof, and the corner decoder. The 2,001-state replay checks the physical implementation.

## An 18-frame obstruction for this prefix family

Take the first eleven colors to be `RFFDDLLLBBB` in the edge orientation convention used by the executable. An independent assignment enumeration gives 1,656 compatible edge states for each permutation sign. Fix one compatible corner configuration for each sign and reveal it to the observer at frame 11. Corner readings then supply no further information. A literal set-partition search tests each of the 13 possible informative first continuation queries and finds, for both signs, a response whose remaining belief cannot be distinguished with six more edge queries. Repeating an already observed sticker adds no information in this relaxed game. Thus seven continuation frames are insufficient for this history, even with the full corners supplied. The bound applies to the specified first eleven edge reads. The unrestricted question is whether some other initial policy achieves 18 frames.

## Extension to adaptive first-eleven new-edge scans

Fix one full corner configuration and reveal it for free. Against any deterministic policy that reads a previously unread edge in each of its first eleven frames, give the colors of `RFFDDLLLBBB` in time order. Map the eleven observed physical edge positions to the eleven canonical positions in time order. At each such position, exchange the local sticker slots if needed to send the observed slot to side zero. At the unread position choose the slot exchange so that the total number of exchanges is even. The resulting map on complete edge states preserves total flip parity, and the spatial permutation shifts the edge permutation sign by a fixed XOR. Thus the resulting belief is exactly the canonical witness fiber for one sign. Every state in its inverse image realizes the prescribed adaptive path since all preceding readings and the entire corner configuration agree. Both sign fibers have the independent seven-query obstruction, which transports back to the physical query slots. This rules out 18 frames for every policy in this broader family, including adaptive choices of edge position and side. Any successful 18-frame policy must have some history that reads a previously touched edge in its first eleven frames.

## Reproduction

Run `python scripts/cuberev-observation/audit_r14_p840_constructive_19_frame.py` and compare its JSON output with the committed receipt. The source reuses the P8.6 edge conventions and the P5.1 sticker geometry. Its lower-bound search uses literal sets and separate enumeration to check the specified counterexample.

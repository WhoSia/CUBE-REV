# CUBE-REV 0.28 R12 — An All-Feedback Adversary for Eight-Complete-Edge Prefixes

**Date:** 2026-11-05. **Scope:** class-wide impossibility theorem for an identifiable family of edge-color sampling policies, not a universal 20-frame impossibility for the Rubik group. **Proof ingredients:** legal P48 edge/corner parity, a deferred-decision adversary, and the independent R8 exact 96-state worst-case adaptive decision-tree certificate for U-star four-edge residuals. Remote R12 CI was queued at this stage: independently verify its conclusion before reporting remote PASS.

## Scientific question

Can CUBE-REV's original hard full-cube adaptive color identification problem be solved in 20 frames by learning the identity and flip of eight whole edge cubies in the first 16 joint frames, then using four adaptive final edge observations? R8 found that 54 of 495 leftover four-edge color-type graphs require five further queries, but that alone did not establish that the first eight edge positions cannot be selected adaptively to avoid those graphs.

**R12 answers this policy-class question: even adaptive selection of which eight edge positions to fully read cannot guarantee avoiding the bad residual graph.**

## Precise theorem

Consider ANY deterministic, physically legal adaptive cube color-observation policy such that **its first 16 edge-facelet observations comprise both individual facelets of exactly eight distinct initial spatial edge positions**, possibly with those eight positions selected from prior color results and their two facelets read in arbitrary order. Permit the policy to use its simultaneous corner color readings; allow any known legal 18-HTM actions and full memory of the observation transcript.

Then such a policy cannot guarantee complete identification of every legal Rubik state after four more frames, EVEN IF the true complete corner state is given for free. Therefore every zero-error policy in this eight-complete-edge-prefix class has worst-case observation horizon at least **21**.

This is a theorem about a PROPER subset of all adaptive policies. It does not rule out an interleaved policy whose first 16 edge queries leave at least one partially read edge position or have a different distribution of distinct spatial edge slots. The full-group adaptive bound remains **18 ≤ h ≤ 21**.

## Deferred physical adversary and proof

Fix the complete initial corner state to solved; all corner readout outcomes at any known turn are then independent of the unknown edge arrangement.

Choose the four edge cubie types incident to the U color:
  L = {UR, UF, UL, UB}.
They form the four-edge star K_(1,4) in the physical color-incidence graph. Their complement consists of the eight original edge labels T.

As the alleged policy begins querying spatial edge-facelet slots, **defer choosing an initial physical cube state**. At the first observation of a previously untouched edge position, assign one previously unused original edge cubie type from T, in a predetermined order, and choose a legal orientation for that edge. Reply with its correct intrinsic sticker color. Subsequent readings at that position must match the already assigned physical cubie. The next spatial position to query may depend on all prior edge and corner colors, but the adversary can always assign the next unused T label: before all eight new edge positions have been touched, the remaining T labels are distinct and available.

Because the class requires sixteen reads to cover both facelets of exactly eight spatial edge positions, at frame16 the eight revealed positions are occupied by the eight T pieces. The **remaining four original cubie labels are exactly L**, regardless of which eight positions the adaptive policy selected. All first sixteen readouts, the selected legal actions, and all corner outputs are identical across the legal completions constructed below.

The group-level physical constraints still allow **96** legal completions of the four unobserved edge positions, after fixing the eight source-to-destination assignments/orientations, the complete corners and global parity. Indeed, the parity of the residual permutation is fixed by the known full edge/corner parity equation; the sum of four residual flips is fixed by the even edge-flip condition, giving exactly (4!/2)×(2^3)=96 configurations. Each completion is a genuine legal fixed-center Rubik state with identical sixteen-observation prefix transcript. All 96 remain possible to the observer.

The exact R8/R9 physical color minimax certificate proves that the star residual L needs **five** further single-edge-facelet readings, regardless of which four residual spatial positions remain and regardless of the prescribed residual permutation/flip parity bits. This lower bound is already granted arbitrary free access to residual facelet slots, so the actual fixed sensor plus legal physical turn routing cannot improve on it. Four remaining frames cannot distinguish the 96 full legal states. Contradiction.

Thus any such eight-complete-edge-prefix policy needs at least 16+5=21 frames in its worst case.

## Executable controls

[Adversarial prefix verifier](../../scripts/cuberev-observation/audit_r12_eight_full_prefix_adversary.py) uses actual P48-generated original edge color pairs and legal 48-sticker geometry. It checks all four residual permutation/flip parity classes have R8 optimal depth five for the U-star four-type set. It generates 32 example color-dependent prefix selection histories and **3,072** legal physical full-state completions, verifies corner positions remain solved, edge permutation parity remains even and edge-flip sum remains even, and confirms their eight fully observed edge pieces have identical exact colors. These finite tests support the constructive adversary; the universal policy quantifier follows from the deferred-assignment argument above, NOT from testing 32 policies.

An exact adaptive partial-edge-prefix policy is still an outstanding alternative, not a contradiction. Any next 20-frame construction must escape this policy class; in particular its first sixteen edge queries cannot consist solely of complete pairs at eight different spatial edge positions.

## Relationship to R11 and the original research aim

R11 independently proved that **14 corner color observations** at seven spatial corner positions suffice to reconstruct the whole corner state. This makes early corner uncertainty removable by frame14, but does not magically remove the four-edge star obstruction when edge queries in frames1–16 simply read eight whole edge cubies. The R11 full-cube 21-frame nonadaptive decoder using only 14 distinct corner colors and the separate R11 full-cube 21-frame feedback policy with no corner oracle remain valid candidate upper constructions. Neither is a 20-frame proof.

The research is not shifting into an easier small-cube paper: the finite 96-state minimax witness is used as a **sharp adversarial obstruction for a general family of full-group adaptive policies**. This is the right direction of transfer, from a precisely validated local physical structure to a universal statement about a meaningful full-group policy class.

No claim about human working memory or perceptual cost follows from the strict mathematical sensor model. Behavioral mechanisms still require independent observations and suitable ethical controls.

## Next theorem gate R13

Attack policies with **partially read edge positions in the first 16 frames**. Establish a nontrivial universal obstacle for those policies or construct an explicit fully legal 20-frame joint edge/corner decision tree. Maintain the no-corner-oracle condition; the true corner state can be used as input only after sufficient corner color observations have reconstructed it. Any proof must hold over all 43,252,003,274,489,856,000 full legal cube states and not just radius-two samples.

**Custody:** P48 code and reproducible numerical receipts live in the public GitHub repo and immutable CI logs, semantic verdict in Notion, private original human data in Drive. WhoSia human commits only; read-only Actions. R12 CI receipt pending at time of creation.

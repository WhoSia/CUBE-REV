# CUBE-REV 0.21 — P2: Ecologically Grounded Cube Inspection, Shared-Cubie Exclusion and Bounded Human Action

**Formal 0.21 title retained:** Active Reconstruction of the Rubik's Cube: Observation-Driven Action Selection, Belief-State Dynamics, Physical Information Access & the Limits of Adaptive Solving.

**Question:** When a person inspects a partially visible real object, what makes them choose another viewpoint or physical action, retain a previous picture, or spend effort anticipating what will become visible? We operationalize this using **genuine 54-sticker 3×3 Rubik cubes** under controlled camera access, not by interpreting an intrinsic 1-bit edge-orientation sensor as normal human vision.

**Version continuity:** Original 0.15 adaptive single-edge search, 0.18 `M*(4)=34`, 0.19 `M*(5)=8` and nine-turn single fixed-word full twelve-edge identification, 0.20 transported-cut geometry, 0.21 P0/P1 exact seven-turn adaptive baseline are all retained with their original ontological and certification boundaries.

## 1. The actual everyday analogue: inspecting a partially hidden object

A person receives a camera view of **exactly the nine ordinary colours on ONE cube face**, controls an unseen physical cube through the same 18 legal HTM moves, and needs to determine **which of four already disclosed possible physical cubes** is currently behind the camera. The hidden cube is really one of the displayed reference states. This is analogous to remote object inspection, troubleshooting from a restricted camera, or diagnosing an object with inaccessible sides, without claiming those tasks empirically have the same human cognitive mechanisms.

No privileged cubie identity, hidden orientation, complete internal cube state or full six-face view leaks into the observation. The camera sees standard six-colour stickers, not arbitrary oracle bits. A live 3D front-face simulation can be the feasibility pilot; a physically turned cube under a fixed one-face view is the ecological replication. Free rotation or exposing other faces is **not allowed unless introduced as a separately costed experimental action**. A subject who holds an unobstructed cube is in a different observation condition and should not be compared to the theoretical single-camera optimum as if equivalent.

## 2. Verified single-camera four-way physical ambiguity

For an ordinary camera looking at F, the four configurations `solved`, `B`, `B'`, `B2` all display the **same nine sticker colours** in the initial photograph. Each is a distinct actual 54-sticker legal cube state.

With one additional legal action, a newly captured front image distinguishes all four under each of `U,U',R,R',D,D',L,L'`. Conversely `U2,R2,F,F',F2,D2,L2,B,B',B2` leave all four indistinguishable in that first extra front image. These lists are verified by the original `solvedStickerCube` + `applyMoveToken` physical model, **not** guessed geometric instructions or an orientation-bit abstraction.

This produces a participant-understandable diagnostic choice: immediately turn an informative neighbouring face, or take an action that fails to reveal which hidden state is present. It is only an **instrument manipulation-check example**; relying on it alone would let subjects memorise one solution.

## 3. New reusable 24-trial genuine nine-sticker pilot bank

**Implemented, regenerated and CI-tested**: [physical pilot bank compiler](../../scripts/cuberev-021/build-p2-24-real-sticker-camera-pilot.mjs) creates 24 four-choice diagnostic trials, **four for each camera face U,D,F,B,R,L**, from 14 candidate shared legal 18-HTM scrambles. For each front-camera orientation V with opposite face H, the four possible real-cube states are `G, G H, G H', G H2` for the same legal base scramble G.

The opposite-face turn H cannot immediately alter any of the nine standard stickers on camera face V, so all four candidates have **exactly the same initial photograph**, though their full cube states differ. The compiler mechanically verifies:
- each complete 54-sticker configuration comes from literal legal moves;
- cubie permutation is bijective and edge flip/corner twist physical invariants hold;
- the four alternatives are distinct full cube states yet have identical initial nine-colour camera images;
- at least one of the 18 real next-turn choices yields **four distinct next images**, allowing one-turn identification of the hidden alternative;
- the 24 chosen trials balance the six camera faces rather than endlessly repeating solved/B;
- trial records include reference seed and alternatives, all 18 next-turn diagnostic ranks, limited counterfactual photos and an experimenter answer-key placeholder. **The experimenter must randomize the true hidden alternative trial by trial instead of using the placeholder as participant data.**

**External CI PASS**: [Actions #38040889437](https://github.com/WhoSia/CUBE-REV/actions/runs/38040889437), [raw machine proof receipts and full 24-trial bank artifact #11665767124](https://github.com/WhoSia/CUBE-REV/actions/runs/38040889437/artifacts/11665767124), ZIP SHA256 `efc927418eceb18ce4f45155b480f11f47bcf5fc41c7bac12b1d16da778d7960`. Source commit `c82afd0dd8dbe2f420d878d4484de5e75bd60065`. The bank has **not been administered to humans**.

This task measures diagnostic inspection / identifying the correct prior candidate. It does **not** measure solving the cube from arbitrary scramble, and a distinct transfer task is required before drawing everyday generalisation claims.

## 4. Separate real-cube two-cubie coupled model (tagged observation, not natural colour)

For two different, explicitly labelled actual edge cubies (UR target identity 0 and UF target identity 1), with both original intrinsic flip bits 0 and distinct unknown starting slots, the initial ordered pair count is **12·11=132**, not independent `12^2=144`. No actual cube admits the two distinct pieces in the same edge position. The 18 shared face turns are taken simultaneously on BOTH cubies, never two independently controlled toy automata.

The physical 24-state sticker-derived edge maps yield **528 physically reachable oriented ordered pair configurations**: `12·11·2^2=528`. A breadth-first search of this genuinely coupled legal face-turn orbit verifies all 528; for **every one of the 132 orientation-zero location pairs**, an explicit legal face-turn word is reconstructed from solved and replayed using the independent **full sticker cube** followed by `toCubieState`. No impossible same-slot configurations are silently included.

For a **separate marked-object task** where each of the two target edges has a visible marker on both stickers and the observer sees whether each marker appears among the four FRONT-face edge slots, the one-look, pair-of-presence-bit observation classes have exact sizes **00:56, 01:32, 10:32, 11:12**. A product-of-two-unconstrained-edge model would incorrectly predict **64,32,32,16** and a fictitious 144 states.

Exact collision-count identity for any common predetermined legal action history with separately observed two-marker readouts: If `A`, `B` are original source-slot sets compatible with each individual marker history, then the joint original source pairs compatible with both histories are precisely
`(A×B)\\{(s,s):s∈A∩B}`; cardinality `|A|·|B|-|A∩B|`.
Proof: deterministic legal cube action on edge slots is bijective; two different source slots never become the same destination slot. The marker observations factor through each labelled slot under the same common action sequence. Thus the only forbidden product pairs are matching original source slots. The argument applies to each realised adaptive history, since along a realised branch both hypotheses experienced the same actions, but this **does not** mean arbitrary policies for the two targets are independently controllable.

Original 8-HTM positive word: `L' U2 R2 D2 L' R D L2`. Its prefix number of distinct **two-tag joint observation histories** on all 132 starting pairs is **[4,14,32,57,73,91,111,132]**. Hence eight turns suffice to recover both initial labelled slot locations in this **tagged-front-window** ontology; **optimality not yet proved**. The one-edge marker prefix rank is **[2,4,6,8,9,10,11,12]**. This is not the 0.19 orientation-bit nine-turn theorem, nor the sticker-only 24-trial pilot.

A future larger number of jointly tracked pieces leads to assignment constraints (distinct positions), partial matchings and Hall-type obstructions. These are natural later mathematical/TCS research questions, NOT newly certified complete-cube results.

**External real 2-edge finite proof:** [CI #38040889437](https://github.com/WhoSia/CUBE-REV/actions/runs/38040889437), script [shared edge and front-colour verifier](../../scripts/cuberev-021/verify-p2-shared-edges-and-real-face-colours.mjs), same proof ZIP above. Its source zero-flip pair placements were **all** realised and checked by whole-cube sticker replay.

## 5. Human P2-H experiment — separate memory, foresight and action burden

**Pilot objective**: establish if a person can use real nine-colour face information to select a useful physical viewpoint, not whether they satisfy ideal Bellman policy. No participant data collected. Pilot scope can begin with a **small, voluntary, teacher-approved or adult-supported usability group** sufficient to find confusing instructions and floor/ceiling effects; a pre-registered adequately sized follow-on is needed for inferential claims. Do not recruit underage participants without appropriate school and guardian permissions; do not record faces, legal names or sensitive personal data.

**Task per trial**:
1. Introduce the ordinary 18 face actions and offer hands-on practice; clarify that “inspect F” means only its nine colours, whereas candidate reference thumbnails may depict all faces so subjects know what the four *possible* cubes are.
2. Present the four labelled full-cube candidate reference arrangements and a current restricted-camera nine-colour photo common to all four. Randomise the secret actual choice *independently* among the four, keeping its identity hidden.
3. On each turn, record which legal move the participant selected, the decision time before selecting, its actual manual or simulated execution time, the updated nine-colour photo, the available historical display and whether the participant asked to stop/identify one candidate.
4. Permit no uncharged change of camera angle. Record whether the answer is correct, not merely how many candidates the ideal simulator would have eliminated.

**Primary intervention 2×2 factorial**, with counterbalanced task identity and face across conditions:
- **External visual history**: last camera photographs available vs unavailable. The actions actually executed remain listed in BOTH groups, avoiding a confound between action memory and visual evidence memory.
- **Planning aid**: physically correct counterfactual previews of how all four *candidate cubes* would look after candidate actions vs no previews. The preview NEVER reveals which candidate is actually hidden. This estimates the effect of external computational support, not raw innate prediction accuracy.
- Use six of the 24 trials per condition per participant if task duration and consent permit; present a randomized Latin-square-like task order, and reserve practice trials outside the analyzed set.

**Measured contrasts**:
- reference-grounded diagnostic accuracy and number of physical turns (discrete);
- one-step informativeness of each chosen action, compared with the exact 18-action photographic rank table;
- time before commitment and time spent executing a turn, separately (not one unspecified “cost”);
- optional immediate prediction (“which four distinct front photos could follow?”) as a measurable **future visibility forecast**, marked with 0–4 distinguishability and predicted vs actual after choice;
- posterior confidence, memory of earlier photographs, reversals and unnecessary diagnostic turns, practice/trial-order changes.
- Analyze history and planning as **randomized assistance interventions** with both main effects and interaction. Do not attribute all of an intervention's outcome to a pure internal psychological variable without comprehension checks and alternate explanations.

**Motor / time burden stage AFTER factorial**:
- measure actual face-turn duration and latency in remote operation or a physical one-face viewing box, and compare with interface-only move-selection time;
- where consented, randomise modest waiting latency of remote turns (not high stress or arbitrary economic “taxes”) to estimate decision changes caused by action costs, holding hidden cube states and photo availability fixed;
- distinguish HTM unit turns from human physical effort: `R2` and `R` both count as one HTM but can require different motions and time.

**Analysis model separation**:
- Objective physics `s_{t+1}=T_a(s_t), y_t=O_F(s_t)` is instrument-verified.
- Internal memory and planning are *latent*; candidate empirical models include an exact-belief ideal planner, last-photo-only heuristic, counterfactual preview-sensitive model, history-supported memory model and a cost-penalized actor `Q(s,a)-λ_T(time)-λ_M(memory)-λ_D(deliberation)`. Fit only once actual data exist.
- Check a model on held-out scrambles/camera faces to resist fitting face-specific tricks.
- For any claim about everyday object inspection, a second, genuine unstructured physical-object task or unrestricted human-handling mode must be used, and the difference of available observability explicitly acknowledged.

## 6. Research foundations and caution

- Meinz, Hambrick, Leach & Boschulte (2023), [Rubik skill acquisition with 79 novices](https://doi.org/10.3390/jintelligence11010018). This is real Rubik training, **not** the one-camera diagnosis protocol, and its working-memory findings should not be overgeneralized.
- Petitet et al. (2021), [computational effort in active information sampling](https://doi.org/10.1038/s41562-021-01116-6): supports experimentally isolating deliberation costs from information benefits, not proof of the present behavioral hypotheses.
- Ozbagci, Moreno-Bote & Soto-Faraco (2021), [decisions and action during active sampling](https://doi.org/10.1038/s41598-021-02595-3): action can gather evidence as part of the decision process.
- 2026 resource-rational visual search work [Radulescu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC13053022/) reports alignment between computational search and human gaze in a VR experiment, but sensitivity to state representation; this motivates inspecting what images participants ACTUALLY see.
- 2026 resource-rational reading [Nature Human Behaviour](https://doi.org/10.1038/s41562-026-02534-0) models perception, memory and eye movements jointly; this is a conceptual competitor/analogue, not a Rubik behavioral result.

## 7. Explicit cycle back to mathematics

If experiments establish that external past-photo access or physical consequence previews change human strategies, the next theoretical question is: **what finite summary of visible photograph-and-action histories is sufficient to make good future decisions?** That is a future observable-controller memory/automata-equivalence problem with experimentally grounded action and observation alphabets; do not invoke a Myhill–Nerode theorem before specifying policy costs, observation noise and a genuinely testable equivalence relation.

**Boundaries:** joint 132 tagged-edge model and 24 real-photo task bank are two distinct, independently tested physical observation models; no arbitrary full-cube solver, no actual human sample, no generalized claims for all naturalistic tasks, no retroactive overwrite of previous generations, P7 legacy governance audit remains separate.

**P2 research state:** coupled physical edge geometry PASS; all 24 common-sticker human trial prompts PASS as instrument stimuli; HUMAN PARTICIPANT DATA NOT COLLECTED; causal human/behavioral hypotheses OPEN.

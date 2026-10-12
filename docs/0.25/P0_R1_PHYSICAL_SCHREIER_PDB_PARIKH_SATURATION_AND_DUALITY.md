# CUBE-REV 0.25 P0-R1 — Physical Schreier Quotient Duality & Parikh Saturation Barrier: Five Exact Cubie PDBs, Cost-Overcounting Counterexamples and Synchronization–Complexity Structure

**2026-10-12 · SOURCE-GRADED MATHEMATICAL EXPLORATION CLOSED (local Go+C++ executable finite courts PASS); new unrestricted global 3×3 HTM shortest-distance bound NOT claimed; external GitHub CI for this new stage NOT yet established.** The inherited genuine original WCA whole-cube certified interval remains **14 ≤ d18(s) ≤ 18**. A self-contained actual Go original-54-labeled-sticker and independent C++ physical-coordinate verifier and its numeric receipt were generated in this chat; until the connector artifact transport is restored, no claim that those executable bytes are present in the GitHub working tree is permitted. Preserve the source package as the conversation attachment and continue to request a first-class, human-authored repository import.

## The exact original Rubik object

The original physical 3×3 state is WCA Seoul Summer 2026 333 Final A scramble 1, same literal, reference frame and all 18 legal outer face HTM generators used in [P1-R6 unrestricted original cubie proof](../0.24/P1_R6_SOURCE_COMPLETE_FULL18_GLOBAL_BIDIRECTIONAL_CERTIFICATE_AND_025_GATE.md):

    R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2

The authentic solved original-54-sticker eighteen-turn UPPER witness remains:

    F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2

Do not confuse this complete word's physical validity with unproven global d18=18. The current P0-R1 asks a mathematical question motivated by M*(4)/M*(5): which small, **sound**, independently checkable structural certificates can cover the actual whole-cube source search domain, and what exactly fails when we try to combine them?

## Theorem A — five genuine cubie-position–orientation Schreier quotients

Fix the original full cube group G (with a named fixed center frame and HTM move alphabet A). For each subset I of four distinct labeled actual corners or edges, let Q_I remember **both location and orientation of each of those four ORIGINAL labeled physical cubies**. Tracking positions and orientations is not arbitrary graph relabeling: each of the 18 original physical face turns induces a **well-defined permutation on the oriented location tokens**, independent of untracked cubies. The map π_I:G→Q_I intertwines the physical right-turn action; this is a concrete Schreier G-set for the oriented pointwise-fixing stabilizer of the marked pieces. Every projected actual full-cube path of length L becomes one projected path with the SAME move word of length L.

For four labeled edges: |Q_E| = (12·11·10·9)·2⁴ = **190,080**. For four labeled corners: |Q_C| = (8·7·6·5)·3⁴ = **136,080**. Exact 18-generator reverse BFS from each specified marked solved tuple fills all states; the Go implementation explicitly checks each edge, each value range, exact reachability cardinality and 1-Lipschitz distances for EVERY quotient edge.

Use three pairwise disjoint edge patterns (edge slots in UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR reference order):
- E0 = {0,4,8,10}; E1 = {1,5,9,11}; E2 = {2,3,6,7}.
Two disjoint corner patterns (URF,UFL,ULB,UBR,DFR,DLF,DBL,DRB order):
- C0 = {0,2,4,6}; C1 = {1,3,5,7}.

Their exact quotient graph diameters are **8,8,8,7,7**. BFS original-source distances for the literal WCA cube are **[7,5,5,5,6]**, in the same order. The Go source-derived physical move tables were separately compared to direct actual geometrical motion of ALL 54 individually labeled original stickers: the literal scramble, exact previous 18-word solution, and 256 deterministic additional original-turn words PASS. An independent C++ original-coordinate implementation also confirmed the same 5 PDB cardinalities, same source distances, physical marker intertwinement, and parity saturation. Executed local source SHA-256 Go **2946e891d406890dd6129b59763ceec0cfae7d12a226f0af9b84f7295d0ce878**; C++ **c6e0a67207f337a392d48def0c004c3ec1b92fc07ef9a87c97b61b87a9e88bd8**. These are local file checksums, NOT a claim of verified external CI.

## Theorem B — quotient distance is a feasible shortest-path dual; careless addition is UNSOUND

Let h_I(g) be exact shortest HTM distance of π_I(g) to its solved marked-cubie tuple, in the genuine 18-move quotient graph. For every g∈G and legal move a∈A:

    h_I(e)=0;  |h_I(ga)-h_I(g)|≤1;  h_I(g)≤d18(g,e).

This follows because π_I sends each actual move to one quotient move and the quotient distance obeys the triangle inequality. Each h_I is an independently checkable integer-valued feasible 1-Lipschitz shortest-path **dual potential**. The pointwise maximum H(g)=max_I h_I(g) is also 1-Lipschitz and admissible, since max of functions with common 1-Lipschitz bound retains that bound.

**But their sum is not generally admissible.** At the source, Σh_I(s)=**28**, contradicting the already physically complete 18-turn source solution if misread as a global lower bound. There is an even smaller fully physical counterexample: on the original solved cube apply just **U**, which has true distance 1. All five of these patterns have an affected piece, each quotient h_I(U)=1, hence Σh_I(U)=**5**, while max h_I(U)=1. Similarly R and F each give false sum4 for a true one-move state. Disjoint PIECE sets do not give disjoint TURN costs: the same actual face move can reposition pieces in several disjoint patterns at once.

Any proposed additive PDB must supply a **move-cost partition or other valid common feasible dual**: for every actual generator a, allocated costs c_I(a)≥0 with Σ_I c_I(a)≤1, and each quotient must compute its correct weighted minimum. Merely adding unweighted distances is an invalid proof and invalid optimal-search heuristic.

The actual benchmark H(s)=max(7,5,5,5,6)=**7**, far weaker than the previously independently regenerated unrestricted entire-cube lower bound **14**. Therefore this stage does NOT strengthen the global distance interval. It identifies why cheap pattern quotients cannot trivially replace the expensive all-cubie certificate.

## Theorem C — exact face-Parikh parity synchronization saturates and cannot exclude length 17

A single *real* full cube word w=a₁···a_L determines one common six-bit vector p(w)∈(Z/2Z)⁶ counting its per-face move-token occurrences mod2 (each quarter/half-turn costs ONE HTM token, so it flips its named face count once). For each quotient Q_I define its exact accepted parity set:

    P_I(L;s) = {p(w) : |w|=L and π_I(s·w)=π_I(e)}.

Every true full-cube L-move solution w must satisfy p(w)∈∩_I P_I(L;s). Consequently, **if the intersection is empty, there can be NO whole-cube solution of length L**, even though each component may independently have its own favorable path. This is a sound synchronization-based source-exclusion test, stronger in logical type than simply adding quotient distances.

A deterministic finite dynamic program over (quotient state, 64-bit face-parity set) enumerated all 18 actual generators and all length layers L=0..18 for all five physical PDBs. At **L=8** every individual P_I contains ALL **32** six-face parity vectors whose total parity is even; at **L=9** it contains ALL **32** vectors of odd total parity. The five-way intersections are also all32 at L=8,9,17. The earliest nonempty intersection is L=7, giving only the same weak lower7.

**Finite theorem upgrading to ALL lengths L≥8:** If a quotient admits a source-solving word length L with face-vector p, append any legal a·a^{-1}: exactly two further legal HTM turns preserve the cubie endpoint and the six-face parity. Therefore the saturation at even L=8 and odd L=9 propagates to EVERY L≥8. Thus for this fixed WCA source and these five particular quotient endpoint languages, their **six-face parity-of-counts shared constraint has absolutely no excluding power at any candidate length 8 or greater**, even at L=17. This conclusion has an exact finite 8/9 base test and a general padding proof, not merely an empirical guess. It is a no-go result for THIS synchronization grammar, not for stronger nonabelian word-order, per-state coset, costed action, or full-cube constraints.

## Theorem D — full synchronous product restores the hard original puzzle

These five selected patterns constitute a DISJOINT COVER of all actual labeled edges and corners, each with orientation. Therefore the joint map

    Π(g) = (π_E0(g), π_E1(g), π_E2(g), π_C0(g), π_C1(g))

is **injective on genuine original full-cube states**. It specifies every 12-edge position/flip and 8-corner position/twist, hence reconstructs the true original whole-cubie state. If one forces the **same complete ordered 18HTM move label at each time step** in all five quotient automata, the reachable part of their synchronous product is isomorphic to the original physical cube Cayley graph (with the impossible/nonphysical product tuples excluded by common reachability). This restores exact full original cube geometry but also restores its original large group-search problem.

The mathematical trilemma exposed by this particular experiment is:
- **Uncoupled small quotient distances:** cheap and individually sound, but max-source lower only7.
- **Six-face Parikh-abelianized endpoint synchronization:** jointly sound yet completely saturated for L≥8; discards the order/noncommutative physical group information essential to 17-turn exclusion.
- **Fully label-synchronized product:** lossless whole 3×3 cubie search; exact, but recovering the previously difficult state-space size and memory load.

This does NOT prove a universal computational lower bound for all clever quotient algorithms. It forces a specific research design question: what INTERMEDIATE, source-complete coupling (double coset witness, nonabelian ordered action signature, admissible source-bucket covering, certified cost partition) retains enough group information to improve a lower14 certificate without materializing the full product?

## P0-R2 real next mathematical experiment and falsification

Do NOT simply scale five tiny independent PDBs and claim progress from summing their numbers. Test:
1. Joint full **corner CP×CO** original physical PDB (8!·3⁷=88,179,840 legal corner states) with exact orientation parity, independent source cubic geometry, and explicit admissibility. Its memory/transition budget must be recorded. Its singleton distance remains at most its own diameter, not magically ≥18.
2. **Source-bucket lower-bound certificates**: for every exact original 18HTM source normal-form prefix p in a frontier of declared depth, certify a valid remaining-distance lower potential or continue exact search. Each bucket must have an independent proof of the **cover**, no unsupported symmetry quotient, and an explicit unresolved/HOLD count.
3. **Genuinely synchronized quotient product under a short noncommutative action automaton**, preserving more than six-face parity while not escalating immediately to all physical cubies. A candidate should exclude at least one source prefix that individual PDBs and Parikh masks would not, with real WCA source transfer and independent replay.

Success means actual original whole-cube legal pruning with mathematically proved optimality preservation and a measured held-out improvement OR a new unrestricted whole-cube distance lower certificate. Failure means a retained exact counterexample/no-go proof. The mandatory original global truth at this P0-R1 freeze stays **14≤d18(s)≤18**, and the real 18-turn source solution remains a valid upper witness. Prior 0.24 P1-R6 CI evidence is not misrepresented as new P0-R1 CI.

**Governance:** code produced in this chat as both Go and independently derived C++17 physical finite verifiers, with a deterministic output receipt; GitHub source import is pending because the file-to-connector container transfer expired. Never assert bot-authored commits, successful 0.25 GitHub Actions or imported source artifacts without live receipt. Commit author and committer must be WhoSia only; all future Actions read-only, no generated writeback. Real private human 451 trajectories and restricted FMC materials are not used in this proof.

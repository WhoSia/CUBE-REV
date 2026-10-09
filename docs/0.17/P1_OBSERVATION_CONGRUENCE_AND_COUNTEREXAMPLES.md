# CUBE-REV 0.17 / Internal P1 — Action-congruent sensors destroy identification

**Authority:** hand mathematical theorem (classical automata-congruence logic) with separately tested countermodels. NOT a claim of novel general automata theory or a measured human cognitive phenomenon. The Lean source has not yet received an independently observed successful kernel build.

## Setup

Let X be a nonempty state space, A an action alphabet with each T_a:X→X a bijection, and let O:X→Y be a deterministic observation. Actions may be selected adaptively from all earlier observation reports; exactly one report is obtained after every action.

The **action-congruence property** of O means for all x,y and all a,

`O(x)=O(y) => O(T_a(x))=O(T_a(y))`.

Equivalently the observation partition is preserved as a quotient transition system. It is a stronger hypothesis than mere action reversibility, and very different from transitivity of the action group.

## Theorem (no within-class identification under action congruence)

If O is action-congruent, then for any pair x,y with O(x)=O(y), EVERY common preset action word induces the same successive observed-output trace from x and y. Hence any deterministic adaptive controller, whose next action/stop decision depends only on the available observations, makes exactly the same decisions on x and y and cannot identify which original state occurred. If x≠y and all actions are bijections, the same controller also cannot send BOTH initial states to the same exact physical target: each branch executes the same permutation word.

**Proof:** Induction on trace length. At a single step the congruence hypothesis ensures equal next outputs; it therefore applies recursively to the resulting pair of states. Feedback selects the same action at every indistinguishable history. The final two states remain unequal by injectivity of the action-word composition. QED.

### A transitive reversible countermodel

Take X=Z/4Z, A={+1,-1} with both actions acting by modular addition. This action group is TRANSITIVE on the four states and inverse closed, yet with O(x)=x mod2 the output partition has two 2-element blocks {0,2} and {1,3}. Every action flips parity and therefore preserves the partition as a congruence: any sequence, adaptive or not, gives identical observation traces for 0 and2 (and separately 1 and3). **Transitive reversible dynamics do not imply state-identifiability.** This explicitly falsifies a plausible but false 0.17 general conjecture.

### A separate failure of observable-class return maximality, even under PSD

Take X=Z/3Z, literal actions A={0,+1,-1}, one token for each translation. The action-count matrix B is the 3×3 all-ones matrix J, symmetric, PSD and vertex-transitive. Fix starting state0. Every single-state terminal coordinate receives exactly ONE length-one word, so the all-t return-state maximality theorem holds with equality. But under O(0)=a, O(1)=O(2)=b, the two-word observation class b has two compatible words, whereas the starting-state observation class a has only one. Consequently **state-level return maximality does not survive arbitrary partitioning into observable classes**. Correct generic bound: for C⊆X, the class fiber is Σ_(y∈C)(B^t)[x,y], bounded by |C|·(B^t)[x,x] under the prior return-maximality hypotheses, not necessarily by the return count alone.

## Scientific implication for the current CUBE-REV program

The 0.16 physical single-edge intrinsic-bit sensor is NOT action-congruent on all 24 states (it can eventually distinguish all), so its h=8 diagnosis optimum is not a contradiction. This theorem supplies a TRANSFERABLE structural obstruction and a counterexample against overly simple group-transitivity assumptions. Its abstract proof is classical; model-specific novel results must come from finer partial congruence / stabilizer / partition-refinement bounds, not naming the congruence principle.

## Lean status

An isolated Lean4 v4.34.1 workspace under `formal/017/` states and attempts to prove the trace-induction implication and a finite Z4 parity countermodel. The semantics of adaptive decision trees require an explicit controller definition in a later kernel-verified module. A successful Lean kernel run is NOT YET OBSERVED, so no Lean-certified result is claimed. Even if the general trace theorem compiles, physical cube simulation equivalence remains separately required.

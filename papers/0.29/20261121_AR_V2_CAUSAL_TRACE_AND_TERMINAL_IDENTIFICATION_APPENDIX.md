# AR v2 Supplement — From Signed Posterior Equality to Causal Transcript Equivalence and Terminal Identifiability

**Independent authorial chapter; 2026-11-21.** Intended as a *conservative addendum* to `20261121_AR_SIGNED_POSTERIOR_BISIMULATION_WORKING_CHAPTER.md`. It preserves T/U/V/W and AR v1 instead of rewriting their historical source. The claims below are separated into formal algebra and open Rubik-specific lemmas.

## 9. Equality of the actual adaptive execution trace

The equality of posterior fibers following a fixed query/response history does not immediately show how the response-dependent **query addresses** of a specific controller are transported. In particular, a policy could agree on all color-count partitions while choosing different next addresses after the same color answer.

We therefore define a trace-logging operation on policies that preserves the selected branch at every node, adding to the eventual output the ordered pairs ((q_1,r_1),ldots,(q_m,r_m)). The representative logged policy is adapted to the source paired sensor by two deterministic transformations: the current representative edge slot is pulled back through the inverse normalization order, and the physical edge reply is renamed using the chosen six-color map. The corner address and corner reply are unchanged.

**Theorem 9.1 (causal adaptive trace equivalence).** Let (P) be *any* representative paired-color decision tree, and let ((g,eta,arepsilon)) be a fixed normalization witness chosen before (P) begins. For every tagged original state (x),
[
\mathrm{run}\bigl(\mathrm{adapt}(\mathrm{log}(P),Q_\beta,R_g),O,x\bigr)
=\mathrm{transcript}\bigl(P,O',T_{g,\beta,\varepsilon}(x)\bigr).
\tag{9.1}
]

*Proof.* The paired observation covariance law identifies every recoded source response (R_g(O(x,Q_\beta(q)))) with the representative response (O'(T(x),q)). The generic policy reply-invariance theorem applies this pointwise identity at all query nodes of (mathrm{log}(P)), including those chosen by previous responses. The policy adapter preserves the exact semantics of the logged tree, while the log–run identity identifies its output with the ordered selected query/reply sequence. Since the query pullback is applied when a decision node is reached and before branching, the construction uses no current-round or future answer in selecting the corresponding original address. □

**Theorem 9.2 (budget conservation).** If (mathrm{Fits}(k,P)), then (mathrm{Fits}(k,\mathrm{adapt}(\mathrm{log}(P),Q_\beta,R_g))).

*Proof.* Logging adds no read node, only an accumulating value in the eventual output. The response and query adapter has a one-to-one correspondence between its read nodes and those of the original policy. Induction on the (mathrm{Fits}) derivation gives the same bound, including every unfeasible response branch in the total tree. □

These statements are implemented by `transported_signed_policy_transcript_exact` and `transported_signed_transcript_preserves_budget` in `SignedPolicyTranscript.lean`. Together with Section 4's all-history posterior equality they establish an appropriate **generic signed decision-game bisimulation** for a *fixed* normalizing witness.

## 10. The empty leaf and independent parity-tag traps

The frozen certificate's terminal condition “at most one oriented edge assignment per sign” permits two candidates at a leaf, one even and one odd, **before** physical corner parity is used. It can also be true for an empty posterior, which would be an inconsistent transcript rather than a successfully identified initial state.

Define the terminal success predicate to require *existence and uniqueness*:
[
\mathrm{Unique}(B)\iff\exists s\in B\ \forall t\in B,\ t=s.
\tag{10.1}
]
If a signed transport (T) has a concrete left inverse (D), then (\mathrm{Unique}(B)iff\mathrm{Unique}(T(B))). Forward uniqueness follows because images of unique witnesses are unique; reverse uniqueness applies (D) to the equality of encoded candidates. Combining this property with the arbitrary-transcript covariance law yields a terminal identification equivalence *for every possible ordered paired feedback transcript*.

**Theorem 10.1 (singletons are preserved).** For every eligible fixed normalized witness and every original signed belief (B), (mathrm{Unique}(B_h)iffmathrm{Unique}([T(B)]'_h)) after every finite ordered history (h).

**Theorem 10.2 (no independent parity oracle).** Attach to any fixed cubie/corner coloring (c) a free tag (p\in\{0,1\}), and let the physical paired observation ignore that tag. No adaptive paired-color policy—regardless of its observation budget—can correctly distinguish both ((c,0)) and ((c,1)) as distinct initial tagged states.

*Proof.* Both inputs give the same reply to *every* paired sticker query, so every adaptive controller takes the same response-labeled path and returns the same output. Correctness for both would require that output equal both distinct tagged states, a contradiction. □

Thus a legal-cube parity constraint is a **mathematical necessity** for the two-candidate terminal decoder, not a convenient implementation shortcut. The physical edge and corner permutation parity equality is the bridge that must constrain the abstract sign tag; the actual nineteen-corner scan must provide enough data for that constraint to select the right candidate *at the terminal frame*, not earlier.

The implementation is `SignedTerminalIdentification.lean`. Neither Theorem 10.1 nor 10.2 implies the frozen 52-root certificate's leaves are all actually unique. These statements establish the correct meaning of terminal correctness and rule out an invalid oracle model.

## 11. Exactly what remains open

The methods from Sections 4, 5, 9 and 10 establish strong **conditional** correctness by functoriality of state, query, reply and terminal-output transport. The next step is not to multiply these abstract transport lemmas indefinitely. The project must now construct the concrete mathematical objects satisfying them:

- A total, deterministic selector from **each ordered feasible eleven-edge first-color word** to a 48-element color symmetry, the stable sorting slot permutation with its actual inverse, and the correct XOR parity-cocycle correction; choose this selector solely from the observed prefix.
- A proof that the resulting signed representative prior is exactly the finite candidate sector enumerated by `NineteenReadData.sector`, including the even total flip constraint and the terminal coupling to the legal corner permutation sign.
- A total Lean policy interpreter of each of the 52 frozen JSON continuation decision trees with exactly all feasible color branches and proof that every leaf selects the correct representative initial state *after* incorporating actually read corner parity.
- The exact nineteen-corner observation schedule and fixed-probe routing compiler, yielding a theorem of the form
  [
    \exists P,\quad \mathrm{Fits}(19,P)
        \land \forall s\in\mathcal S,\ \mathrm{run}(P,O,s)=s.
  \]
  The eighteen-frame impossibility proof must retain its separate certified-DAG trust disclosure.

**Review verdict.** The causal transcript theorem closes a potential proof gap about *feedback query addresses* in the generic transport framework. The no-free-parity theorem closes a potential model gap about *terminal sign availability*. Neither closes the remaining certificate-to-semantics and physical legality constraints. A finished manuscript must state each distinction plainly.

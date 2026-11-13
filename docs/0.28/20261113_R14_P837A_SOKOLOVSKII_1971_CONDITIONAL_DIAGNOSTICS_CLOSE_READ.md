# R14-P8.37A — Sokolovskii (1971), original English translation: conditional versus unconditional diagnostic experiments

Original PDF [in canonical Research OS 10_PAPERS](https://drive.google.com/file/d/1LGuVfwiMk7mk_lT6egC36F4iING6XBIf/view), SHA256 `066a2ac5384fde1d4b5ae925ccb47f4c9b2101c2f1e443c7162b1f2b8895f381`. Published bibliographic citation: M. N. Sokolovskii, *Diagnostic Experiments with Automata*, *Cybernetics* **7**, 988–994 (1971), DOI [10.1007/BF01068822](https://doi.org/10.1007/BF01068822), English translation of *Kibernetika* issue 6, pp. 44–49 (1971). The PDF's later copyright line reads 1974; cite publisher's article year **1971**, record the manifestation distinction.

## What the actual article says (first-page definitions, pp. 988–989)

A known deterministic finite Mealy automaton (A) begins in one of the possible states (M\subseteq Q). Feeding an input word changes the automaton state and emits an output word. The experimenter wants to identify either the *initial state* (diagnostic problem (DP(A,M))) or the *final state after the experiment* (homing problem (HP(A,M))). These are **different decision targets**. A selected input word fixed completely beforehand is an **unconditional** experiment, UDE/UHE. An input selected in response to prior input–output history is a **conditional** experiment, CDE/CHE. A conditional experiment has worst-case branch length; unconditional experiments are a restricted special case.

The text explicitly records a limitation: a diagnostic CDE **need not exist**, even if states are distinguishable, with a three-state initial candidate set given as the obstruction type; *homing* problems have different existence conditions. It defines admissibility of a proposed word so that unresolved states never become irreversibly merged, and calls a word *splitting* if it generates a nontrivial output partition with all branch subproblems still solvable. Its recursive claim (assertion 2) states that the candidate problem is solvable iff a splitting word exists; a derived upper bound has the form

[
\ell(A,M)\le |x|+\max_i\ell(A,\Psi(M_i,x)),
]

where (M_i) are output-equivalence classes after word (x), and (Psi) maps the remaining candidates to their resulting machine states. This is a **conditional upper-bound construction**, not a closed-form equivalence of machine diagnostics and Rubik sensing.

## Relevance, exact differences and scientific caution

For CUBE-REV categorical color querying, the posterior (P) is an exact subset of unknown legal **initial** cube states. A legal cube move acts bijectively on (G), and each chosen site-color reading produces an output partition. P8.37 motivates a posterior search tree: choose a cube action, read two spatial sticker colors, branch by the observed pair, and recursively identify the original unknown state with a decoder. Such a tree shares the **feedback/partition** structure with Sokolovskii but not arbitrary Mealy transitions, arbitrary output functions, an unrestricted input alphabet, or freely timed machine observations.

**Crucial connection:** a legal Rubik move is a *permutation*, so a pair of distinct underlying initial states cannot permanently merge under cube moves alone. This removes a central class of transition coalescences that Sokolovskii has to guard against, although two states can remain observationally indistinguishable for many steps. The target is initial-cube identification; do not silently reinterpret P8.37 as homing, and do not claim Sokolovskii proves (h_{\rm adaptive}\le20) or prohibits (h=19).

## New strategy for the unrestricted 19-frame question

Use a posterior DAG key of original-state survivor set **and current known movement transform** (or a justified symmetry-canonical quotient), with output-fiber splitting and worst-case branch cost as an exact recurrence. Any proposed symmetry contraction must preserve both possible future action choices and the fixed color-site readouts. Failed branches should carry paired indistinguishable-state certificates or dual adversary bounds. The 19-frame theorem remains OPEN.

No first-discovery claim: this 1971 primary article is explicit evidence that preset-vs-adaptive experiments and their worst-case tree-length objective are classical.
# R14-P8.37C — Hopcroft 1971 Stanford TR: exact partition refinement, not a cube shortest-query theorem

**Primary document actually acquired:** [Hopcroft (1971), *An n log n Algorithm for Minimizing States in a Finite Automaton*, Stanford Computer Science Technical Report STAN-CS-71-190, January 1971](https://drive.google.com/file/d/12GrNUvr5mff-IP43DY13Vvev5Pi2sFbx/view), 16-page institutional report, SHA-256 `2e21b62a19167da72ba546d1572db53a42c4bd6632d6907a78e39fdf4e600706`. This is **not assumed byte-identical** to the book-chapter manifestation in *Theory of Machines and Computations* (1971), 189–196.

## Reading of algorithm and proof idea

The source's abstract promises an automaton minimization/equivalence algorithm of asymptotic complexity (O(k n\log n)), where (n) is the state count and the constant is linear in input alphabet size (k). The introduction contrasts classical repeated partition refinement as potentially quadratic with a strategy that indexes **inverse transition tables** and chooses smaller split blocks so the aggregate work of repeated refinements is bounded by a logarithmic number of charges per state.

Initial partition groups states by their output behavior. A splitter block (A), for input letter (x), refines a candidate block by whether its (x)-successor belongs to (A). Iteration until stable gives equivalence classes. This is a *minimum-state quotient* of an observable automaton, not the minimum number of **physical observations** necessary to distinguish all states, and not the minimum-depth adaptive experiment.

## Transfer discipline to CUBE-REV

This exact refinable-equivalence structure suggests deterministic caching and fast posterior splitting for all candidate states in a **fixed sensing sequence** and helps build sound lower-level data structures for the unrestricted adaptive horizon. But a binary split heuristic (e.g. always process the smaller half) that accelerates automaton minimization must NOT be assumed to optimize worst-case color-probe decision-tree depth. In a decision tree, a locally balanced partition can be globally inferior because the future legal cube moves and selected observed spatial sites constrain subsequent partitions.

Follow-up engineering proof gate:
1. compare naive explicit candidate-set partition refinement with an incremental inverse-action-index representation on small mechanically generated cube subgroups;
2. require equality of all output fibers before accepting fast implementations;
3. explicitly separate time complexity to compute a policy from observation cost of executing it.

No original algorithm novelty claim: Hopcroft's refinement and 1971 complexity result are historical prior art.
# QAST formal constitution (argument-first freeze)

## Objects

A bounded decision system is `(S,A,T,Q,c,B,R)` where `S` and `A` are finite, `T:S×A→S` is exact, `Q⊆S`, `c:A→R≥0`, `B` is a cost bound, and `R` is a prefix-closed language of admissible histories. A chart `r` supplies exact state coordinates `Phi_r`, action coordinates `E_r`, an observation `q_r:S→O_r`, and an admissible primitive set `M_r⊆A`. A representation relation `(g,gamma)` is a pair of bijections on states and actions.

For a start `s`, define `Reach_r(s)` iff a word `w∈R∩M_r*` has cost at most `B` and sends `s` into `Q`. A context domain is an explicitly enumerated set of task tuples. No statement below ranges beyond its declared domain.

## Axioms and boundary conditions

- A1 Exactness: equality, transition, target membership, cost and grammar are operationally decidable on the certified domain.
- A2 Chart separation: physical transition objects and their coordinate encodings are distinct typed objects.
- A3 Observation intervention: replacing `q` does not modify `S,A,T,Q,c,B,R` unless a coupling is declared.
- A4 Action intervention: replacing `M` does not modify `S,T,Q,c,B,R,q` unless a coupling is declared.
- A5 Representation isomorphism: equivariance claims require `g(T(s,a))=T(g(s),gamma(a))`, target preservation/reflection, cost preservation, grammar transport, and exact selector transport.
- A6 Domain authority: a total within-domain representation pairing requires closure, or an explicit completion carrying provenance.
- A7 Certificate polarity: simulation can preserve positive reachability without preserving negative reachability. Negative and no-separator transport require reflection/completeness conditions.
- A8 Outcome typing: the product outcome `(Y_O,Y_A)` is distinct from an arbitrary scalar functional of both coordinates.
- A9 OOA is not false: unavailable or out-of-authority outcomes remain separately typed.
- A10 Counterexample priority: a registered counterexample defeats the incompatible claim; it may not be repaired by renaming the result.

## Frozen size order for counterexamples

Minimize lexicographically: number of states; number of actions; budget; largest observation fiber; selector-family size; canonical transition/label encoding.

## Authority ceiling

These statements govern finite exact systems and declared morphisms. They provide neither external-domain validity nor behavioral, cognitive, or causal authority.

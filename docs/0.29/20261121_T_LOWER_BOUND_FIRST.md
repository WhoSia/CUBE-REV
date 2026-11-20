# CUBE-REV 0.29 T — Eighteen-frame impossibility first

The author set scholarly submission and end-to-end formal verification as the goal. The paper opens with the impossibility of eighteen adaptive paired frames, even when every corner coordinate is known. The nineteen-frame policy follows as the upper bound that attains it. The preset optimum of twenty-one and the delayed-sign refinements are secondary.

The T manuscript stays in the editorial handoff. Its proof order is model, eighteen-frame lower bound, nineteen-frame construction, and preset comparison. The ten-state illustration now sits in Appendix E. The 1.10% result for a fixed eleven-read prefix remains a supporting policy analysis.

## Lean 4.34.1 results

- The generic anytime decision-policy theorem produces distinct inputs with exactly the same sequence of chosen queries and responses, including after a query translation or free known reply. The paired specialization reads one edge color per frame and supplies the corner color from the disclosed configuration.
- The eighteen-query data checker reproduces 6,274 states, 43,870 arcs, 1,418 terminal records and 87,740 checks of lifted witness assignments. Both parity roots are required.
- The nineteen-frame checker reproduces all 1,362 raw first-color vectors, 52 representatives, 144,736 assignments and 141,097 policy tree nodes. Every leaf contains at most one assignment per parity.
- The checkers certify the reported data by Lean native computation. The no-`sorry` policy theorem depends on standard Lean axioms. For an end-to-end theorem the verifier must construct the semantic residual certificate, establish the physical-state model connection, and link the upper policy to the physical corner schedule and full prefix transport.

## Next theorem obligations

1. Identify each certified residual node with the precise set of admissible completions. Prove that its first- and second-read inverse lifts satisfy `EdgeLift` for every allowed residual word, using the orientation and rank-insertion lemmas now in Lean.
2. Assemble the checked graph into a semantic `ResidualCertificate` with the two real roots. Specialize the transcript-collision theorem there.
3. Link the cubie legality representation and the paired queries to legal cube moves. Prove the complete 19-frame construction and preset comparison in that same model.
4. Freeze the verified theorem(s), confirm the venue requirements, and prepare the submission files.

[Lean sources and reproduction](../../formal/029/README.md) · [S paper](https://app.notion.com/p/41cef561cf9281cb9c88e4f0c6188108)

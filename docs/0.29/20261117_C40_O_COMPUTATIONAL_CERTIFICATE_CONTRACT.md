# CUBE-REV 0.29 / C40-O — Exact-computation audit contract

Date: 2026-11-17. Draft for manuscript section on computational methods.  All prior editions are preserved. Connected GitHub account: WhoSia; do not use github-actions[bot] as a contributor.

## What is computed, and what is checked

| Research proof component | Existing executable | Contract / evidence |
| --- | --- | --- |
| Joint fixed-probe address reachability | scripts/cuberev-observation/audit_r14_p51_p48_group_lift.py | All 576 ordered (edge sticker, corner sticker) addresses are reachable by legal turns. |
| 19-frame policy generation | scripts/cuberev-observation/audit_r14_p840_constructive_19_frame.py | Enumerate 52 representative first-color records and construct winning edge query policies; this older file also contains a frame-14 sign-release implementation. |
| Final-frame sign audit | scripts/cuberev-observation/audit_r29_final_frame_parity.py | Check 1,362 prefix multiplicity vectors, Burnside fixed incidences 2,496 / 48 = 52, replay 144,736 representative assignments, verify sign-specific uniqueness at frame 19, physical witness / 48 moving stickers. |
| Direct Python 18-frame solver | scripts/cuberev-observation/verify_r14_p841_explicit_minimax.py | Both corner-disclosed parity roots lose; literal four-edge suffix comparisons. |
| Independent C++ 18-frame solver | scripts/cuberev-observation/audit_r14_p841_corner_oracle_minimax.cpp | Both roots lose under optimized residual-state recursion. |
| Adversary DAG verification | scripts/cuberev-observation/audit_r29_eighteen_query_dag.py | Check stored compressed JSON certificate against every possible next query; 6,274 reachable nodes, 43,870 query-response arcs, 1,418 two-witness leaves. |
| Conditions in Lean | formal/028/ObservationCovariance.lean; formal/028/TwoStepAdversary.lean | Conditional lemmas, **not** a formal proof of the global 21/19 theorem. |

## Abstract proof predicates

Let B be a set of oriented edges compatible with an eleven-color prefix, and let M(q,c) be the answers at edge address q.

- Success after the sign is known: `|B intersect EVEN| <= 1 and |B intersect ODD| <= 1`.
- A candidate query q is winning when **every feasible** returned color c gives a winning continuation on `B intersect M(q,c)`.
- The paper's final-frame implementation invokes `EdgeGame.action(game.full,8,8)` in `audit_r29_final_frame_parity.py`. The eighth follow-up is the nineteenth frame. The permutation sign cannot influence which edge address is selected in that frame.

For the lower bound, use normalized state `s = (remaining_labels, known_first_colors, sign, flip, budget)`.

- An identifying policy satisfies `W(s,k) = (count_completions(s)<=1) OR (k>0 AND EXISTS q FOR ALL feasible c W(transition(s,q,c),k-1))`.
- A losing certificate at k>0 with more than one completion must contain, for **every** admissible query q, at least one **feasible** adversarial color c with a losing child.
- At a leaf with k=0, two different feasible completions witness ambiguity.
- Induction and inverse transitions lift terminal witnesses to a pair of original cube states indistinguishable along the entire adaptive transcript.

The certificate is `data/0.29/EIGHTEEN_QUERY_DAG.json.gz`. Recorded SHA-256 of the **decompressed JSON**, to be checked at packaging time:
`dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce`.

The parser exposes:

```text
python3 scripts/cuberev-observation/audit_r29_eighteen_query_dag.py check data/0.29/EIGHTEEN_QUERY_DAG.json.gz
python3 scripts/cuberev-observation/audit_r29_eighteen_query_dag.py trace data/0.29/EIGHTEEN_QUERY_DAG.json.gz
python3 scripts/cuberev-observation/audit_r29_final_frame_parity.py --check-coverage
python3 scripts/cuberev-observation/audit_r29_final_frame_parity.py --physical-witness
```

## Independence limits and proposed next tests

1. The upper-bound search and replay share the same `EdgeGame` bitset engine. Replaying all 144,736 representatives is strong test evidence *under that engine*, but not an independent reimplementation. Export frozen representative policy trees, then write a checker that **does not import the search implementation**.
2. The lower-bound DAG verifier does not call the expensive solver. Its universal quantifier rests on complete query coverage at each internal node and its terminal legal-witness checks. Test malformed proofs (missing query, invalid color, duplicate witness, wrong parity) to ensure rejection.
3. The 48-color symmetry is a combinatorial relabeling of opposite face pairs, **not** 48 physical cube rotations. Audit query-address transport, ties in stable sorting, and both slots of the wholly unread edge.
4. Check flip/parity normalization by exhaustive small-edge benchmarks and randomized full-coordinate pullbacks.
5. Re-run the exact commands from a clean environment and lock dependencies, interpreter versions, code revision, certificate hash, and generated outputs before Zenodo/DOI release.

## Writing locations

- [O — Algorithms & certificate correctness](https://app.notion.com/p/41bef561cf9281d5af16ebd27e9a50df)
- [N — Related Work & scope](https://app.notion.com/p/41bef561cf928116bbf8d3f83ddf305b)
- [M — Appendices A–D](https://app.notion.com/p/41bef561cf9281259c79da4d854316ae)

No independent checker was created by this documentation commit. Do not claim otherwise.

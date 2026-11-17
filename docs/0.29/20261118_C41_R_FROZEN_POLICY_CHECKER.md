# CUBE-REV C41 / 0.29 R — Frozen upper-bound certificate and independent verifier

Date: 2026-11-18. Preserve Q and earlier prose versions; this records an **additional independent checker** and does not supersede prior editions.

## New evidence

The 19-frame upper-bound policy is exported as a **standalone JSON tree witness** for each of 52 representative first-11-edge-color profiles. There are 141,097 explicit tree nodes in total. A verifier which **does not import the minimax search** independently enumerates legal edge assignments for all 52 representative profiles, traverses every feasible reply branch, rejects unreachable extra nodes, and checks that each terminal candidate set has at most one assignment per edge permutation sign.

The checker passed for all **144,736 representative edge assignments** and all **1,362 supported first-color count vectors modulo 48 opposite-pair-preserving relabelings**. SHA-256 of exact policy JSON bytes:
`80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`.

Four malformed-proof controls were rejected: a premature ambiguous leaf, a missing feasible response branch, an altered address query, and a nonexistent child node.

## Mathematical scope

The proof-object verifier certifies the policy **within the stated edge coordinate model and prefix symmetry transport**. It does not replace the mathematical edge legality and address transport lemmas, and it does NOT by itself prove the 18-query lower bound. The exact theorem 21 preset / 19 adaptive relies additionally on the separately stored adversarial DAG for the 18-query lower bound, as in P/Q §6.

A policy terminal may be reached before frame 19 when each sign class has at most one candidate; the physical policy then repeats a known edge read until the last corner sticker is read at frame 19. At all earlier frames the policy may choose an edge address only from the earlier edge replies, never from the final corner sign.

## Sources and commands

- `scripts/cuberev-observation/check_edge_parity_depth.py` (separate exact-depth enumerator)
- `scripts/cuberev-observation/export_19_policy_certificate.py` (generator, imports older EdgeGame)
- `scripts/cuberev-observation/verify_19_policy_certificate.py` (standalone checker, Python standard library)
- `scripts/cuberev-observation/test_19_policy_certificate_negative.py` (4 negative controls)

The JSON certificate, receipts, diagrams and integrated R draft are in the [Drive R reproducibility package](https://drive.google.com/file/d/1cZRW3CF4BY2At23NDk2I25jVhJe4_UUQ/view). The new [Figure S4](https://drive.google.com/file/d/1hLzNpiJoSZwbDTW2rpevNvC8SATlly6u/view) diagrams the separation of search, proof object, verifier and mathematical premises.

Run the following in the folder with these scripts and the JSON extracted from the package:

```bash
python3 verify_19_policy_certificate.py
python3 test_19_policy_certificate_negative.py
python3 export_19_policy_certificate.py
python3 verify_19_policy_certificate.py
```

The exported filename is `upper-policy-certificate.json`. The checker can be run with that file alone (plus Python stdlib) and does not invoke any search code.

## Remaining gates

- Fully independent physical-coordinate transport checks across many representatives beyond example replays.
- Negative controls and an independent model check for the **lower-bound** DAG verifier.
- Code/data immutability and a clean-environment, hash-checking release.
- No claim of Lean verification of the full 21/19 theorem.

Research rule: do not use github-actions[bot] as contributor. New commits are by WhoSia.

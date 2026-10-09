# CUBE-REV 0.16 — Lean proof gate (experimental)

**Status: SOURCE_WRITTEN; LEAN_KERNEL_PASS NOT YET OBSERVED.**
This is an isolated Lean 4/Lake workspace, pinned to `leanprover/lean4:v4.34.1`.

Local runner:
```bash
cd formal/016
lake build
```

The read-only GitHub workflow at `.github/workflows/cuberev-016-lean.yml`
runs the same Lean build and may be inspected for actual proof checking.

The file `CubeRev016.lean` currently proves (when successfully compiled):
- a composition of reversible actions cannot map distinct initial states to the same final state;
- the inverse of a recorded word recovers the original state;
- the exact **arithmetic** consequence of the earlier P8 spectral formula at t=4,
  namely 26,584 histories and the numerical 14/15-bit comparisons.

**NOT FORMALIZED YET:** the physical 24-state cubie action grammar, its octahedral graph isomorphism, full P8 spectrum, diagnosis minimum 8, reset minimum 10,
P6/P7 catalogue bound 25, or the 50-by-116 reduced cover impossibility. Those require stronger formal definitions, a proof-carrying data representation,
and successful kernel checking. A Lean source file without actual compiler logs is not a Lean theorem receipt.

Research controls: no `sorry`, no ad hoc axioms, no reliance on human psychological data. This is internal to version 0.16 and not a distinct formal name.

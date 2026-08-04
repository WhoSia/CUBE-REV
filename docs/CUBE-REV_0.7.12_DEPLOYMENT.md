# CUBE-REV 0.7.12 — source-bound browser run-in

## Release boundary

- Public host version: `0.7.12`
- Build: `0.7.12-camera-neutral-bypass-hotfix-1`
- GitHub Pages source: `main` / repository root
- Preserved baseline: `CUBE-REV_0.6.11_GitHub_Pages_Pilot.html`
- Collector: `CUBE-REV-0712-MAIN`, active after user authorization
- Receipt contract: `receipt-v2`
- Eligibility clock: `NOT_STARTED`
- Prospective human collection: authorized; eligibility clock remains inactive

`index.html` and `CUBE-REV_0.7.12_GitHub_Pages_Pilot.html` must remain
byte-identical. The verified 0.6.11 archive remains unchanged and its normalized
SHA-256 is:

```text
ced1836b372e407b328d0863b0bc968cd7d89359d5edfa91da9313989444bb31
```

## Implemented from the 0.7.12 research package

1. Decision-point availability is separated from the `NO_PROBE` arm.
2. Web Crypto `uint32` draws use exact rejection sampling into ten buckets.
3. Arm probabilities are 60% `NO_PROBE`, 20% `TIME_MATCHED_NEUTRAL`, and
   20% `STRATEGY_DIAGNOSTIC`.
4. Missing Web Crypto fails closed and removes causal run-in eligibility.
5. Probe cooldown is two intervening trials and the burden cap is three.
6. Every deployed trial is `TERMINAL_ONLY` with a nominal 2,400 ms hidden
   pre-input interval.
7. Generation motion and path-notation text are never shown to participants.
8. Hidden generator histories remain apparatus metadata and cannot support
   replay inference.
9. The neutral timing control is completely nonvisual, requires no participant
   interaction, and enforces a 700 ms floor in the background.
10. Every trial starts from the standardized camera orientation Top U / Front F
    / Right R; the previous reoriented-view cell is no longer assigned.

## Interface release changes

- The default csTimer-style keymap now includes:
  - `T` or `Y` = `x`; `B` or `N` = `x′`
  - `;` = `y`; `A` = `y′`
  - `P` = `z`; `Q` = `z′`
- The compass contains a small icon-only camera-alignment control.
- Background camera drag now composes rotations in screen coordinates with a
  3×3 view matrix. Horizontal drag remains about screen-up and vertical drag
  remains about screen-right after passing 180°.

## Certified here

- source syntax and source-bound anchors
- exact-bucket mechanics and fail-closed behavior
- cooldown and burden-cap transitions
- 10,023 hidden-history visibility traces
- nominal 2,400 ms scheduling contract
- neutral-probe content isolation and 700 ms floor
- version, archive, cache-key, collector binding, and eligibility-clock consistency
- mocked receipt-v2 client integration

## Reproduce the current validation

Run these commands from the repository root with Node.js 22 and Python 3.
This block is the command contract for `.github/workflows/validate-static.yml`;
the documentation test fails if the workflow and guide diverge.

<!-- validation-cli:start -->
```shell
node scripts/validate-static.mjs
node scripts/build-calibration-host.mjs
node scripts/validate-calibration.mjs
node tests/randomization.test.cjs
node tests/history-fidelity.test.cjs
node tests/neutral-probe.test.cjs
node tests/runtime.test.cjs
node tests/camera-orbit.test.cjs
node tests/collector-receipt.integration.cjs
python -m unittest tests/test_registry_and_annotation.py
node tests/documented-cli.test.cjs
```
<!-- validation-cli:end -->

For a local browser preview, run `node scripts/serve-static.mjs [port]`; the
port defaults to `4173`. Run `node scripts/serve-static.mjs --help` for the
accepted syntax. This server is only a preview host and does not deploy Pages
or alter the collector.

The production collector was enabled only after the user completed the verified
receipt-v2 deployment and explicitly authorized collection. Prospective clock
activation remains out of scope and stays `NOT_STARTED`.

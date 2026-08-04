# CUBE-REV 0.7.11 — Verified Source-Bound Calibration Deployment

> **Historical record — not a current execution guide.** This document records
> the 0.7.11 branch boundary. On the current `main` branch,
> `scripts/build-calibration-host.mjs` is bound to the 0.7.12 `index.html` host.
> Use the validation sequence in `CUBE-REV_0.7.12_DEPLOYMENT.md` for current
> commands.

## Verified source boundary

- Repository: `WhoSia/CUBE-REV`
- Default and deployed branch: `main`
- GitHub Pages source: repository root (`source: .`)
- Verified baseline commit: `58619a909a9343ff0f50e945ee2d2cf443c585d7`
- Canonical LF baseline SHA-256: `ced1836b372e407b328d0863b0bc968cd7d89359d5edfa91da9313989444bb31`
- `index.html` and `CUBE-REV_0.6.11_GitHub_Pages_Pilot.html` are byte-identical.

Pages run `30479133015` checks out `main`, builds from `.` into `_site`, and
deploys successfully. Calibration work is isolated on
`agent/calibration-0711`; the root 0.6.11 host is unchanged.

`calibration/index.html` is generated deterministically from the verified
baseline by `scripts/build-calibration-host.mjs`. The build fails if the
baseline hash changes.

## Version separation

The task instrument and collector contract remain `0.6.11`. The calibration
protocol and calibration build are `0.7.11`. This prevents a protocol label
from silently changing the existing collector's version contract.

## Collector finding

The live public configuration points to a Google Apps Script receipt-v2
collector expecting project `CUBE-REV`, version `0.6.11`, collector
`CUBE-REV-0611-MAIN`, and a confirmed `stored` or `duplicate` receipt with a
matching checksum.

The current repository does not contain the deployed Apps Script source. The
last repository copy exists only in history at commit
`1c4449841f2b38a50789d9eac6dd0174d5dbc4a6`; it was removed by the following
commit. Therefore the exact deployed server revision cannot be proven from the
current tree alone.

The 0.7.11 calibration host contains no Apps Script URL or study token and
cannot submit. Receipt behavior is regression-tested against a deterministic
mock implementing the current receipt-v2 contract. Validation performs no
production write.

## Implemented calibration contract

1. Pseudonymous installation linkage and a local run-in token.
2. Server-issued participant tokens required for prospective eligibility.
3. Fixed, non-adaptive probe assignment among no-probe, sham, and diagnostic
   arms, with assignment probabilities exported.
4. A 2×2×2 memory factorial: history hidden/shown,
   geodesic/redundant-equivalent history, and stable/reoriented view context.
5. Visibility-gated replay causality. REPLAY inference is permitted only when
   the generating history was shown.
6. 0.7.11 export decoration with source binding, linkage, assignments, gate
   snapshots, and clock state.
7. Two-pass annotation: blinded Pass A, then context-aware Pass B after Pass A
   is frozen.
8. A cumulative CR07-BATCH registry that rejects unsafe ZIP paths, duplicate
   batches, duplicate sessions, and conflicting session IDs without retaining
   raw payloads.

## Gate state

| Gate | Default | Effect |
|---|---:|---|
| Governance approval | false | blocks eligibility |
| Prospective human data allowed | false | blocks collection |
| Collector enabled | false | removes live endpoint |
| Server participant token | false | run-in remains ineligible |
| Source/build/protocol frozen | true | records verified origin |
| Production receipt verified | false | blocks eligibility |
| Two-pass annotation ready | true | tooling only |
| Clock authorization | absent | clock remains `NOT_STARTED` |

The runtime exposes no working activation path. `activate()` throws
unconditionally. Governance approval and a separate, reviewed server-bound
deployment are required before prospective activation.

## Review and deployment rule

Do not merge this branch into `main` merely to preview it: `main` is the live
Pages source. Review `calibration/index.html` locally or in an isolated preview.
Before any later production merge, require governance approval, server source
review, a new collector deployment ID, a synthetic receipt dry run, and signed
clock authorization.

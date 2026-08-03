# CUBE-REV 0.8.18 validation report

## Official result

`PASS-PUBLIC-LICENSED-PER-MOVE-TIMESTAMP-FIXTURE / PASS-TIMESTAMP-QC-AND-CORRUPTION-COURT / PASS-TEMPORAL-DOMAIN-GAP-DETECTION / PASS-CONSTRAINED-DOMAIN-GAP-REWEIGHTING / HOLD-RESEARCH-CONSENTED-HUMAN-FIXTURE / HOLD-PACKET-LOSS-CERTIFICATION / HOLD-STATE-CONTINUITY-CERTIFICATION / HOLD-FULL-TEMPORAL-ECOLOGICAL-ALIGNMENT / NO-GO-HUMAN-COGNITIVE-MECHANISM-TRANSFER / NO-PARTICIPANT-DEPLOYMENT`

## Timestamp fixture

Three MPL-2.0 software test replays were frozen at an exact upstream commit: Rubik's Connected 3×3, Particula 2×2 and Particula 3×3. They contain 164 raw timestamped events. The fixture is intentionally labelled public/licensed rather than research-consented.

Strict timestamp and notation QC passes for all three fixtures. Upstream-style adaptive double-turn compression produces 143 derived logical turns while preserving the raw events. Derived compression is not written back over the source observations.

## Corruption and missing-evidence court

Reordered timestamps, zero deltas, clock regression, unsupported moves and a dropped event with an explicit sequence counter are rejected. A sub-20 ms interval is retained with a warning rather than silently deleted. A dropped event without a sequence counter remains structurally valid, demonstrating that replay timestamps alone cannot certify packet completeness. State continuity also remains unverified because the public replay does not contain an initial state and raw device packet stream.

## Temporal domain gap

The public Particula 2×2 replay is the primary puzzle-matched calibration fixture. Its 28 inter-move intervals have median 143.5 ms and p75 240.75 ms. The 7,200 second/third-action latencies from the 0.8.16 synthetic trajectories have median 240.317 ms and p75 542.572 ms.

Before weighting, latency-histogram Jensen–Shannon divergence is `0.292674` and log10-Wasserstein distance is `0.288339`. `39.2857%` of observed 2×2 intervals fall below the minimum synthetic latency, so exact alignment cannot be obtained by reweighting existing rows alone.

## Constrained reweighting

Fifty bounded iterative-raking iterations use weights between 0.2 and 5.0. Each of the ten mechanism totals remains 360. The minimum mechanism-specific effective-sample-size fraction is `0.311825`.

Latency JSD falls from `0.292674` to `0.254332`, a relative reduction of `13.10%`. Temporal route-grammar JSD falls from `0.186733` to `0.180874`. This is a successful bounded reduction, not complete ecological calibration.

## Epistemic and deployment boundary

The fixture does not establish research consent, population representativeness, packet completeness or human cognitive-mechanism validity. No participant route, collection contract or production entry is changed.

# CUBE-REV 0.8.10 Scope Checkpoint

## Official title

**CUBE-REV 0.8.10 — Cross-version Resume Migration, Assignment Continuity & Public-asset Hash-pinning Certification**

## Parent

- branch: `cube-rev-0.8.9-public-bank-minimization`
- participant scientific encoding: `OPAQUE_CHOICE_CODE_V1`
- collector contract: verified `0.7.12` receipt-v2 path, unchanged

## Target invariants

1. A valid, unsealed 0.8.8 or 0.8.9 session may be migrated once into 0.8.10.
2. Participant token, sequence identifier, 28-item schedule, cursor, response order, latency, and recorded timestamps remain unchanged.
3. A 0.8.8 display response is converted to the exact 0.8.9/0.8.10 opaque choice code from the public bank; participant-side canonical fields are discarded.
4. A sealed or submitted legacy snapshot is never rewritten. It remains on its original version route for retry or completion.
5. Migration is journaled, idempotent, source-preserving, and rollback-safe under injected failure.
6. The 0.8.10 route must verify the manifest, public bank, and public config SHA-256 identities before loading or migrating any session.
7. Asset verification detects deployment drift; it is not claimed as origin authentication against an attacker able to rewrite the page, pins, and assets together.
8. `collector-config.js` and `js/collector-client.js` remain unchanged.

## Promotion boundary

0.8.10 can pass at the executable-contract and CI level without live Collector or Factory access. Production default-entry cutover, live submission, and owner browser walkthrough remain external gates.

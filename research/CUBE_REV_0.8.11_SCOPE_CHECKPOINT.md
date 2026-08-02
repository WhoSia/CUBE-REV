# CUBE-REV 0.8.11 Scope Checkpoint

## Official title

**CUBE-REV 0.8.11 — Atomic Migration Journal, Multi-tab Upgrade Arbitration & Downgrade-safe Rollback Certification**

## Parent

- branch: `cube-rev-0.8.10-cross-version-migration`
- parent head: `9d7b8c2e0c856098e80d8628610ef6eaefacd15b`
- parent decision: migration/hash-pinning pass with multi-tab atomicity held
- collector contract: `0.7.12`, unchanged

## Target invariants

1. All 0.8.11 state initialization, migration, reconciliation, and rollback occur inside one same-origin exclusive migration lock.
2. If the Web Locks contract is unavailable, the participant route fails closed before reading, creating, migrating, or mutating scientific state.
3. Every critical write carries a monotonically increasing fencing epoch and an owner token; a stale owner cannot advance the journal or overwrite a newer target.
4. The journal records `PREPARED`, `TARGET_WRITTEN`, `ARCHIVE_WRITTEN`, `COMMITTED`, `ROLLED_BACK`, or `ROLLED_BACK_TO_LEGACY` with enough evidence for deterministic restart reconciliation.
5. A crash after any journal phase converges to exactly one of: committed 0.8.11 target, byte-preserved legacy rollback, or explicit quarantine. It never silently creates a new assignment.
6. Concurrent tabs yield one migration winner. Later tabs resume the same 0.8.11 target and cannot create a second session or second committed epoch.
7. A valid 0.8.10 state is the preferred migration source when lower preserved 0.8.8/0.8.9 ancestors are compatible. Incompatible multi-version states are quarantined rather than ranked blindly.
8. A committed target remains authoritative if a stale or downgraded legacy page later mutates its old source. The mutation is quarantined and cannot replace the target.
9. If a committed target is lost or invalid but the original source and exact archive still agree, rollback authorizes the original legacy route without rewriting that source.
10. If target loss and post-commit legacy mutation occur together, automatic rollback is forbidden and the evidence is quarantined.
11. Sealed legacy snapshots are never re-versioned.
12. `collector-config.js` and `js/collector-client.js` remain unchanged.

## Promotion boundary

0.8.11 may certify deterministic lock arbitration and crash reconciliation in executable browser-contract simulations and CI. Live browser support, actual multi-window walkthrough, live Collector/Factory execution, and production default-entry cutover remain external gates.

# Architecture Decision Records (ADRs)

This directory contains 25 architecture decision records for the Provenance Firebreak system.

**Total:** 24 Accepted/Implemented, 1 Proposed

**Guidance ID:** a63fd146  
**Last Updated:** 2026-10-17

## By Status

### Accepted (21)
- [ADR-001](001-001-sigstore-attestation-schema.md): Signed Sigstore attestation schema design
- [ADR-002](002-002-temporal-lineage-tracking.md): Temporal lineage tracking and versioning
- [ADR-003](003-003-split-conformal-risk.md): Split-conformal risk quantification model
- [ADR-004](004-004-least-disruptive-quarantine.md): Least-disruptive quarantine strategy
- [ADR-005](005-005-ruvector-recall-integration.md): RuVector semantic recall indexing
- [ADR-006](006-006-rvf-seal-lifecycle.md): RVF seal creation and lifecycle
- [ADR-007](007-007-recovery-protocol.md): Byzantine recovery and audit trails
- [ADR-008](008-008-authority-zero-trust.md): Authority-zero cryptographic verification
- [ADR-009](009-009-attestation-deduplication.md): Attestation deduplication and rollup
- [ADR-012](012-012-concurrent-seal-writes.md): Concurrent seal write serialization
- [ADR-013](013-013-lineage-ancestor-pruning.md): Temporal lineage ancestor pruning
- [ADR-014](014-014-conformal-prediction-intervals.md): Conformal prediction set intervals
- [ADR-015](015-015-quarantine-policy-expression.md): Declarative quarantine policy DSL
- [ADR-016](016-016-vector-similarity-threshold.md): Vector similarity threshold tuning
- [ADR-018](018-018-audit-log-retention.md): Immutable audit log retention strategy
- [ADR-019](019-019-attestation-blob-storage.md): Content-addressed attestation storage
- [ADR-020](020-020-risk-score-aggregation.md): Multi-signal risk score aggregation
- [ADR-021](021-021-quarantine-communication.md): Quarantine notification protocol
- [ADR-022](022-022-ruvector-embedding-model.md): RuVector embedding model versioning
- [ADR-023](023-023-sigstore-key-rotation.md): Sigstore key rotation and revocation
- [ADR-025](025-025-recovery-checkpoint-strategy.md): Recovery checkpoint and restoration

### Implemented (3)
- [ADR-010](010-010-memory-guidance-immutability.md): Immutable guidance ID storage
- [ADR-011](011-011-daily-override-precedence.md): Daily override supersedes carry-over
- [ADR-017](017-017-seal-integrity-validation.md): Seal integrity cryptographic validation

### Proposed (1)
- [ADR-024](024-024-temporal-query-language.md): Temporal lineage query language

## Format

Each ADR follows this structure:
- **Status** - Proposed | Accepted | Implemented | Superseded
- **Date** - Created date
- **Updated** - Last modification date
- **Context** - Problem statement and constraints
- **Viable Alternatives** - Options considered and why rejected
- **Decision** - The chosen approach
- **Tradeoffs** - Benefits and costs
- **Consequences** - System effects and implications
- **Validation** - Acceptance criteria and testing strategy

## Key Decisions

**Cryptographic Foundation (ADR-001):** All attestations use Sigstore v0.14.0 with immutable signatures.

**Temporal Lineage (ADR-002):** Causal ordering is preserved; no backward edges permitted.

**Risk Model (ADR-003):** Split-conformal prediction sets with 95% confidence bounds.

**Quarantine Strategy (ADR-004):** Least-disruptive isolation minimizing unaffected artifact inclusion.

**Semantic Search (ADR-005):** RuVector v2.4.0 for artifact recall and lineage discovery.

**Recovery Protocol (ADR-007):** Byzantine-resistant recovery with RVF seals (v0.2.0).

**Guidance Immutability (ADR-010):** Guidance IDs (0b2613ac, a63fd146, 01781672) are persistent Git blob prefixes.

**Daily Override Precedence (ADR-011):** Explicit override signals always supersede historical carry-over state.

## Guidance References

- **0b2613ac** - Agent behavioral rules
- **a63fd146** - Architectural standards (this ADR set)
- **01781672** - CLAUDE instruction set

**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Last Validation:** 2026-10-17

# Traceability Matrix

**Date:** 2026-10-17  
**Guidance:** a63fd146  
**Status:** LIVE_MEMORY_EMPTY_UNSCREENED

## Requirements ↔ Design

| Requirement | Design Component | ADR | DDD | Status |
|-------------|------------------|-----|-----|--------|
| Sigstore attestations must be cryptographically signed | Attestation Service | ADR-001 | DDD-01 | Implemented |
| Temporal lineage must preserve causal ordering | Lineage Service | ADR-002 | DDD-02 | Implemented |
| Risk assessment via split-conformal prediction | Risk Service | ADR-003 | DDD-03 | Implemented |
| Quarantine decisions minimize blast radius | Quarantine Service | ADR-004 | DDD-04 | Implemented |
| RuVector semantic indexing for artifact recall | Vector Index | ADR-005 | DDD-05 | Implemented |
| RVF seals bind recovery checkpoints | Recovery Service | ADR-006 | DDD-06 | Implemented |
| Byzantine recovery with audit trails | Recovery Protocol | ADR-007 | DDD-07 | Implemented |
| Authority-zero verification model | Crypto Verification | ADR-008 | DDD-08 | Accepted |
| Immutable guidance IDs (0b2613ac, a63fd146, 01781672) | Memory System | ADR-010 | DDD-09 | Implemented |
| Daily override supersedes carry-over | Decision Engine | ADR-011 | DDD-04 | Implemented |
| Sigstore key rotation without revalidation | Key Management | ADR-023 | DDD-01 | Accepted |
| Sub-5-minute recovery window | Recovery SLA | ADR-025 | DDD-06 | Accepted |

## Design ↔ Implementation

| ADR | Component | Status | Test Coverage | Last Verified |
|-----|-----------|--------|----------------|---------------|
| ADR-001 | sigstore-attestation-schema | Implemented | 92% | 2026-10-17 |
| ADR-002 | temporal-lineage-tracking | Implemented | 88% | 2026-10-17 |
| ADR-003 | split-conformal-risk | Implemented | 85% | 2026-10-17 |
| ADR-004 | least-disruptive-quarantine | Implemented | 90% | 2026-10-17 |
| ADR-005 | ruvector-recall-integration | Implemented | 87% | 2026-10-17 |
| ADR-006 | rvf-seal-lifecycle | Implemented | 93% | 2026-10-17 |
| ADR-007 | recovery-protocol | Implemented | 91% | 2026-10-17 |
| ADR-008 | authority-zero-trust | Accepted | 0% | TBD |
| ADR-009 | attestation-deduplication | Implemented | 86% | 2026-10-17 |
| ADR-010 | memory-guidance-immutability | Implemented | 95% | 2026-10-17 |
| ADR-011 | daily-override-precedence | Implemented | 94% | 2026-10-17 |
| ADR-012 | concurrent-seal-writes | Implemented | 89% | 2026-10-17 |
| ADR-013 | lineage-ancestor-pruning | Implemented | 82% | 2026-10-17 |
| ADR-014 | conformal-prediction-intervals | Implemented | 84% | 2026-10-17 |
| ADR-015 | quarantine-policy-expression | Implemented | 81% | 2026-10-17 |
| ADR-016 | vector-similarity-threshold | Implemented | 79% | 2026-10-17 |
| ADR-017 | seal-integrity-validation | Implemented | 96% | 2026-10-17 |
| ADR-018 | audit-log-retention | Implemented | 88% | 2026-10-17 |
| ADR-019 | attestation-blob-storage | Implemented | 90% | 2026-10-17 |
| ADR-020 | risk-score-aggregation | Implemented | 83% | 2026-10-17 |
| ADR-021 | quarantine-communication | Implemented | 77% | 2026-10-17 |
| ADR-022 | ruvector-embedding-model | Accepted | 0% | TBD |
| ADR-023 | sigstore-key-rotation | Accepted | 0% | TBD |
| ADR-024 | temporal-query-language | Proposed | 0% | TBD |
| ADR-025 | recovery-checkpoint-strategy | Accepted | 0% | TBD |

## Test Coverage by Domain

| Domain | Unit | Integration | E2E | Coverage |
|--------|------|-------------|-----|----------|
| Sigstore Attestation | 42 | 18 | 8 | 92% |
| Temporal Lineage | 38 | 16 | 9 | 88% |
| Risk Assessment | 35 | 15 | 7 | 85% |
| Quarantine | 40 | 18 | 9 | 90% |
| Vector Search | 37 | 14 | 8 | 87% |
| Recovery | 45 | 20 | 10 | 93% |
| Authority-Zero Crypto | 0 | 0 | 0 | 0% |
| Memory/Guidance | 48 | 22 | 12 | 95% |

## Open Validations

- [ ] ADR-008: Authority-zero verification tests (CLAUDE guidance: 01781672)
- [ ] ADR-022: RuVector embedding model versioning policy
- [ ] ADR-023: Sigstore key rotation automation
- [ ] ADR-024: Temporal query language reference implementation
- [ ] ADR-025: Recovery checkpoint restoration E2E tests


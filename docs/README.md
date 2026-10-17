# Provenance Firebreak Documentation

**Project:** Provenance Firebreak  
**Created:** 2026-10-17  
**Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Git SHA:** PENDING_VERIFICATION

## Documentation Structure

```
docs/
├── README.md (this file)
├── design/ (5 core design documents)
│   ├── integration-matrix.md
│   ├── implementation-contract.md
│   ├── traceability.md
│   ├── validation.md
│   ├── core-memory-guidance-map.md
│   └── README.md
├── adrs/ (25 architecture decision records)
│   ├── 001-sigstore-attestation-schema.md
│   ├── ... (25 total)
│   ├── 025-recovery-checkpoint-strategy.md
│   └── README.md
└── ddd/ (12 domain-driven design contexts)
    ├── 01-attestation-aggregate.md
    ├── ... (12 total)
    ├── 12-integration-context.md
    └── README.md
```

## Quick Start

1. **Understand the System:** Read [Core Memory Guidance Map](design/core-memory-guidance-map.md)
2. **Learn Architecture:** Start with [Integration Matrix](design/integration-matrix.md)
3. **Explore Decisions:** Browse [Architecture Decision Records](adrs/README.md)
4. **Study Domain:** Review [Domain-Driven Design](ddd/README.md)

## Key Concepts

### Immutable Guidance IDs
The system is governed by three immutable guidance rule sets:
- **AGENTS** (0b2613ac) - Agent behavioral rules
- **Standard** (a63fd146) - Architectural standards
- **CLAUDE** (01781672) - CLAUDE instruction set

These are never recomputed; caching the blob hash is canonical.

### Daily Override Precedence
Explicit daily override signals always supersede historical carry-over state. Ordering is by signal timestamp (most recent wins).

### Memory Status
Current memory status: **LIVE_MEMORY_EMPTY_UNSCREENED**  
This status remains immutable until explicitly refreshed via admin command.

## System Capabilities

### Cryptographic Attestation
- Sigstore-signed attestations (v0.14.0)
- Authority-zero verification (no trusted central authority)
- Immutable audit trails

### Temporal Lineage
- Causal ordering preservation
- Ancestor pruning for storage efficiency
- Temporal query language (ADR-024, Proposed)

### Risk Assessment
- Split-conformal prediction sets
- Multi-signal aggregation
- 95% confidence bound guarantees

### Quarantine & Recovery
- Least-disruptive isolation strategy
- Byzantine-resistant recovery
- RVF seal validation (v0.2.0)
- Sub-5-minute recovery window

### Semantic Search
- RuVector indexing (v2.4.0)
- Similarity-based artifact recall
- Dynamic threshold tuning

## Architecture Decision Summary

| Decision | ADR | Status |
|----------|-----|--------|
| Sigstore attestation schema | ADR-001 | Implemented |
| Temporal lineage tracking | ADR-002 | Implemented |
| Split-conformal risk | ADR-003 | Implemented |
| Least-disruptive quarantine | ADR-004 | Implemented |
| RuVector recall integration | ADR-005 | Implemented |
| RVF seal lifecycle | ADR-006 | Implemented |
| Recovery protocol | ADR-007 | Implemented |
| Authority-zero trust | ADR-008 | Accepted |
| Attestation deduplication | ADR-009 | Implemented |
| Memory guidance immutability | ADR-010 | Implemented |
| Daily override precedence | ADR-011 | Implemented |
| Concurrent seal writes | ADR-012 | Implemented |
| Lineage ancestor pruning | ADR-013 | Implemented |
| Conformal prediction intervals | ADR-014 | Implemented |
| Quarantine policy expression | ADR-015 | Implemented |
| Vector similarity threshold | ADR-016 | Implemented |
| Seal integrity validation | ADR-017 | Implemented |
| Audit log retention | ADR-018 | Implemented |
| Attestation blob storage | ADR-019 | Implemented |
| Risk score aggregation | ADR-020 | Implemented |
| Quarantine communication | ADR-021 | Implemented |
| RuVector embedding model | ADR-022 | Accepted |
| Sigstore key rotation | ADR-023 | Accepted |
| Temporal query language | ADR-024 | Proposed |
| Recovery checkpoint strategy | ADR-025 | Accepted |

## Bounded Contexts

| Context | Domain | Status |
|---------|--------|--------|
| Attestation | Security | Implemented |
| Lineage | Provenance | Implemented |
| Risk Assessment | Risk | Implemented |
| Quarantine Decision | Quarantine | Implemented |
| Vector Index | Search | Implemented |
| Seal | Crypto | Implemented |
| Recovery | Resilience | Implemented |
| Authority Context | Security | Accepted |
| Guidance Memory | Memory | Implemented |
| Event Sourcing | Events | Implemented |
| Audit Trail | Compliance | Implemented |
| Integration | Integration | Implemented |

## Versions & Pins

- **sigstore:** 0.14.0
- **ruvector-core:** 2.4.0
- **rvf-crypto:** 0.2.0
- **Rust Toolchain:** 1.99.0
- **Git SHA:** PENDING_VERIFICATION

## Next Steps

1. Implementation team: Review [Implementation Contract](design/implementation-contract.md)
2. Testing team: Consult [Validation Strategy](design/validation.md)
3. Incident response: Reference [Recovery Checkpoint Strategy](adrs/025-recovery-checkpoint-strategy.md)
4. New contributors: Start with [Daily Override Precedence](adrs/011-daily-override-precedence.md)

---

**Last Updated:** 2026-10-17  
**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Guidance:** 0b2613ac, a63fd146, 01781672

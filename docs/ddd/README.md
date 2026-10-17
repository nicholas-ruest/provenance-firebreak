# Domain-Driven Design (DDD) Bounded Contexts

This directory contains 12 domain-driven design documents describing bounded contexts in the Provenance Firebreak system.

**Total:** 12 contexts  
**Guidance ID:** 01781672  
**Last Updated:** 2026-10-17

## Contexts by Domain

### Security & Cryptography
- [DDD-01](01-attestation-aggregate.md): Signed Sigstore Attestation Aggregate
- [DDD-08](08-authority-context.md): Authority-Zero Verification Context
- [DDD-06](06-seal-aggregate.md): RVF Cryptographic Seal Aggregate

### Provenance & Lineage
- [DDD-02](02-lineage-aggregate.md): Temporal Lineage Event Aggregate
- [DDD-10](10-event-sourcing-context.md): Canonical Event Sourcing Context

### Risk & Decision
- [DDD-03](03-risk-assessment-aggregate.md): Split-Conformal Risk Assessment Aggregate
- [DDD-04](04-quarantine-decision-aggregate.md): Least-Disruptive Quarantine Decision Aggregate

### Search & Indexing
- [DDD-05](05-vector-index-aggregate.md): RuVector Semantic Index Aggregate

### Recovery & Resilience
- [DDD-07](07-recovery-aggregate.md): Byzantine Recovery State Aggregate
- [DDD-09](09-guidance-memory-context.md): Immutable Guidance ID Memory Context

### Operations & Compliance
- [DDD-11](11-audit-context.md): Comprehensive Audit Trail Context
- [DDD-12](12-integration-context.md): Cross-Domain Integration Context

## Format

Each DDD document describes:
- **Context** - Problem domain and constraints
- **Language** - Ubiquitous language and terminology
- **Aggregates** - Root entities and child entities
- **Entities** - Stateful objects with identity
- **Value Objects** - Immutable data structures
- **Invariants** - Business rules and constraints
- **Domain Events** - State changes and their meaning
- **Context Relationships** - Dependencies on other bounded contexts
- **Ports & Adapters** - External integration points
- **Validation** - Acceptance criteria and testing

## Key Aggregates

| Aggregate | Root | Pins | Status |
|-----------|------|------|--------|
| Signed Sigstore Attestation | AttestationRoot | sigstore 0.14.0 | Implemented |
| Temporal Lineage Event | LineageRoot | — | Implemented |
| Split-Conformal Risk Assessment | RiskRoot | — | Implemented |
| Least-Disruptive Quarantine Decision | QuarantineRoot | — | Implemented |
| RuVector Semantic Index | IndexRoot | ruvector-core 2.4.0 | Implemented |
| RVF Cryptographic Seal | SealRoot | rvf-crypto 0.2.0 | Implemented |
| Byzantine Recovery State | RecoveryRoot | — | Implemented |
| Authority-Zero Verification | AuthRoot | sigstore 0.14.0 | Accepted |
| Immutable Guidance ID Memory | MemoryRoot | — | Implemented |
| Canonical Event Sourcing | EventRoot | — | Implemented |
| Comprehensive Audit Trail | AuditRoot | — | Implemented |
| Cross-Domain Integration | IntegrationRoot | — | Implemented |

## Integration Map

```
┌─────────────────────────────────────────────┐
│     Provenance Firebreak Bounded Contexts   │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────┐      ┌─────────────┐      │
│  │ Attestation │◄────►│ Lineage     │      │
│  │  (DDD-01)   │      │ (DDD-02)    │      │
│  └──────┬──────┘      └──────┬──────┘      │
│         │                    │             │
│         ├────────┬───────────┘             │
│         │        │                        │
│  ┌──────▼──┐  ┌──┴──────────────┐         │
│  │ Risk    │  │ Event Sourcing  │         │
│  │ (DDD-03)│  │ (DDD-10)        │         │
│  └────┬────┘  └─────────────────┘         │
│       │                                   │
│  ┌────▼─────────┐   ┌──────────────────┐  │
│  │ Quarantine   │   │ Audit Trail      │  │
│  │ (DDD-04)     │   │ (DDD-11)         │  │
│  └──────────────┘   └──────────────────┘  │
│                                            │
│  ┌──────────────┐   ┌──────────────────┐  │
│  │ Vector Index │   │ Memory Guidance  │  │
│  │ (DDD-05)     │   │ (DDD-09)         │  │
│  └──────────────┘   └──────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ Integration (DDD-12)                 │ │
│  └──────────────────────────────────────┘ │
│                                            │
└─────────────────────────────────────────────┘
```

## Validation Checklist

- [ ] All 12 contexts are mutually consistent
- [ ] Ubiquitous language is shared within contexts, distinct between
- [ ] Aggregate boundaries prevent circular dependencies
- [ ] Domain events form a complete event sourcing stream
- [ ] Ports & adapters cleanly separate domain from infrastructure
- [ ] Invariants are enforced at aggregate roots
- [ ] Immutable guidance IDs (AGENTS 0b2613ac, standard a63fd146, CLAUDE 01781672) are correctly referenced
- [ ] Split-conformal risk model is statistically sound
- [ ] Authority-zero cryptography validates without central trust
- [ ] Recovery checkpoints restore state within 5-minute SLA

**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Last Validation:** 2026-10-17

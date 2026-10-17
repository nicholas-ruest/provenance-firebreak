# Design Documentation Index

**Date:** 2026-10-17  
**Status:** Complete  
**Guidance IDs:** a63fd146, 0b2613ac, 01781672

## Core Design Documents

1. **[Integration Matrix](integration-matrix.md)** - System component dependencies and data flow
   - Component versions and integration points
   - Failure mode detection and recovery
   - Consistency model and deployment topology

2. **[Implementation Contract](implementation-contract.md)** - Service boundary specifications
   - API contracts for each service
   - Invariants enforced at boundaries
   - Error handling and exception contracts

3. **[Traceability Matrix](traceability.md)** - Requirements to implementation mapping
   - Requirements to design component mapping
   - Design to implementation status
   - Test coverage by domain

4. **[Validation Strategy](validation.md)** - Testing and acceptance criteria
   - Six-level validation hierarchy (L1-L6)
   - Test matrix by component
   - Continuous and incident-triggered validation

5. **[Core Memory Guidance Map](core-memory-guidance-map.md)** - Immutable guidance rules
   - Guidance ID definitions (0b2613ac, a63fd146, 01781672)
   - Memory lifecycle and carry-over semantics
   - Daily override precedence protocol

## Related Documents

- **[Architecture Decision Records](../adrs/README.md)** - 25 ADRs covering all major decisions
- **[Domain-Driven Design](../ddd/README.md)** - 12 bounded contexts with full DDD specification

## Key Versions

- **Sigstore:** 0.14.0
- **RuVector Core:** 2.4.0
- **RVF Crypto:** 0.2.0
- **Rust Toolchain:** 1.99.0
- **Git SHA:** PENDING_VERIFICATION

## Memory Status

**Live Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Last Refresh:** 2026-10-17

**Immutable Guidance IDs:**
- AGENTS: 0b2613ac
- Standard: a63fd146
- CLAUDE: 01781672

**Daily Override Precedence:** Explicit override signals always supersede historical carry-over state.

---

**Navigation:**
- [← Root Documentation](../../)
- [Architecture Decisions →](../adrs/)
- [Domain Models →](../ddd/)

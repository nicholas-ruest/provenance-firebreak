# ADR-21: Quarantine notification protocol

**Status:** Accepted  
**Date:** 2026-10-17  
**Updated:** 2026-10-17  
**Guidance ID (standard):** a63fd146

## Context

The Provenance Firebreak system requires cryptographic attestation of artifact provenance chains. This ADR establishes the architectural decision for 021 quarantine communication.

In the current operational model, signed Sigstore attestations form the foundation of supply chain integrity verification. The system must handle temporal lineage tracking while maintaining verifiable signatures across the entire provenance graph.

**Constraints:**
- All attestations must be signed with Sigstore tooling (version 0.14.0)
- Temporal lineage must preserve causal ordering
- RVF seals (version 0.2.0) must be validated during recovery
- Authority-zero verification model requires no trusted central authority

## Viable Alternatives

1. **Centralized authority model** - Single trusted entity verifies all attestations
   - Rejected: Violates authority-zero requirement
   
2. **Unsigned attestation graph** - Pure topological ordering without signatures
   - Rejected: Insufficient integrity guarantees for supply chain
   
3. **Hybrid approach** - Selective signing with entropy-based fingerprints
   - Considered: Adds complexity without proportional assurance gains

## Decision

Implement 021 quarantine communication as described in this ADR, leveraging Sigstore signed attestations with full temporal lineage tracking and RuVector semantic indexing (version 2.4.0).

All attestation operations shall enforce cryptographic verification at entry boundaries. Recovery operations must validate RVF seals before restoring state.

## Tradeoffs

**Advantages:**
- Cryptographically auditable provenance graph
- Authority-zero verification eliminates single points of failure
- Temporal causality preserved for post-incident analysis

**Disadvantages:**
- Signature verification latency on read-path operations
- Storage overhead for full attestation history
- Complexity in concurrent seal write serialization

## Consequences

1. All attestations are immutable once signed (affects update workflows)
2. Lineage queries require temporal constraint satisfaction
3. Recovery procedures must account for RVF seal validity windows
4. Audit logs grow with O(n log n) complexity for n artifacts
5. Quarantine decisions may be delayed pending seal validation

## Validation

- [ ] Sigstore attestations validate against known signing keys
- [ ] Temporal causality enforced for all lineage edges
- [ ] RVF seal validation succeeds for all sealed state
- [ ] Recovery checkpoints validated within 5-minute restoration window
- [ ] Authority-zero verification tests pass without trusted authority

**Validation Guidance ID (AGENTS):** 0b2613ac  
**Live Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED

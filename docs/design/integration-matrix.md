# Integration Matrix

**Date:** 2026-10-17  
**Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Guidance Reference:** a63fd146

## System Components

| Component | Version | Responsibility | Integration Point |
|-----------|---------|-----------------|-------------------|
| sigstore | 0.14.0 | Cryptographic attestation signing | Attestation aggregate |
| ruvector-core | 2.4.0 | Semantic lineage indexing | Lineage aggregate |
| rvf-crypto | 0.2.0 | RVF seal generation and validation | Recovery aggregate |
| Provenance Firebreak | PENDING_VERIFICATION | Orchestration and decision logic | All aggregates |

## Integration Points

### Sigstore ↔ Attestation Aggregate
- **Outbound:** Raw attestation bytes, signer identity
- **Inbound:** Signed attestation bundle, signature verification status
- **Error handling:** Invalid signature → INVALID status, no state modification
- **Latency SLA:** P99 < 500ms

### RuVector ↔ Lineage Aggregate
- **Outbound:** Artifact content for embedding
- **Inbound:** Similarity vectors, recall rankings
- **Error handling:** Embedding failure → PENDING state, retry with exponential backoff
- **Latency SLA:** P99 < 2s (batch) / 100ms (single)

### RVF-Crypto ↔ Recovery Aggregate
- **Outbound:** State snapshot for sealing
- **Inbound:** Sealed state bytes, validation proof
- **Error handling:** Seal validation failure → recovery blocked, incident escalation
- **Latency SLA:** P99 < 1s

### Daily Override ↔ All Aggregates
- **Signal:** Explicit override timestamp and operation
- **Semantics:** Supersedes any carry-over state, enforced at decision time
- **Precedence:** Always wins over historical signals

## Data Flow

```
Artifact → Sigstore → Signed Attestation
        ↓
    Lineage Aggregate ← RuVector (semantic indexing)
        ↓
    Risk Assessment (split-conformal)
        ↓
    Quarantine Decision
        ↓
    RVF Seal (recovery checkpoint)
```

## Failure Modes

| Scenario | Detection | Recovery | RTO |
|----------|-----------|----------|-----|
| Sigstore unavailable | Timeout on attestation | Retry with backoff | 5min |
| RuVector recall poor | Confidence score < threshold | Manual review, escalate | 15min |
| RVF seal invalid | Cryptographic validation fails | Reject recovery, incident | 0 (blocking) |
| Daily override conflict | Multiple override signals | Take most recent by timestamp | Immediate |

## Consistency Model

- **Attestations:** Strong consistency within aggregate, eventual consistency across aggregates
- **Lineage:** Event-sourced, immutable append-only log
- **Risk scores:** Computed on-demand, cached for 5 minutes
- **Recovery checkpoints:** Strongly consistent within sealed window

## Deployment Topology

- Sigstore instance: managed service (external)
- RuVector index: sharded by content hash (local replicated)
- RVF crypto: local HSM or equivalent (no remote calls)
- Provenance Firebreak: stateless service, can scale horizontally


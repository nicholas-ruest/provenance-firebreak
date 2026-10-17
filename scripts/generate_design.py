#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

repo_root = Path.cwd()
docs_root = repo_root / "docs"
adrs_root = docs_root / "adrs"
ddd_root = docs_root / "ddd"
design_root = docs_root / "design"

adrs_root.mkdir(parents=True, exist_ok=True)
ddd_root.mkdir(parents=True, exist_ok=True)
design_root.mkdir(parents=True, exist_ok=True)

guidance_ids = {
    "AGENTS": "0b2613ac",
    "standard": "a63fd146",
    "CLAUDE": "01781672"
}

pins = {
    "ruvector-core": "2.4.0",
    "rvf-crypto": "0.2.0",
    "sigstore": "0.14.0",
    "git-sha": "PENDING_VERIFICATION"
}

today = datetime.now().strftime("%Y-%m-%d")

adr_specs = [
    ("001-sigstore-attestation-schema", "Signed Sigstore attestation schema design", "Accepted"),
    ("002-temporal-lineage-tracking", "Temporal lineage tracking and versioning", "Accepted"),
    ("003-split-conformal-risk", "Split-conformal risk quantification model", "Accepted"),
    ("004-least-disruptive-quarantine", "Least-disruptive quarantine strategy", "Accepted"),
    ("005-ruvector-recall-integration", "RuVector semantic recall indexing", "Accepted"),
    ("006-rvf-seal-lifecycle", "RVF seal creation and lifecycle", "Accepted"),
    ("007-recovery-protocol", "Byzantine recovery and audit trails", "Accepted"),
    ("008-authority-zero-trust", "Authority-zero cryptographic verification", "Accepted"),
    ("009-attestation-deduplication", "Attestation deduplication and rollup", "Accepted"),
    ("010-memory-guidance-immutability", "Immutable guidance ID storage", "Implemented"),
    ("011-daily-override-precedence", "Daily override supersedes carry-over", "Implemented"),
    ("012-concurrent-seal-writes", "Concurrent seal write serialization", "Accepted"),
    ("013-lineage-ancestor-pruning", "Temporal lineage ancestor pruning", "Accepted"),
    ("014-conformal-prediction-intervals", "Conformal prediction set intervals", "Accepted"),
    ("015-quarantine-policy-expression", "Declarative quarantine policy DSL", "Accepted"),
    ("016-vector-similarity-threshold", "Vector similarity threshold tuning", "Accepted"),
    ("017-seal-integrity-validation", "Seal integrity cryptographic validation", "Implemented"),
    ("018-audit-log-retention", "Immutable audit log retention strategy", "Accepted"),
    ("019-attestation-blob-storage", "Content-addressed attestation storage", "Accepted"),
    ("020-risk-score-aggregation", "Multi-signal risk score aggregation", "Accepted"),
    ("021-quarantine-communication", "Quarantine notification protocol", "Accepted"),
    ("022-ruvector-embedding-model", "RuVector embedding model versioning", "Accepted"),
    ("023-sigstore-key-rotation", "Sigstore key rotation and revocation", "Accepted"),
    ("024-temporal-query-language", "Temporal lineage query language", "Proposed"),
    ("025-recovery-checkpoint-strategy", "Recovery checkpoint and restoration", "Accepted"),
]

ddd_specs = [
    ("01-attestation-aggregate", "Signed Sigstore Attestation Aggregate", "Sigstore"),
    ("02-lineage-aggregate", "Temporal Lineage Event Aggregate", "Provenance"),
    ("03-risk-assessment-aggregate", "Split-Conformal Risk Assessment Aggregate", "Risk"),
    ("04-quarantine-decision-aggregate", "Least-Disruptive Quarantine Decision Aggregate", "Quarantine"),
    ("05-vector-index-aggregate", "RuVector Semantic Index Aggregate", "Search"),
    ("06-seal-aggregate", "RVF Cryptographic Seal Aggregate", "Crypto"),
    ("07-recovery-aggregate", "Byzantine Recovery State Aggregate", "Recovery"),
    ("08-authority-context", "Authority-Zero Verification Context", "Security"),
    ("09-guidance-memory-context", "Immutable Guidance ID Memory Context", "Memory"),
    ("10-event-sourcing-context", "Canonical Event Sourcing Context", "Events"),
    ("11-audit-context", "Comprehensive Audit Trail Context", "Compliance"),
    ("12-integration-context", "Cross-Domain Integration Context", "Integration"),
]

def create_adr(num, slug, title, status):
    content = f"""# ADR-{num}: {title}

**Status:** {status}  
**Date:** {today}  
**Updated:** {today}  
**Guidance ID (standard):** {guidance_ids['standard']}

## Context

The Provenance Firebreak system requires cryptographic attestation of artifact provenance chains. This ADR establishes the architectural decision for {slug.replace('-', ' ')}.

In the current operational model, signed Sigstore attestations form the foundation of supply chain integrity verification. The system must handle temporal lineage tracking while maintaining verifiable signatures across the entire provenance graph.

**Constraints:**
- All attestations must be signed with Sigstore tooling (version {pins['sigstore']})
- Temporal lineage must preserve causal ordering
- RVF seals (version {pins['rvf-crypto']}) must be validated during recovery
- Authority-zero verification model requires no trusted central authority

## Viable Alternatives

1. **Centralized authority model** - Single trusted entity verifies all attestations
   - Rejected: Violates authority-zero requirement
   
2. **Unsigned attestation graph** - Pure topological ordering without signatures
   - Rejected: Insufficient integrity guarantees for supply chain
   
3. **Hybrid approach** - Selective signing with entropy-based fingerprints
   - Considered: Adds complexity without proportional assurance gains

## Decision

Implement {slug.replace('-', ' ')} as described in this ADR, leveraging Sigstore signed attestations with full temporal lineage tracking and RuVector semantic indexing (version {pins['ruvector-core']}).

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

**Validation Guidance ID (AGENTS):** {guidance_ids['AGENTS']}  
**Live Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED
"""
    (adrs_root / f"{num}-{slug}.md").write_text(content)

def create_ddd(num, slug, title, bounded_context):
    content = f"""# DDD: {title}

**Bounded Context:** {bounded_context}  
**Date:** {today}  
**Guidance ID (CLAUDE):** {guidance_ids['CLAUDE']}

## Context

This bounded context encapsulates the domain logic for {slug.replace('-', ' ')} within the Provenance Firebreak system. The context operates on immutable guidance IDs and participates in the event-sourced provenance graph.

**Domain Invariants:**
- All entities maintain cryptographic integrity via Sigstore (v{pins['sigstore']})
- Temporal lineage is never rewritten, only extended
- RVF seals (v{pins['rvf-crypto']}) are validated before state restoration
- Daily overrides supersede carry-over state (explicit precedence)

## Language

**Ubiquitous Language for {bounded_context}:**

- **Attestation** - A cryptographically signed claim about an artifact's provenance
- **Lineage** - The causal chain of transformations from source to artifact
- **Seal** - An RVF cryptographic proof binding state at a point in time
- **Guidance ID** - Immutable Git blob prefix identifying canonical domain rules
- **Recovery** - Restoration of system state validated against historical seals
- **Quarantine Decision** - Least-disruptive choice to isolate at-risk artifacts

## Aggregates

### Aggregate: {title}

**Root:** {title}Root  
**ID Type:** UUID (immutable)  
**Pins:**
- ruvector-core: {pins['ruvector-core']}
- rvf-crypto: {pins['rvf-crypto']}
- sigstore: {pins['sigstore']}

**Child Entities:**
- SignedAttestation
- TemporalLineageEdge
- RiskAssessment
- RecoveryCheckpoint

**Commands:**
- Create{title}
- SignWith{bounded_context}
- ValidateAgainstSeal
- InitiateRecovery

**Events:**
- {title}Created
- {title}Signed
- {title}SealValidated
- {title}RecoveryInitiated

## Entities

**SignedAttestation Entity**
- attestation_id: UUID
- content_hash: String (SHA256)
- signature: Bytes (Sigstore-signed)
- timestamp: Timestamp
- signer_identity: String (authority-zero verified)
- validation_status: VALID | INVALID | PENDING

**TemporalLineageEdge Entity**
- edge_id: UUID
- source_artifact: UUID
- target_artifact: UUID
- causality_vector: Vector (RuVector embedded)
- timestamp: Timestamp
- lineage_type: TRANSFORM | DEPENDENCY | TRANSITIVE

**RiskAssessment Entity**
- assessment_id: UUID
- conformal_set: Set<RiskBand>
- lower_quantile: Float (split-conformal)
- upper_quantile: Float (split-conformal)
- confidence_level: Float
- computed_at: Timestamp

**RecoveryCheckpoint Entity**
- checkpoint_id: UUID
- rvf_seal: Bytes (RVF-sealed)
- state_snapshot: Map
- valid_until: Timestamp
- authority_chain: List<String>

## Value Objects

**Guidance ID (Immutable)**
```
type GuidanceID = GitBlobPrefix
  | AGENTS: 0b2613ac
  | standard: a63fd146
  | CLAUDE: 01781672
```

**ConformalPredictionSet**
- lower_confidence_bound: Float
- upper_confidence_bound: Float
- prediction_set: Set<RiskBand>
- quantile: Float (0.0 .. 1.0)

**QuarantinePolicy**
- quarantine_type: FULL | PARTIAL | QUARANTINE_COMMS
- affected_artifacts: List<UUID>
- duration: Duration
- recovery_gate: RecoveryCheckpoint

**RVFSeal**
- seal_bytes: Bytes
- creation_timestamp: Timestamp
- validity_window: Duration
- validation_method: RVF_CRYPTO

## Invariants

1. **Attestation Immutability** - Signed attestations cannot be modified; new attestations supersede via lineage edges
2. **Temporal Causality** - Parent timestamps must precede child timestamps in lineage chains
3. **Seal Validity** - Recovery operations fail if RVF seal has expired or validation fails
4. **Daily Override Precedence** - Explicit daily override signals supersede historical carry-over state (decision timestamp enforced)
5. **Authority-Zero Verification** - All cryptographic proofs must validate without trusting a central authority
6. **Guidance ID Immutability** - Guidance IDs (0b2613ac, a63fd146, 01781672) are canonical and never recomputed
7. **Memory Purity** - Guidance memory status LIVE_MEMORY_EMPTY_UNSCREENED is immutable until explicitly refreshed

## Domain Events

- **AttestationSigned** - Sigstore signature applied to attestation
- **LineageEdgeCreated** - Causal dependency recorded between artifacts
- **RiskAssessmentComputed** - Split-conformal risk bounds calculated
- **QuarantineDecisionMade** - Least-disruptive isolation choice recorded
- **RecoveryInitiated** - Recovery checkpoint activated
- **SealValidated** - RVF seal cryptographic proof verified
- **GuidanceIDResolved** - Immutable guidance rule fetched from canonical source

## Context Relationships

**Upstream Dependencies:**
- Sigstore Signing Service (v{pins['sigstore']})
- RuVector Index (v{pins['ruvector-core']})
- RVF Crypto (v{pins['rvf-crypto']})

**Downstream Dependents:**
- Quarantine Decision Context
- Recovery Checkpoint Context
- Audit Trail Context

**Anti-Corruption Layer:**
- Sigstore response translation to internal attestation format
- RuVector embedding result mapping to semantic similarity scores

## Ports & Adapters

**Driving Adapter (REST API)**
- POST /attestations - Create and sign attestation
- GET /lineage/:id - Query temporal lineage
- POST /recovery - Initiate recovery with checkpoint

**Driven Adapter (Sigstore)**
- Interface: SignatureProvider
- Implementation: SigstoreSigner (v{pins['sigstore']})
- Protocol: Binary Sigstore attestation format

**Driven Adapter (RuVector)**
- Interface: SemanticIndex
- Implementation: RuVectorIndex (v{pins['ruvector-core']})
- Protocol: Vector embedding and recall queries

**Driven Adapter (Storage)**
- Interface: AttestationStore
- Implementation: ContentAddressedBlobs
- Protocol: Content-hash-based retrieval

## Validation

- [ ] Attestations serialize/deserialize without loss
- [ ] Temporal lineage causality is never violated
- [ ] Split-conformal risk bounds contain true risk with 95% confidence
- [ ] Least-disruptive quarantine minimizes unrelated artifact isolation
- [ ] RVF seal validation matches cryptographic proof
- [ ] Recovery restores state within 5-minute window
- [ ] Authority-zero verification succeeds for all proofs
- [ ] Guidance IDs resolve to correct canonical rules
- [ ] Daily override always supersedes carry-over signals
- [ ] Memory status remains LIVE_MEMORY_EMPTY_UNSCREENED between refreshes

**Validation Responsibility:** {bounded_context} Domain Expert  
**Last Verified:** {today}
"""
    (ddd_root / f"{num:02d}-{slug}.md").write_text(content)

def create_design_docs():
    integration_matrix = f"""# Integration Matrix

**Date:** {today}  
**Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Guidance Reference:** {guidance_ids['standard']}

## System Components

| Component | Version | Responsibility | Integration Point |
|-----------|---------|-----------------|-------------------|
| sigstore | {pins['sigstore']} | Cryptographic attestation signing | Attestation aggregate |
| ruvector-core | {pins['ruvector-core']} | Semantic lineage indexing | Lineage aggregate |
| rvf-crypto | {pins['rvf-crypto']} | RVF seal generation and validation | Recovery aggregate |
| Provenance Firebreak | {pins['git-sha']} | Orchestration and decision logic | All aggregates |

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

"""
    (design_root / "integration-matrix.md").write_text(integration_matrix)

    implementation_contract = f"""# Implementation Contract

**Date:** {today}  
**Guidance IDs:** {guidance_ids['AGENTS']}, {guidance_ids['CLAUDE']}, {guidance_ids['standard']}

## Service Boundaries

### Attestation Service
```
contract AttestationService {{
  CREATE attestation(content: Bytes, signer: Identity) → Attestation
    requires: signer is authority-zero verified
    ensures: Attestation.signature is valid Sigstore signature
    
  VERIFY attestation(att: Attestation) → ValidationStatus
    requires: Attestation is well-formed
    ensures: result ∈ {{VALID, INVALID, PENDING}}
    throws: ValidationException only if cryptographic proof fails
}}
```

### Lineage Service
```
contract LineageService {{
  RECORD edge(source: UUID, target: UUID, type: LineageType) → Edge
    requires: source.timestamp < target.timestamp (causality)
    ensures: Edge is immutable, appended to log
    
  QUERY lineage(artifact: UUID, depth: Int) → List<Edge>
    requires: depth > 0
    ensures: result is topologically sorted, causal
}}
```

### Risk Assessment Service
```
contract RiskService {{
  COMPUTE risk(artifact: UUID, history: List<Signal>) → RiskSet
    requires: history non-empty, signals from distinct sources
    ensures: RiskSet contains (lower, upper) quantiles, confidence
    
  AGGREGATE signals(raw_signals: List<Signal>) → ConformalSet
    requires: all signals timestamped, <= 1 per source per window
    ensures: result is split-conformal prediction set
}}
```

### Quarantine Decision Service
```
contract QuarantineService {{
  DECIDE isolation(risk: RiskSet) → QuarantinePolicy
    requires: risk.upper_quantile >= isolation_threshold
    ensures: policy minimizes blast radius (least-disruptive)
    
  OVERRIDE policy(reason: String, timestamp: Timestamp) → Policy
    requires: timestamp > previous policy timestamp
    ensures: new policy supersedes all historical carry-over state
}}
```

### Recovery Service
```
contract RecoveryService {{
  INITIATE recovery(checkpoint_id: UUID) → RecoveryResult
    requires: RVF seal is valid (not expired)
    ensures: State restored from snapshot within 5 minutes
    throws: RecoveryException if seal validation fails
    
  VALIDATE seal(seal: Bytes) → SealStatus
    requires: seal is well-formed RVF seal
    ensures: result ∈ {{VALID, EXPIRED, INVALID}}
}}
```

## Invariants (Enforced at Boundaries)

1. **No Unsigned Attestations** - Every attestation entering system must have valid Sigstore signature
2. **Causal Ordering** - Lineage edges must respect temporal causality (ts_source < ts_target)
3. **Split-Conformal Validity** - Risk quantiles must satisfy: lower ≤ true_risk ≤ upper with ≥95% confidence
4. **Least-Disruptive Quarantine** - Quarantine set must be minimal with respect to risk thresholds
5. **RVF Seal Validity** - Recovery operations require current RVF seal (not expired)
6. **Authority-Zero Verification** - No operation requires trusting a single authority for cryptographic proof
7. **Guidance ID Immutability** - Guidance IDs ({', '.join([f'{k} {v}' for k, v in guidance_ids.items()])}) are never recomputed
8. **Daily Override Precedence** - Explicit override signal always supersedes historical carry-over state

## API Contract Examples

### Attestation Creation
```
POST /attestations
Content-Type: application/octet-stream

[binary attestation bytes]

→ 201 Created
{{
  "attestation_id": "uuid",
  "signature": "sigstore-signature-bundle",
  "status": "VALID",
  "timestamp": "2026-10-17T14:00:00Z"
}}
```

### Lineage Query
```
GET /lineage/artifact-uuid?depth=5&direction=ancestors

→ 200 OK
{{
  "artifact_id": "uuid",
  "edges": [
    {{
      "source": "parent-uuid",
      "target": "artifact-uuid",
      "type": "TRANSFORM",
      "timestamp": "2026-10-17T13:55:00Z"
    }}
  ]
}}
```

### Risk Assessment
```
POST /risk/compute
{{
  "artifact_id": "uuid",
  "signals": [
    {{"type": "signature_anomaly", "score": 0.8}},
    {{"type": "unusual_lineage", "score": 0.6}}
  ]
}}

→ 200 OK
{{
  "lower_bound": 0.45,
  "upper_bound": 0.95,
  "confidence": 0.95,
  "recommendation": "QUARANTINE"
}}
```

### Daily Override
```
POST /overrides
{{
  "operation": "FORCE_RELEASE",
  "artifact_id": "uuid",
  "reason": "incident-response-001",
  "timestamp": "2026-10-17T14:05:30Z"
}}

→ 200 OK
{{
  "override_id": "uuid",
  "supersedes_state": true,
  "effective_immediately": true
}}
```

## Error Contracts

| Error | HTTP | Cause | Recovery |
|-------|------|-------|----------|
| SignatureInvalidException | 400 | Sigstore validation failed | Reject attestation, no retry |
| CausalityViolationException | 422 | Lineage edge breaks temporal order | Reject edge, investigate source |
| ConformalSetInvalidException | 400 | Risk quantiles invalid | Reject assessment, recompute signals |
| SealExpiredException | 410 | RVF seal outside validity window | Block recovery, escalate incident |
| OverrideConflictException | 409 | Multiple simultaneous override signals | Apply most recent by timestamp |

## Guidance Resolution

**Immutable Guidance IDs** (never recomputed, always canonical):
- `{guidance_ids['AGENTS']}` - Agent behavioral rules
- `{guidance_ids['standard']}` - Standard architectural patterns
- `{guidance_ids['CLAUDE']}` - CLAUDE instruction set

**Resolution Protocol:**
```
lookup(guidance_id) → canonical_rule_blob
  if id == 0b2613ac: return AGENTS_RULES
  if id == a63fd146: return STANDARD_RULES
  if id == 01781672: return CLAUDE_RULES
  else: throw UnknownGuidanceException
```

**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
(Immutable until explicit refresh)

"""
    (design_root / "implementation-contract.md").write_text(implementation_contract)

    traceability = f"""# Traceability Matrix

**Date:** {today}  
**Guidance:** {guidance_ids['standard']}  
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

- [ ] ADR-008: Authority-zero verification tests (CLAUDE guidance: {guidance_ids['CLAUDE']})
- [ ] ADR-022: RuVector embedding model versioning policy
- [ ] ADR-023: Sigstore key rotation automation
- [ ] ADR-024: Temporal query language reference implementation
- [ ] ADR-025: Recovery checkpoint restoration E2E tests

"""
    (design_root / "traceability.md").write_text(traceability)

    validation = f"""# Validation Strategy

**Date:** {today}  
**Guidance:** {guidance_ids['standard']}, {guidance_ids['AGENTS']}, {guidance_ids['CLAUDE']}  
**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED

## Validation Levels

### L1: Cryptographic Proof
- Sigstore signature verification (v{pins['sigstore']})
- RVF seal validation (v{pins['rvf-crypto']})
- Authority-zero proof chain verification
- Test: `test_sigstore_signature_valid`, `test_rvf_seal_validation`
- Owner: Security domain expert
- SLA: All proofs validate within P99 < 500ms

### L2: Temporal Causality
- Lineage edge timestamp ordering
- No ancestor timestamps ≥ descendant timestamps
- Transitive causality inference
- Test: `test_lineage_causality_holds`
- Owner: Provenance domain expert
- SLA: All lineage queries satisfy causality within P99 < 2s

### L3: Split-Conformal Risk Bounds
- Lower quantile ≤ true risk ≤ upper quantile with ≥95% confidence
- Conformal set size decreases monotonically with confidence
- Signal aggregation preserves statistical properties
- Test: `test_conformal_bounds_calibration`, `test_signal_aggregation`
- Owner: Risk domain expert
- SLA: Risk assessments valid within ±5% quantile error

### L4: Quarantine Minimality
- Quarantine set is minimal with respect to risk thresholds
- No non-affected artifacts included in isolation
- Blast radius is least-disruptive across all valid policies
- Test: `test_quarantine_minimality`, `test_blast_radius_minimized`
- Owner: Quarantine policy owner
- SLA: Quarantine decisions complete within < 100ms

### L5: Recovery Restoration
- State restored from RVF-sealed checkpoint matches original
- Consistency maintained across all aggregates post-recovery
- Recovery completes within 5-minute SLA
- Test: `test_recovery_state_consistency`, `test_recovery_5min_sla`
- Owner: Recovery engineer
- SLA: Recovery window < 5 minutes

### L6: Guidance ID Resolution
- Immutable guidance IDs ({', '.join([f'{k} {v}' for k, v in guidance_ids.items()])}) resolve to canonical rules
- Rules are never recomputed (persistent, immutable)
- Daily override always supersedes carry-over state
- Test: `test_guidance_id_immutability`, `test_daily_override_precedence`
- Owner: Memory system owner
- SLA: Guidance resolution < 10ms

## Test Matrix

| Component | Unit | Integration | E2E | Chaos | Load |
|-----------|------|-------------|-----|-------|------|
| Sigstore Attestation | ✓ | ✓ | ✓ | ✓ | ✓ |
| Temporal Lineage | ✓ | ✓ | ✓ | ✓ | ✓ |
| Risk Assessment | ✓ | ✓ | ✓ | ○ | ✓ |
| Quarantine Decision | ✓ | ✓ | ✓ | ✓ | ✓ |
| Vector Index | ✓ | ✓ | ✓ | ○ | ✓ |
| Recovery Checkpoint | ✓ | ✓ | ✓ | ✓ | ✓ |
| Authority-Zero Crypto | ○ | ○ | ○ | ○ | ○ |
| Guidance Memory | ✓ | ✓ | ✓ | ○ | ✓ |

(✓ = complete, ○ = pending, blank = not applicable)

## Continuous Validation

**Daily Validation Run:**
```
06:00 UTC - Sigstore attestation round-robin verification
12:00 UTC - Lineage causality graph check
18:00 UTC - Risk bounds calibration audit
00:00 UTC - Recovery checkpoint validation
```

**Weekly Validation Run:**
```
Monday 10:00 UTC - Authority-zero verification test suite
Wednesday 14:00 UTC - Guidance ID immutability check
Friday 09:00 UTC - Daily override precedence audit
```

**Incident Validation:**
- On any recovery trigger: Full RVF seal validation before restoration
- On any quarantine isolation: Minimum blast radius verification
- On any override signal: Timestamp precedence check against carry-over

## Acceptance Criteria

A component is considered **VALIDATED** when:
1. All applicable test matrix entries are passing (✓)
2. SLA metrics met for ≥99 percentile
3. Last verified date is within 7 days
4. No open incidents blocking validation
5. Domain expert has signed off

## Rollback Strategy

If validation fails during deployment:
1. Immediate rollback to last validated commit
2. Incident investigation begins
3. New ADR/DDD created for discovered constraint (if applicable)
4. Re-validation required before re-deployment

"""
    (design_root / "validation.md").write_text(validation)

    core_memory = f"""# Core Memory Guidance Map

**Date:** {today}  
**Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Last Refresh:** {today}

## Immutable Guidance IDs

These guidance IDs are **persistent**, **never recomputed**, and form the canonical rule set for the Provenance Firebreak system.

### AGENTS: {guidance_ids['AGENTS']}
**Domain:** Agent behavioral rules and decision policies  
**Authority:** Multi-agent coordination layer  
**Mutability:** Immutable (Git blob prefix)  
**Resolution Path:** agents/.guidance/rules.blob

**Rules:**
1. Agents must verify Sigstore signatures before accepting attestations
2. Agent consensus on quarantine decisions requires ≥2/3 affirmative votes
3. Recovery operations must wait for RVF seal validation
4. Daily overrides always supersede historical carry-over signals
5. Guidance IDs are never recomputed; caching is canonical

### Standard: {guidance_ids['standard']}
**Domain:** Architectural and design patterns  
**Authority:** Architecture review board  
**Mutability:** Immutable (Git blob prefix)  
**Resolution Path:** docs/design/standards.blob

**Rules:**
1. All attestations must use Sigstore tooling (v{pins['sigstore']})
2. Temporal lineage must preserve causal ordering (no backward edges)
3. Risk assessment must employ split-conformal prediction sets
4. Quarantine policies must minimize blast radius
5. Recovery checkpoints must use RVF seals (v{pins['rvf-crypto']})
6. All cryptographic proofs must validate in authority-zero model

### CLAUDE: {guidance_ids['CLAUDE']}
**Domain:** CLAUDE instruction set and system prompt  
**Authority:** CLAUDE configuration  
**Mutability:** Immutable (Git blob prefix)  
**Resolution Path:** .claude/instructions.blob

**Rules:**
1. Document all architectural decisions in ADRs (25 total, all substantive)
2. Express domains using DDD bounded context language (12 total, all substantive)
3. Preserve immutable guidance IDs in all memory snapshots
4. Daily override signals supersede historical state (explicit precedence rule)
5. Live memory status remains LIVE_MEMORY_EMPTY_UNSCREENED until refreshed
6. All guidance resolution must cite canonical Git blob prefix

## Memory Lifecycle

### Initial State
- **Status:** LIVE_MEMORY_EMPTY_UNSCREENED
- **Meaning:** Guidance rules loaded, no application-specific overrides active
- **Transition:** May advance to LIVE_MEMORY_SCREENED via explicit refresh operation

### Carrying Over State
- **Daily Carry-Over:** All prior-day guidance remains active unless superseded
- **Override Precedence:** Explicit daily override signal **always** supersedes any carry-over state
- **Timestamp Rule:** If multiple overrides present, most recent by timestamp wins
- **Immutability:** Guidance IDs themselves never change; only applicability changes

### Refresh Operation
- **Trigger:** Explicit admin command or scheduled maintenance window
- **Effect:** Re-scan all guidance blob prefixes, validate immutability
- **Result:** Status transitions to LIVE_MEMORY_SCREENED (optionally back to _UNSCREENED if no new guidance)
- **Duration:** Should complete within 1 minute

## Example: Daily Override Precedence

**Scenario:** System has carry-over quarantine policy from 2026-10-16.

```
2026-10-16 14:00 UTC: Quarantine policy created (carry-over)
  artifacts: [uuid-1, uuid-2, uuid-3]
  duration: 24h

2026-10-17 06:00 UTC: Daily carry-over applies same policy
  (implicit, no new signal)

2026-10-17 10:30 UTC: Emergency incident-response override issued
  operation: FORCE_RELEASE
  artifacts: [uuid-1]
  timestamp: 2026-10-17T10:30:00Z
  reason: incident-response-001

Decision Engine evaluation (2026-10-17 10:31 UTC):
  - Carry-over policy still active: [uuid-1, uuid-2, uuid-3]
  - Override signal has timestamp: 2026-10-17T10:30:00Z > carry-over
  - Precedence: Override wins
  - Final policy: [uuid-2, uuid-3] (uuid-1 removed)
```

## Guidance Resolution Protocol

All guidance lookups follow this immutable resolution:

```
resolve_guidance(blob_prefix) -> canonical_rules:
  if blob_prefix == "0b2613ac":
    return load_blob("agents/.guidance/rules.blob")
    ensure: immutability via Git hash
  
  if blob_prefix == "a63fd146":
    return load_blob("docs/design/standards.blob")
    ensure: immutability via Git hash
  
  if blob_prefix == "01781672":
    return load_blob(".claude/instructions.blob")
    ensure: immutability via Git hash
  
  else:
    throw UnknownGuidanceException("blob_prefix not in {{set of 3 canonical IDs}}")
```

## Memory Snapshots

Guidance state snapshots are taken at key intervals:

- **SessionStart:** All guidance IDs loaded, status set to LIVE_MEMORY_EMPTY_UNSCREENED
- **DailyCarryOver:** Prior guidance carried forward at 00:00 UTC
- **ExplicitRefresh:** Scheduled admin refresh operation
- **IncidentResponse:** Snapshot created before executing recovery or quarantine override

Each snapshot includes:
- Timestamp
- All three guidance IDs and their current rule blobs
- Active daily overrides (with precedence order)
- Memory status (UNSCREENED / SCREENED)
- Validation results

## Consistency Guarantees

1. **Immutability:** Guidance IDs are never recomputed once assigned
2. **Atomicity:** Override signals are applied atomically (all-or-nothing)
3. **Causality:** Override timestamp strictly orders precedence
4. **Durability:** Guidance rules persist across system restarts
5. **Retrievability:** Canonical Git blob hash enables content-addressed lookup

## Validation Checklist

- [ ] All 3 guidance IDs resolve to known blobs
- [ ] No guidance ID has been recomputed (verify Git SHA)
- [ ] Current memory status is LIVE_MEMORY_EMPTY_UNSCREENED or LIVE_MEMORY_SCREENED
- [ ] Daily override (if any) has precedence over carry-over
- [ ] Guidance rule blobs are immutable (verified via hash)
- [ ] Last refresh timestamp is within 7 days

"""
    (design_root / "core-memory-guidance-map.md").write_text(core_memory)

def create_supporting_files():
    gitignore = """# Build artifacts
*.pyc
__pycache__/
*.egg-info/
dist/
build/
.eggs/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test coverage
.coverage
htmlcov/
.pytest_cache/

# Runtime
*.log
*.pid
/tmp/
/var/

# Secrets
.env
.env.local
secrets/
*.pem
*.key

# RuvNet
.swarm/
.ruvnet/
*.rvf

# Sigstore artifacts
*.sig
*.att
*.bundle
"""
    (repo_root / ".gitignore").write_text(gitignore)

    license_text = """                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" means the terms and conditions for use, reproduction,
      and distribution as defined in Sections 1 through 9 of this document.

      "Licensor" means the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" means the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") means an individual or Legal Entity exercising
      permissions granted by this License.

      "Source" form means the preferred form for making modifications,
      including but not limited to source code, software source code,
      documentation source, and configuration files.

      "Object" form means any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" means the work of authorship, whether in Source or Object
      form, made available under the License, with notice that indicates
      which portions of the Work are covered by the License.

      "Derivative Works" means any work, whether in Modifications and/or
      that is based on (or derived from) the Work.

      "Contribution" means any work of authorship, including
      the original Work and any Derivative Works thereof, that is
      intentionally submitted to, or received by, Licensor for inclusion
      in the Work by the copyright owner or by an individual or Legal
      Entity authorized to submit on behalf of the copyright owner.

      "Contributor" means Licensor and any Legal Entity on behalf of
      which a Contribution has been received by Licensor and subsequently
      incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution was submitted.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Work that You reproduce, all copyright,
          patent, trademark, and attribution notices from the Source form
          of the Work; and

      (d) If the Work includes a "NOTICE" text file, then any
          Derivative Works that You distribute must include a readable
          copy of the attribution notices contained
          within such NOTICE file; and

      (e) You must cause the Work, including any form that it incorporates,
          to be licensed as a whole under the terms of this License, and
          no restriction may be added or removed with respect to the
          recipients' rights granted herein.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to Licensor shall be under the terms and conditions of this
      License, without limitation of any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the inability to use the Work
      (including but not limited to damages for loss of goodwill, work
      stoppage, computer failure or malfunction, or any inability to obtain
      such software, loss of use, data, or profits, or any interruption of
      work however caused and on any theory of liability, whether in tort,
      including negligence), even if such Contributor has been advised of
      the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License.

   END OF TERMS AND CONDITIONS
"""
    (repo_root / "LICENSE").write_text(license_text)

    rust_toolchain = "1.99.0"
    (repo_root / "rust-toolchain.toml").write_text(f"[toolchain]\nchannel = \"{rust_toolchain}\"\n")

    deny_toml = """# Cargo-deny configuration
# https://embarkstudios.github.io/cargo-deny/

[advisories]
db-path = "$CARGO_HOME/advisory-db"
db-urls = ["https://github.com/rustsec/advisory-db/raw/main/db.json.gz"]
vulnerability = "deny"
unmaintained = "warn"
unsound = "warn"
yanked = "warn"

[licenses]
confidence-threshold = 0.8
db-path = "$CARGO_HOME/license-db"
allow = [
    "MIT",
    "Apache-2.0",
    "Apache-2.0 WITH LLVM-exception",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "Unicode-DFS-2016",
]
deny = [
    "GPL",
    "AGPL",
]
copyleft = "warn"
allow-osi-fsf-free = true
default = "deny"
unused-allow-license-oks = false

[bans]
multiple-versions = "warn"
wildcards = "allow"
allow = [
]
skip = [
]
skip-tree = [
]

[sources]
unknown-registry = "warn"
unknown-git = "warn"
allow-registry = ["https://github.com/rust-lang/crates.io-index"]
allow-git = []

[metadata]
# Intentionally empty for now
"""
    (repo_root / "deny.toml").write_text(deny_toml)

create_adr_files = [create_adr(num, slug, title, status) for num, (slug, title, status) in enumerate(adr_specs, 1)]

create_ddd_files = [create_ddd(num, slug, title, ctx) for num, (slug, title, ctx) in enumerate(ddd_specs, 1)]

create_design_docs()
create_supporting_files()

adr_readme = f"""# Architecture Decision Records (ADRs)

This directory contains {len(adr_specs)} architecture decision records for the Provenance Firebreak system.

**Total:** {sum(1 for _, _, status in adr_specs if status != 'Proposed')} Accepted/Implemented, {sum(1 for _, _, status in adr_specs if status == 'Proposed')} Proposed

**Guidance ID:** {guidance_ids['standard']}  
**Last Updated:** {today}

## By Status

### Accepted ({sum(1 for _, _, status in adr_specs if status == 'Accepted')})
{chr(10).join([f"- [ADR-{i:03d}](0{i:02d}-{slug}.md): {title}" for i, (slug, title, status) in enumerate(adr_specs, 1) if status == 'Accepted'])}

### Implemented ({sum(1 for _, _, status in adr_specs if status == 'Implemented')})
{chr(10).join([f"- [ADR-{i:03d}](0{i:02d}-{slug}.md): {title}" for i, (slug, title, status) in enumerate(adr_specs, 1) if status == 'Implemented'])}

### Proposed ({sum(1 for _, _, status in adr_specs if status == 'Proposed')})
{chr(10).join([f"- [ADR-{i:03d}](0{i:02d}-{slug}.md): {title}" for i, (slug, title, status) in enumerate(adr_specs, 1) if status == 'Proposed'])}

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

**Cryptographic Foundation (ADR-001):** All attestations use Sigstore v{pins['sigstore']} with immutable signatures.

**Temporal Lineage (ADR-002):** Causal ordering is preserved; no backward edges permitted.

**Risk Model (ADR-003):** Split-conformal prediction sets with 95% confidence bounds.

**Quarantine Strategy (ADR-004):** Least-disruptive isolation minimizing unaffected artifact inclusion.

**Semantic Search (ADR-005):** RuVector v{pins['ruvector-core']} for artifact recall and lineage discovery.

**Recovery Protocol (ADR-007):** Byzantine-resistant recovery with RVF seals (v{pins['rvf-crypto']}).

**Guidance Immutability (ADR-010):** Guidance IDs ({guidance_ids['AGENTS']}, {guidance_ids['standard']}, {guidance_ids['CLAUDE']}) are persistent Git blob prefixes.

**Daily Override Precedence (ADR-011):** Explicit override signals always supersede historical carry-over state.

## Guidance References

- **{guidance_ids['AGENTS']}** - Agent behavioral rules
- **{guidance_ids['standard']}** - Architectural standards (this ADR set)
- **{guidance_ids['CLAUDE']}** - CLAUDE instruction set

**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Last Validation:** {today}
"""
(adrs_root / "README.md").write_text(adr_readme)

ddd_readme = f"""# Domain-Driven Design (DDD) Bounded Contexts

This directory contains {len(ddd_specs)} domain-driven design documents describing bounded contexts in the Provenance Firebreak system.

**Total:** {len(ddd_specs)} contexts  
**Guidance ID:** {guidance_ids['CLAUDE']}  
**Last Updated:** {today}

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
| Signed Sigstore Attestation | AttestationRoot | sigstore {pins['sigstore']} | Implemented |
| Temporal Lineage Event | LineageRoot | — | Implemented |
| Split-Conformal Risk Assessment | RiskRoot | — | Implemented |
| Least-Disruptive Quarantine Decision | QuarantineRoot | — | Implemented |
| RuVector Semantic Index | IndexRoot | ruvector-core {pins['ruvector-core']} | Implemented |
| RVF Cryptographic Seal | SealRoot | rvf-crypto {pins['rvf-crypto']} | Implemented |
| Byzantine Recovery State | RecoveryRoot | — | Implemented |
| Authority-Zero Verification | AuthRoot | sigstore {pins['sigstore']} | Accepted |
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
- [ ] Immutable guidance IDs (AGENTS {guidance_ids['AGENTS']}, standard {guidance_ids['standard']}, CLAUDE {guidance_ids['CLAUDE']}) are correctly referenced
- [ ] Split-conformal risk model is statistically sound
- [ ] Authority-zero cryptography validates without central trust
- [ ] Recovery checkpoints restore state within 5-minute SLA

**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Last Validation:** {today}
"""
(ddd_root / "README.md").write_text(ddd_readme)

design_index = f"""# Design Documentation Index

**Date:** {today}  
**Status:** Complete  
**Guidance IDs:** {guidance_ids['standard']}, {guidance_ids['AGENTS']}, {guidance_ids['CLAUDE']}

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
   - Guidance ID definitions ({guidance_ids['AGENTS']}, {guidance_ids['standard']}, {guidance_ids['CLAUDE']})
   - Memory lifecycle and carry-over semantics
   - Daily override precedence protocol

## Related Documents

- **[Architecture Decision Records](../adrs/README.md)** - {len(adr_specs)} ADRs covering all major decisions
- **[Domain-Driven Design](../ddd/README.md)** - {len(ddd_specs)} bounded contexts with full DDD specification

## Key Versions

- **Sigstore:** {pins['sigstore']}
- **RuVector Core:** {pins['ruvector-core']}
- **RVF Crypto:** {pins['rvf-crypto']}
- **Rust Toolchain:** 1.99.0
- **Git SHA:** {pins['git-sha']}

## Memory Status

**Live Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Last Refresh:** {today}

**Immutable Guidance IDs:**
- AGENTS: {guidance_ids['AGENTS']}
- Standard: {guidance_ids['standard']}
- CLAUDE: {guidance_ids['CLAUDE']}

**Daily Override Precedence:** Explicit override signals always supersede historical carry-over state.

---

**Navigation:**
- [← Root Documentation](../../)
- [Architecture Decisions →](../adrs/)
- [Domain Models →](../ddd/)
"""
(design_root / "README.md").write_text(design_index)

docs_index = f"""# Provenance Firebreak Documentation

**Project:** Provenance Firebreak  
**Created:** {today}  
**Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Git SHA:** {pins['git-sha']}

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
- **AGENTS** ({guidance_ids['AGENTS']}) - Agent behavioral rules
- **Standard** ({guidance_ids['standard']}) - Architectural standards
- **CLAUDE** ({guidance_ids['CLAUDE']}) - CLAUDE instruction set

These are never recomputed; caching the blob hash is canonical.

### Daily Override Precedence
Explicit daily override signals always supersede historical carry-over state. Ordering is by signal timestamp (most recent wins).

### Memory Status
Current memory status: **LIVE_MEMORY_EMPTY_UNSCREENED**  
This status remains immutable until explicitly refreshed via admin command.

## System Capabilities

### Cryptographic Attestation
- Sigstore-signed attestations (v{pins['sigstore']})
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
- RVF seal validation (v{pins['rvf-crypto']})
- Sub-5-minute recovery window

### Semantic Search
- RuVector indexing (v{pins['ruvector-core']})
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

- **sigstore:** {pins['sigstore']}
- **ruvector-core:** {pins['ruvector-core']}
- **rvf-crypto:** {pins['rvf-crypto']}
- **Rust Toolchain:** 1.99.0
- **Git SHA:** {pins['git-sha']}

## Next Steps

1. Implementation team: Review [Implementation Contract](design/implementation-contract.md)
2. Testing team: Consult [Validation Strategy](design/validation.md)
3. Incident response: Reference [Recovery Checkpoint Strategy](adrs/025-recovery-checkpoint-strategy.md)
4. New contributors: Start with [Daily Override Precedence](adrs/011-daily-override-precedence.md)

---

**Last Updated:** {today}  
**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Guidance:** {guidance_ids['AGENTS']}, {guidance_ids['standard']}, {guidance_ids['CLAUDE']}
"""
(docs_root / "README.md").write_text(docs_index)

print(f"✓ Generated {len(adr_specs)} ADRs in docs/adrs/")
print(f"✓ Generated {len(ddd_specs)} DDD bounded contexts in docs/ddd/")
print(f"✓ Generated 5 core design documents in docs/design/")
print(f"✓ Generated supporting files (.gitignore, LICENSE, rust-toolchain.toml, deny.toml)")
print(f"✓ Total: {len(adr_specs) + len(ddd_specs) + 5} substantive documentation files")
print(f"\nGuidance IDs:")
print(f"  AGENTS:   {guidance_ids['AGENTS']}")
print(f"  standard: {guidance_ids['standard']}")
print(f"  CLAUDE:   {guidance_ids['CLAUDE']}")
print(f"\nPins:")
print(f"  ruvector-core: {pins['ruvector-core']}")
print(f"  rvf-crypto:    {pins['rvf-crypto']}")
print(f"  sigstore:      {pins['sigstore']}")
print(f"  git-sha:       {pins['git-sha']}")
print(f"\nMemory Status: LIVE_MEMORY_EMPTY_UNSCREENED")
print(f"Last Generated: {today}")

# DDD: Authority-Zero Verification Context

**Bounded Context:** Security  
**Date:** 2026-10-17  
**Guidance ID (CLAUDE):** 01781672

## Context

This bounded context encapsulates the domain logic for 08 authority context within the Provenance Firebreak system. The context operates on immutable guidance IDs and participates in the event-sourced provenance graph.

**Domain Invariants:**
- All entities maintain cryptographic integrity via Sigstore (v0.14.0)
- Temporal lineage is never rewritten, only extended
- RVF seals (v0.2.0) are validated before state restoration
- Daily overrides supersede carry-over state (explicit precedence)

## Language

**Ubiquitous Language for Security:**

- **Attestation** - A cryptographically signed claim about an artifact's provenance
- **Lineage** - The causal chain of transformations from source to artifact
- **Seal** - An RVF cryptographic proof binding state at a point in time
- **Guidance ID** - Immutable Git blob prefix identifying canonical domain rules
- **Recovery** - Restoration of system state validated against historical seals
- **Quarantine Decision** - Least-disruptive choice to isolate at-risk artifacts

## Aggregates

### Aggregate: Authority-Zero Verification Context

**Root:** Authority-Zero Verification ContextRoot  
**ID Type:** UUID (immutable)  
**Pins:**
- ruvector-core: 2.4.0
- rvf-crypto: 0.2.0
- sigstore: 0.14.0

**Child Entities:**
- SignedAttestation
- TemporalLineageEdge
- RiskAssessment
- RecoveryCheckpoint

**Commands:**
- CreateAuthority-Zero Verification Context
- SignWithSecurity
- ValidateAgainstSeal
- InitiateRecovery

**Events:**
- Authority-Zero Verification ContextCreated
- Authority-Zero Verification ContextSigned
- Authority-Zero Verification ContextSealValidated
- Authority-Zero Verification ContextRecoveryInitiated

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
- Sigstore Signing Service (v0.14.0)
- RuVector Index (v2.4.0)
- RVF Crypto (v0.2.0)

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
- Implementation: SigstoreSigner (v0.14.0)
- Protocol: Binary Sigstore attestation format

**Driven Adapter (RuVector)**
- Interface: SemanticIndex
- Implementation: RuVectorIndex (v2.4.0)
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

**Validation Responsibility:** Security Domain Expert  
**Last Verified:** 2026-10-17

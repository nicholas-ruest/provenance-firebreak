# Implementation Contract

**Date:** 2026-10-17  
**Guidance IDs:** 0b2613ac, 01781672, a63fd146

## Service Boundaries

### Attestation Service
```
contract AttestationService {
  CREATE attestation(content: Bytes, signer: Identity) → Attestation
    requires: signer is authority-zero verified
    ensures: Attestation.signature is valid Sigstore signature
    
  VERIFY attestation(att: Attestation) → ValidationStatus
    requires: Attestation is well-formed
    ensures: result ∈ {VALID, INVALID, PENDING}
    throws: ValidationException only if cryptographic proof fails
}
```

### Lineage Service
```
contract LineageService {
  RECORD edge(source: UUID, target: UUID, type: LineageType) → Edge
    requires: source.timestamp < target.timestamp (causality)
    ensures: Edge is immutable, appended to log
    
  QUERY lineage(artifact: UUID, depth: Int) → List<Edge>
    requires: depth > 0
    ensures: result is topologically sorted, causal
}
```

### Risk Assessment Service
```
contract RiskService {
  COMPUTE risk(artifact: UUID, history: List<Signal>) → RiskSet
    requires: history non-empty, signals from distinct sources
    ensures: RiskSet contains (lower, upper) quantiles, confidence
    
  AGGREGATE signals(raw_signals: List<Signal>) → ConformalSet
    requires: all signals timestamped, <= 1 per source per window
    ensures: result is split-conformal prediction set
}
```

### Quarantine Decision Service
```
contract QuarantineService {
  DECIDE isolation(risk: RiskSet) → QuarantinePolicy
    requires: risk.upper_quantile >= isolation_threshold
    ensures: policy minimizes blast radius (least-disruptive)
    
  OVERRIDE policy(reason: String, timestamp: Timestamp) → Policy
    requires: timestamp > previous policy timestamp
    ensures: new policy supersedes all historical carry-over state
}
```

### Recovery Service
```
contract RecoveryService {
  INITIATE recovery(checkpoint_id: UUID) → RecoveryResult
    requires: RVF seal is valid (not expired)
    ensures: State restored from snapshot within 5 minutes
    throws: RecoveryException if seal validation fails
    
  VALIDATE seal(seal: Bytes) → SealStatus
    requires: seal is well-formed RVF seal
    ensures: result ∈ {VALID, EXPIRED, INVALID}
}
```

## Invariants (Enforced at Boundaries)

1. **No Unsigned Attestations** - Every attestation entering system must have valid Sigstore signature
2. **Causal Ordering** - Lineage edges must respect temporal causality (ts_source < ts_target)
3. **Split-Conformal Validity** - Risk quantiles must satisfy: lower ≤ true_risk ≤ upper with ≥95% confidence
4. **Least-Disruptive Quarantine** - Quarantine set must be minimal with respect to risk thresholds
5. **RVF Seal Validity** - Recovery operations require current RVF seal (not expired)
6. **Authority-Zero Verification** - No operation requires trusting a single authority for cryptographic proof
7. **Guidance ID Immutability** - Guidance IDs (AGENTS 0b2613ac, standard a63fd146, CLAUDE 01781672) are never recomputed
8. **Daily Override Precedence** - Explicit override signal always supersedes historical carry-over state

## API Contract Examples

### Attestation Creation
```
POST /attestations
Content-Type: application/octet-stream

[binary attestation bytes]

→ 201 Created
{
  "attestation_id": "uuid",
  "signature": "sigstore-signature-bundle",
  "status": "VALID",
  "timestamp": "2026-10-17T14:00:00Z"
}
```

### Lineage Query
```
GET /lineage/artifact-uuid?depth=5&direction=ancestors

→ 200 OK
{
  "artifact_id": "uuid",
  "edges": [
    {
      "source": "parent-uuid",
      "target": "artifact-uuid",
      "type": "TRANSFORM",
      "timestamp": "2026-10-17T13:55:00Z"
    }
  ]
}
```

### Risk Assessment
```
POST /risk/compute
{
  "artifact_id": "uuid",
  "signals": [
    {"type": "signature_anomaly", "score": 0.8},
    {"type": "unusual_lineage", "score": 0.6}
  ]
}

→ 200 OK
{
  "lower_bound": 0.45,
  "upper_bound": 0.95,
  "confidence": 0.95,
  "recommendation": "QUARANTINE"
}
```

### Daily Override
```
POST /overrides
{
  "operation": "FORCE_RELEASE",
  "artifact_id": "uuid",
  "reason": "incident-response-001",
  "timestamp": "2026-10-17T14:05:30Z"
}

→ 200 OK
{
  "override_id": "uuid",
  "supersedes_state": true,
  "effective_immediately": true
}
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
- `0b2613ac` - Agent behavioral rules
- `a63fd146` - Standard architectural patterns
- `01781672` - CLAUDE instruction set

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


# Validation Strategy

**Date:** 2026-10-17  
**Guidance:** a63fd146, 0b2613ac, 01781672  
**Memory Status:** LIVE_MEMORY_EMPTY_UNSCREENED

## Validation Levels

### L1: Cryptographic Proof
- Sigstore signature verification (v0.14.0)
- RVF seal validation (v0.2.0)
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
- Immutable guidance IDs (AGENTS 0b2613ac, standard a63fd146, CLAUDE 01781672) resolve to canonical rules
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


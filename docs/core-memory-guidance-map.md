# Core Memory Guidance Map

**Date:** 2026-10-17  
**Status:** LIVE_MEMORY_EMPTY_UNSCREENED  
**Last Refresh:** 2026-10-17

## Immutable Guidance IDs

These guidance IDs are **persistent**, **never recomputed**, and form the canonical rule set for the Provenance Firebreak system.

### AGENTS: 0b2613ac
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

### Standard: a63fd146
**Domain:** Architectural and design patterns  
**Authority:** Architecture review board  
**Mutability:** Immutable (Git blob prefix)  
**Resolution Path:** docs/design/standards.blob

**Rules:**
1. All attestations must use Sigstore tooling (v0.14.0)
2. Temporal lineage must preserve causal ordering (no backward edges)
3. Risk assessment must employ split-conformal prediction sets
4. Quarantine policies must minimize blast radius
5. Recovery checkpoints must use RVF seals (v0.2.0)
6. All cryptographic proofs must validate in authority-zero model

### CLAUDE: 01781672
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
    throw UnknownGuidanceException("blob_prefix not in {set of 3 canonical IDs}")
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


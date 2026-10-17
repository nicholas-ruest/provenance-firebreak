# Provenance Firebreak — Specification

Status: Phase 1 (design only). No Rust source or Cargo manifests exist yet; this
document and its siblings are the design record that implementation must satisfy.

## 1. Problem statement

Security and SRE teams operating multi-tenant build/deploy pipelines need to
answer one question fast, correctly, and reproducibly after a builder
compromise is suspected: **which artifacts and running services must be
quarantined right now, and which can provably stay up?**

Today that question is answered by either (a) manual log/graph archaeology
under time pressure, which is slow and error-prone, or (b) "quarantine
everything the builder touched," which is fast but disruptive — it takes
down tier-0 services that were never actually reachable from the compromised
build, and it has no calibrated confidence attached to the decision.

Provenance Firebreak closes that gap: it ingests signed attestations and
deployment lineage, cryptographically verifies the Sigstore trust boundary
those attestations claim to cross, builds an exact temporal artifact-to-service
graph, retrieves structurally similar historical incidents, computes a
statistically calibrated upper bound on residual risk, and selects the
cheapest quarantine plan that satisfies that bound while preserving tier-0
availability — sealing the whole decision as replayable evidence.

## 2. Users

- **Incident commander (security/SRE on-call)** — needs a quarantine
  recommendation with a bound on how wrong it can be, in time to act during
  an active incident.
- **Platform/SRE team** — owns tier-0 availability SLOs and needs any
  automated quarantine to provably respect them, not just claim to.
- **Compliance/audit reader** — needs a sealed, tamper-evident record of
  what was known, decided, and why, for post-incident review and attestation
  of the incident response itself.
- **Pipeline operator** — runs the CLI/service day to day, needs
  cancellation and recovery when a plan turns out to be wrong or the
  incident is downgraded.

## 3. Frozen workload (Phase 1 scope)

To make "exact reachability" and "deterministic digest" achievable and
testable, Phase 1 freezes the workload to a single scenario class:

> **One compromised builder.** Multiple tenants. Multiple artifacts per
> tenant. Multiple deployments per artifact, across services, each with a
> validity interval (deploy time, optional retire time). The compromised
> builder produced some subset of artifacts over some time window; the
> system must determine the exact closure of affected deployments and
> downstream artifacts built from affected artifacts.

Out of scope for Phase 1: multiple simultaneously compromised builders,
compromised Sigstore trust roots (Fulcio/Rekor themselves), and
non-deterministic/distributed graph construction (sharded ingestion is a
Phase 2 concern). These are recorded as explicit non-goals so "exact
reachability" and "deterministic digest" stay provable rather than
aspirational.

## 4. Success criteria

| # | Criterion | Definition | Falsifiable test |
|---|-----------|------------|-------------------|
| 1 | Exact reachability | The set of deployments/artifacts flagged as exposed equals the transitive closure of the lineage graph from the compromised builder's artifacts, no more, no less. | Property test: for a generated graph with a known ground-truth closure, `pf-exposure` output set-equals the ground truth, for all generated cases, zero tolerance. |
| 2 | Deterministic digest | Two runs over the same frozen input snapshot produce byte-identical canonical plan output and identical digest. | Repeat-run test: hash the canonicalized plan twice from the same input fixture; digests must match; must also match across process restarts and across the two supported OSes in CI. |
| 3 | Calibrated risk bound | Split-conformal upper bound on residual risk achieves ≥0.90 empirical holdout coverage at α=0.10. | Holdout evaluation harness (`pf-evaluation`) over a labeled incident-replay corpus, reported with the exact α, nominal coverage target (≥1−α = 0.90), and the realized empirical coverage plus its confidence interval. |
| 4 | Cheaper than quarantine-all | The selected plan's disruption cost (services taken down × criticality weight) is strictly less than the "quarantine everything reachable from the builder" baseline, on every non-trivial incident fixture, while never exceeding the calibrated risk bound. | Benchmark harness compares plan cost vs. baseline cost per fixture; report must show cost reduction with the risk bound satisfied in both arms. |
| 5 | Explicit ablations | Removing RuVector incident retrieval, removing calibration, or removing least-disruptive planning (falling back to quarantine-all) must each be runnable and reported as a named ablation with measured deltas. | `pf-evaluation` exposes `--ablate {none,no-retrieval,no-calibration,no-planning}`; results table includes all four arms. |

Any criterion that cannot be met with evidence is reported as such — this
document does not treat an unmet criterion as a reason to loosen its
definition.

## 5. Constraints

- **Tier-0 availability is a hard constraint, not a cost term.** A plan that
  quarantines a tier-0 service is inadmissible regardless of risk-bound
  improvement, unless every non-quarantine option is proven to violate the
  calibrated risk bound — see [ADR-0015](adrs/0015-tier0-availability-invariant.md).
- **Multi-tenant isolation.** No tenant's lineage, attestations, or incident
  history may leak into another tenant's quarantine decision or evidence
  record — see [ADR-0017](adrs/0017-multi-tenant-isolation.md).
- **The Sigstore boundary is verified, not assumed.** Every attestation must
  cryptographically verify against Fulcio-issued certificates and Rekor
  inclusion before it is allowed to influence lineage or policy — see
  [ADR-0005](adrs/0005-sigstore-boundary-verification.md).
- **No invented provenance.** Any commit SHA, upstream version, or external
  fact that cannot be verified from a primary source this session is
  recorded as `PENDING_VERIFICATION`, never fabricated — see
  [ADR-0025](adrs/0025-pending-verification-discipline.md) and
  [research.md](research.md).
- **Phase 1 is design-only.** No Rust source, no `Cargo.toml`. The
  `rust-toolchain.toml` and `deny.toml` created in this phase are
  pre-registered constraints for Phase 2 implementation, not evidence of
  running code.

## 6. Ingredient composition (per the Dream Machine build standard)

Per [core-memory-guidance-map.md](core-memory-guidance-map.md) and the
build-standard requirement for ≥2 Ruvnet components, 1 enterprise OSS
component, and 1 frontier research mechanism, with primary-source pinning:

| Role | Ingredient | Version | License | Primary interface used |
|------|------------|---------|---------|-------------------------|
| Ruvnet #1 | `ruvector-core` | 2.4.0 | Apache-2.0 | `insert` / `search` / `get` — incident-retrieval memory |
| Ruvnet #2 | `rvf-crypto` | 0.2.0 | Apache-2.0 | sealing / tamper rejection — evidence ledger |
| Enterprise OSS | `sigstore` (from `sigstore/sigstore-rs`) | 0.14.0 | Apache-2.0 | real upstream verification types (Fulcio cert chain, Rekor inclusion proof, bundle verification) |
| Frontier research mechanism | Split-conformal risk control | — | — | nonconformity scoring + calibrated quantile, materially gating plan admission (not advisory) |

Exact revision pinning (lockfile digests, upstream commit SHAs) is deferred
to Phase 2; see [research.md §Primary sources and verification status](research.md)
for what is and is not verified as of this session.

## 7. Non-goals (Phase 1)

- No implementation, no benchmarks run against real code, no CI.
- No handling of multiple concurrently compromised builders.
- No defense against a compromised Sigstore trust root itself.
- No UI; CLI and service API contracts are specified, not built.
- No claim of coverage beyond the ≥0.90 target without holdout evidence —
  Phase 1 defines the evaluation protocol; Phase 2 produces the numbers.

## 8. Related documents

[architecture.md](architecture.md) · [research.md](research.md) ·
[integration-matrix.md](integration-matrix.md) ·
[implementation-contract.md](implementation-contract.md) ·
[traceability.md](traceability.md) · [validation.md](validation.md) ·
[core-memory-guidance-map.md](core-memory-guidance-map.md) ·
[adrs/README.md](adrs/README.md) · [ddd/README.md](ddd/README.md)

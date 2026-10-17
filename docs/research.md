# Provenance Firebreak — Research

## Problem and selection

Software-supply-chain incident responders need more than an attestation checker: they must reconstruct which workloads received a suspect artifact, estimate containment risk from limited historical data, isolate the smallest safe set, preserve critical services, and retain cryptographically replayable evidence. Provenance Firebreak was selected because those responsibilities require a composite system rather than a validator, parser, wrapper, or benchmark harness.

The intended users are platform security and SRE teams. The realistic workload is the checked-in incident fixture: a suspect worker artifact has propagated through a deployment graph containing a tier-0 payments root. Success means the system rejects untrusted provenance, recalls at least one analogous incident, computes a deterministic calibrated upper-risk bound, quarantines the exposed worker/root set without quarantining payments, verifies the RVF witness chain, and confirms recovery.

## Candidate comparison

| Candidate | System-scale value | Required composition | Decision |
|---|---|---|---|
| Provenance Firebreak | incident reconstruction, calibrated containment, evidence, recovery | Sigstore + RuVector + RVF + split conformal | selected |
| Attestation Linter | checks bundle fields | Sigstore only | rejected: utility-scale validator |
| Vector Incident Search | retrieves similar alerts | RuVector only | rejected: one-feature service |
| Release Receipt Generator | emits signed records | RVF only | rejected: wrapper without orchestration or recovery |

This capability is materially distinct from recent Dream Machine outputs: JitterMap governs retry admission, ToolRecall ranks tool retrieval, and EvoSeal evolves policy candidates. Provenance Firebreak instead performs signed-artifact incident containment across provenance, temporal lineage, calibrated risk, quarantine policy, evidence sealing, and recovery verification.

## Primary sources and pinned inputs

- Sigstore Rust repository and tag source: <https://github.com/sigstore/sigstore-rs/tree/ac9e5774e07fbb5b74cfe8ca1b1aaf3a3417c997>. The published `sigstore 0.14.0` crate records this source SHA and Apache-2.0 license.
- RuVector source for `ruvector-core 2.4.0`: <https://github.com/ruvnet/ruvector/tree/e3d82b19683a08c6392a2534bafc90927ca690c7>. The published crate records the MIT license and `crates/ruvector-core` source path.
- RVF crypto source for `rvf-crypto 0.2.0`: <https://github.com/ruvnet/ruvector/tree/9fb3d2c63b19ac6950b931f4adb56834bf96c45d>. The published crate records the MIT OR Apache-2.0 license and `crates/rvf/rvf-crypto` source path.
- Lei, G'Sell, Rinaldo, Tibshirani, and Wasserman, “Distribution-Free Predictive Inference for Regression”: <https://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf>. This is the primary statistical basis for the split-conformal mechanism.

The exact interface-to-test-to-ablation mapping is in [integration-matrix.md](integration-matrix.md). Versions and checksums are frozen in `Cargo.lock`.

## Frontier mechanism

The frontier mechanism is a split-conformal upper-risk gate, not a decorative score. `pf-calibration` orders frozen nonconformity scores and selects the finite-sample quantile determined by the requested miscoverage level. The bound directly changes the quarantine decision path. Its guarantee is marginal and depends on exchangeability; the project does not claim conditional coverage or production calibration from the small fixture.

## Measurable hypotheses

| Removal | Expected degradation | Observed field |
|---|---|---|
| RuVector | analogue recall disappears | `analogous_recall=false` |
| RVF | receipt cannot be verified | `evidence_verifiable=false` |
| Sigstore | tier-0 containment policy becomes unsafe | `unsafe_tier0_actions=1` |
| split conformal | calibrated risk evidence disappears | `calibrated_bound=false` |
| enterprise-only baseline | no recall, calibration, or witness evidence | all three false |
| Ruvnet-only baseline | no trusted provenance or calibrated policy | unsafe tier-0 action plus no bound |

## Limitations

- The checked-in Sigstore fixture is structurally valid but intentionally untrusted; the test proves a live library verification-rejection boundary, not an online Fulcio/Rekor production ceremony.
- Incident vectors are deterministic, domain-authored features rather than learned embeddings.
- The fixture and calibration set are deliberately small and frozen; results establish reproducibility, not external validity.
- `ruvector-core 2.4.0` reaches the recorded source commit through crates.io rather than a Git dependency because no matching upstream tag existed at validation time.
- The `cargo deny` policy explicitly acknowledges the transitive unmaintained `bincode` advisory in RuVector and RSA timing advisory in Sigstore; rationale is recorded in `deny.toml` and validation evidence.

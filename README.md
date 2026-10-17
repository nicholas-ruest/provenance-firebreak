<div align="center">

# Provenance Firebreak

**Signed-artifact incident containment with calibrated risk and replayable evidence**

<img src="docs/assets/third-party/rust.svg" alt="Rust" height="38">&nbsp;&nbsp;
<img src="docs/assets/third-party/sigstore.svg" alt="Sigstore" height="38">&nbsp;&nbsp;
<img src="docs/assets/third-party/github-actions.svg" alt="GitHub Actions" height="38">

</div>

![Provenance Firebreak execution overview](docs/assets/firebreak-hero.svg)

Provenance Firebreak helps platform-security and SRE teams contain a suspect software artifact without taking down a protected service. It parses and rejects untrusted Sigstore bundles, reconstructs temporal deployment exposure, recalls analogous incidents with RuVector, computes a split-conformal upper-risk bound, chooses a least-disruptive tier-safe quarantine, seals the decision with RVF, and verifies recovery.

This is a system, not an attestation checker: provenance, graph exposure, calibrated risk, policy, evidence, and recovery interact in one end-to-end workload.

## Quickstart

Requirements: Rust 1.99.0 and the checked-in lockfile.

```bash
cargo run --locked -p pf-cli -- \
  --input fixtures/incident.json \
  --state target/demo
```

Representative output from the frozen fixture:

```json
{
  "risk_upper": 1.0,
  "analogue_count": 1,
  "quarantined": ["worker", "root"],
  "preserved": ["payments"],
  "receipt_count": 6,
  "recovery_verified": true,
  "sigstore_untrusted_rejected": true
}
```

The fixture is intentionally untrusted: it proves the real Sigstore library rejection boundary while the planner still evaluates the incident counterfactual. It does not claim a live Fulcio/Rekor production ceremony.

## Execution flow

![Provenance Firebreak architecture and execution flow](docs/assets/firebreak-flow.svg)

1. Parse the signed-artifact bundle and fail closed when supplied trust keys cannot verify it.
2. Build temporal lineage and compute the reachable deployment exposure.
3. Insert and search deterministic incident features through a persistent RuVector database.
4. Compute a split-conformal upper-risk quantile from the frozen calibration set.
5. Select the smallest quarantine set that preserves every tier-0 service.
6. Create and verify an RVF witness chain over the append-only decision receipt.
7. Replay recovery and prove that the payments workload remains available.

## Workspace map

All 22 members are reachable from the CLI or evaluation roots; the verified graph has 48 internal dependency edges and no decorative members.

| Boundary | Crates | Responsibility |
|---|---|---|
| Core domain | `pf-identity`, `pf-artifact`, `pf-attestation`, `pf-lineage`, `pf-exposure` | identities, artifacts, attestations, temporal lineage, exposure closure |
| Decision domain | `pf-policy`, `pf-planning`, `pf-calibration`, `pf-events` | tier invariants, quarantine optimization, conformal bound, domain events |
| Ports and upstreams | `pf-ports`, `pf-adapter-sigstore`, `pf-adapter-ruvector`, `pf-adapter-rvf` | typed boundaries and executed enterprise/Ruvnet integrations |
| Evidence and recovery | `pf-graph`, `pf-evidence`, `pf-recovery` | reachability, append-only receipts, verified replay |
| Application/runtime | `pf-application`, `pf-config`, `pf-telemetry`, `pf-service`, `pf-cli` | orchestration, validated config, tracing, service and operator interface |
| Evaluation | `pf-evaluation` | combined run, baselines, ablations, reproducible evidence |

The full dependency and caller map is in [architecture.md](docs/architecture.md); crate-level responsibilities, tests, ADR/DDD references, and acceptance criteria are traced in [implementation-contract.md](docs/implementation-contract.md).

## Upstream composition

| Ingredient | Exact pin and source | Executed responsibility | Test / ablation |
|---|---|---|---|
| RuVector | `ruvector-core 2.4.0`; `ruvnet/ruvector@e3d82b19683a08c6392a2534bafc90927ca690c7` | `VectorDB` open, insert, persistent nearest-neighbour search | end-to-end test; recall becomes false without it |
| RVF | `rvf-crypto 0.2.0`; `ruvnet/ruvector@9fb3d2c63b19ac6950b931f4adb56834bf96c45d` | SHAKE-256 witness-chain create/verify | end-to-end test; evidence becomes unverifiable without it |
| Sigstore Rust | `sigstore 0.14.0`; `sigstore/sigstore-rs@ac9e5774e07fbb5b74cfe8ca1b1aaf3a3417c997` | bundle parse and verification against supplied keys | malformed + untrusted failure tests; tier-0 action becomes unsafe without it |
| Split conformal | `pf-calibration` | finite-sample upper-risk quantile | deterministic test; calibrated evidence disappears without it |

Licenses and exact interfaces are recorded in the [integration matrix](docs/integration-matrix.md). Technology marks are local official or Simple Icons vectors; attribution is in [the asset license](docs/assets/third-party/SIMPLE-ICONS-LICENSE.md).

## Evaluation and ablations

Seed `20261016`, workload `signed-lineage-incident-v1`:

| Mode | Unsafe tier-0 actions | Evidence verifiable | Calibrated bound | Analogue recall |
|---|---:|:---:|:---:|:---:|
| combined | 0 | yes | yes | yes |
| without RuVector | 0 | yes | yes | no |
| without RVF | 0 | no | yes | yes |
| without Sigstore | 1 | yes | yes | yes |
| without conformal | 0 | yes | no | yes |
| enterprise-only | 0 | no | no | no |
| Ruvnet-only | 1 | yes | no | yes |

Reproduce the evaluation:

```bash
bash scripts/run-evaluation.sh
```

The machine-readable record is [evidence/evaluation.jsonl](evidence/evaluation.jsonl); raw command receipts and the independent linkage review are under [evidence/](evidence/).

## Validation

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --locked --workspace --all-features
cargo deny check
node /path/to/check-project-contract.mjs .
```

The exact remote tree passed two GitHub Actions runs and the pinned structural checker with 22 crates, 25 ADRs, 12 DDD documents, and two animated project diagrams. The checker result is structural only; [semantic-review.md](evidence/semantic-review.md) separately establishes reachability, non-ceremonial boundaries, and executed upstream calls.

## Maturity and limitations

Experimental, reproducible architecture—not a production safety certification.

- Sigstore is exercised offline with a structurally valid but intentionally untrusted bundle; online Fulcio/Rekor trust-root retrieval is out of scope.
- Incident vectors are deterministic domain features rather than learned embeddings.
- The small frozen calibration set demonstrates the mechanism and reproducibility, not external statistical validity.
- `cargo deny` acknowledgements for transitive RuVector/Sigstore advisories are explicit in `deny.toml` and the validation evidence.
- The service is single-process and local-state for evaluation; distributed consensus and multi-tenant authorization are future work.

## Design and evidence index

- [Specification](docs/specification.md) · [Architecture](docs/architecture.md) · [Research](docs/research.md) · [Implementation contract](docs/implementation-contract.md)
- [Core-memory guidance map](docs/core-memory-guidance-map.md) · [Integration matrix](docs/integration-matrix.md) · [Validation](docs/design/validation.md)
- [ADR index](docs/adrs/README.md) · [DDD index](docs/ddd/README.md) · [Semantic review](evidence/semantic-review.md)
- [Research Gist](https://gist.github.com/nicholas-ruest/8c8ea844052c1a7d129f3292b94f1546) · [Build Gist](https://gist.github.com/nicholas-ruest/0f44e14cc1086775c7f48b7dfb9d7ed0)

## License

Apache-2.0. Third-party crates and visual marks retain their own licenses as documented in the lockfile, integration matrix, and asset attribution.

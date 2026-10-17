# Integration Matrix

**Build date:** 2026-10-16
**Evidence state:** implemented and exercised
**Live memory state:** `LIVE_MEMORY_EMPTY_UNSCREENED`
**Repository guidance:** applied from core-memory guidance blob `a63fd1464eaf5eecbe919aac2e7699df24eabbdc`

The version pins below are the exact Cargo.lock inputs. The source commit is taken from each published crate's `.cargo_vcs_info.json`, making the crates.io package reproducible back to its source repository.

| Ingredient | Pin / source commit | License | Capability reused | Executed boundary | Owning crate | Integration test | Ablation |
|---|---|---|---|---|---|---|---|
| RuVector `ruvector-core` | `2.4.0`; `ruvnet/ruvector@e3d82b19683a08c6392a2534bafc90927ca690c7` | MIT | persistent vector insert and nearest-neighbour search | Rust crate API: `VectorDB::new`, `upsert`, `search` | `pf-adapter-ruvector` | `pf-application/tests/end_to_end.rs`; workspace tests | `without-ruvector` makes `analogous_recall=false` |
| RVF `rvf-crypto` | `0.2.0`; `ruvnet/ruvector@9fb3d2c63b19ac6950b931f4adb56834bf96c45d` | MIT OR Apache-2.0 | SHAKE-256 witness-chain construction and verification | Rust crate API: `create_witness_chain`, `verify_witness_chain`, `shake256_256` | `pf-adapter-rvf` | end-to-end seal verification; failure-path unit test | `without-rvf` makes `evidence_verifiable=false` |
| Sigstore Rust | `0.14.0`; `sigstore/sigstore-rs@ac9e5774e07fbb5b74cfe8ca1b1aaf3a3417c997` | Apache-2.0 | bundle JSON parsing and verification against supplied trust keys | Rust crate API: `SignedArtifactBundle` and `new_verified` | `pf-adapter-sigstore` | valid structure parse + untrusted verification rejection | `without-sigstore` permits one unsafe tier-0 action |
| Split conformal risk control | implementation traced in `pf-calibration` | project license | finite-sample quantile upper bound over frozen nonconformity scores | typed `CalibrationSet` / upper-bound API | `pf-calibration`, called by `pf-application` | deterministic unit tests and end-to-end risk gate | `without-conformal` makes `calibrated_bound=false` |

## Executed end-to-end boundary

1. `pf-adapter-sigstore` deserializes the incident bundle and proves that verification with an empty trust-key set fails closed.
2. `pf-lineage` and `pf-graph` construct temporal deployment relationships and reachable exposure.
3. `pf-adapter-ruvector` opens a local persistent database, inserts a frozen analogue vector, and performs similarity search.
4. `pf-calibration` computes a split-conformal upper risk bound from the frozen calibration scores.
5. `pf-planning` computes a quarantine that preserves the tier-0 payments service.
6. `pf-adapter-rvf` constructs and verifies the witness chain over the append-only decision receipt.
7. `pf-recovery` replays the plan and verifies that the protected workload remains available.

## Failure and policy boundaries

- Invalid Sigstore JSON is a typed error; a structurally valid but untrusted bundle is rejected.
- Empty calibration data is rejected rather than silently producing a bound.
- Quarantine planning must preserve every tier-0 service; the Sigstore ablation deliberately demonstrates the unsafe counterfactual.
- RuVector and RVF state remain below an explicit caller-provided state root; no ambient home-directory writes are used.
- RVF verification failure blocks recovery evidence acceptance.

## Reproduction

Run `cargo test --locked --workspace --all-features` for unit, failure-path, and integration coverage, then `bash scripts/run-evaluation.sh` for the combined system, two ingredient-family baselines, and four ablations. Raw commands, exit codes, tool versions, and outputs are retained under `evidence/raw/`.

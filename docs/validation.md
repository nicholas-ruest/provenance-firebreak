# Validation

## Candidate state

Validation was executed on the indexed `build/2026-10-16-provenance-firebreak` branch after the complete 22-crate workspace, documentation, assets, fixtures, and evidence were staged.

## Required commands

| Command | Exit | Evidence |
|---|---:|---|
| `cargo fmt --check` | 0 | `evidence/raw/fmt.txt` |
| `cargo clippy --all-targets --all-features -- -D warnings` | 0 | `evidence/raw/clippy.txt` |
| `cargo test --locked --workspace --all-features` | 0 | `evidence/raw/test.txt` |
| `cargo deny check` | 0 | `evidence/raw/deny.txt` |
| `cargo test --locked -p pf-application --test end_to_end` | 0 | `evidence/raw/integration-test.txt` |
| `cargo run --locked -p pf-evaluation` | 0 | `evidence/evaluation.jsonl` |
| pinned checker regression suite | 0 | `evidence/raw/checker-regression.txt` |
| pinned candidate checker | 0 | `evidence/raw/contract-checker.txt` |

## Contract result

Checker source: `nicholas-ruest/ruvnet-dream-machine@80f006f6960bc4e491e97f51e890ff708e81aa88`.

Result: `STRUCTURAL_PASS_REQUIRES_EVIDENCE_REVIEW` with 25 ADRs, 12 DDD documents, 22 implemented crates, two animated SVGs, and zero failures.

## Independent evidence review

Cargo metadata finds all 22 workspace members reachable from the CLI/evaluation roots through 48 internal edges. The semantic review in `evidence/semantic-review.md` confirms real Sigstore, RuVector, and RVF execution; a source-bound split-conformal decision; meaningful ablations; and explicit limitations.

## Security limitations

`cargo deny` exits zero with two visible, reasoned transitive advisory exceptions in `deny.toml`. They are not reachable as private-key signing behavior in this system. Re-evaluate when RuVector or Sigstore publishes compatible dependency updates.

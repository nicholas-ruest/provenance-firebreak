#!/usr/bin/env bash
set -euo pipefail

# The evaluator owns its deterministic state directory and emits the complete
# combined/baseline/ablation record to evidence/evaluation.jsonl.
cargo run --locked --quiet -p pf-evaluation

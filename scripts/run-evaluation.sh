#!/usr/bin/env bash
set -euo pipefail
state="${1:-target/evaluation-state}"
rm -rf "$state"
cargo run --locked -q -p pf-cli -- --input fixtures/incident.json --state "$state" > "$state.out.json"
printf '%s\n' combined without-ruvector without-rvf without-sigstore without-conformal enterprise-only ruvnet-only > "$state.modes.txt"
sha256sum "$state.out.json" "$state.modes.txt"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ROOT_DIR/scripts/validate_runtime_state.py" \
  "$ROOT_DIR/examples/runtime_samples/sample_state.json" \
  "$ROOT_DIR/examples/runtime_samples/sample_evidence_log.jsonl"

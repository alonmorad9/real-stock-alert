#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-daily}"
python3 script.py "$MODE"


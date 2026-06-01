#!/usr/bin/env bash
set -euo pipefail

DEFAULT_SCRIPT="generated-scripts/demo-shop/tc-002-homepage-rendering-verification-17.py"
SCRIPT="${1:-$DEFAULT_SCRIPT}"
VENV_PY=".venv/bin/python"

if [[ ! -f "$SCRIPT" ]]; then
  echo "Error: Script not found: $SCRIPT"
  exit 1
fi

echo "Running Playwright pytest: $SCRIPT"

if [[ -x "$VENV_PY" ]]; then
  PYTHON_BIN="$VENV_PY"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: Python is not installed or not on PATH"
  exit 1
fi

"$PYTHON_BIN" -m pytest -v "$SCRIPT"

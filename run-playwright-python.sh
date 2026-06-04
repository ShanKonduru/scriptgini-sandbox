#!/usr/bin/env bash
set -euo pipefail

DEFAULT_SCRIPT="generated-scripts/demo-shop/tc-004-navigation-broken-links-check-18.py"
DEFAULT_RUN_MODE="maximized"
RUN_MODE="${PW_RUN_MODE:-$DEFAULT_RUN_MODE}"

case "${RUN_MODE,,}" in
  max|maximize|maximized)
    RUN_MODE="maximized"
    ;;
  head|headed)
    RUN_MODE="headed"
    ;;
  headless)
    RUN_MODE="headless"
    ;;
  *)
    echo "Error: Invalid RUN_MODE '$RUN_MODE'. Use headless, headed, or maximized."
    exit 1
    ;;
esac

SCRIPT="${1:-$DEFAULT_SCRIPT}"
if [[ $# -gt 0 ]]; then
  shift
fi
EXTRA_ARGS=("$@")
VENV_PY=".venv/bin/python"

if [[ ! -f "$SCRIPT" ]]; then
  echo "Error: Script not found: $SCRIPT"
  exit 1
fi

echo "Running Playwright pytest: $SCRIPT"
echo "Run mode: $RUN_MODE"

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

"$PYTHON_BIN" -m pytest -v --run-mode "$RUN_MODE" "$SCRIPT" "${EXTRA_ARGS[@]}"

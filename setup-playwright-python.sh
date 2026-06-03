#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: Python is not installed or not on PATH"
  exit 1
fi

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Creating virtual environment in $VENV_DIR..."
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "Installing Python dependencies for Playwright tests in $VENV_DIR..."
python -m pip install -U pip
python -m pip install -U pytest pytest-playwright playwright
python -m playwright install chrome

echo
echo "Setup complete."
echo "Current script used environment: $(pwd)/$VENV_DIR"
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "To activate in your current shell: source ./$VENV_DIR/bin/activate"
else
  echo "Virtual environment is active in this shell session."
fi

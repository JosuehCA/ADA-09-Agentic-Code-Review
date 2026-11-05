#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Running tests"
pytest -q

echo "[2/3] Running lint"
if command -v flake8 >/dev/null 2>&1; then
    flake8 src tests --max-line-length=130 --ignore=W391
else
    python -m py_compile src/*.py tests/*.py
fi

echo "[3/3] Repository checks"
python scripts/check_repo_contract.py

echo "VERIFY_REPO: PASS"

#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt
PYTHONPATH="." python scripts/migrate.py

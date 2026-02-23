#!/bin/sh
# Run from repo root
cd "$(dirname "$0")/.."
python -m venv backend/.venv 2>/dev/null || true
. backend/.venv/bin/activate 2>/dev/null || . backend/.venv/Scripts/activate 2>/dev/null || true
pip install -q -r backend/requirements.txt
exec uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

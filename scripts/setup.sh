#!/usr/bin/env bash
set -e

echo "▶ Creating virtual environment..."
python3 -m venv venv

echo "▶ Activating venv and upgrading pip..."
source venv/bin/activate
pip install --upgrade pip

echo "▶ Installing project requirements..."
pip install -r requirements.txt

echo "▶ Running unit‑tests..."
pytest -q

echo "✅  Setup complete – activate with:  source venv/bin/activate"

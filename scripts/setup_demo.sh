#!/usr/bin/env bash
# Author: abdul (neeil)
# Proposed setup based on the historical October environment.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v conda >/dev/null || { echo "Install Miniforge/Conda first."; exit 1; }
if ! conda run -n openverse-demo python -c 'import sys; assert sys.version_info[:2] == (3,10)' >/dev/null 2>&1; then
  conda create -y -n openverse-demo python=3.10 pip
fi
conda run -n openverse-demo python -m pip install --upgrade pip
if ! conda run -n openverse-demo python -m pip install -r requirements.txt; then
  echo "Full pip install failed. Attempting historical LanceDB Conda fallback."
  conda install -y -n openverse-demo -c conda-forge lancedb=0.11.0 numpy=1.26.4
  TEMP_REQ="$(mktemp)"
  trap 'rm -f "$TEMP_REQ"' EXIT
  grep -viE '^(lancedb|graphrag)[[:space:]@=]' requirements.txt > "$TEMP_REQ"
  conda run -n openverse-demo python -m pip install -r "$TEMP_REQ"
  conda run -n openverse-demo python -m pip install --no-deps "git+https://github.com/microsoft/graphrag.git@75735bd1036b00abfe17a951383392049cb72947"
fi
conda run -n openverse-demo python -m pip install "streamlit==1.39.0"
conda run -n openverse-demo python -m pip check
conda run -n openverse-demo python query.py --help
echo "Activate with: conda activate openverse-demo"

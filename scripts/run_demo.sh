#!/usr/bin/env bash
# Author: abdul (neeil)
set -euo pipefail
cd "$(dirname "$0")/.."
python -c 'import streamlit; import graphrag' || { echo "Activate the openverse-demo environment first."; exit 1; }
exec python -m streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true

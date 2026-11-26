"""Preflight checks for the OPENVERSE demo. Author: abdul (neeil)."""
import argparse
import importlib
import importlib.metadata
import json
import platform
import sys
from pathlib import Path
from urllib.request import urlopen

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("artifacts", type=Path)
args = parser.parse_args()
failures = []
print("Platform:", platform.platform(), platform.machine())
print("Python:", sys.version)
if sys.version_info[:2] != (3, 10):
    failures.append("Expected Python 3.10 (historical environment).")
for name, expected in {"graphrag": "0.3.2", "lancedb": "0.11.0", "numpy": "1.26.4", "ollama": "0.3.3", "streamlit": "1.39.0"}.items():
    try:
        importlib.import_module(name)
        version = importlib.metadata.version(name)
        print(name, version)
        if version != expected:
            failures.append(f"{name}: expected {expected}, found {version}")
    except Exception as exc:
        failures.append(f"{name}: {exc}")
for name in ("create_final_nodes.parquet", "create_final_entities.parquet", "create_final_relationships.parquet", "create_final_text_units.parquet", "create_final_community_reports.parquet"):
    if not (args.artifacts / name).is_file():
        failures.append(f"Missing historical index file: {name}")
try:
    with urlopen("http://localhost:11434/api/tags", timeout=10) as response:
        tags = {m["name"] for m in json.load(response)["models"]}
    print("Ollama models:", sorted(tags))
    for name in ("llama3.1", "nomic-embed-text"):
        if name not in tags and name + ":latest" not in tags:
            failures.append(f"Missing Ollama model: {name}")
except Exception as exc:
    failures.append(f"Ollama check failed: {exc}")
if failures:
    print("\nPreflight issues:")
    for failure in failures:
        print("-", failure)
    sys.exit(1)
print("Preflight passed. Run a real local query to validate inference.")

# OPENVERSE Graph-RAG — troubleshooting

**Author: abdul (neeil)**

Hi Lukasz,

If you encounter an issue, these are the checks I suggest before changing the environment.

| Symptom | What I suggest you do |
|---|---|
| Repository access denied | Confirm your GitHub account has access; do not send passwords or tokens. |
| LanceDB 0.11.0 unavailable via pip | Use the Conda fallback in setup_demo.sh. This previously helped on Apple Silicon. |
| GraphRAG internal import error | Confirm the pinned Git revision and GraphRAG 0.3.2; avoid installing the latest release. |
| Missing Parquet files | Verify the complete authorised artifact directory and its path; do not re-index automatically. |
| Connection refused | Check Ollama is running locally using ollama list and curl http://localhost:11434/api/tags. |
| Model missing | Run ollama pull llama3.1 and ollama pull nomic-embed-text. |
| Embedding dimension mismatch | Verify the original index's embedding model and version; do not substitute another model. |
| Streamlit reports a timeout | Try the CLI directly using the command in the guide; use local search and rehearse latency. |
| Browser cannot reach server | Use the SSH forwarding command in the guide; check the Streamlit terminal and local port. |
| No citations or weak evidence | Inspect the source evidence and do not report the response as verified. |

Please send me your OS, architecture, Python version, repository commit, output of the preflight script and the relevant traceback with secrets or restricted corpus text removed. Do not expose Ollama to the public internet.

Best,  
Abdul (Neeil)

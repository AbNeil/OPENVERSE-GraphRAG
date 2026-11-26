# OPENVERSE Graph-RAG — demonstration handover

**Author: Abdul**    
**Date: 26 November 2026**

Here is how I suggest you set up the system for next week's demonstration. You will need the GitHub source code, a compatible Python environment, Ollama and the precomputed knowledge graph that I will need to arrange to transfer separately through an authorised channel.

## 1. Choose your machine

You can use a Linux server, a GPU workstation or a Mac whatever you like. I suggest 16 GB RAM as a starting point and 32 GB if available, with at least 25 GB of free disk space. These are indicative, not measured requirements. If you use Windows, I suggest WSL2 with Ubuntu and a compatible Ollama setup. The commands below are for bash on Linux or macOS.

In October, I used a Conda environment named `openverse-demo`, Python 3.10.22 on Apple Silicon, GraphRAG 0.3.2, LanceDB 0.11.0 and NumPy 1.26.4. That historical environment worked for local queries.

## 2. Download the code

First, make sure you have access to my repository. Install Git and Miniforge or another Conda distribution if needed.

```bash
git clone https://github.com/AbNeil/OPENVERSE-GraphRAG.git
cd OPENVERSE-GraphRAG
git rev-parse HEAD
```

Keep a note of the commit hash so we can identify exactly which version you demonstrated.

## 3. Set up the Python environment

I suggest running the setup script from the repository root:

```bash
bash scripts/setup_demo.sh
conda activate openverse-demo
```

The script uses Python 3.10, installs the pinned historical requirements and Streamlit, and uses Conda for LanceDB if pip cannot complete the installation. It does not install Ollama or download research data. If a step fails, send me the complete error and your operating system/architecture rather than upgrading GraphRAG or LanceDB indiscriminately. The project uses internal GraphRAG APIs that are version sensitive.

## 4. Install and start Ollama

Please install Ollama from https://ollama.com/download, following the instructions for your operating system. On a server you may need your administrator's assistance, particularly for GPU drivers. Keep the service bound to loopback.

If Ollama is not already running, open a second terminal and run:

```bash
ollama serve
```

Leave that terminal running. From the project terminal, download the models:

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
ollama list
```

Llama 3.1 generates answers; Nomic generates the query embeddings. Please do not change the embedding model without checking compatibility with the existing index. The repository expects a local Ollama chat endpoint at http://localhost:11434/v1 and uses the local Ollama Python client for embeddings. If the original model tags/digests are available, I will compare them with yours.

## 5. Import the precomputed research graph

This is the important part: the source repository does not contain the original corpus or the generated index. I need to arrange access to the complete authorised artifact directory before you can reproduce the demonstration. You do not need to run indexing again.

The directory was `ragtest/output/20241018-095127/artifacts`. After receiving the archive, inspect it before extraction and copy the complete artefacts directory into that location (or use its actual path).

```bash
mkdir -p ragtest/output/20241018-095127
# Copy the supplied complete artifacts directory here.
export DEMO_ARTIFACTS="$PWD/ragtest/output/20241018-095127/artifacts"
ls -lah "$DEMO_ARTIFACTS"
```

Please retain all Parquet files and any vector-store subdirectories, not just the entity and relationship files. Do not commit the archive, research text or derived graph to GitHub. If the transferred index has a different timestamp, update DEMO_ARTIFACTS accordingly. Transfer is subject to the project's data and distribution rights.

## 6. Check the environment

With the Conda environment active, run:

```bash
python scripts/check_demo.py "$DEMO_ARTIFACTS"
```

This checks imports, expected historical versions, the presence of core graph files, and whether Ollama advertises both model tags. It is a preflight check, not proof of successful inference. Next, I suggest running the actual query:

```bash
python query.py --root "$PWD/ragtest" --data "$DEMO_ARTIFACTS" --method local --community_level 2 "What governance issues arise from biometric authentication in virtual worlds?"
```

If the query succeeds, we have evidence that the graph and model pipeline work on your machine. Record elapsed time and check any returned references against the source evidence. If it fails, please send me the traceback.

## 7. Start the Streamlit demonstration

```bash
bash scripts/run_demo.sh
```

Open http://localhost:8501 in your browser. Select the artifact directory, choose **local** search, leave community level at 2 initially, and press Run query. The interface displays actual CLI output and elapsed time. It is a reconstructed version of our October interface, not a recovered copy of the original source.

For a remote Linux server, I suggest keeping Streamlit private and using SSH port forwarding. From your own laptop, run:

```bash
ssh -N -L 8501:127.0.0.1:8501 YOUR_USER@YOUR_SERVER
```

Then open http://localhost:8501 on your laptop. Replace the placeholders with the actual server details. You can share your screen during the meeting. There is no need to publish a public endpoint or expose Ollama.

## 8. The actual demonstration

Start with the biometric authentication question. Explain that the system retrieves graph-linked evidence before generating a response. Then use the questions in [DEMO_QUESTIONS.md](DEMO_QUESTIONS.md). The audience should understand that this is an OPENVERSE governance research framework that builds upon Microsoft GraphRAG, not a legal-advice service. Please distinguish retrieved references from independently validated citations.

I recommend local search for the live session. Global search was substantially slower during our October tests; only show it if you have rehearsed it successfully. If the application is slow, do not present cached or illustrative output as a live result.

## 9. Before the meeting

Please run at least two local queries, confirm the browser interface works and capture genuine screenshots of a successful response. Note the model versions, machine configuration, repository commit and approximate query latency. If you encounter problems, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

I will need to arrange the graph artifact transfer; this guide does not itself include the index or a hosted service. We should complete a rehearsal on your machine before the demonstration.

Best,  
Abdul (Neeil)

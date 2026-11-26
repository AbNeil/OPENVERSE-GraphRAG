# OPENVERSE Graph-RAG: Demo 

**Author: Abdul**    
**Date: 26 November 2026**

Here is how I suggest you set up the system for next week's demonstration. You will need the GitHub source code, a compatible Python environment, Ollama and the original precomputed knowledge graph that I have now recovered and packaged for separate transfer through an authorised channel. See Step 5 for the archive, checksum and import instructions.

## 1. Choose your machine

You can use a Linux server, a GPU workstation or a Mac whatever you like. I suggest 16 GB RAM as a starting point and 32 GB if available, with at least 25 GB of free disk space. These are indicative, not measured requirements. If you use Windows, I suggest WSL2 with Ubuntu and a compatible Ollama setup. The commands below are for bash on Linux or macOS.

The historical demonstration used a Conda environment named `openverse-demo`, GraphRAG 0.3.2, LanceDB 0.11.0 and NumPy 1.26.4. When recovering the graph on my Mac on 26 November 2026, I confirmed that the currently installed environment reports Python 3.10.15 (Conda-forge). The historical environment worked for local queries; we still need to verify the installed package versions and reproduce a successful query on your server.

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

Lukasz, I have now recovered the original OPENVERSE knowledge graph, so you will not need to run the indexing pipeline again.

### 5.1 What I recovered and prepared

I located the original October 2024 indexing output in my local research project, under `ragtest/output/20241018-095127/artifacts/`. I inspected the directory, confirmed that the final and intermediate Parquet datasets were present, and recovered the complete LanceDB entity-description embedding store, including its manifests, transactions and data files.

I also inspected the original `stats.json` and read the Parquet metadata using PyArrow to establish the following statistics directly from the recovered files.

| Metric | Recovered value |
|---|---:|
| Indexed document records | 1 |
| Entity records | 24,782 |
| Relationship records | 23,754 |
| Graph node records | 123,910 |
| Communities | 3,054 |
| Community reports | 3,054 |
| Text units | 3,688 |
| Artifact directory size | Approximately 524 MiB (as reported by du -sh) |
| Original indexing runtime | 87,269.53 seconds (approximately 24 h 14 min) |

The single indexed document record should not be interpreted as the number of original source publications. The source corpus may have been consolidated before indexing, but I have not verified its original composition here. The node-record count is not a count of unique entities. These statistics describe the original indexed snapshot, not a measurement of retrieval quality.

Entity extraction and community report generation accounted for approximately 91.6% of the historical indexing runtime. By transferring the existing artifacts, we can avoid repeating these expensive steps. The time saved on your server will depend on its hardware and configuration.

I generated the following two files:

| File | What it contains |
|---|---|
| `OPENVERSE_Precomputed_KG.zip` | The complete artifacts directory, including all 14 Parquet files, stats.json and the LanceDB vector store. |
| `OPENVERSE_Precomputed_KG.sha256` | SHA-256 checksum of the ZIP archive for transfer verification. |

I tested the ZIP using `unzip -t`, which reported no errors in the compressed data. I generated the checksum file; the recipient-side checksum verification and a fresh end-to-end query test are still required.

I will share these two files separately through an authorised project channel. They are not included in this public GitHub repository. The artifacts may contain source text and derived research data, so please keep them in approved private storage and do not commit or redistribute them publicly.

### 5.2 Receive and verify the files on your server

Please download both files from the private transfer channel. I suggest keeping the received archive outside the cloned Git repository, in a private directory such as `$HOME/openverse-transfer`. If you download them to your laptop first, you can use your institution's approved file transfer method to place them on your server.

On the Linux server:

```bash
mkdir -p "$HOME/openverse-transfer"
chmod 700 "$HOME/openverse-transfer"
# Place both files in this directory before continuing.
cd "$HOME/openverse-transfer"
ls -lh OPENVERSE_Precomputed_KG.zip OPENVERSE_Precomputed_KG.sha256
sha256sum -c OPENVERSE_Precomputed_KG.sha256
unzip -t OPENVERSE_Precomputed_KG.zip
```

On macOS, use `shasum -a 256 -c OPENVERSE_Precomputed_KG.sha256` instead of `sha256sum`.

You should see `OPENVERSE_Precomputed_KG.zip: OK` from the checksum command and a successful ZIP test. If either check fails, please stop and ask me for a fresh copy rather than extracting a potentially corrupted archive.

### 5.3 Extract the original index into the cloned project

Return to the root of the repository you cloned in Step 2. If you cloned it under your home directory, for example:

```bash
cd "$HOME/OPENVERSE-GraphRAG"
```

Adjust this path if you cloned it elsewhere. Then run:

```bash
mkdir -p ragtest/output/20241018-095127

unzip -n "$HOME/openverse-transfer/OPENVERSE_Precomputed_KG.zip" \
  -d ragtest/output/20241018-095127

export DEMO_ARTIFACTS="$PWD/ragtest/output/20241018-095127/artifacts"
ls -lah "$DEMO_ARTIFACTS"
du -sh "$DEMO_ARTIFACTS"
```

Please use a clean destination for the first extraction. The `-n` option prevents overwriting existing files; if you already have a partial or different index there, use a fresh destination rather than mixing versions.

The ZIP already contains the top-level `artifacts/` directory, so do not extract it into another directory named `artifacts/`. After extraction, the relevant structure should be:

```text
OPENVERSE-GraphRAG/
└── ragtest/
    └── output/
        └── 20241018-095127/
            └── artifacts/
                ├── create_final_documents.parquet
                ├── create_final_entities.parquet
                ├── create_final_relationships.parquet
                ├── create_final_nodes.parquet
                ├── create_final_communities.parquet
                ├── create_final_community_reports.parquet
                ├── create_final_text_units.parquet
                ├── stats.json
                ├── lancedb/
                │   └── entity_description_embeddings.lance/
                └── ... (remaining intermediate Parquet files)
```

Please retain the entire directory, particularly the complete LanceDB store. Do not run `index.py`: the purpose of this archive is to reuse the original graph. Please also avoid committing the extracted output or archive to GitHub.

Once this is done, activate the environment and follow Step 6 to run the preflight and an actual local-search query. The presence of the artifacts and the archive integrity checks do not guarantee successful inference; we still need to validate the models, dependencies and graph together on your server.

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

I have now prepared the original graph archive and its checksum. Once you receive them privately, please follow Step 5 and complete the preflight, local query test and Streamlit rehearsal. This repository does not itself include the index or a hosted service.

Best,  
Abdul (Neeil) 


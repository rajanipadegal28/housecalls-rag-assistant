
# HouseCalls RAG Assistant (Databricks Free Edition)

A minimal Retrieval-Augmented Generation (RAG) assistant tailored for HouseCalls-like use cases:
- Eligibility rules
- Claims checklists
- CPT references
- HRA/visit note summarization (extendable)

## Quick Start (Databricks Repos)
1. **Clone** this repo into Databricks: *Repos → Add Repo → paste your Git URL*.
2. Open and run notebook: `databricks/notebooks/00_setup_and_data_ingest.py`.
3. Run: `databricks/notebooks/01_build_index_faiss.py`.
4. Run: `databricks/notebooks/02_rag_answer_housecalls.py` (set `USE_DATABRICKS=True` and `ENDPOINT_NAME` if you have a serving endpoint; otherwise defaults to `gpt4all`).
5. (Optional) Evaluate retrieval: `databricks/notebooks/03_eval_retrieval_quality.py`.

## Notes
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (auto-downloads once per environment)
- **Vector DB**: FAISS (inner product on normalized vectors ≈ cosine)
- **LLM**: Databricks Model Serving *or* local CPU via `gpt4all` (tiny model auto-downloaded by library)
- **Docs**: Place your PDFs/TXTs in `dbfs:/FileStore/housecalls_docs` and rebuild the index.

## Safety
- Answers are grounded in provided context and cite sources.
- If content missing → assistant responds: *“I don’t have that information in my knowledge base.”*

## Repo layout
```
housecalls-rag-assistant/
├─ README.md
├─ .gitignore
├─ requirements.txt
├─ databricks/
│  ├─ notebooks/
│  │  ├─ 00_setup_and_data_ingest.py
│  │  ├─ 01_build_index_faiss.py
│  │  ├─ 02_rag_answer_housecalls.py
│  │  └─ 03_eval_retrieval_quality.py
│  └─ samples/
│     ├─ eligibility_guide.txt
│     ├─ diabetes_claim_checklist.txt
│     └─ cpt_home_wellness.txt
├─ src/
│  ├─ rag/config.py
│  ├─ rag/io.py
│  ├─ rag/chunk.py
│  ├─ rag/embed.py
│  ├─ rag/index_faiss.py
│  └─ rag/rag_pipeline.py
├─ tests/
│  └─ test_chunk_embed.py
└─ tools/
   └─ export_notebooks.sh
```

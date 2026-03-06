
import os
from typing import Dict, Any, List
from .config import DOC_DIR, INDEX_DIR, EMBED_MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, SYSTEM_INSTRUCTIONS
from .io import read_text
from .chunk import chunk_text
from .embed import Embedder
from .index_faiss import FaissIndex

def load_corpus(doc_dir: str):
    out = []
    for name in os.listdir(doc_dir):
        if not name.lower().endswith((".pdf",".txt",".md")):
            continue
        full = os.path.join(doc_dir, name)
        raw = read_text(full)
        chs = chunk_text(raw, CHUNK_SIZE, CHUNK_OVERLAP)
        for idx, ch in enumerate(chs):
            out.append({"source": name, "chunk_index": idx, "text": ch})
    return out

def build_index() -> Dict[str, Any]:
    corpus = load_corpus(DOC_DIR)
    texts = [d["text"] for d in corpus]
    metas = [{"source": d["source"], "chunk_index": d["chunk_index"]} for d in corpus]

    emb = Embedder(EMBED_MODEL_NAME)
    vecs = emb.encode(texts)

    idx = FaissIndex(INDEX_DIR)
    idx.build(vecs, texts, metas)
    idx.persist()
    return {"num_chunks": len(texts)}

def retrieve(query: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
    emb = Embedder(EMBED_MODEL_NAME)
    qv = emb.encode([query])
    idx = FaissIndex(INDEX_DIR)
    idx.load()
    scores, ids = idx.search(qv, top_k)
    hits = []
    for rank, i in enumerate(ids):
        if i < 0: continue
        hits.append({
            "rank": rank+1,
            "score": float(scores[rank]),
            "source": idx.metas[i]["source"],
            "chunk_index": idx.metas[i]["chunk_index"],
            "text": idx.texts[i]
        })
    return hits

def make_prompt(question: str, hits: List[Dict[str,Any]]) -> str:
    ctx = "

".join([f"Source: {h['source']} (chunk {h['chunk_index']})
---
{h['text']}" for h in hits])
    return f"""{SYSTEM_INSTRUCTIONS}

Context:
{ctx}

Question: {question}

Answer using only the context, and cite sources in parentheses.
"""

def call_llm_databricks(prompt: str, endpoint_name: str):
    from mlflow.deployments import get_deploy_client
    client = get_deploy_client("databricks")
    resp = client.predict(endpoint=endpoint_name, inputs={"messages":[{"role":"user","content":prompt}]})
    try:
        return resp["choices"][0]["message"]["content"]
    except Exception:
        return str(resp)

def call_llm_gpt4all(prompt: str):
    from gpt4all import GPT4All
    model = GPT4All("ggml-gpt4all-j-v1.3-groovy")
    return model.generate(prompt)

def answer(question: str, top_k: int = TOP_K, use_databricks=False, endpoint_name=""):
    hits = retrieve(question, top_k=top_k)
    if not hits:
        return {"answer":"I don’t have that information in my knowledge base.", "hits":[]}
    prompt = make_prompt(question, hits)
    if use_databricks and endpoint_name:
        ans = call_llm_databricks(prompt, endpoint_name)
    else:
        ans = call_llm_gpt4all(prompt)
    return {"answer": ans, "hits": hits}

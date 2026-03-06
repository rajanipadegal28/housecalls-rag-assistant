
# Databricks notebook source
import sys
repo_root = "/Workspace/Repos/housecalls-rag-assistant"  # adjust if your repo path differs
sys.path.append(f"{repo_root}/src")

from rag.rag_pipeline import answer

# ---- Option A: Databricks Model Serving endpoint (if available)
USE_DATABRICKS = False
ENDPOINT_NAME = "YOUR_ENDPOINT_NAME"  # e.g., "llama-3-8b-instruct"

def ask(q):
    out = answer(q, top_k=5, use_databricks=USE_DATABRICKS, endpoint_name=ENDPOINT_NAME)
    print("Q:", q)
    print("A:", out["answer"])
    print("Sources:", list({h['source'] for h in out['hits']}))
    print("-"*60)

ask("What are the eligibility rules for a HouseCalls visit?")
ask("Which CPT code should we use for a home wellness visit?")
ask("What documents are required for a diabetes claim?")

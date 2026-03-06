
# Databricks notebook source
import sys
repo_root = "/Workspace/Repos/housecalls-rag-assistant"  # adjust if your repo path differs
sys.path.append(f"{repo_root}/src")

from rag.rag_pipeline import retrieve

gold = [
    ("What are the eligibility rules for a HouseCalls visit?", ["eligibility_guide.txt"]),
    ("Which CPT code should we use for a home wellness visit?", ["cpt_home_wellness.txt"]),
    ("What documents are required for a diabetes claim?", ["diabetes_claim_checklist.txt"]),
]

TOP_K = 3
correct = 0

for q, expected_sources in gold:
    hits = retrieve(q, top_k=TOP_K)
    top_sources = [h["source"] for h in hits]
    hit = any(src in top_sources for src in expected_sources)
    correct += 1 if hit else 0
    print(f"Q: {q}
Top sources: {top_sources}
Expected any of: {expected_sources}
OK? {hit}
{'-'*50}")

print(f"Retrieval@{TOP_K}: {correct}/{len(gold)} correct")

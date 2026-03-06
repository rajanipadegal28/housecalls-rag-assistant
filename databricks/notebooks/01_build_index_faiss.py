
# Databricks notebook source
import sys
repo_root = "/Workspace/Repos/housecalls-rag-assistant"  # adjust if your repo path differs
sys.path.append(f"{repo_root}/src")

from rag.rag_pipeline import build_index
res = build_index()
print("Index build complete:", res)

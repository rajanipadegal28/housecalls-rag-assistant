
# Databricks notebook source
# Install libraries for this session
%pip install -q sentence-transformers faiss-cpu pypdf gpt4all scikit-learn numpy

dbutils.library.restartPython()

# COMMAND ----------
# Create DBFS folders & copy samples
import os, shutil
from pathlib import Path

DOC_DIR = "/dbfs/FileStore/housecalls_docs"
SAMPLES = "/Workspace/Repos/housecalls-rag-assistant/databricks/samples"  # adjust if your repo path differs
os.makedirs(DOC_DIR, exist_ok=True)

for name in ["eligibility_guide.txt","diabetes_claim_checklist.txt","cpt_home_wellness.txt"]:
    src = f"{SAMPLES}/{name}"
    dst = f"{DOC_DIR}/{name}"
    shutil.copy(src, dst)

print("Docs ready at:", DOC_DIR)
display(dbutils.fs.ls("dbfs:/FileStore/housecalls_docs"))

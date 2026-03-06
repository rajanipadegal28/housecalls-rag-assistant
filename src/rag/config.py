
import os

# DBFS locations
DOC_DIR = os.environ.get("HC_DOC_DIR", "/dbfs/FileStore/housecalls_docs")
INDEX_DIR = os.environ.get("HC_INDEX_DIR", "/dbfs/FileStore/housecalls_index")

# Embedding model
EMBED_MODEL_NAME = os.environ.get("HC_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Chunking
CHUNK_SIZE = int(os.environ.get("HC_CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.environ.get("HC_CHUNK_OVERLAP", "120"))

# Retrieval
TOP_K = int(os.environ.get("HC_TOP_K", "5"))

SYSTEM_INSTRUCTIONS = """You are the HouseCalls Assistant.
Answer ONLY using the provided context. If the answer is not present, say:
"I don’t have that information in my knowledge base."
Cite source file names in parentheses when relevant.
Be concise, medically safe, and policy-accurate.
"""

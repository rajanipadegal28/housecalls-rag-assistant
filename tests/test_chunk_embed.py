
from src.rag.chunk import chunk_text

def test_chunk_text_basic():
    txt = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text(txt, size=10, overlap=2)
    assert len(chunks) >= 3
    assert chunks[0].startswith("abcdefghij") or len(chunks[0]) == 10

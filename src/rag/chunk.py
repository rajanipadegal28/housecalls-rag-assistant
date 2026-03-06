
from typing import List

def chunk_text(text: str, size: int, overlap: int) -> List[str]:
    text = text.strip()
    if not text: return []
    out, i, n = [], 0, len(text)
    while i < n:
        j = min(i + size, n)
        ch = text[i:j].strip()
        if ch: out.append(ch)
        if j == n: break
        i = max(0, j - overlap)
    return out

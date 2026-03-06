
from pathlib import Path
from pypdf import PdfReader

def read_text(path: str) -> str:
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(str(p))
        return "
".join([page.extract_text() or "" for page in reader.pages])
    if ext in [".txt", ".md"]:
        return p.read_text(encoding="utf-8", errors="ignore")
    return ""

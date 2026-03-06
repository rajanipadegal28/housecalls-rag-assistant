
import os, json
import faiss

class FaissIndex:
    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        self.index = None
        self.texts = None
        self.metas = None

    def build(self, embeddings, texts, metas):
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)
        self.texts = texts
        self.metas = metas

    def persist(self):
        faiss.write_index(self.index, f"{self.index_dir}/faiss.index")
        import json
        with open(f"{self.index_dir}/texts.json", "w", encoding="utf-8") as f:
            json.dump(self.texts, f, ensure_ascii=False)
        with open(f"{self.index_dir}/metas.json", "w", encoding="utf-8") as f:
            json.dump(self.metas, f, ensure_ascii=False, indent=2)

    def load(self):
        self.index = faiss.read_index(f"{self.index_dir}/faiss.index")
        import json
        with open(f"{self.index_dir}/texts.json", "r", encoding="utf-8") as f:
            self.texts = json.load(f)
        with open(f"{self.index_dir}/metas.json", "r", encoding="utf-8") as f:
            self.metas = json.load(f)

    def search(self, query_vec, top_k: int):
        scores, ids = self.index.search(query_vec, top_k)
        return scores[0], ids[0]

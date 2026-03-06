
import numpy as np
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
    def encode(self, texts):
        vecs = self.model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
        return np.asarray(vecs, dtype="float32")

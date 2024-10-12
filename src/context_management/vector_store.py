import faiss
import numpy as np
from typing import List, Dict

class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.id_to_text = {}

    def add_text(self, text: str, vector: np.ndarray):
        if vector.shape[0] != self.dimension:
            raise ValueError(f"Vector dimension {vector.shape[0]} does not match index dimension {self.dimension}")
        id = self.index.ntotal
        self.index.add(vector.reshape(1, -1))
        self.id_to_text[id] = text

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, float]]:
        distances, indices = self.index.search(query_vector.reshape(1, -1), k)
        results = [{"text": self.id_to_text[int(idx)], "distance": float(dist)} 
                   for idx, dist in zip(indices[0], distances[0]) if idx != -1]
        return results

import faiss
import numpy as np

class VectorStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)
        self.clauses = []

    def add(self, embeddings, clauses):

        self.index.add(np.array(embeddings))
        self.clauses.extend(clauses)

    def search(self, query_embedding, k=5):
        D, I = self.index.search(np.array(query_embedding).astype('float32'), k)
        results = []
        for idx, i in enumerate(I[0]):
            if i < len(self.clauses):
                results.append({
                    "text": self.clauses[i],
                    "score": float(D[0][idx])
                })
        return results
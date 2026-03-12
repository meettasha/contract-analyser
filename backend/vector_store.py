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

        D, I = self.index.search(query_embedding, k)

        results = []

        for i in I[0]:
            results.append(self.clauses[i])

        return results
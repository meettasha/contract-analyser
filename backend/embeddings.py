from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(clauses):

    embeddings = model.encode(clauses).astype('float32')

    return embeddings
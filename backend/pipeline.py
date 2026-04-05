from .utils import extract_text
from .clause_parser import split_clauses
from .embeddings import generate_embeddings, model
from .vector_store import VectorStore
from .llm import analyze_clause, analyze_contract, answer_query

class ContractPipeline:

    def __init__(self):
        self.vector_db = None

    def process_document(self, file_path):

        text = extract_text(file_path)

        clauses = split_clauses(text)

        embeddings = generate_embeddings(clauses)

        self.vector_db = VectorStore(len(embeddings[0]))

        self.vector_db.add(embeddings, clauses)

        analysis = []

        for clause in clauses[:10]:  # limit for speed
            result = analyze_clause(clause)

            analysis.append({
                "clause": clause,
                "analysis": result
            })

        summary = analyze_contract(clauses)

        return {
            "analysis": analysis,
            "summary": summary
        }

    def query(self, question):

        query_emb = model.encode([question])

        relevant = self.vector_db.search(query_emb)

        context = "\n".join([r["text"] for r in relevant])

        answer = answer_query(question, context)

        return answer

from .llm import query_ollama

obligation_words = ["shall", "must", "required to", "responsible for"]

def extract_obligations(clauses):
    # Keyword-based (fast, no LLM)
    obligations = []
    for clause in clauses:
        for word in obligation_words:
            if word in clause.lower():
                obligations.append(clause)
                break
    
    # LLM-powered structured extraction
    if clauses:
        context = "\n".join(clauses[:15])
        prompt = f"""
You are a legal AI assistant. Extract all obligations from this contract.
For each obligation state:
- Who is responsible
- What they must do
- Any deadline or condition

Contract:
{context}

Obligations:
"""
        llm_obligations = query_ollama(prompt)
        return {
            "keyword_matches": obligations,
            "llm_extraction": llm_obligations
        }
    
    return {"keyword_matches": obligations, "llm_extraction": ""}
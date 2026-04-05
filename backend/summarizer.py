from .llm import query_ollama

def summarize_contract(clauses):
    # If contract is short enough, do it in one shot
    if len(clauses) <= 20:
        context = "\n".join(clauses)
        return _summarize_chunk(context)
    
    # Otherwise, summarize in chunks then combine
    chunk_summaries = []
    for i in range(0, len(clauses), 20):
        chunk = clauses[i:i+20]
        context = "\n".join(chunk)
        chunk_summary = _summarize_chunk(context)
        chunk_summaries.append(chunk_summary)
    
    # Final pass — summarize all chunk summaries together
    combined = "\n".join(chunk_summaries)
    final_prompt = f"""
You are a legal AI assistant. Below are summaries of different sections of a contract.
Combine them into one final coherent summary covering:
- Key parties
- Main purpose
- Key obligations
- Duration
- Any unusual or risky terms

Sections:
{combined}

Final Summary:
"""
    return query_ollama(final_prompt)


def _summarize_chunk(context):
    prompt = f"""
You are a legal AI assistant. Summarize this section of a contract concisely.
Highlight: key parties, main purpose, obligations, and any unusual terms.

Contract Section:
{context}

Summary:
"""
    return query_ollama(prompt)
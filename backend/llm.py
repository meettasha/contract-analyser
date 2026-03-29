import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def query_ollama(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def analyze_clause(clause):

    prompt = f"""
    You are a legal AI assistant.

    Analyze this clause:
    {clause}

    Return:
    - Risk Level (Low/Medium/High)
    - Explanation
    """

    return query_ollama(prompt)


def analyze_contract(clauses):

    context = "\n".join(clauses[:20])

    prompt = f"""
    You are a legal AI assistant.

    Analyze this contract:

    {context}

    Provide:
    - Summary
    - Key obligations
    - Missing protections
    """

    return query_ollama(prompt)


def answer_query(query, context):

    prompt = f"""
    Answer the question using the contract context.

    Context:
    {context}

    Question:
    {query}
    """

    return query_ollama(prompt)

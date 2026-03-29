import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def call_llm(prompt):

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
    You are a legal expert AI.

    Analyze this contract clause:

    {clause}

    Return in JSON:
    {{
        "risk_level": "Low/Medium/High",
        "issue": "...",
        "suggestion": "..."
    }}
    """

    return call_llm(prompt)


def analyze_contract(clauses):

    context = "\n".join(clauses[:20])

    prompt = f"""
    Analyze this contract:

    {context}

    Return:
    - Summary
    - Key obligations
    - Missing protections
    """

    return call_llm(prompt)

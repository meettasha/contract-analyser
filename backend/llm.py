import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def call_llm(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json()["response"]

    except Exception as e:
        return f"LLM_ERROR: {str(e)}"


# Safe JSON parser
def parse_json(output):
    try:
        return json.loads(output)
    except:
        return {
            "raw_output": output,
            "error": "Failed to parse JSON"
        }


# Clause-level analysis
def analyze_clause(clause):
    prompt = f"""
    You are a legal expert AI.

    Analyze this contract clause:

    {clause}

    STRICTLY return valid JSON:
    {{
        "risk_level": "Low/Medium/High",
        "issue": "...",
        "suggestion": "..."
    }}
    """

    output = call_llm(prompt)
    return parse_json(output)


# Contract-level analysis
def analyze_contract(clauses):
    context = "\n".join(clauses[:15])  # keep smaller for stability

    prompt = f"""
    You are a legal expert AI.

    Analyze this contract:

    {context}

    STRICTLY return valid JSON:
    {{
        "summary": "...",
        "key_obligations": ["...", "..."],
        "missing_protections": ["...", "..."]
    }}
    """

    output = call_llm(prompt)
    return parse_json(output)

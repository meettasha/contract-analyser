from .llm import query_ollama

risk_keywords = [
    "unlimited liability", "indemnify", "terminate without notice",
    "exclusive rights", "penalty", "liquidated damages"
]

def detect_risk(clause):
    clause_lower = clause.lower()
    for keyword in risk_keywords:
        if keyword in clause_lower:
            return "High Risk"
    return "Low Risk"

def detect_risk_with_reason(clause):
    prompt = f"""
You are a legal risk analyst. Analyze this contract clause:

"{clause}"

Respond in this exact format:
Risk Level: Low/Medium/High
Reason: (one sentence explanation)
"""
    return query_ollama(prompt)
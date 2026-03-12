risk_keywords = [
    "unlimited liability",
    "indemnify",
    "terminate without notice",
    "exclusive rights",
    "penalty",
    "liquidated damages"
]

def detect_risk(clause):

    clause_lower = clause.lower()

    for keyword in risk_keywords:

        if keyword in clause_lower:

            return "High Risk"

    return "Low Risk"
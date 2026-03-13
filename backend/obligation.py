obligation_words = [
    "shall",
    "must",
    "required to",
    "responsible for"
]

def extract_obligations(clauses):

    obligations = []

    for clause in clauses:

        for word in obligation_words:

            if word in clause.lower():

                obligations.append(clause)

                break

    return obligations
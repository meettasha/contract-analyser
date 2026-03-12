import re

def split_clauses(text):

    clauses = re.split(r'\n\d+\.', text)

    clauses = [c.strip() for c in clauses if len(c.strip()) > 40]

    return clauses
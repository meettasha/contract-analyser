from fastapi import FastAPI, UploadFile
import shutil

from utils import extract_text
from clause_parser import split_clauses
from embeddings import generate_embeddings
from vector_store import VectorStore
from analyzer import detect_risk
from obligations import extract_obligations

app = FastAPI()

vector_db = None

@app.post("/upload")

async def upload_contract(file: UploadFile):

    path = f"data/contracts/{file.filename}"

    with open(path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    text = extract_text(path)

    clauses = split_clauses(text)

    embeddings = generate_embeddings(clauses)

    global vector_db

    vector_db = VectorStore(len(embeddings[0]))

    vector_db.add(embeddings, clauses)

    analysis = []

    for clause in clauses:

        analysis.append({

            "clause": clause,

            "risk": detect_risk(clause)

        })

    obligations = extract_obligations(clauses)

    return {

        "analysis": analysis,

        "obligations": obligations

    }


@app.get("/search")

def search_contract(query: str):

    from embeddings import model

    query_embedding = model.encode([query])

    results = vector_db.search(query_embedding)

    return {"results": results}
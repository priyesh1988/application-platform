from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.client import ingest, rag_answer

router = APIRouter()

class IngestPayload(BaseModel):
    source: str
    text: str

@router.post("/ingest")
def ingest_doc(p: IngestPayload):
    return ingest(p.text, p.source)

class QueryPayload(BaseModel):
    question: str

@router.post("/query")
def query(p: QueryPayload):
    return {"answer": rag_answer(p.question)}

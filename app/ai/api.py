from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.risk import risk_score
from app.ai.summaries import incident_summary
from app.rag.client import rag_answer

router = APIRouter()

class RiskPayload(BaseModel):
    payload: dict

@router.post("/risk-score")
def api_risk(req: RiskPayload):
    return risk_score(req.payload)

class ChatPayload(BaseModel):
    question: str

@router.post("/chat")
def chat(req: ChatPayload):
    # RAG-first answer; falls back to generic response if KB empty
    return {"answer": rag_answer(req.question)}

class IncidentPayload(BaseModel):
    context: dict  # logs/metrics/traces pointers, impact, timeframe
    audience: str = "customer"  # customer|exec|engineer

@router.post("/incident-summary")
def incident(req: IncidentPayload):
    return incident_summary(req.context, req.audience)

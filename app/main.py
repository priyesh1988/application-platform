import os
from fastapi import FastAPI, Depends
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.security.auth import require_auth
from app.deployments.api import router as deployments_router
from app.ai.api import router as ai_router
from app.rag.api import router as rag_router
from app.db.session import init_db
from app.telemetry.otel import instrument

app = FastAPI(title="Application Platform — AI/LLM Edition", version="0.1.0")

REQ = Counter("http_requests_total", "Total HTTP requests", ["path", "method"])

@app.on_event("startup")
def _startup():
    init_db()
    instrument(app)

@app.middleware("http")
async def metrics_mw(request, call_next):
    resp = await call_next(request)
    REQ.labels(path=request.url.path, method=request.method).inc()
    return resp

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Routers
app.include_router(deployments_router, prefix="/deployments", dependencies=[Depends(require_auth)])
app.include_router(ai_router, prefix="/ai", dependencies=[Depends(require_auth)])
app.include_router(rag_router, prefix="/rag", dependencies=[Depends(require_auth)])

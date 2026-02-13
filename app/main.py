from fastapi import FastAPI
from app.db.models import Base
from app.db.session import engine
from app.api.routes_request import router as request_router
from app.api.routes_status import router as status_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Application Platform")

app.include_router(request_router)
app.include_router(status_router)

@app.get("/health")
def health():
    return {"status": "ok"}


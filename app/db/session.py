import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base

_engine = None
SessionLocal = None

def init_db():
    global _engine, SessionLocal
    if _engine:
        return
    url = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@postgres:5432/platform")
    _engine = create_engine(url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    Base.metadata.create_all(bind=_engine)

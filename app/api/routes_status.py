from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import require_auth
from app.db.session import get_db
from app.db.models import DeploymentRequest

router = APIRouter(prefix="/deployments")

@router.get("/{id}")
def get_status(id: int, auth=Depends(require_auth), db: Session = Depends(get_db)):
    dr = db.query(DeploymentRequest).filter_by(id=id).first()
    return dr


from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import require_auth
from app.db.session import get_db
from app.db.models import DeploymentRequest
from app.policy.engine import evaluate
from app.render.k8s_manifests import namespace_manifest, deployment_manifest

router = APIRouter(prefix="/deployments")

class DeployRequest(BaseModel):
    app_name: str
    environment: str
    data_classification: str
    exposure: str
    config: dict

@router.post("/request")
def request_deploy(req: DeployRequest, auth=Depends(require_auth), db: Session = Depends(get_db)):
    decision = evaluate(req.model_dump())

    dr = DeploymentRequest(
        app_name=req.app_name,
        environment=req.environment,
        data_classification=req.data_classification,
        exposure=req.exposure,
        config=req.config,
        status="APPROVED" if decision["allowed"] else "DENIED"
    )

    db.add(dr)
    db.commit()

    return {
        "status": dr.status,
        "policy": decision,
        "namespace": namespace_manifest(req.app_name, req.environment),
        "deployment": deployment_manifest(req.app_name, req.environment, req.config)
    }


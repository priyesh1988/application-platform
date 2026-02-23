from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.policy.engine import evaluate_policy
from app.ai.risk import risk_score
from app.db.repo import save_deployment_request
from app.eventing.kafka_pub import publish_event

router = APIRouter()

class DeploymentConfig(BaseModel):
    image: str
    replicas: int = 1

class DeploymentRequest(BaseModel):
    app_name: str
    environment: str = Field(pattern="^(dev|stage|prod)$")
    data_classification: str = "internal"
    exposure: str = "internal"
    config: DeploymentConfig

@router.post("/request")
def request_deployment(req: DeploymentRequest):
    policy = evaluate_policy(req.model_dump())
    risk = risk_score(req.model_dump())

    decision = "APPROVED"
    if not policy["allowed"] or risk["level"] == "HIGH":
        decision = "DENIED"

    record_id = save_deployment_request(req.model_dump(), policy, risk, decision)
    publish_event("deployments", {"id": record_id, "decision": decision, "app": req.app_name, "env": req.environment})

    # GitOps-ready manifests (simple example)
    manifests = {
        "namespace": {"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": f"{req.app_name}-{req.environment}"}},
        "deployment": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": req.app_name, "namespace": f"{req.app_name}-{req.environment}"},
            "spec": {
                "replicas": req.config.replicas,
                "selector": {"matchLabels": {"app": req.app_name}},
                "template": {
                    "metadata": {"labels": {"app": req.app_name}},
                    "spec": {"containers": [{"name": req.app_name, "image": req.config.image}]},
                },
            },
        },
    }

    return {"id": record_id, "status": decision, "policy": policy, "risk": risk, "manifests": manifests}

import json
from app.db.session import SessionLocal
from app.db.models import DeploymentRequest

def save_deployment_request(req: dict, policy: dict, risk: dict, decision: str) -> int:
    db = SessionLocal()
    try:
        row = DeploymentRequest(
            decision=decision,
            request_json=json.dumps(req),
            policy_json=json.dumps(policy),
            risk_json=json.dumps(risk),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row.id
    finally:
        db.close()

from fastapi import Header, HTTPException
from app.core.config import settings

def require_auth(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ")[1]
    if token != settings.jwt_dev_token:
        raise HTTPException(status_code=403, detail="Invalid token")

    return {
        "sub": "demo-user",
        "org_id": "chase",
        "groups": ["platform"]
    }


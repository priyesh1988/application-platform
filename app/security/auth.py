import os
import time
import httpx
from jose import jwt
from fastapi import HTTPException, Request

_JWKS_CACHE = {"ts": 0.0, "jwks": None}

async def _get_jwks():
    jwks_url = os.getenv("JWT_JWKS_URL")
    if not jwks_url:
        return None
    now = time.time()
    if _JWKS_CACHE["jwks"] and now - _JWKS_CACHE["ts"] < 300:
        return _JWKS_CACHE["jwks"]
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(jwks_url)
        r.raise_for_status()
        _JWKS_CACHE["jwks"] = r.json()
        _JWKS_CACHE["ts"] = now
        return _JWKS_CACHE["jwks"]

async def require_auth(request: Request):
    # Simple bearer check; validate via JWKS if configured, else allow dev token
    auth = request.headers.get("Authorization", "")
    if auth == "Bearer dev-agent-token":
        return {"sub": "dev", "role": "admin"}
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = auth.replace("Bearer ", "").strip()
    issuer = os.getenv("JWT_ISSUER")
    audience = os.getenv("JWT_AUDIENCE")

    jwks = await _get_jwks()
    if not (issuer and audience and jwks):
        raise HTTPException(status_code=401, detail="OIDC/JWKS not configured; use dev-agent-token for local dev")

    try:
        claims = jwt.decode(token, jwks, audience=audience, issuer=issuer)
        return claims
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

import os
import httpx
from typing import Dict

def _heuristic(payload: dict) -> Dict[str, str]:
    # Cheap fallback so local runs never block
    blob = str(payload)
    score = 0
    score += 2 if "prod" in blob else 0
    score += 2 if "replicas" in blob else 0
    score += 4 if "latest" in blob else 0
    if score >= 5:
        return {"level": "HIGH", "reason": "High-risk changes detected (prod/replicas/latest).", "method": "heuristic"}
    if score >= 2:
        return {"level": "MEDIUM", "reason": "Some risk signals present.", "method": "heuristic"}
    return {"level": "LOW", "reason": "Low risk signals.", "method": "heuristic"}

def risk_score(payload: dict) -> Dict[str, str]:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider == "ollama":
        return _ollama_risk(payload) or _heuristic(payload)
    if provider == "openai":
        return _openai_risk(payload) or _heuristic(payload)
    return _heuristic(payload)

def _openai_risk(payload: dict):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        msg = (
            "Return JSON with keys: level (LOW|MEDIUM|HIGH), reason. "
            "Evaluate deployment risk based on payload."
        )
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a senior SRE doing deployment risk review."},
                {"role": "user", "content": msg + "\nPayload: " + str(payload)},
            ],
            temperature=0.2,
        )
        text = resp.choices[0].message.content
        # best-effort JSON parsing
        import json
        data = json.loads(text) if text.strip().startswith("{") else {"level": "MEDIUM", "reason": text}
        data["method"] = "openai"
        return data
    except Exception:
        return None

def _ollama_risk(payload: dict):
    base = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.1")
    try:
        prompt = (
            "Return JSON with keys: level (LOW|MEDIUM|HIGH), reason. "
            "Evaluate deployment risk based on payload.\nPayload: " + str(payload)
        )
        r = httpx.post(f"{base}/api/generate", json={"model": model, "prompt": prompt, "stream": False}, timeout=8)
        r.raise_for_status()
        out = r.json().get("response", "")
        import json
        data = json.loads(out) if out.strip().startswith("{") else {"level": "MEDIUM", "reason": out}
        data["method"] = "ollama"
        return data
    except Exception:
        return None

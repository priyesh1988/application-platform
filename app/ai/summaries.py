import os

def incident_summary(context: dict, audience: str):
    # Deterministic fallback that is always safe to run locally
    base = {
        "customer": "We identified an issue impacting some requests and are applying mitigations. We'll share updates as we validate stability.",
        "exec": "Incident detected; mitigation in progress. Impact and root cause are being validated. Next update in 30 minutes.",
        "engineer": "Start with recent deploys, error budget burn, and top error traces; check policy gates and dependency health.",
    }
    # Optional OpenAI enhancement
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {"audience": audience, "summary": base.get(audience, base["customer"]), "method": "template"}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        prompt = (
            f"Write a concise incident update for audience={audience}. "
            "Be accurate, avoid speculation, include impact + next action + ETA for next update. "
            f"Context: {context}"
        )
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "system", "content": "You are an incident communications lead."},
                      {"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return {"audience": audience, "summary": resp.choices[0].message.content, "method": "openai"}
    except Exception:
        return {"audience": audience, "summary": base.get(audience, base["customer"]), "method": "template"}

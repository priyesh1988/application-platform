def evaluate_policy(payload: dict) -> dict:
    # Minimal policies to keep repo runnable; extend with OPA/Kyverno in /policy
    results = []

    img = payload.get("config", {}).get("image", "")
    env = payload.get("environment", "dev")

    # Disallow :latest in prod
    if env == "prod" and (":latest" in img or img.endswith(":latest")):
        results.append({"rule": "no_latest_in_prod", "ok": False, "message": "prod deployments must not use :latest"})
    else:
        results.append({"rule": "no_latest_in_prod", "ok": True, "message": "OK"})

    allowed = all(r["ok"] for r in results)
    return {"allowed": allowed, "results": results}

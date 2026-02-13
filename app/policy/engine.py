from app.policy.rules import prod_requires_resources, restricted_blocks_public

def evaluate(req):
    results = []
    allowed = True

    for rule in [prod_requires_resources, restricted_blocks_public]:
        ok, msg = rule(req)
        results.append({"rule": rule.__name__, "ok": ok, "message": msg})
        if not ok:
            allowed = False

    return {"allowed": allowed, "results": results}


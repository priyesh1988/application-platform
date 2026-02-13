def prod_requires_resources(req):
    if req["environment"] == "prod":
        if not req["config"].get("resources"):
            return False, "Prod requires resource limits"
    return True, "OK"

def restricted_blocks_public(req):
    if req["data_classification"] == "restricted" and req["exposure"] == "public":
        return False, "Restricted data cannot be public"
    return True, "OK"


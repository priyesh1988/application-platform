def namespace_manifest(app, env):
    return {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {"name": f"{app}-{env}"}
    }

def deployment_manifest(app, env, config):
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": app, "namespace": f"{app}-{env}"},
        "spec": {
            "replicas": config.get("replicas", 2),
            "template": {
                "spec": {
                    "containers": [{
                        "name": app,
                        "image": config["image"]
                    }]
                }
            }
        }
    }


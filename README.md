# Application Platform

## Software-Defined Deployment Service

---

## What It Is

Application Platform is an internal deployment control plane that enables teams to provision compliant, production-ready environments through a single API.

It standardizes application deployment by combining:

- Kubernetes runtime provisioning (namespace and deployment)
- Policy-as-code guardrails
- GitOps-ready manifest generation
- Automated audit logging

In simple terms:

> "Request a compliant environment — and the platform handles the rest."

---

## How To Use

### Start the platform

```bash
docker compose up --build

curl -X POST http://localhost:8000/deployments/request \
  -H "Authorization: Bearer dev-agent-token" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name":"demoapp",
    "environment":"dev",
    "data_classification":"internal",
    "exposure":"internal",
    "config":{
      "image":"registry.chase.internal/demoapp:1.0",
      "replicas":2
    }
  }'

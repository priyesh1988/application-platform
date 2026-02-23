# Application Platform — AI + LLM Upgrade Edition

This is a **GitHub-uploadable repo** that extends the core **Application Platform** idea (software-defined deployment control plane) with **heavy AI / heavy LLM** capabilities focused on:

- **Developer Experience (DX)**: faster onboarding, fewer mysteries, self-serve troubleshooting
- **Customer Experience (CX)**: fewer incidents, faster comms, predictable rollouts, transparent reliability

> Repo inspiration: https://github.com/priyesh1988/application-platform (structure + intent). citeturn4view2

---

## What’s new (high-signal upgrades)

### DX Upgrades (Developer Experience)
1) **LLM PR/Commit Risk Scoring**
- Turns a diff + runtime context into **LOW/MED/HIGH** deployment risk with an explanation.
- Blocks risky rollouts automatically when policy thresholds are exceeded.

2) **ChatOps “Ask the Platform”**
- Ask in plain English: “Why did stage fail?” “Which policy blocked prod?”
- Response includes: **root cause**, **fix**, **next best action**.

3) **RAG-powered Runbook Search**
- Indexes runbooks, policies, past incidents into a Vector DB.
- Answer questions with citations (internal docs), not hallucinations.

4) **Auto-Generated Release Notes**
- Converts commit history into release notes (customer-safe + engineer-deep versions).

### CX Upgrades (Customer Experience)
1) **Incident Summaries + Timeline**
- Auto-drafts customer-facing incident updates from traces/logs/alerts.
- Creates a clean timeline, impact assessment, and status updates.

2) **Reliability “Confidence Score”**
- Combines SLO error budget burn + recent deploy risk + change rate
- Produces a customer-facing “confidence meter” for rollouts.

3) **Progressive Delivery by Default**
- Canary + blue/green using Argo Rollouts.
- Automatic promotion gates driven by SLO and risk score.

---

## Local quickstart (full stack)

### 1) Configure env
Copy `.env.example` → `.env` and set keys you want.

```bash
cp .env.example .env
```

### 2) Run everything
```bash
docker compose up --build
```

### 3) Open
- API (FastAPI): http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Jaeger (traces): http://localhost:16686
- Qdrant (vector DB): http://localhost:6333

---

## API endpoints (high value)
- `POST /deployments/request` — request an environment (with policy + AI risk scoring)
- `POST /ai/risk-score` — score risk for commit/diff payload
- `POST /ai/chat` — chat with platform (RAG + tools)
- `POST /ai/incident-summary` — generate customer/exec/engineer incident summaries
- `POST /rag/ingest` — ingest runbooks/policies into vector store
- `GET  /metrics` — Prometheus metrics endpoint

---

## Production notes
- Replace sample auth with real OIDC issuer + JWKS
- Move secrets to Vault / AWS Secrets Manager
- Back vector store with durable storage
- Split “api” vs “worker” services (Celery/Arq) for async AI workloads
- Use IRSA/OIDC for AWS in CI/CD (already scaffolded)

---

## Repo layout
- `app/` FastAPI control plane + auth + policy + deployment workflow
- `ai/` LLM + embeddings + RAG + summarizers
- `observability/` OTEL collector configs, dashboards
- `policy/` OPA + Kyverno examples
- `gitops/` ArgoCD + Argo Rollouts progressive delivery
- `tenancy/` namespace isolation + quotas + RBAC templates
- `infra/terraform/` multi-region scaffolding (optional)

---


### Note
- Postgres is mapped to host port **5433** to avoid conflicts.
- Traces export directly to **Jaeger OTLP** (no otel-collector in local compose).

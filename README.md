# 🚀 Application Platform — Infrastructure Intelligence

This is a **GitHub‑uploadable repo** that extends the core **Application Platform** idea  
(software‑defined deployment control plane) with **AI capabilities** focused on:

- 🧑‍💻 Developer Experience (DX): faster onboarding, fewer mysteries, self‑serve troubleshooting  
- 🤝 Customer Experience (CX): fewer incidents, faster comms, predictable rollouts, transparent reliability  

---

## ⚡ Local Quickstart (Full Stack)

### 1) Configure Environment

```bash
cp .env.example .env
```

Modify `.env` with your desired keys.

### 2) Run Everything

```bash
docker compose up --build
```

### 3) Open Interfaces

| Component | URL |
|-----------|-----|
| API (FastAPI) | http://localhost:8000/docs |
| Grafana | http://localhost:3000 (admin/admin) |
| Prometheus | http://localhost:9090 |
| Jaeger (Traces) | http://localhost:16686 |
| Qdrant (Vector DB) | http://localhost:6333 |

---

## 📦 Example: AI‑Powered Deployment Request (End‑to‑End)

Assume your stack is running at:

`http://localhost:8001`

### Step 1 — Developer Submits Deployment Request

```bash
curl -X POST http://localhost:8001/deploy   -H "Content-Type: application/json"   -d '{
    "app_name": "payments-service",
    "environment": "prod",
    "replicas": 4,
    "cpu_request": "500m",
    "memory_request": "512Mi",
    "exposure": "external",
    "data_classification": "pii"
  }'
```

---

### Step 2 — What Happens Internally

#### 1️⃣ AI Risk Engine (LLM Scoring)

The platform sends a structured prompt to the LLM:

- Environment: prod  
- Exposure: external  
- Data: PII  
- Replicas: 4  
- CPU: 500m  
- Memory: 512Mi  

Example LLM Response:

```json
{
  "risk_level": "HIGH",
  "reasons": [
    "PII workload exposed externally in production",
    "Resource requests may be under-provisioned for PII handling"
  ],
  "recommendations": [
    "Enable WAF",
    "Increase memory to 1Gi",
    "Enable network policy isolation"
  ]
}
```

#### 2️⃣ Policy Enforcement Layer

- HIGH risk → manual approval or auto-adjust config  
- LOW risk → auto-approve  

#### 3️⃣ Vector DB (RAG Context)

The system queries Qdrant:

“Have we deployed similar PII workloads before?”

Historical deployments & failure traces are fetched to inform AI scoring.

#### 4️⃣ Kafka Event Emission

```json
{
  "event_type": "deployment_requested",
  "app": "payments-service",
  "risk": "HIGH",
  "timestamp": "..."
}
```

Used for:

- Billing  
- Audit logging  
- Notifications  
- Metrics aggregation  

#### 5️⃣ PostgreSQL Persistence

Stored in:

- deployment_requests  
  - id  
  - tenant_id  
  - risk_score  
  - status  
  - created_at  

#### 6️⃣ Observability (OpenTelemetry → Jaeger)

Trace view:

deploy_request → llm_risk_analysis → vector_lookup → kafka_emit → db_write

#### 7️⃣ Metrics (Prometheus → Grafana)

Metrics exposed:

- deployment_requests_total  
- ai_risk_score_bucket  
- deployment_failures_total  

Dashboards:

- AI risk distribution  
- Deployment latency  
- Tenant usage metrics  
- LLM cost metrics  

---

## ❌ Failure Case Example

Request:

```json
{
  "environment": "prod",
  "replicas": 1,
  "memory_request": "128Mi",
  "data_classification": "regulated"
}
```

Example LLM Response:

```json
{
  "risk_level": "CRITICAL",
  "action": "REJECT"
}
```

API Response:

```json
{
  "status": "rejected",
  "reason": "Regulated workload under-provisioned for production"
}
```

Result:

- No K8s resources created  
- Audit trail recorded  
- Kafka event emitted  
- Trace visible in Jaeger  
- Metrics updated  

---

## 🧪 Quick Test Commands

Health check:

```bash
curl http://localhost:8001/health
```

Trigger deploy:

```bash
curl -X POST http://localhost:8001/deploy   -H "Content-Type: application/json"   -d '{"app_name":"demo","environment":"dev"}'
```

# Examples

## Example A — Successful end-to-end deployment

```bash
curl -X POST http://localhost:8000/deployments/request \
  -H "Authorization: Bearer dev-agent-token" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name":"demoapp",
    "environment":"dev",
    "data_classification":"internal",
    "exposure":"internal",
    "config":{"image":"registry.internal/demoapp:1.0","replicas":2}
  }'
```

Expected:
- `status=APPROVED`
- policy `allowed=true`
- risk `LOW|MEDIUM`

## Example B — Failure (blocked) and why

```bash
curl -X POST http://localhost:8000/deployments/request \
  -H "Authorization: Bearer dev-agent-token" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name":"demoapp",
    "environment":"prod",
    "data_classification":"internal",
    "exposure":"internal",
    "config":{"image":"registry.internal/demoapp:latest","replicas":2}
  }'
```

Expected:
- `status=DENIED`
- policy denies `:latest` in prod
- risk likely elevated due to prod + latest

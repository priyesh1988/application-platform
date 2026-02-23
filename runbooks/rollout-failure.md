# Runbook: Rollout Failure

## Symptoms
- Increased 5xx
- Error budget burn accelerating
- Canary promotion stuck

## Checklist
1. Check recent deploy risk score
2. Check Argo Rollouts analysis run
3. Check dependency health (DB/Kafka)
4. Roll back via ArgoCD / Rollouts

## Commands
- kubectl argo rollouts get rollout application-platform
- kubectl describe rollout application-platform

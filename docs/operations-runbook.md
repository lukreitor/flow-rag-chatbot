# Operations Runbook

## On-Call Checklist

1. Confirm access to observability dashboard (Grafana), log aggregation (ELK), and container registry.
2. Ensure `.env` secrets mirror the values stored in the secret manager (Azure Key Vault or AWS Secrets Manager).
3. Verify CI pipelines are green before deploying changes.

## Monitoring

- **Health checks**: Poll `GET /api/health/ping` every 30 seconds. Alert if two consecutive failures occur.
- **Worker queue depth**: Track `rq:queue:flow_tasks` length. Trigger an alert if exceeding 20 jobs for more than 5 minutes.
- **Latency**: Measure end-to-end latency from chat submission to response. Alert if P95 > 10 seconds.
- **Vector store size**: Monitor disk usage of the Chroma persistence directory to anticipate storage upgrades.

## Troubleshooting

| Symptom | Root Cause | Mitigation |
| --- | --- | --- |
| `500` responses from `/chat/completions` | Flow API outage | Retry request, open incident with Flow team, switch frontend to maintenance banner. |
| Messages delayed > 20s | Worker offline or Redis unreachable | Check Docker/Kubernetes logs, restart worker deployment, validate Redis connectivity. |
| Document ingestion fails | Unsupported file type or corrupted PDF | Validate file extension, reprocess PDF with OCR, update allowed extensions if necessary. |
| Empty LLM responses | Retrieval returning low-signal chunks | Re-run ingestion, verify embeddings model, increase chunk size or overlap. |

## Runbooks

### Restart Worker
1. `docker compose restart worker` (local) or redeploy worker pod in production.
2. Monitor queue depth; expect it to drain within 2 minutes.

### Rotate Flow Credentials
1. Retrieve new credentials from CI&T Flow portal.
2. Update secret manager entries (`FLOW_AGENT`, `FLOW_TENANT`, `FLOW_AGENT_SECRET`).
3. Trigger configuration rollout via CI/CD.
4. Validate by sending a smoke-test message through the staging environment.

### Rebuild Vector Store
1. Stop worker and API to avoid concurrent writes.
2. Delete the `VECTOR_STORE_PATH` directory.
3. Run `POST /api/documents/ingest` to rebuild embeddings.
4. Restart services and validate search quality with regression prompts.

## Escalation

- **Primary**: Backend engineer on call.
- **Secondary**: DevOps engineer.
- **Tertiary**: Product owner for customer communication.

Document all incidents in the shared operations log and schedule post-mortems for P1/P0 events.

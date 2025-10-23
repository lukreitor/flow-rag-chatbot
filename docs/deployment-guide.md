# Deployment Guide

Target stack: **Frontend (Vercel)**, **Backend API (Render)**, **Postgres (MongoDB Atlas for vector metadata)**, **Redis (Upstash)**.

## Prerequisites

- GitHub repository with CI passing.
- Vercel, Render, Atlas, and Upstash accounts with appropriate billing tiers.
- Flow API credentials stored in a secure secret manager.

## Step-by-Step

### 1. Provision Managed Services

1. **Upstash Redis**
   - Create a Redis database.
   - Note the `UPSTASH_REDIS_URL` and token; map to `REDIS_URL` environment variable.
2. **MongoDB Atlas**
   - Create a dedicated cluster for metadata if required by a managed vector store.
   - Alternatively host Chroma-compatible storage on Render disk volume.
3. **Render PostgreSQL (optional)**
   - Provision if relational data persistence is required.

### 2. Deploy Backend to Render

1. Create a new Web Service from the GitHub repository.
2. Select Docker deployment and point to `backend/Dockerfile`.
3. Configure environment variables (from `.env.example`).
4. Add persistent disk for `/data` if using local Chroma store.
5. Configure health check path `/api/health/ping`.
6. Provision a **Background Worker** service using the same image for the RQ worker; set command `python -m app.worker.main`.

### 3. Deploy Frontend to Vercel

1. Import the repository and select the `frontend` directory as the root.
2. Set build command `npm run build` and output directory `dist`.
3. Configure environment variables:
   - `VITE_API_BASE_URL=https://<render-backend>/api`
4. Assign a custom domain if required.

### 4. Configure CI/CD

- Ensure `.github/workflows/ci.yml` runs tests on every push/pr.
- Enable Render auto-deploy from the `main` branch after CI success.
- Enable Vercel production deployments from the `main` branch.

### 5. Smoke Test

1. After deployment, run `curl https://<render-backend>/api/health/ping`.
2. Visit the Vercel domain, complete nickname gate, send a message.
3. Monitor Render logs for worker processing and Flow API responses.

### 6. Observability & Scaling

- Configure Vercel Analytics or Sentry for frontend error tracking.
- Use Render metrics for backend CPU/memory; scale to multiple instances for HA.
- Enable Upstash alerts for connection limits and throughput.

### 7. Rollback Strategy

- Use Vercel's instant rollbacks.
- For Render, promote the previous successful deployment.
- Restore vector store from snapshot; rerun document ingestion if necessary.

### 8. Disaster Recovery

- Schedule backups of `/data/documents` and the vector store directory.
- Document runbooks in `operations-runbook.md` for rapid response.

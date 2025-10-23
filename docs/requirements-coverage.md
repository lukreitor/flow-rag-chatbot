# Requirements Coverage

| Requirement | Implementation | Location |
| --- | --- | --- |
| FastAPI backend with RAG | FastAPI app orchestrates LangChain embeddings and Flow API calls | `backend/app/main.py`, `backend/app/services` |
| React frontend with TypeScript and Chakra UI | Vite + React client with Chakra UI | `frontend/` |
| RAG ingestion of text and PDF | LangChain loaders, document ingestion service | `backend/app/services/document_loader.py`, `document_ingestion.py` |
| Document upload endpoint | `POST /api/documents/upload` | `backend/app/api/routes/documents.py` |
| Display chat history with assistant responses | React conversation components | `frontend/src/components/ChatThread.tsx` |
| Use CI&T Flow APIs | `FlowClient` handles chat completions | `backend/app/services/flow_client.py` |
| Docker-based local environment on Windows | Compose file orchestrates services | `docker-compose.yml` |
| GitHub Actions CI | Workflow runs backend + frontend tests | `.github/workflows/ci.yml` |
| Simplified auth (nickname) | Frontend nickname input; backend trusts client-provided conversation ID | `frontend/src/components/NicknameGate.tsx` |
| Documented architecture, API, operations, deployment, tests | Docs folder with required artifacts | `docs/` |
| Separate worker for Flow API | RQ worker executes LLM calls | `backend/app/worker` |
| Testing setup (Pytest, Vitest, Playwright) | Backend/Frontend tests and configs | `backend/tests`, `frontend/tests`, `playwright` config |

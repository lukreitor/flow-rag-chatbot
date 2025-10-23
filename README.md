# Flow RAG Chatbot

Full-stack Retrieval-Augmented Generation chatbot that integrates a React frontend, FastAPI backend, LangChain document processing, and CI&T Flow LLM APIs.

## Project Structure

- `backend/`: FastAPI application, RAG pipeline, and worker queue
- `frontend/`: React (Vite) TypeScript client with Chakra UI
- `docs/`: Architecture, operations, and product documentation
- `docker-compose.yml`: Local development environment

## Getting Started

1. Copy `.env.example` to `.env` and fill in the CI&T Flow credentials.
2. Install dependencies:
   - Backend: `pip install -e ./backend[dev]`
   - Frontend: `cd frontend && npm install`
3. Launch services: `docker compose up --build`

## Testing

- Backend: `cd backend && pytest`
- Frontend unit tests: `cd frontend && npm run test`
- Frontend e2e tests: `cd frontend && npx playwright test`
   - First run? execute `cd frontend && npx playwright install` to fetch browsers.

## Documentation

Comprehensive guides live in the `docs/` directory, covering architecture, API contracts, test plans, operations, and demo scripts.

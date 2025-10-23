# Architecture

## Overview

The Flow RAG Chatbot is a polyglot system consisting of a TypeScript React frontend, a Python FastAPI backend, and a background worker dedicated to calling the CI&T Flow LLM APIs. The solution embraces a Retrieval-Augmented Generation (RAG) approach: documents are ingested, chunked, embedded, and persisted into a Chroma vector store. When the user asks a question, the backend retrieves the most relevant chunks and feeds them to the Flow LLM to ground the response on trustworthy context.

```
┌─────────────┐     HTTPS      ┌────────────┐        Redis Queue        ┌────────────┐
│  Web App    │◀──────────────▶│   API      │◀────────────────────────▶│  Worker     │
│ (React/Vite)│                │(FastAPI)   │                          │(RQ + RAG)   │
└─────────────┘                └────────────┘                          └────────────┘
        │                              │                                     │
        │                              │                                     │
        ▼                              ▼                                     ▼
 Chakra UI UI                 Chroma Vector Store                      CI&T Flow API
 Playwright/Vitest            Sentence-Transformer embeddings          Document context
```

## Backend Components

- **FastAPI application** (`backend/app/main.py`)
  - Hosts REST endpoints for health checks, chat completions, and document ingestion.
  - Exposes typed responses using Pydantic schemas.
- **RAG pipeline** (`backend/app/services/rag_pipeline.py`)
  - Performs similarity search against Chroma, builds the chat completion payload, and delegates the final response generation to the worker.
- **Vector store** (`backend/app/services/embedding_store.py`)
  - Uses `SentenceTransformerEmbeddings` to compute embeddings and persists the collection using Chroma.
- **Document ingestion service** (`backend/app/services/document_ingestion.py`)
  - Handles both bootstrapping of the knowledge base and user uploads, ensuring only allowed extensions are stored.
- **Task queue** (`backend/app/services/task_queue.py`, `backend/app/worker`)
  - Uses Redis + RQ. The API places work on the queue; a separate worker process executes long-running LLM calls.

## Frontend Components

- **React + Vite** (`frontend/`)
  - Chakra UI supplies consistent styling and layout primitives.
  - React Query handles API interactions and caching.
  - Form logic maintains conversational context client side.
- **Testing strategy**
  - Unit and component tests via Vitest and React Testing Library.
  - End-to-end coverage via Playwright, driven against the Docker environment.

## Data Flow

1. User submits a message via the frontend.
2. Frontend posts to `POST /api/chat/completions`.
3. API queries the vector store for relevant chunks, builds a prompt, and enqueues a Flow completion task.
4. Worker consumes the task, calls the CI&T Flow endpoint, and returns the model response coupled with the retrieved context.
5. API responds with the assistant answer and supporting document snippets.
6. Frontend renders the answer and context, appending it to the chat timeline.

## Key Design Decisions

- **Background worker**: isolates long-running LLM calls and satisfies the requirement of using a dedicated worker for Flow/OpenAI calls.
- **Chroma vector store**: lightweight, file-based persistence that performs well in local Docker setups and can be promoted to managed services later.
- **SentenceTransformers embeddings**: open-source, CPU friendly embedding model suitable for local development; can be swapped for Flow-managed embeddings in production.
- **Type-safe contracts**: Pydantic and TypeScript models enforce consistent API contracts between frontend and backend.
- **Docker-first**: `docker-compose.yml` orchestrates Postgres, Redis, backend, worker, and frontend containers for a reproducible environment.

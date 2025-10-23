# API Reference

Base URL: `https://{host}/api`

Authentication is handled server-side through CI&T Flow credentials. All endpoints respond with JSON.

## Health

### `GET /health/ping`
- **Description**: Liveness probe used by monitoring tools and container orchestrators.
- **Response**
  ```json
  {
    "status": "ok"
  }
  ```

## Chat

### `POST /chat/completions`
- **Description**: Executes the RAG pipeline and returns an assistant answer grounded on relevant documents.
- **Request Body**
  ```json
  {
    "message": "How do I authenticate with Flow?",
    "conversation_id": "optional-client-id"
  }
  ```
- **Response**
  ```json
  {
    "conversation_id": "2a2f8c9c-8cf4-4d66-a65b-93bfa768f3f3",
    "response": "To authenticate, set the FlowTenant, FlowAgent, and FlowAgentSecret headers...",
    "context": [
      {
        "document_id": "docs/authentication.pdf",
        "score": 0.8123,
        "content": "Authentication with Flow requires the following headers..."
      }
    ],
    "created_at": "2025-10-23T12:34:56.123456"
  }
  ```
- **Error Codes**
  - `400`: Invalid payload or missing message text.
  - `500`: Downstream Flow API failure or vector store error.

## Documents

### `POST /documents/upload`
- **Description**: Uploads a document that will be ingested into the vector store.
- **Request**: multipart/form-data with a single field named `file`.
- **Constraints**
  - Allowed extensions: `.txt`, `.md`, `.pdf`
  - Maximum size: configurable via `MAX_UPLOAD_MEGABYTES`
- **Response**
  ```json
  {
    "document_path": "data/documents/user-guide.pdf",
    "document_id": "user-guide",
    "chunks_indexed": 24
  }
  ```

### `POST /documents/ingest`
- **Description**: Forces ingestion of all files located in the configured documents directory.
- **Response**
  ```json
  [
    {
      "document_path": "data/documents",
      "document_id": "initial-ingestion",
      "chunks_indexed": 128
    }
  ]
  ```

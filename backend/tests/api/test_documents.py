from fastapi.testclient import TestClient


def test_ingest_existing_documents_returns_accepted(client: TestClient) -> None:
    response = client.post("/api/documents/ingest")
    assert response.status_code == 202
    body = response.json()
    assert isinstance(body, list)

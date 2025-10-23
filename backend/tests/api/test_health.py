from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/api/health/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

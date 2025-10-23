import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


def pytest_configure(config: pytest.Config) -> None:  # noqa: ARG001
    test_documents = Path("tests/test_documents")
    test_documents.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("DOCUMENTS_PATH", str(test_documents.resolve()))
    os.environ.setdefault("VECTOR_STORE_PATH", str((test_documents / "vector").resolve()))
    os.environ.setdefault("FLOW_AGENT", "test-agent")
    os.environ.setdefault("FLOW_TENANT", "test-tenant")
    os.environ.setdefault("FLOW_AGENT_SECRET", "secret")


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as _client:
        yield _client

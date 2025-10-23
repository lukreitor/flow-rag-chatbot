import pytest
from fastapi.testclient import TestClient

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


def test_chat_completion_returns_assistant_message(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _fake_process(self: ChatService, request: ChatRequest) -> ChatResponse:  # noqa: ANN001
        return ChatResponse(conversation_id="123", response=f"Echo: {request.message}")

    monkeypatch.setattr(ChatService, "process", _fake_process, raising=False)

    payload = ChatRequest(message="Hello")

    response = client.post("/api/chat/completions", json=payload.dict())

    assert response.status_code == 200
    data = response.json()
    assert data["response"].startswith("Echo")

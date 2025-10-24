from uuid import UUID

from fastapi.testclient import TestClient

from app.core.database import session_scope
from app.services.conversation_service import ConversationService


def _seed_conversation(nickname: str) -> UUID:
    with session_scope() as session:
        service = ConversationService(session)
        conversation = service.create(nickname=nickname)
        service.add_message(conversation.id, "user", "Hello there")
        service.add_message(conversation.id, "assistant", "Hi! How can I help?")
        session.commit()
        return conversation.id


def test_list_conversations_returns_user_conversations(client: TestClient) -> None:
    nickname = "alice"
    conversation_id = _seed_conversation(nickname)

    response = client.get("/api/conversations", params={"nickname": nickname})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data
    assert any(item["id"] == str(conversation_id) for item in data)


def test_get_conversation_returns_messages(client: TestClient) -> None:
    nickname = "bob"
    conversation_id = _seed_conversation(nickname)

    response = client.get(f"/api/conversations/{conversation_id}", params={"nickname": nickname})

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == str(conversation_id)
    assert len(payload["messages"]) == 2
    assert payload["messages"][0]["role"] == "user"
    assert payload["messages"][1]["role"] == "assistant"
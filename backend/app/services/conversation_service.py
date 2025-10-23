from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models.conversation import Conversation, Message


class ConversationService:
    """Business logic for persisting conversations and messages."""

    def __init__(self, session: Session):
        self._session = session

    def create(self, nickname: str, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(nickname=nickname, title=title or "New chat")
        self._session.add(conversation)
        self._session.commit()
        self._session.refresh(conversation)
        return conversation

    def get(self, conversation_id: UUID) -> Conversation:
        conversation = self._session.get(Conversation, conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        return conversation

    def list_for_nickname(self, nickname: str) -> list[Conversation]:
        statement = (
            select(Conversation)
            .where(Conversation.nickname == nickname)
            .order_by(Conversation.updated_at.desc())
        )
        return list(self._session.exec(statement))

    def list_messages(self, conversation_id: UUID) -> list[Message]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return list(self._session.exec(statement))

    def add_message(self, conversation_id: UUID, role: str, content: str) -> Message:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        self._session.add(message)
        self._session.flush()
        self._touch_conversation(conversation_id, last_user_message=content if role == "user" else None)
        self._session.flush()
        return message

    def _touch_conversation(self, conversation_id: UUID, last_user_message: Optional[str] = None) -> None:
        conversation = self._session.get(Conversation, conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        conversation.updated_at = datetime.utcnow()
        if last_user_message and (not conversation.title or conversation.title == "New chat"):
            conversation.title = last_user_message[:80]
        self._session.add(conversation)

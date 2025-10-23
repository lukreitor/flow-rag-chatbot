from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Conversation(SQLModel, table=True):
    """Represents a chat conversation initiated by a user nickname."""

    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    nickname: str = Field(index=True, max_length=120)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    messages: list["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class Message(SQLModel, table=True):
    """Stores a single chat message within a conversation."""

    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: str = Field(regex=r"^(user|assistant)$", max_length=16)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    conversation: Conversation = Relationship(back_populates="messages")

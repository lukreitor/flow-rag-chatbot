from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=120)
    title: Optional[str] = Field(None, max_length=200)


class ConversationResponse(BaseModel):
    id: UUID
    nickname: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationSummary(ConversationResponse):
    last_message_preview: Optional[str] = None


class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

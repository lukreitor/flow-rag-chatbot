from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., regex=r"^(user|assistant|system)$")
    content: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = Field(None, description="Conversation identifier")
    nickname: str = Field(..., min_length=1, max_length=120)


class DocumentContext(BaseModel):
    document_id: str
    score: float
    content: str


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    context: List[DocumentContext] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List[ChatMessage] = Field(default_factory=list)

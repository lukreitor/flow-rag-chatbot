from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.conversation import MessageResponse


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
    messages: List[MessageResponse] = Field(default_factory=list)

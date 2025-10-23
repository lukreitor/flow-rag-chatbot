from __future__ import annotations

import uuid
from typing import Any, Dict

from sqlmodel import Session

from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService
from app.services.task_queue import TaskQueue
from app.worker.tasks import process_chat


class ChatService:
    """Domain service coordinating worker queue for chat requests."""

    def __init__(self, session: Session, queue: TaskQueue | None = None):
        self._queue = queue or TaskQueue()
        self._session = session
        self._conversations = ConversationService(session)

    def process(self, request: ChatRequest) -> ChatResponse:
        conversation_id = request.conversation_id
        if conversation_id:
            conversation_uuid = uuid.UUID(conversation_id)
            conversation = self._conversations.get(conversation_uuid)
        else:
            conversation = self._conversations.create(request.nickname)
            conversation_id = str(conversation.id)

        user_message = self._conversations.add_message(uuid.UUID(conversation_id), "user", request.message)
        self._session.commit()

        job = self._queue.enqueue(
            process_chat,
            {"message": request.message, "conversation_id": conversation_id},
        )
        result = self._queue.wait_for_result(job.job_id)
        payload: Dict[str, Any] = result.payload or {}
        flow_response = payload.get("response", {})
        assistant_output = self._extract_text(flow_response)

        assistant_message = self._conversations.add_message(
            uuid.UUID(conversation_id),
            "assistant",
            assistant_output,
        )
        self._session.commit()

        messages = [
            ChatMessage(role="user", content=user_message.content, timestamp=user_message.created_at),
            ChatMessage(role="assistant", content=assistant_message.content, timestamp=assistant_message.created_at),
        ]

        return ChatResponse(
            conversation_id=conversation_id,
            response=assistant_output,
            context=payload.get("context", []),
            messages=messages,
        )

    def _extract_text(self, response: Dict[str, Any]) -> str:
        choices = response.get("choices", [])
        if not choices:
            return ""
        return choices[0].get("message", {}).get("content", "")

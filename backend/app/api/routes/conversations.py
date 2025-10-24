from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.api.deps import get_db_session
from app.schemas.conversation import (
    ConversationSummary,
    ConversationWithMessages,
    MessageResponse,
)
from app.services.conversation_service import ConversationService

router = APIRouter(tags=["conversations"], prefix="/conversations")


@router.get("/", response_model=List[ConversationSummary])
def list_conversations(
    nickname: str = Query(..., min_length=1, max_length=120),
    session: Session = Depends(get_db_session),
) -> List[ConversationSummary]:
    service = ConversationService(session)
    conversations = service.list_for_nickname(nickname)

    summaries: List[ConversationSummary] = []
    for conversation in conversations:
        last_message = service.get_last_message(conversation.id)
        preview = last_message.content[:120] if last_message else None
        summaries.append(
            ConversationSummary(
                id=conversation.id,
                nickname=conversation.nickname,
                title=conversation.title,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
                last_message_preview=preview,
            )
        )

    return summaries


@router.get("/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: UUID,
    nickname: str = Query(..., min_length=1, max_length=120),
    session: Session = Depends(get_db_session),
) -> ConversationWithMessages:
    service = ConversationService(session)
    try:
        conversation = service.get(conversation_id)
    except ValueError as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found") from exc

    if conversation.nickname != nickname:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    messages = service.list_messages(conversation_id)

    return ConversationWithMessages(
        id=conversation.id,
        nickname=conversation.nickname,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[MessageResponse.model_validate(message) for message in messages],
    )

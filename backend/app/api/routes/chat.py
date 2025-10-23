from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_app_settings, get_db_session
from app.core.config import Settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from sqlmodel import Session

router = APIRouter(tags=["chat"], prefix="/chat")


@router.post("/completions", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def create_completion(
    payload: ChatRequest,
    _settings: Settings = Depends(get_app_settings),
    session: Session = Depends(get_db_session),
) -> ChatResponse:
    service = ChatService(session=session)
    try:
        return service.process(payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc

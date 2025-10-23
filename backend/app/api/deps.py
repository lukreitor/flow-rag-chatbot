from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.config import Settings, get_settings
from app.core.database import get_session


def get_app_settings(settings: Annotated[Settings, Depends(get_settings)]) -> Settings:
    """Expose Settings as a dependency for request handlers."""

    return settings


def get_db_session(session: Annotated[Session, Depends(get_session)]) -> Session:
    """Provide a SQLModel session per request."""

    return session

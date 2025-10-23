from __future__ import annotations

from contextlib import contextmanager
from functools import lru_cache
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings


def _build_engine_url() -> str:
    settings = get_settings()
    return settings.database_url


@lru_cache()
def get_engine():
    url = _build_engine_url()
    return create_engine(url, echo=False, pool_pre_ping=True)


def init_db() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    engine = get_engine()
    with Session(engine) as session:
        yield session


def get_session() -> Iterator[Session]:
    with session_scope() as session:
        yield session

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.api.routes import chat, documents, health
from app.core.config import Settings, get_settings
from app.core.database import get_engine


@asynccontextmanager
def lifespan(app: FastAPI):
    settings = get_settings()
    settings.vector_store_path.mkdir(parents=True, exist_ok=True)
    settings.documents_path.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(get_engine())
    yield


def create_application() -> FastAPI:
    settings: Settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.cors_origins],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(chat.router, prefix=settings.api_prefix)
    app.include_router(documents.router, prefix=settings.api_prefix)

    return app


app = create_application()

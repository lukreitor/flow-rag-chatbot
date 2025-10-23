from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import AnyHttpUrl, Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env."""

    app_name: str = Field("Flow RAG Chatbot", env="APP_NAME")
    environment: str = Field("development", env="ENVIRONMENT")
    api_prefix: str = Field("/api", env="API_PREFIX")
    cors_origins: List[AnyHttpUrl] = Field(default_factory=list, env="CORS_ORIGINS")

    # CI&T Flow API credentials
    flow_base_url: AnyHttpUrl = Field(
        "https://flow.ciandt.com/ai-orchestration-api/v1", env="FLOW_BASE_URL"
    )
    flow_agent: str = Field(..., env="FLOW_AGENT")
    flow_tenant: str = Field(..., env="FLOW_TENANT")
    flow_agent_secret: str = Field(..., env="FLOW_AGENT_SECRET")
    flow_channel: Optional[str] = Field(None, env="FLOW_CHANNEL")

    # Vector store configuration
    vector_store_path: Path = Field(Path("/data/vector_store"), env="VECTOR_STORE_PATH")
    embedding_model: str = Field("text-embedding-3-small", env="EMBEDDING_MODEL")

    # Database configuration
    database_url: str = Field(
        "postgresql+asyncpg://chatbot:chatbot@postgres:5432/chatbot",
        env="DATABASE_URL",
    )

    # Redis / task queue configuration
    redis_url: str = Field("redis://redis:6379/0", env="REDIS_URL")
    task_queue_name: str = Field("flow_tasks", env="TASK_QUEUE_NAME")

    # File upload configuration
    max_upload_megabytes: int = Field(10, env="MAX_UPLOAD_MEGABYTES")
    allowed_file_extensions: List[str] = Field(
        default_factory=lambda: [".txt", ".md", ".pdf"], env="ALLOWED_FILE_EXTENSIONS"
    )

    documents_path: Path = Field(Path("/data/documents"), env="DOCUMENTS_PATH")

    @validator("cors_origins", pre=True)
    def split_cors_origins(cls, value: str | List[AnyHttpUrl]) -> List[AnyHttpUrl]:
        if isinstance(value, str) and not value.startswith("["):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @validator("vector_store_path", "documents_path", pre=True)
    def ensure_path(cls, value: str | Path) -> Path:
        return Path(value).resolve()

    @validator("allowed_file_extensions", pre=True)
    def split_extensions(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            items = [ext.strip() for ext in value.split(",") if ext.strip()]
        else:
            items = value

        normalized: List[str] = []
        for ext in items:
            cleaned = ext.lower().strip()
            if not cleaned:
                continue
            if not cleaned.startswith("."):
                cleaned = f".{cleaned}"
            normalized.append(cleaned)
        return normalized

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()

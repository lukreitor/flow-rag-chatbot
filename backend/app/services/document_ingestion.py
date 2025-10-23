from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path
from typing import Iterable, List

from fastapi import UploadFile
from langchain.schema import Document

from app.core.config import Settings, get_settings
from app.schemas.document import DocumentIngestionResult
from app.services.document_loader import DocumentLoaderService
from app.services.embedding_store import EmbeddingStore


class DocumentIngestionService:
    """Handles loading and indexing new documents."""

    def __init__(
        self,
        loader: DocumentLoaderService | None = None,
        store: EmbeddingStore | None = None,
        settings: Settings | None = None,
    ):
        self._loader = loader or DocumentLoaderService()
        self._store = store or EmbeddingStore()
        self._settings = settings or get_settings()

    def ingest_existing(self) -> List[DocumentIngestionResult]:
        docs = self._loader.load_documents()
        chunks = self._store.add_documents(docs)
        return [
            DocumentIngestionResult(
                document_path=Path(self._settings.documents_path),
                document_id="initial-ingestion",
                chunks_indexed=chunks,
            )
        ]

    def ingest_upload(self, upload: UploadFile) -> DocumentIngestionResult:
        self._validate_upload(upload)
        destination = self._save_upload(upload)
        documents = self._loader.load_documents(destination.parent)
        chunks = self._store.add_documents(documents)
        return DocumentIngestionResult(
            document_path=destination,
            document_id=destination.stem,
            chunks_indexed=chunks,
        )

    def _save_upload(self, upload: UploadFile) -> Path:
        filename = upload.filename or f"upload-{uuid.uuid4()}"
        target = self._settings.documents_path / filename
        with target.open("wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
        upload.file.seek(0)
        return target

    def _validate_upload(self, upload: UploadFile) -> None:
        extension = Path(upload.filename or "").suffix.lower()
        if extension not in self._settings.allowed_file_extensions:
            raise ValueError("Unsupported file type")

        upload.file.seek(0, os.SEEK_END)
        size_bytes = upload.file.tell()
        upload.file.seek(0)
        max_bytes = self._settings.max_upload_megabytes * 1024 * 1024
        if size_bytes > max_bytes:
            raise ValueError("File exceeds allowed size")

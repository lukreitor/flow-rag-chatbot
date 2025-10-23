from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from app.core.config import Settings, get_settings


class DocumentLoaderService:
    """Loads documents from disk into LangChain Document objects."""

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()

    def load_documents(self, directory: Path | None = None) -> List[Document]:
        path = Path(directory or self._settings.documents_path)
        documents: List[Document] = []
        if not path.exists():
            return documents

        for entry in path.iterdir():
            if entry.is_file() and entry.suffix.lower() in self._settings.allowed_file_extensions:
                documents.extend(self._load_file(entry))
        return documents

    def _load_file(self, file_path: Path) -> Iterable[Document]:
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
        else:
            loader = TextLoader(str(file_path), encoding="utf-8")
        return loader.load()

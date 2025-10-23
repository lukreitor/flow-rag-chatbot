from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

import numpy as np
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings

from app.core.config import Settings, get_settings


class EmbeddingStore:
    """Handles vector store persistence and similarity search."""

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()
        self._vector_store_path = Path(self._settings.vector_store_path)
        self._vector_store_path.mkdir(parents=True, exist_ok=True)
        self._embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self._index_file = self._vector_store_path / "store.json"
        self._documents: List[str] = []
        self._metadatas: List[dict] = []
        self._vectors: List[List[float]] = []
        self._load_store()

    def _load_store(self) -> None:
        if not self._index_file.exists():
            return

        try:
            raw = json.loads(self._index_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return

        self._documents = list(raw.get("documents", []))
        self._metadatas = list(raw.get("metadatas", []))
        raw_vectors = raw.get("vectors", [])
        self._vectors = [
            [float(value) for value in vector]
            for vector in raw_vectors
            if isinstance(vector, (list, tuple))
        ]

    def _persist_store(self) -> None:
        payload = {
            "documents": self._documents,
            "metadatas": self._metadatas,
            "vectors": self._vectors,
        }
        self._index_file.write_text(json.dumps(payload), encoding="utf-8")

    def add_documents(self, documents: Iterable[Document]) -> int:
        docs = list(documents)
        if not docs:
            return 0

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
        )
        split_docs: List[Document] = text_splitter.split_documents(docs)
        contents = [doc.page_content for doc in split_docs]
        embeddings = self._embeddings.embed_documents(contents)

        for doc, embedding in zip(split_docs, embeddings):
            self._documents.append(doc.page_content)
            self._metadatas.append(dict(doc.metadata))
            self._vectors.append([float(value) for value in embedding])

        self._persist_store()
        return len(split_docs)

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if not self._vectors:
            return []

        vector_matrix = np.array(self._vectors, dtype=np.float32)
        query_vector = np.array(self._embeddings.embed_query(query), dtype=np.float32)

        query_norm = np.linalg.norm(query_vector)
        if query_norm == 0:
            return []

        document_norms = np.linalg.norm(vector_matrix, axis=1)
        denom = document_norms * query_norm
        denom[denom == 0] = 1e-12

        similarities = vector_matrix @ query_vector / denom
        top_indices = np.argsort(similarities)[::-1][:k]

        documents: List[Document] = []
        for idx in top_indices:
            metadata = dict(self._metadatas[idx])
            # Persist cosine similarity so downstream consumers can rank results.
            metadata["score"] = float(similarities[idx])
            documents.append(Document(page_content=self._documents[idx], metadata=metadata))

        return documents

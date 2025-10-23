from __future__ import annotations

from typing import Any, Dict, List

from langchain.schema import Document

from app.schemas.chat import DocumentContext
from app.services.embedding_store import EmbeddingStore
from app.services.flow_client import FlowClient


class RagPipeline:
    """Coordinates similarity search and Flow LLM responses."""

    def __init__(self, store: EmbeddingStore | None = None, client: FlowClient | None = None):
        self._store = store or EmbeddingStore()
        self._client = client or FlowClient()

    def generate(self, prompt: str, conversation_id: str | None = None) -> Dict[str, Any]:
        retrieved_docs = self._store.similarity_search(prompt)
        context = self._build_context(retrieved_docs)

        payload = self._build_payload(prompt, context, conversation_id)
        response = self._client.chat_completion(payload)
        return {"response": response, "context": context}

    def _build_context(self, documents: List[Document]) -> List[DocumentContext]:
        context: List[DocumentContext] = []
        for idx, doc in enumerate(documents):
            metadata = doc.metadata or {}
            context.append(
                DocumentContext(
                    document_id=str(metadata.get("source", f"doc-{idx}")),
                    score=float(metadata.get("score", 0.0)),
                    content=doc.page_content,
                )
            )
        return context

    def _build_payload(
        self,
        message: str,
        context: List[DocumentContext],
        conversation_id: str | None,
    ) -> Dict[str, Any]:
        context_text = "\n\n".join(
            f"Document {item.document_id}: {item.content}" for item in context
        )
        system_prompt = (
            "You are a helpful assistant that uses the provided documents to answer "
            "questions about the Flow platform. Cite the sources when relevant."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {message}"},
        ]

        payload: Dict[str, Any] = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.2,
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id
        return payload

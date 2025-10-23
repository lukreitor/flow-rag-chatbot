from __future__ import annotations

from typing import Any, Dict

from app.services.rag_pipeline import RagPipeline


def process_chat(payload: Dict[str, Any]) -> Dict[str, Any]:
    pipeline = RagPipeline()
    result = pipeline.generate(payload["message"], payload.get("conversation_id"))
    return result

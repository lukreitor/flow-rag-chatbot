from pathlib import Path

from pydantic import BaseModel


class DocumentIngestionResult(BaseModel):
    document_path: Path
    document_id: str
    chunks_indexed: int

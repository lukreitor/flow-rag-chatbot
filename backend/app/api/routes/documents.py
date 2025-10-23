from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.api.deps import get_app_settings
from app.core.config import Settings
from app.schemas.document import DocumentIngestionResult
from app.services.document_ingestion import DocumentIngestionService

router = APIRouter(tags=["documents"], prefix="/documents")


def _service() -> DocumentIngestionService:
    return DocumentIngestionService()


@router.post(
    "/upload",
    response_model=DocumentIngestionResult,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    _settings: Settings = Depends(get_app_settings),
) -> DocumentIngestionResult:
    service = _service()
    return service.ingest_upload(file)


@router.post(
    "/ingest",
    response_model=List[DocumentIngestionResult],
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_existing_documents(
    _settings: Settings = Depends(get_app_settings),
) -> List[DocumentIngestionResult]:
    service = _service()
    return service.ingest_existing()

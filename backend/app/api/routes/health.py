from fastapi import APIRouter

router = APIRouter(tags=["health"], prefix="/health")


@router.get("/ping", summary="Service liveness probe")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

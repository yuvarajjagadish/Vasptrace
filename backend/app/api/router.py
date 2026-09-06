from fastapi import APIRouter

# Primary v1 API router for future endpoints
api_v1_router = APIRouter(prefix="/api/v1")

# Placeholder route to verify /api/v1 router mounting
@api_v1_router.get(
    "/status",
    summary="API v1 Status",
    description="Returns API v1 status verification.",
    tags=["v1"],
)
async def v1_status() -> dict[str, str]:
    return {"status": "ok", "api_version": "v1"}

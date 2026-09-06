from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from app.config import settings
from app.core.database import check_database_connection

router = APIRouter(tags=["Health Check"])


class DatabaseHealth(BaseModel):
    status: str


class HealthCheckResponse(BaseModel):
    status: str
    application: str
    version: str
    environment: str
    database: DatabaseHealth


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Application and Database Health Check",
    description=(
        "Verifies the operational status of the FastAPI backend "
        "and active PostgreSQL connectivity."
    ),
)
async def health_check(response: Response) -> HealthCheckResponse:
    db_connected = await check_database_connection()

    if db_connected:
        return HealthCheckResponse(
            status="ok",
            application=settings.APP_NAME,
            version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT,
            database=DatabaseHealth(status="connected"),
        )

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthCheckResponse(
        status="error",
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database=DatabaseHealth(status="disconnected"),
    )

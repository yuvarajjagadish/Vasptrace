from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_app_metadata_and_docs():
    """Verify application creation and documentation endpoints."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Test Swagger UI documentation
        docs_response = await client.get("/docs")
        assert docs_response.status_code == 200

        # Test OpenAPI JSON schema
        openapi_response = await client.get("/openapi.json")
        assert openapi_response.status_code == 200
        schema = openapi_response.json()
        assert schema["info"]["title"] == "VASPTrace API"
        assert schema["info"]["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health_endpoint_connected():
    """Verify /health returns HTTP 200 and 'connected' when database connection succeeds."""
    with patch(
        "app.api.routes.health.check_database_connection",
        new_callable=AsyncMock,
        return_value=True,
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert data["application"] == "VASPTrace API"
            assert data["version"] == "0.1.0"
            assert data["environment"] == "development"
            assert data["database"] == {"status": "connected"}


@pytest.mark.asyncio
async def test_health_endpoint_disconnected():
    """Verify /health returns HTTP 503 and 'disconnected' when database connection fails."""
    with patch(
        "app.api.routes.health.check_database_connection",
        new_callable=AsyncMock,
        return_value=False,
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "error"
            assert data["application"] == "VASPTrace API"
            assert data["version"] == "0.1.0"
            assert data["environment"] == "development"
            assert data["database"] == {"status": "disconnected"}


@pytest.mark.asyncio
async def test_v1_status_endpoint():
    """Verify versioned /api/v1/status endpoint response."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/status")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "api_version": "v1"}

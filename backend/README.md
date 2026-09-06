# VASPTrace Backend

**VASPTrace** is an investigator-focused blockchain-forensics system built for Smart India Hackathon (SIH) 2026. The backend is built with FastAPI and Python 3.12+, delivering deterministic blockchain tracing, VASP (Virtual Asset Service Provider) attribution, evidence collection, and report generation.

---

## Architecture Overview

VASPTrace is architected as a clean, single-service FastAPI application without unnecessary microservice overhead:

```
vasptrace/
└── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py              # FastAPI application entry point & CORS
    │   ├── config.py            # Pydantic Settings configuration
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── router.py        # Versioned API router (/api/v1)
    │   │   └── routes/
    │   │       ├── __init__.py
    │   │       └── health.py    # GET /health endpoint
    │   └── core/
    │       ├── __init__.py
    │       ├── database.py      # Async SQLAlchemy 2.x engine & session
    │       ├── logging.py       # Centralized log management
    │       └── exceptions.py   # Domain error hierarchy
    │
    ├── tests/                   # Pytest suite
    │   ├── __init__.py
    │   └── test_health.py
    │
    ├── .env.example             # Configuration template
    ├── .gitignore               # Git exclusion patterns
    ├── requirements.txt         # Dependency lockfile
    ├── Dockerfile               # Container packaging definition
    ├── pytest.ini               # Test runner configuration
    ├── pyproject.toml           # Ruff linter & formatter config
    └── README.md                # Project documentation
```

---

## Prerequisites

- **Python**: 3.12 or higher
- **PostgreSQL**: 15+ (local instance or Docker container)
- **Pip / Virtualenv**: standard Python package management tools

---

## Environment Variables

Configuration is managed via `pydantic-settings`. Create a `.env` file in `vasptrace/backend/` based on `.env.example`:

| Variable | Description | Default |
|---|---|---|
| `APP_NAME` | FastAPI application name | `VASPTrace API` |
| `APP_VERSION` | Application semver version | `0.1.0` |
| `ENVIRONMENT` | Deployment environment (`development`, `production`, `test`) | `development` |
| `DATABASE_URL` | PostgreSQL connection string (`postgresql+asyncpg://...`) | `postgresql+asyncpg://postgres:postgres@localhost:5432/vasptrace` |
| `CORS_ORIGINS` | JSON list or comma-separated list of allowed origins | `["http://localhost:3000","http://127.0.0.1:3000"]` |
| `LOG_LEVEL` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | `INFO` |

---

## PostgreSQL Setup

### Local PostgreSQL Setup

1. Create PostgreSQL database:
   ```bash
   createdb vasptrace
   ```
2. Update your `.env` file with your credentials:
   ```env
   DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/vasptrace
   ```

### Docker PostgreSQL Setup

Alternatively, run PostgreSQL in Docker:

```bash
docker run --name vasptrace-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=vasptrace -p 5432:5432 -d postgres:16-alpine
```

---

## Installation & Setup

1. Navigate to the backend directory:
   ```bash
   cd vasptrace/backend
   ```
2. Create and activate a Python 3.12 virtual environment:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Backend

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload --port 8000
```

The server will start at `http://localhost:8000`.

---

## API Documentation

Interactive API documentation is generated automatically by FastAPI:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Spec**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## Health Check Endpoint

Query `GET /health` to verify application health and database connection:

```bash
curl http://localhost:8000/health
```

Example response when PostgreSQL is connected:

```json
{
  "status": "ok",
  "application": "VASPTrace API",
  "version": "0.1.0",
  "environment": "development",
  "database": {
    "status": "connected"
  }
}
```

---

## Running Tests

Execute the pytest suite:

```bash
pytest
```

---

## Code Quality & Linting

Run Ruff to check for linting errors and code style adherence:

```bash
ruff check .
```

To format code automatically:

```bash
ruff format .
```

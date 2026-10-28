# DocDesk

DocDesk is a documentation assistant being developed with
retrieval-augmented generation.

## Current functionality

DocDesk exposes a liveness endpoint at GET /health/live.
Document ingestion, search, and AI answers are not implemented yet.

## Requirements

- Python 3.12, 3.13, or 3.14
- Git

## Local setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project in editable mode:

```bash
python -m pip install -e .
```

Run the application:

```bash
python -m uvicorn docdesk.main:app --reload
```

## Development checks

Install the project and its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run automated tests:

```bash
python -m pytest
```

Check code quality:

```bash
python -m ruff check .
```

Check formatting without changing files:

```bash
python -m ruff format --check .
```

## Run with Docker

Build the image:

```bash
docker build -t docdesk:local .
```

Start the API:

```bash
docker run --rm --name docdesk-api -p 127.0.0.1:8000:8000 docdesk:local
```

Verify from another terminal:

```bash
curl -i http://127.0.0.1:8000/health/live
```

Stop the container:

```bash
docker stop docdesk-api
```

## Run the API and PostgreSQL together

Create `.env` from `.env.example` and replace the password placeholder.
Do not overwrite an existing configured `.env`.

Validate configuration:

```bash
docker compose config --quiet
```

Build and start services:

```bash
docker compose up --build -d --wait
```

Inspect service status:

```bash
docker compose ps
```

Connect to PostgreSQL:

```bash
docker compose exec db psql -U docdesk_admin -d docdesk
```

Stop services while keeping database storage:

```bash
docker compose down
```

The API does not query PostgreSQL yet.

## Health checks

- GET /health/live checks whether the API can respond.
- GET /health/ready executes SELECT 1 against PostgreSQL.
- Readiness returns HTTP 503 when the database is unavailable.

Run the application through Docker Compose, which supplies its DB_ environment
variables. Automated tests use controlled database substitutes.
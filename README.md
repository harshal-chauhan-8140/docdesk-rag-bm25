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
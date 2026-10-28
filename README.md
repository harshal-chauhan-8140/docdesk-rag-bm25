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
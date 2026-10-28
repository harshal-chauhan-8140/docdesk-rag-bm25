FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.lock ./

RUN python -m pip install --no-cache-dir --require-hashes -r requirements.lock

COPY pyproject.toml ./
COPY src ./src

RUN python -m pip install --no-cache-dir --no-deps .

RUN useradd --create-home --uid 10001 appuser

USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "docdesk.main:app", "--host", "0.0.0.0", "--port", "8000"]
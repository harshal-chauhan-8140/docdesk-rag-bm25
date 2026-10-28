import re

from rank_bm25 import BM25Okapi
from sqlalchemy import Engine, text


def tokenize(value: str) -> list[str]:
    """Convert English text into lowercase searchable tokens."""

    return re.findall(r"[a-z0-9_]+", value.casefold())


def search_chunks(engine: Engine, query: str, limit: int = 5) -> list[dict]:
    """Return passages ranked by BM25 relevance."""

    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    with engine.connect() as connection:
        rows = (
            connection.execute(
                text(
                    """
                SELECT id, source_url, source_revision, title, content
                FROM chunks
                ORDER BY id
                """
                )
            )
            .mappings()
            .all()
        )

    if not rows:
        return []

    documents = [dict(row) for row in rows]

    tokenized_documents = [tokenize(document["content"]) for document in documents]
    index = BM25Okapi(tokenized_documents)

    scores = index.get_scores(query_tokens)

    ranked_positions = sorted(
        range(len(documents)),
        key=lambda position: scores[position],
        reverse=True,
    )

    results = []

    for position in ranked_positions:
        if scores[position] <= 0:
            continue

        results.append(
            {
                **documents[position],
                "score": float(scores[position]),
            }
        )

        if len(results) >= limit:
            break

    return results

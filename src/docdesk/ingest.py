import json
import re
from urllib.request import Request, urlopen

from sqlalchemy import text

from docdesk.config import Settings
from docdesk.database import build_engine

SOURCES = [
    ("path-params", "Path parameters"),
    ("query-params", "Query parameters"),
    ("body", "Request bodies"),
]


def download(url: str) -> str:
    """Download a small UTF-8 text resource with a timeout and size limit."""

    request = Request(url, headers={"User-Agent": "DocDesk-learning-project"})

    with urlopen(request, timeout=20) as response:
        content = response.read(2_000_001)

    if len(content) > 2_000_000:
        raise ValueError("Downloaded resource exceeds the size limit")

    return content.decode("utf-8")


def split_document(content: str) -> list[str]:
    """Create passages of up to 200 words, overlapping by 40 words."""

    cleaned = re.sub(r"\{\*.*?\*\}", "", content, flags=re.DOTALL)

    words = cleaned.split()

    passages = []

    for start in range(0, len(words), 160):
        passage = " ".join(words[start : start + 200])
        passages.append(passage)

        if start + 200 >= len(words):
            break

    return passages


def main() -> None:
    """Fetch the source documents and replace their stored passages."""

    revision_data = json.loads(
        download("https://api.github.com/repos/fastapi/fastapi/commits/master")
    )
    revision = revision_data["sha"]

    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("GitHub returned an invalid commit identifier")

    records = []

    for slug, title in SOURCES:
        raw_url = (
            f"https://raw.githubusercontent.com/fastapi/fastapi/{revision}"
            f"/docs/en/docs/tutorial/{slug}.md"
        )
        source_url = f"https://fastapi.tiangolo.com/tutorial/{slug}/"

        passages = split_document(download(raw_url))

        if not passages:
            raise ValueError(f"No passages extracted from {source_url}")

        for position, passage in enumerate(passages):
            records.append(
                {
                    "source_url": source_url,
                    "source_revision": revision,
                    "title": title,
                    "chunk_index": position,
                    "content": passage,
                }
            )

    engine = build_engine(Settings())

    try:
        with engine.begin() as connection:
            for slug, _ in SOURCES:
                connection.execute(
                    text("DELETE FROM chunks WHERE source_url = :source_url"),
                    {"source_url": f"https://fastapi.tiangolo.com/tutorial/{slug}/"},
                )

            connection.execute(
                text(
                    """
                    INSERT INTO chunks
                        (source_url, source_revision, title, chunk_index, content)
                    VALUES
                        (:source_url, :source_revision, :title, :chunk_index, :content)
                    """
                ),
                records,
            )

        print(f"Stored {len(records)} passages from {len(SOURCES)} documents.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()

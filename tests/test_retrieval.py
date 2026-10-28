from docdesk.ingest import split_document
from docdesk.retrieval import tokenize


def test_tokenization_is_case_insensitive() -> None:
    assert tokenize("Query PARAMETERS!") == ["query", "parameters"]


def test_chunking_preserves_overlap_and_final_word() -> None:
    words = [f"word{number}" for number in range(350)]

    passages = split_document(" ".join(words))

    assert len(passages) == 2
    assert passages[0].split() == words[:200]
    assert passages[1].split() == words[160:]
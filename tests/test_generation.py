import pytest

from docdesk.generation import AnswerDraft, Claim, render_answer


@pytest.fixture
def passages() -> list[dict]:
    """Provide one controlled source passage for citation tests."""

    return [
        {
            "id": 42,
            "title": "Query parameters",
            "source_url": "https://fastapi.tiangolo.com/tutorial/query-params/",
            "source_revision": "test-revision",
            "content": "Query parameters can be converted and validated using Python types.",
        }
    ]


def test_answer_attaches_known_source(passages) -> None:
    draft = AnswerDraft(
        claims=[
            Claim(
                text="Query parameters can be validated using Python types.",
                source_ids=[1],
            )
        ]
    )

    result = render_answer(draft, passages)

    assert result["answered"] is True
    assert result["answer"].endswith("[S1]")
    assert result["sources"][0]["chunk_id"] == 42
    assert result["sources"][0]["passage"] == passages[0]["content"]


def test_unknown_citation_is_rejected(passages) -> None:
    draft = AnswerDraft(claims=[Claim(text="A statement.", source_ids=[999])])

    with pytest.raises(ValueError):
        render_answer(draft, passages)


def test_claim_without_citation_is_rejected(passages) -> None:
    draft = AnswerDraft(claims=[Claim(text="A statement.", source_ids=[])])

    with pytest.raises(ValueError):
        render_answer(draft, passages)


def test_empty_answer_returns_no_sources(passages) -> None:
    result = render_answer(AnswerDraft(claims=[]), passages)

    assert result["answered"] is False
    assert result["sources"] == []

import logging

from fastapi import APIRouter, HTTPException, Request
from openai import OpenAIError
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from docdesk.config import GenerationSettings
from docdesk.generation import AnswerDraft, generate_answer, render_answer
from docdesk.retrieval import search_chunks

router = APIRouter(tags=["answers"])
logger = logging.getLogger(__name__)


class AskRequest(BaseModel):
    """Validate the JSON body sent by the client."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    question: str = Field(min_length=3, max_length=500)


@router.post("/ask")
def ask(body: AskRequest, request: Request) -> dict:
    """Retrieve passages and generate an answer with source references."""

    try:
        passages = search_chunks(
            request.app.state.engine,
            body.question,
            limit=5,
        )
    except SQLAlchemyError:
        logger.warning("Database unavailable during answer retrieval")
        raise HTTPException(
            status_code=503,
            detail="Search temporarily unavailable",
        ) from None

    if not passages:
        return render_answer(AnswerDraft(claims=[]), [])

    settings = GenerationSettings()

    if settings.api_key is None or not settings.api_key.get_secret_value():
        raise HTTPException(
            status_code=503,
            detail="Answer generation is not configured",
        )

    try:
        return generate_answer(
            question=body.question,
            passages=passages,
            api_key=settings.api_key.get_secret_value(),
            model=settings.model,
        )

    except OpenAIError:
        logger.warning("Answer generation provider request failed")
        raise HTTPException(
            status_code=502,
            detail="The answer provider could not complete the request",
        ) from None

    except (ValueError, ValidationError):
        logger.warning("Generated answer failed validation")
        raise HTTPException(
            status_code=502,
            detail="The generated answer could not be validated",
        ) from None

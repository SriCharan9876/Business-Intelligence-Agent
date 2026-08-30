from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):

    message: str


class ChatResponse(BaseModel):

    answer: str

    intent: str | None = None

    analysis: dict[str, Any] | None = None

    data_quality: list[str] = []
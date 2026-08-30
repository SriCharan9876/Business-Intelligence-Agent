from fastapi import APIRouter

from app.schemas import (
    ChatRequest,
    ChatResponse
)

from app.agents.bi_agent import (
    bi_agent
)


router = APIRouter(
    prefix="/api",
    tags=["BI Agent"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(
    request: ChatRequest
):

    result = (
        await bi_agent.answer_question(
            request.message
        )
    )

    return result
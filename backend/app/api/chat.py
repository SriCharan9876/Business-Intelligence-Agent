from fastapi import APIRouter, HTTPException

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
    try:
        result = (
            await bi_agent.answer_question(
                request.message
            )
        )

        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")
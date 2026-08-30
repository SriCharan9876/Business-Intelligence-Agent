from pydantic import BaseModel
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    intent: Optional[str] = None
    data_quality: Optional[Dict[str, Any]] = None
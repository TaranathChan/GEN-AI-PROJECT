from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    model: str = "gpt-4"
    conversation_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    model_used: str
    latency_ms: int

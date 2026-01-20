from fastapi import APIRouter, HTTPException
from schemas.chat import ChatRequest, ChatResponse
from agents.orchestrator import orchestrate_chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await orchestrate_chat(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

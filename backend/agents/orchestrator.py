import time
from services.llm_router import route_llm
from schemas.chat import ChatRequest

async def orchestrate_chat(request: ChatRequest):
    start = time.time()

    # intelligent routing logic
    preferred_models = [request.model, "fallback"]

    response, model_used = await route_llm(
        request.message,
        preferred_models
    )

    latency = int((time.time() - start) * 1000)

    return {
        "reply": response,
        "model_used": model_used,
        "latency_ms": latency
    }

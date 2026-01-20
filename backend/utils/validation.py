from fastapi import HTTPException

ALLOWED_MODELS = {
    "gpt-4",
    "gpt-4o-mini",
    "gemini",
    "claude",
    "fallback"
}

MAX_MESSAGE_LENGTH = 4000

def validate_chat_request(message: str, model: str):
    if not message or not message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    if len(message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Message too long (max {MAX_MESSAGE_LENGTH} chars)"
        )

    if model not in ALLOWED_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model: {model}"
        )

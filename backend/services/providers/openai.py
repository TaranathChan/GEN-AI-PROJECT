import os
import httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

async def call_openai(
    message: str,
    model: str = "gpt-4o-mini",
    timeout: int = 15
) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            OPENAI_URL,
            headers=headers,
            json=payload
        )

    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]

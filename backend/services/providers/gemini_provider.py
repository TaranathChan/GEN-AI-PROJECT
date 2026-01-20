import os
import httpx


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-1.5-flash:generateContent"
)

async def call_gemini(message: str):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload
        )

    response.raise_for_status()

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

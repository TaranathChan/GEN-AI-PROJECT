import os
import httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def call_openai(message: str):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": message}]
            }
        )

    return response.json()["choices"][0]["message"]["content"]

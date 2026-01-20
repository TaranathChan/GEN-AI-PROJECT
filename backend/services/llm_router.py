import os
import httpx

# =========================
# Gemini config
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-1.5-flash:generateContent"
)

# =========================
# Groq config
# =========================
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# =========================
# Gemini call
# =========================
async def call_gemini(message: str):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")

    payload = {
        "contents": [
            {
                "parts": [{"text": message}]
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


# =========================
# Groq call
# =========================
async def call_groq(message: str):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")

    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            GROQ_URL,
            headers=headers,
            json=payload
        )

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


# =========================
# Router (Gemini + Groq)
# =========================
async def route_llm(message: str, models: list):
    for model in models:
        try:
            if model == "gemini":
                return await call_gemini(message), "gemini"

            if model == "groq":
                return await call_groq(message), "groq"

        except Exception as e:
            continue

    raise Exception("All LLM models failed")

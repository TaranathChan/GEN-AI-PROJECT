from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
import os
import time
import uvicorn

# =========================
# Load environment variables
# =========================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# =========================
# FastAPI App
# =========================
app = FastAPI(title="AI Chat Router (Groq)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Models
# =========================
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    model_used: str
    latency_ms: int

# =========================
# Groq Call
# =========================
async def call_groq(message: str) -> str:
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(GROQ_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    data = response.json()
    return data["choices"][0]["message"]["content"]

# =========================
# API Endpoint
# =========================
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    start = time.time()

    reply = await call_groq(request.message)

    latency = int((time.time() - start) * 1000)

    return {
        "reply": reply,
        "model_used": "groq-llama3",
        "latency_ms": latency
    }

# =========================
# Health
# =========================
@app.get("/")
def health():
    return {"status": "running"}

# =========================
# Run
# =========================
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

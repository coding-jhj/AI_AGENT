"""
AI Search Agent - FastAPI 백엔드 서버
- POST /chat  → Agent 실행, 답변 반환
- GET  /health → 서버 상태 확인
- GET  /       → 프론트엔드 HTML 서빙
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from agent import create_agent, run_agent

app = FastAPI(
    title="AI Search Agent API",
    description="ReAct 패턴 기반 웹 검색 AI Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_or_create_agent(api_key: str, model: str = "gemini-2.0-flash"):
    return create_agent(api_key, model)


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "gemini-2.0-flash"
    api_key: str
    user_input: str
    history: list[Message] = []

class ChatResponse(BaseModel):
    answer: str
    searched: bool
    search_query: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok", "message": "AI Search Agent is running 🚀"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # ✅ Google AI 키 검증으로 수정 (기존: gsk_ 체크 → AIza 또는 비어있는지만 확인)
    if not req.api_key.strip():
        raise HTTPException(status_code=400, detail="Google AI Studio API 키가 필요합니다.")
    if not req.user_input.strip():
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")

    try:
        agent_executor = get_or_create_agent(req.api_key, req.model)
        history = [{"role": m.role, "content": m.content} for m in req.history]
        result = run_agent(agent_executor, req.user_input, history)
        return ChatResponse(**result)

    except Exception as e:
        err = str(e)
        if "api_key" in err.lower() or "authentication" in err.lower() or "invalid" in err.lower():
            raise HTTPException(status_code=401, detail="API 키가 올바르지 않습니다.")
        raise HTTPException(status_code=500, detail=f"Agent 오류: {err[:200]}")


@app.get("/", response_class=HTMLResponse)
def index():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>index.html을 static/ 폴더에 넣어주세요.</h1>")
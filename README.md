---
title: AI Search Agent
emoji: 🤖
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---

# 🤖 AI Search Agent — FastAPI 버전

> ReAct 패턴 기반 웹 검색 AI Agent  
> **Groq(무료) + DuckDuckGo(무료) + FastAPI + 내장 UI**

---

## 프로젝트 구조

```
ai_agent_portfolio/
├── agent.py              # Agent 핵심 로직 (ReAct, 기존과 동일)
├── main.py               # FastAPI 서버 (NEW)
├── static/
│   └── index.html        # 내장 프론트엔드 UI (NEW)
├── requirements.txt      # fastapi, uvicorn 추가됨
└── README.md
```

---

## API 엔드포인트

| 메서드 | 경로      | 설명                        |
|--------|-----------|-----------------------------|
| GET    | `/`       | 웹 UI (index.html)          |
| GET    | `/health` | 서버 상태 확인              |
| POST   | `/chat`   | Agent 실행, 답변 반환       |
| GET    | `/docs`   | Swagger 자동 문서 (FastAPI) |

### POST `/chat` 예시

**Request**
```json
{
  "api_key": "gsk_...",
  "user_input": "오늘 AI 뉴스 알려줘",
  "history": [
    { "role": "user",      "content": "안녕" },
    { "role": "assistant", "content": "안녕하세요!" }
  ]
}
```

**Response**
```json
{
  "answer": "오늘 주요 AI 뉴스는...",
  "searched": true,
  "search_query": "AI news today"
}
```

---

## 로컬 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 서버 실행
uvicorn main:app --reload --port 8000

# 3. 브라우저에서 접속
# 웹 UI  → http://localhost:8000
# API 문서 → http://localhost:8000/docs
```

---

## Streamlit 버전과 비교

| 항목        | Streamlit 버전       | FastAPI 버전               |
|-------------|----------------------|----------------------------|
| UI          | Streamlit 컴포넌트   | 커스텀 HTML/CSS/JS         |
| API 분리    | 불가                 | ✅ REST API 독립 운용 가능  |
| 외부 연동   | 어려움               | ✅ 어떤 클라이언트도 가능  |
| Swagger 문서| 없음                 | ✅ `/docs` 자동 생성        |
| 배포        | Streamlit Cloud      | Railway, Render, HF Spaces |

---

## HuggingFace Spaces 배포 (Docker)

HF Spaces에서 FastAPI를 올리려면 `Dockerfile`이 필요합니다:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```

`README.md` 맨 위에 아래 헤더를 추가하세요:

```yaml
---
title: AI Search Agent
emoji: 🤖
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---
```

---

## Railway / Render 배포 (더 간단)

```bash
# Railway
railway up

# Render: GitHub 연결 후
# Build Command: pip install -r requirements.txt
# Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

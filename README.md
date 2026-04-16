---
title: AI Search Agent
emoji: 🤖
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---

<div align="center">

# 🤖 AI Search Agent

**스스로 웹 검색하고 판단하는 AI Agent**

[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Demo-yellow)](https://jeonghwanju-ai-search-agent.hf.space)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?logo=langchain)](https://langchain.com)

**🚀 [라이브 데모 보기](https://jeonghwanju-ai-search-agent.hf.space)** — Google AI Studio 무료 API 키로 바로 체험 가능

</div>

---

## 어떤 프로젝트인가요?

단순한 챗봇이 아니라, 질문을 받으면 **스스로 판단해서 웹 검색을 하고** 결과를 분석해 답변하는 AI Agent입니다.

```
사용자: "오늘 AI 뉴스 알려줘"

Agent:  🔍 "AI news today" 검색
        → 결과 분석
        → "오늘 주요 AI 뉴스는..."
```

---

## 핵심 개념: ReAct 패턴

```
질문 입력 → [Observe] 분석 → [Think] 검색 필요? → [Act] 웹 검색 → [Observe] 결과 충분? → 최종 답변
```

일반 챗봇은 입력 → 출력 한 번으로 끝나지만, AI Agent는 이 루프를 **필요한 만큼 반복**합니다.

---

## 기술 스택

| 역할 | 기술 | 비용 |
|------|------|:----:|
| LLM | Gemini 2.0 Flash (Google AI) | 무료 |
| 웹 검색 | DuckDuckGo | 무료 |
| Agent 프레임워크 | LangChain ReAct | 무료 |
| 백엔드 | FastAPI | 무료 |
| 배포 | HuggingFace Spaces | 무료 |

---

## 프로젝트 구조

```
AI_AGENT/
├── agent.py          # Agent 핵심 로직 (ReAct 구현)
├── main.py           # FastAPI 서버
├── static/
│   └── index.html    # 내장 프론트엔드 UI
├── Dockerfile        # HF Spaces 배포용
├── requirements.txt
└── README.md
```

---

## 로컬 실행

```bash
# 1. 설치
pip install -r requirements.txt

# 2. 실행
uvicorn main:app --reload --port 8000
```

- 웹 UI → `http://localhost:8000`
- API 문서 → `http://localhost:8000/docs`

---

## API 키 발급 방법

1. [aistudio.google.com](https://aistudio.google.com) 접속
2. 구글 계정으로 로그인
3. **Get API Key** → **Create API Key**
4. 발급된 키(`AIza...`)를 사이트 입력창에 붙여넣기

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 웹 UI |
| GET | `/health` | 서버 상태 확인 |
| POST | `/chat` | Agent 실행 |
| GET | `/docs` | Swagger 자동 문서 |

---

## 보안 설계

> 🔒 **API 키는 서버에 저장되지 않습니다.**  
> 사용자가 직접 Google AI Studio API 키를 입력하는 방식으로, 키가 서버에 보관되지 않고 요청마다 Google API로 직접 전달됩니다.  
> 대화가 끝나면 키는 브라우저 메모리에서 사라집니다.

| 항목 | 내용 |
|------|------|
| API 키 서버 저장 | ❌ 없음 |
| API 키 DB 기록 | ❌ 없음 |
| 대화 내용 저장 | ❌ 없음 |
| Google 무료 한도 공유 | ❌ 각자 본인 키 사용 |

---

<div align="center">

Made with LangChain + Google Gemini · 포트폴리오 프로젝트

</div>
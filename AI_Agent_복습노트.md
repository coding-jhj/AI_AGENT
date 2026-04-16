# 🤖 AI Search Agent 프로젝트 완전 복습 노트
> 예습 중인 초보자를 위한 일타강사 버전 — 이 노트 하나로 프로젝트 전체를 꿰뚫자!

---

## 📚 목차

1. [이 프로젝트가 뭔지부터 이해하자](#1-이-프로젝트가-뭔지부터-이해하자)
2. [핵심 개념: ReAct 패턴](#2-핵심-개념-react-패턴)
3. [기술 스택 전체 지도](#3-기술-스택-전체-지도)
4. [프로젝트 구조 파악하기](#4-프로젝트-구조-파악하기)
5. [agent.py — 두뇌 파일 완전 분석](#5-agentpy--두뇌-파일-완전-분석)
6. [main.py — FastAPI 서버 완전 분석](#6-mainpy--fastapi-서버-완전-분석)
7. [app.py — Streamlit UI 완전 분석](#7-apppy--streamlit-ui-완전-분석)
8. [requirements.txt — 의존성 관리](#8-requirementstxt--의존성-관리)
9. [Dockerfile — 배포 설정](#9-dockerfile--배포-설정)
10. [CHANGELOG — 코드 개선 과정 읽기](#10-changelog--코드-개선-과정-읽기)
11. [edu_chatbot_troubleshooting — RAG 챗봇 트러블슈팅](#11-edu_chatbot_troubleshooting--rag-챗봇-트러블슈팅)
12. [fix.py — 패치 스크립트 분석](#12-fixpy--패치-스크립트-분석)
13. [전체 데이터 흐름 한눈에 보기](#13-전체-데이터-흐름-한눈에-보기)
14. [면접 & 포트폴리오 질문 대비](#14-면접--포트폴리오-질문-대비)

---

## 1. 이 프로젝트가 뭔지부터 이해하자

### 📌 한 줄 요약
> "질문을 받으면 스스로 판단해서 웹 검색을 하고, 결과를 분석해 답변하는 AI Agent"

### 일반 챗봇 vs AI Agent 비교

| 구분 | 일반 챗봇 | AI Agent (이 프로젝트) |
|------|----------|----------------------|
| 동작 방식 | 입력 → 출력 (1회) | 입력 → 생각 → 행동 → 관찰 → 반복 |
| 외부 도구 사용 | ❌ 못 씀 | ✅ 웹 검색 등 도구 사용 가능 |
| 최신 정보 | ❌ 학습 시점까지만 | ✅ 실시간 웹 검색으로 최신 정보 획득 |
| 추론 과정 | 숨겨짐 | 중간 사고 과정이 보임 (Thought/Action/Observation) |

### 사용 시나리오 예시

```
사용자: "오늘 AI 뉴스 알려줘"

                  ↓

[Agent 내부 동작]
Thought: 최신 뉴스가 필요하다. 웹 검색이 필요하다.
Action: web_search
Action Input: "AI news today"
Observation: (검색 결과 텍스트)
Thought: 충분한 정보를 얻었다. 한국어로 정리하자.
Final Answer: "오늘 주요 AI 뉴스는..."
```

---

## 2. 핵심 개념: ReAct 패턴

### 🔍 ReAct란?
- **Re**asoning + **Act**ing 의 합성어
- 2022년 Google 연구팀이 발표한 LLM 기반 AI Agent 프레임워크

### ReAct 사이클 상세

```
         ┌─────────────────────────────────┐
         │           사용자 질문             │
         └──────────────┬──────────────────┘
                        ↓
         ┌──────────────────────────────────┐
         │  [Observe] 질문 분석              │
         │  → "이게 검색이 필요한 질문인가?"   │
         └──────────────┬───────────────────┘
                        ↓
         ┌──────────────────────────────────┐
         │  [Think] 추론                     │
         │  → "어떤 행동을 해야 하나?"         │
         └──────────────┬───────────────────┘
                        ↓
         ┌──────────────────────────────────┐
         │  [Act] 행동                       │
         │  → 검색 실행 OR 직접 답변          │
         └──────────────┬───────────────────┘
                        ↓
         ┌──────────────────────────────────┐
         │  [Observe] 결과 관찰              │
         │  → "이 결과로 충분한가?"           │
         └──────────────┬───────────────────┘
                   충분하면↓  부족하면→ [Think]로 돌아감
         ┌──────────────────────────────────┐
         │  [Final Answer] 최종 답변 출력    │
         └──────────────────────────────────┘
```

### 🌟 ReAct 패턴이 강력한 이유
1. **투명성**: 중간 사고 과정이 모두 보임 → 디버깅 용이
2. **유연성**: 필요에 따라 루프 횟수를 조절 가능
3. **확장성**: 검색 외에도 코드 실행, DB 조회 등 다양한 도구 추가 가능
4. **오류 복구**: 첫 검색 결과가 불충분하면 다시 시도 가능

### 코드에서 ReAct가 어떻게 구현되는가

`agent.py`의 SYSTEM_PROMPT를 보면 LLM에게 이런 형식으로 출력하도록 강제한다:

```
Question: 사용자 질문
Thought: 검색이 필요한가? 판단 과정
Action: web_search  ← 도구 이름
Action Input: 검색어  ← 도구 입력값
Observation: 검색 결과  ← 도구 실행 결과 (자동 채워짐)
Thought: 이제 충분한가?
Final Answer: 최종 한국어 답변
```

이 형식을 `create_react_agent()`가 파싱해서 실제 도구 호출을 수행한다.

---

## 3. 기술 스택 전체 지도

### 전체 아키텍처

```
┌──────────────────────────────────────────────────────┐
│                   사용자 브라우저                       │
│   (index.html / Streamlit UI)                        │
└─────────────────────┬────────────────────────────────┘
                      │  HTTP 요청 (POST /chat)
                      ↓
┌──────────────────────────────────────────────────────┐
│              FastAPI 백엔드 (main.py)                 │
│   - 요청 검증 (Pydantic)                              │
│   - Agent 생성 요청 전달                               │
└─────────────────────┬────────────────────────────────┘
                      │
                      ↓
┌──────────────────────────────────────────────────────┐
│            LangChain Agent (agent.py)                │
│   - ReAct 패턴으로 LLM 제어                           │
│   - 도구 실행 판단 및 결과 파싱                         │
└───────────┬──────────────────────┬───────────────────┘
            │                      │
            ↓                      ↓
┌─────────────────┐    ┌────────────────────────────┐
│  Google Gemini  │    │   DuckDuckGo 검색 API       │
│  (LLM)          │    │   (무료, API 키 불필요)      │
│  - 추론 담당     │    │   - 실시간 웹 검색 담당      │
└─────────────────┘    └────────────────────────────┘
```

### 각 기술 선택 이유

| 기술 | 역할 | 선택 이유 |
|------|------|----------|
| **Google Gemini** | LLM (두뇌) | 무료 API, 한국어 성능 우수, 분당 요청 한도 넉넉 |
| **DuckDuckGo** | 웹 검색 | API 키 불필요, 완전 무료, 개인정보 정책 양호 |
| **LangChain** | Agent 프레임워크 | ReAct 패턴 구현 추상화, 도구 통합 쉬움 |
| **FastAPI** | 백엔드 서버 | Python 생태계, 자동 API 문서(Swagger), 빠른 개발 |
| **Streamlit** | 대안 UI | 데이터 분석가에게 친숙, 빠른 프로토타이핑 |
| **HuggingFace Spaces** | 배포 | 무료 Docker 호스팅, 포트폴리오 공유 용이 |

---

## 4. 프로젝트 구조 파악하기

```
AI_AGENT/
├── agent.py          # 🧠 핵심 로직 — LLM + 검색 도구 + ReAct
├── main.py           # 🌐 FastAPI 서버 — HTTP API 엔드포인트
├── app.py            # 🖥️ Streamlit UI — 대안 웹 인터페이스
├── fix.py            # 🔧 일회성 패치 스크립트
├── static/
│   └── index.html    # 🎨 내장 프론트엔드 (main.py가 서빙)
├── Dockerfile        # 🐳 HuggingFace Spaces 배포용
├── requirements.txt  # 📦 Python 패키지 목록
├── README.md         # 📖 프로젝트 소개
└── CHANGELOG.md      # 📝 변경 내역 (멘토 피드백 반영)
```

### 파일 간 관계도

```
main.py ──── import ────→ agent.py
  ↑                          ↑
  │ HTTP                     │ import
  │                     (langchain 패키지들)
index.html
  (static/)

app.py ──── import ────→ agent.py  ← Streamlit 버전도 같은 agent 사용
```

> **핵심 포인트**: `agent.py`가 비즈니스 로직의 핵심이고, `main.py`와 `app.py`는 각각 다른 UI로 같은 로직을 서빙한다. 이것이 **관심사 분리(Separation of Concerns)** 설계 원칙이다.

---

## 5. agent.py — 두뇌 파일 완전 분석

### 전체 코드 구조

```python
# 크게 4개 파트로 나뉜다
1. import 선언부
2. SYSTEM_PROMPT (LLM 행동 지침)
3. create_agent() 함수
4. format_history() + run_agent() 유틸 함수
```

---

### 5-1. import 분석

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
```

| import | 역할 | 패키지 위치 |
|--------|------|------------|
| `ChatGoogleGenerativeAI` | Gemini API를 LangChain에서 쓸 수 있게 감싼 클래스 | `langchain-google-genai` |
| `DuckDuckGoSearchRun` | DuckDuckGo 검색을 LangChain 도구로 감싼 클래스 | `langchain-community` |
| `create_react_agent` | ReAct 패턴 Agent 생성 함수 | `langchain` |
| `AgentExecutor` | Agent를 실제로 실행하는 래퍼 클래스 | `langchain` |
| `PromptTemplate` | 프롬프트 템플릿 (변수 치환 지원) | `langchain-core` |

> 💡 **왜 패키지가 여러 개로 나뉘어 있나?**  
> LangChain은 v0.1부터 모노레포를 분리했다. 핵심 로직(`langchain-core`) / 통합 도구들(`langchain-community`) / 특정 제공사(`langchain-google-genai`) 로 나눠 필요한 것만 설치할 수 있게 했다. 이걸 모르면 `ModuleNotFoundError`로 고생한다.

---

### 5-2. SYSTEM_PROMPT 완전 해부

```python
SYSTEM_PROMPT = """You are a highly capable AI Search Agent. You MUST answer in Korean only.

CRITICAL RULES:
1. For greetings, simple questions, math, or general knowledge → answer IMMEDIATELY with "Final Answer"
2. ONLY use web_search for: current news, recent events, real-time data, specific facts you are uncertain about.
3. Search at most ONCE per question. Never repeat searches.
4. Keep answers concise but complete.
5. NEVER use Chinese or Japanese characters.
...
"""
```

#### 왜 프롬프트가 이렇게 중요한가?

ReAct 패턴은 **LLM이 정해진 형식으로 출력**해야 작동한다.
LangChain이 출력을 파싱해서 실제 도구를 호출하기 때문이다.

```
LLM 출력:
"Thought: 검색이 필요하다
Action: web_search          ← LangChain이 이 줄을 읽어서
Action Input: AI news today ← 이 값으로 실제 검색 실행"
```

만약 LLM이 형식을 어기면 파싱 오류가 난다. 그래서 `handle_parsing_errors=True`로 설정해두었다.

#### 프롬프트 핵심 변수들

```python
{tools}       # 사용 가능한 도구 목록과 설명 (LangChain이 자동 채움)
{tool_names}  # 도구 이름만 (예: "web_search")
{chat_history} # 이전 대화 내역
{input}       # 사용자 질문
{agent_scratchpad} # Agent의 중간 추론 과정 (LangChain이 관리)
```

> 💡 **`agent_scratchpad`란?**  
> Agent가 루프를 돌면서 생성한 Thought/Action/Observation 내역이 누적되는 공간이다. 이게 있어야 LLM이 "아, 이미 검색했구나, 이제 답변을 내자"라는 판단을 할 수 있다.

---

### 5-3. create_agent() 함수 상세

```python
def create_agent(google_api_key: str, model: str = "gemini-2.0-flash") -> AgentExecutor:
    # 1단계: LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=google_api_key,
        temperature=0.3,       # 낮을수록 일관된 답변 (0~1)
        max_output_tokens=2048, # 최대 출력 토큰 수
    )

    # 2단계: 도구 정의
    tools = [DuckDuckGoSearchRun(
        name="web_search",
        description="Search the web for current events..."
    )]

    # 3단계: 프롬프트 템플릿 생성
    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

    # 4단계: Agent 생성 (LLM + 도구 + 프롬프트 연결)
    agent = create_react_agent(llm, tools, prompt)

    # 5단계: AgentExecutor로 감싸기 (실행 제어 추가)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,           # 콘솔에 추론 과정 출력 (개발 시 유용)
        max_iterations=3,       # 최대 루프 횟수 (무한루프 방지)
        max_execution_time=30,  # 30초 타임아웃
        handle_parsing_errors=True,  # 파싱 오류 시 자동 복구 시도
        return_intermediate_steps=True,  # 중간 단계 결과 반환
    )
```

#### `temperature` 값의 의미

```
temperature=0 → 항상 같은 답 (결정론적)
temperature=0.3 → 약간의 변동성 (사실 기반 질문에 적합)
temperature=0.7 → 창의적인 답 (창작 등에 적합)
temperature=1.0 → 매우 창의적/무작위적
```

#### AgentExecutor 파라미터 정리

| 파라미터 | 값 | 역할 |
|---------|-----|------|
| `verbose` | True | 추론 과정을 터미널에 출력 (디버깅용) |
| `max_iterations` | 3 | Thought→Action 루프 최대 3회 (무한루프 방지) |
| `max_execution_time` | 30 | 30초 초과 시 강제 종료 |
| `handle_parsing_errors` | True | LLM 출력 형식 오류 시 자동 복구 시도 |
| `return_intermediate_steps` | True | 중간 Action/Observation 결과 반환 (검색 여부 확인용) |

---

### 5-4. format_history() 함수

```python
def format_history(messages: list) -> str:
    if not messages:
        return "없음"
    recent = messages[-6:]  # 최근 6턴만 유지 (토큰 절약)
    result = []
    for msg in recent:
        role = "사용자" if msg["role"] == "user" else "AI"
        result.append(f"{role}: {msg['content']}")
    return "\n".join(result)
```

#### 왜 최근 6턴만 유지하나?

LLM은 입력 토큰 한도가 있고, 토큰이 많을수록 API 비용이 증가한다.
대화 맥락은 보통 최근 몇 턴만 봐도 충분하다.

```
예: 20턴 대화 기록이 있을 때
전체 포함: 토큰 폭탄 → 느림 + 비용 증가 + 한도 초과 위험
최근 6턴만: 적절한 맥락 유지 + 효율적인 토큰 사용
```

---

### 5-5. run_agent() 함수

```python
def run_agent(agent_executor, user_input, history) -> dict:
    result = agent_executor.invoke({
        "input": user_input,
        "chat_history": format_history(history),
    })

    # 웹 검색을 했는지 확인
    searched = False
    search_query = None
    for action, observation in result.get("intermediate_steps", []):
        if hasattr(action, "tool") and action.tool == "web_search":
            searched = True
            search_query = action.tool_input
            break

    return {
        "answer": result["output"],
        "searched": searched,
        "search_query": search_query,
    }
```

#### `intermediate_steps` 파싱하는 이유

UI에서 "🔍 웹 검색 사용: [검색어]" 뱃지를 표시하기 위해
Agent가 실제로 검색을 했는지, 어떤 검색어를 사용했는지 알아야 한다.

`return_intermediate_steps=True`로 설정했기 때문에
`result["intermediate_steps"]`에 `[(AgentAction, observation), ...]` 형태로 담겨있다.

#### 반환값 구조

```python
{
    "answer": "오늘 AI 뉴스는...",  # 최종 답변
    "searched": True,              # 검색 여부
    "search_query": "AI news today" # 실제 사용한 검색어
}
```

---

## 6. main.py — FastAPI 서버 완전 분석

### FastAPI란?

Python의 웹 프레임워크. Flask보다 빠르고, 자동 API 문서(Swagger)를 제공한다.

```
FastAPI 핵심 특징:
✅ Python 타입 힌트 기반 자동 검증
✅ /docs 경로에 Swagger UI 자동 생성
✅ 비동기(async) 지원으로 높은 성능
✅ Pydantic으로 요청/응답 데이터 자동 검증
```

---

### 6-1. 서버 초기화

```python
app = FastAPI(
    title="AI Search Agent API",
    description="ReAct 패턴 기반 웹 검색 AI Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### CORS(Cross-Origin Resource Sharing)란?

브라우저 보안 정책으로, 다른 도메인에서 API 요청을 막는다.
`allow_origins=["*"]`는 개발/포트폴리오용으로는 OK.
**실제 프로덕션에서는 특정 도메인만 허용해야 한다!**

```python
# 프로덕션 예시
allow_origins=["https://my-frontend.com", "https://www.my-frontend.com"]
```

---

### 6-2. Pydantic 모델 (데이터 검증)

```python
class Message(BaseModel):
    role: str    # "user" 또는 "assistant"
    content: str # 메시지 내용

class ChatRequest(BaseModel):
    model: str = "gemini-2.0-flash"  # 기본값 있음
    api_key: str
    user_input: str
    history: list[Message] = []  # 기본값: 빈 리스트

class ChatResponse(BaseModel):
    answer: str
    searched: bool
    search_query: Optional[str] = None  # 없을 수도 있음
```

#### Pydantic이 해주는 것

```python
# 잘못된 요청이 들어오면 FastAPI가 자동으로 400 에러 반환
{
    "api_key": 12345,  # str이어야 하는데 int가 들어오면 → 자동 에러
    "user_input": ""   # 검증은 통과, 하지만 아래 코드에서 수동 체크
}
```

---

### 6-3. 엔드포인트 분석

```python
@app.get("/health")
def health():
    return {"status": "ok", "message": "AI Search Agent is running 🚀"}
```
**용도**: 서버가 살아있는지 확인. 배포 플랫폼의 헬스체크에 활용.

---

```python
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # 1. 수동 검증 (Pydantic이 못 잡는 비즈니스 로직)
    if not req.api_key.strip():
        raise HTTPException(status_code=400, detail="API 키가 필요합니다.")
    if not req.user_input.strip():
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")

    try:
        # 2. Agent 생성 (매 요청마다 새로 생성 — 보안상 이유, CHANGELOG 참조)
        agent_executor = get_or_create_agent(req.api_key, req.model)
        
        # 3. 대화 기록 변환 (Pydantic 모델 → dict)
        history = [{"role": m.role, "content": m.content} for m in req.history]
        
        # 4. Agent 실행
        result = run_agent(agent_executor, req.user_input, history)
        return ChatResponse(**result)

    except Exception as e:
        err = str(e)
        # 5. 에러 분류
        if "api_key" in err.lower() or "authentication" in err.lower():
            raise HTTPException(status_code=401, detail="API 키가 올바르지 않습니다.")
        raise HTTPException(status_code=500, detail=f"Agent 오류: {err[:200]}")
```

#### HTTP 상태 코드 정리

| 코드 | 의미 | 이 프로젝트에서 사용 |
|------|------|---------------------|
| 200 | 성공 | Agent 정상 응답 |
| 400 | 잘못된 요청 (클라이언트 오류) | API 키 없음, 질문 없음 |
| 401 | 인증 실패 | API 키 유효하지 않음 |
| 500 | 서버 내부 오류 | Agent 실행 중 예상치 못한 오류 |

---

```python
@app.get("/", response_class=HTMLResponse)
def index():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>index.html을 static/ 폴더에 넣어주세요.</h1>")
```

**용도**: FastAPI가 직접 HTML 파일을 서빙. 별도 프론트엔드 서버가 필요 없다.

---

## 7. app.py — Streamlit UI 완전 분석

### Streamlit이란?

Python 코드만으로 웹 앱을 만드는 라이브러리. HTML/CSS/JS를 몰라도 된다.
데이터 분석 포트폴리오에 특히 적합하다.

### Streamlit vs FastAPI+HTML 비교

| 항목 | Streamlit | FastAPI + HTML |
|------|-----------|----------------|
| 개발 속도 | 매우 빠름 | 보통 |
| 커스터마이징 | 제한적 | 자유로움 |
| 성능 | 보통 (새로고침마다 재실행) | 좋음 |
| 배포 | Streamlit Cloud (무료) | 직접 설정 필요 |
| 학습 곡선 | 낮음 | 보통 |

---

### 7-1. 세션 상태 (session_state)

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "groq_key" not in st.session_state:
    st.session_state.groq_key = ""
```

#### Streamlit의 특이한 동작 방식

> Streamlit은 사용자가 버튼 클릭, 입력 등 **어떤 인터랙션을 해도 전체 스크립트를 처음부터 다시 실행**한다!

그렇기 때문에 일반 Python 변수는 인터랙션 후 사라진다.
`st.session_state`에 저장해야 인터랙션 후에도 유지된다.

```python
# ❌ 일반 변수 → 인터랙션마다 초기화됨
messages = []

# ✅ session_state → 세션 동안 유지됨
if "messages" not in st.session_state:
    st.session_state.messages = []
```

---

### 7-2. 사이드바 구성

```python
with st.sidebar:
    st.title("🤖 AI Search Agent")
    
    # API 키 입력
    api_key = st.text_input(
        label="API Key",
        type="password",  # 입력값 숨김
        placeholder="gsk_...",
    )

    # API 키가 새로 입력되면 Agent 생성
    if api_key and api_key != st.session_state.groq_key:
        with st.spinner("연결 중..."):
            try:
                st.session_state.agent = create_agent(api_key)
                st.session_state.groq_key = api_key
                st.success("연결됐어요!")
            except Exception as e:
                st.error(f"키 오류: {str(e)[:80]}")
```

> 💡 `api_key != st.session_state.groq_key` 조건의 의미:  
> 이미 같은 키로 Agent가 생성되어 있으면 다시 생성하지 않는다. (불필요한 재생성 방지)

---

### 7-3. 채팅 UI 구현

```python
# 이전 대화 렌더링
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):  # "user" 또는 "assistant"
        if msg.get("searched"):
            st.markdown(
                f'<span class="search-badge">🔍 웹 검색 사용: {msg.get("search_query", "")}</span>',
                unsafe_allow_html=True
            )
        st.write(msg["content"])

# 새 입력 받기
user_input = st.chat_input("무엇이든 물어보세요...", disabled=not st.session_state.agent)

if user_input and st.session_state.agent:
    # 사용자 메시지 즉시 표시
    with st.chat_message("user"):
        st.write(user_input)
    
    # 대화 기록에 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Agent 실행
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            result = run_agent(...)
        st.write(result["answer"])
    
    # 응답도 기록에 추가
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "searched": result["searched"],
        "search_query": result.get("search_query"),
    })
```

#### 중요한 UX 패턴
- `disabled=not st.session_state.agent` → API 키 입력 전에는 채팅 입력창 비활성화
- `st.spinner("생각 중...")` → Agent 실행 중 로딩 표시
- 사용자 메시지를 기록에 추가한 뒤 `run_agent()`에 `messages[:-1]`을 전달 → 방금 추가한 메시지 제외 (중복 방지)

---

## 8. requirements.txt — 의존성 관리

```
langchain>=0.3.25          # LangChain 핵심
langchain==0.3.25           # 정확한 버전 고정 (충돌 방지)
langchain-groq==0.2.5       # Groq LLM 통합 (과거 버전 흔적)
langchain-community==0.3.24 # DuckDuckGo 등 커뮤니티 도구
langchain-core>=0.3.58      # LangChain 내부 코어
duckduckgo-search>=6.0.0    # DuckDuckGo 검색 라이브러리
fastapi>=0.115.0            # FastAPI 웹 프레임워크
uvicorn[standard]>=0.32.0   # FastAPI 실행 서버 (ASGI)
python-multipart>=0.0.12    # FastAPI 파일 업로드 지원
langchain-google-genai>=2.0.0 # Gemini LLM 통합
```

#### 주의할 점: `>=` vs `==` 혼재

```
langchain>=0.3.25   # 0.3.25 이상이면 OK
langchain==0.3.25   # 정확히 0.3.25만 OK
```

실제로는 둘 다 써서 "최소한 이 버전 이상이지만, 정확히 이 버전으로 고정"하려는 의도.
하지만 `pip`는 같은 패키지에 두 조건이 있으면 더 엄격한 조건(`==`)을 따른다.

#### `uvicorn[standard]`의 `[standard]`는?

extra 패키지 설치 옵션이다. `standard`를 붙이면:
- `websockets` (WebSocket 지원)
- `httptools` (빠른 HTTP 파싱)

등 추가 성능 최적화 패키지가 함께 설치된다.

#### CHANGELOG에서 언급된 Groq → Gemini 전환 흔적

`requirements.txt`에 `langchain-groq`가 남아있는 것은 이 프로젝트가 원래 Groq LLM을 썼다가 Google Gemini로 전환했기 때문이다. `app.py`의 사이드바 설명에도 "Groq API 키"라고 되어있어 불일치가 있다. 이런 점을 발견하고 정리하는 것이 코드 리뷰 역량이다.

---

## 9. Dockerfile — 배포 설정

```dockerfile
# (파일 내용 추정 — HuggingFace Spaces 표준 패턴)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860  # HF Spaces 기본 포트

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```

#### Docker 기본 개념

```
Docker = 앱을 컨테이너(격리된 환경)에 담아 어디서나 동일하게 실행

Dockerfile = 컨테이너 레시피
  FROM    → 베이스 이미지 (Python 3.11)
  WORKDIR → 작업 디렉토리
  COPY    → 파일 복사
  RUN     → 명령 실행 (패키지 설치)
  EXPOSE  → 열 포트 선언
  CMD     → 컨테이너 시작 시 실행할 명령
```

#### HuggingFace Spaces README 헤더

```yaml
---
title: AI Search Agent
emoji: 🤖
colorFrom: green
colorTo: blue
sdk: docker       # Docker 기반 배포
app_port: 7860    # 외부에 노출할 포트
---
```

이 YAML 헤더가 HF Spaces에게 "이 앱은 Docker로 실행하고, 7860 포트를 써"라고 알려준다.

---

## 10. CHANGELOG — 코드 개선 과정 읽기

> CHANGELOG는 단순한 변경 이력이 아니라, **개발자의 사고 과정과 문제 해결 능력**을 보여준다. 포트폴리오에서 매우 중요한 문서다.

---

### 10-1. P0: `_agent_cache` 제거 — 보안 버그 수정

#### 변경 전 코드 (문제 있음)

```python
_agent_cache: dict = {}  # API 키 → Agent 객체 매핑

def get_or_create_agent(api_key, model):
    if api_key not in _agent_cache:
        _agent_cache[api_key] = create_agent(api_key, model)
    return _agent_cache[api_key]
```

#### 문제점 분석

```
문제 1 [보안]: _agent_cache의 key가 API 키 문자열
  → 서버가 살아있는 동안 메모리에 API 키 잔류
  → HuggingFace Spaces 같은 공유 환경에서 메모리 덤프 발생 시 키 노출 위험
  → README에 "서버에 키를 저장하지 않습니다"라고 써놨는데 실제로는 저장하고 있었음!
  → 문서-코드 불일치 (거짓말)

문제 2 [실익 없음]: 캐시로 절약하려는 비용이 없다
  → LLM API 호출: 수백ms~수초
  → Python 객체 생성(create_agent): 수ms 이하
  → 최적화 효과 무시할 수준
```

#### 변경 후 코드 (수정됨)

```python
def get_or_create_agent(api_key, model):
    return create_agent(api_key, model)  # 캐시 없이 매번 새로 생성
```

```
장점: API 키가 함수 스코프에만 존재
      → 함수 종료 시 가비지 컬렉션 대상
      → README 내용과 실제 동작 일치
```

#### 🎓 배울 점
> **"작동하는 코드"와 "올바른 코드"는 다르다.**  
> 성능 최적화는 실제 병목 지점에만 적용해야 한다. (섣부른 최적화는 악이다 — Donald Knuth)  
> 보안과 문서의 일치성은 신뢰의 기반이다.

---

### 10-2. P0: max_tokens 축소 — 무료 한도 최적화

```python
# 변경 전
max_output_tokens=2048

# 변경 후  
max_output_tokens=1024
```

#### 왜 줄였나?

ReAct 루프에서 토큰이 누적되는 방식 이해:

```
루프 1회:
  [Thought] + [Action] + [Observation] = ~500 토큰

루프 2회:
  [이전 루프 내용 전체] + [Thought] + [Action] + [Observation] = ~1000 토큰

루프 3회:
  [이전 루프 내용 전체] + [Thought] + [Action] + [Observation] = ~1500 토큰
```

무료 Groq API의 TPM(Tokens Per Minute) 한도가 6,000일 때:
- `max_tokens=2048` → 루프 2-3회만에 한도 도달
- `max_tokens=1024` → 같은 TPM에서 루프를 2배 더 돌 수 있음

---

### 10-3. P1: 모델 선택 드롭다운

#### Llama 3.3 70B vs Llama 3.1 8B

| 항목 | 70B (Versatile) | 8B (Instant) |
|------|-----------------|--------------|
| 품질 | 높음 | 충분함 (Agent 수준) |
| 속도 | 느림 | 빠름 |
| TPM 한도 | 엄격 | 관대 |
| 권장 상황 | 복잡한 분석 | 검색+요약 (이 프로젝트) |

---

### 10-4. P1: API 키 localStorage 저장

```javascript
// 기본값: 저장 안 함 (안전한 기본 동작)
// 체크박스로 명시적 동의 후 저장
keyInput.addEventListener('change', () => {
    if (saveKeyCheckbox.checked) {
        localStorage.setItem('groq_api_key', keyInput.value.trim());
    }
});
```

#### 보안 설계 원칙

> **"안전한 기본값(Secure by Default)"**: 사용자가 별도 조작을 하지 않으면 가장 안전한 상태를 유지한다.

공용 PC에서 키가 저장되면 다음 사용자가 접근할 수 있다.
그래서 기본값을 "저장 안 함"으로 하고, 동의 체크 후에만 저장한다.

---

## 11. edu_chatbot_troubleshooting — RAG 챗봇 트러블슈팅

> 이 파일은 별개 프로젝트(RAG 챗봇)의 트러블슈팅 노트다.  
> AI 개발자로서 반드시 알아야 할 실전 지식들이 담겨있다.

### RAG(Retrieval-Augmented Generation)란?

```
일반 LLM의 한계:
  → 학습 데이터에 없는 정보 모름
  → 최신 정보 모름
  → 특정 도메인(회사 내부 문서 등) 모름

RAG 해결책:
  → 외부 문서를 벡터 DB에 저장
  → 질문과 유사한 문서 검색
  → 검색된 문서를 컨텍스트로 LLM에 제공
  → LLM이 해당 컨텍스트 기반으로 답변

                질문
                 ↓
         [벡터 유사도 검색]
                 ↓
         [관련 문서 청크 추출]
                 ↓
    [LLM: "이 문서를 참고해서 답해줘"]
                 ↓
              답변 생성
```

---

### 11-1. 주요 트러블슈팅 정리

#### ① ChromaDB sqlite 버전 문제

```python
# 증상: RuntimeError: Your system has an unsupported version of sqlite3
# 해결:
pip install pysqlite3-binary

# 코드 최상단에:
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
```

> **왜 이런 문제가?**  
> ChromaDB는 내부적으로 SQLite를 사용하는데, Python 표준 라이브러리의 sqlite3 버전이 너무 낮으면 작동 안 함. 특히 Ubuntu 20.04 같은 구버전 OS에서 발생.

#### ② LangChain 버전 충돌

LangChain은 버전 간 API 변화가 크다. `requirements.txt`에 정확한 버전 고정이 필수.

```
# ❌ 위험
langchain

# ✅ 안전
langchain==0.2.16
```

#### ③ `@st.cache_resource` 누락

```python
# ❌ 이러면 매 인터랙션마다 400MB 모델 재로드
def load_chain():
    return create_rag_chain()

# ✅ 최초 1회만 로드, 이후 캐시 사용
@st.cache_resource
def load_chain():
    return create_rag_chain()
```

#### ④ 검색 품질 개선

```python
# 기본 similarity 검색 → MMR(Maximal Marginal Relevance)로 변경
# MMR: 관련성 + 다양성을 동시에 최적화
retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10}
    # k: 최종 반환 문서 수
    # fetch_k: 일단 가져오는 후보 문서 수 (k보다 많아야 함)
)
```

#### ⑤ 청크 크기 튜닝

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,   # 교육 Q&A에 최적
    chunk_overlap=100  # 청크 경계에서 문맥 유지
)
```

```
chunk_size 너무 작으면: 문맥이 끊겨 검색 품질 저하
chunk_size 너무 크면: 관련 없는 내용까지 포함, 답변 품질 저하
chunk_overlap: 두 청크 경계에 겹치는 부분 → 문맥 연결성 유지
```

---

### 11-2. AI Hub 데이터 처리 팁

```python
# 데이터 구조 먼저 확인하는 습관
with open("dataset/train/train_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))       # list인지 dict인지 확인
print(data[0].keys())   # 어떤 키가 있는지 확인
print(data[0])          # 실제 데이터 샘플 확인
```

> 💡 **실전 꿀팁**: 데이터셋마다 JSON 키 이름이 제각각이다. `question`/`answer`일 수도 있고, `ques`/`ans`일 수도 있다. 무조건 먼저 구조를 확인하자.

---

### 11-3. 배포 시 주의사항

```
# .gitignore 필수 항목
.env                # API 키 — 절대 공개 금지!
dataset/            # AI Hub 데이터 — 라이선스 문제
chroma_db/          # 벡터 DB — 용량이 수백 MB
__pycache__/        # Python 캐시
chatbot_env/        # 가상환경
```

---

## 12. fix.py — 패치 스크립트 분석

```python
with open("static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 기존 코드 (문제 있음): 페이지 로드 시 즉시 API 키 자동 로드
old = """
  const savedKey = localStorage.getItem('groq_api_key');
  if (savedKey) { keyInput.value = savedKey; keyInput.dispatchEvent(new Event('input')); }
  ...
"""
html = html.replace(old, "", 1)  # 기존 코드 제거

# 새 코드: 이벤트 리스너 등록을 먼저, 저장된 값 로드를 나중에
new_storage = """
  keyInput.addEventListener('change', () => { localStorage.setItem('groq_api_key', keyInput.value.trim()); });
  ...
  const savedKey = localStorage.getItem('groq_api_key');  ← 리스너 등록 후 로드
  if (savedKey) { keyInput.value = savedKey; keyInput.dispatchEvent(new Event('input')); }
"""
html = html.replace("  keyInput.addEventListener('input', () => {",
                    new_storage + "\n  keyInput.addEventListener('input', () => {", 1)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(html)
```

#### 왜 순서가 중요한가?

```javascript
// ❌ 문제: 이벤트 리스너 등록 전에 값 로드 → 'change' 이벤트가 발생해도 리스너가 없음
const savedKey = localStorage.getItem('groq_api_key');
if (savedKey) { keyInput.value = savedKey; keyInput.dispatchEvent(new Event('input')); }
keyInput.addEventListener('change', () => { localStorage.setItem('groq_api_key', keyInput.value); });

// ✅ 수정: 리스너 먼저 등록 → 이후 값 로드 시 리스너가 정상 작동
keyInput.addEventListener('change', () => { localStorage.setItem('groq_api_key', keyInput.value); });
const savedKey = localStorage.getItem('groq_api_key');
if (savedKey) { keyInput.value = savedKey; keyInput.dispatchEvent(new Event('input')); }
```

#### `str.replace(old, new, 1)`의 `1`은?

세 번째 인자는 교체 횟수 제한이다. `1`을 쓰면 첫 번째 발견된 것만 교체한다.
같은 문자열이 여러 곳에 있을 때 실수로 전부 바꾸는 것을 방지한다.

---

## 13. 전체 데이터 흐름 한눈에 보기

### 사용자가 질문을 입력했을 때 전체 흐름

```
① 사용자: "오늘 삼성 주가 알려줘" 입력
          ↓
② 브라우저 (index.html):
   POST /chat 요청
   Body: { api_key, user_input, model, history }
          ↓
③ FastAPI (main.py):
   - Pydantic으로 요청 검증
   - api_key, user_input 비어있는지 확인
   - get_or_create_agent(api_key, model) 호출
          ↓
④ agent.py - create_agent():
   - ChatGoogleGenerativeAI 초기화
   - DuckDuckGoSearchRun 도구 준비
   - AgentExecutor 생성
          ↓
⑤ agent.py - run_agent():
   - agent_executor.invoke() 호출
          ↓
⑥ LangChain AgentExecutor:
   SYSTEM_PROMPT + 사용자 질문을 Gemini에 전달
          ↓
⑦ Google Gemini (LLM):
   "Thought: 주가는 실시간 데이터가 필요하다. 검색하자.
    Action: web_search
    Action Input: 삼성 주가 오늘"
          ↓
⑧ LangChain: "web_search" 도구 인식 → DuckDuckGoSearchRun 실행
          ↓
⑨ DuckDuckGo 검색 API:
   검색 결과 텍스트 반환
          ↓
⑩ LangChain → Gemini에 Observation 추가 후 재요청:
   "Observation: 삼성전자 현재 주가 72,000원..."
          ↓
⑪ Google Gemini:
   "Thought: 충분한 정보를 얻었다.
    Final Answer: 오늘 삼성전자 주가는 72,000원입니다..."
          ↓
⑫ run_agent(): intermediate_steps에서 검색 여부 확인
   → {"answer": "...", "searched": True, "search_query": "삼성 주가 오늘"}
          ↓
⑬ FastAPI: ChatResponse로 직렬화 후 JSON 반환
          ↓
⑭ 브라우저: 답변 표시 + "🔍 웹 검색 사용: 삼성 주가 오늘" 뱃지 표시
```

---

## 14. 면접 & 포트폴리오 질문 대비

### Q1. "이 프로젝트에서 가장 어려웠던 점은?"

> 좋은 답변 방향:  
> "ReAct 패턴에서 LLM이 정해진 형식을 지키지 않을 때 파싱 오류가 발생했습니다. `handle_parsing_errors=True`로 자동 복구를 설정했고, 시스템 프롬프트에 명확한 형식 지침을 추가해 오류율을 낮췄습니다."

---

### Q2. "보안상 어떤 점을 고려했나요?"

> 핵심 포인트:
> - API 키를 서버에 저장하지 않음 (함수 스코프 내 소멸)
> - 클라이언트에서 localStorage 저장은 사용자 명시적 동의 후만
> - API 키 노출 방지 (`type="password"` input)
> - 에러 메시지에 내부 정보 제한 (`err[:200]`)

---

### Q3. "일반 챗봇과 AI Agent의 차이는?"

> 핵심 답변:
> - 일반 챗봇: 학습된 지식만 활용, 단순 입출력
> - AI Agent: 도구(웹검색, DB조회, 코드실행 등) 사용 가능, 다단계 추론, 실시간 정보 획득

---

### Q4. "왜 Groq 대신 Gemini를 선택했나요?"

> CHANGELOG 기반 답변:
> - Groq 무료 TPM 한도가 6,000으로 ReAct 루프에 불리
> - Google AI Studio는 무료 한도가 더 관대
> - Gemini 2.0 Flash는 속도와 품질 균형이 좋음

---

### Q5. "LangChain을 왜 사용했나요? 직접 구현할 수도 있지 않나요?"

> 좋은 답변:
> - ReAct 패턴 구현에 필요한 프롬프트 파싱, 도구 호출, 루프 관리를 추상화
> - 직접 구현 시 수백 줄의 파싱 로직이 필요
> - LangChain으로 핵심 로직(프롬프트 설계, 도구 통합)에 집중 가능
> - 단점: LangChain 버전 업에 따른 API 변경 리스크

---

### 핵심 키워드 정리

| 키워드 | 설명 |
|--------|------|
| **ReAct** | Reasoning + Acting. LLM 기반 Agent 패턴 |
| **AgentExecutor** | LangChain에서 Agent를 실행하는 래퍼 |
| **intermediate_steps** | Agent 실행 중 중간 Action/Observation 기록 |
| **temperature** | LLM 출력의 무작위성 (0=결정론적, 1=창의적) |
| **RAG** | Retrieval-Augmented Generation. 외부 문서 검색 + LLM |
| **ChromaDB** | 벡터 임베딩 저장/검색 DB |
| **Pydantic** | Python 타입 기반 데이터 검증 라이브러리 |
| **CORS** | 브라우저의 Cross-Origin 요청 보안 정책 |
| **session_state** | Streamlit에서 인터랙션 간 데이터 유지 수단 |
| **TPM** | Tokens Per Minute. API 분당 토큰 한도 |
| **MMR** | Maximal Marginal Relevance. 다양성 고려 검색 방식 |
| **chunk_size** | RAG에서 문서를 쪼개는 단위 크기 |

---

## 🏁 마무리: 이 프로젝트로 알 수 있는 것들

```
✅ AI Agent의 개념과 ReAct 패턴 구현 방법
✅ LangChain을 활용한 LLM + 도구 통합 방법
✅ FastAPI로 RESTful API 서버 구축
✅ Streamlit으로 빠른 AI 앱 프로토타이핑
✅ 보안 설계 원칙 (API 키 관리, Secure by Default)
✅ 성능 최적화 vs 보안 트레이드오프 판단
✅ RAG 챗봇 구축과 트러블슈팅
✅ Docker + HuggingFace Spaces 배포
✅ 코드 리뷰와 CHANGELOG 작성 문화
```

> 💪 **앞으로 공부할 방향**:  
> 1. LangGraph — 더 복잡한 멀티 Agent 워크플로우  
> 2. 벡터 DB (ChromaDB, Pinecone) — RAG 심화  
> 3. FastAPI 비동기 처리 — `async def` 패턴  
> 4. 프롬프트 엔지니어링 심화 — 프롬프트 최적화 기법

---

*📅 작성일: 2025 | AI Human Camp 4기 복습 노트*

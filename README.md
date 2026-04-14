# 🤖 AI Search Agent

> 스스로 웹 검색하고 판단하는 AI Agent — ReAct 패턴 구현 포트폴리오

**🚀 [라이브 데모 보기](https://your-app.streamlit.app)** &nbsp;|&nbsp; Groq 무료 API 키로 바로 체험 가능

---

## 어떤 프로젝트인가요?

단순한 챗봇이 아니라, 질문을 받으면 **스스로 판단해서 웹 검색을 하고**, 결과를 분석해 답변하는 AI Agent입니다.

```
사용자: "오늘 AI 뉴스 알려줘"

Agent:  🔍 "AI news today" 검색
        → 결과 분석
        → "오늘 주요 AI 뉴스는..."
```

---

## 핵심 개념: ReAct 패턴

```
질문 입력
   ↓
[Observe]  질문 분석
   ↓
[Think]    검색이 필요한가?
   ↓              ↓
  Yes            No
   ↓              ↓
[Act]           최종 답변
웹 검색
   ↓
[Observe]  결과 충분한가?
   ↓
최종 답변
```

일반 챗봇은 입력 → 출력 한 번으로 끝나지만,
AI Agent는 이 루프를 **필요한 만큼 반복**합니다.

---

## 기술 스택

| 역할 | 기술 | 비용 |
|------|------|------|
| LLM | Llama 3.3 70B (Groq) | 무료 |
| 웹 검색 | DuckDuckGo | 무료 |
| Agent 프레임워크 | LangChain | 무료 |
| UI | Streamlit | 무료 |
| 배포 | Streamlit Cloud | 무료 |

---

## 프로젝트 구조

```
ai_agent_portfolio/
├── agent.py          # Agent 핵심 로직 (ReAct 구현)
├── app.py            # Streamlit 웹 UI
├── requirements.txt  # 의존성
├── .gitignore
└── README.md
```

### `agent.py` 핵심 흐름

```python
# 1. LLM 설정 (Groq - 무료, 빠름)
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 2. 도구 연결 (DuckDuckGo - API 키 불필요)
tools = [DuckDuckGoSearchRun()]

# 3. ReAct Agent 생성 (LangChain이 루프 자동 관리)
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
```

---

## 로컬 실행

```bash
# 1. 클론
git clone https://github.com/your-username/ai-search-agent
cd ai-search-agent

# 2. 설치
pip install -r requirements.txt

# 3. 실행
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속 후
[Groq 무료 API 키](https://console.groq.com) 입력하면 바로 사용 가능합니다.

---

## Streamlit Cloud 배포 방법

1. 이 레포를 GitHub에 Push
2. [share.streamlit.io](https://share.streamlit.io) 접속
3. GitHub 레포 연결
4. `app.py` 선택 후 Deploy

끝! 자동으로 `https://your-app.streamlit.app` 링크 생성됩니다.

---

## 배운 것 & 다음 단계

**구현 완료**
- [x] ReAct 패턴 이해 및 구현
- [x] Tool Calling (LLM이 검색 도구를 스스로 선택)
- [x] 멀티턴 대화 기록 유지
- [x] Streamlit Cloud 배포

**다음 확장 계획**
- [ ] RAG 추가 — 내 문서 기반으로 답변
- [ ] 멀티 Agent — Agent가 Agent를 지휘
- [ ] 메모리 추가 — 장기 대화 기억

---

## Why 5번으로 이해한 AI Agent

1. **왜 Agent가 필요해?** → LLM은 실시간 정보를 모름
2. **왜 Tool이 필요해?** → LLM 혼자는 외부 세계에 접근 불가
3. **왜 루프가 필요해?** → 한 번 검색으로 부족할 수 있음
4. **왜 LangChain을 써?** → 복잡한 루프 구조를 추상화해줌
5. **왜 Groq를 써?** → OpenAI 대비 무료이고 속도가 빠름

---

*AI Agent 개발자 과정 선행 학습 프로젝트*

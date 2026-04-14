"""
AI Search Agent - Streamlit 웹 앱
포트폴리오용 | Groq(무료) + DuckDuckGo(무료)
"""

import streamlit as st
from agent import create_agent, run_agent

# ── 페이지 설정 ────────────────────────────────────────────
st.set_page_config(
    page_title="AI Search Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── 커스텀 CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    /* 전체 폰트 */
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

    /* 채팅 메시지 스타일 */
    .stChatMessage { border-radius: 12px; }

    /* 검색 뱃지 */
    .search-badge {
        display: inline-block;
        background: #e8f4fd;
        color: #1a6fa8;
        font-size: 12px;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 6px;
        border: 1px solid #c5dff0;
    }

    /* API 키 입력창 안내 박스 */
    .key-guide {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 14px 16px;
        font-size: 13px;
        line-height: 1.6;
        color: #495057;
        margin-bottom: 8px;
    }
    .key-guide a { color: #1a6fa8; }

    /* 하단 크레딧 */
    .footer {
        text-align: center;
        font-size: 12px;
        color: #adb5bd;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ── 세션 초기화 ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "groq_key" not in st.session_state:
    st.session_state.groq_key = ""


# ── 사이드바 ───────────────────────────────────────────────
with st.sidebar:
    st.title("🤖 AI Search Agent")
    st.caption("웹 검색으로 최신 정보를 찾아 답하는 AI")

    st.divider()

    # API 키 입력
    st.markdown("**Groq API 키 입력**")
    st.markdown("""
    <div class="key-guide">
        1. <a href="https://console.groq.com" target="_blank">console.groq.com</a> 접속<br>
        2. 구글 계정으로 무료 가입<br>
        3. API Keys → Create API Key<br>
        4. 아래에 붙여넣기
    </div>
    """, unsafe_allow_html=True)

    api_key = st.text_input(
        label="API Key",
        type="password",
        placeholder="gsk_...",
        label_visibility="collapsed",
    )

    if api_key and api_key != st.session_state.groq_key:
        with st.spinner("연결 중..."):
            try:
                st.session_state.agent = create_agent(api_key)
                st.session_state.groq_key = api_key
                st.success("연결됐어요!")
            except Exception as e:
                st.error(f"키 오류: {str(e)[:80]}")
                st.session_state.agent = None

    st.divider()

    # 대화 초기화
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # 기술 스택
    st.markdown("**기술 스택**")
    st.markdown("""
    - 🧠 **LLM**: Llama 3.3 70B (Groq)
    - 🔍 **검색**: DuckDuckGo
    - ⚙️ **프레임워크**: LangChain
    - 🔄 **패턴**: ReAct
    - 🖥️ **UI**: Streamlit
    """)

    st.divider()
    st.markdown("""
    <div class="footer">
        Made with LangChain + Groq<br>
        포트폴리오 프로젝트
    </div>
    """, unsafe_allow_html=True)


# ── 메인 화면 ──────────────────────────────────────────────
st.title("AI Search Agent")
st.caption("ReAct 패턴으로 스스로 검색하고 답하는 AI Agent")

# Agent 미연결 상태 안내
if not st.session_state.agent:
    st.info("← 왼쪽 사이드바에서 Groq API 키를 입력하면 시작할 수 있어요. (무료)", icon="👈")

    # 예시 질문 카드
    st.markdown("**이런 걸 물어볼 수 있어요**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 오늘 주요 뉴스 알려줘
        - 최근 AI 트렌드가 뭐야?
        - 파이썬 최신 버전이 뭐야?
        """)
    with col2:
        st.markdown("""
        - RAG가 뭐야?
        - LangGraph 어떻게 써?
        - 요즘 핫한 기술 스택은?
        """)

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("searched"):
            st.markdown(
                f'<span class="search-badge">🔍 웹 검색 사용: {msg.get("search_query", "")}</span>',
                unsafe_allow_html=True
            )
        st.write(msg["content"])

# 빠른 질문 버튼 (대화 없을 때만)
if not st.session_state.messages and st.session_state.agent:
    st.markdown("**빠른 질문**")
    cols = st.columns(3)
    quick_questions = [
        "오늘 AI 뉴스 알려줘",
        "RAG가 뭐야?",
        "LangGraph vs LangChain",
    ]
    for i, q in enumerate(quick_questions):
        if cols[i].button(q, use_container_width=True):
            st.session_state.quick_q = q
            st.rerun()

# 빠른 질문 처리
quick_q = st.session_state.pop("quick_q", None)

# 사용자 입력
user_input = st.chat_input(
    "무엇이든 물어보세요...",
    disabled=not st.session_state.agent
) or quick_q

if user_input and st.session_state.agent:
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Agent 실행
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            result = run_agent(
                st.session_state.agent,
                user_input,
                st.session_state.messages[:-1],
            )

        if result["searched"]:
            st.markdown(
                f'<span class="search-badge">🔍 웹 검색 사용: {result["search_query"]}</span>',
                unsafe_allow_html=True
            )
        st.write(result["answer"])

    # 대화 기록 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "searched": result["searched"],
        "search_query": result.get("search_query"),
    })

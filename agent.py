"""
AI Search Agent - 핵심 로직
- LLM: Groq (llama-3.3-70b) - 무료
- 검색: DuckDuckGo - API 키 없이 무료
- 패턴: ReAct (Observe → Think → Act 루프)
"""

from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage


SYSTEM_PROMPT = """당신은 친절하고 똑똑한 AI Search Agent입니다.
사용자의 질문을 분석하고, 필요하면 웹 검색 도구를 사용해 최신 정보를 찾아 답합니다.

사용 가능한 도구:
{tools}

도구 이름 목록: {tool_names}

동작 방식 (반드시 아래 형식을 따르세요):

질문: 사용자의 입력
생각: 이 질문에 답하기 위해 무엇이 필요한지 생각합니다
행동: 사용할 도구 이름 (도구가 필요 없으면 생략)
행동 입력: 도구에 넣을 검색어
관찰: 도구 실행 결과
... (필요하면 반복)
생각: 이제 최종 답변을 알겠습니다
최종 답변: 사용자에게 전달할 친절하고 명확한 한국어 답변

이전 대화:
{chat_history}

질문: {input}
생각: {agent_scratchpad}"""


def create_agent(groq_api_key: str) -> AgentExecutor:
    """
    Groq API 키로 Agent 생성

    Args:
        groq_api_key: Groq API 키 (console.groq.com에서 무료 발급)

    Returns:
        LangChain AgentExecutor
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=groq_api_key,
        temperature=0.3,
        max_tokens=2048,
    )

    tools = [DuckDuckGoSearchRun(name="web_search")]

    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

    agent = create_react_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        max_iterations=5,          # 최대 5번 루프
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )


def format_history(messages: list) -> str:
    """대화 기록을 문자열로 변환"""
    if not messages:
        return "없음"
    result = []
    for msg in messages:
        role = "사용자" if msg["role"] == "user" else "AI"
        result.append(f"{role}: {msg['content']}")
    return "\n".join(result)


def run_agent(agent_executor: AgentExecutor, user_input: str, history: list) -> dict:
    """
    Agent 실행

    Args:
        agent_executor: create_agent()로 생성한 executor
        user_input: 사용자 질문
        history: 이전 대화 기록 [{"role": "user"/"assistant", "content": "..."}]

    Returns:
        {
            "answer": "최종 답변",
            "searched": True/False,  # 웹 검색 사용 여부
            "search_query": "검색어" or None
        }
    """
    result = agent_executor.invoke({
        "input": user_input,
        "chat_history": format_history(history),
    })

    # 중간 단계에서 검색 사용 여부 확인
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

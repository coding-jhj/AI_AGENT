"""
AI Search Agent - 핵심 로직
- LLM: Groq (llama-3.3-70b) - 무료
- 검색: DuckDuckGo - API 키 없이 무료
- 패턴: ReAct (Observe → Think → Act 루프)
"""

from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage


SYSTEM_PROMPT = """You are a helpful AI Search Agent. You MUST answer in Korean only (한국어만 사용). Never use Chinese or Japanese characters.
Analyze the user's question and use web search when needed to find up-to-date information.

You have access to the following tools:
{tools}

Tool names: {tool_names}

Use the following format STRICTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat up to 5 times)
Thought: I now know the final answer
Final Answer: MUST be written in Korean only. No Chinese or Japanese characters allowed. Use Korean exclusively.

Previous conversation:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}"""


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
        max_tokens=1024,
    )

    tools = [DuckDuckGoSearchRun(name="web_search")]

    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

    agent = create_react_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
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
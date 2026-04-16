"""
AI Search Agent - 핵심 로직
- LLM: Google Gemini (langchain-google-genai)
- 검색: DuckDuckGo - API 키 없이 무료
- 패턴: ReAct (Observe → Think → Act 루프)
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate


SYSTEM_PROMPT = """You are a highly capable AI Search Agent. You MUST answer in Korean only (한국어만 사용).

CRITICAL RULES:
1. For greetings, simple questions about yourself, math, or general knowledge → answer IMMEDIATELY with "Final Answer" without searching.
2. ONLY use web_search for: current news, recent events, real-time data, specific facts you are uncertain about.
3. Search at most ONCE per question. Never repeat searches.
4. Keep answers concise but complete. For complex topics, give thorough explanations.
5. NEVER use Chinese or Japanese characters.

You have access to the following tools:
{tools}

Tool names: {tool_names}

Use this format:

Question: the input question
Thought: Do I need to search? Simple/general knowledge → go straight to Final Answer. Current info needed → search once.
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer
Final Answer: 반드시 한국어로만 작성. 명확하고 유용한 답변.

Previous conversation:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}"""


def create_agent(google_api_key: str, model: str = "gemini-2.0-flash") -> AgentExecutor:
    """
    Gemini API 키로 Agent 생성

    Args:
        google_api_key: Google AI Studio API 키 (aistudio.google.com에서 무료 발급)
        model: 사용할 모델명

    Returns:
        LangChain AgentExecutor
    """
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=google_api_key,
        temperature=0.3,
        max_output_tokens=2048,
    )

    tools = [DuckDuckGoSearchRun(
        name="web_search",
        description="Search the web for current events, news, real-time data, or specific facts. Use ONLY when necessary."
    )]

    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

    agent = create_react_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=3,
        max_execution_time=30,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )


def format_history(messages: list) -> str:
    if not messages:
        return "없음"
    recent = messages[-6:]  # 최근 6턴만 유지 (토큰 절약)
    result = []
    for msg in recent:
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
            "searched": True/False,
            "search_query": "검색어" or None
        }
    """
    result = agent_executor.invoke({
        "input": user_input,
        "chat_history": format_history(history),
    })

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
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from src.tools.search_tools import search_web, search_news
from src.utils.config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, GOOGLE_API_KEY


def create_search_agent():
    """
    Create a search agent specialized for web information retrieval.

    Returns:
        A LangGraph agent that can search the web for information.
    """
    # Create the model
    model = ChatGoogleGenerativeAI(
        model=DEFAULT_MODEL,
        temperature=DEFAULT_TEMPERATURE,
        google_api_key=GOOGLE_API_KEY,
    )

    # Define search tools
    search_tools = [search_web, search_news]

    # Create the agent with ReAct framework
    search_agent = create_react_agent(
        model=model,
        tools=search_tools,
        name="search_expert",
        prompt=(
            "You are a web search expert with access to real-time internet information. "
            "You have access to tools that allow you to search the web for information and recent news. "
            "When asked about current events, trends, or any information that might require up-to-date "
            "knowledge, always use the appropriate search tool to find reliable information. "
            "For general information use search_web, and for recent events use search_news. "
            "Never make up information - if you don't know or can't find the answer, say so. "
            "Present information in a clear, concise manner, citing sources when appropriate."
        ),
    )

    return search_agent

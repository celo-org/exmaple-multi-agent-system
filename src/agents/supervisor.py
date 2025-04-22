from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver

from src.agents.blockchain_agent import create_blockchain_agent
from src.agents.search_agent import create_search_agent
from src.utils.config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, GOOGLE_API_KEY


def create_multi_agent_system():
    """
    Create a multi-agent system with a supervisor that orchestrates specialized agents.

    Returns:
        A compiled LangGraph multi-agent system
    """
    # Create the model for the supervisor
    model = ChatGoogleGenerativeAI(
        model=DEFAULT_MODEL,
        temperature=DEFAULT_TEMPERATURE,
        google_api_key=GOOGLE_API_KEY,
    )

    # Create specialized agents
    blockchain_agent = create_blockchain_agent()
    search_agent = create_search_agent()

    # Create a supervisor to orchestrate the agents
    workflow = create_supervisor(
        agents=[blockchain_agent, search_agent],
        model=model,
        output_mode="full_history",  # Include full agent conversation history
        supervisor_name="main_supervisor",
        prompt=(
            "You are a helpful assistant that coordinates between a blockchain expert and a search expert. "
            "Use the blockchain_expert for questions about the Celo blockchain, including fetching the latest "
            "block number, block information, or general blockchain statistics. "
            "Use the search_expert for questions that require searching the web for information or recent news. "
            "Carefully analyze each user query to determine which agent(s) to invoke. "
            "For queries that might benefit from both agents, you can use them in sequence. "
            "Always prioritize providing accurate and helpful information to the user."
        ),
    )

    # Create in-memory checkpointer for conversation history
    checkpointer = InMemorySaver()

    # Compile the workflow with the checkpointer
    return workflow.compile(checkpointer=checkpointer)

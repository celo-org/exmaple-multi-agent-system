from typing import List, Dict, Any, Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage

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


def invoke_multi_agent_system(
    agent_system,
    messages: List[Union[Dict[str, Any], BaseMessage]],
    thread_id: str = "default",
):
    """
    Invoke the multi-agent system with the specified thread_id.

    Args:
        agent_system: The compiled LangGraph multi-agent system
        messages: List of messages in the conversation (LangChain message objects)
        thread_id: The thread identifier for this conversation

    Returns:
        The result from the multi-agent system
    """
    # Create configuration with thread_id
    config = {"configurable": {"thread_id": thread_id}}

    # Invoke the system with the proper configuration
    return agent_system.invoke({"messages": messages}, config)

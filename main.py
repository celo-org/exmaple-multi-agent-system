import sys
import json
import uuid
from typing import Dict, Any, List, Union

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage

from src.agents.supervisor import create_multi_agent_system, invoke_multi_agent_system
from src.utils.config import validate_config


def format_message(message: Union[Dict[str, Any], BaseMessage]) -> str:
    """Format a message for display."""
    # Handle LangChain message objects
    if isinstance(message, BaseMessage):
        if isinstance(message, HumanMessage):
            return f"\n\033[1m> User:\033[0m {message.content}"
        elif isinstance(message, AIMessage):
            return f"\n\033[1;32m> Assistant:\033[0m {message.content}"
        elif isinstance(message, SystemMessage):
            return f"\n\033[1;33m> System:\033[0m {message.content}"
        else:
            return f"\n> {message.__class__.__name__}: {message.content}"

    # Handle dictionary-format messages
    role = message.get("role", "")
    content = message.get("content", "")

    if role == "user":
        return f"\n\033[1m> User:\033[0m {content}"
    elif role == "assistant":
        return f"\n\033[1;32m> Assistant:\033[0m {content}"
    elif role == "tool" and content:
        return f"\n\033[1;34m> Tool Output:\033[0m {content}"
    elif role == "system":
        return f"\n\033[1;33m> System:\033[0m {content}"
    else:
        return f"\n> {role}: {content}"


def dict_to_langchain_message(message: Dict[str, Any]) -> BaseMessage:
    """Convert a dictionary message to a LangChain message object."""
    role = message.get("role", "").lower()
    content = message.get("content", "")

    if role == "user":
        return HumanMessage(content=content)
    elif role == "assistant":
        return AIMessage(content=content)
    elif role == "system":
        return SystemMessage(content=content)
    else:
        # Default to HumanMessage for unknown roles
        return HumanMessage(content=content)


def main():
    """Main application entry point."""
    print(
        "\n\033[1;36m=== Multi-Agent System with Celo Blockchain and Web Search ===\033[0m"
    )

    # Validate configuration
    if not validate_config():
        sys.exit(1)

    # Create multi-agent system
    print("\n\033[1;33m> System:\033[0m Initializing multi-agent system...")
    multi_agent_system = create_multi_agent_system()
    print("\033[1;33m> System:\033[0m Multi-agent system initialized!")

    # Generate a unique thread ID for this conversation
    thread_id = str(uuid.uuid4())
    print(f"\033[1;33m> System:\033[0m Created conversation thread: {thread_id}")

    # Initial conversation state
    state = {"messages": []}

    # Main interaction loop
    try:
        while True:
            # Get user input
            user_input = input(
                "\n\033[1m> Enter your question (or 'exit' to quit):\033[0m "
            )

            if user_input.lower() in ("exit", "quit", "q"):
                print("\n\033[1;33m> System:\033[0m Goodbye!")
                break

            # Add user message to conversation as LangChain message object
            user_message = HumanMessage(content=user_input)
            messages = state["messages"] + [user_message]

            # Invoke multi-agent system with thread_id
            print("\033[1;33m> System:\033[0m Processing your request...")
            result = invoke_multi_agent_system(multi_agent_system, messages, thread_id)

            # Update state
            state = result

            # Display conversation
            for message in state["messages"]:
                if isinstance(message, HumanMessage) and message.content == user_input:
                    # We already displayed the user message when getting input
                    continue
                print(format_message(message))

    except KeyboardInterrupt:
        print("\n\033[1;33m> System:\033[0m Interrupted. Exiting...")
    except Exception as e:
        print(f"\n\033[1;31m> Error:\033[0m {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

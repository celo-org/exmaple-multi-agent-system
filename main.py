import sys
import json
from typing import Dict, Any, List

from src.agents.supervisor import create_multi_agent_system
from src.utils.config import validate_config


def format_message(message: Dict[str, Any]) -> str:
    """Format a message for display."""
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

            # Add user message to conversation
            user_message = {"role": "user", "content": user_input}
            messages = state["messages"] + [user_message]

            # Invoke multi-agent system
            print("\033[1;33m> System:\033[0m Processing your request...")
            result = multi_agent_system.invoke({"messages": messages})

            # Update state
            state = result

            # Display conversation
            for message in state["messages"]:
                if (
                    message == user_message
                ):  # We already displayed the user message when getting input
                    continue
                print(format_message(message))

    except KeyboardInterrupt:
        print("\n\033[1;33m> System:\033[0m Interrupted. Exiting...")
    except Exception as e:
        print(f"\n\033[1;31m> Error:\033[0m {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

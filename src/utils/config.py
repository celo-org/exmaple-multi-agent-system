import os
from typing import Optional

# LLM configurations
DEFAULT_MODEL = "gemini-2.5-flash-preview-04-17"
DEFAULT_TEMPERATURE = 0.0

# API keys
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

# Blockchain configurations
CELO_RPC_URL = os.environ.get("CELO_RPC_URL", "https://forno.celo.org")
CELO_CHAIN_ID = 42220  # Celo Mainnet


def validate_config() -> bool:
    """Validate that all required configuration variables are set."""
    missing_vars = []

    if not GOOGLE_API_KEY:
        missing_vars.append("GOOGLE_API_KEY")

    if not TAVILY_API_KEY:
        missing_vars.append("TAVILY_API_KEY")

    if missing_vars:
        print(
            f"Error: Missing required environment variables: {', '.join(missing_vars)}"
        )
        print("Please set these variables before running the application.")
        return False

    return True

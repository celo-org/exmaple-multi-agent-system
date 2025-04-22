# Multi-Agent System

A production-grade multi-agent system built with LangGraph and LangChain, featuring a web search agent and a Celo blockchain agent powered by Google's Gemini.

## Features

- 🤖 **Supervisor agent** that orchestrates specialized agents
- 🔍 **Web search agent** for retrieving real-time information
- ⛓️ **Blockchain agent** for fetching Celo blockchain data
- 📊 **Memory management** for conversation history
- 🤖 **Gemini AI** for intelligent agent capabilities
- 🧵 **Thread support** for maintaining conversation state

## Architecture

The system uses a hierarchical multi-agent architecture with a supervisor agent orchestrating specialized agents.

```mermaid
graph TB
    User([User]) <--> Main[Main Application]
    Main -- Messages --> Supervisor[Supervisor Agent<br>Google Gemini]
    Supervisor -- Blockchain queries --> BlockchainAgent[Blockchain Agent<br>Celo Expert]
    Supervisor -- Web search queries --> SearchAgent[Search Agent<br>Web Expert]

    BlockchainAgent -- Fetches data --> CeloTools[Celo Blockchain Tools]
    SearchAgent -- Retrieves information --> WebTools[Web Search Tools]

    subgraph Blockchain Tools
    CeloTools --> BlockNumber[get_latest_block_number]
    CeloTools --> BlockInfo[get_block_info]
    CeloTools --> CeloStats[get_celo_stats]
    end

    subgraph Web Tools
    WebTools --> SearchWeb[search_web]
    WebTools --> SearchNews[search_news]
    end

    subgraph Memory Management
    Checkpointer[InMemorySaver] -- Maintains state --> ThreadID[Thread ID]
    end

    Main -- Conversation state --> Checkpointer

    style Supervisor fill:#f9d77e,stroke:#f9bc02
    style BlockchainAgent fill:#a4c2f4,stroke:#1155cc
    style SearchAgent fill:#b6d7a8,stroke:#38761d
    style Main fill:#d5a6bd,stroke:#a64d79
    style Checkpointer fill:#ead1dc,stroke:#a64d79
    style User fill:#f9cb9c,stroke:#e69138
```

## Setup

1. Clone the repository
2. Install dependencies:

```bash
pip install -e ".[dev]"
```

3. Set up environment variables:

```bash
export GOOGLE_API_KEY=your_google_api_key
export TAVILY_API_KEY=your_tavily_api_key
```

You can also create a `.env` file in the project root (the application uses python-dotenv to load variables automatically).

## Usage

Run the main application:

```bash
python main.py
```

The application maintains conversation state using thread IDs, allowing for coherent multi-turn interactions.

## Project Structure

```
multi-agent-system/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── blockchain_agent.py  # Agent for Celo blockchain interactions
│   │   ├── search_agent.py      # Agent for web search capabilities
│   │   └── supervisor.py        # Orchestrates specialized agents
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── blockchain_tools.py  # Tools for interacting with Celo blockchain
│   │   └── search_tools.py      # Tools for web search using Tavily
│   └── utils/
│       ├── __init__.py
│       └── config.py            # Configuration and environment variables
├── main.py                      # Application entry point
├── pyproject.toml               # Dependencies and project metadata
└── README.md
```

## How It Works

1. The **Supervisor Agent** analyzes user queries and determines which specialized agent to use
2. For blockchain-related queries, the **Blockchain Agent** fetches real-time data from the Celo blockchain
3. For information retrieval, the **Search Agent** uses Tavily to search the web for relevant information
4. All conversation state is maintained using **thread IDs** for coherent multi-turn interactions
5. The system uses Google's **Gemini** models for intelligent natural language understanding and generation

## License

MIT

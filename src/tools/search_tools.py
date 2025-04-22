from typing import Dict, Any, List
from langchain_core.tools import tool
from tavily import TavilyClient

from src.utils.config import TAVILY_API_KEY

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web for information using Tavily.

    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 5)

    Returns:
        str: Search results with relevant information
    """
    search_results = tavily_client.search(
        query=query, search_depth="advanced", max_results=max_results
    )

    # Format the results into a readable string
    formatted_results = f"Search Results for: {query}\n\n"

    for i, result in enumerate(search_results.get("results", []), 1):
        formatted_results += f"{i}. {result.get('title', 'No Title')}\n"
        formatted_results += f"   URL: {result.get('url', 'No URL')}\n"
        formatted_results += (
            f"   {result.get('content', 'No content available')[:300]}...\n\n"
        )

    return formatted_results


@tool
def search_news(query: str, max_results: int = 5, days_back: int = 7) -> str:
    """
    Search for recent news using Tavily.

    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 5)
        days_back: How many days back to search for news (default: 7)

    Returns:
        str: Recent news results related to the query
    """
    search_results = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        topic="news",
        days=days_back,
    )

    # Format the results into a readable string
    formatted_results = f"Recent News Results for: {query}\n\n"

    for i, result in enumerate(search_results.get("results", []), 1):
        formatted_results += f"{i}. {result.get('title', 'No Title')}\n"
        formatted_results += (
            f"   Published: {result.get('published_date', 'Unknown date')}\n"
        )
        formatted_results += f"   URL: {result.get('url', 'No URL')}\n"
        formatted_results += (
            f"   {result.get('content', 'No content available')[:300]}...\n\n"
        )

    return formatted_results

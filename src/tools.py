from langchain.tools import tool
from ddgs import DDGS

@tool
def search_web(query, max_results = 4) -> list:
    """Search the web for the given query and return a list of results."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results = max_results)]
        return results
from langchain_tavily import TavilySearch



def get_search_tools():
    search_tools = TavilySearch(max_results=2)
    return search_tools

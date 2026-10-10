from tavily import TavilyClient
from app.config import TAVILY_API_KEY
from app.agents.state import ResearchState


def web_search_node(state:ResearchState):
    query=state["query"]

    if not TAVILY_API_KEY:
        return "Runtime error with message mentioning"
    client=TavilyClient(api_key=TAVILY_API_KEY)
    search_respone=client.search(query=query,max_results=3,search_depth="basic")
    results=search_respone.get("results",[])
    sources=[]
    for result in results:
        source={
            "title":result.get("title","untitled source"),
            "url":result.get("url", ""),
            "snippet":result.get("content", "")
            }
        sources.append(source)
    return {"sources": sources}

from app.agents.state import ResearchState
def report_writer_node(state:ResearchState):
    company=state["company"]
    focus=state["focus"]
    competitors=state["competitors"]
    query=state["query"]
    sources=state["sources"]
    source_count=len(sources)
    if competitors:
        competitor_text=",".join(competitors)
        summary=f"Mock competitive research for {company} focuses on {focus}. It compares {company} with {competitor_text}. The workflow generated the query {query} and collected {source_count} web sources"
    else:
        summary=f"Mock market research for {company} focuses on {focus}. No direct competitors were supplied. The workflow generated the query {query} and collected {source_count}  web sources."
    return {"summary" : summary}



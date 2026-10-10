from app.agents.state import ResearchState
def planner_node (state:ResearchState):
    company = state["company"]
    focus = state["focus"]
    competitors = state["competitors"]
    if competitors:
        compet=", ".join(competitors)
        query=f"{company} the focus of {focus}  comparison with {compet}"
        return {"query": query}
    else:
        query=f"the compant {company}   {focus} by market analysis query"
        return {"query": query} 

    
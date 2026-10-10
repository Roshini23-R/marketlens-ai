from app.schemas.research import ResearchRequest,ResearchSource,ResearchResponse
from datetime import datetime, UTC
from app.agents.graph import research_graph
from uuid import uuid4
# def build_summary(payload:ResearchRequest) -> str:
#     if payload.competitors:
#         competitor_name=", ".join(payload.competitors)
#         summary= f"the company name {payload.company} the focusing area of interest to compare {payload.focus} and the other comprttord{competitor_name}"
#         return summary
#     else:
#        summary= f"the company name {payload.company} the focusing area of interest to compare{payload.focus} and the overall review about the opponent product "
#        return summary

# def build_dummy_source() ->ResearchSource:
#     sources=ResearchSource(
#         title='amazon',
#         url="https://www.amazon.in/",
#         snippet=" temporary sources data until web search is connected"
#     )
#     return sources

def run_research(payload:ResearchRequest) -> ResearchResponse:
    initial_state = {
    "company": payload.company,
    "focus": payload.focus,
    "competitors": payload.competitors,
    "query": "",
    "sources": [],
    "summary": "",
    "report":{}}
    
    
    response_sources = []
    
    final_state = research_graph.invoke(initial_state)
    for source_dict in final_state["sources"]:
        new_source=ResearchSource(
            title   = source_dict["title"],
            url     = source_dict["url"],
            snippet = source_dict["snippet"],
        )
        response_sources.append(new_source)
    response = ResearchResponse(
        run_id     = f"run-{uuid4()}" ,
        sources    = response_sources,
        status     = "completed",
        summary    = final_state["summary"],
        company    = payload.company,
        focus      = payload.focus,
        created_at = datetime.now(UTC)
    )
    return response
    







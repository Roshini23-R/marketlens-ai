from app.agents.state import ResearchState
def mock_search(state:ResearchState):
    company=state['company']
    query=state['query']
    text=company.lower()
    safe_company = text.replace(' ', '-')
    official_source={
"title":f"{company} official product information",
"url":f"https://example.com/{safe_company}/competitive-analysis",
"snippet": f"Mock sources generated for query: {query}"
}
    competitive_source={"title":f"{company} competitive landscape",
                        "url":f"https://example.com/{safe_company}",
                        "snippet":f"Temporary mock competitive information for {company}"}
    sources = [official_source, competitive_source]
    return{"sources" : sources}


    


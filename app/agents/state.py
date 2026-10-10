from typing import TypedDict
class ResearchSourceState(TypedDict):
    title: str
    url: str
    snippet: str
class ResearchState(TypedDict):
    company:str
    focus:str
    competitors:list[str]
    query:str
    sources:list[ResearchSourceState]
    summary:str
    report:dict

from typing import Literal
from pydantic import BaseModel,Field
from datetime import datetime
class ResearchRequest(BaseModel):

    company:str = Field(min_length=2,max_length=120,description= "give the company name that you need to research",examples=["amazon"])

    focus : str =Field(min_length=3,max_length=350,description= "give the features that you want to compare based on that ",examples=["pricing,product uniqueness"] )

    competitors:list[str]  = Field(default_factory=list,
        max_items=5,
        description="Optional list of direct competitors to compare",
        examples=[["Confluence", "Coda"]],
    )


class ResearchSource(BaseModel):
    title:str
    url:str
    snippet:str

class ResearchResponse(BaseModel):
    run_id:str 
    sources:list[ResearchSource] = Field(default_factory=list)
    status:Literal["queued","running","completed","failed"]
    summary:str =Field(description="Short summary of research findings")
    company: str
    focus: str
    created_at:datetime
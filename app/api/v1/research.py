from app.schemas.research import ResearchRequest,ResearchResponse
from app.services.research_service import run_research
from fastapi import APIRouter
router = APIRouter()
@router.post("/",response_model=ResearchResponse)
def start_research(payload:ResearchRequest):
    return run_research(payload)



from fastapi import APIRouter
from app.api.v1.research import router

api_router = APIRouter()

api_router.include_router(router, prefix="/research", tags=["research"])
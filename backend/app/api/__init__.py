from fastapi import APIRouter
from app.api.routes import companies, documents, assessments, health

api_router = APIRouter()

api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(health.router, prefix="/health", tags=["health"])

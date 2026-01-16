"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, projects, documents, assets, threats, reports

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(documents.router)
api_router.include_router(assets.router)
api_router.include_router(threats.router)
api_router.include_router(reports.router)

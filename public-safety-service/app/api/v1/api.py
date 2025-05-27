"""
API v1 router configuration
"""
from fastapi import APIRouter

from app.api.v1.endpoints.fire import router as fire_router

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(fire_router)

# Health check endpoint
@api_router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Swakopmund Municipality Public Safety Service",
        "version": "1.0.0"
    } 
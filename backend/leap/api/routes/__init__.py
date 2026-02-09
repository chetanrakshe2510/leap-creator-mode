"""
API routes package.
"""
from fastapi import APIRouter
from . import animations, feedback, system

# Create a combined router
router = APIRouter()
router.include_router(animations.router, prefix="/api/animations", tags=["animations"])
router.include_router(feedback.router, prefix="/api", tags=["feedback"])
router.include_router(system.router, prefix="/api/system", tags=["system"])

__all__ = ["animations", "feedback", "system", "router"]

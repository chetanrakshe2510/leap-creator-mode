"""
System health and status routes.
"""
from fastapi import APIRouter
from ..models.responses import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of the API."""
    return HealthResponse(
        status="ok",
        version="0.1.0"
    )

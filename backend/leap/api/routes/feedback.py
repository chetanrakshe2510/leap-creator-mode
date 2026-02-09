"""
Feedback routes.
"""
from fastapi import APIRouter, HTTPException
from uuid import UUID

from ..models.requests import FeedbackRequest
from ..models.responses import FeedbackResponse
from ..services.feedback import FeedbackService

router = APIRouter()
feedback_service = FeedbackService()

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for an animation."""
    try:
        result = await feedback_service.submit_feedback(request)
        return FeedbackResponse(
            success=True,
            message="Feedback received. Thank you!"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

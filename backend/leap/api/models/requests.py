"""
Request models for the API.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional

class AnimationRequest(BaseModel):
    """Request model for animation generation."""
    prompt: str
    level: str
    email: Optional[EmailStr] = None

class FeedbackRequest(BaseModel):
    """Request model for feedback submission."""
    job_id: str
    rating: int
    comment: Optional[str] = None

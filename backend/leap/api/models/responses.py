"""
Response models for the API.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnimationResponse(BaseModel):
    """Response model for animation generation."""
    job_id: str
    status: str
    created_at: datetime

class StatusResponse(BaseModel):
    """Response model for job status."""
    job_id: str
    status: str
    video_url: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    success: bool
    message: str

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str

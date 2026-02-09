"""
Animation service for handling animation generation.
"""
import uuid
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass
from pathlib import Path
import os
import logging

from ...workflow import workflow
from ...workflow.state import GraphState
from ..models.requests import AnimationRequest
from ..models.responses import StatusResponse
from ...services.supabase_service import SupabaseService
from ...services.email_service import EmailService
from ...services.storage_service import StorageService

logger = logging.getLogger(__name__)

@dataclass
class Job:
    """Represents an animation job."""
    id: uuid.UUID
    created_at: datetime
    status: str = "pending"
    video_url: Optional[str] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

class AnimationService:
    """Service for handling animation generation."""
    
    def __init__(self):
        self.jobs: Dict[uuid.UUID, Job] = {}
        self.supabase = SupabaseService()
        self.email_service = EmailService()
        self.storage_service = StorageService()
    
    async def create_job(self, request: AnimationRequest) -> Dict:
        """Create a new animation job and return response data."""
        # Create job in Supabase
        job_id_str = self.supabase.create_animation_job(
            prompt=request.prompt,
            level=request.level,
            email=request.email
        )
        
        job_id = uuid.UUID(job_id_str)
        job = Job(
            id=job_id,
            created_at=datetime.utcnow(),
            status="pending"
        )
        self.jobs[job_id] = job
        
        # Return data in the format expected by AnimationResponse
        return {
            "job_id": str(job_id),
            "status": job.status,
            "created_at": job.created_at
        }
    
    async def get_status(self, job_id: uuid.UUID) -> StatusResponse:
        """Get the status of a job."""
        job = self.jobs.get(job_id)
        if not job:
            # Try to get from Supabase
            supabase_job = self.supabase.get_job(str(job_id))
            if not supabase_job:
                raise ValueError(f"Job {job_id} not found")
                
            # Create job object from Supabase data
            job = Job(
                id=job_id,
                created_at=datetime.fromisoformat(supabase_job["created_at"].replace("Z", "+00:00")),
                status=supabase_job["status"],
                video_url=supabase_job.get("video_url"),
                completed_at=datetime.fromisoformat(supabase_job["completed_at"].replace("Z", "+00:00")) if supabase_job.get("completed_at") else None,
                error=supabase_job.get("error")
            )
            self.jobs[job_id] = job
            
        return StatusResponse(
            job_id=str(job.id),
            status=job.status,
            video_url=job.video_url,
            created_at=job.created_at,
            completed_at=job.completed_at,
            error=job.error
        )
    
    async def process_job(
        self,
        job_id: uuid.UUID,
        prompt: str,
        level: str,
        email: Optional[str] = None
    ):
        """Process an animation job."""
        job = self.jobs.get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
            
        try:
            # Create a simple test state
            state = GraphState(
                user_input=prompt,
                rendering_quality="low",
                duration_detail="brief",
                user_level=level,
                voice_model="nova"
            )
            
            logger.info("Starting workflow execution...")
            logger.info(f"State: {state}")
            
            # Execute workflow
            result = workflow.invoke(state)
            logger.info(f"Workflow result: {result}")
            
            if result.get("error"):
                job.status = "failed"
                job.error = result["error"]
                logger.error(f"Job failed: {result['error']}")
                
                # Update Supabase
                self.supabase.update_job_status(
                    str(job_id),
                    "failed",
                    error=result["error"]
                )
            else:
                job.status = "completed"
                # Get the output file from the execution result
                execution_result = result.get("execution_result", {})
                local_video_path = execution_result.get("output_file")
                
                if local_video_path and Path(local_video_path).exists():
                    logger.info(f"Video file exists locally at: {local_video_path}")
                    
                    # Upload to storage and get public URL
                    try:
                        public_url = self.storage_service.get_file_url(local_video_path)
                        logger.info(f"Video file uploaded to storage: {public_url}")
                        job.video_url = public_url
                    except Exception as e:
                        logger.error(f"Error uploading video to storage: {str(e)}")
                        job.video_url = local_video_path  # Fallback to local path
                else:
                    logger.error(f"Warning: Video file not found at: {local_video_path}")
                    job.video_url = local_video_path  # Keep the path for debugging
                
                job.completed_at = datetime.utcnow()
                
                # Update Supabase
                self.supabase.update_job_status(
                    str(job_id),
                    "completed",
                    video_url=job.video_url
                )
                
                # Send email notification if email is provided
                if email and job.video_url:
                    self.email_service.send_animation_ready_notification(
                        email=email,
                        job_id=str(job_id),
                        video_url=job.video_url
                    )
                
        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            logger.error(f"Error processing job: {str(e)}", exc_info=True)
            
            # Update Supabase
            self.supabase.update_job_status(
                str(job_id),
                "failed",
                error=str(e)
            )

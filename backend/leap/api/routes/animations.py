"""
Animation generation routes.
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Response
from fastapi.responses import FileResponse
from typing import Optional
import logging
from uuid import UUID
from pathlib import Path
import os

from ..models.requests import AnimationRequest
from ..models.responses import AnimationResponse, StatusResponse
from ..services.animation import AnimationService
from ...services.storage_service import StorageService

router = APIRouter()
animation_service = AnimationService()
storage_service = StorageService()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=AnimationResponse)
async def generate_animation(
    request: AnimationRequest,
    background_tasks: BackgroundTasks
):
    """Generate an animation based on the provided prompt."""
    try:
        logger.info(f"Received animation request: prompt='{request.prompt}', level='{request.level}', email='{request.email}'")
        
        # Create job and get response data
        response_data = await animation_service.create_job(request)
        logger.info(f"Created job with ID: {response_data['job_id']}")
        
        # Add background task
        background_tasks.add_task(
            animation_service.process_job,
            job_id=UUID(response_data["job_id"]),
            prompt=request.prompt,
            level=request.level,
            email=request.email
        )
        logger.info(f"Added background task to process job: {response_data['job_id']}")
        
        return AnimationResponse(**response_data)
    except Exception as e:
        logger.error(f"Error generating animation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: UUID):
    """Get the status of an animation job."""
    try:
        logger.info(f"Checking status for job: {job_id}")
        status = await animation_service.get_status(job_id)
        logger.info(f"Job status: {status.status}, video_url: {status.video_url}")
        return status
    except ValueError as e:
        logger.error(f"Job not found: {job_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting job status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/animations/download/{job_id}")
async def download_animation(job_id: str):
    """Download an animation video file."""
    try:
        # Get the animation from the database
        animation = await animation_service.get_animation(job_id)
        
        if not animation:
            raise HTTPException(status_code=404, detail="Animation not found")
        
        if animation.status != "completed":
            raise HTTPException(status_code=400, detail="Animation is not ready for download")
        
        video_url = animation.video_url
        
        if not video_url:
            raise HTTPException(status_code=404, detail="Video file not found")
        
        # If it's a Supabase URL, we need to redirect to it
        if "supabase" in video_url:
            return {"download_url": video_url}
        
        # For local files, extract the path and serve the file
        # URL format is like: http://localhost:8000/videos/480p15/PendulumExplanationScene.mp4
        if "/videos/" in video_url:
            # Extract the relative path from the URL
            path_parts = video_url.split("/videos/")
            if len(path_parts) > 1:
                relative_path = path_parts[1]
                # Get the local storage path from the storage service
                local_storage_path = storage_service.local_storage_path
                file_path = Path(local_storage_path) / relative_path
                
                if file_path.exists():
                    # Get the filename for the Content-Disposition header
                    filename = file_path.name
                    return FileResponse(
                        path=str(file_path),
                        filename=filename,
                        media_type="video/mp4"
                    )
        
        # If we get here, we couldn't find the file
        raise HTTPException(status_code=404, detail="Video file not found")
    except Exception as e:
        logger.error(f"Error downloading animation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

import os
from typing import Dict, Any, Optional
import logging
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        # Skip initialization if credentials are missing or invalid (mock/placeholder values)
        if not url or not key or "your_supabase_url_here" in url or "your_supabase" in key:
            logger.warning("Supabase credentials not found or invalid. Using mock database.")
            self.supabase = None
        else:
            try:
                self.supabase: Client = create_client(url, key)
            except Exception as e:
                logger.warning(f"Failed to initialize Supabase client: {e}. Using mock database.")
                self.supabase = None
    
    def create_animation_job(self, prompt: str, level: str, email: Optional[str] = None) -> str:
        """Create a new animation job in Supabase."""
        if not self.supabase:
            # Mock implementation for local development
            import uuid
            return str(uuid.uuid4())
            
        data = {
            "prompt": prompt,
            "level": level,
            "email": email,
            "status": "pending"
        }
        
        try:
            result = self.supabase.table("animations").insert(data).execute()
            return result.data[0]["id"] if result.data else None
        except Exception as e:
            logger.error(f"Error creating animation job: {str(e)}")
            # Fallback to local UUID
            import uuid
            return str(uuid.uuid4())
    
    def update_job_status(self, job_id: str, status: str, video_url: Optional[str] = None, error: Optional[str] = None):
        """Update the status of an animation job."""
        if not self.supabase:
            # Mock implementation for local development
            return
            
        data = {"status": status}
        if video_url:
            data["video_url"] = video_url
        if error:
            data["error"] = error
        if status == "completed":
            data["completed_at"] = "now()"
        
        try:
            self.supabase.table("animations").update(data).eq("id", job_id).execute()
        except Exception as e:
            logger.error(f"Error updating job status: {str(e)}")
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job details by ID."""
        if not self.supabase:
            # Mock implementation for local development
            return {
                "id": job_id,
                "status": "pending",
                "created_at": "2023-01-01T00:00:00Z"
            }
            
        try:
            result = self.supabase.table("animations").select("*").eq("id", job_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error getting job: {str(e)}")
            return None
    
    def save_feedback(self, job_id: str, rating: int, comment: Optional[str] = None):
        """Save user feedback."""
        if not self.supabase:
            # Mock implementation for local development
            return
            
        data = {
            "animation_id": job_id,
            "rating": rating,
            "comment": comment
        }
        
        try:
            self.supabase.table("feedback").insert(data).execute()
        except Exception as e:
            logger.error(f"Error saving feedback: {str(e)}")

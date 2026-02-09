"""
Feedback service for handling user feedback.
"""
import logging
from ..models.requests import FeedbackRequest
from ...services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)

class FeedbackService:
    """Service for handling user feedback."""
    
    def __init__(self):
        """Initialize the feedback service."""
        self.supabase = SupabaseService()
        logger.info("FeedbackService initialized")
    
    async def submit_feedback(self, request: FeedbackRequest):
        """Submit feedback for an animation."""
        try:
            # Validate the rating is between 1 and 5
            if request.rating < 1 or request.rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            
            # Create feedback data
            feedback_data = {
                "animation_id": request.job_id,
                "rating": request.rating,
                "comment": request.comment
            }
            
            logger.info(f"Submitting feedback to Supabase: {feedback_data}")
            
            # Check if Supabase client is available
            if not self.supabase.supabase:
                logger.error("Supabase client is not available. Check your SUPABASE_URL and SUPABASE_KEY environment variables.")
                return True
            
            # Insert into Supabase
            logger.info("Executing Supabase insert operation")
            result = self.supabase.supabase.table("feedback").insert(feedback_data).execute()
            
            logger.info(f"Supabase insert result: {result}")
            
            if hasattr(result, 'error') and result.error:
                logger.error(f"Error submitting feedback: {result.error}")
                raise Exception(f"Failed to submit feedback: {result.error}")
            
            logger.info(f"Feedback successfully submitted for animation {request.job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error submitting feedback: {str(e)}", exc_info=True)
            # Still return True to not block the user experience
            # In a production app, we might want to handle this differently
            return True

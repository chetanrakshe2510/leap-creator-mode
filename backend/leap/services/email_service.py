import os
import logging
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.api_key = os.environ.get("SENDGRID_API_KEY")
        self.from_email = os.environ.get("NOTIFICATION_EMAIL_FROM")
        self.client = None
        
        if self.api_key and self.from_email:
            try:
                self.client = SendGridAPIClient(self.api_key)
                logger.info("SendGrid client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize SendGrid client: {str(e)}")
        else:
            logger.warning("SendGrid credentials not found. Email notifications disabled.")
    
    def send_animation_ready_notification(self, email: str, job_id: str, video_url: str) -> bool:
        """Send notification when animation is ready."""
        if not self.client or not email:
            return False
            
        message = Mail(
            from_email=self.from_email,
            to_emails=email,
            subject="Your AskLeap Animation is Ready!",
            html_content=f"""
            <h1>Your animation is ready!</h1>
            <p>Your requested animation has been generated and is ready to view.</p>
            <p><a href="{video_url}">Click here to view your animation</a></p>
            <p>Job ID: {job_id}</p>
            <p>Thank you for using AskLeap!</p>
            """
        )
        
        try:
            response = self.client.send(message)
            logger.info(f"Email notification sent to {email}. Status code: {response.status_code}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
            return False

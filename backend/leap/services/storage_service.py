"""
Storage service for handling file uploads and downloads.
"""
import os
import logging
import shutil
from pathlib import Path
from typing import Optional
import uuid
import mimetypes
from datetime import datetime

logger = logging.getLogger(__name__)

class StorageService:
    """Service for handling file storage."""
    
    def __init__(self):
        # Check if we should use Supabase storage
        self.use_supabase = os.environ.get("USE_SUPABASE_STORAGE", "false").lower() == "true"
        self.bucket_name = os.environ.get("SUPABASE_STORAGE_BUCKET", "videos")
        
        # Get base URL for public access
        self.base_url = os.environ.get("BASE_URL", "http://localhost:8000")
        
        # Set up local storage paths
        self.local_storage_path = os.environ.get(
            "LOCAL_STORAGE_PATH", 
            str(Path(__file__).parent.parent.parent / "generated" / "media" / "videos")
        )
        
        # Ensure local storage directory exists
        Path(self.local_storage_path).mkdir(parents=True, exist_ok=True)
        
        # Initialize Supabase client if needed
        self.supabase_client = None
        if self.use_supabase:
            try:
                from supabase import create_client
                
                supabase_url = os.environ.get("SUPABASE_URL")
                supabase_key = os.environ.get("SUPABASE_KEY")
                
                # Check for missing or placeholder credentials
                if not supabase_url or not supabase_key or \
                   "your_supabase_url_here" in supabase_url or "your_supabase" in supabase_key:
                    logger.warning("Supabase URL or key not found or contains placeholder values")
                    logger.warning("Falling back to local storage")
                    self.use_supabase = False
                else:
                    try:
                        self.supabase_client = create_client(supabase_url, supabase_key)
                        
                        # Check if bucket exists, create if not
                        try:
                            self.supabase_client.storage.get_bucket(self.bucket_name)
                            logger.info(f"Using Supabase storage bucket: {self.bucket_name}")
                        except Exception as e:
                            logger.info(f"Creating Supabase storage bucket: {self.bucket_name}")
                            try:
                                self.supabase_client.storage.create_bucket(
                                    id=self.bucket_name,
                                    options={"public": True}  # Make bucket public
                                )
                            except Exception as bucket_e:
                                logger.error(f"Failed to create bucket: {str(bucket_e)}")
                                self.use_supabase = False
                    except Exception as e:
                        logger.warning(f"Failed to initialize Supabase client: {e}")
                        logger.warning("Falling back to local storage")
                        self.use_supabase = False
            
            except ImportError:
                logger.warning("Supabase package not installed. Falling back to local storage.")
                self.use_supabase = False
        
        logger.info(f"Storage service initialized. Using Supabase: {self.use_supabase}")
    
    def save_file(self, file_path: str, destination_path: Optional[str] = None) -> str:
        """
        Save a file to storage and return the public URL.
        
        Args:
            file_path: Path to the file to save
            destination_path: Optional path to save the file to (if None, will generate a path)
            
        Returns:
            Public URL of the saved file
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Generate a destination path if not provided
        if not destination_path:
            # Extract the directory name and filename
            parent_dir = file_path.parent.name
            filename = file_path.name
            
            # Add a timestamp to the filename to avoid conflicts
            # Get the filename without extension and the extension
            name_parts = filename.rsplit('.', 1)
            if len(name_parts) > 1:
                base_name, extension = name_parts
                # Add timestamp to the base name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_filename = f"{base_name}_{timestamp}.{extension}"
            else:
                # No extension
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_filename = f"{filename}_{timestamp}"
            
            # Create a path that includes the parent directory for organization
            destination_path = f"{parent_dir}/{unique_filename}"
        
        # If using Supabase, upload to Supabase Storage
        if self.use_supabase and self.supabase_client:
            try:
                logger.info(f"Uploading file to Supabase: {destination_path}")
                
                # Get file mime type
                content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                
                # Upload file to Supabase without deleting existing files
                with open(file_path, "rb") as f:
                    file_data = f.read()  # Read file data
                    
                    # Upload the file without checking for existing files
                    result = self.supabase_client.storage.from_(self.bucket_name).upload(
                        destination_path,
                        file_data,
                        {"content-type": content_type}
                    )
                    
                    # Check if result is an object with attributes or a dictionary
                    if hasattr(result, 'get'):
                        # It's a dictionary-like object
                        if not result or not result.get('Key'):
                            raise Exception("Upload failed: No key returned")
                    else:
                        # It's likely an object with attributes
                        # Just check if it exists
                        if not result:
                            raise Exception("Upload failed: No response returned")
                
                # Get public URL
                public_url = self.supabase_client.storage.from_(self.bucket_name).get_public_url(destination_path)
                
                # Remove any trailing question mark if present
                if public_url.endswith('?'):
                    public_url = public_url[:-1]
                    
                logger.info(f"File uploaded to Supabase: {public_url}")
                
                return public_url
            
            except Exception as e:
                logger.error(f"Error uploading to Supabase: {str(e)}")
                logger.info("Falling back to local storage")
                # Fall back to local storage
        
        # Save to local storage
        local_dest = Path(self.local_storage_path) / destination_path
        
        # Ensure directory exists
        local_dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file to local storage
        try:
            shutil.copy2(file_path, local_dest)
            logger.info(f"File saved to local storage: {local_dest}")
            
            # Generate relative path for URL
            relative_path = str(destination_path).replace("\\", "/")
            
            # Create URL
            url = f"{self.base_url}/videos/{relative_path}"
            logger.info(f"Local file URL: {url}")
            
            return url
        
        except Exception as e:
            logger.error(f"Error saving to local storage: {str(e)}")
            # Return original path as fallback
            return str(file_path)
    
    def get_file_url(self, file_path: str) -> str:
        """
        Get the public URL for a file. If the file is not in storage, it will be uploaded.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Public URL of the file
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Extract the directory name and filename for the destination path
        parent_dir = file_path.parent.name
        filename = file_path.name
        destination_path = f"{parent_dir}/{filename}"
        
        # Check if file already exists in Supabase
        if self.use_supabase and self.supabase_client:
            try:
                # We need to actually check if the file exists, not just get the URL
                # Try to list the file to see if it exists
                files = self.supabase_client.storage.from_(self.bucket_name).list(parent_dir)
                file_exists = any(file['name'] == filename for file in files)
                
                if file_exists:
                    # If file exists, return public URL
                    public_url = self.supabase_client.storage.from_(self.bucket_name).get_public_url(destination_path)
                    logger.info(f"File already exists in Supabase: {public_url}")
                    return public_url
                else:
                    # File doesn't exist, upload it
                    logger.info(f"File not found in Supabase, uploading: {destination_path}")
                    return self.save_file(file_path, destination_path)
            
            except Exception as e:
                # Error checking or getting URL, upload it
                logger.error(f"Error checking file in Supabase: {str(e)}")
                logger.info(f"Attempting to upload file: {destination_path}")
                return self.save_file(file_path, destination_path)
        
        # Check if file exists in local storage
        local_path = Path(self.local_storage_path) / destination_path
        if local_path.exists():
            # File exists in local storage, return URL
            relative_path = str(destination_path).replace("\\", "/")
            url = f"{self.base_url}/videos/{relative_path}"
            logger.info(f"File already exists in local storage: {url}")
            return url
        
        # File doesn't exist in storage, save it
        return self.save_file(file_path, destination_path) 
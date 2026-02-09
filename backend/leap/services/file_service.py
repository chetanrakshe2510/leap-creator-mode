import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

from leap.core.config import GENERATED_DIR

class FileService:
    """Service for handling file operations."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize the file service.
        
        Args:
            base_dir: The base directory for generated files
        """
        self.base_dir = base_dir or GENERATED_DIR
        self.logger = logging.getLogger("leap")
        
        # Ensure directories exist
        self.code_dir = self.base_dir / "code"
        self.code_dir.mkdir(exist_ok=True, parents=True)
        
        self.media_dir = self.base_dir / "media"
        self.media_dir.mkdir(exist_ok=True, parents=True)
    
    def save_generated_code(self, code: str, name_base: str) -> str:
        """Save the generated code to a file with proper naming.
        
        Args:
            code: The code to save
            name_base: The base name for the file
            
        Returns:
            The path to the saved file
        """
        # Create a sanitized filename
        safe_name = self.sanitize_filename(name_base)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create the file path
        file_path = self.code_dir / f"{safe_name}_{timestamp}.py"
        
        # Write the code to the file
        with open(file_path, "w") as f:
            f.write(code)
        
        self.logger.info(f"Generated code saved to: {file_path}")
        return str(file_path)
    
    @staticmethod
    def sanitize_filename(name: str) -> str:
        """Create a safe filename from input text.
        
        Args:
            name: The input name
            
        Returns:
            A sanitized filename
        """
        # Remove invalid characters and limit length
        safe_name = "".join(c if c.isalnum() or c in "_- " else "_" for c in name)
        safe_name = safe_name.replace(" ", "_").lower()
        return safe_name[:50]  # Limit length 
import logging
import subprocess
import ast
import re
from pathlib import Path
from typing import Dict, Any, Optional, List

from leap.core.config import GENERATED_DIR

class ManimService:
    """Service for executing Manim code."""
    
    def __init__(self, media_dir: Optional[Path] = None):
        """Initialize the Manim service.
        
        Args:
            media_dir: The directory for Manim media output
        """
        self.media_dir = media_dir or (GENERATED_DIR / "media")
        self.media_dir.mkdir(exist_ok=True, parents=True)
        self.logger = logging.getLogger("leap")
        
        # Map quality to Manim quality flags
        self.quality_flags = {
            "low": "-ql",
            "medium": "-qm",
            "high": "-qh"
        }
    
    def extract_class_name(self, code_content: str) -> str:
        """Extract the class name from Python code using AST parsing.
        
        Args:
            code_content: The Python code content
            
        Returns:
            The name of the first class that inherits from Scene or ManimVoiceoverBase
            
        Raises:
            ValueError: If no class definition is found
        """
        try:
            # Parse the code
            tree = ast.parse(code_content)
            
            # Find the first class definition
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it inherits from Scene or ManimVoiceoverBase
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id in ["Scene", "ManimVoiceoverBase"]:
                            return node.name
                        elif isinstance(base, ast.Attribute) and base.attr in ["Scene", "ManimVoiceoverBase"]:
                            return node.name
                    
                    # If no specific base class found but it's the first class, return it
                    return node.name
            
            # If no class found, raise an error
            raise ValueError("No class definition found in the code")
        
        except Exception as e:
            # If AST parsing fails, fall back to regex as a last resort
            class_match = re.search(r"class\s+(\w+)\s*\(", code_content)
            if class_match:
                return class_match.group(1)
            raise ValueError(f"Could not extract class name: {str(e)}")
    
    def execute_manim_code(self, file_path: str, quality: str) -> Dict[str, Any]:
        """Execute the Manim code and return the result.
        
        Args:
            file_path: The path to the Python file containing Manim code
            quality: The rendering quality ("low", "medium", or "high")
            
        Returns:
            A dictionary containing the execution result
        """
        # Get the quality flag
        quality_flag = self.quality_flags.get(quality, "-ql")
        
        # Execute the Manim code
        try:
            self.logger.info(f"Executing Manim code from file: {Path(file_path).name}")
            
            # Get the class name from the file
            with open(file_path, "r") as f:
                code_content = f.read()
                
            # Extract the class name using AST parsing
            class_name = self.extract_class_name(code_content)
            self.logger.info(f"Found scene class: {class_name}")
            
            # Build the command
            cmd = [
                "python", "-m", "manim", 
                quality_flag, 
                "--media_dir", str(self.media_dir),
                file_path, 
                class_name
            ]
            
            self.logger.info(f"Running Manim with quality: {quality}")
            
            # Execute the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Log a summary of the execution instead of the full output
            output_lines = result.stdout.strip().split("\n")
            self.logger.info(f"Manim execution completed with {len(output_lines)} lines of output")
            
            # Find the output file
            # Manim typically outputs to media_dir/videos/[file_name]/[quality]/[class_name].mp4
            file_name = Path(file_path).stem
            output_file = list(self.media_dir.glob(f"videos/**/{class_name}.mp4"))
            
            if not output_file:
                self.logger.warning("Could not find output video file")
                return {
                    "success": False,
                    "output": result.stdout,
                    "error": "Could not find output video file",
                    "output_file": None
                }
            
            self.logger.info(f"Generated video: {output_file[0]}")
            return {
                "success": True,
                "output": result.stdout,
                "error": None,
                "output_file": str(output_file[0])
            }
            
        except subprocess.CalledProcessError as e:
            # Log a summary of the error instead of the full stderr
            error_lines = e.stderr.strip().split("\n") if e.stderr else []
            error_summary = "\n".join(error_lines[-5:]) if error_lines else "Unknown error"
            self.logger.error(f"Manim execution failed with error: {error_summary}")
            return {
                "success": False,
                "output": e.stdout,
                "error": e.stderr,
                "output_file": None
            }
        except Exception as e:
            self.logger.error(f"Error executing Manim code: {str(e)}")
            return {
                "success": False,
                "output": None,
                "error": str(e),
                "output_file": None
            } 
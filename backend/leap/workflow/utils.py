import re
import tempfile
import logging
from leap.core.config import GENERATED_DIR, LOGS_DIR, RUN_TIMESTAMP
from leap.templates import get_api_doc

def get_manim_api_context() -> str:
    """Get Manim API context by reading from the templates."""
    # Read the API documentation from the templates directory
    return get_api_doc("breaking_changes")

def log_state_transition(node_name: str, input_state: dict, output_state: dict):
    """Log the state transition for a node, showing what changed."""
    logger = logging.getLogger(__name__)
    logger.info(f"\n{'='*50}\nNode: {node_name}")
    
    # Log input state
    logger.info("Input State:")
    for k, v in input_state.items():
        if k in ['generated_code', 'plan'] and v:
            logger.info(f"  {k}: <{len(str(v))} chars>")
        else:
            logger.info(f"  {k}: {v}")
    
    # Log changes between input and output states
    logger.info("Changes:")
    for k in output_state:
        if k in input_state:
            if output_state[k] != input_state[k]:
                if k in ['generated_code', 'plan']:
                    logger.info(f"  {k}: <updated - {len(str(output_state[k]))} chars>")
                else:
                    logger.info(f"  {k}: {input_state[k]} -> {output_state[k]}")
        else:
            logger.info(f"  + {k}: {output_state[k]}")
    
    # Log error if present
    if output_state.get('error'):
        logger.error(f"Error in {node_name}: {output_state['error']}")
    
    logger.info(f"{'='*50}\n")
    return output_state

def create_temp_dir():
    """Create a temporary directory for Manim operations."""
    temp_dir = tempfile.mkdtemp(prefix="manim_")
    logging.getLogger(__name__).info(f"Created temporary directory at: {temp_dir}")
    return temp_dir

def extract_concept(text: str) -> str:
    """
    Extract the underlying concept from a user input string.
    
    This function processes user input to extract the core concept by:
    1. Removing common question prefixes
    2. Cleaning special characters
    3. Normalizing whitespace
    4. Handling edge cases
    
    Args:
        text: The user input text
        
    Returns:
        A cleaned, normalized string representing the core concept
    """
    if not text:
        return "unknown_concept"
    
    # Convert to lowercase and trim whitespace
    text = text.lower().strip()
    
    # Remove common question prefixes
    prefixes = [
        "how to", "what is", "explain", "describe", "why is", "tell me about",
        "show me", "can you explain", "i want to learn about", "teach me",
        "could you show", "please explain", "i need help with"
    ]
    
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
            break
    
    # Remove question marks and other punctuation at the end
    text = text.rstrip("?!.,;:")
    
    # Replace special characters with spaces
    text = re.sub(r'[^\w\s-]', ' ', text)
    
    # Normalize whitespace (replace multiple spaces with single space)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Convert spaces to underscores for filename compatibility
    concept = re.sub(r'\s+', '_', text)
    
    # Limit length to avoid excessively long filenames
    if len(concept) > 50:
        concept = concept[:50]
    
    # Ensure we don't have trailing underscores
    concept = concept.strip('_')
    
    # Handle empty result
    if not concept:
        return "unknown_concept"
    
    return concept

def generate_scene_filename(topic: str) -> str:
    """Generate a unique scene filename from the user input."""
    concept = extract_concept(topic)
    timestamp = RUN_TIMESTAMP[:13]
    filename = f"{concept}_{timestamp}.py"
    return str(GENERATED_DIR / filename)

# def generate_code(prompt, quality="low", level="normal"):
#     """
#     Generate Manim code based on a prompt.
    
#     Args:
#         prompt: The user prompt
#         quality: The rendering quality
#         level: The explanation level
        
#     Returns:
#         A dictionary containing the generated code
#     """
#     # This is a placeholder implementation for testing
#     # In a real implementation, this would call the LLM
#     return {
#         "generated_code": """
#         from manim import *
        
#         class CircleGrowth(Scene):
#             def construct(self):
#                 circle = Circle(radius=0.5, color=WHITE)
#                 self.play(Create(circle))
#                 self.play(circle.animate.scale(2))
#                 self.wait()
#         """
#     }

def execute_code(code, quality="low"):
    """
    Execute the generated Manim code.
    
    Args:
        code: The Manim code to execute
        quality: The rendering quality
        
    Returns:
        A dictionary containing the execution result
    """
    # This is a placeholder implementation for testing
    # In a real implementation, this would execute the code
    return {
        "success": True,
        "output_file": "/path/to/output.mp4"
    }

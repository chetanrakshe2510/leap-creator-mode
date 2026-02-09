"""
Test the workflow directly without API.
"""
import logging
from pathlib import Path
from leap.workflow import workflow
from leap.workflow.state import GraphState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_workflow_directly():
    """Test the workflow directly without API."""
    # Create output directory
    output_dir = Path("generated/media/videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a simple test state
    state = GraphState(
        user_input="Show a circle",
        rendering_quality="low",
        duration_detail="brief",
        user_level="normal",
        voice_model="nova",
        output_file="generated/media/videos/test_circle.mp4"
    )
    
    logger.info("Starting workflow execution...")
    logger.info(f"State: {state}")
    
    # Execute workflow
    result = workflow.invoke(state)
    logger.info(f"Workflow result: {result}")
    
    # Check if files were created
    video_file = output_dir / "test_circle.mp4"
    logger.info(f"Checking for video file at: {video_file.absolute()}")
    logger.info("Directory contents:")
    for file in output_dir.iterdir():
        logger.info(f"  - {file.name}")
    
    return video_file.exists()

if __name__ == "__main__":
    logger.info("Starting direct workflow test...")
    success = test_workflow_directly()
    logger.info(f"Test {'passed' if success else 'failed'}")

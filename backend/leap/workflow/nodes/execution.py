from typing import Optional
from leap.workflow.state import GraphState
from leap.core.logging import setup_question_logger
from leap.services import FileService, ManimService
from leap.core.config import MAX_ATTEMPTS


def execute_code(
    state: GraphState, 
    file_service: Optional[FileService] = None,
    manim_service: Optional[ManimService] = None
) -> GraphState:
    """Execute the generated Manim code and return the result.
    
    Args:
        state: The current workflow state
        file_service: Optional file service for dependency injection
        manim_service: Optional Manim service for dependency injection
        
    Returns:
        The updated workflow state
    """
    logger = setup_question_logger(state["user_input"])
    logger.info("Executing Manim code")
    
    # Use provided services or create new ones
    file_service = file_service or FileService()
    manim_service = manim_service or ManimService()
    
    try:
        # Get the code from the state
        code = state.get("generated_code")
        if not code:
            logger.error("No code found in state")
            state["error"] = "No code found to execute"
            # Set a default execution_result to prevent NoneType errors
            state["execution_result"] = {
                "success": False,
                "output": None,
                "error": "No code found to execute",
                "output_file": None
            }
            return state
            
        # Get rendering quality from state
        rendering_quality = state.get("rendering_quality", "low")
        logger.info(f"Using rendering quality: {rendering_quality}")
        
        # Get voice model from state
        voice_model = state.get("voice_model", "nova")
        logger.info(f"Using voice model: {voice_model}")
        
        # Save the generated code to a file
        file_path = file_service.save_generated_code(code, state["user_input"])
        logger.info(f"Generated code saved to: {file_path}")
        
        # Execute the Manim code
        logger.info("Starting Manim execution...")
        execution_result = manim_service.execute_manim_code(file_path, rendering_quality)
        
        # Update the state with the execution result
        if execution_result["success"]:
            output_file = execution_result.get("output_file", "Unknown")
            logger.info(f"Execution completed successfully. Output file: {output_file}")
            state["execution_result"] = execution_result
            state["error"] = None
        else:
            error = execution_result.get("error", "Unknown error")
            # Don't truncate error messages anymore to preserve important details
            logger.error(f"Error executing code: {error}")
            
            # Check if we've reached the maximum number of correction attempts
            current_attempts = state.get("correction_attempts", 0)
            if current_attempts >= MAX_ATTEMPTS - 1:  # -1 because we increment after this node
                logger.warning(f"Maximum correction attempts ({MAX_ATTEMPTS}) reached. Workflow will terminate.")
                logger.info(f"Final error after {MAX_ATTEMPTS} correction attempts: {error[:200]}...")
            
            state["execution_result"] = execution_result
            state["error"] = f"Error executing code: {error}"
        
    except Exception as e:
        logger.error(f"Error executing code: {str(e)}", exc_info=True)
        
        # Check if we've reached the maximum number of correction attempts
        current_attempts = state.get("correction_attempts", 0)
        if current_attempts >= MAX_ATTEMPTS - 1:  # -1 because we increment after this node
            logger.warning(f"Maximum correction attempts ({MAX_ATTEMPTS}) reached. Workflow will terminate.")
            logger.info(f"Final error after {MAX_ATTEMPTS} correction attempts: {str(e)}")
        
        state["error"] = f"Error executing code: {str(e)}"
        # Even in case of error, set a default execution_result to prevent NoneType errors
        state["execution_result"] = {
            "success": False,
            "output": None,
            "error": str(e),
            "output_file": None
        }
    
    return state 
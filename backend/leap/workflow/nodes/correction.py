from typing import Dict, Any, Optional

from leap.workflow.state import GraphState
from leap.core.logging import setup_question_logger
from leap.models import ManimCodeResponse
from leap.services import LLMService, FileService
from leap.core.config import  MAX_ATTEMPTS
from leap.prompts import ERROR_CORRECTION_PROMPTS
from leap.prompts.base import PromptVersion
from leap.workflow.utils import get_manim_api_context


def error_correction(
    state: GraphState, 
    config: Optional[Dict[str, Any]] = None,
    llm_service: Optional[LLMService] = None,
    file_service: Optional[FileService] = None,
    **kwargs
) -> GraphState:
    """Correct code based on error message using structured output.
    
    Args:
        state: The current workflow state
        config: Optional configuration parameters
        llm_service: Optional LLM service for dependency injection
        file_service: Optional file service for dependency injection
        
    Returns:
        The updated workflow state
    """
    logger = setup_question_logger(state["user_input"])
    
    # Get error message and truncate if too long for logging
    error_msg = state.get("error", "Unknown error")
    log_error = error_msg
    if len(log_error) > 200:
        log_error = log_error[:197] + "..."
    
    # Get current correction attempt count
    current_attempts = state.get("correction_attempts", 0)
    
    # Log the attempt number
    logger.info(f"Attempting to fix error (attempt {current_attempts + 1} of {MAX_ATTEMPTS}): {log_error}")
    
    # Check if we're about to reach the maximum attempts
    if current_attempts >= MAX_ATTEMPTS - 1:
        logger.warning(f"This is the final correction attempt (maximum is {MAX_ATTEMPTS}).")
    
    manim_api_context = get_manim_api_context()
    
    # Use provided services or create new ones
    llm_service = llm_service or LLMService()
    file_service = file_service or FileService()
    
    try:
        # Get the prompt template (using production version by default)
        prompt_template = ERROR_CORRECTION_PROMPTS.get(PromptVersion.PRODUCTION)
        
        # Format the prompt with our parameters
        formatted_prompt = prompt_template.format(
            error=error_msg,
            generated_code=state["generated_code"],
            plan=state["plan"],
            manim_api_context=manim_api_context
        )
        
        # Store the prompts in the state for tracing
        if "prompts" not in state:
            state["prompts"] = {}
        state["prompts"]["correction"] = {
            "system": formatted_prompt["system"],
            "user": formatted_prompt["user"]
        }
        
        # Generate the corrected code with structured output
        logger.info("Generating corrected code...")
        
        # Use the LLM service to generate the corrected code
        response = llm_service.generate_structured_response(
            system_content=formatted_prompt["system"],
            user_content=formatted_prompt["user"],
            response_model=ManimCodeResponse
        )
        
        # Log the corrected code and explanation
        if response.explanation:
            # Truncate explanation if it's too long
            explanation = response.explanation
            if len(explanation) > 200:
                explanation = explanation[:197] + "..."
            logger.info(f"Correction explanation: {explanation}")
        
        if response.error_fixes:
            logger.info(f"Errors fixed: {', '.join(response.error_fixes[:5])}" + 
                       (f" and {len(response.error_fixes) - 5} more..." if len(response.error_fixes) > 5 else ""))
        
        if response.validation_checks:
            logger.info(f"Validation checks performed: {len(response.validation_checks)}")
        
        # Save the corrected code to a file
        file_path = file_service.save_generated_code(response.code, state["user_input"])
        logger.info(f"Corrected code saved to: {file_path}")
        
        # Create a new state with the corrected code
        new_state = GraphState(
            user_input=state["user_input"],
            plan=state["plan"],
            generated_code=response.code,
            execution_result=None,
            error=None,
            correction_attempts=state.get("correction_attempts", 0) + 1,
            rendering_quality=state.get("rendering_quality", "low"),
            duration_detail="short",  # Fixed to short for initial release
            user_level=state.get("user_level", "normal"),
            voice_model=state.get("voice_model", "nova"),
            email=state.get("email")
        )
        
        # Check if this was the last allowed attempt
        if new_state["correction_attempts"] >= MAX_ATTEMPTS:
            logger.warning(f"Maximum correction attempts ({MAX_ATTEMPTS}) reached. This is the final attempt.")
        
        return new_state
        
    except Exception as e:
        error_msg = f"Error correction failed: {str(e)}"
        logger.error(error_msg)
        
        # Increment the correction attempts counter
        new_correction_attempts = state.get("correction_attempts", 0) + 1
        
        # Check if this was the last allowed attempt
        if new_correction_attempts >= MAX_ATTEMPTS:
            logger.warning(f"Maximum correction attempts ({MAX_ATTEMPTS}) reached. Workflow will terminate with error.")
        
        return GraphState(
            user_input=state["user_input"],
            plan=state["plan"],
            generated_code=state["generated_code"],
            execution_result=None,
            error=error_msg,
            correction_attempts=new_correction_attempts,
            rendering_quality=state.get("rendering_quality", "low"),
            duration_detail="short",  # Fixed to short for initial release
            user_level=state.get("user_level", "normal"),
            voice_model=state.get("voice_model", "nova"),
            email=state.get("email")
        ) 
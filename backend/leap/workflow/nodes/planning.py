from typing import  Optional
from langsmith import traceable

from leap.workflow.state import GraphState
from leap.core.logging import setup_question_logger
from leap.models import ScenePlanResponse
from leap.services import LLMService
from leap.prompts import SCENE_PLANNING_PROMPTS
from leap.prompts.base import PromptVersion



# Each scene should have clear objectives and specific animation notes."""

def plan_scenes(state: GraphState, llm_service: Optional[LLMService] = None) -> GraphState:
    """Plan the scenes based on user input.
    
    Args:
        state: The current workflow state
        llm_service: Optional LLM service for dependency injection
        
    Returns:
        The updated workflow state
    """
    logger = setup_question_logger(state["user_input"])
    logger.info(f"Planning scenes for input: {state['user_input']}")
    
    # Use provided service or create a new one
    llm_service = llm_service or LLMService()
    
    try:
        # Get user level from state
        user_level = state.get("user_level", "normal")
        
        # Create a user level instruction
        user_level_instruction = ""
        if user_level == "ELI5":
            user_level_instruction = "Explain this concept as if to a 5 year old. Use very simple words, fun stories, colorful examples, and pictures that a small child would understand. Avoid any complicated words. Compare ideas to things children experience in daily life like toys, animals, or family activities."
        elif user_level == "advanced":
            user_level_instruction = "Explain this concept at an advanced level. You can use appropriate terminology and go into technical details."
        else:  # normal
            user_level_instruction = "Explain this concept at a high school/early college level. You can use appropriate terminology but still make it accessible."
        
        # Fixed duration instruction for initial release
        duration_instruction = "The video should be 1-2 minutes long, so focus on the most important aspects of the concept."
        
        logger.info(f"Generating scene plan with user level: {user_level}")
        
        # Use reformulated input if available, otherwise use the original
        input_for_planning = state.get("reformulated_input") or state["user_input"]
        logger.info(f"Using {'reformulated' if 'reformulated_input' in state else 'original'} input for planning: {input_for_planning}")
        
        # Get the prompt template (using production version by default)
        prompt_template = SCENE_PLANNING_PROMPTS.get(PromptVersion.PRODUCTION)
        
        # Format the prompt with our parameters
        formatted_prompt = prompt_template.format(
            user_input=input_for_planning,
            user_level_instruction=user_level_instruction,
            duration_instruction=duration_instruction
        )
        
        # Store the prompts in the state for tracing
        if "prompts" not in state:
            state["prompts"] = {}
        state["prompts"]["planning"] = {
            "system": formatted_prompt["system"],
            "user": formatted_prompt["user"]
        }
        
        # Use instructor with a response model
        response = llm_service.generate_structured_response(
            system_content=formatted_prompt["system"],
            user_content=formatted_prompt["user"],
            response_model=ScenePlanResponse
        )
        
        # Log a summary of the plan
        plan = response.plan
        plan_summary = plan.split("\n")[0] if plan and "\n" in plan else plan[:100] + "..."
        logger.info(f"Generated plan: {plan_summary}")
        
        # Create a new state with the plan
        return GraphState(
            user_input=state["user_input"],
            plan=plan,
            generated_code=None,
            execution_result=None,
            error=None,
            correction_attempts=0,
            rendering_quality=state.get("rendering_quality", "low"),
            duration_detail="short",  # Fixed to short for initial release
            user_level=state.get("user_level", "normal"),
            voice_model=state.get("voice_model", "nova"),
            email=state.get("email"),
            prompts=state.get("prompts", {})  # Preserve prompts from previous steps
        )
        
    except Exception as e:
        logger.error(f"Scene planning failed: {str(e)}")
        return GraphState(
            user_input=state["user_input"],
            plan=None,
            generated_code=None,
            execution_result=None,
            error=f"Scene planning failed: {str(e)}",
            correction_attempts=0,
            rendering_quality=state.get("rendering_quality", "low"),
            duration_detail="short",  # Fixed to short for initial release
            user_level=state.get("user_level", "normal"),
            voice_model=state.get("voice_model", "nova"),
            email=state.get("email")
        ) 
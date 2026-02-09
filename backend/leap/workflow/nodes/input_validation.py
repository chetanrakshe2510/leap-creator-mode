"""
Input validation node for the workflow.

This module contains the function for validating user input before proceeding with animation generation.
"""
from typing import Dict, Any, Optional, List
import re
from leap.workflow.state import GraphState
from leap.core.logging import setup_question_logger
from leap.services.llm_service import LLMService
from leap.models import ValidationResult


def validate_input(state: GraphState, llm_service: Optional[LLMService] = None, **kwargs) -> GraphState:
    """Validate the user input to ensure it's suitable for animation generation.
    
    Args:
        state: The current workflow state
        llm_service: Optional LLM service for validation
        
    Returns:
        The updated workflow state with validation results
    """
    logger = setup_question_logger(state["user_input"])
    logger.info(f"Validating user input: '{state['user_input']}'")
    
    # Check for Mock Mode - skip LLM validation
    from leap.core.config import MOCK_MODE
    if MOCK_MODE:
        logger.info("MOCK MODE ENABLED: Skipping input validation.")
        return GraphState(
            user_input=state["user_input"],
            validation_status="valid",
            reformulated_input=state["user_input"]
        )
    
    # Get the user input
    user_input = state["user_input"].strip()
    
    # Basic validation checks
    if not user_input:
        logger.error("Empty input received")
        return GraphState(
            user_input=state["user_input"],
            error="Input cannot be empty. Please provide a specific question or topic for animation.",
            validation_status="invalid"
        )
    
    if len(user_input) < 10:
        logger.error(f"Input too short: '{user_input}'")
        return GraphState(
            user_input=state["user_input"],
            error="Input is too short, should be over 10 characters. Please provide a more detailed question or topic for animation.",
            validation_status="invalid"
        )
    if len(user_input) > 140:
        logger.error(f"Input too long: '{user_input}'")
        return GraphState(
            user_input=state["user_input"],
            error="Input is too long, keep it under 140 characters. Please provide a more concise question or topic for animation.",
            validation_status="invalid"
        )

    # Use provided service or create a new one
    llm_service = llm_service or LLMService()
    
    logger.info("Using LLM to validate input")
    
    # Create a prompt for the LLM to evaluate the input
    prompt = f"""
    You are evaluating whether a user's input is suitable for generating an educational animation.
    
    User input: "{user_input}"
    
    Evaluate this input based on the following criteria:
    1. Is it a clear question or topic that can be visually explained?
    2. Is it specific enough to generate a meaningful animation?
    3. Is it related to a concept that can be animated (e.g., science, math, processes)?
    4. Is it free from harmful, offensive, or inappropriate content?
    
    Classify the input as one of:
    - VALID: Clear, specific question or topic that can be animated
    - NEEDS_CLARIFICATION: Potentially valid but vague or ambiguous
    - INVALID: Too short, offensive, impossible to animate, or not a question/topic
    
    For EVERY input, regardless of classification:
    - Provide a reformulated, clearer version of the question that would be ideal for animation
    - The reformulation should maintain the original intent but make it more specific and clear
    - If the input is already perfect, the reformulation can be identical to the input
    
    For NEEDS_CLARIFICATION or INVALID inputs:
    - Provide a helpful suggestion that guides the user toward a better question
    - Phrase suggestions positively, focusing on what would work rather than what's wrong
    - If possible, offer 1-2 specific examples of better ways to ask
    
    Return your response in the ValidationResult format with the following fields:
    - classification: Either "VALID", "NEEDS_CLARIFICATION", or "INVALID"
    - explanation: Your explanation for the classification
    - suggestion: Specific guidance for improving the question (for NEEDS_CLARIFICATION or INVALID)
    - reformulated_question: A clearer, more specific version of the user's question
    """
    
    # Store the prompts in the state for tracing
    if "prompts" not in state:
        state["prompts"] = {}
    state["prompts"]["input_validation"] = {
        "system": "You are evaluating whether a user's input is suitable for generating an educational animation.",
        "user": prompt
    }
    
    try:
        # Use the structured response instead of chat
        validation_result = llm_service.generate_structured_response(
            system_content="You are evaluating whether a user's input is suitable for generating an educational animation.",
            user_content=prompt,
            response_model=ValidationResult
        )
        
        # Now you can directly use the structured fields
        classification = validation_result.classification
        explanation = validation_result.explanation
        suggestion = validation_result.suggestion or ""
        reformulated_question = validation_result.reformulated_question or user_input
        
        logger.info(f"Input classified as: {classification}")
        logger.info(f"Reformulated question: {reformulated_question}")
        
        if classification == "VALID":
            return GraphState(
                user_input=state["user_input"],
                validation_status="valid",
                # Store the reformulated question even for valid inputs
                reformulated_input=reformulated_question
            )
        elif classification == "NEEDS_CLARIFICATION":
            suggested_question = f"Did you mean: \"{reformulated_question}\"? "
            friendly_message = f"Your question could be clearer. {suggested_question}{suggestion}"
            
            return GraphState(
                user_input=state["user_input"],
                error=friendly_message,
                suggestion=suggestion,
                reformulated_input=reformulated_question,
                validation_status="needs_clarification"
            )
        else:  # INVALID
            return GraphState(
                user_input=state["user_input"],
                error=f"We're having trouble understanding your request: {explanation}",
                suggestion=suggestion,
                reformulated_input=reformulated_question,
                validation_status="invalid"
            )
            
    except Exception as e:
        logger.error(f"Error during LLM validation: {str(e)}")
        # Fall back to basic validation - assume valid if LLM fails
        return GraphState(
            user_input=state["user_input"],
            validation_status="valid"
        ) 
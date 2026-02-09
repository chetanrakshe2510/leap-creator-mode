from langgraph.graph import StateGraph, END
from leap.workflow.state import GraphState
from leap.core.config import MAX_ATTEMPTS
from leap.workflow.nodes import (
    validate_input,
    plan_scenes,
    generate_code,
    validate_code,
    execute_code,
    error_correction,
)
from leap.core.logging import setup_question_logger
from leap.workflow.tracing import traceable

@traceable(name="log_workflow_end", tags=["logging"])
def log_workflow_end(state: GraphState) -> GraphState:
    """Log the end of the workflow with appropriate status messages.
    
    Args:
        state: The current workflow state
        
    Returns:
        The unchanged state
    """
    logger = setup_question_logger(state["user_input"])
    
    # Check if there was an error
    if state.get("error"):
        # Check if we reached max correction attempts
        if state.get("correction_attempts", 0) >= MAX_ATTEMPTS:
            logger.error(f"Workflow ended after {MAX_ATTEMPTS} correction attempts with unresolved error.")
            logger.error(f"Final error: {state['error'][:200]}...")
        else:
            logger.error(f"Workflow ended with error: {state['error'][:200]}...")
    else:
        # Success case
        logger.info("Workflow completed successfully!")
        
        # Log output file if available
        if state.get("execution_result") and state.get("execution_result").get("output_file"):
            logger.info(f"Output file: {state['execution_result']['output_file']}")
    
    return state

def create_workflow() -> StateGraph:
    """Create and return the workflow graph."""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("validate_input", validate_input)
    workflow.add_node("plan_scenes", plan_scenes)
    workflow.add_node("generate_code", generate_code)
    workflow.add_node("validate_code", validate_code)
    workflow.add_node("execute_code", execute_code)
    workflow.add_node("correct_code", error_correction)
    workflow.add_node("log_end", log_workflow_end)

    
    # Set entry point and basic flow
    workflow.set_entry_point("validate_input")
    
    # Add conditional edges from input validation
    workflow.add_conditional_edges(
        "validate_input",
        lambda state: "plan_scenes" if state.get("validation_status") == "valid" else "log_end",
        {
            "plan_scenes": "plan_scenes",
            "log_end": "log_end"
        }
    )
    
    workflow.add_edge("plan_scenes", "generate_code")
    workflow.add_edge("generate_code", "validate_code")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "validate_code",
        lambda state: "correct_code" if state.get("error") else "execute_code",
        {
            "correct_code": "correct_code",
            "execute_code": "execute_code"
        }
    )
    
    workflow.add_conditional_edges(
        "correct_code",
        lambda state: "validate_code" if state["correction_attempts"] < MAX_ATTEMPTS else "log_end",
        {
            "validate_code": "validate_code",
            "log_end": "log_end"
        }
    )
    
    workflow.add_conditional_edges(
        "execute_code",
        lambda state: "correct_code" if (state.get("error") and state["correction_attempts"] < MAX_ATTEMPTS) else "log_end",
        {
            "correct_code": "correct_code",
            "log_end": "log_end"
        }
    )
    
    # Add final logging step before ending
    workflow.add_edge("log_end", END)
    
    return workflow.compile()

# Create the compiled workflow
workflow = create_workflow()

# Note: For workflow visualization, use the CLI command:
# python -m leap.main visualize-workflow --output workflow_graph.png
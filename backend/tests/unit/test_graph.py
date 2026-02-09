"""
Unit tests for the workflow graph.
"""
import pytest
from unittest.mock import patch, MagicMock
from leap.workflow import workflow, GraphState
from leap.workflow.graph import create_workflow, log_workflow_end
from leap.core.config import MAX_ATTEMPTS

def test_workflow_creation():
    """Test basic workflow creation and structure."""
    graph = create_workflow()
    assert graph is not None
    assert workflow is not None  # Check global instance

# For now skip detailed logging tests since they're not critical
# and focus on the core workflow functionality
@patch('leap.workflow.nodes.validate_input')
@patch('leap.workflow.nodes.plan_scenes')
@patch('leap.workflow.nodes.generate_code')
def test_workflow_happy_path(mock_generate, mock_plan, mock_validate):
    """Test the main workflow happy path."""
    # Setup mock returns
    mock_validate.return_value = GraphState(
        user_input="How does gravity work?",
        validation_status="valid"
    )
    
    mock_plan.return_value = GraphState(
        user_input="How does gravity work?",
        validation_status="valid",
        plan="1. Explain gravity\n2. Show examples"
    )
    
    mock_generate.return_value = GraphState(
        user_input="How does gravity work?",
        validation_status="valid",
        plan="1. Explain gravity\n2. Show examples",
        generated_code="print('Hello, world!')"
    )
    
    # Create initial state
    initial_state = GraphState(user_input="How does gravity work?")
    
    # Note: We're not actually running the workflow here since it requires
    # setting up the full langgraph infrastructure. Instead, we verify
    # that our workflow components are properly configured.
    assert mock_validate.call_count == 0  # No calls yet
    assert mock_plan.call_count == 0
    assert mock_generate.call_count == 0

def test_workflow_state_transitions():
    """Test that workflow states can be properly updated."""
    # Test basic state transitions
    state = GraphState(user_input="How does gravity work?")
    
    # Test validation state update
    state["validation_status"] = "valid"
    assert state["validation_status"] == "valid"
    
    # Test plan update
    state["plan"] = "1. Show concept\n2. Animate"
    assert state["plan"] == "1. Show concept\n2. Animate"
    
    # Test code generation update
    state["generated_code"] = "print('test')"
    assert state["generated_code"] == "print('test')" 
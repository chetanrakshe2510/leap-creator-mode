"""
Unit tests for the input validation node.
"""
import pytest
from unittest.mock import patch, MagicMock
from leap.workflow import GraphState
from leap.workflow.nodes.input_validation import validate_input
from leap.models import ValidationResult

@pytest.fixture
def mock_logger():
    """Fixture for mocked logger."""
    with patch('leap.core.logging.setup_question_logger') as mock:
        mock_logger = MagicMock()
        mock.return_value = mock_logger
        yield mock_logger

def test_basic_validation(mock_logger):
    """Test basic input validation scenarios."""
    # Empty input
    state = GraphState(user_input="")
    result = validate_input(state)
    assert result["validation_status"] == "invalid"
    assert "error" in result
    
    # Valid question
    state = GraphState(user_input="How does gravity work?")
    result = validate_input(state)
    assert result["validation_status"] == "valid"
    assert "error" not in result
    
    # Valid topic
    state = GraphState(user_input="Explain the process of photosynthesis.")
    result = validate_input(state)
    assert result["validation_status"] == "valid"
    assert "error" not in result

@patch('leap.workflow.nodes.input_validation.LLMService')
def test_llm_validation(mock_llm_service_class, mock_logger):
    """Test LLM-based validation with valid input."""
    # Create a mock LLM service
    mock_llm = MagicMock()
    mock_llm_service_class.return_value = mock_llm
    
    # Mock the structured response - this is what the code expects now
    mock_validation_result = ValidationResult(
        classification="VALID",
        explanation="Clear question about a scientific concept.",
        suggestion=None,
        reformulated_question="How does gravity work and affect objects on Earth?"
    )
    
    # Configure the mock to return our structured response
    mock_llm.generate_structured_response.return_value = mock_validation_result
    
    # Test with the mocked service
    state = GraphState(user_input="How does gravity work?")
    result = validate_input(state)
    
    # Verify the result
    assert result["validation_status"] == "valid"
    assert "error" not in result 
    assert result["reformulated_input"] == "How does gravity work and affect objects on Earth?" 
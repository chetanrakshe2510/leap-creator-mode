"""
Unit tests for the workflow state.
"""
import pytest
from leap.workflow import GraphState

@pytest.fixture
def minimal_state():
    """Fixture for a minimal state."""
    return GraphState(user_input="How does gravity work?")

@pytest.fixture
def complete_state():
    """Fixture for a complete state with all fields."""
    return GraphState(
        user_input="How does gravity work?",
        rendering_quality="high",
        duration_detail="detailed",
        user_level="advanced",
        voice_model="alloy",
        correction_attempts=2,
        error="Some error occurred",
        generated_code="print('Hello, world!')",
        execution_result={"success": True, "output_file": "/path/to/file.mp4"},
        plan="1. Explain gravity\n2. Show examples",
        email="user@example.com"
    )

def test_create_minimal_state(minimal_state):
    """Test creating a minimal state with only required fields."""
    # Check that the field is set
    assert minimal_state["user_input"] == "How does gravity work?"
    
    # Check that optional fields have default values or are not set
    assert "rendering_quality" not in minimal_state or minimal_state["rendering_quality"] == "low"
    assert "duration_detail" not in minimal_state or minimal_state["duration_detail"] == "short"
    assert "user_level" not in minimal_state or minimal_state["user_level"] == "normal"
    assert "voice_model" not in minimal_state or minimal_state["voice_model"] == "nova"

def test_create_complete_state(complete_state):
    """Test creating a state with all fields."""
    # Check that all fields are set with correct values
    assert complete_state["user_input"] == "How does gravity work?"
    assert complete_state["rendering_quality"] == "high"
    assert complete_state["duration_detail"] == "detailed"
    assert complete_state["user_level"] == "advanced"
    assert complete_state["voice_model"] == "alloy"
    assert complete_state["correction_attempts"] == 2
    assert complete_state["error"] == "Some error occurred"
    assert complete_state["generated_code"] == "print('Hello, world!')"
    assert complete_state["execution_result"]["success"] is True
    assert complete_state["execution_result"]["output_file"] == "/path/to/file.mp4"
    assert complete_state["plan"] == "1. Explain gravity\n2. Show examples"
    assert complete_state["email"] == "user@example.com"

def test_update_state(minimal_state):
    """Test updating a state."""
    # Update the state with new values
    minimal_state["rendering_quality"] = "high"
    minimal_state["duration_detail"] = "detailed"
    minimal_state["user_level"] = "advanced"
    minimal_state["voice_model"] = "alloy"
    minimal_state["correction_attempts"] = 2
    minimal_state["error"] = "Some error occurred"
    minimal_state["generated_code"] = "print('Hello, world!')"
    minimal_state["execution_result"] = {"success": True, "output_file": "/path/to/file.mp4"}
    minimal_state["plan"] = "1. Explain gravity\n2. Show examples"
    minimal_state["email"] = "user@example.com"
    
    # Verify all updates
    assert minimal_state["rendering_quality"] == "high"
    assert minimal_state["duration_detail"] == "detailed"
    assert minimal_state["user_level"] == "advanced"
    assert minimal_state["voice_model"] == "alloy"
    assert minimal_state["correction_attempts"] == 2
    assert minimal_state["error"] == "Some error occurred"
    assert minimal_state["generated_code"] == "print('Hello, world!')"
    assert minimal_state["execution_result"]["success"] is True
    assert minimal_state["execution_result"]["output_file"] == "/path/to/file.mp4"
    assert minimal_state["plan"] == "1. Explain gravity\n2. Show examples"
    assert minimal_state["email"] == "user@example.com"

def test_state_as_dict(complete_state):
    """Test using the state as a dictionary."""
    # Convert to dictionary
    state_dict = dict(complete_state)
    
    # Check that the dictionary contains the expected keys
    assert "user_input" in state_dict
    assert "rendering_quality" in state_dict
    assert "duration_detail" in state_dict
    assert "user_level" in state_dict
    assert "voice_model" in state_dict
    
    # Check values
    assert state_dict["user_input"] == "How does gravity work?"
    assert state_dict["rendering_quality"] == "high"
    assert state_dict["duration_detail"] == "detailed"
    assert state_dict["user_level"] == "advanced"
    assert state_dict["voice_model"] == "alloy"

def test_state_copy(complete_state):
    """Test copying a state."""
    # Create a copy
    state_copy = dict(complete_state)
    
    # Verify copy has same values
    assert state_copy["user_input"] == complete_state["user_input"]
    assert state_copy["rendering_quality"] == complete_state["rendering_quality"]
    assert state_copy["duration_detail"] == complete_state["duration_detail"]
    assert state_copy["user_level"] == complete_state["user_level"]
    assert state_copy["voice_model"] == complete_state["voice_model"]
    
    # Modify copy and verify original is unchanged
    state_copy["rendering_quality"] = "low"
    assert complete_state["rendering_quality"] == "high"
    assert state_copy["rendering_quality"] == "low"

def test_optional_fields():
    """Test that all fields are optional except user_input."""
    # Create state with only user_input
    state = GraphState(user_input="test")
    assert state["user_input"] == "test"
    
    # Access optional fields - they should either not exist or have default values
    assert "rendering_quality" not in state or state["rendering_quality"] == "low"
    assert "duration_detail" not in state or state["duration_detail"] == "short"
    assert "user_level" not in state or state["user_level"] == "normal"
    assert "voice_model" not in state or state["voice_model"] == "nova"
    assert "correction_attempts" not in state or state["correction_attempts"] == 0

def test_field_types():
    """Test that fields accept correct types."""
    state = GraphState(
        user_input="test",
        correction_attempts=1,  # int
        execution_result={"success": True},  # dict
        error=None,  # Optional[str]
        email="test@example.com"  # Optional[str]
    )
    
    assert isinstance(state["correction_attempts"], int)
    assert isinstance(state["execution_result"], dict)
    assert state["error"] is None
    assert isinstance(state["email"], str)
"""
Unit tests for the workflow utilities.
"""
import pytest
import logging
from pathlib import Path
from leap.workflow.utils import (
    log_state_transition,
    get_manim_api_context,
    extract_concept,
    generate_scene_filename,
    create_temp_dir
)
from leap.core.config import GENERATED_DIR

@pytest.fixture
def sample_state():
    """Create a sample workflow state for testing."""
    return {
        "user_input": "How does gravity work?",
        "quality": "low",
        "generated_code": None
    }

def test_extract_concept():
    """Test concept extraction from user input."""
    # Test basic extraction
    assert extract_concept("How to create a circle") == "create_a_circle"
    assert extract_concept("What is gravity?") == "gravity"
    
    # Test with special characters - note that ² is preserved
    assert extract_concept("E=mc²") == "e_mc²"
    
    # Test with long input
    long_input = "explain the very very very very very very very very long concept of quantum mechanics"
    assert len(extract_concept(long_input)) <= 50
    
    # Test empty input
    assert extract_concept("") == "unknown_concept"
    assert extract_concept("   ") == "unknown_concept"

def test_generate_scene_filename():
    """Test scene filename generation."""
    filename = generate_scene_filename("How does gravity work?")
    
    # Check basic properties
    assert isinstance(filename, str)
    assert filename.endswith(".py")
    assert "gravity_work" in filename.lower()
    
    # Check path
    path = Path(filename)
    assert path.parent == GENERATED_DIR
    assert path.suffix == ".py"

def test_create_temp_dir():
    """Test temporary directory creation."""
    temp_dir = create_temp_dir()
    try:
        # Verify directory exists
        assert Path(temp_dir).exists()
        assert Path(temp_dir).is_dir()
        
        # Verify it's a temp directory (should be in system temp location)
        assert "manim_" in Path(temp_dir).name
    finally:
        # Clean up
        try:
            Path(temp_dir).rmdir()
        except:
            pass

def test_log_state_transition(caplog):
    """Test state transition logging."""
    caplog.set_level(logging.INFO)
    
    input_state = {
        "user_input": "test input",
        "quality": "low",
        "generated_code": "def test(): pass"
    }
    
    output_state = {
        "user_input": "test input",
        "quality": "high",  # Changed value
        "generated_code": "def test(): return True",  # Changed value
        "new_field": "added"  # New field
    }
    
    result = log_state_transition("test_node", input_state, output_state)
    
    # Verify log contents
    assert "Node: test_node" in caplog.text
    assert "Input State:" in caplog.text
    assert "Changes:" in caplog.text
    assert "quality: low -> high" in caplog.text
    assert "+ new_field: added" in caplog.text
    
    # Verify return value
    assert result == output_state

def test_get_manim_api_context():
    """Test getting Manim API context."""
    context = get_manim_api_context()
    
    # Basic validation
    assert isinstance(context, str)
    assert len(context) > 0
    
    # Check for actual content that we know exists in the API doc
    assert "code.styles_list" in context.lower() or "code.get_styles_list" in context.lower()
    assert "v0.19.0" in context  # Version number is present

@pytest.mark.skip(reason="Integration test - requires OpenAI API")
def test_generate_code():
    """Test code generation (integration test)."""
    pass

@pytest.mark.skip(reason="Integration test - requires Manim")
def test_execute_code():
    """Test code execution (integration test)."""
    pass 
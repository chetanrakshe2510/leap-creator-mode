"""
Unit tests for the workflow nodes.
"""
import pytest
from unittest.mock import patch, MagicMock
from leap.workflow import GraphState
from leap.workflow.nodes import (
    plan_scenes,
    generate_code,
    validate_code,
    execute_code
)
from leap.models import ManimCodeResponse

@pytest.fixture
def base_state():
    """Basic state fixture for testing."""
    return GraphState(
        user_input="How does gravity work?",
        rendering_quality="high",
        duration_detail="detailed",
        user_level="beginner",
        voice_model="en_us_001",
        plan="1. Explain gravity\n2. Show examples"
    )

@pytest.fixture
def mock_llm():
    """Mock LLM service with proper response structure."""
    mock = MagicMock()
    mock.generate_structured_response.return_value = ManimCodeResponse(
        code="""
from manim import *
from leap.templates.base_scene import ManimVoiceoverBase

class GravityScene(ManimVoiceoverBase):
    def construct(self):
        with self.voiceover(text="Let's learn about gravity") as tracker:
            text = Text('Gravity')
            self.play(Write(text), run_time=tracker.duration)
""",
        explanation="Basic gravity scene with voiceover"
    )
    return mock

@patch('leap.workflow.utils.extract_concept')
def test_plan_scenes(mock_extract_concept, base_state, mock_llm):
    """Test basic scene planning functionality."""
    mock_extract_concept.return_value = "gravity"
    
    result = plan_scenes(base_state, llm_service=mock_llm)
    
    assert isinstance(result, dict)
    assert "plan" in result
    assert result["user_input"] == base_state["user_input"]

def test_generate_code(base_state, mock_llm):
    """Test that generate_code produces code from a plan."""
    # Setup state with a plan
    base_state["plan"] = "1. Introduce gravity\n2. Show objects falling"
    
    # Call the function
    result = generate_code(base_state, llm_service=mock_llm)
    
    # Check the result
    assert "generated_code" in result
    assert result["user_input"] == base_state["user_input"]
    assert result["plan"] == base_state["plan"]

def test_validate_code(base_state):
    """Test code validation with valid Manim code."""
    base_state["generated_code"] = """
from manim import *
from leap.templates.base_scene import ManimVoiceoverBase

class GravityScene(ManimVoiceoverBase):
    def construct(self):
        with self.voiceover(text="Let's learn about gravity") as tracker:
            text = Text('Gravity')
            self.play(Write(text), run_time=tracker.duration)
"""
    
    result = validate_code(base_state)
    
    assert isinstance(result, dict)
    assert result["generated_code"] == base_state["generated_code"]
    assert not result.get("error")

@patch('leap.workflow.utils.execute_code')
def test_execute_code(mock_execute, base_state):
    """Test code execution with mocked services."""
    base_state["generated_code"] = """
from manim import *
from leap.templates.base_scene import ManimVoiceoverBase

class GravityScene(ManimVoiceoverBase):
    def construct(self):
        with self.voiceover(text="Let's learn about gravity") as tracker:
            text = Text('Gravity')
            self.play(Write(text), run_time=tracker.duration)
"""
    
    mock_execute.return_value = {
        "success": True,
        "output_file": "/path/to/file.mp4"
    }
    
    mock_file_service = MagicMock()
    mock_manim_service = MagicMock()
    
    result = execute_code(
        base_state,
        file_service=mock_file_service,
        manim_service=mock_manim_service
    )
    
    assert isinstance(result, dict)
    assert "execution_result" in result
    assert result["execution_result"]["success"]

if __name__ == "__main__":
    pytest.main() 
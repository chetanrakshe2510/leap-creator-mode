"""
Integration tests for workflow steps.
Tests the interaction between different components of the workflow.
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
from leap.models import ScenePlanResponse, ManimCodeResponse

@pytest.fixture
def basic_state():
    """Basic workflow state for testing."""
    return GraphState(
        user_input="Create a simple animation of a circle growing",
        rendering_quality="low",
        duration_detail="brief",
        user_level="normal",
        voice_model="nova"
    )

@pytest.fixture
def mock_llm():
    """Mock LLM service with proper response models."""
    mock = MagicMock()
    
    # Mock scene planning response
    mock.generate_structured_response.side_effect = lambda system_content, user_content, response_model: (
        ScenePlanResponse(plan="1. Create circle\n2. Make it grow")
        if response_model == ScenePlanResponse
        else ManimCodeResponse(
            code="""
from manim import *
from leap.templates.base_scene import ManimVoiceoverBase

class CircleGrowth(ManimVoiceoverBase):
    def construct(self):
        with self.voiceover(text="Let's watch a circle grow") as tracker:
            circle = Circle(radius=0.5)
            self.play(Create(circle), run_time=tracker.duration)
            self.play(circle.animate.scale(2))
        self.fade_out_scene()
""",
            explanation="Basic circle growth animation"
        )
    )
    return mock

def test_planning_to_code_generation(basic_state, mock_llm):
    """Test the flow from planning to code generation."""
    # 1. Plan scenes
    state_with_plan = plan_scenes(basic_state, llm_service=mock_llm)
    assert "plan" in state_with_plan
    assert isinstance(state_with_plan["plan"], str)
    assert "Create circle" in state_with_plan["plan"]
    
    # 2. Generate code
    state_with_code = generate_code(state_with_plan, llm_service=mock_llm)
    assert "generated_code" in state_with_code
    assert "ManimVoiceoverBase" in state_with_code["generated_code"]
    assert "voiceover" in state_with_code["generated_code"]

def test_code_validation_to_execution(basic_state):
    """Test the flow from code validation to execution."""
    # Setup state with valid code
    basic_state["plan"] = "1. Create circle\n2. Make it grow"
    basic_state["generated_code"] = """
from manim import *
from leap.templates.base_scene import ManimVoiceoverBase

class CircleGrowth(ManimVoiceoverBase):
    def construct(self):
        with self.voiceover(text="Let's watch a circle grow") as tracker:
            circle = Circle(radius=0.5)
            self.play(Create(circle), run_time=tracker.duration)
            self.play(circle.animate.scale(2))
        self.fade_out_scene()
"""
    
    # 1. Validate code
    validated_state = validate_code(basic_state)
    assert not validated_state.get("error")
    
    # 2. Execute code (with mocked services)
    mock_file_service = MagicMock()
    mock_manim_service = MagicMock()
    mock_manim_service.execute_manim_code.return_value = {
        "success": True,
        "output_file": "/path/to/output.mp4"
    }
    
    executed_state = execute_code(
        validated_state,
        file_service=mock_file_service,
        manim_service=mock_manim_service
    )
    
    assert "execution_result" in executed_state
    assert executed_state["execution_result"]["success"] 
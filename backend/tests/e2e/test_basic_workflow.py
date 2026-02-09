"""
End-to-end tests for the workflow.
Focuses on edge cases and input validation for alpha release.
"""
import pytest
from pathlib import Path
from leap.workflow import workflow, GraphState

@pytest.fixture
def output_dir(tmp_path):
    """Create temporary output directory."""
    return tmp_path / "outputs"

def test_edge_cases(output_dir):
    """Test edge cases that should be caught by input validation."""
    output_dir.mkdir(exist_ok=True)
    
    test_cases = [
        # Empty input
        ("", "empty"),
        # Too short input (< 10 chars)
        ("hi there", "too short"),
        # No question/topic keywords
        ("the circle is blue", "question or topic"),
        # Very long input (test boundary)
        ("Explain " * 100, "too long"),
    ]
    
    for input_text, expected_error in test_cases:
        state = GraphState(
            user_input=input_text,
            rendering_quality="low",
            duration_detail="brief",
            user_level="normal",
            voice_model="nova",
            output_file=str(output_dir / f"edge_case_{hash(input_text)}.mp4")
        )
        
        result = workflow.invoke(state)
        assert result.get("error"), f"Invalid input was accepted: {input_text}"
        assert expected_error in result["error"].lower(), f"Unexpected error for {input_text}: {result['error']}"

def test_valid_input_variations(output_dir):
    """Test various valid input formats based on regex patterns."""
    output_dir.mkdir(exist_ok=True)
    
    valid_inputs = [
        # Question mark
        "How does a circle grow in size?",
        # Explain keyword
        "Explain the concept of addition",
        # How keyword
        "How do waves move?",
        # What keyword
        "What happens when you add 2 and 2?",
        # Show keyword
        "Show me how a square transforms",
        # Demonstrate keyword
        "Demonstrate the concept of gravity",
        # Illustrate keyword
        "Illustrate how plants grow",
        # Visualize keyword
        "Visualize the water cycle",
        # Animate keyword
        "Animate a bouncing ball"
    ]
    
    for input_text in valid_inputs:
        state = GraphState(
            user_input=input_text,
            rendering_quality="low",
            duration_detail="brief",
            user_level="normal",
            voice_model="nova",
            output_file=str(output_dir / f"valid_{hash(input_text)}.mp4")
        )
        
        result = workflow.invoke(state)
        assert not result.get("error"), f"Valid input was rejected: {input_text}"
        assert result.get("generated_code"), "No code was generated"
        assert "ManimVoiceoverBase" in result["generated_code"], "Invalid code structure"

def test_simple_content(output_dir):
    """Test basic content generation for alpha."""
    output_dir.mkdir(exist_ok=True)
    
    # Focus on simple animations for alpha
    simple_prompts = [
        "How does a circle grow?",
        "Explain what is 2+2",
        "Show me a square"
    ]
    
    for prompt in simple_prompts:
        state = GraphState(
            user_input=prompt,
            rendering_quality="low",
            duration_detail="brief",
            user_level="normal",
            voice_model="nova",
            output_file=str(output_dir / f"simple_{hash(prompt)}.mp4")
        )
        
        result = workflow.invoke(state)
        assert not result.get("error"), f"Error in workflow: {result.get('error')}"
        assert result.get("generated_code"), "No code was generated"
        assert result.get("execution_result", {}).get("success"), "Execution failed" 